#!/usr/bin/env python3
"""For the deployed site: drop .html from internal links (GitHub Pages serves /about for about.html)."""
import sys, os, re, glob
D = sys.argv[1]; names = {os.path.basename(f) for f in glob.glob(os.path.join(D, '*.html'))}
def fix(m):
    fn, frag = m.group(1), m.group(2) or ''
    if fn not in names: return m.group(0)
    base = './' if fn == 'index.html' else fn[:-5]
    return f'href="{base}{frag}"'
n = 0
for f in glob.glob(os.path.join(D, '*.html')):
    s = open(f, encoding='utf-8').read()
    s2, k = re.subn(r'href="([A-Za-z0-9_-]+\.html)(#[^"]*)?"', fix, s); n += k
    open(f, 'w', encoding='utf-8').write(s2)
print('clean links', n)
