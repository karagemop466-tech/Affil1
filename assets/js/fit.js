/* Progressive enhancement: no script leaves all three formats readable. */
(() => {
  'use strict';
  const form = document.getElementById('fit-form');
  if (!form) return;
  const heading = document.getElementById('fit-heading');
  const status = document.getElementById('fit-status');
  const results = [...document.querySelectorAll('[data-fit-result]')];
  function update() {
    const selected = form.querySelector('input:checked')?.value;
    const match = results.find(result => result.dataset.fitResult === selected);
    for (const result of results) result.hidden = Boolean(match && result !== match);
    heading.textContent = match ? 'Your starting point' : 'Three routes to a shortlist';
    status.textContent = match ? match.querySelector('h3').textContent + '. See the checklist below.' : '';
  }
  form.hidden = false;
  form.addEventListener('change', update);
  window.addEventListener('pageshow', update);
  update();
})();
