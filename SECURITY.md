# Security

## Reporting a vulnerability

Report privately with [GitHub private vulnerability reporting](../../security/advisories/new) or email hello@devcon.ph. Please don't open a public issue. See also `/.well-known/security.txt` on the site.

## How the site is hardened

The site is static: no backend, no accounts, no stored personal data.

- **Content-Security-Policy on every page:** `default-src 'none'`; scripts only from `'self'` plus SHA-256 hashes of each inline script (no `unsafe-inline`, no `unsafe-eval`); `object-src 'none'`, `base-uri 'none'`, `form-action 'none'`; frames limited to OpenStreetMap and Google Forms; `upgrade-insecure-requests`.
- **No inline event handlers or `javascript:` URLs, and no external script files.**
- **Anti-clickjacking:** pages hide themselves when framed by another site.
- **Links:** every new-tab link uses `rel="noopener"`, and the referrer policy is `strict-origin-when-cross-origin`.
- **Delivery:** GitHub Pages' CDN with HTTPS enforced. For devcon.ph, use Cloudflare for DDoS protection, WAF, and rate limiting.
- **Repo:** protected `main`, code-owner review, deploy approval, secret scanning with push protection, Dependabot, CodeQL, and read-only workflow permissions.

`scripts/check_site.py` enforces these rules on every pull request. After editing a page, regenerate the CSP hashes with the build's `harden.py` step.
