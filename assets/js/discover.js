/* Local discovery only: no request, query log or persistent identifier. */
(() => {
  const desk = document.querySelector('.searchdesk');
  const open = document.querySelector('[data-find]');
  if (desk && open && typeof desk.showModal === 'function') {
    const input = desk.querySelector('input');
    const rows = [...desk.querySelectorAll('li')];
    const filter = () => {
      const words = input.value.toLowerCase().trim().split(/\s+/);
      rows.forEach(r => r.hidden = !words.every(w => r.textContent.toLowerCase().includes(w)));
      const count = rows.filter(r => !r.hidden).length;
      desk.querySelector('[role=status]').textContent = count ? `${count} matching pages` : 'No matches. Try “basket” or “guide”.';
    };
    open.hidden = false;
    open.addEventListener('click', () => {input.value = ''; filter(); desk.showModal(); input.focus();});
    input.addEventListener('input', filter);
    desk.addEventListener('click', event => {if (event.target === desk && !desk.contains(document.elementFromPoint(event.clientX,event.clientY))) desk.close();});
  }
  const tabs = document.querySelector('.shelftabs');
  if (!tabs) return;
  const select = key => {
    tabs.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === key)));
    document.querySelectorAll('[data-category]').forEach(c => c.hidden = key !== 'all' && key !== c.dataset.category);
  };
  tabs.hidden = false;
  tabs.addEventListener('click', e => {const b = e.target.closest('[data-filter]'); if (b) select(b.dataset.filter);});
  select('air-fryers');
})();
