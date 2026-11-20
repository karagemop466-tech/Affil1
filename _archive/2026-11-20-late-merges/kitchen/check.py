#!/usr/bin/env python3
"""Release assertions for the scoped editorial edition."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
BASE = 'https://karagemop466-tech.github.io/Affil1/kitchen/'
DISCLOSURE = 'As an Amazon Associate I earn from qualifying purchases.'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def existing(path):
    return path / 'index.html' if path.is_dir() else path


def check():
    records = json.loads((HERE/'records.json').read_text())['products']
    assert len({r['submitted'] for r in records}) == 5
    for row in records:
        assert re.fullmatch(r'https://link\.amazon/[A-Za-z0-9]{9}', row['submitted']), row
        assert re.fullmatch(r'[A-Z0-9]{10}', row['observed_asin']), row
        assert row['observed_redirect_target'] == 'https://www.amazon.com/dp/' + row['observed_asin'], row
        assert all(row[k] is None for k in ('intended_asin','official_listing_url','confirmation_date','confirmation_source','special_link')), row
    pages = list(HERE.glob('*.html'))
    assert len(pages) == 7
    indexable = set()
    evidence = set()
    for path in pages:
        content = path.read_text(encoding='utf-8')
        assert content.count(DISCLOSURE) == 2 and DISCLOSURE in content.split('<main',1)[0], path
        tag_list = Page(path).tags
        assert sum(t == 'h1' for t,_ in tag_list) == 1, path
        assert not any('data-measure' in a or 'data-special-product' in a for _,a in tag_list), path
        canonical = BASE + ('' if path.name == 'index.html' else path.name)
        assert ('link', {'rel':'canonical','href':canonical}) in tag_list, path
        if ('meta', {'name':'robots','content':'noindex,follow'}) not in tag_list:
            indexable.add(canonical)
        for tag,attrs in tag_list:
            for attr in ('href','src'):
                if attr not in attrs:
                    continue
                url = urlsplit(attrs[attr])
                if url.netloc:
                    assert attr != 'src', (path, attrs)
                    assert 'tag' not in parse_qs(url.query, keep_blank_values=True), (path, attrs)
                    if tag == 'a' and (url.hostname == 'link.amazon' or url.hostname == 'www.amazon.com'):
                        assert 'sponsored' in attrs.get('rel','').split(), (path, attrs)
                        if path.name == 'flagged.html':
                            evidence.add(attrs[attr])
                    continue
                assert not url.scheme and not url.path.startswith('/'), (path, attrs)
                target = existing(path.parent / unquote(url.path)) if url.path else path
                assert target.is_file(), (path, attrs)
                if url.fragment and target.suffix == '.html':
                    assert unquote(url.fragment) in {a.get('id') for _,a in Page(target).tags}, (path, attrs)
    assert evidence == {r[k] for r in records for k in ('submitted','observed_redirect_target')}, evidence
    site = ET.parse(HERE/'sitemap.xml')
    assert indexable == {x.text for x in site.findall('.//{*}loc')}
    for item in ET.parse(HERE/'feed.xml').findall('.//item'):
        href = item.findtext('link')
        assert href and href.startswith(BASE.removesuffix('kitchen/'))
        assert existing(HERE.parent / href.removeprefix(BASE.removesuffix('kitchen/'))).is_file(), href
    print(f'{len(pages)} pages; local links and fragments, sponsored markers, disclosure, blank confirmation fields and XML checked.')


if __name__ == '__main__':
    check()
