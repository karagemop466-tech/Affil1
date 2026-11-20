/* Opt-in first-party counters. Never set the flag on static GitHub Pages. */
(() => {
  "use strict";
  if (window.CC_ANALYTICS_ENABLED !== true || navigator.globalPrivacyControl ||
      navigator.doNotTrack === "1" || window.doNotTrack === "1") return;
  const script = document.currentScript;
  const base = new URL("../../", script.src);
  if (base.origin !== location.origin || !location.pathname.startsWith(base.pathname)) return;
  const page = location.pathname.slice(base.pathname.length).replace(/(^|\/)index\.html$/, "$1");
  function track(event, product = null) {
    fetch("/api/e", {
      method: "POST", keepalive: true, credentials: "omit", referrerPolicy: "no-referrer",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify([{event, page, product}])
    }).catch(() => {});
  }
  track("page_view");
  if (page === "compare/") track("compare_view");
  if (page === "review/") track("flag_page_view");
  if (/^guides\/[^/]+\.html$/.test(page)) {
    const main = document.querySelector("main");
    function checkDepth() {
      if (!main) return;
      const box = main.getBoundingClientRect();
      if (box.height > 0 && box.bottom > 0 && box.top + box.height * 0.75 <= innerHeight) {
        removeEventListener("scroll", checkDepth);
        removeEventListener("resize", checkDepth);
        track("guide_read_75");
      }
    }
    addEventListener("scroll", checkDepth, {passive: true});
    addEventListener("resize", checkDepth);
    checkDepth();
  }
  function recordClick(event) {
    const a = event.target.closest?.("a[rel~='sponsored']");
    if (!a) return;
    const url = new URL(a.href);
    const match = /^\/dp\/([A-Z0-9]{10})(?:\/|$)/.exec(url.pathname);
    if (url.origin === "https://www.amazon.com" && match) track("outbound_product_click", match[1]);
  }
  document.addEventListener("click", recordClick);
  document.addEventListener("auxclick", event => { if (event.button === 1) recordClick(event); });
})();
