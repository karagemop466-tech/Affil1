'use strict';
const button = document.getElementById('export');
button.addEventListener('click', () => {
  const decisions = Array.from(document.querySelectorAll('[data-choice]'))
    .filter(select => select.value)
    .map(select => `${select.closest('tr').querySelector('th').textContent}: ${select.value}`);
  const status = document.getElementById('decision-status');
  if (!decisions.length) {
    status.textContent = 'Select at least one decision first.';
    return;
  }
  const url = URL.createObjectURL(new Blob(['Good Measure Kitchen Notes\n\n' + decisions.join('\n') + '\n'], {type: 'text/plain'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'good-measure-decisions.txt';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  status.textContent = 'Shortlist downloaded.';
});
