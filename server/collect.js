/* Aggregate-only collector for the maintained Crisp & Counter edition. */
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const browserEvents = new Set(['page_view', 'outbound_product_click', 'guide_read_75', 'compare_view', 'flag_page_view']);

function createCollector({ origin, directory }) {
  if (!origin || new URL(origin).origin !== origin || !/^https?:\/\//.test(origin) || !path.isAbsolute(directory)) {
    throw new Error('Set an exact site origin and an absolute private storage directory');
  }
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  return http.createServer({ requestTimeout: 10000 }, (req, res) => {
    const end = status => { res.statusCode = status; res.end(); };
    res.setHeader('Cache-Control', 'no-store');
    if (req.url === '/health' && req.method === 'GET') return end(204);
    if (req.url !== '/analytics/collect') return end(404);
    if (req.headers.origin !== origin) return end(403);
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
    if (req.method !== 'POST') return end(405);
    if (req.headers['sec-gpc'] === '1' || req.headers.dnt === '1') return end(204);
    if (req.headers['content-type']?.split(';')[0] !== 'text/plain') return end(415);
    let bytes = 0;
    const chunks = [];
    req.on('error', () => {});
    req.on('data', chunk => {
      bytes += chunk.length;
      if (bytes > 512) {
        if (!res.writableEnded) { res.setHeader('Connection', 'close'); end(413); }
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      if (res.writableEnded) return;
      let events;
      try { events = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
      catch { return end(400); }
      // The report import event must come from an authorized ledger, never a beacon.
      if (!Array.isArray(events) || !events.length || events.length > 10 || events.some(event => !browserEvents.has(event))) return end(400);
      try {
        const file = path.join(directory, new Date().toISOString().slice(0, 10) + '.json');
        const counts = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : {};
        for (const event of events) counts[event] = (counts[event] || 0) + 1;
        fs.writeFileSync(file + '.tmp', JSON.stringify(counts) + '\n', { mode: 0o600 });
        fs.renameSync(file + '.tmp', file);
        return end(204);
      } catch { return end(503); }
    });
  });
}

module.exports = { createCollector };
if (require.main === module) {
  createCollector({ origin: process.env.ANALYTICS_ORIGIN, directory: process.env.ANALYTICS_DIRECTORY || '' })
    .listen(Number(process.env.PORT || 8080), process.env.HOST || '127.0.0.1');
}
