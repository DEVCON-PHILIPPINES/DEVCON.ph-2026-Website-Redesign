# Security

- Report a vulnerability privately with [GitHub private vulnerability reporting](../../security/advisories/new) or email hello@devcon.ph. Please don't open a public issue.
- Never commit tokens, passwords, or personal data. Use repository or organization secrets.
- Workflows run with read-only permissions by default. Only the deploy job gets `pages: write`, and only after an admin approves it.
