'use strict';
// The dynamic host sets this flag only after its privacy review. Pages never sets it.
(() => {
  if (document.documentElement.dataset.measure !== 'on' || navigator.globalPrivacyControl ||
      navigator.doNotTrack === '1' || window.doNotTrack === '1') return;
  const {page, kind} = document.body.dataset;
  const send = (event, product) => {
    const data = product ? {event, page, product} : {event, page};
    fetch('/api/e', {method: 'POST', body: JSON.stringify(data), keepalive: true,
      credentials: 'omit', referrerPolicy: 'no-referrer',
      headers: {'Content-Type': 'application/json'}}).catch(() => {});
  };
  send('page_view');
  if (kind === 'compare') send('compare_view');
  if (kind === 'flag') send('flag_page_view');
  if (kind === 'guide') {
    const article = document.querySelector('article');
    if (article) {
      const check = () => {
        const {top, height} = article.getBoundingClientRect();
        if (top + height * 0.75 <= innerHeight) {
          send('guide_read_75');
          removeEventListener('scroll', check);
          removeEventListener('resize', check);
        }
      };
      addEventListener('scroll', check, {passive: true});
      addEventListener('resize', check);
      check();
    }
  }
  const productClick = event => {
    if ((event.type === 'auxclick' && event.button !== 1) || event.defaultPrevented) return;
    const link = event.target.closest('a[data-special-product][href]');
    if (!link || !link.relList.contains('sponsored')) return;
    send('outbound_product_click', link.dataset.specialProduct);
  };
  document.addEventListener('click', productClick, {passive: true});
  document.addEventListener('auxclick', productClick, {passive: true});
})();
