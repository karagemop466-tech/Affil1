const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { once } = require('node:events');
const { createCollector } = require('./collect');

test('collector persists only allowed daily counts', async t => {
  const origin = 'https://example.com';
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'cc-analytics-'));
  const server = createCollector({ origin, directory }).listen(0, '127.0.0.1');
  t.after(async () => {
    server.close();
    server.closeAllConnections();
    await fs.rm(directory, { recursive: true, force: true });
  });
  await once(server, 'listening');
  const url = `http://127.0.0.1:${server.address().port}/analytics/collect`;
  async function post(body, headers) {
    return (await fetch(url, { method: 'POST', headers: { origin, ...headers }, body })).status;
  }
  assert.equal(await post('["page_view"]', { origin: 'https://other.example' }), 403);
  assert.equal(await post('["page_view"]', { 'sec-gpc': '1' }), 204);
  assert.equal(await post('["page_view"]', { dnt: '1' }), 204);
  assert.equal(await post('["page_view"]', { 'content-type': 'application/json' }), 415);
  assert.equal(await post('x'.repeat(513)), 413);
  assert.equal(await post('["page_view",{"referrer":"private"}]'), 400);
  assert.equal(await post('["report_import"]'), 400);
  assert.deepEqual(await fs.readdir(directory), []);
  assert.equal(await post('["page_view","guide_read_75","compare_view","flag_page_view","outbound_product_click"]'), 204);
  assert.equal(await post('["outbound_product_click"]'), 204);
  const [file] = await fs.readdir(directory);
  assert.match(file, /^\d{4}-\d{2}-\d{2}\.json$/);
  assert.deepEqual(JSON.parse(await fs.readFile(path.join(directory, file))), {
    page_view: 1, guide_read_75: 1, compare_view: 1, flag_page_view: 1, outbound_product_click: 2
  });
});
