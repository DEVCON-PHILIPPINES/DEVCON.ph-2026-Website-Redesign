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
    'ai-fluency': 'ai-fluency-masterclass', 'ai-fluency-for-builders': 'ai-fluency-masterclass', 'masterclass': 'ai-fluency-masterclass',
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

def rel_link_fix(s, depth, names):
    """Rewrite href="x.html#a" and href="index.html" for a page that lives `depth` levels deep."""
    up = '../' * depth
    def fix(m):
        fn, frag = m.group(1), m.group(2) or ''
        if fn not in names: return m.group(0)
        if fn == 'index.html': target = up or './'
        else: target = f'{up}{fn[:-5]}/'
        return f'href="{target}{frag}"'
    return re.sub(r'href="([A-Za-z0-9_-]+\.html)(#[^"]*)?"', fix, s)

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
        for p in os.listdir(OUT):
            if p in ('.nojekyll', '.well-known'): continue
            fp = os.path.join(OUT, p)
            shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    os.makedirs(OUT, exist_ok=True)
    names = {os.path.basename(f) for f in glob.glob(os.path.join(SRC, '*.html'))}
    slugs = sorted(n[:-5] for n in names if n != 'index.html')
    # static files (sitemap, robots, llms, icons, og image)
    for f in os.listdir(SRC):
        if not f.endswith('.html'): shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
    # pages
    s = open(os.path.join(SRC, 'index.html'), encoding='utf-8').read()
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(rel_link_fix(s, 0, names))
    for slug in slugs:
        s = open(os.path.join(SRC, slug + '.html'), encoding='utf-8').read()
        os.makedirs(os.path.join(OUT, slug), exist_ok=True)
        open(os.path.join(OUT, slug, 'index.html'), 'w', encoding='utf-8').write(rel_link_fix(s, 1, names))
        # /<slug>.html -> /<slug>/
        open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8').write(stub(f'{slug}/', f'https://devcon.ph/{slug}/'))
    # old URLs -> new pages
    made = 0
    for old, new in REDIRECTS.items():
        if old in slugs: continue                      # a real page already lives there
        assert new == '' or new.split('#')[0] in slugs, (old, new)
        depth = old.count('/') + 1
        target = ('../' * depth) + (f'{new}/' if new else '')
        d = os.path.join(OUT, old); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(stub(target, f'https://devcon.ph/{new + "/" if new else ""}'))
        made += 1
    # smart 404 for everything else
    alias = {k: v for k, v in REDIRECTS.items()}
    for sl in slugs: alias[sl] = sl
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(NOT_FOUND.replace('__ALIAS__', json.dumps(alias, separators=(',', ':'))))
    json.dump({'pages': ['/'] + [f'/{x}/' for x in slugs], 'redirects': {f'/{k}/': (f'/{v}/' if v else '/') for k, v in REDIRECTS.items() if k not in slugs}},
              open(os.path.join(OUT, 'url-map.json'), 'w'), indent=1)
    # Cloudflare Pages: server-side 301s (search engines keep rankings) + real security headers
    lines = ['# Generated by scripts/restructure.py. Server-side redirects for Cloudflare Pages.']
    for old, new in REDIRECTS.items():
        if old in slugs: continue
        tgt = f'/{new}/' if new else '/'
        lines += [f'/{old} {tgt} 301', f'/{old}/ {tgt} 301']
    for sl in slugs:
        lines += [f'/{sl} /{sl}/ 301', f'/{sl}.html /{sl}/ 301']
    lines += ['/index.html / 301']
    open(os.path.join(OUT, '_redirects'), 'w').write('\n'.join(lines) + '\n')
    open(os.path.join(OUT, '_headers'), 'w').write(HEADERS)
    print(f'pages {len(slugs) + 1}, .html stubs {len(slugs)}, old-URL redirects {made}, 404 aliases {len(alias)}, _redirects rules {len(lines) - 1}')

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
  var k=parts.indexOf('DEVCON.ph-2026-Website-Redesign'); if(k>-1){ base='/'+parts.slice(0,k+1).join('/')+'/'; parts=parts.slice(k+1); }
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
