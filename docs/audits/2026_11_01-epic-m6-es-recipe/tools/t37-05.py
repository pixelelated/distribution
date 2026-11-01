#!/usr/bin/env python3
"""Write 05-punch-list.md (T37, #684) from one item table: each item's section, the Phase 7
resolution gate (every item Open before stage D's issue exists) and the punch_index YAML
(question: in the brief's § 4 numbering -- Q1 the pin, Q2 the build options and install steps, Q3
the dependencies, Q4 the credentials, Q5 the themes and lowerdeck, Q6 the patches, Q7 currency and
structure). Asserts unique ids, a known severity, question and proof per item, and the three views
agreeing; exits 1 on a drift (--drift drops one item from the gate to show it fires).
    python3 -B -I t37-05.py <audit folder> [--drift]"""
import pathlib, re, sys

SEV = ("Critical", "High", "Medium", "Low")
PROVED = ("tree", "history", "tool-run", "fixture", "guest", "design")
ITEMS = [
 dict(id="PL-01", title="The `es_systems.cfg` fallback link points at a build-host path", sev="Medium", cat="Install step",
      q="Q2", src="L-03; #613", lines="`emulationstation/package.mk:101`; `scripts/build:140`; `config/functions:1380`",
      owner="T37 (the recipe's line, if the coordinator routes #613 here); upstream's form",
      what="`ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/...`: in `makeinstall_target` `INSTALL` is `$BUILD/install_pkg/emulationstation-<pin>`, and neither `scripts/install` nor `scripts/image` rewrites a link, so an image built from the tip carries `/etc/emulationstation/es_systems.cfg` pointing into the build host. The candidate image's link is the corrected `/usr/config/...` and resolves (G-03), because its own recipe differs (ruling (h)).",
      disp="take up as #613: the device path in this slice's stream if routed (`fix-fixture` by the checker's L-03 assertion, `fix-image-pending`); a #585 line",
      proved="tool-run"),
 dict(id="PL-02", title="`emulationstation/patches/x86_64/` is reached on no device", sev="Medium", cat="Patch directories",
      q="Q6", src="L-02; #1072", lines="`emulationstation/patches/x86_64/`; `scripts/unpack:127-128`, `:137-160`",
      owner="T37 (the recipe's `PKG_PATCH_DIRS`); T40 (the patch's content and place, #1072)",
      what="`PATCH_ARCH` is `x86` for an `x86_64` target and the recipe sets no `PKG_PATCH_DIRS`, so `cpugov.patch` applies on none of the 15 devices (`stage-b/reach-15.out`); its string is absent from the candidate's binary (G-05). Added by `40fce2a089 2026-08-20 amd64: wip am64 changes`.",
      disp="take up as #1072, **after** T40 corrects the patch's GPU call (the seat's G-1, confirmed: its `+` lines call `get_available_cpu_governors` 4 times and `get_available_gpu_governors` 0 times, so reaching it as it is wires the CPU list into the GPU rows): the pause chooses T37's `[ \"${ARCH}\" = \"x86_64\" ] && PKG_PATCH_DIRS+=\" x86_64\"` (appending, the seat's G-2; `TARGET_ARCH=\"${ARCH}\"` at `config/options:36`, so the test is the unpacker's) or T40's rename to `patches/x86/`; only a build proves the patch applies",
      proved="tool-run"),
 dict(id="PL-03", title="`PKG_NEED_UNPACK=\"busybox\"` is a bare word, so busybox never moves the ES stamp", sev="Low", cat="Build order",
      q="Q3", src="L-19", lines="`emulationstation/package.mk:14`; `config/functions:1114`, `:1126`",
      owner="T37; upstream's line (`9f1fab30f6`)",
      what="`calculate_stamp` adds the word to its `find -L` paths relative to the root, where `busybox` names nothing (`0` files); the framework and upstream recipes pass a directory (`$(get_pkg_directory vdr)` in the vdr plugins' recipes, `config/functions:1322-1333`).",
      disp="rule 6: `PKG_NEED_UNPACK=\"$(get_pkg_directory busybox)\"` (the fixture passes `pkgcheck` and the checker with it), or the line dropped if no ES build needs busybox; a #585 line",
      proved="tool-run"),
 dict(id="PL-04", title="The `rm` of `resources/logo.png` runs before the directory exists", sev="Low", cat="Install step",
      q="Q2", src="L-04", lines="`emulationstation/package.mk:79`, `:81-82`; the pin's `es-core/src/Splash.h:17`",
      owner="T37; upstream's order (`9f1fab30f6`)",
      what="The line removes nothing, so the pin's `logo.png` ships (G-05, 283,835 bytes). Corrected after the seat: under `ROCKNIX` the default splash is `:/pixelelated-wordmark.svg` (the pin's `Splash.h:10-11`); `:/logo.png` is the `else` branch's (`:16-17`), so the shipped file is the one the line meant to drop, and nothing in the build's splash reads it.",
      disp="a contained fix for the pause: the `rm` moved after `:82` (it then does what it says and drops an unused file), or recorded as written with a #585 note",
      proved="tree"),
 dict(id="PL-05", title="Upstream's ARMSX2 *vulkan driver* block was dropped by four merges", sev="Low", cat="Merge debt",
      q="Q7", src="L-01", lines="`emulationstation/package.mk:125-129` (`651150fc88:104-108`); `es_features.cfg:1331`, `:1333`, `:1393`",
      owner="T37",
      what="`a06539d8ec`, `049765fba0`, `fa2990c1e7` and `f370dc8787` each had an upstream parent with the two ARMSX2 lines and a result without them (`stage-b/l01-merges.out`); the tip's catalogue keeps `armsx2-sa`'s *vulkan driver* feature on every device that ships `armsx2-sa`, so devices without ARMSX2's own Turnip offer it (RK3566 of the fork's). Lowered to Low at stage D: the launcher points the loader at the bundled Turnip only when its ICD file exists (`armsx2-sa/scripts/start_armsx2.sh:215-218`), so on those devices the row's two choices change nothing -- a misleading row, not a broken launch.",
      disp="a bug candidate for the pause: upstream's five lines restored after `:128` (moves only ES's stamp). The seat's G-3 asked for the capability: upstream's list `SM4450|SM6115|SM8250|SM8550|SM8650` is exactly `armsx2-sa`'s own `armsx2-turnip` predicate (`armsx2-sa/package.mk:25-29`; SM8750 *keeps the system driver*), so the block matches the installer. The fixture with upstream's two edits in `xml.etree` at stage E",
      proved="history"),
 dict(id="PL-06", title="The candidate's ES does not link fribidi; the recipe declares it nowhere", sev="Low", cat="Build order",
      q="Q3", src="L-09; D-WORKFLOW-216; T36's G-01", lines="`emulationstation/package.mk:13`; the pin's `CMakeLists.txt:236-241`, `:462`",
      owner="T37 (the declaration, D-WORKFLOW-216); the integration (why the find failed)",
      what="ES's plan reaches fribidi only by `SDL2 -> swaywm-env -> sway -> pango -> fribidi`; T36's G-01 on the candidate reads `libfribidi` NOT linked, so its `QUIET` find failed and the built-in reordering shipped.",
      disp="the pause's ruling under D-WORKFLOW-216 (declare `fribidi` at `:13`, the seat's choice, or record the chain as the recipe's decision); lowered to Low after the seat: the fallback is designed (`CMakeLists.txt:230-233`) and an `ldd` absence alone does not show which branch compiled; the find's failure is the integration's configure log (`CANNOT` here)",
      proved="tool-run"),
 dict(id="PL-07", title="A missing French catalog would install silently", sev="Low", cat="Guard that fails open",
      q="Q2", src="L-08", lines="`emulationstation/package.mk:67-68`; the pin's `CMakeLists.txt:565-578`",
      owner="T37 (the install line); ES's CMake the integration's",
      what="Without the gettext tools ES builds no `.mo` and says only `Native language support disabled.`; the recipe copies what is there. The tools reach the build by `toolchain -> gcc:host -> autoconf:host -> gettext:host`, and the candidate carries the French `.mo` (G-03).",
      disp="a stream question at the pause (\"a loud catalog\"): a line that fails when `fr/LC_MESSAGES/emulationstation2.mo` is absent; the checker WARNs at the tip",
      proved="tree"),
 dict(id="PL-08", title="`HFS_DEV_LOGIN` builds a scraper with no `USING:` line", sev="Low", cat="Guard that fails open",
      q="Q4", src="L-05", lines="`emulationstation/package.mk:42-44`; `scripts/get_env:14`; the pin's `CMakeLists.txt:328-330`",
      owner="T37",
      what="The log loop names three of the four secret-shaped names `get_env` keeps by exception; `HFS_DEV_LOGIN` (read at the pin's `HfsDBScraper.cpp:1`, `:181`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33`) is the fourth. Corrected after the seat (G-5): `get_env:16-21` forwards every variable that is not secret-shaped, so `SCREENSCRAPER_SOFTNAME` (`CMakeLists.txt:303-305`) reaches a container build too, also unlogged.",
      disp="a stream candidate: `HFS_DEV_LOGIN` added to the loop's list (names only)",
      proved="tree"),
 dict(id="PL-09", title="`--log-path /var/log` is passed to ES and parsed by nothing", sev="Low", cat="Install step",
      q="Q2", src="T2 PL-029 (`deferred:#684`)", lines="`sources/start_es.sh:8`; `system.d/emustation.service:12`; the pin's `Paths.cpp:76-81`",
      owner="T37 (upstream's two lines)",
      what="`parseArgs` has no such branch; under `-DROCKNIX` the log path is `/var/log`, and the candidate writes `/var/log/es_log.txt` with the flag in its argv (G-04).",
      disp="kept with the reason (inert; editing either file makes an upstream-carried file fork-modified, `start_es.sh` already behind upstream); a #585 line",
      proved="guest"),
 dict(id="PL-10", title="The two checkers that would measure these recipes pass over nothing", sev="Low", cat="Guard that fails open",
      q="Q7", src="L-10, L-21", lines="`tools/pkgcheck:157`, `:169`; `tools/fork-package-freshness:16-18`, `:42-44`",
      owner="T6 (the tools); the coordinator (`EXTRA_PACKAGES`)",
      what="`pkgcheck` with a name that matches nothing prints nothing and exits 0; freshness prints its header for an unknown name and exits 0 with a missing ref, and its `--list` reaches none of the three (`lines=48 ui=0`).",
      disp="a Backlog lead for the coordinator to file, naming the three fail-opens and the three recipes' reach",
      proved="tool-run"),
 dict(id="PL-11", title="`sed \"s#-#_##g\"` replaces only the first hyphen of `DEVICE`", sev="Low", cat="Install step",
      q="Q2", src="L-06", lines="`emulationstation/package.mk:54`",
      owner="T37; upstream's line",
      what="`echo a-b-c | sed \"s#-#_##g\"` prints `a_b-c`; no device name has a hyphen today.",
      disp="recorded as written, with a #585 line (`s#-#_#g`)",
      proved="tool-run"),
 dict(id="PL-12", title="The pre-generated locale's failure is silent", sev="Low", cat="Guard that fails open",
      q="Q2", src="L-07", lines="`emulationstation/package.mk:70-75`; `sources/es_settings:26-35`",
      owner="T37; upstream's (`96d387fffd`)",
      what="`|| true` ends the `localedef` step: a failure is silent in its status, though its verbose output still reaches the build log (the seat's narrowing); `es_settings:26-35` regenerates a missing locale at first start but checks neither that result nor the export after it. The candidate has the pre-generated locale (G-03).",
      disp="recorded as written (a best-effort cache with a correct fallback); the checker's WARN",
      proved="tree"),
 dict(id="PL-13", title="`lowerdeck` is behind its author's `HEAD`", sev="Low", cat="Package currency",
      q="Q5", src="R1 C20 (2026-10-31)", lines="`lowerdeck/package.mk:5-6`",
      owner="T37 (a finding); a bump needs a fetch",
      what="Pinned at `ab735114ab` (ROCKNIX's pin too); its author's `HEAD` was `8fefe16e9c` at R1's dated read, by a count nobody made.",
      disp="a currency finding, never a bump here (ruling (b)): the bump, with its new `PKG_SHA256`, at the integration or with ROCKNIX's",
      proved="tree"),
 dict(id="PL-14", title="Upstream's six `ui/` changes and two overlaps wait for the distribution merge", sev="Low", cat="Merge debt",
      q="Q7", src="§ The currency (14 rows)", lines="the 14 files of `2174265e9c..651150fc88` over `ui/`",
      owner="`release-candidates.md` step 0 (the merge); #791 (the ES 14)",
      what="`upstream-only 6 fork-only 6 both 2`: the RK3566 patch and `PKG_PATCH_DIRS+=\" ${DEVICE}\"`, the two THP drop-ins, `start_es.sh`'s two functions, `emustation.service`'s `start.games` path and 107 lines of `es_features.cfg` the fork lacks; the ES recipe and `essway.service` changed on both sides.",
      disp="deferred to the distribution merge and #791 (a finding per row in `02` § The currency, never a merge here)",
      proved="tool-run"),
 dict(id="PL-15", title="Two rules describe the recipe as it is not", sev="Low", cat="Documentation",
      q="Q1", src="L-17, L-18", lines="`device-builds.md` § Iterating on EmulationStation; `CLAUDE.md` (patches per device)",
      owner="the coordinator's sweep",
      what="The rule names `maxengel/emulationstation-next` where `:8` is `pixelelated/emulationstation`; `CLAUDE.md`'s `patches/<DEVICE>/` holds only where a recipe sets `PKG_PATCH_DIRS`.",
      disp="the coordinator's doc sweep",
      proved="tree"),
 dict(id="PL-17", title="A verbose build prints the compiled-in pair in its compile commands", sev="Low", cat="Credentials",
      q="Q4", src="G-6 (gpt)", lines="`emulationstation/package.mk:40`; the pin's `CMakeLists.txt:307-309`, `:320-330`; `config/functions:378-382`",
      owner="T37 (the recipe's comment); the build engine T6's",
      what="CMake turns each credential variable into a `-D` definition; a build with the `verbose` flag (default `no`, `config/functions:379`) prints every compile command, so the log carries the definitions the recipe's echo at `:48-50` keeps out. No disclosure is shown; D-INFRA-006 tolerates a value in a local build log.",
      disp="recorded under D-INFRA-006 (a local build log), with a sentence beside `:48-50` naming the verbose route; judged outside D-WORKFLOW-215's hold test (not shipped code; an input only the builder sets)",
      proved="tree"),
 dict(id="PL-18", title="The autostart alias repairs neither a real directory nor a wrong link", sev="Low", cat="Install step",
      q="Q2", src="G-7 (gpt)", lines="`emulationstation/autostart/001-emulationstation:8-11`",
      owner="T37; upstream's (JELOS)",
      what="A real `/storage/.emulationstation` directory passes `! -L`, and `ln -sf` then makes the link inside it; an existing symlink, right or wrong, is skipped. ES itself reads `/storage/.config/emulationstation` under `ROCKNIX` (`Paths.cpp:79`), so only the legacy alias is affected.",
      disp="recorded as written (upstream's; the alias is legacy), or a contained `ln -sfn` with a directory test at the pause",
      proved="tree"),
 dict(id="PL-19", title="An empty serial-number read is treated as a changed device", sev="Low", cat="Guard that fails open",
      q="Q2", src="G-8 (gpt)", lines="`emulationstation/sources/serial_number_check:8-24`",
      owner="T37; upstream's (D-UI-079: outside the fork's lanes)",
      what="When the path is set and the read is empty, a stored serial differs from `\"\"`, so the empty value is stored and the warning raised (`:21-24`); the unquoted path at `:12` is L-12.",
      disp="recorded for upstream (a #585 line); a contained guard (an empty read skips the check) only if the coordinator opens the lane",
      proved="tree"),
 dict(id="PL-16", title="`tools/pixelelated-state-check --payload` cannot run on this host", sev="Low", cat="Tooling",
      q="Q4", src="stage B (G-05's host half)", lines="`tools/pixelelated-state-check:767-792`",
      owner="the coordinator (a tool note; the tool fails closed, as it should)",
      what="The `.img.gz` route needs `mcopy`, absent here: `rc=2`, `input-invalid`. The `--root` route over an extracted `SYSTEM` ran instead and passed.",
      disp="a tool note for the integration (§ What the integration inherits item 9); no slice fix",
      proved="tool-run"),
]

