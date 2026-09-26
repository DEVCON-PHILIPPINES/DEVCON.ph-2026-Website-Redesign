# DEVCON.PH 2026 Website Redesign: Product Requirements Document

**Status:** Live on GitHub Pages · **Current version:** v1.74 · **Owner:** DEVCON Philippines National Office (Communications)
**Source of truth:** this file. When the site, a brief, or a chat thread disagrees with this PRD, update this PRD first, then the site.

---

## 1. Overview

The DEVCON.PH 2026 website is the public home of DEVCON Philippines (DevConnect Philippines Inc.), the country's largest volunteer tech community: a non-profit founded in 2009 with 13 locations nationwide. The 2026 redesign launches with DEVCON 17 and its theme, **Engineering an AI-Ready Nation**.

The site is a static, self-contained HTML build. It is a visual and content blueprint for the eventual production site at devcon.ph, and it is live today at https://devcon-philippines.github.io/DEVCON.ph-2026-Website-Redesign/.

## 2. Goals

1. **Grow participation:** make it easy to find a free event, volunteer, join a chapter, or apply to a program.
2. **Win partners:** show verifiable outcomes through DevRel case studies so companies, schools, and LGUs partner with confidence.
3. **Build trust:** present DEVCON as a registered, accountable non-profit with clear standards (Community Playbook, policies, leadership).
4. **Collect feedback:** gather feedback on the redesign during review through the Give Feedback tab and Devie.
5. **Be discoverable:** rank in search and AI answers (SEO and AEO) for DEVCON, Philippine tech community, and AI education topics.

### Non-goals

