#!/usr/bin/env python3
"""Deploy layout for GitHub Pages (and later devcon.ph):
  * every page lives at /<slug>/index.html, the same trailing-slash URLs devcon.ph uses (/manila/, /about/)
  * /<slug>.html (links shared from earlier previews) redirect to /<slug>/
  * every known old devcon.ph URL that changed redirects to its new home
  * 404.html resolves anything else (old news posts, feeds, typos) to the closest page
Usage: restructure.py <flat_pages_dir> <out_docs_dir>
"""
import sys, os, re, shutil, glob, html, json

SRC, OUT = sys.argv[1], sys.argv[2]

# Old devcon.ph paths (and common aliases) -> new slug (+ optional #anchor). '' = homepage.
REDIRECTS = {
    # renamed pages and old campaign/news URLs
    'she-2026': 'sheisdevcon', 'she': 'sheisdevcon', 'she-is-devcon': 'sheisdevcon', 'women-in-tech': 'sheisdevcon',
    'campussummit2023': 'case-study-campus-devcon-summit', 'campus-summit-2023': 'case-study-campus-devcon-summit', 'campus-summit': 'case-study-campus-devcon-summit',
    'prosummit2023': 'case-study-pro-summit', 'pro-summit-2023': 'case-study-pro-summit', 'prosummit': 'pro-summit',
    'summergiveaway2023': 'case-study-zoho-creator', 'summer-giveaway-2023': 'case-study-zoho-creator', 'zoho-creator': 'case-study-zoho-creator',
    'ai-fluency': 'ai-fluency-masterclass', 'agentic-training': 'ai-fluency-masterclass', 'agentic-training-for-leaders': 'ai-fluency-masterclass',
    'programs/ai-fluency-masterclass': 'ai-fluency-masterclass', 'programs/agentic-training': 'ai-fluency-masterclass', 'ai-fluency-agentic-training': 'ai-fluency-masterclass', 'ai-fluency-for-builders': 'ai-fluency-masterclass', 'masterclass': 'ai-fluency-masterclass',
    'sui-and-devcon-philippines-launch-build-beyond-developer-events-and-code-camps': 'case-study-sui', 'sui': 'case-study-sui', 'build-beyond': 'case-study-sui',
    '2025-news-isla-camp-ph-and-devcon-ph-renew-partnership-for-nationwide-smart-contracts-code-camps-and-emerging-technologies-education-in-2025': 'case-study-icp',
    'icp': 'case-study-icp', 'isla-camp': 'case-study-icp',
    '2025-news-inaugural-ai-engineering-scholarship-launched-by-ai-academy-ph-in-collaboration-with-devcon-apper-cloudschool-indigo-research': 'ai',
    'ai-scholarship': 'ai', 'ai-scholarships': 'ai', 'scholarship': 'ai', 'scholarships': 'ai', 'certification': 'ai',
    'climate-bayanihan-devcon-dost-dlsu-climate-innovator-workshop-2025': 'programs',
    'hour-of-ai': 'case-study-hour-of-ai', 'hour-of-code': 'case-study-hour-of-ai', 'kids': 'devcon-kids',
    'mindanao-ai-caravan': 'case-study-mindanao-ai-caravan', 'ai-angat': 'case-study-mindanao-ai-caravan', 'caravan': 'case-study-mindanao-ai-caravan',
    'code-camps': 'ai-code-camps', 'codecamps': 'ai-code-camps', 'barangay-ai': 'ai-code-camps',
    # structure aliases
    'events': 'attend', 'event': 'attend', 'calendar': 'attend', 'register': 'attend',
    'case-studies': 'devrel-case-studies', 'casestudies': 'devrel-case-studies', 'devrel': 'devrel-case-studies',
    'sponsors': 'partner', 'sponsor': 'partner', 'partners': 'partner', 'partnership': 'partner', 'partnerships': 'partner',
    'contact': 'partner', 'contact-us': 'partner', 'donate': 'partner',
    'leaders': 'leadership', 'team': 'leadership', 'officers': 'leadership', 'board': 'leadership', 'our-team': 'leadership',
    'our-story': 'about', 'about-us': 'about', 'history': 'about', 'organization': 'about', 'the-organization': 'about', 'who-we-are': 'about',
    'locations': 'chapters', 'regional-chapters': 'chapters', 'chapter': 'chapters', 'start-a-chapter': 'invite', 'invite-devcon': 'invite',
    'internship': 'jumpstart-internships', 'internships': 'jumpstart-internships', 'jumpstart': 'jumpstart-internships', 'ojt': 'jumpstart-internships',
    'volunteer': 'volunteers-guide', 'volunteers': 'volunteers-guide', 'be-a-volunteer': 'volunteers-guide', 'volunteering-basics': 'volunteers-guide',
    'code-of-conduct': 'code-of-conduct-for-national-and-chapter-officers-and-volunteers', 'anti-harassment-policy': 'code-of-conduct-for-national-and-chapter-officers-and-volunteers',
    'privacy': 'standard-privacy-and-safespace-consent', 'privacy-policy': 'standard-privacy-and-safespace-consent', 'safe-space': 'standard-privacy-and-safespace-consent',
    'event-participation-guidelines': 'campus-events-guidelines', 'child-protection': 'child-protection-policy',
    'brand': 'brand-kit', 'brandkit': 'brand-kit', 'logos': 'brand-kit', 'media-kit': 'brand-kit', 'press-kit': 'brand-kit',
    'our-initiatives': 'programs', 'initiatives': 'programs', 'program': 'programs',
    'summit': 'pro-summit', 'devcon-summit': 'pro-summit', 'campus-devcon': 'campus', 'sheisdevcon-2026': 'sheisdevcon',
    'cdo': 'cagayandeoro', 'cagayan-de-oro': 'cagayandeoro', 'metro-manila': 'manila', 'ncr': 'manila',
    # WordPress leftovers
    'news': '', 'blog': '', 'home': '', 'feed': '', 'comments/feed': '', 'author/devconadmin': '', 'brand-kit/feed': 'brand-kit',
}

