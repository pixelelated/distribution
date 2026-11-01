Independent audit (depth: independent, one seat GPT-6 Astra at `max`) of the EmulationStation recipe and themes in the distribution -- the 15 paths of `projects/ROCKNIX/packages/ui/**` (the slice's ownership row D-WORKFLOW-217) at `2174265e9c`, with the ES pin `16dbac5211` read by hash. Artifacts: `docs/audits/2026_11_01-epic-m6-es-recipe/` (`00` to `05`, `second-opinions/`, `stage-a` to `stage-c`, `guest-cycle/`, `tools/`), on `feature/m6-es-recipe-684`.

**What the checker shows:** `tools/t37-checks.sh` fails at the tip on four defects nothing caught before -- the `es_systems.cfg` link (PL-01), the unreached patch directory (PL-02), the bare `PKG_NEED_UNPACK` (PL-03), the no-op `rm` (PL-04) -- `TOTAL: 55 of 60 assertions`; a fixed scratch fixture passes `66 of 66`, and 15 of 15 mutations are caught by name (`stage-c/failfirst.out`).

**The seat:** 3 confirmed, 8 confirmed with narrowing, 5 cannot tell, 0 refuted, 9 added (G-1 to G-9), each read at its source by the lane; three of the lane's claims corrected (`04` § Second opinion). Pre-issue lint PASS.

## Punch items (acceptance checklist)

Each item is ticked when `05-punch-list.md`'s Phase 7 gate records its outcome with its evidence; a fix's evidence is the checker's PASS line for its assertion at `fixed-at` (`fix-fixture`), then the integration's image (`fix-image-pending`).

- [ ] PL-01 (Medium, L-03): the `es_systems.cfg` fallback link points at a build-host path -- `tools/t37-checks.sh` prints `PASS step 5 no-link-to-${INSTALL}-target (L-03)` at `fixed-at`, or the item deferred to #613 with the line posted there
- [ ] PL-02 (Medium, L-02): `emulationstation/patches/x86_64/` is reached on no device -- the checker prints `PASS step 4 patch-dir-reached patches/x86_64/` (or the patch moved by T40) at `fixed-at`, or the item deferred to #1072, after the patch's GPU call is corrected
- [ ] PL-03 (Low, L-19): `PKG_NEED_UNPACK="busybox"` names no directory -- the checker prints `PASS step 5 ... PKG_NEED_UNPACK-words-are-directories (L-19)` for both listed devices at `fixed-at` (its bug below)
- [ ] PL-04 (Low, L-04): the `rm` of `resources/logo.png` runs before the directory exists -- the checker prints `PASS step 5 no-rm-before-its-directory-is-filled (L-04)` at `fixed-at` (its bug below)
- [ ] PL-05 (Low, L-01): upstream's ARMSX2 *vulkan driver* filter was dropped by four merges -- a scratch fixture of the filter over `es_features.cfg` counts `0` such features outside the five Turnip devices and `1` on them at `fixed-at` (its bug below)
- [ ] PL-06 (Low, L-09): fribidi declared nowhere; the candidate's binary does not link it -- the pause's ruling under D-WORKFLOW-216 recorded in `05`, and the integration's configure-log item named in `02` § What the integration inherits
- [ ] PL-07 (Low, L-08): a missing French catalog would install silently -- `05` records the pause's ruling (a failing install line, or as written)
- [ ] PL-08 (Low, L-05): `HFS_DEV_LOGIN` builds a scraper with no `USING:` line -- a sandboxed sourcing of the recipe with four placeholder names prints four `USING:` lines at `fixed-at`, or `05` records it as written
- [ ] PL-09 (Low, T2 PL-029): `--log-path` is parsed by nothing -- `05` records it kept with its reason and a #585 line
- [ ] PL-10 (Low, L-10, L-21): the two checkers that would measure these recipes pass over nothing -- the Backlog issue the coordinator files, named in `05`
- [ ] PL-11 (Low, L-06): `sed "s#-#_##g"` replaces only the first hyphen -- `05` records it as written with its #585 line
- [ ] PL-12 (Low, L-07): the pre-generated locale's failure is silent in its status -- `05` records it as written
- [ ] PL-13 (Low): `lowerdeck` is behind its author's `HEAD` -- `05` records the finding with its dated read
- [ ] PL-14 (Low): six upstream `ui/` changes and two overlaps wait for the distribution merge -- `05` defers it to the merge and #791
- [ ] PL-15 (Low, L-17, L-18): two rules describe the recipe as it is not -- the coordinator's sweep named in `05`
- [ ] PL-16 (Low): the state check's payload route cannot run on this host -- `05` names the tool note
- [ ] PL-17 (Low, G-6): a verbose build prints the compiled-in pair in its compile commands -- `05` records the ruling (a Backlog candidate or a record, under D-INFRA-006)
- [ ] PL-18 (Low, G-7): the autostart alias repairs neither a real directory nor a wrong link -- `05` records it as written, or the checker's assertion for a contained fix
- [ ] PL-19 (Low, G-8): an empty serial-number read is treated as a changed device -- `05` records it for upstream with its #585 line

## Bugs filed from this audit

- #1382 -- PL-03 (Low): `PKG_NEED_UNPACK="busybox"` names no directory
- #1383 -- PL-04 (Low): the `rm` of `resources/logo.png` runs before the directory exists
- #1384 -- PL-05 (Low): four merges dropped upstream's ARMSX2 *vulkan driver* filter
- PL-01 is carried on #613 and PL-02 on #1072 (a line on each naming what T37 adds); PL-06 is D-WORKFLOW-216's item, inherited by the integration (`02` § What the integration inherits item 4).

Punch list detail and proposed dispositions: `05-punch-list.md`. Second opinion: `04-analysis.md` § Second opinion.
