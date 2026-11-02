# T43 #690 bounded source preparation

2026-11-02T18:46:06Z. Codex, actual harness session `01a19d11-dda5-72e3-86f9-416f36341c24`, P1 lane `m6-p1-survey`, wN:p3, returning to wN:p2. Authority: #690 comment [6585182159](https://github.com/pixelelated/distribution/issues/690#issuecomment-6585182159). This is source preparation, not a new audit, planning decision or dispatch verdict.

Read complete #690 (one comment at capture) and the current M6 milestone plan/order. The issue is OPEN, titled `M6.P2 E1054/T43`; its generated opening still describes future re-parenting from #339. The 17:58 milestone recovery paragraph predates the subsequent T39 dispatch/T41 acceptance; this report uses the user's latest dispatch statement and the immutable accepted packets for those facts. T43 remains after T42. No tracker text was changed.

## Exact membership and identity

Compared P1 `2174265e9cc1b248c0fbe27fa101875984d46d6b` with coordinator `7f25f9f78b3da3a6b2c893397b58a3ce5a04be75`.

- Canonical ID `patches-unshipped`: area `patches-and-configs`, selector reach `unshipped` or `n/a`, evaluated with the pinned selector implementation. Actual population: **432 unshipped, zero n/a; 328,516 logical Git-blob lines**. All are distribution/vendor-carried; no overlap/shadow marker.
- Membership rows, all 432 modes/blobs, and all five input files (`inventory.json`, `slices.json`, `areas.json`, `order.md`, inventory tool) are identical at both refs. Zero missing paths and zero changed member modes/blobs. The inventory remains its recorded snapshot at `eb4763e3cc`; this comparison did not generate new build plans or claim refreshed reachability.
- Sorted newline-terminated path-list SHA256: `8ec78172f80d28d28117eaf1efefe2c769ea58d07a57c3a16616b595fb429912`.
- Exact 432-row mode/blob manifest: `members.tsv`, SHA256 `ccbbe1543349e51f56545afc3e96aadc3fc3e965e19b1fdb18731ee809cc083e`. Its blob column applies to both refs. `results.json` records input Git blob IDs/SHA256, selector function ranges/digests, comparisons and groups.

| Population | Paths | Logical lines |
| --- | ---: | ---: |
| Linux-source patches | 346 | 222,494 |
| Kernel configurations | 12 | 101,229 |
| Patches to other source packages | 74 | 4,793 |
| Total | 432 | 328,516 |

The 74 include nine `mali-bifrost` module patches; “other source” is a recipe boundary, not a claim that these are unrelated to the kernel. All 420 patch-suffixed paths comprise **418 regular patches plus two symlinks**. Alongside the 12 regular configurations, modes are **428 × 100644, 2 × 100755, 2 × 120000**. No binary-content exception was needed for the inventory line counts.

Both executable-mode patches are retained as facts, not executed or changed:

- `projects/ROCKNIX/devices/RK3588/patches/linux/007-add-ion-allocator.patch`, blob `20a6039cc9cd2969349f85139417810f85a412de`, 5,163 lines.
- `projects/ROCKNIX/packages/audio/alsa-ucm-conf/patches/SM8250/0002_Add-Retroid-Pocket-SM8250-configuration.patch`, blob `e6e1c640fff51b4e5b98362be09be3842d76ef1b`, 184 lines.

**Fork-written set: empty, 0 paths / 0 lines.** Every `tier_note` is null, and the selected paths have an empty net diff against the inventory's fork base `c445081a59518f37d9776e5412dd7b14910696f7` at both refs. This establishes the requested inventory/base-delta set, not a new authorship audit.

**Line semantics:** 10,690,267 literal blob bytes; 328,512 newline bytes versus 328,516 logical lines. The two symlink blobs and two regular patches lack final newlines: SM8250 `0100-revert-force-16bit-audio.patch` and SM8750 ALSA `0001_SM8750-AYN-Odin3.patch`. Every per-path logical count agrees with inventory. Regular-member content alone is 328,514 lines. Following the two links per member would instead count 328,585 lines (328,583 newline bytes), duplicating referent content; that is not the membership total. Nothing was exported or filesystem-dereferenced.

