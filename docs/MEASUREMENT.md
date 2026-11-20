# Measurement plan

Status: **specified, not deployed.** Nothing on the live site collects anything.
This document exists so that the first optimisation decision is argued from a
defined schema rather than from an impression.

## Why it is not running

GitHub Pages serves static files. There is no process to receive a POST, so a
first-party collector has nowhere to live. The three available options and their
honest costs:

| Option | Meets the goal | Cost |
| --- | --- | --- |
| Deploy a collector on a small host (Cloudflare Worker, Fly, a VPS) | Yes, first-party | Needs a host, a domain and a deploy pipeline |
| Use a third-party analytics provider | Partly | Breaks the first-party principle; adds a cookie disclosure obligation |
| Parse GitHub Pages access logs | No | Pages does not expose per-site request logs to the repo owner |

The plan below assumes the first option, because it is the only one that keeps
the site's privacy claim true.

## The five events

Defined in `src/data/events.json`. Summary:

| ID | Event | Fires when | Answers |
| --- | --- | --- | --- |
| E1 | `page_view` | Any page renders | Which pages get reached |
| E2 | `outbound_product_click` | A reader activates a product link | Which products and positions earn the click |
| E3 | `guide_read_75` | 75% of a guide's height is reached | Whether guides are read or merely opened |
| E4 | `compare_view` | The comparison table renders | Whether readers want tabular data |
| E5 | `flag_page_view` | The review page opens | Whether the verification work is seen |

## Explicit non-goals

- **No conversion tracking on this site.** A conversion happens on Amazon. This
  site cannot observe it and must not imply that it can. Reported orders come
  only from the Associates dashboard or API.
- **No cross-site identity.** No cookie, no local storage, no fingerprint, no
  persistent identifier. Session counting uses a rotating in-memory bucket that
  is discarded on the hour.
- **No revenue model.** The campaign ledger starts empty with defined columns.
  A forecast built on zero orders is fiction with a decimal point.

## The campaign ledger

Columns: `date`, `source`, `channel`, `eligible_sessions`, `outbound_clicks`,
`reported_orders`, `provenance`.

Current row count: **0**.

Rules enforced by review, not by code (there is no code yet):

1. A row is added only from an authorised first-party report.
2. `provenance` names the report and the date it was pulled.
3. `reported_orders` is blank until the Associates report supplies it. A blank
   is information; a zero would be a claim.
4. No projection, forecast or modelled figure is permitted in any column.

## What the first real experiment should be

Not a content experiment. The one-link test:

1. Pick one product, P-01.
2. Publish exactly one outbound link for it, using the enrolled Special Link.
3. Click it from a browser with no extensions, while signed in to Associates.
4. Check that the click appears in the report, attributed to `shopnow047c-20`.
5. Only then publish the other links.

Step 4 is the pass condition. If the click does not appear, no amount of
content or design will make the site earn, and every subsequent decision is
building on sand.

## Ordering constraint

Measurement must be live before topic selection is automated. Otherwise the
"data-driven" loop is selecting topics from a table with no rows in it, which
looks rigorous and is not.