- No user accounts, logins, payments, or stored personal data on this site. Registration lives on DEVCON+ (https://www.devcon.plus) and partner forms.
- No costs, budgets, or financial figures in public content (for example, case studies never mention costs).

## 3. Audiences

| Audience | What they need | Primary pages |
|---|---|---|
| Students and young developers | Free events, programs, internships, scholarships | Programs, Attend, Internships, AI Scholarships |
| Professionals and builders | Summits, AI Fluency for Builders, certification | Programs, PRO Summit, AI Scholarships |
| Volunteers and chapter officers | How to help, standards, playbook | Volunteer popup, Playbook, Locations |
| Partners and sponsors | Proof of impact, formats, contact | Partner, DevRel Case Studies, Brand Kit |
| Schools, LGUs, communities | How to bring DEVCON to their city | Invite DEVCON |
| Media | Boilerplate, logos, facts | Brand Kit, Our Story |

## 4. Information architecture

**Top menu:** Our Story, Programs, Locations, DevRel Case Studies, Community Playbook, Volunteer.

**Homepage order:** hero, logo carousel ("Trusted by leaders and pioneers"), locations map (static on mobile), numbers, about, 17 years, explore, Recent news 3×3 ("What we've been building", led by the Mindanao AI Caravan as major news), Be part of DEVCON 17 hub, FAQ, partners, DEVCON+ banner.

**Pages (47):**

- **Core:** Home (`/`), Our Story (`about`), Leadership (`leadership`), Programs (`programs`), Attend (`attend`), Partner (`partner`), Invite DEVCON (`invite`), AI Scholarships (`ai`), Jumpstart Internships (`jumpstart-internships`), AI code camps (`ai-code-camps`).
- **Locations:** Locations hub (`chapters`) and 13 location pages: manila, laguna, legazpi, pampanga, cebu, iloilo, bohol, bacolod, tacloban, davao, iligan, cagayandeoro, bukidnon.
- **Programs:** devcon-kids, campus, sheisdevcon, pro-summit, crest, dctx, educators, ai-fluency-masterclass.
- **DevRel case studies:** hub (`devrel-case-studies`) and case-study-sui, case-study-icp, case-study-hour-of-ai, case-study-zoho-creator, case-study-campus-devcon-summit, case-study-pro-summit, case-study-mindanao-ai-caravan.
- **Community Playbook:** playbook, volunteers-guide, code-of-conduct-for-national-and-chapter-officers-and-volunteers, standard-privacy-and-safespace-consent, campus-events-guidelines, child-protection-policy, brand-kit.

**URLs match devcon.ph.** Every page lives at a trailing-slash URL, the same as the current devcon.ph (for example `/about/`, `/manila/`, `/jumpstart-internships/`), so existing links, bookmarks, and search results keep working. The downloadable ZIP keeps `.html` file names so pages open locally.

**Legacy URL migration.** Every known devcon.ph URL either maps to a page with the same path or redirects to its new home. `docs/url-map.json` lists all pages and redirects. Highlights:

| Old URL | New page |
|---|---|
| `/she-2026/` | `/sheisdevcon/` |
| `/campussummit2023/` | `/case-study-campus-devcon-summit/` |
| `/prosummit2023/` | `/case-study-pro-summit/` |
| `/summergiveaway2023/` | `/case-study-zoho-creator/` |
| `/ai-fluency/` | `/ai-fluency-masterclass/` |
| `/events/` | `/attend/` |
| Sui "Build Beyond" news post | `/case-study-sui/` |
| ISLA CAMP / ICP 2025 news post | `/case-study-icp/` |
| AI Engineering Scholarship 2025 news post | `/ai/` |
| Climate Bayanihan workshop 2025 post | `/programs/` |
| `/feed/`, `/comments/feed/`, `/author/devconadmin/`, `/news/`, `/blog/` | `/` |
| `/<page>.html` links from earlier previews | `/<page>/` |

Common aliases also redirect (for example `/sponsors/`, `/partners/`, `/contact/` → `/partner/`; `/case-studies/` → `/devrel-case-studies/`; `/cdo/` → `/cagayandeoro/`). Anything else hits a smart `404.html`, which matches the old path by slug or keyword (chapter names, programs, news topics) and forwards to the closest page. If nothing matches, it shows links to Home, Locations, Programs, Events, and Partner, never a dead end. On Cloudflare Pages, `docs/_redirects` turns these into server-side 301s, so search engines transfer rankings. When a new old URL is reported, add it to `REDIRECTS` in `scripts/restructure.py`.

## 5. Content rules (style guide)

These rules are enforced by review and, where possible, by `scripts/check_site.py`.

- **Locations:** say "13 locations", never "13 chapters". Nine are active chapters; Bohol, Bacolod, Tacloban, and Cagayan de Oro are volunteer communities.
- **Chapter status:** volunteer communities have no active or renewed chapter officers. Promotion to active chapter status follows a stringent process that tests commitment, readiness, and long-term alignment with DEVCON as a non-profit, beyond seed funds and tech hype. Volunteer-community pages use Volunteer CTAs.
- **Who we are:** DEVCON is a volunteer tech community, not an events company. Speakers, mentors, officers, and organizers volunteer to pay it forward and give back to the community, and every program is a public good. Homepage, Locations, every chapter page, Leadership, and Invite carry this message.
- **Chapter capacity:** as a volunteer community, DEVCON has limited capacity. To date, 4 chapters were not renewed for non-compliance and inactivity. DEVCON always prioritizes quality over quantity, of both events and impact. Requirements are listed on the Invite page (`/invite/#chapter-requirements`).
- **How chapters start:** every chapter starts with a DEVCON speaker paying it forward at a free event. Hosts cover each volunteer speaker's transportation, meals, a token of appreciation, and accommodations (as applicable); this is required outside existing chapter locations. Invitations go to hello@devcon.ph using the pre-filled invitation email on the Invite page.
- **Office:** "DEVCON HQ Office at Makati or Ortigas".
- **Programs and names:** "AI Fluency for Builders"; "Beyond the capital" (chapter presidents section); mention AI Certification Scholarships; AI tools are "OpenCode, Anthropic Claude, Ollama, and more".
- **AI Scholarships:** scholarships and exam attempts are granted on an approval basis and are not guaranteed.
- **Internships:** Jumpstart runs five months, voluntary or as an academic requirement. Applications go through the Airtable form.
- **Partners:** "They make our programs free, possible, and life-changing for grassroots communities." Credit Amihan and Avtica (never NMBLR). Sui verified figure is "330+".
- **Exclusions:** no mention of Michael Lance Domagas. No dates on chapter event lists. No costs in public content.
- **Links:** no links out to the old devcon.ph site; every page lives in this repo. When a destination is unknown, link to https://www.facebook.com/devconph (the build replaces any empty link with it).
- **Changelog:** notes stay generic, with no sponsor, partner, or people names.
- **Voice:** clear, declarative, grounded. No hedging or reported speech in content adapted from keynotes.

## 6. Features

### 6.1 Volunteer popup
Every Volunteer CTA opens a centered popup with the DEVCON volunteer Google Form (https://docs.google.com/forms/d/e/1FAIpQLSczVxZPmHIRPphNJNgbuRVzEC5QTponVzjDPPMmkSxP0cIdrg/viewform). The form URL is the no-JavaScript fallback. The popup closes with Esc, the close button, or a click outside, and offers "Open in new tab".

### 6.2 Feedback
Feedback is collected through Devie (6.3). The right-edge Give Feedback tab was removed in v1.72. Feedback emails go to:

- **To:** jumpstart-interns-c5-2026@devcon.ph, rj@devcon.ph, acapucion@devcon.ph, ddeleon@devcon.ph, jfernando@devcon.ph
- **Subject:** DEVCON.PH 2026 Website Redesign Feedback and Screenshots
- **Body:** the visitor's feedback, page, link, version, screen, browser, and a reminder to attach screenshots.

### 6.3 Devie, DEVCON AI Assistant
A rule-based chat at the lower right of every page. Devie is a **basic FAQ bot, not an AI or LLM**: it matches keywords to set answers written by the DEVCON team and runs entirely in the browser, with no AI model, no API, and no data collected. The header, welcome message, footer note, and an "are you AI?" answer all say so. The panel is up to 420 × 720 px (full width on phones) with 16 px message text, sized so the welcome fits without scrolling.

- **Primary job is feedback:** the welcome asks for feedback, a Submit feedback button sits above the input, and every answer ends with a feedback prompt. Feedback mode turns the visitor's words into the feedback email in 6.2.
- **Motion:** the panel pops in, messages slide in, and a typing indicator shows before each reply (about 0.7 to 1.6 seconds, longer for longer questions). Reduced-motion users get instant replies with no animation.
- **Local welcome:** the greeting matches the chapter page (Tagalog, Bisaya, Hiligaynon, Bikol, Kapampangan, or Waray) and is random elsewhere.
- **FAQ answers:** basic questions in English, Filipino, and regional words, with a Gen Z tone. Every answer links to the right page or section.

### 6.4 Other features
- **Locations map:** homepage map with pulsing chapter dots, where rows and pins link to chapter pages. Each location page has a Philippines mini-map, an OpenStreetMap view framed on the chapter's whole administrative region (for example, Central Visayas for Cebu and Bohol), and an Open in Google Maps link. There is no Get directions button.
- **FAQ next steps:** every FAQ answer ends with "Next step" links.
- **Leaders:** board, national office, area program leaders, and chapter presidents, each with a LinkedIn link. Chapter president photos use a standardized head-and-shoulders crop.
- **Intern quotes:** each name links to Jumpstart intern stories on Medium.
- **Scroll animations:** homepage headings and cards fade up with a light stagger; off for reduced-motion users.
- **Brand Kit:** logos, palette, Montserrat, key visuals, boilerplate, and entity information.

## 7. Design system

- **Colors:** navy #070430, deep navy #05022A, yellow #F2C500, purple #7808FF, lavender #A57BFF, orange #EA641D, green #71B405, pink #EC4899. Region colors: Luzon purple, Visayas orange, Mindanao green.
- **Type:** Montserrat (900/800 headlines, 700/600 labels, 400 body).
- **Accessibility:** WCAG-minded contrast, 44 px minimum tap targets, visible focus states, skip link, semantic landmarks, reduced-motion support, alt text on every meaningful image.
- **Responsive:** verified at 1440, 820, and 375 px with no horizontal scroll.

## 8. Technical architecture

- **Self-contained pages:** each page is one HTML file with inlined CSS, JavaScript, and images (base64). This prevents broken rendering when files are opened individually.
- **Build:** a single-page build is split into per-page files, stamped with version and PHT time (filename, header change-log comment, and meta tags; never the visible footer), then hardened.
- **Repo layout:** `docs/` is the deployed site (`docs/<slug>/index.html` per page, redirect stubs, `404.html`, `url-map.json`); `combined/` holds the single-file version; `scripts/restructure.py` builds the deploy layout and redirects; `scripts/harden.py` pins the CSP; `scripts/check_site.py` runs the checks, including that every redirect lands on a real page.
- **SEO and AEO:** per-page titles and descriptions, canonical URLs for devcon.ph, Open Graph and X cards, JSON-LD (NGO, Organization, Breadcrumb, Article, FAQPage), sitemap.xml, AI-friendly robots.txt, and llms.txt.

## 9. Security

The site is static, has no backend, and stores no personal data. Hardening:

| Threat | Control |
|---|---|
| XSS and unauthorized scripts | Strict Content-Security-Policy on every page: `default-src 'none'`, scripts limited to `'self'` plus SHA-256 hashes of each inline script (no `unsafe-inline`, no `unsafe-eval`), `object-src 'none'`, `base-uri 'none'`, `form-action 'none'`, frames limited to OpenStreetMap and Google Forms, and `upgrade-insecure-requests`. No inline event handlers, no `javascript:` URLs, no external script files. Devie writes visitor text with `textContent`, never as HTML. |
| Clickjacking | Pages hide themselves when loaded inside another site's frame. |
| Tabnabbing and referrer leaks | Every new-tab link has `rel="noopener"`; referrer policy is `strict-origin-when-cross-origin`. |
| DDoS and traffic spikes | Served from Cloudflare Pages (project `devcon-ph-2026-website-redesign`, output `docs/`, branch `main`) on Cloudflare's global network with built-in DDoS protection; GitHub Pages remains a mirror. When devcon.ph is connected, enable Bot Fight Mode, WAF managed rules, and rate limiting on the zone. |
| Missing HTTP security headers | `docs/_headers` (Cloudflare Pages) sends HSTS, `X-Frame-Options: DENY`, `frame-ancestors 'none'`, `nosniff`, referrer policy, Permissions-Policy, and COOP; `*.pages.dev` is `noindex` so only devcon.ph is indexed. |
| Supply chain and secrets | Secret scanning and push protection, Dependabot updates, CodeQL code scanning, and read-only workflow permissions by default. |
| Unauthorized changes | Protected `main` (pull request, code-owner approval, passing checks, no force pushes) and deploy approval for the `github-pages` environment. |

`scripts/check_site.py` fails any pull request that breaks these rules. Report vulnerabilities through GitHub private vulnerability reporting or hello@devcon.ph (see `SECURITY.md` and `/.well-known/security.txt`).

## 10. Workflow and governance

1. Open an issue (Content update or Bug report); it lands on the project board (org project #2).
2. Branch from `main`, change the site, and open a pull request.
3. **site-checks** must pass: links, anchors, SEO tags, JSON-LD, wording, and security rules.
4. A code owner approves (`@domdeleondevcon` or `@JFernando-DEVCON`), then squash-merge.
5. **Deploy (GitHub Pages + Cloudflare Pages)** runs and waits for an admin to approve the `github-pages` environment. One approval deploys the same commit to Cloudflare Pages first, then GitHub Pages, and a verify job confirms both hosts serve the same version and every page. Cloudflare's Git auto-deploy for production is off, so production only changes through this workflow; pull requests still get Cloudflare preview URLs.

Every release bumps the minor version and updates `CHANGELOG.md`.

## 11. Acceptance criteria for any release

- All pages return 200, with no console errors or CSP violations.
- No horizontal scroll at 1440, 820, and 375 px, and every interactive element is at least 44 px.
- `scripts/check_site.py` passes.
- The content rules in section 5 hold.
- The version and PHT timestamp are updated in the filename, header comment, and meta tags.

## 12. Open items

- **LinkedIn URLs:** replace the LinkedIn people-search links on the Leadership page with each leader's exact profile URL.
- **Custom domain:** connect devcon.ph, put it behind Cloudflare, then submit the sitemap to Google Search Console and Bing.
- **Content gaps:** real headshot for the Winston Damarillo placeholder, better Tacloban and Manila photos, and actual Mindanao AI Caravan attendance to replace targets.
- **AI Scholarships:** move the application from email to a form.
- **Legazpi award:** confirm the official name.

## 13. Contacts

- **Website team:** jumpstart-interns-c5-2026@devcon.ph, rj@devcon.ph, acapucion@devcon.ph, ddeleon@devcon.ph, jfernando@devcon.ph
- **General and partnerships:** hello@devcon.ph