## Groups and source/pin boundaries

There are **72 containing directories**, **31 path-prefix groups**, and **28 distinct buildable-by combinations** over **21 target/architecture configurations**. Per-configuration counts overlap: they are in `results.json:per_target_nonadditive`, not additive membership. All exact directory/group lists and line totals are retained there.

The physical target directories account for **377 paths / 324,591 lines**:

| Target directory | Paths | Lines | Kernel recipe pin at both refs |
| --- | ---: | ---: | --- |
| AMD64 | 4 | 12,529 | 7.1.2 |
| RK3326 | 25 | 27,895 | 7.1.2 |
| RK3399 | 10 | 7,604 | 6.18.49 |
| RK3566 | 41 | 11,164 | 7.0.2 |
| RK3576 | 24 | 15,132 | 7.0.2 |
| RK3588 | 18 | 143,156 | b8e62bed74766b6c8c423a767b35495e78b64caf |
| S922X | 46 | 17,004 | 6.18.49 |
| SM4450 | 45 | 16,993 | 7.2 |
| SM6115 | 47 | 15,427 | 7.2 |
| SM8250 | 37 | 19,034 | 7.2 |
| SM8650 | 21 | 12,407 | 7.2 |
| SM8750 | 59 | 26,246 | 7.2 |

The remaining **55 paths / 3,925 lines** sit in 19 `projects/ROCKNIX/packages/` prefixes: gamepadtester, mangohud, oga_controls, alsa-lib, alsa-ucm-conf, pipewire, azahar-sa, ppsspp-sa, xemu-sa, libmali, mesa, vulkan-wsi-layer, linux, ffmpeg, rkmpp, atf, wlroots, weston and weston-kiosk-shell-dpms. No T43 member is under generic `packages/` or another project.

The six `linux/patches/mainline-rockchip/` members total **791 lines**. Their inventory consumers are both arches of RK3326/RK3399/RK3566/RK3576. The kernel recipe adds `mainline-rockchip` for RK*, but RK3588 resets `PKG_PATCH_DIRS` in its vendor-pin branch. The largest member is RK3588 `999-MALI-rockchip-upgrade-bifrost-DDK-to-g21p0-01eac0-fr.patch`, **125,129 lines**; it remains one upstream-carried member.

`recipes.json` lists **31 direct source recipes**, their exact pins/conditional selector excerpts, modes/blobs/SHA256 at both refs, canonical owner and member-directory mapping. All 31 recipe blobs are unchanged between the refs. They are context, not T43-owned source:

| Recipe owner | Recipes | T43 members mapped to those recipes |
| --- | ---: | ---: |
| T25 `devices-unshipped` | 12 | 25 |
| T8 `image-packages` | 10 | 36 |
| T30 `emulators-standalone` | 3 | 3 |
| T23 `packages-dead-ends` | 5 | 10 |
| T11 `device-generic-x64-and-kernel` | 1 | 358 |

Useful pin distinctions for the brief:

- T11's override `projects/ROCKNIX/packages/linux/package.mk:16–53` supplies the kernel pins above. The 12 conf headers match the corresponding release strings (`7.2.0` headers for `7.2`); RK3588's header is 6.1.75 against the vendor commit, whose archive contents were not examined. Config source is not the final built `.config`: the recipe mutates options, including hostname at line 160. SM8750's conf literal `ROCKNIX` at line 51 is T25's retained lead, not a newly established image defect.
- RK3566 Generic/Specific loader recipes both pin `v2026.01`; their five patch members belong to those source recipes. The separate T25-owned `u-boot` wrapper has version `1.0`, empty URL and subdevice dependencies; it is not their source pin.
- `mali-bifrost` pins `39da994bb6fc8819e5e8c1873907dd21d17e53c1`; its nine patches target the module's source, not the Linux archive.
- `libmali` defaults to `0fe30426b822699f0a660268a6040fdafce229d1` but RK3326/RK3566/RK3576 switch to `4233031d818e97a19e8a9cdbbd5c15795ededd93` and `patches/next`; wlroots' `libmali` patch selects `0.19.3-rk`. ATF's RK3399 patch uses the `*)` pin 2.10.0, not H700's 2.12.0.
- `scripts/unpack:136–199` expands recipe/architecture/version/project/device patch patterns and follows file links through `-f`, then reads their content. The inventory helper at `382–402` identifies selected directories, not successful applications. Its pure slice selector at `1211–1246` determines ownership; neither function proves applicability. No shell recipe/config or unpack code was executed.

