## Current identity transition — 2026-10-04

#409 is first within M7.P3 before the next freeze/build: lowercase **pixelelated**, organization `pixelelated`, owner `rasteratops`, unchanged developer `blitterbot`, default `/pixelelated`. Rasteratops remains a character. D-WORKFLOW-144/D-CLOUD-174 supersede earlier project/default naming below. The owner confirms no systems use `/Rasteratops`: **ROCKNIX → pixelelated** is the required adoption path. Existing cloud folders may move through the established verified migration. Historical replacement02 remains RASTERATOPS evidence; new bytes require new qualification. The milestone body owns the order, followed by remaining P3 checks, expanded P4 fixes audit and separately gated P5.

## Source implemented; candidate evidence pending — 2026-10-02 (#385)

Distribution fcd0f20c9a (next df23faff6c) pins ES 97523542963dcc72e9ea51cfbcd26b735ff28c1f and splash 7450aa8180ae66684814dd460f31eb502b2abf61. RASTERATOPS/0.0.1, wordmark, manual updater, reporting disablement and licence files exist in source; there is no branded candidate image yet. D-WORKFLOW-093 selects manual adoption; the site is the approved placeholder (D-WORKFLOW-098), not a new full-site gate. Legacy cloud names remain where compatibility readers/migration need them. See docs/rasteratops/release-readiness.md.

**Maintainer, 2026-09-29 (chat, D-QA-012), and later the same evening on sponsorships:** *"I also don't need to accept sponsorship. I really don't care either way. If at some point I wanted a Patreon or something, I could do that. This is more about whether it would be about sponsoring my work, but then that's just actually creating more issues because I have sponsors to deal with. Let's strike that concept: no sponsorships here."* The first message: *"At a certain point, it might be easier to fork, create the version I want, not allow for contributors, enable GitHub sponsorships, and just quietly offer an alternative. I have no interest in a Discord server, managing a community, etc., but I am interested in having a better experience, even if it's mainly just for me. If others can enjoy it, all the better, but to put in a lot of work and then not have it upstreamed seems silly. I also have a name we could use for this."* -- *"pixelelated", where I own the domain as well.*

**What the fork's own identity takes**, from #334's licence read (the branding is CC BY-NC-SA and must not suggest ROCKNIX's endorsement) and the tree as it stands. Not started until D-WORKFLOW-081 is called.

1. **The name in the tree**: `distributions/ROCKNIX/` becomes `distributions/pixelelated/` (the options file's `DISTRONAME`, `OS_NAME`, the version), the update URL the updater reads pointed at the fork's own releases, the theme's logo and the splash replaced by artwork of the fork's own (the ROCKNIX images may not be reused as a fork's identity), the device pages' names where they say ROCKNIX, and a line in the fork's README and release notes: *a fork of ROCKNIX, itself a fork of JELOS*, with the credits kept whole. The kernel, bootloaders, device trees, quirks and every package stay as merged from `upstream/next`.
2. **The repositories**: the distribution fork renamed to match (GitHub redirects the old name), the EmulationStation fork likewise; issues on, pull requests unsolicited (a public repository cannot refuse them; a `CONTRIBUTING.md` says the project takes none and the template says so), no sponsorships of any kind (struck by the maintainer, below), no Discord and no community channel -- the releases page and the site are the whole surface.
3. **The site**: the domain the maintainer owns, a MkDocs site like rocknix.org's from the pages already written for it (`docs/configure/cloud-sync.md`, `networking.md`, `play/retro-achievements.md` in the site checkout), under the new name, in the maintainer's voice.
4. **The releases**: the same `tools/fork-publish-release` and notes as RC1 and RC2, under the new tag prefix and name; every image built from one head, proven on the VM first, on the devices with a yes.

Can this be done on the VM? Yes: an image that boots under the new name with its own splash on guest d is the proof; a device after, on its yes.

## Acceptance criteria

- [ ] The register row that calls the direction (D-WORKFLOW-081's answer) names the fork's name and the licence terms it keeps (GPL-2 and MIT kept whole; the CC BY-SA attribution line; no ROCKNIX images).
- [ ] A GENERIC_X64 image boots under the new name with its own splash and logo, `OS_NAME` read from `/etc/os-release`, the manual-update row visible, and no automatic upstream update request in the captured guest network evidence (frame/readback/capture filed here).
- [ ] The approved placeholder site under the fork domain carries lineage/attribution and release/adoption links; its build/retrieval receipt is filed here. A full site is later scope (D-WORKFLOW-098).




## Added 2026-10-01: the cloud root is part of the brand transition (D-CLOUD-159)

> let's move everything to "/Rasteratops" as the default root directory we look for. that should be part of our baseline brand transition

So the identity change carries the cloud folder with the name, the splash, the version and the strings: `cloud_sync.conf` and `.defaults` ship `/Rasteratops/Saves`, `/Rasteratops/Backups`, `/Rasteratops/Content` (`SAVES_REMOTE`, `SETTINGS_REMOTE`, `CONTENT_REMOTE`, and `DEFAULT_*`), `cloud_setup`'s derived paths, the wizard's and the transfer page's words, `cloud_migrate_layout`'s target, the device-name fallbacks and the `/ROCKNIX` strings in the interface (`GuiMenu.cpp:5230`) read the new name; the migrations and guards are #353's.

- [ ] A fresh guest on the candidate, signed in to the QA cloud, creates and uses `/pixelelated/{Saves,Backups,Content}`: `tools/cloud-test-backend ls` after a backup and a saves sync shows the three folders and nothing under `/ROCKNIX`; `grep -rn ROCKNIX projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf*` prints nothing; `tools/vocabulary-check` passes.
- [ ] Every `/ROCKNIX` cloud path in the interface and the scripts is listed by the sweep (`docs/rasteratops/p0-sweep-hits.txt`, rule `cloud-path`, 56 lines) and each is changed or marked history in the same commit; the sweep re-run on the candidate's tree lists none as current.


## Added 2026-10-01: the case, the placeholder mark, the tar's name, the password note (D-WORKFLOW-127 to 130)

> Our convention might be better in the OS release to either be lowercase or uppercase. I'm fine either way, but the general convention looks good. I'm happy with whatever you recommend there.

> I'm still working on the artwork. In the short term, maybe we just use a word mark without an icon until I have one as a placeholder.

- [ ] `DISTRONAME="pixelelated"`: `os-release` reads `OS_NAME="pixelelated"`, the images are `pixelelated-<board>.<arch>-0.0.1.*`, the info page reads `OPERATING SYSTEM: pixelelated` (a 640x480 frame from guest d; `/etc/os-release` from the image's SYSTEM); repositories, packages and hosts stay lowercase `rasteratops`; the cloud folder is `/pixelelated` (D-CLOUD-158).
- [ ] The migration tar carries the suffix `-from-ROCKNIX` (`IMAGE_SUFFIX`), so its name passes the RC2 init's check (`init:882`): the built name is `pixelelated-H700.aarch64-0.0.1-from-ROCKNIX.tar` and `tools/vm-upgrade-rehearsal` from RC2's image applies it; the suffix is dropped in the build after 0.0.1 (D-WORKFLOW-128).
- [ ] The splash and the theme's logo carry the word mark alone until the icon arrives (D-WORKFLOW-130): the splash frame at boot and the theme's logo frame on guest d show the name in the chosen face and no pictorial mark.
- [ ] The release notes and the site's ssh page say the ssh password is unchanged in 0.0.1 (D-WORKFLOW-129, #358): the notes file's line and the docs PR.