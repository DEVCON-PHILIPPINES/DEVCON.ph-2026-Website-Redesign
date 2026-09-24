#!/usr/bin/env python3
"""Harden built HTML files: strict Content-Security-Policy (hash-pinned inline scripts),
referrer policy, and a frame-buster. Idempotent: re-running recomputes hashes."""
import sys, os, re, hashlib, base64, glob
FRAMEBUST = "<script>/* anti-clickjacking */if(window.top!==window.self){document.documentElement.style.display='none';try{window.top.location.replace(window.location.href);}catch(e){}}</script>"
BASE = ("default-src 'none'; script-src 'self' {hashes}; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com data:; img-src 'self' data:; "
        "frame-src https://www.openstreetmap.org https://docs.google.com https://accounts.google.com; "
        "connect-src 'self'; manifest-src 'self'; media-src 'self' data:; base-uri 'none'; form-action 'none'; object-src 'none'; "
        "upgrade-insecure-requests")
def harden(html):
    html = re.sub(r'\s*<meta http-equiv="Content-Security-Policy"[^>]*>', '', html)
    html = re.sub(r'\s*<meta name="referrer"[^>]*>', '', html)
    html = re.sub(r'<script>/\* anti-clickjacking \*/.*?</script>\n?', '', html, flags=re.S)
    if True:
        html = re.sub(r'(<meta charset="[^"]*"\s*/?>)', r'\1\n' + FRAMEBUST.replace('\\', '\\\\'), html, count=1)
    hashes = []
    for m in re.finditer(r'<script(?P<a>[^>]*)>(?P<b>.*?)</script>', html, re.S):
        a = m.group('a')
        if 'src=' in a or 'application/ld+json' in a: continue
        h = base64.b64encode(hashlib.sha256(m.group('b').encode('utf-8')).digest()).decode()
        hashes.append(f"'sha256-{h}'")
    csp = BASE.format(hashes=' '.join(sorted(set(hashes))))
    meta = f'<meta http-equiv="Content-Security-Policy" content="{csp}">\n<meta name="referrer" content="strict-origin-when-cross-origin">'
    html = re.sub(r'(<meta charset="[^"]*"\s*/?>)', lambda m: m.group(1) + '\n' + meta, html, count=1)
    assert 'Content-Security-Policy' in html, 'no <meta charset> found'
    return html
if __name__ == '__main__':
    files = []
    for p in sys.argv[1:]: files += glob.glob(os.path.join(p, '*.html')) if os.path.isdir(p) else [p]
    for f in files:
        s = open(f, encoding='utf-8').read(); open(f, 'w', encoding='utf-8').write(harden(s))
    print('hardened', len(files), 'files')
