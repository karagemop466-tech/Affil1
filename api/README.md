# Analytics collector

A self-hosted, privacy-preserving collector for the five events this site defines:
`page_view`, `outbound_click`, `guide_open`, `search_query_referral`, `report_import`.

Two interchangeable implementations, same contract:

| File | Shape | Storage |
| --- | --- | --- |
| `collect.js` | Zero-dependency Node HTTP server | newline-delimited JSON on disk |
| `worker.js` | Cloudflare Worker / Pages Function | KV namespace binding |

## Contract

```
GET  /api/collect/health   -> 200 {"ok":true,"service":"good-measure-collector",...}
POST /api/collect          -> 202 {"ok":true}
```

The browser tracker probes `/health` once per session. If it does not answer, the tracker
disables itself and sets `data-collector="inactive"` on the root element, so the site never
implies measurement that is not happening.

## What is collected

| Field | When | Notes |
| --- | --- | --- |
| `event` | always | one of the five defined events |
| `path` | always | page path only; the query string is stripped |
| `ts` | always | epoch milliseconds |
| `day` | always | UTC date, for daily aggregates |
| `vhash` | always | truncated SHA-256 of the salted IP address. The salt rotates daily by including the date in the hash input, so the value cannot be joined across days. The IP address itself is never stored. |
| `ref` | `search_query_referral` | referring host only |
| `q` | `search_query_referral` | the search term, only when the landing URL carried it |
| `target` | `outbound_click` | destination host only. Never the query string, because a Special Link's query string carries the tracking tag. |
| `guide` | `guide_open` | the guide id |
| `label` | `outbound_click` | short truncated text of the clicked link |
| `report`, `period` | `report_import` | report file name and the period it covers |

## What is never collected

Cookies, localStorage keys, advertising identifiers, fingerprint data, user agents, full
referrer URLs, outbound query strings, and any request field not on the list above.

Retention is 90 days by default (`RETENTION_DAYS`). Old entries are pruned on write.

## Deploying

### Node

```bash
export ANALYTICS_SALT="$(openssl rand -hex 32)"
export ANALYTICS_DATA_DIR=/var/lib/gmk-analytics
node api/collect.js
```

Put it behind a reverse proxy on the same origin as the site, and route `/api/collect` to it.
Set `window.GM_SITE.collector.deployed = true` in `assets/site-config.js` once it answers.

### Cloudflare

Create a KV namespace, bind it as `ANALYTICS`, set a secret `ANALYTICS_SALT`, and deploy
`worker.js` as a Pages Function at `/api/collect`.

## Before you switch it on

Gate rows **G-09** and **G-10** in the publishing gate are human checks and both are still
pending. Write the privacy notice against the deployed collector's actual behaviour, not
against its intended behaviour. The Amazon Associates IP License requires accurate and adequate
disclosure of the use of cookies, pixels and other technologies and of how visitor data is
collected, used, stored and disclosed.
