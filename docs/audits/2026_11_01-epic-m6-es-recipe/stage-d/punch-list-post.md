**T37 stage D: the punch list with a proposed disposition per item (02:21 UTC 2026-11-01).** Tip `264a39f6d7`. Audit issue **#1381**, a sub-issue of #684 (19 checkboxes, `box-check` `0 fail`). Bugs **#1382** (PL-03), **#1383** (PL-04) and **#1384** (PL-05), each `box-check` `0 fail`. T37's lines are on **#613** (PL-01, comment 6552262443) and **#1072** (PL-02, comment 6552262614). `tools/lint-audit-artifacts ... --phase pre-issue`, run both plain and with `--issue 1381`, prints `PASS pre-issue artifacts (does not certify resolution)`. Every disposition below is **proposed**; the pause rules them.

| Item | Severity | Q | Finding | Tracked | Proposed disposition |
| --- | --- | --- | --- | --- | --- |
| PL-01 | Medium | Q2 | The `es_systems.cfg` fallback link points at a build-host path | #613 | Resolve in stage E (a contained recipe edit at `:101`, if #613 is routed here); else Defer to #613 |
| PL-02 | Medium | Q6 | `emulationstation/patches/x86_64/` is reached on no device | #1072 | Defer to #1072 (T40 corrects the patch's GPU call first; then T37's `PKG_PATCH_DIRS+=` line or T40's rename) |
| PL-03 | Low | Q3 | `PKG_NEED_UNPACK="busybox"` is a bare word, so busybox never moves the ES stamp | #1382 | Resolve in stage E (#1382): `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"` |
| PL-04 | Low | Q2 | The `rm` of `resources/logo.png` runs before the directory exists | #1383 | Resolve in stage E (#1383): the `rm` moved after `:82` |
| PL-05 | Low | Q7 | Upstream's ARMSX2 *vulkan driver* block was dropped by four merges | #1384 | Resolve in stage E (#1384): upstream's five ARMSX2 lines restored after `:128` |
| PL-06 | Low | Q3 | The candidate's ES does not link fribidi; the recipe declares it nowhere | D-WORKFLOW-216; the integration's configure log | Resolve in stage E: `fribidi` declared in `:13` (the seat's choice; the probe stays optional), the configure-log proof inherited by the integration |
| PL-07 | Low | Q2 | A missing French catalog would install silently | #1381 (this audit) | Resolve in stage E: a `makeinstall_target` line that fails when the French `.mo` is missing |
| PL-08 | Low | Q4 | `HFS_DEV_LOGIN` builds a scraper with no `USING:` line | #1381 (this audit) | Resolve in stage E: `HFS_DEV_LOGIN` added to the loop at `:42-44` (names only) |
| PL-09 | Low | Q2 | `--log-path /var/log` is passed to ES and parsed by nothing | #1381 (this audit) | Record: kept with its reason, a #585 line |
| PL-10 | Low | Q7 | The two checkers that would measure these recipes pass over nothing | a Backlog the coordinator files | Defer to a Backlog the coordinator files |
| PL-11 | Low | Q2 | `sed "s#-#_##g"` replaces only the first hyphen of `DEVICE` | #1381 (this audit) | Record: as written, a #585 line |
| PL-12 | Low | Q2 | The pre-generated locale's failure is silent | #1381 (this audit) | Record: as written (a best-effort cache with a fallback) |
| PL-13 | Low | Q5 | `lowerdeck` is behind its author's `HEAD` | #1381 (this audit) | Record: the dated currency finding; the bump at the integration |
| PL-14 | Low | Q7 | Upstream's six `ui/` changes and two overlaps wait for the distribution merge | the distribution merge; #791 | Defer to the distribution merge (`release-candidates.md` step 0) and #791 |
| PL-15 | Low | Q1 | Two rules describe the recipe as it is not | the coordinator's sweep | Defer to the coordinator's doc sweep |
| PL-16 | Low | Q4 | `tools/pixelelated-state-check --payload` cannot run on this host | #1381 (this audit) | Record: the tool note (`02` § What the integration inherits item 9) |
| PL-17 | Low | Q4 | A verbose build prints the compiled-in pair in its compile commands | #1381 (this audit) | Record under D-INFRA-006 (a mask on the verbose path is a Backlog candidate for the coordinator) |
| PL-18 | Low | Q2 | The autostart alias repairs neither a real directory nor a wrong link | #1381 (this audit) | Record: as written (upstream's legacy alias) |
| PL-19 | Low | Q2 | An empty serial-number read is treated as a changed device | #1381 (this audit) | Record: for upstream, a #585 line |

_19 items, generated from `05-punch-list.md` at the stage-D commit._

**Since stage C:** **PL-05 is lowered to Low.** The launcher uses ARMSX2's bundled Turnip only when its ICD file exists (`armsx2-sa/scripts/start_armsx2.sh:215-218`). So off the five Turnip devices, the row upstream's filter hides offers two choices that change nothing: a misleading row, not a broken launch. The punch list is now **2 Medium and 17 Low**.

**The proposed stage-E stream:** one stream, every edit in `projects/ROCKNIX/packages/ui/emulationstation/package.mk`, so only the ES recipe's stamp moves. Never `:5` or `:6`. Each edit is proven `fix-fixture` and named `fix-image-pending`:

- **PL-01**: the device path at `:101`, if #613 is routed here. Proof: the checker's L-03 assertion.
- **PL-03** (#1382): `$(get_pkg_directory busybox)`. Proof: the L-19 assertion and the stamp compare.
- **PL-04** (#1383): the `rm` moved after `:82`. Proof: the L-04 assertion.
- **PL-05** (#1384): upstream's five ARMSX2 lines. Proof: the `xml.etree` fixture, `0` outside the five and `1` on them.
- **PL-06**: `fribidi` declared in `:13`, with the probe staying optional. Proof: the effective-depends read; the configure-log proof is inherited by the integration.
- **PL-07**: a `makeinstall_target` line that fails without the French `.mo`. Proof: a new checker assertion, FAIL-first.
- **PL-08**: `HFS_DEV_LOGIN` added to the loop. Proof: a sandboxed sourcing counting `USING:` lines with placeholder names assembled at run time, 4 after the fix and 3 before.

Every edit is followed by `tools/pkgcheck emulationstation` after its `find` positive, the checker and the stamp compare.