import posixpath
_here = os.path.dirname(os.path.abspath(__file__))
_paths_file = os.path.join(_here, 'paths.py')
exec(open(_paths_file).read())

def _rel(from_path, to_path):
    """Relative URL from folder page from_path ('' = home) to folder page to_path."""
    r = posixpath.relpath('/' + to_path if to_path else '/', '/' + from_path if from_path else '/')
    return './' if r == '.' else r + '/'

def rel_link_fix(s, here, names):
    """Rewrite href="x.html#a" to the nested folder URL of x, relative to the page at folder `here`."""
    def fix(m):
        fn, frag = m.group(1), m.group(2) or ''
        if fn not in names: return m.group(0)
        return f'href="{_rel(here, path_of(fn[:-5]))}{frag}"'
    s = re.sub(r'href="([A-Za-z0-9_-]+\.html)(#[^"]*)?"', fix, s)
    return abs_fix(s)

def abs_fix(s):
    """Canonical, Open Graph, JSON-LD, sitemap, llms.txt: https://devcon.ph/<stem>/ -> nested path."""
    return re.sub(r'https://devcon\.ph/([a-z0-9-]+)/', lambda m: f'https://devcon.ph/{path_of(m.group(1))}/' if m.group(1) in PATHS else m.group(0), s)