## Symlinks and adjacent slices

Within T43, MangoHud's two SM8650 links resolve to T43 SM8750 regular members:

| SM8650 link basename | Literal target | Referent lines / blob |
| --- | --- | --- |
| 0001-SM8650-GPU.patch | ../SM8750/0001-SM8750-GPU.patch | 34 / d8c3456058663ff5100380282c2a3e74a133af06 |
| 0002-SM8750-Battery.patch | ../SM8750/0002-SM8750-Battery.patch | 37 / 84176a1dad503fe03ff3535a552b454c60cf859f |

T42 separately owns `projects/ROCKNIX/packages/apps/mangohud/patches/SM8550/0002-SM8750-Battery.patch`, link blob `77f00f11a744931e14787c8d7f033a8cab866229`, pointing to that same 37-line T43 referent. All these modes/blobs match across both refs. MangoHud's recipe at both refs pins `992103e4fb744897826de04ea00a2f71e7018214` (comment v0.8.4), adds `qualcomm` and `${DEVICE}`, and conditionally `batteryplus`.

**Consequent wording limit:** “unshipped” is canonical path-row classification, not proof that these bytes have no shipped consumer. Preserve T43 ownership of the SM8750 referent and T42 ownership of the SM8550 link. Its shipped consumer is explicit source context; no patch application or runtime battery behavior is claimed.

Membership intersections with T41's 107, T42's 384 and T40's 778 are all empty. The entire patch population used by an unshipped target is not necessarily contained in T43: shared patches selected by shipped/test plans remain T41/T42 rows. T43's 12 confs exclude H700 (T27), GENERIC_X64 (T11) and SM8550 (T41).

## Accepted context retained, without replay

Exact object identities and source hashes are in `context-inputs.json`:

- **T25:** `9b9be6a9481e4e9ee5b9d97f6c7bb72eda3ca3b4`, `2026_10_25-epic-m6-devices-unshipped/02-forward-audit.md`, targets/pins and F-01/F-03/F-05/leads. Its per-target patch counts match the 12 directory groups above after adding one conf each. RK3326/RK3566 remain the held first widening (D185), not shipped. #1101 records unpack-edge limits; do not turn inventory reach into a universal proof of non-use. It retains the RK3576 `cellwise,cw221X` consumer match and SM8750 hostname lead; neither is a fresh defect verdict here.
- **T11:** `47672fe4a04fc3b69dee9f0381fbc9f076b891e5`, `2026_10_25-epic-m6-device-generic-x64-and-kernel/02-forward-audit.md`, configuration and Stage-C F-09 context. GENERIC_X64's config and shared kernel/firmware recipes remain its ownership. Its existing built-config findings are historical evidence, not tests performed here; preserve GENERIC_X64's version branch at integration.
- **T27:** `0ac98afe434c0429bace5f239482e5de0e0bc394`, `2026_10_25-epic-m6-device-h700/02-forward-audit.md`, pins/configuration. H700's config and U-Boot sources stay there. Its ATF URL/checksum pairing context also reaches RK3399 via T25; do not combine a later URL with an earlier archive checksum.
- **T41:** `7e5d1546712df2eb79c585fce663186770d1ceb9`, `2026_11_02-epic-m6-patches-shipped-kernel/02-forward-audit.md:318–342,548–565`, plus the coordinator-retained Stage-B acceptance. The accepted packet has 107 unchanged source rows and 120 normal applications over 106 patch paths. Those accepted applications are not T43 applicability evidence. D222 makes complete normal application authoritative and dry-run diagnostic; no method was replayed here.
- T41 hands forward `mainline-rockchip/`, the 12 confs, upstream `7.2.6/` additions and the polldev move to RK3326. At its pinned upstream context **651150fc88**, the kernel's actual version for RK3566/RK3576/S922X is **7.2.11**, with **7.2.6 as a patch-directory selector**, not the source pin; RK3399 is 6.18.54. These are later-context inputs, not members or pins silently imported into either requested snapshot. Integration #563/#559 owns the upstream move/additions. The firmware recipe is T11-owned (the T41 brief's later correction supersedes its historical T42 wording).
- **T42:** coordinator-retained P1 report under `docs/qa-logs/2026-11-02-m6-resume/t42-membership/` confirms 384 native members and the MangoHud seam. The separate 50 inherited comparisons are not additions to T43 membership.

