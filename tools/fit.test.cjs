const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

test('fit finder shows all formats until a choice then updates on keyboard-compatible change', () => {
  const keys = ['one', 'two', 'tray'];
  const results = keys.map(k => ({dataset: {fitResult:k}, hidden:false, querySelector: () => ({textContent:k})}));
  let selected;
  let change;
  let pageshow;
  const heading = {};
  const status = {};
  const form = {hidden:true, querySelector: () => selected ? {value:selected} : null,
    addEventListener(type, fn) { assert.equal(type, 'change'); change = fn; }};
  const document = {getElementById: id => ({'fit-form':form,'fit-heading':heading,'fit-status':status})[id],
    querySelectorAll: () => results};
  const window = {addEventListener(type, fn) { assert.equal(type, 'pageshow'); pageshow = fn; }};
  vm.runInNewContext(readFileSync(join(__dirname, '../assets/js/fit.js'), 'utf8'), {document,window});
  assert.equal(form.hidden, false);
  assert.equal(heading.textContent, 'Three routes to a shortlist');
  assert.deepEqual(results.map(x => x.hidden), [false,false,false]);
  for (const key of keys) {
    selected = key;
    change();
    assert.equal(heading.textContent, 'Your starting point');
    assert.deepEqual(results.map(x => x.hidden), keys.map(k => key !== k));
    assert.match(status.textContent, new RegExp(`^${key}\\.`));
  }
  selected = undefined;
  pageshow();
  assert.deepEqual(results.map(x => x.hidden), [false,false,false]);
  assert.equal(status.textContent, '');
});
