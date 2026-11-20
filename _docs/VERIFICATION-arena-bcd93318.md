# Verification record — arena/bcd93318-affil1 · 2026-11-20 (UTC)

Scope: a line-by-line re-check of the five submitted short links, their direct `/dp/`
destinations, and the Associates Operating Agreement §5 disclosure sentence. Nothing here
changes a product value. Observations are recorded as dated observations, not as proof of
intent, attribution, or compliance.

Method: `fetch_page` (redirects followed), one fetch per URL unless noted. Product prices,
star ratings and review counts that appear on the fetched pages were **not** copied anywhere
(Program Policies: price and availability may only be shown through Amazon-served links or the
Creators/PA API). No Associates account was accessed; no tag was added or tested.

## 1. Short links, as submitted

| Ref | Submitted link | Final URL observed 2026-11-20 | Page title observed | Matches register? |
|---|---|---|---|---|
| P-01 | https://link.amazon/B04G1MEwY | https://www.amazon.com/ | Amazon.com. Spend less. Smile more. | **No** — register records `/dp/B0CDY277D3` |
| P-02 | https://link.amazon/B02NbDxp3 | https://www.amazon.com/ | Amazon.com. Spend less. Smile more. | **No** — register records `/dp/B09B7SB46R` |
| P-03 | https://link.amazon/B00hJ57DV | https://www.amazon.com/ | Amazon.com. Spend less. Smile more. | **No** — register records `/dp/B08DKYBTPH` |
| P-04 | https://link.amazon/B0c8moW59 | https://www.amazon.com/ (two separate attempts) | Amazon.com. Spend less. Smile more. | **No** — register records `/dp/B0DHZTCNR5` |
| P-05 | https://link.amazon/B0f3GKalj | https://www.amazon.com/ | Amazon.com. Spend less. Smile more. | **No** — register records `/dp/B0DZFD6R9Z` |

Reading: the short links did not reproduce the recorded destinations on this date. The cause is
not established here (see FLG-028). The register's observed redirect values for these five links
are therefore not reproducible today and must not be presented as current.

## 2. Direct `/dp/` destinations, as recorded

| Ref | Observed ASIN (register) | Final URL observed 2026-11-20 | Page title observed (root) | Result |
|---|---|---|---|---|
| P-01 | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3?lv=shuf&channelId=500&plpRedirect=mhFallback | Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows … | Resolves to the listing; `plpRedirect=mhFallback` marker present |
| P-04 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5?lv=shuf&channelId=500&plpRedirect=mhFallback | Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer … | Resolves to the listing; `plpRedirect=mhFallback` marker present |
| P-05 | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z?lv=shuf&channelId=500&plpRedirect=mhFallback&th=1 | Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer … Gen3 | Resolves to the listing; `plpRedirect=mhFallback` marker present |

P-02 and P-03 `/dp/` pages were not re-fetched in this pass.

Each fetched `/dp/` URL carries `plpRedirect=mhFallback`, which is the same marker FLG-018
describes. That is Amazon's own signal of a merchandised fallback. It is a reason to keep the
mapping labelled as an observation, not a reason to change it.

## 3. Associates Operating Agreement §5 (disclosure wording)

Source: https://affiliate-program.amazon.com/help/operating/agreement (updated October 15, 2025;
retrieved 2026-11-20, section 5 is on fetched chunk index 1, the second of four).

Verbatim text found in §5: “You must clearly and prominently state the following, or any
substantially similar statement previously allowed under this Agreement, on your Site … :
“As an Amazon Associate I earn from qualifying purchases.”

The sentence the site publishes matches this exactly. Result: **consistent with §5**.

Not re-checked in this pass: Program Policies (§2, §6(w), §6(y)) and the Commission Income
Statement. Those remain as recorded in the register and in `src/data/sources.json`.

## 4. Irregularities raised by this pass

1. **FLG-028 (high).** Short links did not reproduce their recorded destinations on 2026-11-20.
   Recorded as a flag; no observed field changed.
2. **README P-04 row contradicted the data** (said "none, no buy button"; `products.json` and the
   built product pages point to `B0DHZTCNR5`). Corrected in `README.md`.
3. **`now/` caption contradicted its table.** The caption was hard-coded to "The five high-severity flags" while the table lists every high flag (7 before this pass, 8 after). Fixed in `_tools/page_now.py`: the caption now uses the row count. No other session claimed that file.
4. **No attribution tag on any outbound link.** Unchanged from FLG-002. The tag can only be
   produced from an enrolled Associates account and a tested Special Link; neither is available
   to this session.

## 5. Not done, and why

- No Associates account, SiteStripe or Special Link was generated or tested (account access
  unavailable to this session; see FLG-002 and FLG-003).
- No click, traffic, order or revenue figure was obtained or inferred.
- P-02 and P-03 `/dp/` pages were not re-fetched, so their destination was not re-observed today.
