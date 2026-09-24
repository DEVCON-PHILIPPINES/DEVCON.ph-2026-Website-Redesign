# Contributing to the DEVCON.ph 2026 website

Thanks for helping. Every change goes through a pull request, a review, and an approved deploy.

## How changes go live

1. **Open an issue** (Content update or Bug report). It is added to the [DEVCON 2026 Website Design](https://github.com/orgs/DEVCON-PHILIPPINES/projects/2) project board automatically.
2. **Create a branch** from `main`, such as `content/cebu-photos`, and make your change in `docs/`.
3. **Open a pull request.** The **site-checks** job runs automatically and checks links, SEO tags, structured data, and style-guide wording.
4. **Get a review.** A website admin (see `.github/CODEOWNERS`) must approve before the pull request can merge. Pushing new commits resets the approval.
5. **Approve the deploy.** After the merge, the **Deploy (GitHub Pages + Cloudflare Pages)** workflow waits for an admin to approve the `github-pages` environment, then publishes the same commit to both hosts and verifies they match.

Direct pushes to `main`, force pushes, and branch deletion are blocked for everyone.

## Style guide

- Say **13 locations**, never "13 chapters".
- Say **AI Fluency for Builders** and **Beyond the capital**.
- Say **DEVCON HQ Office at Makati or Ortigas**.
- No links to the old devcon.ph site. Every page lives in this repo.
- Keep changelog notes generic, with no sponsor, partner, or people names.

## Run the checks locally

```
python3 scripts/check_site.py
```