def stub(target_rel, target_abs, title='Redirecting'):
    t = html.escape(target_rel, quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex"/>
<meta http-equiv="refresh" content="0; url={t}"/>
<link rel="canonical" href="{html.escape(target_abs, quote=True)}"/>
<title>{title} · DEVCON Philippines</title>
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#070430;color:#fff;font:16px/1.5 system-ui,sans-serif;text-align:center;padding:24px}}a{{color:#F2C500}}</style>
</head>
<body><p>This page moved. <a href="{t}">Continue to the new DEVCON page</a>.</p></body>
</html>
'''

def main():
    if os.path.exists(OUT):
        for q in os.listdir(OUT):
            if q in ('.nojekyll', '.well-known'): continue
            fp = os.path.join(OUT, q)
            shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    os.makedirs(OUT, exist_ok=True)
    names = {os.path.basename(f) for f in glob.glob(os.path.join(SRC, '*.html'))}
    stems = sorted(n[:-5] for n in names)
    real = {path_of(st) for st in stems}                       # folders that hold real pages
    # static files (sitemap, robots, llms, icons, og image) with nested URLs
    for f in os.listdir(SRC):
        if f.endswith('.html'): continue
        if f.endswith(('.xml', '.txt')):
            open(os.path.join(OUT, f), 'w', encoding='utf-8').write(abs_fix(open(os.path.join(SRC, f), encoding='utf-8').read()))
        else: shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
    # pages in nested folders
    for st in stems:
        here = path_of(st)
        s = open(os.path.join(SRC, st + '.html'), encoding='utf-8').read()
        d = os.path.join(OUT, here) if here else OUT
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(rel_link_fix(s, here, names))
    # redirects: every older address -> its nested page
    moves = {}                                                 # old folder path -> new folder path ('' = home)
    for st in stems:
        if st == 'index': continue
        new = path_of(st)
        if st != new: moves[st] = new                          # /cebu/ -> /locations/cebu/
    for old, tgt in REDIRECTS.items():
        moves.setdefault(old, path_of(tgt) if tgt else '')
    made = 0
    for old, new in moves.items():
        if old in real: continue                               # a real page lives there
        assert new == '' or new in real, (old, new)
        d = os.path.join(OUT, old); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(stub(_rel(old, new), f'https://devcon.ph/{new + "/" if new else ""}'))
        made += 1
    # /<stem>.html -> nested page (links shared from earlier previews)
    for st in stems:
        if st == 'index': continue
        open(os.path.join(OUT, st + '.html'), 'w', encoding='utf-8').write(stub(_rel('', path_of(st)), f'https://devcon.ph/{path_of(st)}/'))
    # smart 404: aliases -> stems, stems -> nested
    alias = dict(REDIRECTS)
    for st in stems:
        if st != 'index': alias[st] = st
    pm = {st: path_of(st) for st in stems if st != 'index'}
    nf = NOT_FOUND.replace('__ALIAS__', json.dumps(alias, separators=(',', ':')))
    nf = nf.replace("function go(slug){ location.replace(base+(slug?slug+'/':'')+location.hash); }",
                    "var PM=" + json.dumps(pm, separators=(',', ':')) + ";\n  function go(slug){ var t=slug?(PM[slug]||slug):''; location.replace(base+(t?t+'/':'')+location.hash); }")
    nf = nf.replace("  document.getElementById('nf-title').textContent=",
                    "  var sec=(parts[0]||'').toLowerCase(); if(['locations','programs','case-studies','playbook','about'].indexOf(sec)>-1){ location.replace(base+sec+'/'); return; }\n  document.getElementById('nf-title').textContent=", 1)
    assert 'var PM=' in nf and "indexOf(sec)" in nf
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)
    json.dump({'pages': sorted({'/' + (path_of(st) + '/' if path_of(st) else '') for st in stems}),
               'redirects': {f'/{k}/': (f'/{v}/' if v else '/') for k, v in moves.items() if k not in real}},
              open(os.path.join(OUT, 'url-map.json'), 'w'), indent=1)
    # Cloudflare Pages: server-side 301s
    lines = ['# Generated by scripts/restructure.py. Server-side redirects for Cloudflare Pages.']
    for old, new in moves.items():
        if old in real: continue
        t = f'/{new}/' if new else '/'
        lines += [f'/{old} {t} 301', f'/{old}/ {t} 301']
    for st in stems:
        if st == 'index': continue
        np_ = path_of(st)
        lines += [f'/{st}.html /{np_}/ 301']
        if np_ == st: lines += [f'/{st} /{st}/ 301']
        else: lines += [f'/{np_} /{np_}/ 301']
    lines += ['/index.html / 301', '/.well-known/security.txt /security.txt 200']
    open(os.path.join(OUT, '_redirects'), 'w').write('\n'.join(lines) + '\n')
    open(os.path.join(OUT, '_headers'), 'w').write(HEADERS)
    os.makedirs(os.path.join(OUT, '.well-known'), exist_ok=True)
    for f in (os.path.join(OUT, '.well-known', 'security.txt'), os.path.join(OUT, 'security.txt')):
        open(f, 'w').write(SECURITY_TXT)
    print(f'pages {len(stems)}, moved {sum(1 for st in stems if st != "index" and path_of(st) != st)}, redirect folders {made}, _redirects rules {len(lines) - 1}')

SECURITY_TXT = '''Contact: mailto:hello@devcon.ph
Contact: https://github.com/DEVCON-PHILIPPINES/staging-devcon-ph-2026-website-redesign/security/advisories/new
Expires: 2027-09-24T00:00:00.000Z
Preferred-Languages: en, fil
Policy: https://github.com/DEVCON-PHILIPPINES/staging-devcon-ph-2026-website-redesign/blob/main/SECURITY.md
Canonical: https://prod-devcon-ph-2026-website-redesign.pages.dev/.well-known/security.txt
'''

HEADERS = '''# Generated by scripts/restructure.py. HTTP security headers for Cloudflare Pages.
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()
  Cross-Origin-Opener-Policy: same-origin
  Content-Security-Policy: frame-ancestors 'none'; base-uri 'none'; object-src 'none'; upgrade-insecure-requests

# Keep the *.pages.dev preview out of search results (devcon.ph stays indexable)
https://:project.pages.dev/*
  X-Robots-Tag: noindex

/*.png
  Cache-Control: public, max-age=604800

/url-map.json
  Cache-Control: no-store
'''

NOT_FOUND = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>Page moved · DEVCON Philippines</title>
<style>
body{margin:0;min-height:100vh;display:grid;place-items:center;background:#070430;color:#fff;font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;padding:24px}
main{max-width:560px;text-align:center}
h1{font-size:clamp(1.6rem,4vw,2.4rem);margin:.2em 0}
p{color:#cfcaf0}
nav{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:22px}
nav a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;border:2px solid rgba(255,255,255,.4);color:#fff;text-decoration:none;font-weight:700}
nav a.primary{background:#F2C500;border-color:#F2C500;color:#070430}
</style>
</head>
<body>
<main>
  <p style="color:#F2C500;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:.8rem">DEVCON Philippines</p>
  <h1 id="nf-title">Taking you to the new DEVCON site</h1>
  <p id="nf-msg">This link is from the old website. We&#8217;re finding the right page for you.</p>
  <nav id="nf-nav"></nav>
</main>
<script>
(function(){
  var A=__ALIAS__;
  var parts=location.pathname.split('/').filter(Boolean), base='/';
  var k=-1; ['staging-devcon-ph-2026-website-redesign','DEVCON.ph-2026-Website-Redesign'].forEach(function(n){ if(k<0) k=parts.indexOf(n); });
  if(k>-1){ base='/'+parts.slice(0,k+1).join('/')+'/'; parts=parts.slice(k+1); }
  var p=parts.join('/').toLowerCase().replace(/\\.(html?|php)$/,'').replace(/\\/(feed|amp|page\\/\\d+)$/,'');
  function go(slug){ location.replace(base+(slug?slug+'/':'')+location.hash); }
  if(Object.prototype.hasOwnProperty.call(A,p)){ go(A[p]); return; }
  var last=(parts[parts.length-1]||'').toLowerCase().replace(/\\.(html?|php)$/,'');
  if(Object.prototype.hasOwnProperty.call(A,last)){ go(A[last]); return; }
  var kw=[['manila','manila'],['laguna','laguna'],['legazpi','legazpi'],['pampanga','pampanga'],['cebu','cebu'],['iloilo','iloilo'],['bohol','bohol'],['bacolod','bacolod'],
    ['tacloban','tacloban'],['davao','davao'],['iligan','iligan'],['cagayan','cagayandeoro'],['bukidnon','bukidnon'],['sui','case-study-sui'],['icp','case-study-icp'],
    ['isla','case-study-icp'],['scholarship','ai'],['caravan','case-study-mindanao-ai-caravan'],['campus','campus'],['pro-summit','pro-summit'],['prosummit','pro-summit'],
    ['summit','pro-summit'],['kids','devcon-kids'],['hour-of','case-study-hour-of-ai'],['she','sheisdevcon'],['women','sheisdevcon'],['intern','jumpstart-internships'],
    ['jumpstart','jumpstart-internships'],['volunteer','volunteers-guide'],['sponsor','partner'],['partner','partner'],['event','attend'],['news','']];
  for(var i=0;i<kw.length;i++){ if(p.indexOf(kw[i][0])>-1){ go(kw[i][1]); return; } }
  document.getElementById('nf-title').textContent='We couldn\\u2019t find that page';
  document.getElementById('nf-msg').textContent='It may have moved in the redesign. Try one of these:';
  var links=[['','Go to the homepage',1],['chapters','Find a location'],['programs','Programs'],['attend','Events'],['partner','Partner with us']], nav=document.getElementById('nf-nav');
  links.forEach(function(l){ var a=document.createElement('a'); a.href=base+(l[0]?l[0]+'/':''); a.textContent=l[1]; if(l[2]) a.className='primary'; nav.appendChild(a); });
})();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    main()
