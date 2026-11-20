/* Site configuration for the tracker.
 *
 * The collector is NOT deployed by default. The tracker probes the health endpoint
 * once per session and disables itself if the endpoint does not answer, so the site
 * never pretends to collect something it is not collecting.
 *
 * Set `collector.deployed` to true only after the endpoint is live AND the privacy
 * notice (gate row G-10) has been written against the deployed behaviour.
 */
window.GM_SITE = {
  siteName: 'Good Measure Kitchen',
  siteId: 'gmk-01',
  collector: {
    endpoint: '/api/collect',
    healthPath: '/health',
    deployed: false,
    timeoutMs: 2500,
    maxQueue: 20
  },
  tracking: {
    /* Supplied by the site owner. Enrollment on an Associates account is not
       independently confirmed - see FLG-003 on the flagged-for-review page. */
    associatesTag: 'shopnow047c-20',
    /* Events recorded by the tracker. Nothing else is collected. */
    events: ['page_view', 'outbound_click', 'guide_open', 'search_query_referral', 'report_import'],
    /* Search engines recognised for the search_query_referral event. */
    searchEngines: ['google.', 'bing.', 'duckduckgo.', 'yahoo.', 'ecosia.', 'brave.', 'startpage.', 'qwant.']
  }
};