Concrete brief inputs are therefore the exact 432-row manifest; its patch/config/link and line-count distinctions; directory versus overlapping consumer groups; empty fork-written set; 31 immutable recipe boundaries with conditional pins; the shipped MangoHud consumer; and the accepted contexts above. D209 says this table removes nothing and edits no recipe. Current authority also excludes removal proposals. Coordinator retains the brief, criteria, ownership row, acceptance and dispatch; this report does not choose those.

## Commands and artifacts

Run the two small Python readers from this directory. They use `git show`, immutable `ls-tree`, `rev-parse` and scoped `diff` only; the inventory tool's five inspected pure selector functions are extracted with AST, without its CLI/generator/plan runner. They write only this private directory:

```sh
python3 /tmp/m6-t43-source-prep-690.W5n0f6/reproduce.py
python3 /tmp/m6-t43-source-prep-690.W5n0f6/recipes.py
```

Exact source/readback commands used for the boundaries (all from the launch repository):

```sh
gh issue view 690 --repo pixelelated/distribution --json number,title,body,state,milestone,comments
git show 7f25f9f78b:docs/reviews/order.md | sed -n '/^### T43\./,/^### T44\./p'
git show 7f25f9f78b:tools/renovation-inventory | sed -n '130,158p;382,499p;1211,1248p'
git show 7f25f9f78b:projects/ROCKNIX/packages/linux/package.mk | nl -ba | sed -n '1,92p;150,192p'
git show 7f25f9f78b:scripts/unpack | nl -ba | sed -n '136,199p'
git show 7f25f9f78b:config/functions | nl -ba | sed -n '785,803p'
git show 7f25f9f78b:projects/ROCKNIX/devices/RK3566/packages/u-boot/package.mk
git show 651150fc88:projects/ROCKNIX/packages/linux/package.mk | nl -ba | sed -n '16,57p'
git show 9b9be6a948:docs/audits/2026_10_25-epic-m6-devices-unshipped/02-forward-audit.md | sed -n '109,129p;148,174p;291,307p;328,356p'
git show 47672fe4a0:docs/audits/2026_10_25-epic-m6-device-generic-x64-and-kernel/02-forward-audit.md | sed -n '94,108p;136,146p;318,328p'
git show 0ac98afe43:docs/audits/2026_10_25-epic-m6-device-h700/02-forward-audit.md | sed -n '65,93p'
git show 7e5d154671:docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/02-forward-audit.md | sed -n '318,342p;548,566p'
git show 7f25f9f78b:docs/decision-register.md | rg '^\| D-WORKFLOW-(185|209|221|222) '
GIT_OPTIONAL_LOCKS=0 git status --short
```

The manifest includes every member's mode/blob, literal byte/line size and recorded consumer set. `results.json` contains all directory and target tables; `recipes.json` contains exact recipe pins and ownership; `context-inputs.json` hashes the accepted inputs; `issue-690.json` retains the full owning issue, authorization comment and milestone response. `SHA256SUMS` seals the scratch artifacts. Launch worktree remains clean at accepted P1. No source/ledger/tracker/kit edit, source export/extraction, config sourcing, fetch, runtime/provider/device/cloud action, historical check replay or permission answer occurred. Bounded preparation complete; stop at return to wN:p2.
