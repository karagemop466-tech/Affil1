/* Self-hosted counting only. The static Pages build has no collector. */
(() => {
 if (!window.CC_COUNTER || navigator.doNotTrack === '1' || navigator.globalPrivacyControl) return;
 const page = new URL(document.querySelector('[rel=canonical]').href).pathname.replace(/^\/Affil1\//,'').replace(/(^|\/)$/, '$1index.html');
 const send = (event, asin='') => fetch('/api/e', {method:'POST',body:JSON.stringify([event,page,asin]),credentials:'omit',referrerPolicy:'no-referrer',keepalive:true}).catch(()=>{});
 send('page_view');
 if(page==='compare/index.html') send('compare_view');
 if(page==='review/index.html') send('flag_page_view');
 if(/^guides\/(?!index)/.test(page)) {
   const read=()=>{if(scrollY+innerHeight>=document.documentElement.scrollHeight*.75){send('guide_read_75');removeEventListener('scroll',read)}};
   addEventListener('scroll',read,{passive:true});read();
 }
 document.addEventListener('click',e=>{const a=e.target.closest('a[rel~=sponsored]');if(a) send('outbound_product_click',a.href.match(/\/dp\/(\w{10})/)?.[1]||'')});
})();
