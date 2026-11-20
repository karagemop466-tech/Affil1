(function(){
  const grid = document.getElementById('product-grid');
  if (!grid) return;

  (window.PRODUCTS || []).forEach((p) => {
    const card = document.createElement('article');
    card.className = 'product-card';

    const number = document.createElement('span');
    number.className = 'product-number';
    number.textContent = '0' + p.id;

    const title = document.createElement('h3');
    title.textContent = 'Submitted code ' + p.submittedCode;

    const chip = document.createElement('span');
    chip.className = 'product-chip unverified';
    chip.textContent = (p.status === 'unresolved' ? 'UNRESOLVED' : (p.passesAgreed ? 'OBSERVED · UNCONFIRMED' : 'CONFLICT LOGGED'));

    const desc = document.createElement('p');
    desc.textContent = p.observedTarget
      ? 'Observed listing: ' + p.observedTarget + ' (single point-in-time evidence, not an endorsement).'
      : 'Destination not observed — Amazon bot checkpoint on both passes.';

    const note = document.createElement('p');
    note.className = 'quiet';
    note.style.fontSize = '0.78rem';
    note.textContent = p.note;

    const link = document.createElement('a');
    link.href = p.submitted;
    link.target = '_blank';
    link.rel = 'sponsored nofollow noopener';
    link.textContent = 'Check listing →';
    link.setAttribute('aria-label', 'Open submitted Amazon link ' + p.id + '; destination is unverified');
    link.className = 'text-link';

    card.append(number, title, chip, desc, note, link);
    grid.appendChild(card);
  });
})();