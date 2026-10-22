# Preliminary review of the renovation order (M6.P1, #641) — advisory seat

**Verdict: ready with named changes.** The survey's arithmetic holds (I summed the 43 slices' path and read counts back to `inventory.md`'s twelve area rows and all twelve reconcile), T1 and T2 satisfy both D-WORKFLOW-102 gates inside the first three, and the lens argument is coherent as written. But the review depths contradict the order's own sensitive-file lists, five slices' sizes are misstated by the "read" metric, the shipped-device set disagrees with `plan-for-the-plan.md` § 5, and three seams (ApiSystem, ES's vendored rcheevos, ES's state primitives) are cut without being named. All are document changes; one reachability row wants a single command run before T4.

**Corpus note.** I read only the four embedded sources (`docs/reviews/order.md`, `docs/reviews/inventory.md`, `docs/reviews/areas.json`, `docs/reviews/plan-for-the-plan.md`). Not embedded: `assessment.md`, `cross-reference.md`, `p1-tracking.md`, `slices.json`. So the pass-3 lens scores and every figure the order quotes from them (19 blindspot entries, 47 closed bugs, 36 and 16 interface files, 884 callers) are taken on the order's word. Anything marked *(inference)* below goes beyond the embedded text.

---

## 1. The gates and the first three

**Met.** T1 (`os-launch-control-state`, gate `0.1`, 11,560 read lines, one package group `projects/ROCKNIX/packages/rocknix/**`) and T2 (`es-launch-path`, gate "before #336 Step 1", 9,598 read lines) are slices 1 and 2; both inside plan § 5's 8,000–12,000 bound; T3 is a table. Both are also where the lenses point, as order.md § "How the order was argued" says.