# stage D (2026-11-01): each item's tracking and the lane's proposed Phase 7 disposition for the pause
TRACK = {"PL-01": "#613", "PL-02": "#1072", "PL-03": "#1382", "PL-04": "#1383", "PL-05": "#1384",
         "PL-06": "D-WORKFLOW-216; the integration's configure log", "PL-10": "a Backlog the coordinator files",
         "PL-14": "the distribution merge; #791", "PL-15": "the coordinator's sweep"}
PROPOSED = {
 "PL-01": "Resolve in stage E (a contained recipe edit at `:101`, if #613 is routed here); else Defer to #613",
 "PL-02": "Defer to #1072 (T40 corrects the patch's GPU call first; then T37's `PKG_PATCH_DIRS+=` line or T40's rename)",
 "PL-03": "Resolve in stage E (#1382): `PKG_NEED_UNPACK=\"$(get_pkg_directory busybox)\"`",
 "PL-04": "Resolve in stage E (#1383): the `rm` moved after `:82`",
 "PL-05": "Resolve in stage E (#1384): upstream's five ARMSX2 lines restored after `:128`",
 "PL-06": "Resolve in stage E: `fribidi` declared in `:13` (the seat's choice; the probe stays optional), the configure-log proof inherited by the integration",
 "PL-07": "Resolve in stage E: a `makeinstall_target` line that fails when the French `.mo` is missing",
 "PL-08": "Resolve in stage E: `HFS_DEV_LOGIN` added to the loop at `:42-44` (names only)",
 "PL-09": "Record: kept with its reason, a #585 line",
 "PL-10": "Defer to a Backlog the coordinator files",
 "PL-11": "Record: as written, a #585 line",
 "PL-12": "Record: as written (a best-effort cache with a fallback)",
 "PL-13": "Record: the dated currency finding; the bump at the integration",
 "PL-14": "Defer to the distribution merge (`release-candidates.md` step 0) and #791",
 "PL-15": "Defer to the coordinator's doc sweep",
 "PL-16": "Record: the tool note (`02` § What the integration inherits item 9)",
 "PL-17": "Record under D-INFRA-006 (a mask on the verbose path is a Backlog candidate for the coordinator)",
 "PL-18": "Record: as written (upstream's legacy alias)",
 "PL-19": "Record: for upstream, a #585 line",
}
def build(drift):
    ITEMS.sort(key=lambda i: int(i["id"][3:]))
    ids = [i["id"] for i in ITEMS]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for i in ITEMS:
        assert i["sev"] in SEV and re.fullmatch(r"Q[1-7]", i["q"]) and i["proved"] in PROVED and i["id"] in PROPOSED, i["id"]
    out = ["# Punch list (Phases 5 and 6) — M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)", "",
           "Written by `tools/t37-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 the pin, Q2 the build options and install steps, Q3 the dependencies, Q4 the credentials, Q5 the themes and `lowerdeck`, Q6 the patches, Q7 currency and structure); `04` § Renovation face maps them to the plan's seven. Every disposition is proposed; the stage-D pause rules them. At Phase 7 (stage E) every item has its outcome below.", "",
           "reviewed-at: 9fa740a91ba9fcaa21a26cc72f0b50fac10f32df", "reviewed-at-es: none -- no ES change", ""]
    for i in ITEMS:
        out += [f"## {i['id']}: {i['title']}", "",
                f"- **Severity:** {i['sev']}; **category:** {i['cat']}; **question:** {i['q']}",
                f"- **Source finding:** {i['src']}",
                f"- **Lines at the tip:** {i['lines']}",
                f"- **Owner:** {i['owner']}",
                f"- **What is wrong:** {i['what']}",
                f"- **Proposed disposition:** {i['disp']}",
                f"- **Tracked:** {TRACK.get(i['id'], '#1381 (this audit)')}",
                f"- **Proposed at the pause:** {PROPOSED[i['id']]}",
                f"- **proved:** {i['proved']}", ""]
    gate_items = ITEMS[1:] if drift else ITEMS
    out += ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
    out += [f"| {i['id']} | Open | before stage D's audit issue |" for i in gate_items]
    out += ["", "## punch_index", "", "```yaml", "punch_index:"]
    for i in ITEMS:
        out += [f"- id: {i['id']}", f"  severity: \"{i['sev']}\"", f"  category: \"{i['cat']}\"", f"  question: {i['q']}",
                f"  source_finding: \"{i['src'].replace(chr(34), chr(39))}\"", "  outcome: \"open\""]
    out += ["```", ""]
    text = "\n".join(out)
    sec = re.findall(r"^## (PL-\d+):", text, re.M)
    gate = re.findall(r"^\| (PL-\d+) \| Open \|", text, re.M)
    idx = re.findall(r"^- id: (PL-\d+)$", text, re.M)
    if not (sec == gate == idx == ids):
        print(f"ASSERT FAIL: sections {len(sec)}, gate {len(gate)}, index {len(idx)}, items {len(ids)} disagree"); sys.exit(1)
    return text

d = pathlib.Path(sys.argv[1]); drift = "--drift" in sys.argv[2:]
t = build(drift)
(d / "05-punch-list.md").write_text(t)
print(f"wrote 05-punch-list.md: {len(ITEMS)} items, generated, asserted (sections = gate = index)")
