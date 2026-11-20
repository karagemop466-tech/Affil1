"""An appliance decision tool: prioritize a format, never assert a model fits."""
from layout import esc, page, rel


PATHS = (
    ('one', '01', 'One main dish at a time', 'Start with a single basket',
     'Check the flat cooking area against your usual batch. A larger volume does not tell you how many pieces fit side by side.', 'p-03'),
    ('two', '02', 'A main and a side together', 'Start with two baskets',
     'Check what fits in each side separately. Two small baskets don’t give you one large cooking surface.', 'p-01'),
    ('tray', '03', 'A tray, toast, or a small bake', 'Start with an oven-style model',
     'Measure the tray you already use, then check the usable rack dimensions and room for the doors to open.', 'p-02'),
)


def build(d):
    choices = ''.join(f'''<label class="fit-choice">
      <input name="meal" type="radio" value="{key}" aria-controls="fit-results">
      <span><small>{number}</small>{esc(label)}</span></label>'''
      for key, number, label, *_ in PATHS)
    results = ''.join(f'''<article class="fit-result" data-fit-result="{key}">
      <h3>{esc(title)}</h3><p>{esc(note)}</p>
      <a class="tlink" href="{esc(rel(d, f'products/{ref}.html'))}">See a listing example &rarr;</a></article>'''
      for key, _, _, title, note, ref in PATHS)
    return page(d, title="Air fryer fit finder — Crisp & Counter",
                description="Choose the way you cook, then check basket space, tray size and room to open the appliance before you buy.", active="fit/index.html", canonical="fit/", extra_css="assets/css/fit.css", body=f'''
<section class="fit-hero"><div class="wrap fit-hero-grid">
  <div><p class="eyebrow">The countertop edit / shopping tool</p>
  <h1>Make room for<br><em>the right air fryer.</em></h1>
  <p class="dek">A quick way to narrow the field, with a short checklist to take to the listing or manual.</p></div>
  <figure><img src="{esc(rel(d, 'assets/img/decision-tools-w900.jpg'))}" alt="A tape measure and open kitchen notebook on a wooden table" width="900" loading="eager"><figcaption>Editorial illustration</figcaption></figure>
</div></section>
<section class="section"><div class="wrap fit-grid">
  <div><form id="fit-form" hidden><fieldset><legend>What do you want it to do most often?</legend>{choices}</fieldset></form>
  <h2 id="fit-heading">Three routes to a shortlist</h2><p id="fit-status" class="fit-status" role="status"></p>
  <div id="fit-results">{results}</div>
  <p><a href="{esc(rel(d, 'compare/index.html'))}">Compare all formats side by side &rarr;</a></p></div>
  <aside class="fit-checklist"><p class="eyebrow">Before you buy</p><h2>Three things to measure</h2>
  <ol><li><strong>The spot.</strong> Measure the width, height and depth where it will sit. Compare with the manual’s clearance requirements.</li>
  <li><strong>The opening.</strong> Make sure you can pull the basket or swing the doors open without moving the appliance.</li>
  <li><strong>The meal.</strong> Check the inside dimensions against what you cook, not just the number on the carton.</li></ol>
  <p>A format is a starting point, not a confirmed fit. This tool doesn’t have verified dimensions for these models.</p>
  <a class="tlink" href="{esc(rel(d, 'guides/cleanup-and-counter-space.html'))}">Read the counter-space guide &rarr;</a></aside>
</div></section>
<script src="{esc(rel(d, 'assets/js/fit.js'))}" defer></script>''')