- **[material] The 0.1 gate's path set is not stated, and the order's own `state` list puts a state file outside it.** `backuptool` (1,899 lines; inventory.md § Largest units, cloud-sync-and-saves) is in T6 (position 6, gate "none"), while `post-update`, `chksysconfig`, `factoryreset`, `installtointernal`, `automount`, `setsettings.sh` are in T1. If "state" in D-WORKFLOW-102 covers the settings backup/restore, either T6 also gates `0.1` (add it to T6's gate column) or `backuptool` moves to T1 (11,560 + 1,899 = 13,459, over the guide). Likewise "control": `sysutils/{autostart,powerstate,sleep,systemd}` (T11, Independent, position 11) are boot and power control, root on every device. The order should say in one sentence what the gate covers and why T1 = `rocknix/**` minus `backuptool` satisfies it. The D-WORKFLOW-102 text is not embedded, so I cannot settle it.
- **[material] T10 is gated in prose but not in the table.** T10 "why here": "read before that work begins, beside T2's gate"; gate column: "none". Either T10's gate becomes "before #336 Step 1" (and T10 moves next to T2, with the tables sliding to 4–5), or the claim is dropped. Plan § 8 already accepts the re-open cost if #336 lands first; a prose gate the slice issue won't carry is a trap for the planner.
- **[material, inference] T2's boundary may miss the ES-side launch entry.** In batocera-derived ES the launch sequence starts in `views/ViewController` (the launch transition, then `FileData::launchGame`); T23's own text says the fork changed ViewController. T2 has ~2,400 lines of headroom under the guide. One `grep` for `launchGame` in `es-app/src/views/` settles it; if it is the entry, `ViewController.*` belongs in T2 and on the `launch-path` sensitive globs. Same check for `ApiSystem` (if `launchGame` shells out through it) and `Window` (the launch-time surfaces, D-UI-093, cited by T26).
- **[material, inference] The launch path's command table is in none of T1, T2, T10.** `es_systems.cfg` — what `SystemData` (T2) parses and where `runemu.sh`'s command lines live — is produced in the distribution, most plausibly by `projects/ROCKNIX/packages/virtual/emulators` (T21, position 21, Independent; 29 paths, 4,532 fork-own code lines, the second-largest fork-own unit in generic-packages, inventory.md § Largest units) or installed from `projects/ROCKNIX/packages/ui/emulationstation` (T28, position 28, Local; 4,234 non-code lines). Whichever it is, #336 Step 1 rewrites it. It should be named as interacting by T1, T2 and T10 and added to the `launch-path` globs; if it is `virtual/emulators`, read it with T10.
- **[minor] T3 is "one session" by assertion.** A table's bound is rows, not lines (order.md block header). The order should state T3's unit count — the inventory gives the unreached set as 982 units across all areas, not generic-packages' share — and note that reachability is tool-generated, so the executor's work is the removal rows and their `Already written:` lines.

## 2. The argument from the lenses

Sound in shape: gates, dead ends, credentials and player data, planned change, the central and small, devices, interface, harness, tables. Specific placements:

- **[material] The dead-end tables are split against the order's own lens.** T3/T4 go early "because every removal shrinks a later slice"; but T36 (27 unreached paths and the two other distributions), T37 (84 unreached emulator recipes), T38 (216 unreached project/device paths + 122 unshipped) and T40 (348 unshipped patches, 286,952 lines) sit at 36–40. T4 already tables "the other projects' patches" at slice 4, so `projects/RPi` and friends lose their patches at 4 and their `options` at 38. Move T36–T38 to follow T4 (positions 5–7) and T40 with them; at minimum merge T37 into T3. The one reason to hold T38/T40 is the product decision in § 6 #1 below, which the maintainer's yes can settle.
- **[material] T29 (the guards) is too late by the security lens.** Lens tag "security, brittleness"; `.githooks/**` is on the order's security list; "28 blindspot entries name tooling". The guards run on every commit of every slice from T1 onward; a defective secret guard is a program-wide risk during the renovation itself. Move T29 into the security cluster (after T9).
- **[minor] T5–T9 interleaves the pairs it says it keeps together.** "Each pair is read close together because the defects live at the seam" — the sequence puts the proxy (T7) between the cloud scripts (T5, T6) and their pages (T8). Reorder T5, T6, T8, T7, T9. Alternative: merge T7 + T9 (3,656 + 4,929 = 8,585 read lines) into one Extended slice, which is exactly plan § 5's "the proxy and its consumers" — but that makes the first two-tree slice (two `reviewed-at` hashes; plan § 11 Q4 is still open).
- **[minor] T20 before T17–T19.** GENERIC_X64 is "the VM every proof runs on" (T20's own why-here) and T20 holds the kernel recipe (`projects/ROCKNIX/packages/linux`, 432 fork-own) and project boot files that serve all devices. Cost against value puts it first among devices.
- **[minor] T30 (cloud harness) at 30 while T5/T6's closing evidence is `tools/cloud-round-trip`** (blindspot 31, "a harness that agrees with itself"). Either move T30 after T8, or have T5/T6's briefs carry "read `cloud-round-trip`'s assertions for the behaviours you prove and flag any that assert current behaviour rather than the invariant".
- **[minor] T16's lens tag is wrong.** "planned change (#336)" — #336 replaces RetroArch (T10); T16 is the standalone start scripts, lens brittleness/launch path (`tools/emulator-exit-test`). Position 16 is fine; fix the tag.
- **[minor] T12's text misstates its size.** "884 callers of its largest units for 12,328 read lines" is the area's reached code (2,588 fork-own + 9,740 upstream-carried, inventory.md § Read size), i.e., T12 + T36; T12 reads 6,776.

## 3. Seams

- **[material] ApiSystem is the un-named seam.** `es:es-app/src/ApiSystem.cpp` (3,519 fork-own lines, inventory.md § Largest units) is the bridge every ES page uses to call the OS scripts: T8, T9 and T13 reach T1/T5/T6/T7 through it, yet it is read at T24 and named by none of T2, T8, T9, T13. It also assembles shell command lines from player-entered strings (Wi-Fi, accounts), a security seam with `wifictl`/`setrootpass` (T1, security list) and `GuiWifi.*` (T22, security list). Proposal: a new slice `es-apisystem-bridge` — `ApiSystem.*`, `GuiWifi.*`, and any other page that passes credentials through it (~4,000–5,000 lines, counts not in the embedded docs), Extended, placed right after T9; T24 shrinks to ~5,000 fork-own; T22 loses `GuiWifi`.
- **[material] ES's vendored rcheevos carries fork code a version row cannot see.** `es:external/libcheevos/rcheevos`: 68 paths, 33,547 code, **1,352 fork-own**; `libretro-common` 304 fork-own (inventory.md § Largest units). T41 tables `external/` "by provenance and version" at Local. A 1,352-line local delta in the library that speaks the RetroAchievements protocol the proxy (T7) emulates must be read as a diff against the vendored version, with T7/T9, and named in T7's interacting subsystems (T7 names only RetroArch's rcheevos path). Separately, `es:external/doctest/doctest.h` is 7,134 "fork-own" lines that are fork-*added*, not fork-written; T41's table needs a column distinguishing fork-added vendored from fork-modified vendored.
- **[material] The state seam is split across T1 and T26/T27 without being named.** The `state` list names `Settings.*`, `SystemConf.*` (T26) and `AtomicFileUtil.*` (T27, "the fork's last-good writes") — the ES end of the `es_settings.cfg`/`system.cfg` seam whose other end is T1's `setsettings.sh`/`get_setting` and T6's `backuptool`, proven by T32/T33. T1 names `system.cfg` but not its ES writers; T26/T27 are Independent at 26–27. Carve `Settings.*`, `SystemConf.*`, `AtomicFileUtil.*`, `HttpReq.*` into a small Extended slice after T6, named from T1 (line counts are not in the embedded docs; es-core is not listed per file).
- **[minor] Mis-pointed or missing entries.** T5 names "the game-end hook and autostart (`os-launch-control-state`)" — `sysutils/autostart` (5 paths) is in T11 by T11's globs. T13 should name `setsettings.sh`/`SystemConf` (GuiMenu writes what setsettings reads). T17–T19 should name T20's kernel recipe. T6 should name T1's `post-update`/`chksysconfig` *(inference about what `backuptool` archives)*. Standalone start scripts (T16) sit on `runemu.sh`'s launch path but are absent from the `launch-path` globs — add them or say why not.
- **[minor] `es:es-app/tests/**` (22 paths, 5,687 lines) all ride with T8.** If a test's subject is in T2 or T9, it should ride with its subject.

**Sufficiency.** The entries are usually right about *which* slice but seldom give the *paths* and the *shared state* (file, lock, setting key, socket) that plan § 7 item 2 wants as read-only context. The brief can add paths; the order should name the shared state per seam (e.g., T5↔T8: the sync state file/lock and the card payload).

## 4. Sizing and kinds

Kinds are mostly consistent with plan § 3 (I checked fork-own share per slice). Exceptions and sizing errors:

- **[material] Read counts exclude work the slice text says it does.** Patches and configs carry 0 code lines by construction (inventory.md: patches-and-configs code 0, vendor-carried 777,541), so: T7 omits its 18 patches (1,703 lines), T10 its 21 RetroArch patches, T17 its 8,129-line config diff, T20 its 7,754-line config diff, T39 the nine fork-written patch sets it "reads line by line". The briefs will inherit the wrong workload. Add a patch/config-lines column or fold them into Read.
- **[material] T14 is not 190 lines.** Its reading is `.claude/rules` 8,000 + `.claude/skills` 12,400 + CLAUDE.md/AGENTS.md + the registers (~2,000–3,000) ≈ 23,000 lines of binding prose, plus `docs/*` and `docs/{upstream,releases,pixelelated,rasteratops,…}` ≈ 37,000 (inventory.md § Largest units, doctrine). Split into T14a *the binding doctrine* (rules, skills, CLAUDE.md, AGENTS.md, registers; the #640 question) and T14b *the reference docs* (NAMING, TRADEMARK, `licenses/`, `docs/upstream`, `docs/releases`). T14a is Local and cheap and could run earlier.
- **[material] T39, T3, T40 need row counts and a tool.** T39: 575 provenance rows each with "whether it still applies", which needs the pinned source — more than one session unless a tool extracts the header fields (`From:`, `Subject:`, `git am` trailers, `PKG_VERSION`). Say which tool, or split by the patched package's area. T3 and T40 likewise state no row count.
- **[material] T43 is unbounded.** 126,124 paths, "read 15,392,661 (15,392,661)" — an artefact (qa-logs and `inventory.json` classified as shell/json code). Show "—" and state the selection rule for "a record that misleads a reader today" (e.g., records linked from doctrine, READMEs and indexes), else no session can close it.
- **[minor] T11 and T15 are "read" slices of mostly upstream-carried content** (3,002 of 10,898 and 389 of 9,327 fork-own); plan § 3 says currency first, and T15's own text says "the rest as a table". Make T15 currency (size 389) and Local; justify T11's full read by root-at-boot or make it currency too.
- **[minor] T21 (531 recipe paths)** is sized by fork-own lines (6,711) but currency work scales with recipes; likely two sessions, or shed `virtual/emulators` to the launch cluster (§ 1).
- **[minor] Small slices:** T37 (51 read lines) → T3; T34 (3,384) could pair with T31 or T29; T28 (327) could run in T21's session. T7/T9 are small by design.
- **[minor] T32 is justified, but mis-quotes the plan.** Plan § 5's bound is "about 8,000 to 12,000 lines of code … or one package group, or one device" — not "or one unit". A single file is a defensible unit; quote § 5 correctly or amend it. The T32 brief should invite the executor to propose the file's split as a Q7 finding — that is the remediation that justifies reading it whole.

## 5. Depth

- **[material] The order's own sensitive lists name files in slices below Extended.** State: `ThreadedCloudSync.*`, `CloudTransferJob.*` (T8, Independent); `Settings.*`, `SystemConf.*` (T26); `AtomicFileUtil.*` (T27). Security: `RetroAchievements.*` (T9); `get_env` (T12); `GuiWifi.*` (T22); `HttpReq.*` (T26); `.githooks/**` (T29). Plan § 6c: security, state-preservation and launch-path slices are Extended, and "the cloud sync" is named. Fixes: T8 → Extended (the cloud sync's ES half, two state-listed files, 11,116 fork-own lines); the ES state primitives → new Extended slice (§ 3); ApiSystem + GuiWifi → Extended (§ 3). For `get_env`, `.githooks`, `RetroAchievements.*`: either raise, or write the rule the order already applies tacitly in T12 and T29 ("a sensitive file inside an ordinary slice is named to the reviewer, and its drift re-opens at Extended") — and fix the sensitive-files paragraph, which says drift "re-opens at its depth": at T22's depth, `GuiWifi` would re-open Independent.
- **[material] Three slices carry the security lens at Independent:** T9, T11 (root services), T29 (the secret guard). Reconcile tag and depth.
- **[minor] T17–T19 at Independent for 327/118/617 read lines (0 fork-own)** while T15/T28/T35 are Local for more; by the order's "small configuration slices → Local" rule they are Local, and plan § 11 Q3 says the maintainer may want exactly that saving.
- **[minor] "the updater"** (plan § 6c, Extended) is located by no slice; say it is T1's (`post-update`, `installtointernal`) if so.

## 6. Coverage and reachability

**What reconciles.** Per-area path totals equal the slice sums for all twelve areas (e.g., interface 1,129; generic-packages 2,384; devices 510; patches 1,742 = T4 778 + T39 575 + T40 348 + 18 in T7 + 21 in T10 + 1 in T17 + 1 in T20; shipped patches 616 = 575 + 18 + 21 + 1 + 1). Per-area read totals also equal the slice sums (e.g., cloud 29,172 = 7,827 + 11,180 + 10,165; tooling 61,047; interface 339,456). The generator is internally consistent.

- **[material] The shipped-device set disagrees with the plan.** Plan § 5's devices row lists "H700, SM8550, GENERIC_X64 first; RK3566, RK3326, **SM8250, S922X, SM6115** after" as devices "we build". inventory.md § The unshipped set and the order (T38, T40) treat SM8250, S922X, SM6115 as unshipped (SM8250 37 patch paths / 19,034 lines, S922X 43 / 16,825, SM6115 46 patches + dts). The maintainer's yes must pick one; if they are built, that is three more device slices in T18's shape, ~130 patch rows moving T40 → T39, and a changed `shipped` column for every path only those devices reach.
- **[material] Provenance tier for patches is assigned by area, not by git.** patches-and-configs reports fork-own 0, yet the order (pass 6) counts 18 proxy patches, 8 RetroArch patches, nine other fork-written sets and two fork-written kernel configs. The inventory's tier is wrong for ~40 paths and the fork-own totals understate the fork's code. The tool already computes the git tier for other paths; apply it to patch rows.
- **[material — one command settles it] `projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64`** (1 patch, 27 lines) and `vitaquake2-lr/…/patches/x86_64` (4) are "unreached" (inventory.md § The unreached set), yet GENERIC_X64 is x86_64 and shipped. Either the recipe's `PKG_PATCH_DIRS` / `scripts/unpack` selects an arch directory and the inventory's unpack model omits it — then T4 would propose deleting a live patch and every `PKG_PATCH_DIRS`-selected directory is suspect — or the fork's ES patch for its own VM never applies, a defect to file now. Check before T4, and let the inventory's method note say whether `PKG_PATCH_DIRS` is evaluated.
- **[minor, to verify] Fork-added packages marked unreached:** `projects/ROCKNIX/packages/tools/grub` (+4 patches) while an x86_64 image ships — what does GENERIC_X64 boot from?; `projects/ROCKNIX/packages/network/connman` (7 paths); the rust snapshot overrides; `packages/linux` with 358 fork-own code lines (a fork-edited recipe shadowed by `projects/ROCKNIX/packages/linux`). Each is a plausible dead end and a plausible mislabel. T3/T4's briefs should re-derive reachability for a sample with the build engine's own tool (`tools/viewplan` / `scripts/genbuildplan.py`) — "two commands for one quantity", plan § 7 item 2.
- **[minor] Reachability is per package, not per path.** `hardware/quirks/devices/**` (333 paths, 88 models) is all "shipped" because the quirks package is in every plan; T15's dead models are invisible to the column. T15 and T38 should share the device list.
- **[minor] "Overlap" (55 paths, inventory.md § Per area) is undefined;** say which area won and why `ambiguous: 0` still holds.
- **[minor] Interface's "upstream-carried, reached code" (241,540) includes ~146,000 lines of `es:external/**`** that no slice reads (T41 tables them). A vendored-in-tree tier would make the area's read size honest; plan § 2 defines vendor-carried as patches and configs only.
- **[minor] Slice globs rely on the area filter:** T12 and T29 both say `.github/**`; T12 and T42 both `scripts/**`. Write them as `areas.json` does so stage A can re-derive scope from the glob alone.

## 7. Anything else

- **[material] This review ran on four of the order's seven inputs.** `assessment.md`, `cross-reference.md`, `p1-tracking.md`, `slices.json` were not embedded; the lens scores are unchecked. Record that in order.md's § "preliminary review".
- **[minor] Evidence-floor tension.** Plan § 7 item 5: "no build in a build worktree"; T12's closing evidence allows "a package build in the lane's own build worktree only when the brief names one". Reconcile.
- **[minor] Drift for tables.** Plan § 8's "under 20 % of the slice's lines" is meaningless for T3 (464 read lines) or T39 (0); state table drift in paths.
- **[minor] Two trees.** ES slices read at `16dbac5211`; `reviewed-at` must carry the ES hash and `renovation-drift` must diff both trees. Say so once.
- **[minor] T36 should mark the upstream tools the method itself runs** (`tools/pkgcheck`, `viewplan`, `genbuildplan.py`) as reached-by-the-renovation; T12/T28's closing evidence and plan § 4 Q2 depend on them.
- **[minor] `tools/renovation-inventory` (945 lines, T29)** is the generator the whole order rests on; read it — or at least its reachability function — before T3, not at 29.

---

## Changes I would make, in priority order

1. Reconcile depth with the sensitive lists: T8 → Extended; new Extended `es-state-primitives` (Settings, SystemConf, AtomicFileUtil, HttpReq) after T6; new Extended `es-apisystem-bridge` (ApiSystem, GuiWifi) after T9; write the "named to the reviewer / drift re-opens at Extended" rule for `get_env`, `.githooks`, `RetroAchievements.*`; fix "re-opens at its depth".
2. State the 0.1 gate's path set; give T6 the `0.1` gate or move `backuptool`; give T10 a gate row or drop "read before that work begins".
3. Settle SM8250 / S922X / SM6115 with the maintainer (plan § 5 vs. the inventory's shipped set) before any device or patch slice is filed.
4. Verify `emulationstation/patches/x86_64` reachability (and `PKG_PATCH_DIRS` handling) before T4; add the git tier to patch rows.
5. Verify the ES launch entry (`ViewController`) and the `es_systems.cfg` generator; add both to T2/T10 and the `launch-path` globs.
6. Read ES's rcheevos / libretro-common fork delta (1,352 + 304 lines) with T7/T9, not as a T41 version row; add the fork-added vs. fork-modified column to T41.
7. Fix sizes: patch/config lines into the read counts (T7, T10, T17, T20, T39); split T14; row counts and tool for T3, T39, T40; a selection rule and "—" for T43.
8. Reorder: T5, T6, T8, T7, T9; T36–T38 (and T40) up beside T3/T4, or at least T37 into T3; T29 into the security cluster; T20 ahead of T17–T19.
9. Fix the small text errors: T5's `autostart` pointer (T11), T12's "12,328", T16's lens tag, T32's quotation of plan § 5, the `.github/**`/`scripts/**` globs.
10. Downgrade T17–T19 to Local (the maintainer's call, plan § 11 Q3); make T15 currency + Local.
11. Record in order.md that this preliminary review saw four of seven inputs.

---

## Corpus provenance (for `corpus.provenance.json`)

```json
{
  "source_file_paths": [
    "docs/reviews/order.md",
    "docs/reviews/inventory.md",
    "docs/reviews/areas.json",
    "docs/reviews/plan-for-the-plan.md"
  ],
  "source_file_hashes": [
    "7f537288564682ebbf794592833b9cac60aa57cc65e8dc339e3335c0b4b8be91",
    "1b0eac803cb0d46a742d0f7072416311f8e97aa4eb060fb278d8e048c34882db",
    "985f742cfd4a2138339f1ed41bd5f5f9e3755fe69b309ff3ddb10d1466fced90",
    "f01f2b82cc628073640050bcb56cbc9a2e5c9e9a8a289978b171897ce9951f0f"
  ],
  "hash_source": "verified at embed time by the Council Facilitator (council-facilitator@1.14.0); not re-read or re-hashed by this seat",
  "manifest_read_timestamp_utc": "2026-10-22T20:09:11Z",
  "not_embedded": [
    "docs/reviews/assessment.md",
    "docs/reviews/cross-reference.md",
    "p1-tracking.md",
    "slices.json"
  ]
}
```