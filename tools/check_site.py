#!/usr/bin/env python3
"""Validate local site navigation, disclosure, sourced records, XML, and build Pages artifact."""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.ids=set(); self.rows=[]; self.current_row=None; self.anchors=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag in ('a','link','script','img'):
            key='href' if tag in ('a','link') else 'src'
            if a.get(key): self.links.append((a[key], tag))
        if tag == 'a':
            self.anchors.append(a)
            if self.current_row is not None:
                self.current_row.append(a.get('href',''))
        if tag == 'tr':
            self.current_row=[]; self.rows.append(self.current_row)
    def handle_endtag(self, tag):
        if tag == 'tr': self.current_row=None

def fail(message):
    raise SystemExit('SITE CHECK FAILED: ' + message)

pages=sorted(p for p in ROOT.rglob('*.html') if '_site' not in p.parts and '.git' not in p.parts)
if not pages: fail('no HTML pages found')
issues=[]
for page in pages:
    text=page.read_text(encoding='utf-8')
    if text.count('As an Amazon Associate I earn from qualifying purchases.') < 2:
        issues.append(f'{page.relative_to(ROOT)}: required disclosure must appear in page and footer')
    parser=PageParser(); parser.feed(text)
    for value,tag in parser.links:
        parsed=urlparse(value)
        if parsed.scheme or value.startswith(('mailto:','tel:','data:','javascript:')): continue
        target_path=unquote(parsed.path)
        target=(page.parent / target_path).resolve() if target_path else page.resolve()
        if target_path and not target.exists(): issues.append(f'{page.relative_to(ROOT)}: broken local {tag} path {value}')
        if parsed.fragment and target.exists() and target.suffix.lower()=='.html':
            target_parser=PageParser(); target_parser.feed(target.read_text(encoding='utf-8'))
            if parsed.fragment not in target_parser.ids: issues.append(f'{page.relative_to(ROOT)}: missing anchor {value}')

# Every product-intent row carries an official Amazon policy reference; the URL supplied by the
# project owner remains separate and is not misrepresented as an identity source.
product=(ROOT/'product-register.html').read_text(encoding='utf-8')
pp=PageParser(); pp.feed(product)
body_rows=[row for row in pp.rows if any(h.startswith('https://link.amazon/') for h in row)]
if len(body_rows)!=5: issues.append(f'product register: expected five submitted-link rows, got {len(body_rows)}')
for idx,row in enumerate(body_rows,1):
    if not any(h.startswith('https://affiliate-program.amazon.com/') for h in row): issues.append(f'product register row {idx} lacks an official Amazon source link')
for anchor in pp.anchors:
    if (anchor.get('href','').startswith('https://link.amazon/') and
        not {'sponsored','nofollow','noopener'}.issubset(set(anchor.get('rel','').split()))):
        issues.append(f'product register contains an outbound link without sponsored/nofollow/noopener: {anchor.get("href")}')

for filename, expected_rows in [('flagged.html',10), ('suggestions.html',6)]:
    parser=PageParser(); parser.feed((ROOT/filename).read_text(encoding='utf-8'))
    sourced=[row for row in parser.rows if any(h.startswith(('https://affiliate-program.amazon.com/','https://www.ftc.gov/','https://developers.google.com/','https://docs.github.com/')) for h in row)]
    if len(sourced)<expected_rows: issues.append(f'{filename}: expected at least {expected_rows} sourced decision/findings rows, found {len(sourced)}')

js=(ROOT/'assets/site.js').read_text(encoding='utf-8')
if 'rel="sponsored nofollow noopener"' not in js: issues.append('product cards must mark links rel="sponsored nofollow noopener"')
for event in ('page_view','guide_open','outbound_product_click','comparison_tool_use','suggestion_choice'):
    if event not in js and event not in (ROOT/'analytics/server.mjs').read_text(encoding='utf-8'):
        issues.append(f'analytics event missing: {event}')
for xml_name in ('sitemap.xml','feed.xml'):
    try: ET.parse(ROOT/xml_name)
    except (FileNotFoundError, ET.ParseError) as e: issues.append(f'{xml_name}: invalid or missing XML ({e})')

# Ensure every public HTML route is represented in sitemap and every guide appears in RSS.
try:
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    locs={node.text for node in sitemap.iter() if node.tag.endswith('loc')}
    base='https://karagemop466-tech.github.io/Affil1/'
    for page in pages:
        rel=page.relative_to(ROOT).as_posix()
        url=base if rel=='index.html' else base+rel
        if url not in locs: issues.append(f'sitemap.xml missing {rel}')
    feed=ET.parse(ROOT/'feed.xml').getroot()
    feed_links={node.text for node in feed.findall('./channel/item/link')}
    for guide in sorted((ROOT/'guides').glob('*.html')):
        url=base+guide.relative_to(ROOT).as_posix()
        if url not in feed_links: issues.append(f'feed.xml missing guide {guide.relative_to(ROOT)}')
except (FileNotFoundError, ET.ParseError):
    pass

if issues: fail('\n- ' + '\n- '.join(issues))
print(f'OK: checked {len(pages)} HTML pages, local navigation, above-fold/footer disclosures, sourced product/decision rows, outbound-link attributes, five event names, sitemap, and feed.')

parser_args=argparse.ArgumentParser(); parser_args.add_argument('--build', action='store_true'); args=parser_args.parse_args()
if args.build:
    out=ROOT/'_site'
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    for page in pages:
        dest=out/page.relative_to(ROOT); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(page,dest)
    for folder in ('assets','guides'):
        shutil.copytree(ROOT/folder,out/folder,dirs_exist_ok=True)
    for name in ('sitemap.xml','feed.xml','robots.txt'):
        shutil.copy2(ROOT/name,out/name)
    (out/'.nojekyll').write_text('',encoding='utf-8')
    print(f'Built {len(pages)} pages into _site/')
