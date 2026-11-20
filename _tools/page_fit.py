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


def _worksheet(d):
    """A printable sheet the reader fills in at the counter.

    Nothing is pre-filled: no dimension, clearance or capacity value is published
    anywhere on this site, because none was confirmed from an official
    specification sheet. The sheet holds what the reader measures and what the
    manual for the exact model states -- the only reliable source for either.
    """
    return f'''<section class="section section-tint"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Printable</p><h2>The counter fit worksheet</h2></div>
  <p>Print this, take a tape measure, and fill it in beside the manual for the exact model. Nothing is pre-filled, because no dimension on this site was confirmed from an official specification sheet.</p></div>
  <table class="worksheet">
    <caption>Space you are giving it. Write your measurement, then the number the manual requires.</caption>
    <thead><tr><th scope="col">What to measure</th><th scope="col">Your space</th><th scope="col">The manual says</th><th scope="col">Fits?</th></tr></thead>
    <tbody>
      <tr><th scope="row">Width of the free counter</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">Depth of the free counter</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">Height to the cabinet above</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">Clearance above (basket lift or door swing)</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">Clearance in front (drawer pull or door travel)</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">Distance to the nearest socket</th><td></td><td></td><td></td></tr>
    </tbody>
  </table>
  <table class="worksheet">
    <caption>What you actually cook. Measure the food, not the appliance.</caption>
    <thead><tr><th scope="col">Your usual batch</th><th scope="col">Size or count</th><th scope="col">Inside the machine</th><th scope="col">One load?</th></tr></thead>
    <tbody>
      <tr><th scope="row">The tray or pan you already use</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">Portions at a normal dinner</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">The biggest thing you would put in it</th><td></td><td></td><td></td></tr>
      <tr><th scope="row">How many separate things at once</th><td></td><td></td><td></td></tr>
    </tbody>
  </table>
  <p class="worksheet-note">Three rules for filling it in. Write &ldquo;unknown&rdquo; rather than a guess, and treat it as a reason to open the manual. Compare inside dimensions, never the quart figure on the carton. If a number is not in the manual or on the official listing, the seller has not published it, and no shop should invent it for you.</p>
  <p class="sec-foot"><a class="tlink" href="{esc(rel(d, 'guides/air-fryer-capacity-checklist.html'))}">The capacity checklist behind this sheet <span aria-hidden="true">&rarr;</span></a></p>
</div></section>'''


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
{_worksheet(d)}
<script src="{esc(rel(d, 'assets/js/fit.js'))}" defer></script>''')
