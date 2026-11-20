#!/usr/bin/env python3
"""Check relative HTML file references in everything the host actually serves.

_archive is not served (GitHub Pages skips any path segment starting with an
underscore), so its internal links are history, not breakage. The six working
directories are underscore-prefixed for the same reason.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {'.git', '_archive', 'node_modules', '__pycache__',
           '.venv', 'build', 'dist'}
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.refs.append((attrs[attr], self.getpos()[0]))

def main():
    errors = []
    pages = [p for p in ROOT.rglob('*.html') if not EXCLUDE.intersection(p.relative_to(ROOT).parts)]
    for page in pages:
        parser = Parser()
        parser.feed(page.read_text(encoding='utf-8'))
        for ref, line in parser.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
                continue
            target = page.parent / unquote(url.path)
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{page.relative_to(ROOT)}:{line}: {ref}')
    print(f'Checked relative file references in {len(pages)} pages; {len(errors)} broken')
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
