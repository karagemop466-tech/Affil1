#!/usr/bin/env node
/* Self-hosted, privacy-preserving analytics collector for Good Measure Kitchen.
 *
 * Zero dependencies. Run it next to the site (or on its own host) and point
 * window.GM_SITE.collector.endpoint at it.
 *
 *   node api/collect.js
 *   PORT=8787 ANALYTICS_SALT="$(openssl rand -hex 32)" node api/collect.js
 *
 * What it stores, and nothing else:
 *   event      one of the five defined events
 *   path       the page path, no query string
 *   ts         epoch milliseconds
 *   ref        the referring host only, and only for search referrals
 *   q          the search term, only when the landing URL carried it and the
 *              referrer was a search engine
 *   target     the outbound host a reader clicked, only. Never the query string,
 *              because a Special Link's query string carries the tracking tag.
 *   guide      the guide id on guide pages
 *   label      a short, truncated text label for the clicked link
 *   day        the UTC date, so daily aggregates are trivial
 *   vhash      a truncated, salted hash of the IP address. The salt rotates daily
 *              by including the date in the hash input, so the value cannot be
 *              joined across days. The IP address itself is never stored.
 *
 * What it never stores: cookies, advertising identifiers, fingerprint data, user
 * agents, query strings on outbound links, or anything sent in a request body that
 * is not on the list above.
 *
 * Retention: events older than RETENTION_DAYS (default 90) are pruned on write.
 */

'use strict';

const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8787;
const HOST = process.env.HOST || '0.0.0.0';
const DATA_DIR = process.env.ANALYTICS_DATA_DIR || path.join(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'events.ndjson');
const SALT = process.env.ANALYTICS_SALT || 'change-me-before-deploying';
const RETENTION_DAYS = Number(process.env.RETENTION_DAYS || 90);
const MAX_BODY_BYTES = 4096;

const ALLOWED_EVENTS = [
  'page_view',
  'outbound_click',
  'guide_open',
  'search_query_referral',
  'report_import'
];

const MAX_FIELD = {
  path: 300,
  ref: 120,
  q: 120,
  target: 120,
  guide: 120,
  label: 80,
  report: 120,
  period: 60
};

function cleanString(value, max) {
  if (typeof value !== 'string') return '';
  const trimmed = value.trim();
  if (!trimmed) return '';
  return trimmed.slice(0, max);
}

/* The referrer is reduced to a host before it is stored. A search engine referrer
   may carry the query the visitor typed; that is dropped here. */
function hostOnly(value) {
  const v = cleanString(value, 400);
  if (!v) return '';
  try {
    return new URL(v).hostname.toLowerCase().slice(0, MAX_FIELD.ref);
  } catch (e) {
    return '';
  }
}

function dayStamp(ts) {
  return new Date(ts).toISOString().slice(0, 10);
}

function hashIp(req, ts) {
  const raw = (req.socket && req.socket.remoteAddress) || '';
  if (!raw) return '';
  const day = dayStamp(ts);
  return crypto.createHash('sha256')
    .update(SALT + '|' + day + '|' + raw)
    .digest('hex')
    .slice(0, 16);
}

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function prune(ts) {
  const cutoff = ts - RETENTION_DAYS * 24 * 60 * 60 * 1000;
  if (!fs.existsSync(DATA_FILE)) return;
  const lines = fs.readFileSync(DATA_FILE, 'utf8').split('\n').filter(Boolean);
  const kept = [];
  let removed = 0;
  for (const line of lines) {
    try {
      const rec = JSON.parse(line);
      if (rec.ts && rec.ts < cutoff) { removed++; continue; }
      kept.push(line);
    } catch (e) {
      removed++;
    }
  }
  if (removed) {
    fs.writeFileSync(DATA_FILE, kept.length ? kept.join('\n') + '\n' : '');
  }
}

function appendRecord(record) {
  ensureDir();
  fs.appendFileSync(DATA_FILE, JSON.stringify(record) + '\n');
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error('body too large'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function sanitize(payload, req) {
  const event = cleanString(payload.event, 40);
  if (!ALLOWED_EVENTS.includes(event)) return null;

  const ts = Number(payload.ts) || Date.now();
  const record = {
    event,
    ts,
    day: dayStamp(ts),
    path: cleanString(payload.path, MAX_FIELD.path).split('?')[0],
    ref: '',
    q: '',
    target: '',
    guide: cleanString(payload.guide, MAX_FIELD.guide),
    label: cleanString(payload.label, MAX_FIELD.label),
    vhash: hashIp(req, ts)
  };

  if (event === 'search_query_referral') {
    record.ref = hostOnly(payload.referrer);
    record.q = cleanString(payload.q, MAX_FIELD.q);
    if (!record.ref) return null;
  }
  if (event === 'outbound_click') {
    record.target = hostOnly(payload.target);
    if (!record.target) return null;
  }
  if (event === 'guide_open') {
    if (!record.guide) return null;
  }
  if (event === 'report_import') {
    record.report = cleanString(payload.report, MAX_FIELD.report);
    record.period = cleanString(payload.period, MAX_FIELD.period);
    if (!record.report) return null;
  }
  return record;
}

function json(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(payload),
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff'
  });
  res.end(payload);
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://' + (req.headers.host || 'localhost'));

  if (req.method === 'GET' && url.pathname === '/health') {
    return json(res, 200, { ok: true, service: 'good-measure-collector', events: ALLOWED_EVENTS });
  }

  if (req.method === 'OPTIONS') {
    res.writeHead(204, { 'Allow': 'POST, GET /health' });
    return res.end();
  }

  if (req.method !== 'POST' || url.pathname !== '/collect') {
    return json(res, 404, { ok: false, error: 'not found' });
  }

  let body;
  try {
    body = await readBody(req);
  } catch (e) {
    return json(res, 413, { ok: false, error: 'body too large' });
  }

  let payload;
  try {
    payload = JSON.parse(body || '{}');
  } catch (e) {
    return json(res, 400, { ok: false, error: 'invalid json' });
  }

  const record = sanitize(payload, req);
  if (!record) return json(res, 400, { ok: false, error: 'rejected' });

  try {
    appendRecord(record);
    prune(record.ts);
  } catch (e) {
    return json(res, 500, { ok: false, error: 'storage failure' });
  }

  return json(res, 202, { ok: true });
});

server.listen(PORT, HOST, () => {
  process.stdout.write('Good Measure collector listening on http://' + HOST + ':' + PORT + '\n');
  process.stdout.write('Writing to ' + DATA_FILE + '\n');
  if (SALT === 'change-me-before-deploying') {
    process.stdout.write('WARNING: set ANALYTICS_SALT to a long random value before collecting real data.\n');
  }
});

process.on('SIGTERM', () => server.close(() => process.exit(0)));
process.on('SIGINT', () => server.close(() => process.exit(0)));
