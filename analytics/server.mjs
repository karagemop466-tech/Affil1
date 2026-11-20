// Minimal first-party event collector for Countertop Notes.
// Run on an independently deployed Node.js 20+ host; GitHub Pages cannot run this server.
import http from 'node:http';
import { appendFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const port = Number(process.env.PORT || 8787);
const host = process.env.HOST || '0.0.0.0';
const allowedOrigin = process.env.ALLOWED_ORIGIN || '';
const dataFile = resolve(process.env.EVENTS_FILE || './data/events.ndjson');
const maxBytes = 2048;
const eventTypes = new Set([
  'page_view',
  'guide_open',
  'outbound_product_click',
  'comparison_tool_use',
  'suggestion_choice'
]);
const itemPattern = /^[a-z0-9-]{1,48}$/;
const pathPattern = /^\/[a-zA-Z0-9._/-]{0,160}$/;

function send(res, status, body, origin) {
  const headers = {'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
  if (origin && origin === allowedOrigin) {
    headers['Access-Control-Allow-Origin'] = allowedOrigin;
    headers['Vary'] = 'Origin';
  }
  res.writeHead(status, headers);
  res.end(JSON.stringify(body));
}

async function readBody(req) {
  let body = '';
  for await (const chunk of req) {
    body += chunk;
    if (Buffer.byteLength(body) > maxBytes) throw new Error('too_large');
  }
  return body;
}

const server = http.createServer(async (req, res) => {
  const origin = req.headers.origin || '';
  if (req.method === 'OPTIONS' && req.url === '/events') {
    if (origin !== allowedOrigin || !allowedOrigin) return send(res, 403, {error:'origin_not_allowed'}, origin);
    res.writeHead(204, {'Access-Control-Allow-Origin':allowedOrigin,'Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type','Access-Control-Max-Age':'600','Vary':'Origin'});
    return res.end();
  }
  if (req.method === 'GET' && req.url === '/health') return send(res, 200, {ok:true}, origin);
  if (req.method !== 'POST' || req.url !== '/events') return send(res, 404, {error:'not_found'}, origin);
  if (!allowedOrigin || origin !== allowedOrigin) return send(res, 403, {error:'origin_not_allowed'}, origin);
  if (!/^text\/plain(?:;|$)/i.test(req.headers['content-type'] || '')) return send(res, 415, {error:'text_plain_required'}, origin);

  let payload;
  try { payload = JSON.parse(await readBody(req)); }
  catch (err) { return send(res, err.message === 'too_large' ? 413 : 400, {error:err.message === 'too_large' ? 'payload_too_large' : 'invalid_json'}, origin); }
  if (!payload || Object.keys(payload).some(key => !['event','path','item'].includes(key)) || !eventTypes.has(payload.event) || typeof payload.path !== 'string' || !pathPattern.test(payload.path) || payload.path.includes('..')) return send(res, 400, {error:'invalid_event'}, origin);
  if (payload.item !== undefined && (typeof payload.item !== 'string' || !itemPattern.test(payload.item))) return send(res, 400, {error:'invalid_item'}, origin);

  // Deliberately store no IP address, user agent, referrer, cookies, raw query, or client timestamp.
  // The event log contains only an allowlisted event, sanitized path, optional item code, and server time.
  const row = {event:payload.event, path:payload.path, ...(payload.item ? {item:payload.item} : {}), received_at:new Date().toISOString()};
  try {
    await mkdir(dirname(dataFile), {recursive:true});
    await appendFile(dataFile, `${JSON.stringify(row)}\n`, {encoding:'utf8', mode:0o600});
  } catch (_) { return send(res, 500, {error:'storage_unavailable'}, origin); }
  return send(res, 202, {accepted:true}, origin);
});

server.listen(port, host, () => console.log(`Countertop Notes event endpoint listening on ${host}:${port}`));
