/* Cloudflare Worker / Pages Function version of the collector.
 *
 * Same contract as api/collect.js:
 *   GET  /api/collect/health  -> { ok: true, ... }
 *   POST /api/collect         -> { ok: true }
 *
 * Storage is a KV namespace binding named ANALYTICS. The namespace holds one JSON
 * object per day, keyed by the UTC date, so retention is a matter of deleting old
 * keys and the daily salt makes the visitor hash unjoinable across days.
 *
 * Bindings expected:
 *   env.ANALYTICS  KV namespace
 *   env.ANALYTICS_SALT  secret string
 */

const ALLOWED_EVENTS = [
  'page_view',
  'outbound_click',
  'guide_open',
  'search_query_referral',
  'report_import'
];

const MAX_FIELD = {
  path: 300, ref: 120, q: 120, target: 120, guide: 120, label: 80, report: 120, period: 60
};

function cleanString(value, max) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, max);
}

/* A URL is reduced to its host before it is stored. The browser tracker already
   reduces the referrer and the outbound target to a host before sending, so a
   bare host name has to be accepted as well as a full URL. */
function hostOnly(value) {
  const v = cleanString(value, 400);
  if (!v) return '';
  if (/^[a-z0-9.-]+$/i.test(v)) {
    return v.toLowerCase().slice(0, MAX_FIELD.ref);
  }
  try {
    return new URL(v).hostname.toLowerCase().slice(0, MAX_FIELD.ref);
  } catch (e) {
    return '';
  }
}

async function sha256Hex(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff'
    }
  });
}

function clientIp(request) {
  const h = request.headers.get('cf-connecting-ip');
  if (h) return h;
  return request.headers.get('x-forwarded-for') || '';
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  if (request.method === 'GET' && url.pathname.endsWith('/health')) {
    return json({ ok: true, service: 'good-measure-collector', events: ALLOWED_EVENTS }, 200);
  }

  if (request.method !== 'POST' || !url.pathname.endsWith('/collect')) {
    return json({ ok: false, error: 'not found' }, 404);
  }

  let payload;
  try {
    payload = await request.json();
  } catch (e) {
    return json({ ok: false, error: 'invalid json' }, 400);
  }

  const event = cleanString(payload.event, 40);
  if (!ALLOWED_EVENTS.includes(event)) return json({ ok: false, error: 'rejected' }, 400);

  const ts = Number(payload.ts) || Date.now();
  const day = new Date(ts).toISOString().slice(0, 10);
  const salt = env.ANALYTICS_SALT || 'change-me-before-deploying';
  const ip = clientIp(request);
  const vhash = ip ? (await sha256Hex(salt + '|' + day + '|' + ip)).slice(0, 16) : '';

  const record = {
    event,
    ts,
    day,
    path: cleanString(payload.path, MAX_FIELD.path).split('?')[0],
    ref: '',
    q: '',
    target: '',
    guide: cleanString(payload.guide, MAX_FIELD.guide),
    label: cleanString(payload.label, MAX_FIELD.label),
    report: cleanString(payload.report, MAX_FIELD.report),
    period: cleanString(payload.period, MAX_FIELD.period),
    vhash
  };

  if (event === 'search_query_referral') {
    record.ref = hostOnly(payload.referrer);
    record.q = cleanString(payload.q, MAX_FIELD.q);
    if (!record.ref) return json({ ok: false, error: 'rejected' }, 400);
  }
  if (event === 'outbound_click') {
    record.target = hostOnly(payload.target);
    if (!record.target) return json({ ok: false, error: 'rejected' }, 400);
  }
  if (event === 'guide_open' && !record.guide) return json({ ok: false, error: 'rejected' }, 400);
  if (event === 'report_import' && !record.report) return json({ ok: false, error: 'rejected' }, 400);

  const key = 'day:' + day;
  const existing = (await env.ANALYTICS.get(key, 'json')) || { day, events: [] };
  existing.events.push(record);
  await env.ANALYTICS.put(key, JSON.stringify(existing));

  return json({ ok: true }, 202);
}

export default { onRequest };
