# DEVCON.ph 2026 Website Redesign

The rebuilt **devcon.ph** for DEVCON 17: *Engineering an AI-Ready Nation*. It is written to replace the current devcon.ph content, so every page lives here and nothing links back to the old site.

**Current version:** v1.68 · Sep 24, 2026, 12:10 PM PHT (see [CHANGELOG.md](CHANGELOG.md))

## What's in this repo

| Folder | What it is |
|---|---|
| `docs/` | The website: 47 self-contained HTML pages, plus `sitemap.xml`, `robots.txt`, and the social share image. Every image, style, and script is inlined, so any page opens on its own. |
| `combined/` | The same site as one HTML file, for quick review. |

Page file names follow the devcon.ph URL format, so `docs/manila.html` maps to `devcon.ph/manila/`. The compliance pages keep their exact devcon.ph slugs.

## Pages

- **Home and about:** `index.html`, `about.html` (Our Story), `leadership.html`
- **Programs:** `programs.html`, `devcon-kids.html`, `campus.html`, `sheisdevcon.html`, `pro-summit.html`, `crest.html`, `dctx.html`, `educators.html`
- **AI programs:** `ai.html` (AI Scholarships), `ai-fluency-masterclass.html`, `ai-code-camps.html`, `jumpstart-internships.html`
- **Locations:** `chapters.html`, plus one page for each of the 13 locations (`manila.html`, `laguna.html`, `legazpi.html`, `pampanga.html`, `cebu.html`, `iloilo.html`, `bohol.html`, `bacolod.html`, `tacloban.html`, `davao.html`, `iligan.html`, `cagayandeoro.html`, `bukidnon.html`)
- **DevRel case studies:** `devrel-case-studies.html`, `case-study-sui.html`, `case-study-icp.html`, `case-study-hour-of-ai.html`
- **Get involved:** `attend.html`, `invite.html`, `partner.html`
- **Community Playbook:** `playbook.html`, `volunteers-guide.html`, `code-of-conduct-for-national-and-chapter-officers-and-volunteers.html`, `standard-privacy-and-safespace-consent.html`, `campus-events-guidelines.html`, `child-protection-policy.html`, `brand-kit.html`

## Preview locally

Open `docs/index.html` in a browser. The pages link to each other by file name, so keep them in the same folder.

## Publish with GitHub Pages

The site deploys through the **Deploy to GitHub Pages** workflow and is live at `https://devcon-philippines.github.io/DEVCON.ph-2026-Website-Redesign/`.

To serve it on devcon.ph instead, add the domain under **Custom domain** on the same Settings page.

## Contributing and approvals

Changes go through a pull request, a review by a website admin, and an approved deploy. See [CONTRIBUTING.md](CONTRIBUTING.md).

- **site-checks** runs on every pull request and checks links, SEO tags, structured data, and wording.
- `main` is protected: pull request required, one approval from a code owner, passing checks, no force pushes.
- Merges into `main` deploy to GitHub Pages after an admin approves the `github-pages` environment.
- Issues and pull requests are added to the [DEVCON 2026 Website Design](https://github.com/orgs/DEVCON-PHILIPPINES/projects/2) project board.

## SEO

Every page has its own title and description, a canonical `https://devcon.ph/<slug>/` URL, Open Graph and X share tags, and schema.org data. Key pages also have answer-first FAQ sections marked up for AI search, `robots.txt` explicitly allows search engines and AI assistants, and `llms.txt` gives AI tools a plain-text summary with links. After launch, submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.

## Built for

The target CMS is Brizy on WordPress (www.devcon.ph). These pages serve as the visual and content blueprint.
