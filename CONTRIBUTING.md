# Contributing to the DEVCON.ph 2026 website

Thanks for helping. DEVCON is a volunteer tech community, and this site is open source. Anyone can propose a change; **HQ leaders approve every merge and every production release.**

## Branches and environments

| Branch | Environment | URL | Who merges |
|---|---|---|---|
| `feature/*`, `content/*`, `fix/*`, `docs/*`, `chore/*` | Pull request preview | Cloudflare posts a preview link on each PR | Nobody; these are short-lived |
| `staging` (default branch) | **staging-** (GitHub Pages) | https://devcon-philippines.github.io/staging-devcon-ph-2026-website-redesign/ | HQ leaders, after review |
| `main` | **prod-** (Cloudflare Pages) | https://prod-devcon-ph-2026-website-redesign.pages.dev | HQ leaders, release PRs only |
| `hotfix/*` | Emergency fix | Preview link | HQ leaders, straight into `main` |

## How a change goes live

1. **Open an issue** (Content update or Bug report). It lands on the [project board](https://github.com/orgs/DEVCON-PHILIPPINES/projects/2).
2. **Branch from `staging`** using a prefix: `content/cebu-photos`, `fix/map-pins`, `feature/devie-faq`. External contributors fork the repo and branch the same way.
3. **Open a pull request into `staging`.** It's the default base. Checks run automatically: **site-checks** (links, SEO, structured data, wording, security) and **CodeQL**. Cloudflare posts a preview link.
4. **An HQ leader reviews and approves.** Code owners in `.github/CODEOWNERS` are the only approvers. New pushes reset the approval, all review comments must be resolved, and the approver can't be the person who pushed last.
5. **Squash-merge into `staging`.** **Deploy staging (GitHub Pages)** updates staging- automatically for a final look.
6. **Release to production.** An HQ leader opens a pull request from `staging` into `main`, gets approval from another HQ leader, and merges it with a merge commit, which keeps both branches in sync.
7. **Approve the production deploy.** The **Deploy production (Cloudflare Pages)** workflow waits for an HQ leader to approve the `production` environment, deploys to prod-, and verifies every page.

**Hotfixes:** branch `hotfix/<name>` from `main`, open a PR into `main`, get HQ approval, release, then open a PR from `main` back into `staging` so the fix isn't lost.

## Rules that are enforced

- No direct pushes, force pushes, or branch deletion on `staging` or `main`, for anyone, including admins.
- `main` only accepts pull requests from `staging` or `hotfix/*` (the **release-source** check).
- Production deploys need an HQ leader's approval, and admins can't bypass it.
- Pull requests from first-time and outside contributors need approval before workflows run.
- Workflows are read-only by default; secrets are only available to approved deploy jobs.

## Style guide

See section 5 of [PRD.md](PRD.md). The basics: say **13 locations** (never "13 chapters"), **AI Fluency for Builders**, **Beyond the capital**, **DEVCON HQ Office at Makati or Ortigas**; no links to the old devcon.ph site; generic changelog notes.

## Run the checks locally

```
python3 scripts/check_site.py
```
