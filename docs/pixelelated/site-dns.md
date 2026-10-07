# DNS for pixelelated.com on GitHub Pages

Prepared 2026-10-07 for #511. These records apply if GitHub Pages hosts the
site. No DNS changes have been made by this work.

First add `pixelelated.com` under the website repository's **Settings → Pages →
Custom domain**. GitHub recommends configuring that association before pointing
DNS at its servers. The current bot token cannot read or manage Pages settings
(403); repository maintain/push access alone has not established that access.

At the current DNS provider, iwantmyname, add:

| Type | Host/name | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `pixelelated.github.io` |

`@` means the root `pixelelated.com`; some providers use a blank field for it.
Keep the default TTL, or use3600 seconds. The CNAME target has no `https://`
or `/website` suffix. Preserve existing Proton Mail MX and mail-related TXT
records; changing nameservers is unnecessary for these additions.

Optional IPv6 support uses four additional records:

| Type | Host/name | Value |
| --- | --- | --- |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

These values and the GitHub-first setup order come from
[GitHub's custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).
After DNS resolves and GitHub provisions the certificate, enable **Enforce
HTTPS** in Pages settings. DNS/certificate changes can take up to24hours.

For organization-level domain verification, the owner can open organization
**Settings → Pages → Add a domain**, enter `pixelelated.com`, and add the TXT
record GitHub generates. Its usual host is `_github-pages-challenge-pixelelated`;
use the exact host/value shown there. The verification value cannot be inferred
from the domain. See [GitHub's verification instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).

The source repository is private. Before choosing Pages, check the organization
plan's support for private-source Pages; preserve the owner's visibility choice.
Hosting flexibility remains D-WORKFLOW-153. This document supplies DNS values;
it does not claim the website is deployed or that Pages is enabled.

Read-only receipts: `docs/qa-logs/2026-10-07-site-access/`. They contain filtered
repository/commit/access facts and public DNS answers, with no credentials.
