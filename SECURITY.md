# Security

## Reporting a vulnerability

Report privately with [GitHub private vulnerability reporting](../../security/advisories/new) or email hello@devcon.ph. Please don't open a public issue. See also `/.well-known/security.txt` on the site.

## How the site is hardened

The site is static: no backend, no accounts, no stored personal data.

- **Content-Security-Policy on every page:** `default-src 'none'`; scripts only from `'self'` plus SHA-256 hashes of each inline script (no `unsafe-inline`, no `unsafe-eval`); `object-src 'none'`, `base-uri 'none'`, `form-action 'none'`; frames limited to OpenStreetMap and Google Forms; `upgrade-insecure-requests`.
- **No inline event handlers or `javascript:` URLs, and no external script files.**
- **Anti-clickjacking:** pages hide themselves when framed by another site.
- **Links:** every new-tab link uses `rel="noopener"`, and the referrer policy is `strict-origin-when-cross-origin`.
- **Delivery:** production on Cloudflare Pages (DDoS protection, security headers), staging on GitHub Pages with HTTPS enforced and noindex. For devcon.ph, add WAF and rate limiting on the zone.
- **Repo:** protected `main`, code-owner review, deploy approval, secret scanning with push protection, Dependabot, CodeQL, and read-only workflow permissions.

`scripts/check_site.py` enforces these rules on every pull request. After editing a page, regenerate the CSP hashes with the build's `harden.py` step.

## Security audit (Sep 27, 2026)

Checked every repo in the organization and both live sites.

- **Secrets:** full git history of all 9 org repos scanned for tokens, API keys, private keys, and credential files. No leaked secrets. Secret scanning and push protection are on for both public repos.
- **Actions:** every Action is pinned to a full commit SHA (Dependabot keeps pins current); only GitHub-owned Actions may run; workflow tokens are read-only; outside contributors need approval before workflows run. The unused `pull_request_target` workflow was removed.
- **Branches and deploys:** `staging` and `main` rulesets with no bypass; production deploys need HQ approval with no admin bypass or self-review.
- **Redirect repo (`devcon-philippines.github.io`):** protected `main` (PR + approval, no force push or deletion), secret scanning and push protection on, Actions disabled.
- **Private HQ repos:** Dependabot alerts and security updates turned on.
- **Live sites:** strict CSP, HSTS, `X-Frame-Options: DENY`, `nosniff`, Permissions-Policy, COOP on production; HTTP redirects to HTTPS on both; no source or config files exposed; `security.txt` served on both.

**Open items (need an org owner):** rotate the Cloudflare token and revoke the GitHub token that were shared in a chat; downgrade the `DEVCONTools` automation account from Admin; require two-factor authentication for all org members; review the org base permission (interns currently have read access to private HQ repos).
