#!/usr/bin/env node
// Negative test for the build gate. Injects one violation at a time into a
// throwaway copy of a page and asserts the gate rejects it. This is the
// evidence behind SG-07's success measure: prove the gate catches a
// deliberately broken page rather than trusting that it would.
//
// Run with: npm run verify
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const TARGET = path.join(ROOT, "shop", "index.html");
const backup = fs.readFileSync(TARGET, "utf8");

const cases = [
  {
    name: "C01 disclosure strip removed",
    mutate: (h) => h.replace(/<div class="disclosure"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/, "").replace(/As an Amazon Associate I earn from qualifying purchases\./g, "Affiliate notice."),
  },
  {
    name: "C04 outbound link loses rel=sponsored",
    mutate: (h) => h.replace(/rel="sponsored nofollow noopener"/g, 'rel="noopener"'),
  },
  {
    name: "C03 outbound link loses the Associates tag",
    mutate: (h) => h.replace(/\?tag=shopnow047c-20/g, ""),
  },
  {
    name: "C06 a price is published",
    mutate: (h) => h.replace("Everything on the shelf", "Everything on the shelf — now $79.93"),
  },
  {
    name: "C07 a star rating is published",
    mutate: (h) => h.replace("Everything on the shelf", "Everything on the shelf — 4.2 out of 5 stars"),
  },
  {
    name: "C08 a hands-on testing claim appears",
    mutate: (h) => h.replace("Everything on the shelf", "Everything on the shelf — we tested all of them"),
  },
  {
    name: "LNK a link points at a page that does not exist",
    mutate: (h) => h.replace('href="https://karagemop466-tech.github.io/Affil1/shop/"', 'href="https://karagemop466-tech.github.io/Affil1/shop/does-not-exist/"'),
  },
];

function runGate() {
  try {
    execFileSync(process.execPath, [path.join(ROOT, "scripts", "check.mjs")], { cwd: ROOT, stdio: "pipe" });
    return { pass: true, out: "" };
  } catch (e) {
    return { pass: false, out: (e.stdout?.toString() || "") + (e.stderr?.toString() || "") };
  }
}

// Baseline must pass, otherwise the test proves nothing.
const base = runGate();
if (!base.pass) {
  console.error("Baseline gate run FAILED. Fix the site before testing the gate.");
  console.error(base.out);
  process.exit(1);
}
console.log("baseline: gate passes on the built site");

let caught = 0;
const missed = [];

for (const c of cases) {
  const mutated = c.mutate(backup);
  if (mutated === backup) {
    console.error(`  !! test "${c.name}" did not change the file — the injection is stale`);
    missed.push(c.name + " (injection stale)");
    continue;
  }
  fs.writeFileSync(TARGET, mutated, "utf8");
  const r = runGate();
  if (!r.pass) {
    caught++;
    const rule = (r.out.match(/\[([A-Z0-9]+)\]/) || [])[1] || "?";
    console.log(`  caught  ${c.name}  → rule ${rule}`);
  } else {
    missed.push(c.name);
    console.log(`  MISSED  ${c.name}`);
  }
  fs.writeFileSync(TARGET, backup, "utf8");
}

// Restore and re-verify the site is back to a passing state.
fs.writeFileSync(TARGET, backup, "utf8");
const after = runGate();

console.log("──────────────────────────────────────────────");
console.log(`${caught}/${cases.length} injected violations caught`);
if (missed.length) {
  console.error("gate gaps:");
  missed.forEach((m) => console.error("  · " + m));
}
if (!after.pass) {
  console.error("site did not return to a passing state after restore");
  process.exit(1);
}
if (caught !== cases.length) process.exit(1);
console.log("restored: site passes the gate again");
process.exit(0);
