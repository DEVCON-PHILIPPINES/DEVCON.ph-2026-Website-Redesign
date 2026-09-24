#!/usr/bin/env python3
"""Site checks for the DEVCON.ph 2026 website (runs in GitHub Actions on every pull request).

Fails the build if any page in docs/ has:
  - a broken internal link or missing #anchor
  - a link back to the old devcon.ph site (canonical/meta URLs are fine)
  - invalid schema.org JSON-LD
  - a missing or duplicate <title> / meta description
  - banned wording from the DEVCON content style guide
"""
import json, os, re, sys, html

DOCS = os.path.join(os.path.dirname(__file__), '..', 'docs')
BANNED = [(r'\bNMBLR\b', 'use "Amihan and Avtica"'),
          (r'\b13 chapters\b', 'use "13 locations"'),
          (r'Michael Lance', 'name removed by request'),
          (r'Executive AI Fluency', 'use "AI Fluency for Builders"'),
          (r'Beyond NCR', 'use "Beyond the capital"')]
MAX_PAGE_MB = 8

def visible_text(s):
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>', ' ', s, flags=re.S)
    s = re.sub(r'data:[^"\')\s]+', ' ', s)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))

def main():
    files = sorted(f for f in os.listdir(DOCS) if f.endswith('.html'))
    if not files:
        print('No pages found in docs/'); return 1
    ids = {f: set(re.findall(r'id="([^"]+)"', open(os.path.join(DOCS, f), encoding='utf-8').read())) for f in files}
    errors, titles, descs = [], {}, {}
    for f in files:
        path = os.path.join(DOCS, f)
        s = open(path, encoding='utf-8').read()
        size = os.path.getsize(path) / 1e6
        if size > MAX_PAGE_MB: errors.append(f'{f}: {size:.1f} MB is over the {MAX_PAGE_MB} MB page budget')
        body = s[s.find('<body'):]
        for h in re.findall(r'href="([^"]+)"', body):
            if re.match(r'https?://(www\.)?devcon\.ph', h): errors.append(f'{f}: links out to the old site ({h})'); continue
            if h.startswith(('http:', 'https:', 'mailto:', 'tel:', 'data:')): continue
            fn, _, frag = h.partition('#'); fn = fn or f
            if fn not in ids: errors.append(f'{f}: broken link to {h}')
            elif frag and frag not in ids[fn]: errors.append(f'{f}: missing anchor #{frag} in {fn}')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: json.loads(block)
            except ValueError as e: errors.append(f'{f}: invalid JSON-LD ({e})')
        head = s[:s.find('</head>')]
        t = re.findall(r'<title>(.*?)</title>', head); d = re.findall(r'<meta name="description" content="([^"]*)"', head)
        if len(t) != 1: errors.append(f'{f}: expected one <title>, found {len(t)}')
        else: titles.setdefault(t[0], []).append(f)
        if len(d) != 1: errors.append(f'{f}: expected one meta description, found {len(d)}')
        else: descs.setdefault(d[0], []).append(f)
        text = visible_text(s)
        for pat, fix in BANNED:
            if re.search(pat, text): errors.append(f'{f}: banned wording /{pat}/ ({fix})')
    errors += [f'duplicate <title> on {", ".join(v)}' for v in titles.values() if len(v) > 1]
    errors += [f'duplicate meta description on {", ".join(v)}' for v in descs.values() if len(v) > 1]
    print(f'Checked {len(files)} pages.')
    for e in errors: print('::error::' + e)
    if errors: print(f'{len(errors)} problem(s) found.'); return 1
    print('All checks passed.'); return 0

if __name__ == '__main__':
    sys.exit(main())
