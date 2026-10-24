# Retrospective — M6.P2 T7, the generic packages the image builds

Phase 3 of the code-auditor skill over the 266 paths, at `8ebaf8daad`'s bytes. The renovation face (Q1 to Q7) is in `04` § Renovation face; this file holds the skill's own faces.

## 3.1 Architectural coherence

- **One mover per pin.** 227 of the 243 recipes are byte-identical to `upstream/next`, and `upstream/next` has made no commit under `packages/` since the base (`git log c445081a59..upstream/next -- packages/` is empty, out of 325 commits). ROCKNIX's last LibreELEC merge is `d43d166b7a` (2026-08-12). So every upstream-carried pin here moves when ROCKNIX next merges LibreELEC master and the fork then merges ROCKNIX. `scripts/update_packages:16` walks `projects/ROCKNIX/packages` only, so `make update` never reaches these recipes (#644 finding 15, `02` § The #644 findings).
- **A recipe's pin is not always the recipe's own.** 47 ROCKNIX overrides under `projects/` source one of the 243 and then add to it. Three change the version (`opus` 1.6.1 to 1.5.2, `gcc` 16.2.0 to 15.2.0, `libfmt` 12.2.0 to 9.1.0 on every plan but SM8550's). Four change the URL or checksum (`wavpack`, `zlib`, `libevdev`, `libfreeaptx`). The inventory's `shadowed_by` is 0 for all 47, because the generic recipe is still sourced and so still reached. That is correct about reach and silent about the pin (F-12). Q4's table therefore reads the effective pin from `config/options <name>` per plan, as `device-builds.md` § After rebasing item 3 says.
- **The fetch has two sources.** `scripts/get_archive` tries `PKG_URL` and then `${DISTRO_MIRROR}/${PKG_SOURCE_NAME}` (`:31-36`). The mirror is `distributions/ROCKNIX/options:186`, ROCKNIX's `distribution-sources` release `sources-v2`. The fetch sweep shows the mirror covering every archive whose own URL is gone (F-02 to F-05). Losing the mirror would turn those four into build failures from an empty cache.

## 3.2 Project conformance

- **`packaging-and-patches.md`:** the required fields are present in every archive recipe (`PKG_SHA256` in 235 of 235 at top level). `tools/pkgcheck` passes all 243 with the tree's copy and with T6's widened copy (P7). The one recipe that breaks the checksum rule does so in its override, `projects/ROCKNIX/packages/devel/libfmt/package.mk:11` (`PKG_SHA256=""`, F-01), outside this slice's paths and inside its rows.
- **`fork-workflow.md` § When to merge up:** `tools/fork-package-freshness` should exit 0 before an upstream PR; today it exits 1 on four of this slice's 13 (F-06 to F-09). The 16 fork-own recipes sit under `packages/`, which upstream refuses (#645, F-10).
- **`device-builds.md` § A build that fetches its own dependency:** nothing here was read as a fetch outside the recipe's own `PKG_URL`; no build ran, so the meson-wrap check is not made here.
- **D-WORKFLOW-193/194:** the decision stands; its count does not. The archive versions without a checksum are **six**, not five: `libfmt` 9.1.0 joins the five. D-WORKFLOW-194's per-branch test looked for a `PKG_SHA256=` line in each branch and counted `PKG_SHA256=""` as one. That needs a new register row, refining D-WORKFLOW-194's count the way D-WORKFLOW-194 refined D-WORKFLOW-193's; the coordinator writes it (D-WORKFLOW-189), and `05` names the item.

## 3.3 Spec fidelity

Against the brief (version 2):

- **Every count in § 2 reproduced exactly:** 266 / 7,612 / 250-16 / 256-7-3 / 243; 13 / 3 / 227; 942; 46 with patches; 0 shadowed; 8 without a checksum; 243 PASS twice; 226 / 220 / 149 / 227 / 151 built.
- **One claim did not hold: "`ntfs-3g_ntfsprogs` has no build directory in any root."** It has one in three (`ntfs-3g_ntfsprogs-2022.10.3`). The brief's version-stripping `sed` (`s/-[0-9][0-9a-zA-Z._+-]*$//`) starts its match at the first `-<digit>` in the directory name, which is `-3g`, and leaves `ntfs`. It is the only one of the 243 names that contains `-<digit>`. Read by each root's `.stamps` instead, the record agrees with the plans on every name except `btrfs-progs` on GENERIC_X64 (F-11). The seven names Q6 was to settle are therefore six, all virtual.
- **One expectation was met only in form: "the expected count of archive recipes without a checksum here is 0."** It is 0 for the 243 recipes as written. For the 243 as built, it is one (`libfmt`, through its override).

## 3.4 Platform conformance

Can this be done on the VM? **No**, by brief § 5: the bench is the tree, the record and the release sources. Nothing here ran on a guest, a device or a cloud. What a build would meet was read from the plans (`tools/viewplan` in this worktree) and the five M7 roots' listings (read only).

## 3.5 Cross-system interaction audit

### Interaction: the fetch (T5's `get_archive`) x the sweep x `libfmt`'s override

- **Shared state:** the recipe's effective `PKG_SHA256` after `config/options`, and the cache's `.sha256` stamp.
- **At `8ebaf8daad`:** `get_archive:6` skips the stamp check when `PKG_SHA256` is empty, and `:45` accepts any download when it is empty. `libfmt` 9.1.0 is fetched unverified on GENERIC_X64 and H700.
- **At T5's tip `52e6794ba7`:** `get_archive:7-9` dies when `PKG_SHA256` is empty, *before* the cache is read. So every GENERIC_X64 and H700 build stops at `libfmt`, warm cache or not. The merge order (T5 before T7, the lane pointer's merge notes) brings the failure to `next` before this slice's fixes.
- **The override is an orphan.** ROCKNIX deleted `projects/ROCKNIX/packages/devel/libfmt` after the base (`6103571f67`, PR #3470, 2026-10-11; #644 finding 16's class), so the next base merge also ends the defect. The order of T5's merge and the base merge decides which fix is needed.
- **The seam's guard was the count.** T5's E6 gave the five it counted their checksums. The sixth was invisible to a test that asked whether a branch *has* a `PKG_SHA256=` line rather than whether the branch's value is non-empty. **F-01.**

### Interaction: the freshness tool (D-WORKFLOW-024) x the 13

The tool's set under `packages/` is exactly the 13 recipes the fork added (P2): no orphan, no extra (#644 finding 16 does not reach this slice). It resolved all 13; four BEHIND are each a single patch release (`brotli` 1.2.1, `ruby` 3.3.13 in its declared series, `glib-networking` 2.90.1, `webkitgtk` 2.54.2). Its CURRENT verdicts were spot-checked against the hosts it names: `libsoup` 3.8.0 is the newest even-minor release in GNOME's `cache.json`, and `qrencode`'s v4.1.1 is `fukuchi/libqrencode`'s latest release. Two rule-4 cases: the tool says BEHIND on four rows, so it can say it; and `fresh-list.txt` equal to the fork-added 13 is the cross-check A4 asks for, not the source.

### Interaction: `shadowed_by` (T23's filter) x this set's 0

The inventory marks a generic recipe *shadowed* only when an override replaces it without sourcing it (`installer` is the case at hand: `packages/tools/installer` unreached, `projects/ROCKNIX/packages/tools/installer` reached). An override that sources the generic leaves the generic `shipped`, which is right for reach. So T23's 1,604 rows hold no recipe that a sourcing override reaches, and this slice holds all 47 such generic recipes. The effective-pin column is this slice's answer; the inventory's is F-12.

### Interaction: #645 x the 16

#645's 21 files are 16 recipes (this slice's) and five others. Three are patches (`woff2`'s one, `webkitgtk`'s two), in `patches-and-configs`. `packages/linux/package.mk` is `devices`. `packages/tools/installer/package.mk` is unreached and T23's. Each of the 16 has a proposed row in `04` § Q7. The patches move with their recipes, which the rows say, so the coordinator's #645 post covers 19 of the 21; the other two are T8's and T23's.

## The futro's predictions, checked

- **S-1 to S-11 held:**
  - no remote was added;
  - no bump was made;
  - no `update-pkg` or `update_packages` was run;
  - the API loop ran serially with the budget read;
  - `pkgcheck` ran in this worktree;
  - nothing went under `/tmp`;
  - every time was taken from `date -u`.
- **S-12 held:** `PKG_SITE`'s host was not used as the signal. The 75 GitHub repositories the URLs name were read for `fork`, `archived` and rename, which found `populatefs`'s personal fork and `oniguruma`'s archive (F-15).
- **S-5 did not arise:** `pkgcheck` failed nothing.
- **A2's "a 404 is a `bug` in #849's shape" held with one refinement:** ROCKNIX's mirror holds the right bytes for all four gone URLs, so none of the four fails a build from an empty cache. The bugs say so.
- **A5's seventh name was the brief's `sed`, not the record** (§ 3.3).
- **A6's expected 0 held for the recipes as written and missed the one that matters as built** (§ 3.5, F-01).
