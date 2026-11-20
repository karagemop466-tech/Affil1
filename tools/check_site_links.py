#!/usr/bin/env python3
"""Check relative references in published HTML and same-site sitemap/feed URLs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://karagemop466-tech.github.io/Affil1/'
errors = []

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        self.refs.extend(v for k, v in attrs if k in ('href', 'src') and v)

def check(page, ref):
    url = urlsplit(ref)
    if url.scheme or url.netloc or not url.path:
        return
    if url.path.startswith('/'):
        errors.append(f'{page}: root-absolute reference {ref}')
        return
    target = (page.parent / unquote(url.path)).resolve()
    if not target.is_relative_to(ROOT) or not target.exists():
        errors.append(f'{page}: missing {ref}')
    elif target.is_dir() and not (target / 'index.html').is_file():
        errors.append(f'{page}: directory has no index: {ref}')

pages = [p for p in ROOT.rglob('*.html') if not any(x in p.parts for x in ('.git', 'archive', 'node_modules'))]
for page in pages:
    parser = Links()
    parser.feed(page.read_text(encoding='utf-8'))
    for ref in parser.refs:
        check(page, ref)
for name in ('sitemap.xml', 'feed.xml', 'rss.xml'):
    xml = ET.parse(ROOT / name)
    for element in xml.iter():
        text = (element.text or '').strip()
        if text.startswith(SITE):
            check(ROOT / name, text[len(SITE):])
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Validated local references in {len(pages)} published HTML pages and 3 XML files.')
