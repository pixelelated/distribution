# pixelelated site: first version

Status: planning, 2026-10-07. Tracked in [#511](https://github.com/pixelelated/distribution/issues/511),
parallel to M7. D-WORKFLOW-152/153 keeps hosting flexible and site delivery
separate from firmware qualification. No site has been deployed by this work.

## Repository and existing source

Use a dedicated ordinary repository, proposed `pixelelated/website`. The site
and wiki-style guides live together as versioned source. GitHub Pages is a
hosting service for a repository; GitHub's built-in Wiki is separate and is
not needed for these guides. A Pages project repository can use the owned
custom domain; the special `pixelelated.github.io` repository name is needed
only for the default organization-root site. See [GitHub's site types](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

No dedicated site repository appeared in the accessible organization list.
Private Pages settings were inaccessible, so that inventory does not prove
absence of all private sites. A direct read of `pixelelated/website` returned
404. Creation attempts through `gh repo create` and the documented REST
endpoint were rejected for the current blitterbot token; REST returned403.
The bot is an active organization member. An owner must create the repository
and grant write access, or provide the required repository-creation access.
Do not expose credentials in chat. No repository was created by either call.

The existing docs checkout is `/home/max/Development/rocknix.org`, clean on
`docs/cloud-saves-native-wizard` at `4f6df54ca16121ff2cd0620407aea6434ee59147`,
one local commit ahead of its fork remote. It uses MkDocs/Material, Markdown,
search, navigation and screenshots. Remotes still name `maxengel/rocknix.org`
and `ROCKNIX/rocknix.org`. Reuse selected material with its attribution; that
branch is238 commits behind cached upstream, not an appropriate whole-site
baseline. The upstream docs PR188 is open and unmerged as checked today.

## First-version scope

| Page or capability | Purpose |
| --- | --- |
| Home | Identify pixelelated and link to setup/documentation and qualified release information. |
| Cloud setup | Explain linking, enabled categories, expected folders, explicit actions and checks. Match #510/#508's final qualified behavior. |
| ROM setup | Show supported system folders and how to place ROMs from a computer, then check again. No automatic library relocation promise. |
| BIOS setup | Show the expected location and system-specific requirements, distinguishing folder presence from local compatibility checks. |
| Documentation navigation/search | Make the guides usable on a phone after scanning a QR. |
| Release links | Point to manifest-selected firmware/source/release notes; do not store large firmware payloads in the static site. |

Use the approved lowercase Tiny5 Duo LCD Ocean wordmark and readable body
text. Follow the existing developer-relations skill, with current product
terms, reviewed screenshots and preserved upstream credit. Content should
remain useful without an account. Do not add an updater service, telemetry
backend or community system without a concrete requirement.

## Hosting choice

A portable static site fits the first-version requirements. GitHub Pages is
the initial recommendation: it can publish a branch/folder or a generated
artifact from GitHub Actions. It does not execute server-side application
languages. The same generated site can move to another static host later;
a future API can also have its own host. See [creating a Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

Keep the published site small and link to release assets: Pages limits the
published site to1GB and has a soft100GB/month bandwidth limit. See [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
If built-in preview deployments or a server runtime becomes a requirement,
compare hosts against that requirement before choosing. No hosting migration
is necessary merely because a future service might exist.

## Domain and launch sequence

The earlier recorded domain is `pixelelated.com`; a later message says
`pixelated.com`. Exact spelling is awaiting confirmation before DNS changes.
For `pixelelated.com` only, current public DNS reads show no A/AAAA record,
`www` NXDOMAIN, iwantmyname nameservers and Proton Mail MX. Historical
Cloudflare/Hostinger notes are not current authority. Preserve mail records.

1. Establish the dedicated repository and access. Local starter README and
   agent instructions are prepared; no deployment workflow is enabled.
2. Select a current static-site baseline and dependencies, then import only
   reviewed guides/assets, with their licenses and attribution.
3. Reconcile cloud guides against final #510/#508 behavior. Build locally,
   check links, phone layouts, wordmark rendering and instructions. Use hosted
   CI runners; website jobs do not belong on the firmware build machine.
4. Configure the chosen host from the reviewed artifact. For Pages, use the
   documented artifact workflow and deployment environment rather than
   inheriting the old fork's force-push workflow without review.
5. Confirm the owned domain, prepare its exact web DNS changes, establish
   HTTPS, and retain public content/redirect readback. Do not modify mail DNS.
6. Only then enable the handheld's per-guide QR destinations. ROM and BIOS
   findings say See instructions, opening a controller-dismissable modal.
   Decode actual VM frame QR images to verify destinations. Local instructions
   continue to work offline and before guide publication.

Can this be done on the VM? Handheld help/modal behavior and QR rendering can.
Site builds, browser rendering and public HTTPS/DNS reads are host facts; no
physical device or personal cloud is required.
