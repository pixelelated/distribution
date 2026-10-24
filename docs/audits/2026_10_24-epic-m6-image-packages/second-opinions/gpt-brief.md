# Second opinion on a code audit -- M6.P2 T8, the image's own packages, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the command output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 485 paths of a handheld Linux distribution's own package recipes (`projects/ROCKNIX/packages/`, 260 `package.mk` and 225 scripts, units and configs), read at one commit (`8ebaf8daad`) against three movers -- the merge of the upstream distribution (`upstream/next` at `e0f9deb899`, base `c445081a59`), the never-run `make update`, and the fork's own currency. No build ran; nothing was changed. The tables are generated and their counts asserted by script.

The first reader's draft grades: **Medium** -- F-02 (a recipe writes a symlink at load, #852), F-11 (the upstream merge's `glslang` modify/delete would downgrade it under a coupled pin); **Low** -- F-03 and F-04 (dead primary URLs the mirror covers), F-05 (`cairo` behind), F-06 (the freshness tool's blind spots), F-07 (short hash pins), F-08 (a lint's false positive), F-09 (nine conflicts at the merge), F-10 (a unit and udev rule wired to an absent script), F-12 (eleven orphans and their pin changes). F-01 is another lane's issue (#890), already fixed in a packet.

Answer in three parts, in this order:

1. **Your own findings first.** Read the fork-own files, the diffs, the excerpts and the outputs, and list every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. Look especially at: the fork's scripts and units (`sway-ready`, `111-sway-init`, `installer`, `avahi-daemon.service`), the overrides that reset a pin after sourcing a generic recipe, the conflict list's dispositions, and any recipe that writes outside its own build step.
2. **Refute the first reader.** For every finding: agree, disagree, re-grade or narrow, and in each case say what would make the finding false and whether the packet shows it. Say also whether the conflict list's eleven dispositions and the orphan table's "after the base merge" column hold on the packet's own evidence, and whether any Q4 row reads `current` on evidence the packet does not carry.
3. **What you could not judge.** The claims the packet does not let you verify, so the orchestrator knows where its evidence was thin.

Keep each item to a few lines. At most 7,000 words.

# The packet

## 02-forward-audit.md (whole, less the generated coverage rows)

# Forward Audit — M6.P2 T8, the image's own packages (projects/ROCKNIX)

**Scope:** the 485 paths of brief § 2 (260 recipes, 225 other files: 48 shell scripts by shebang, 30 units, 65 configs and the rest) at `8ebaf8daad`'s bytes; `reviewed-at` `caf1de3727`. **Depth:** Independent (D-WORKFLOW-184), one GPT-6 Astra seat at stage C. **Bench:** the tree, the record and the release sources (brief § 5); no guest at stage B. Every result file named below is under `.qa-scratch/t8/` (gitignored) and is rewritten by the command beside it; `tools/t8-tables.py` builds the tables from them and asserts 485 and 260.

## Phase 2: #655's checklist at stage B

| # | Criterion (abridged) | State at stage B | Evidence |
| ---: | --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00` to `04` written; `05` at stage D | this folder |
| 2 | the lint `PASS` | `--phase pre-issue` at stage C | `00` stage C |
| 3 | `review-plan.json`, one `gpt` seat, provenance beside both outputs, `04` § Second opinion | stage C | `second-opinions/` |
| 4 | every punch item at a Phase 7 outcome | stage F | the audit issue |
| 5 | `reviewed-at:` and `fixed-at:` | `reviewed-at` `caf1de3727`; `fixed-at` at stage H | `00` header |
| 6 | `01` § Scope | done: every count equal to the brief's | `01` § Scope; P1, P2 |
| 7 | the coverage table, 485 rows | done | § Coverage table |
| 8 | § Mechanical checks | done | § Mechanical checks |
| 9 | Q4's currency table, 260 rows; no `current` beside `not read`; every fork-own BEHIND an item | done (`q4-table.md`, `q4-pins.json`); 0 `current` beside `not read`; one fork-own BEHIND (`cairo`, F-05) | `04` § Q4 |
| 10 | the orphan table, the conflict list, Q6's 13 | done | `04` § Q4, § Q6; § The conflict set |
| 11 | § The fetch sweep | done | § The fetch sweep |
| 12 | § The #644 findings, 15 and 16 | done | § The #644 findings |
| 13 | proof cells equal to the proof lines; every guest cycle's census | 15 and 15; no guest cycle at stage B | § Proofs |
| 14 | `question:`, `box-check`, no `projects/` change before a brief, no `PKG_VERSION` change | true at stage B | `git diff --stat 8ebaf8daad HEAD -- projects packages` empty |
| 15 | no deletion or rename | true at stage B | `--diff-filter=DR` empty |
| 16 | #852 fixed under a stream brief | stage E; reproduced at stage B (P12) | § Proofs |
| 17 | the retro | stage G | -- |
| 18 | the six checkers | stage H | -- |

## Mechanical checks

| Check | Command (abridged) | Exit | Summary |
| --- | --- | ---: | --- |
| branch against the hash, over the 485 | `tr '\n' '\0' < paths.txt \| xargs -0 git diff --stat 8ebaf8daad HEAD --` | 0 | empty |
| (a), per path | `git cat-file -e upstream/next:$p`, `git diff --quiet`, the base read for the absent (`while IFS= read -r`) → `q4a.txt` (12:13:04) | 0 | **367 identical, 87 differs, 21 orphan, 10 fork-added**; over the 260 recipes: 175 identical, 67 differs, 11 orphan, 7 fork-added. The fork-own and the orphans are the positive controls |
| the conflict set | `comm -12` of `git diff --name-only c445081a59 8ebaf8daad` and `c445081a59 upstream/next` over the 485 → `conflicts.txt` | 0 | **11**, as the brief has it |
| the base merge, simulated | `git merge-tree --write-tree --name-only --messages 8ebaf8daad upstream/next` → `base-merge.txt` (12:23:57; tree `7a44e4f2df`) | 1 | 29 conflicts in the whole tree; **9 of the slice's 11 conflict** (7 content or add/add, 2 modify/delete), `gamescope` and `gamelist.xml` auto-merge (§ The conflict set) |
| every field per plan | `config/options <name>` for GENERIC_X64, H700, SM8550 → `effective.txt` (780 rows, 12:13:05 to 12:13:50) | 0 | an archive URL with an empty or unset checksum: **`libfmt` 9.1.0** on GENERIC_X64 and H700 (#877, read only), **`atf` 2.12.0** on H700 (T5's E6, unmerged here), **`simple-http-server` 0.8.0** on GENERIC_X64 (its `x86_64` and `arm` branches set none: **#890**); `sway`'s only unchecksummed branch is RK3588's 1.9, which no shipped plan builds |
| the sourcing overrides | `grep -E '^\. +\$\{ROOT\}/packages/.*/package\.mk'` over the 260 → `sourcing-true.txt` | 0 | **43** (the brief's 50 counted the 7 that only call `get_pkg_directory` in `PKG_NEED_UNPACK` or `PKG_PATCH_DIRS`); 6 reset a fetched field after the load: `libfreeaptx`, `opus`, `wavpack`, `zlib`, `libfmt`, `gcc`. Nothing is set before a load that the load then overwrites |
| `make update`'s set | the three virtual packages' `PKG_DEPENDS_TARGET` through `config/options` → `update-set-*.txt` | 0 | RK3588 171, GENERIC_X64 147, H700 162, SM8550 185; **13 in this slice**: `box64`, `box86`, `control-gen`, `gamecontrollerdb`, `jstest-sdl`, `moonlight`, `portmaster`, `rocknix-hotkey`, `sdl2text`, `sdljoytest`, `sdltouchtest`, `sixaxis`, `wine`; 9 hash-pinned; `control-gen` and `portmaster` blocklisted (`config/blocklist`, 29 lines) |
| (c), the freshness tool | `FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness <its 34 projects/ names>` → `q4c.txt` (12:15:17 to 12:15:29) | **2** | over the 34 (not all in this slice), counted from `q4c.txt`: CURRENT 4, BEHIND 3 (`vulkan-headers` and `swaybg`, both orphans; `raofflineproxy`, not this slice's), PINNED 7, INHERITED 5, LOCAL 5, UNKNOWN 9, AHEAD 1 (`file`). The tool lists only recipes added since the base, so the **19 recipes the fork edited are outside its set**; of those, the fork moved four pins, read by hand: `cairo` **BEHIND** (1.18.4, latest 1.18.6 on cairographics.org), `glslang` CURRENT, `spirv-tools` PINNED, `rocknix-splash` at its repository's HEAD |
| (c), the hash pins | `gh api repos/<o>/<r>/compare/<pin>...HEAD` for the 49 effective hash pins → `q4c-hash.txt` (12:16:02 to 12:17:10) | 0 | 44 read, 4 not GitHub (`libplacebo`, `x264`, `libxcb-cursor`, `waffle`), 1 with no common ancestor (`lsfg-vk`, pinned off its default branch `migration`); **6 are short hashes** (`SDL2_gfx`, `glfw`, `libsndfile`, `pyudev`, `six`, `soundfont-generaluser`, F-07) |
| the fetch sweep | HEAD without `-L` on the 228 distinct effective archive URLs → `probe/head.txt` (12:17:32 to 12:20:13) | 0 | **200: 82; 301: 25; 302: 118; 404: 2; no answer: 1** (§ The fetch sweep); 10 git URLs `git ls-remote`d, all answer |
| the redirected archives | each of the 143, streamed through `sha256sum` once → `probe/fetch.txt` (12:20:44 to 12:28:36) | 0 | **140 match**; 3 against no checksum: `atf`, `libfmt`, `simple-http-server` |
| `pkgcheck`, the tree's copy | `tools/pkgcheck <name>` per recipe → `pkgcheck-pkgcheck.txt` | 0 | **258 PASS, 2 FAIL**: `moonlight` (duplicate `post_makeinstall_target()`: the two are in an `if`/`else`, a parser false positive) and `wireplumber` (T6's heredoc-parser case, #657) |
| `pkgcheck`, T6's copy | `git show 44f64842b6:tools/pkgcheck`, run here → `pkgcheck-pkgcheck-t6.txt` (12:17:40 to 12:18:33 for both) | 0 | **257 PASS, 3 FAIL**: the same two and `image` (`:109,110`, `ref INSTALL`: #852) |
| `bash -n` by shebang | every path whose first line is a shell shebang → `bashn.txt` (12:19:09) | 0 | **48 ok, 0 FAIL**: the inventory's 45 `shell` rows and three more with a shebang (`portmaster`'s `control.txt` and `mapper.txt`, `zerotier-one`'s `095-zerotier.conf`) |
| the script shapes | `eval`, `echo \| xargs`, a redirection in a test, `rm` then `ln -s`, over the 48 | 0 | **0 hits**; each pattern fires once on a constructed line (`grep-fixture.sh`) |
| the units | `systemd-analyze verify --man=no` on a copy of each of the 30 (`systemd 259`) → `units-verify.txt` (12:19:33) | 0 | 7 rc 0; 23 rc 1, every message a binary or unit the build host lacks (or the host's own `xfs_scrub` units); **no directive warning** |
| each unit's `Exec*` path | against the GENERIC_X64 install tree, then H700's and SM8550's (`ls` only) → `units-exec.txt` | 0 | 29 present, 5 absent: `entware`'s `/opt/...` (on `/storage` by design), `batteryplus` ×2 (H700's, present there), `inputplumber` (SM8550's, present there), and **`/usr/lib/xorg/xorg-configure`, absent from all three images** while its unit and `97-xorg.rules` ship (F-10) |
| the record | the five roots' `build/` listings by name prefix and their `.stamps` by exact name → `listing-*.txt`, `stamps-*.txt` | 0 | by prefix (the brief's `^${n}-[A-Za-z0-9]`): 13 unbuilt, **`entware` in place of `arm`** (its directory is `entware-`, an empty version; `arm` matches `arm-mem-...`, another recipe); corrected, **the 12 virtual and `qcom-abl`** as the brief has them; by stamps, all 260 stamped; **every plan's reached recipes are stamped in that plan's root** (no #879 shape) |
| `qcom-abl` | `config/options qcom-abl` and `tools/viewplan` per plan | 0 | `PKG_URL` empty, version 1.0; SM8550's plan builds it (`viewplan`: 1 line), GENERIC_X64's and H700's do not; stamped in the SM8550 roots |
| the mirror, for the three failures | `${DISTRO_MIRROR}/${PKG_SOURCE_NAME}` streamed through `sha256sum` (12:20:56 to 12:22:07) | 0 | `libaio`, `rocknix-abl` and `samba` each **match their recipe's sha256**, as the cache's stamps do; `samba`'s origin answered 200 on a third read (12:28:05) |
| #852's shape | the build directories this worktree's `config/options` runs created | 0 | `build.pixelelated-{GENERIC_X64.x86_64,H700.aarch64,SM8550.aarch64}/image/system/opt -> /storage/.opt` (12:22:26 to 12:22:27), written by sourcing `virtual/image` (P12) |

## The fetch sweep

HEAD without `-L` on each distinct effective archive URL over the three plans (228): **200: 82; 301: 25; 302: 118; 404: 2; no answer: 1.** The 143 redirects were fetched once each and hashed; nothing was kept. **The controls:** `portaudio`'s dead URL (#849, outside the set) answers **404**; `pciutils`' live one answers **200** (`probe/controls.txt`).

| Recipe | HEAD | The bytes | Disposition |
| --- | --- | --- | --- |
| `libaio` | **404** (a ranged GET 404) | ROCKNIX's mirror `716c7059...` = the recipe = the cache's stamp | **F-03, `bug`**, dead primary URL, mirror-covered |
| `rocknix-abl` | **404** (a ranged GET 404) | mirror `64034fb0...` = recipe = stamp | **F-04, `bug`**, the same class; an orphan (upstream replaced it with `openabl`) |
| `samba` | no answer twice, **200** on a third read | mirror `09bb56db...` = recipe = stamp | transient: no finding |
| `simple-http-server` (x86_64) | 302 | `a16d73db...` = the cache file = its stamp; **no mirror copy (404)**; no `PKG_SHA256` | **F-01, #890** (the coordinator's, fixed in a packet ahead of T5) |
| `libfmt` (9.1.0) | 302 | `5dea48d1...`, no checksum | #877 (read only) |
| `atf` (2.12.0, H700) | 302 | `30abf4da...`, no checksum | T5's E6 gave it one on `52e6794ba7`; not re-filed |
| the other 140 redirects | 301 or 302 | **match** | policy redirects; no row |
| 10 git URLs | `git ls-remote` | each answers; each pin is fetched by clone | no row |

**What a fetch from an empty cache does today** (`scripts/get_archive` at `8ebaf8daad`): every archive arrives with its recipe's checksum, or with none where none is set. At T5's tip it refuses `libfmt` (#877), `simple-http-server` (#890) and `atf` until its E6 lands with it.

## The conflict set

The fork's changes since the base that upstream also changed (11), read hunk by hunk, with `git merge-tree`'s verdict at the base merge:

| # | Path | `merge-tree` | Disposition |
| ---: | --- | --- | --- |
| 1 | `apps/gamescope/package.mk` | auto-merges | different, keep ours: upstream bumps the pin to `6867f509...` (3.16.31), ours adds the glm/stb packages; the wraps at both commits name the same revisions, so the auto-merge builds (`:55` would stop it otherwise) |
| 2 | `graphics/cairo/package.mk` | content | conflict: upstream's is a sourcing override too; take its shape, keep ours' xcb/xlib-xcb options; the version line becomes the generic's |
| 3 | `graphics/glslang/package.mk` | modify/delete | conflict: upstream deleted it (the generic is 16.5.0); ours is 16.6.0 and `spirv-tools` follows 16.6.0's `known_good.json` -- taking the deletion downgrades glslang under spirv-tools (F-11) |
| 4 | `graphics/spirv-tools/package.mk` | content | conflict: upstream made it a sourcing override; ours pins `ef96ed76...` to glslang 16.6.0 with a GCC 12 diagnostic; resolve with glslang (F-11) |
| 5 | `lang/gcc/package.mk` | content | conflict: ours enables libatomic for x86_64; upstream restructured it for aarch64 only and dropped the 15.2.0 hold (the generic is 16.2.0); keep the x86_64 case and decide the hold |
| 6 | `misc/modules/sources/gamelist.xml` | auto-merges | different, keep ours: ours rewrites descriptions (identity); upstream removes the AetherSX2 entry |
| 7 | `multimedia/gstreamer/gst-plugins-base/package.mk` | content | conflict: both enable GL; ours keeps the install WebKit needs (#228); take upstream's GLES/EGL options and keep ours' install |
| 8 | `multimedia/gstreamer/gstreamer/package.mk` | add/add | conflict: added on both sides; ours enables the plugin registry WebKit needs, upstream's removes `/usr/share`; keep ours, check upstream's removal against the registry |
| 9 | `network/networkmanager/config/NetworkManager.conf` | content | same change: both add `hostname-mode=none`; drop ours' comment-only hunk |
| 10 | `tools/rocknix-abl/package.mk` | modify/delete | conflict: upstream replaced it with `openabl`; ours carries the v1.2 checksum fix; take the deletion and check SM8550's bootloader against `openabl` |
| 11 | `wayland/compositor/sway/autostart/111-sway-init` | content | different, keep ours: ours adds the virtio `Virtual` connector and the software cursor (GENERIC_X64); upstream adds essway masking, AFBC and the Duo Lite case; both |

**The hazard at the merge (F-11):** `glslang`'s modify/delete. Taking upstream's deletion leaves the generic `packages/graphics/vulkan/glslang` at **16.5.0** under a `spirv-tools` pinned to **16.6.0's** `known_good.json`.

## The #644 findings

- **15** (*`make update` ... the fork has no check on the upstream-carried pins*). **Disposition here: `make update` would move 11 of this slice's recipes, and it has never run.**
  - `scripts/update_packages:16` sets `PKG_PATH="./projects/ROCKNIX/packages"` and walks the dependencies of `virtual/emulators`, `es-themes` and `gamesupport` (`:7-9`). For RK3588, the Makefile's device, that is 171 names; for the three shipped plans 147, 162 and 185.
  - **13 of the 171 are this slice's** (9 hash-pinned, 2 blocklisted). Each row's `make update` cell says so, and the 11 unblocked rows read *moves to its branch head if run; otherwise follows the base merge*.
  - The base merge is the mover in fact. `box64` is 429 commits behind its default branch: what one run would do to it.
- **16** (*the freshness tool's set is a diff, not a provenance*). **Disposition here: the 11 orphans are separated from the 7 fork-added by the base.**
  - The tool lists 34 under `projects/`: in this slice, 7 fork-added and 11 orphans; the rest are other areas' (the cloud and proxy packages, `aethersx2-sa`, `rclone`).
  - The orphan table (`04` § Q4) gives each one's deletion commit and what the base merge leaves.
  - The tool also misreads two shapes: a `PKG_VERSION` that is a command substitution reads LOCAL (`cargo`, `cargo-snapshot`, `rust-std-snapshot`, `rustc-snapshot`), and it cannot see the 19 recipes the fork edited (F-06).
- **The others**, by their carriers in `docs/reviews/build-path-read.md`: 1 to 14 and 17 to 26 are T5's, T6's, T7's, T10's, the doctrine slice's or the maintainer's; 17 (#645) is T7's. None is taken here.

## Proofs

| # | Claim | Evidence | Class |
| --- | --- | --- | --- |
| P1 | the slice is the brief's 485 paths and 260 recipes; 14 paths with spaces | `01` § Scope; the branch diff empty | proved: tree |
| P2 | 35 fork changes; 11 orphans and 7 fork-added absent upstream; 66 recipes changed upstream | `prov-base.txt`, `prov-up.txt`, `prov-absent.txt` | proved: history |
| P3 | (a): 367 / 87 / 21 / 10 over the 485 | `q4a.txt` | proved: tree |
| P4 | 9 of the 11 conflict at a simulated base merge; `gamescope`'s wraps agree at both commits | `base-merge.txt`; the API's `contents` of both `.wrap` files | proved: history |
| P5 | the per-plan expansion: three archive versions without a checksum on the shipped plans (`libfmt`, `atf`, `simple-http-server`) | `effective.txt` | proved: tree |
| P6 | `make update`'s set holds 13 of this slice's recipes | `update-set-*.txt`; `config/blocklist` | proved: tree |
| P7 | (c): the tool's 34, `cairo` BEHIND, the 44 GitHub hash pins' distances, 6 short pins | `q4c.txt`, `q4c-hash.txt`, `hashpins.txt` | proved: tree |
| P8 | the HEAD histogram; the controls answer 404 and 200 | `probe/head.txt`, `probe/controls.txt` | proved: tree |
| P9 | 140 of 143 redirected archives match; the mirror covers `libaio`, `rocknix-abl` and `samba` | `probe/fetch.txt`; the mirror reads | proved: tree |
| P10 | `pkgcheck` 258 / 257 PASS; each FAIL read at its site | `pkgcheck-*.txt`; `moonlight`'s `if`/`else` | proved: tree |
| P11 | `bash -n` 48 ok; the four script shapes absent, each grep proved on a fixture | `bashn.txt`, `grep-fixture.sh` | proved: fixture |
| P12 | sourcing `virtual/image` writes `image/system/opt` into each plan's build directory (#852) | the three symlinks of 12:22:26 to 12:22:27 in this worktree | proved: tree |
| P13 | the units verify with no directive warning; `xorg-configure`'s script is in no image | `units-verify.txt`, `units-exec.txt`; the three install trees | proved: tree |
| P14 | every plan's reached recipes are stamped; the unbuilt are the 12 virtual and `qcom-abl` | `stamps-*.txt`, `record-stamps.txt`; `viewplan` | proved: tree |
| P15 | the 11 orphans' pins after the base merge; `glslang` would go from 16.6.0 to 16.5.0 | `upstream/next`'s generic copies read with `git show` | proved: history |

## Findings (stage B; graded at stage C)

| F | Q | Finding | Where (at `8ebaf8daad`) |
| --- | --- | --- | --- |
| F-01 | Q3 | `simple-http-server`'s `x86_64` and `arm` branches carry no `PKG_SHA256`; T5's fetch refuses it. **#890**, the coordinator's, fixed in a packet ahead of T5 | `network/simple-http-server/package.mk:12-23` |
| F-02 | Q3 | `virtual/image` writes `${INSTALL}/opt` at load (#852) | `virtual/image/package.mk:109-110` |
| F-03 | Q3 | `libaio`'s `PKG_URL` is gone (pagure's archive 404); the mirror covers it | `devel/libaio/package.mk` `PKG_URL` |
| F-04 | Q3 | `rocknix-abl`'s `PKG_URL` is gone (`ROCKNIX/abl` v1.2's asset 404); the mirror covers it | `tools/rocknix-abl/package.mk` `PKG_URL` |
| F-05 | Q4 | `cairo` 1.18.4, the fork's own pin, is behind 1.18.6 | `graphics/cairo/package.mk` `PKG_VERSION` |
| F-06 | Q4 | `tools/fork-package-freshness` cannot see the 19 recipes the fork edited, and reads a command-substituted `PKG_VERSION` as LOCAL | `tools/fork-package-freshness` `packages()`, `var()` |
| F-07 | Q2 | six recipes pin a git source with a short hash | `SDL2_gfx`, `glfw`, `libsndfile`, `pyudev`, `six`, `soundfont-generaluser` |
| F-08 | Q2 | `pkgcheck`'s duplicate-function check fails functions defined in the two arms of an `if` (`moonlight`) | `tools/pkgcheck`'s duplicate check |
| F-09 | Q7 | the base merge conflicts on 9 of this slice's paths (the conflict list; `gcc`'s 15.2.0 hold carries no reason in its recipe) | § The conflict set |
| F-10 | Q6 | `xorg-configure@.service` and `97-xorg.rules` ship in every image; the script the unit runs is in none | `x11/xserver/xwayland/system.d/xorg-configure@.service:8`, `udev.d/97-xorg.rules:13-17` |
| F-11 | Q4 | the base merge's `glslang` modify/delete would downgrade it to 16.5.0 under a `spirv-tools` pinned to 16.6.0 | `graphics/glslang/package.mk`, `graphics/spirv-tools/package.mk` |
| F-12 | Q1 | 11 orphans, each dropped by the base merge with a pin change for five (`opus` 1.5.2 → 1.6.1, `libfmt` 9.1.0 → 12.2.0 on GENERIC_X64 and H700, `vulkan-headers` 1.4.347 → 1.4.359, `mtdev` and `swaybg` a patch) and `rocknix-abl` replaced by `openabl` | `04` § Q4's orphan table |

## Coverage table

One row per path (485). (a) is `upstream/next`; Q4 is the disposition with the mover; Q6 counts the plans that reach it and the stamp.

(the 485 generated coverage rows are omitted from this packet)

## 03-retrospective.md (whole)

# Retrospective — M6.P2 T8, the image's own packages (projects/ROCKNIX)

Phase 3 of the code-auditor skill over the 485 paths at `8ebaf8daad`'s bytes. The renovation face (Q1 to Q7) is `04`'s; this file holds the skill's own faces.

## 3.1 Architectural coherence

- **Three movers, and only one ever runs.**
  - **The base merge** moves 450 upstream-carried paths; 66 recipes have changed upstream since the base.
  - **`make update`** would move 11 of this slice's recipes and has never run (#644 finding 15).
  - **The fork** keeps its 27 recipes current (D-WORKFLOW-024). `tools/fork-package-freshness` reads only the 7 it added; the 19 it edited are outside the tool's set (F-06).
- **An override is a layer, and the layer can outlive its reason.** 43 recipes source a generic one. Six reset what the build fetches: `opus`, `gcc`, `libfmt`, `wavpack`, `zlib`, `libfreeaptx`. Three of those six are orphans, layers whose upstream has since removed them, so the base merge will put the generic pin back (F-12): `opus` to 1.6.1, `libfmt` to 12.2.0 everywhere. `gcc`'s 15.2.0 hold says nothing about why in its recipe (F-09), against `engineering-practices.md` § A constraint lives beside the thing it constrains.
- **The fetch's second line is ROCKNIX's mirror,** as T7 found: `libaio` and `rocknix-abl` build only because `sources-v2` holds them (F-03, F-04). `simple-http-server`'s x86_64 binary has no mirror copy, only the shared cache (#890).

## 3.2 Project conformance

- **`packaging-and-patches.md`:**
  - **The full-hash rule:** six git pins are short hashes (F-07).
  - **The checksum rule:** `simple-http-server`'s two branches broke it (#890), and `libfmt`'s override did (#877).
- **`device-builds.md` § After rebasing item 3 (every field per plan):** applied to the 260, it found the checksum gaps per plan, `qcom-abl`'s SM8550-only plan, and no `PKG_ARCH` exclusion (P14).
- **D-WORKFLOW-193/194/196:** the archive versions without a checksum on the three shipped plans are `atf` 2.12.0 (T5's), `libfmt` 9.1.0 (#877) and `simple-http-server` 0.8.0 x86_64 and arm (#890; D-WORKFLOW-197, the coordinator's).
- **`tools/pkgcheck`** passes 258 of 260 with the tree's copy. Both FAILs are its parser's (F-08, and #657's `wireplumber`); T6's widened copy adds #852.

## 3.3 Spec fidelity

Against the brief (version 2):
- **Reproduced exactly:** 485 / 20,644 / 450-35 / 478-6-1 / 260 / 60 / 14; 35 / 87 / 11 + 7 / 66 / 40 / 34; the conflict set of 11; `make update`'s 171 / 147 / 162 / 185 and the 13; `config/blocklist` 29; 13 unbuilt names.
- **The deltas:**
  - **The record block's regex** `^${n}-[A-Za-z0-9]` prints `entware` in place of `arm`. `entware`'s directory is `entware-`, and `arm`'s only match is `arm-mem-...`. The list the brief prints is right; its command alone is not.
  - **"50 recipes source a generic recipe"** is 43 that do and 7 that call `get_pkg_directory`.
  - **"8 of them set their own pin after sourcing"** is 6 that reset a fetched field (`PKG_VERSION`, `PKG_SHA256` or `PKG_URL`).
  - **The empty-checksum expectation** (`atf` and `sway` and nothing else): `sway`'s gap is RK3588's branch only, and the third is `simple-http-server` (#890).
  - **The T7 erratum** (`01`): three of T7's six "orphans" are fork-added. The coordinator answered with a note on #654.

## 3.4 Platform conformance

Can this be done on the VM? **Yes, for a stream's behaviour claim** (#852's fix, on the image or the guest). **No guest for the reading:** the unit and the fetch claims were read from the three M7 install trees and the release sources. `xorg-configure`'s rule never fires on the guest: the VM attaches `virtio-gpu-pci` or `virtio-gpu-gl-pci`, PCI class `0x038000`, and the rule matches `0x030000` (F-10).

## 3.5 Cross-system interaction audit

### Interaction: the base merge x the fork's 19 edits

`git merge-tree` against `upstream/next` conflicts on 9 of the 11 paths both sides changed (`02` § The conflict set). Two merge cleanly:
- **`gamescope`**, whose wraps name the same glm and stb revisions at both commits, so the auto-merge builds;
- **`gamelist.xml`**.

The one with a consequence a reader could miss is **`glslang`'s modify/delete** (F-11). Upstream deleted ROCKNIX's override in favour of the generic recipe at 16.5.0, while the fork had bumped it to 16.6.0 and pinned `spirv-tools` to 16.6.0's `known_good.json`. The obvious resolution of a modify/delete (take the deletion) downgrades `glslang` beneath its coupled tools. `NetworkManager.conf` is the same change on both sides.

### Interaction: `make update` x the hash pins

11 of this slice's recipes are in `make update`'s set unblocked. A run would move each to its branch head (`box64` 429 commits) and drop its checksum (`scripts/update_packages` at the hash deletes the recipe's `PKG_SHA256` line where it cannot fill one, as T7's incident did to `hatarisa`; T5's F-19 and E6 change that on T5's branch), and T5's fetch would then refuse each. It has never run (#644 finding 15).

### Interaction: the orphans x their dependants

Every orphan's dependants name it by `PKG_NAME`, and after the base merge the name resolves to upstream's generic copy. So no dependant breaks by name. What changes is what the build fetches: five pins move (F-12), and `rocknix-abl` becomes `openabl` for SM8550's bootloader.

### Interaction: #852 x `scripts/install`

`virtual/image:109-110` runs `mkdir -p ${INSTALL}; ln -sf /storage/.opt ${INSTALL}/opt` at load. So every sourcing (`config/options image`, `viewplan`, `pkgjson`) writes `build.*/image/system/opt` before a build. This worktree's own expansion did, three times (P12). The image's `/opt -> /storage/.opt` is the intent (`3335fc7b76`); the stream moves the two lines into a function that runs at install.

### Interaction: the overrides x T7's generic recipes

T7's table carries the generic rows (its `04` § Q4 names the seven overrides). This slice carries the effective pin per plan for the 43 sourcing overrides, so the two tables meet at the override. `libfmt`'s row is #877 in both.

## 04-analysis.md (whole, less the Q4 rows, which follow)

# Analysis — M6.P2 T8, the image's own packages (projects/ROCKNIX)

## Executive summary

The 260 recipes the images build from `projects/ROCKNIX`, and the 225 scripts, units and configs beside them, were read at `8ebaf8daad` against their three movers. **No pin moved; nothing under `projects/` changed.**

**The movers:**

| Mover | Rows |
| --- | --- |
| the base merge | 224 rows, plus the 5 conflict rows and the 11 orphans it drops |
| `make update` | 11 rows (it has never run) |
| the fork | 4 pinned on purpose, 3 that follow a generic pin, 1 current, and **one BEHIND: `cairo` 1.18.4 against 1.18.6 (F-05)** |

**Findings:**
- **#890 (F-01):** `simple-http-server`'s x86_64 binary has no checksum, so T5's fetch would stop every GENERIC_X64 build. The coordinator filed it and fixed it in a packet ahead of T5.
- **#852 (F-02):** `virtual/image` writes its `/opt` symlink at load. This worktree's own expansion reproduced it (P12); it is this slice's stream.
- **F-03, F-04:** two dead primary URLs (`libaio`, `rocknix-abl`), covered by ROCKNIX's mirror.
- **F-09:** the base merge conflicts on 9 of this slice's paths.
- **F-11:** one of those conflicts, `glslang`'s modify/delete, would downgrade it under `spirv-tools` if resolved the obvious way.
- **F-12:** the base merge drops 11 orphans and moves five pins.
- **Six Low items:**
  - a freshness tool that cannot see the fork's edited recipes (F-06);
  - six short hash pins (F-07);
  - a `pkgcheck` parser false positive (F-08);
  - a unit and udev rule wired to a script no image installs (F-10).

## Acceptance-criteria scorecard

| Bucket | Criteria | Met at stage C | Open (later stage) |
| --- | ---: | ---: | ---: |
| the folder, the lint, the review plan with the seat | 3 | 1 | 2 |
| the punch list at Phase 7, the hashes and the status | 2 | 0 | 2 |
| `01` § Scope | 1 | 1 | 0 |
| `02`'s coverage, checks, sweep, #644, proofs | 5 | 5 | 0 |
| `04`'s Q4 table, orphans, conflicts, Q6 | 2 | 2 | 0 |
| no `projects/` change before a brief, no deletion, `question:` | 2 | 2 | 0 |
| #852's fix | 1 | 0 | 1 |
| the retro, the checkers | 2 | 0 | 2 |
| **Total** | 18 | 11 | 7 |

## Code Quality Assessment

### Strengths

- Every fork change carries its reason in the recipe or its commit:
  - `gamescope`'s and `mangohud`'s pinned subprojects, with a guard that stops the build when wrap and package disagree (`gamescope:55`);
  - `gstreamer`'s plugin registry;
  - `cairo`'s xcb options;
  - `NetworkManager.conf`'s hostname rule.
- 48 shell files pass `bash -n`, and none has the four shapes T30 found.
- 30 units carry no directive `systemd 259` warns about.
- 140 of 143 redirected archives were fetched again today and matched their checksum.

### Concerns

- **A deletion upstream is a pin change here** (the orphans), and nothing reads it before the merge but this table.
- **`gcc`'s hold has no reason in its recipe.**
- **The freshness tool's set leaves out the 19 recipes the fork edited**, four of which carry the fork's own pin.

### Complexity Hotspots

- `tools/installer/scripts/installer` (561 lines, fork-own by its identity edits);
- `wayland/compositor/sway`'s recipe and its three fork scripts (`111-sway-init`, `sway-ready`);
- the GStreamer trio WebKit needs.

## Risk Assessment

| Risk | Likelihood | Impact | Where |
| --- | --- | --- | --- |
| GENERIC_X64 builds stop at `simple-http-server` once T5's fetch merges | none once #890's packet merges first, as ordered | every GENERIC_X64 build | F-01, #890 |
| the base merge takes `glslang`'s deletion and downgrades it under `spirv-tools` | medium: the obvious resolution of a modify/delete | the Vulkan shader tools' build, and anything they compile | F-11 |
| the base merge changes five pins with no review (`opus`, `libfmt`, `vulkan-headers`, `mtdev`, `swaybg`) and swaps SM8550's bootloader payload to `openabl` | certain at the merge | per consumer; SM8550's boot | F-12 |
| ROCKNIX drops `libaio` or `rocknix-abl` from `sources-v2` | low | those two fail from an empty cache; the shared cache still holds both | F-03, F-04 |
| a `make update` run moves 11 hash pins with no checksum | low (never run) | 11 recipes refused by T5's fetch | #644 finding 15 |

## Coverage Boundary

**Read:**
- all 485 paths (`02`'s coverage table) at `8ebaf8daad`;
- `upstream/next`, and the base for each absent path;
- a simulated base merge;
- every recipe's effective fields on three plans;
- `make update`'s set on four plans;
- the freshness tool's 34 and the fork's four moved pins by hand;
- the 49 hash pins (44 by `compare`);
- a HEAD on 228 URLs, with every redirect hashed;
- the mirror for the failures;
- the cache's stamps for the failures;
- `ls-remote` on 10 git URLs;
- the five roots' `build/` and `.stamps/`, and the three install trees (`ls`);
- both `pkgcheck`s, `bash -n`, `systemd-analyze verify`.

**Not read:**
- the project release of the upstream-carried recipes. Their (c) says so, and their disposition names the base merge;
- the four non-GitHub hash pins' projects;
- the 82 URLs that answered 200, whose bytes were not fetched;
- the 60 recipes' patches (T42's and T43's rows);
- `shellcheck` (not on the host).

**Not run:** a build, a guest, `make update`, `update-pkg`, `update-scan`.

## Finding Verification (Phase 4.5)

Each finding attacked; what would make it wrong, and what was checked.

- **F-01** (#890). *Wrong if* GENERIC_X64 does not build it: `virtual/network:26` adds it to every image, and the M7 GENERIC_X64 root holds `build/simple-http-server-0.8.0` with its stamp. *Wrong if* T5's tip fixed it: `git show 52e6794ba7:` counts one `PKG_SHA256` line. **Confirmed**; the coordinator's.
- **F-02** (#852). *Wrong if* the lines run only at install: they are at global scope (`:109-110`, outside any function), and this worktree's sourcing created the symlink in three build directories (P12). **Confirmed.** Medium: a write outside the build's own step, on every sourcing.
- **F-03, F-04.**
  - *Wrong if* transient: each answers 404 on HEAD and on a ranged GET.
  - *Wrong if* a build fails: it does not, because the mirror serves the right bytes.
  - **Confirmed as dead primary URLs, mirror-covered.** Low. `samba`'s no-answer was transient (200 on a third read) and is withdrawn before it became a finding.
- **F-05** (`cairo`). *Wrong if* 1.18.6 is not a stable release: cairo's even-minor series is stable, and the listing at cairographics.org carries 1.18.6. **Confirmed.** Low.
- **F-06.**
  - *Wrong if* the tool lists edited recipes: `packages()` is `git diff --diff-filter=A` plus `EXTRA_PACKAGES`.
  - *Wrong if* `$(get_pkg_version rust)` is LOCAL: `var()` reads the literal, and the verdict tests `-z "$url"` after its own empty `eval`.
  - **Confirmed** as a tool lead for #657. Low.
- **F-07.** *Wrong if* the rule allows short hashes: `packaging-and-patches.md` says *the full commit hash*. All six are upstream-carried (#585). **Confirmed.** Low.
- **F-08.** *Wrong if* `moonlight` defines the function twice at run time: the two are in an `if`/`else` (`:12-45`), so one is ever defined. **Confirmed as a parser false positive** (#657's class). Low.
- **F-09.** *Wrong if* the conflicts resolve themselves: `git merge-tree` reports each. Low as a finding; the conflicts are the integration's to resolve, and the list is its pre-read.
- **F-10.**
  - *Wrong if* an image carries the script: none of the three install trees has `/usr/lib/xorg/xorg-configure`.
  - *Wrong if* nothing pulls the unit in: `97-xorg.rules:13-17` wants it for `i915`, `amdgpu`, `radeon`, `vmwgfx` and `virtio-pci`, on a PCI display of class `0x030000`.
  - The guest's `virtio-gpu-pci` is `0x038000`, so it never fires on a shipped image.
  - **Confirmed as latent.** Low, a #585 candidate.
- **F-11.** *Wrong if* the generic `glslang` is 16.6.0: `git show upstream/next:packages/graphics/vulkan/glslang/package.mk` reads 16.5.0, as does our generic copy at the hash. **Confirmed.** Medium: a silent downgrade at a merge, beneath a coupled pin.
- **F-12.** *Wrong if* a dependant names the override's path: dependants name `PKG_NAME` only. **Confirmed as a pin-change list.** Low.

**Rule 4**, asked of every PASS, each with the FAIL it was seen to give:
- (a) said *orphan* and *fork-added* on the base's split;
- the probe gave 404 and 200 on the controls;
- `pkgcheck` failed `moonlight`, `wireplumber` and `image`;
- each script grep fired on its fixture;
- `merge-tree` reported 9 conflicts;
- `systemd-analyze` reported the host's missing binaries;
- the stamps reported none missing, which the plan-by-plan check could have broken (it found #879's shape on T7's set).

## Renovation face

### Q1 Modernize

- **The 11 orphans (F-12):** upstream moved each to the generic LibreELEC recipe, or for `rocknix-abl` to `openabl` (`71d8932b33`).
- **The fork's own recipes** have no retired series or host: the GNOME, GNU and GitHub hosts all answered.
- **http:** `ffmpeg`'s `PKG_URL` is http (`http://ffmpeg.org/releases/...`), along with the rest of the http rows in `02`'s coverage table's Q1. They are upstream's (#585 with T7's twenty), and integrity rests on the checksum.
- **The units:** no retired directive in the 30.

### Q2 Standards and best practices

- **`tools/pkgcheck`:**
  - the tree's copy: 258 PASS, 2 FAIL, both its parser's (F-08, #657);
  - T6's widened copy: 257 PASS, 3 FAIL, the third #852.
- **`bash -n`:** 48 of 48.
- **`systemd-analyze verify`:** no directive warning.
- **The full-hash rule:** six short pins (F-07).
- **Late binding in the 43 sourcing overrides:** nothing is set before a load that the load then overwrites.

### Q3 Bugs

| F | What | Builds from an empty cache today | Issue |
| --- | --- | --- | --- |
| F-01 | `simple-http-server` 0.8.0 x86_64 and arm: no `PKG_SHA256` | yes, unverified; no, after T5's fetch, until #890's packet | **#890** (the coordinator's) |
| F-02 | `virtual/image` writes `${INSTALL}/opt` at load | n/a: a write, not a fetch | **#852** (this slice's stream) |
| F-03 | `libaio`'s primary URL 404 | yes, from the mirror (`716c7059...`) | filed at stage D |
| F-04 | `rocknix-abl`'s primary URL 404 | yes, from the mirror (`64034fb0...`) | filed at stage D |

The script shapes (`eval`, `echo | xargs`, a redirection in a test, `rm` then `ln`): none in the 48 (P11). Each unit's `Exec*` path is present in its plan's image except `xorg-configure`'s (F-10, Q6) and `entware`'s `/opt` path (on `/storage` by design).

### Q4 Package currency

**The table, 260 rows** (also `q4-table.md` and `q4-pins.json`):

| Disposition | Rows |
| --- | ---: |
| follows the base merge | 224 |
| `make update`'s (never run) | 11 |
| orphan, dropped by the base merge (2 of them modify/delete conflicts) | 11 |
| conflict at the base merge | 5 |
| pinned on purpose | 4 |
| follows a generic recipe's pin | 3 |
| #890 | 1 |
| current | 1 |
| **Total** | 260 |

No row reads `current` beside a `not read`. The fork-own BEHIND row is `cairo` (F-05, a Backlog bump in #839's shape); `glslang` is CURRENT and an orphan.

**The effective pin is not always the recipe's** (`device-builds.md` § After rebasing item 3). Six of the 43 sourcing overrides reset what the build fetches:
- `opus`, 1.5.2 from a xiph mirror;
- `gcc`, 15.2.0;
- `libfmt`, 9.1.0 outside SM8550, #877;
- `wavpack` and `zlib`, their own release URLs;
- `libfreeaptx`, its own checksum.

The table's pin column carries the effective value per plan; `libfmt` is the only one that differs between plans.

**The orphan table (11):**

| # | Orphan | What the fork used it for | Effective now | After the base merge | Upstream's deleting commit | Fork-own dependants |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `audio/libfreeaptx/package.mk` | its own `PKG_SHA256` over the generic URL | `0.2.2` | 0.2.2 | `6103571f67 2026-10-11` | none (by name: 0 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 2 | `audio/opus/package.mk` | 1.5.2 over the generic 1.6.1, from a xiph mirror | `1.5.2` | 1.6.1 | `075a7c303b 2026-10-17` | `multimedia/opusfile/package.mk` (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 3 | `devel/libfmt/package.mk` | 9.1.0 on every plan but SM's (#877) | `9.1.0 / 12.2.0` | 12.2.0 | `6103571f67 2026-10-11` | none (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 4 | `graphics/glslang/package.mk` | 16.6.0, the fork's own bump (`b4fc2a28cf`); spirv-tools' pin follows its `known_good.json` | `16.6.0` | 16.5.0 | `6679670966 2026-10-01` | `apps/mangohud/package.mk` (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 5 | `graphics/vulkan/vulkan-headers/package.mk` | ROCKNIX's own copy | `1.4.347` | 1.4.359 | `075a7c303b 2026-10-17` | `apps/mangohud/package.mk` (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 6 | `rust/cargo/package.mk` | ROCKNIX's own copy | `1.94.1` | $(get_pkg_version rust) | `6679670966 2026-10-01` | none (by name: 5 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 7 | `tools/miniupnpc/package.mk` | ROCKNIX's own copy | `2.3.3` | 2.3.3 | `6103571f67 2026-10-11` | `virtual/network/package.mk` (by name: 3 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 8 | `tools/rocknix-abl/package.mk` | SM8550's bootloader payload (`9aa7affee9`, #600) | `1.2` | none: replaced by `openabl` (`71d8932b33`) | `71d8932b33 2026-10-14` | none (by name: 0 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 9 | `wayland/lib/tllist/package.mk` | ROCKNIX's own copy | `1.1.0` | 1.1.0 | `6679670966 2026-10-01` | none (by name: 1 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 10 | `wayland/mtdev/package.mk` | ROCKNIX's own copy | `1.1.6` | 1.1.7 | `6103571f67 2026-10-11` | none (by name: 1 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 11 | `wayland/util/swaybg/package.mk` | ROCKNIX's own copy | `1.2.1` | 1.2.2 | `6103571f67 2026-10-11` | `wayland/compositor/sway/package.mk` (by name: 1 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |

**The conflict list (11, `git merge-tree` at `8ebaf8daad` against `upstream/next`):**

| # | Path | `merge-tree` | Disposition |
| ---: | --- | --- | --- |
| 1 | `apps/gamescope/package.mk` | auto-merges | different, keep ours: upstream bumps the pin to `6867f509...` (3.16.31), ours adds the glm/stb packages; the wraps at both commits name the same revisions, so the auto-merge builds (`:55` would stop it otherwise) |
| 2 | `graphics/cairo/package.mk` | content | conflict: upstream's is a sourcing override too; take its shape, keep ours' xcb/xlib-xcb options; the version line becomes the generic's |
| 3 | `graphics/glslang/package.mk` | modify/delete | conflict: upstream deleted it (the generic is 16.5.0); ours is 16.6.0 and `spirv-tools` follows 16.6.0's `known_good.json` -- taking the deletion downgrades glslang under spirv-tools (F-11) |
| 4 | `graphics/spirv-tools/package.mk` | content | conflict: upstream made it a sourcing override; ours pins `ef96ed76...` to glslang 16.6.0 with a GCC 12 diagnostic; resolve with glslang (F-11) |
| 5 | `lang/gcc/package.mk` | content | conflict: ours enables libatomic for x86_64; upstream restructured it for aarch64 only and dropped the 15.2.0 hold (the generic is 16.2.0); keep the x86_64 case and decide the hold |
| 6 | `misc/modules/sources/gamelist.xml` | auto-merges | different, keep ours: ours rewrites descriptions (identity); upstream removes the AetherSX2 entry |
| 7 | `multimedia/gstreamer/gst-plugins-base/package.mk` | content | conflict: both enable GL; ours keeps the install WebKit needs (#228); take upstream's GLES/EGL options and keep ours' install |
| 8 | `multimedia/gstreamer/gstreamer/package.mk` | add/add | conflict: added on both sides; ours enables the plugin registry WebKit needs, upstream's removes `/usr/share`; keep ours, check upstream's removal against the registry |
| 9 | `network/networkmanager/config/NetworkManager.conf` | content | same change: both add `hostname-mode=none`; drop ours' comment-only hunk |
| 10 | `tools/rocknix-abl/package.mk` | modify/delete | conflict: upstream replaced it with `openabl`; ours carries the v1.2 checksum fix; take the deletion and check SM8550's bootloader against `openabl` |
| 11 | `wayland/compositor/sway/autostart/111-sway-init` | content | different, keep ours: ours adds the virtio `Virtual` connector and the software cursor (GENERIC_X64); upstream adds essway masking, AFBC and the Duo Lite case; both |

(the 260 generated Q4 rows are the next part, `q4-table.md`)

### Q5 Efficiency

**Not measured:** no build runs. Read:
- **`gcc`'s hold** at 15.2.0 keeps the cross toolchain a major behind the generic 16.2.0; its recipe gives no reason.
- **`box86` and `lib32`** carry the 32-bit chain on ARM (the fork renamed their compatibility roots, `43d0bc3bf4`).
- **The GStreamer trio** installs what WebKit loads.

**On the boot path:**
- **`sway-ready`** (fork-added, `c6afa31db1`) polls for a responsive compositor every 0.1 s with a 1 s bound per round trip, and gives up at 15 s.
- **`111-sway-init`'s added lines** are two greps and an echo.

Neither is measured here; `tools/time-to-play` would show a change.

### Q6 Dead ends

**The 13 unbuilt names:**
- the 12 virtual packages, by construction (no source);
- **`qcom-abl`**, built by SM8550's plan alone: `viewplan` lists it there and nowhere else, it is stamped in the SM8550 roots, and its `PKG_URL` is empty.

**Read by stamps,** every plan's reached recipes are built in that plan's root (P14): no plan reading is contradicted by a `PKG_ARCH`.

**The units:**
- **`xorg-configure@.service` and `97-xorg.rules`** (F-10) are wired to a script no image installs, and are reached only on a PCI VGA-class display, which no shipped image has.
- **`batteryplus` and `inputplumber`** are each device-scoped and present where they ship.

**The orphans' dependants** are in the orphan table: none breaks by name.

### Q7 Clarity and structure

**The fork's 35 changes, each with its reason and what the base merge does to it:**

| # | Fork change | Since the base | Reason (the newest commit) | At the base merge |
| ---: | --- | --- | --- | --- |
| 1 | `apps/gamescope-glm/package.mk` | added | `5b5005879e` gamescope: glm and stb come from pinned sources, never from a clone | stays: no upstream copy |
| 2 | `apps/gamescope-stb/package.mk` | added | `5b5005879e` gamescope: glm and stb come from pinned sources, never from a clone | stays: no upstream copy |
| 3 | `apps/gamescope/package.mk` | edited | `5b5005879e` gamescope: glm and stb come from pinned sources, never from a clone | auto-merges (both changed) |
| 4 | `apps/m8c/config/GENERIC_X64/config.ini` | added | `cbdb91a517` GENERIC_X64 - add per-device emulator/app configs | stays: no upstream copy |
| 5 | `apps/mangohud-vulkan-headers/package.mk` | added | `50f3eeb726` mangohud: the two Vulkan subprojects come from pinned sources in meson's cache, never from a downlo | stays: no upstream copy |
| 6 | `apps/mangohud-vulkan-utility-libraries/package.mk` | added | `50f3eeb726` mangohud: the two Vulkan subprojects come from pinned sources in meson's cache, never from a downlo | stays: no upstream copy |
| 7 | `apps/mangohud/package.mk` | edited | `50f3eeb726` mangohud: the two Vulkan subprojects come from pinned sources in meson's cache, never from a downlo | the fork's change stays (upstream did not touch it) |
| 8 | `compat/box86/package.mk` | edited | `43d0bc3bf4` build - use the distribution name for ARM compatibility roots | the fork's change stays (upstream did not touch it) |
| 9 | `compat/lib32/package.mk` | edited | `43d0bc3bf4` build - use the distribution name for ARM compatibility roots | the fork's change stays (upstream did not touch it) |
| 10 | `graphics/cairo/package.mk` | edited | `bccbf54cd4` packages: comments said once and true; an empty quirk removed | conflict (content): see § The conflict set |
| 11 | `graphics/glslang/package.mk` | edited | `b4fc2a28cf` dependencies: qualify current coupled shader and Rust tools | conflict (modify/delete): see § The conflict set |
| 12 | `graphics/harfbuzz-icu/package.mk` | added | `4e4c31fc4c` harfbuzz-icu: install into the sysroot so WebKit can link it | stays: no upstream copy |
| 13 | `graphics/spirv-tools/package.mk` | edited | `f5f815faff` spirv-tools: tolerate GCC 12 host vector diagnostic | conflict (content): see § The conflict set |
| 14 | `initramfs/config/initramfs.x86_64.conf` | added | `5a00d9963c` GENERIC_X64 - initramfs - add /lib64 symlink for x86_64 loader | stays: no upstream copy |
| 15 | `lang/gcc/package.mk` | edited | `74377a057f` GENERIC_X64 - gcc: enable libatomic for x86_64 | conflict (content): see § The conflict set |
| 16 | `misc/modules/sources/gamelist.xml` | edited | `13ae350769` pixelelated: fix Tools identity and retain qualified VM evidence | auto-merges (both changed) |
| 17 | `multimedia/gstreamer/gst-plugins-bad/package.mk` | added | `5faa73834e` gst-plugins-base/bad: a payload is a name that loads | stays: no upstream copy |
| 18 | `multimedia/gstreamer/gst-plugins-base/package.mk` | edited | `5faa73834e` gst-plugins-base/bad: a payload is a name that loads | conflict (content): see § The conflict set |
| 19 | `multimedia/gstreamer/gstreamer/package.mk` | added | `fac608ff89` gstreamer: retain network library for installed plugins | conflict (add/add): see § The conflict set |
| 20 | `multimedia/libplacebo/package.mk` | edited | `d47acf6693` GENERIC_X64 - libplacebo: fix glslang/SPIRV link + disable demos for x86_64 | the fork's change stays (upstream did not touch it) |
| 21 | `multimedia/opusfile/package.mk` | edited | `63a2090a56` packages: pin retained game data and record licence scope | the fork's change stays (upstream did not touch it) |
| 22 | `network/avahi/package.mk` | edited | `1d07330ae1` avahi: the fork's unit ships; network-base-setup tells an already-up responder the name -- PL-01 (# | the fork's change stays (upstream did not touch it) |
| 23 | `network/avahi/system.d/avahi-daemon.service` | edited | `e76bafe860` avahi: the mDNS responder is on, after the device has its name (#50, D-NET-003) | the fork's change stays (upstream did not touch it) |
| 24 | `network/enet/package.mk` | edited | `63a2090a56` packages: pin retained game data and record licence scope | the fork's change stays (upstream did not touch it) |
| 25 | `network/networkmanager/config/NetworkManager.conf` | edited | `22e43d47c7` network: system.hostname owns the device name; NetworkManager leaves it alone; the name is applied  | conflict (content): see § The conflict set |
| 26 | `network/tailscale/package.mk` | edited | `63a2090a56` packages: pin retained game data and record licence scope | the fork's change stays (upstream did not touch it) |
| 27 | `network/zerotier-one/package.mk` | edited | `077197e6cd` zerotier-one: isolate client sources and retain proof (#528) | the fork's change stays (upstream did not touch it) |
| 28 | `security/gnutls/package.mk` | added | `4e464d7045` gnutls: point it at the CA bundle the image already ships | stays: no upstream copy |
| 29 | `tools/installer/scripts/installer` | edited | `a9af618398` pixelelated: apply lowercase identity and LCD wordmark | the fork's change stays (upstream did not touch it) |
| 30 | `tools/rocknix-abl/package.mk` | edited | `9aa7affee9` rocknix-abl: apply upstream v1.2 checksum fix (#600) | conflict (modify/delete): see § The conflict set |
| 31 | `tools/rocknix-splash/package.mk` | edited | `b137d8c373` pixelelated: integrate Ocean splash and finalize candidate inputs | the fork's change stays (upstream did not touch it) |
| 32 | `virtual/network/package.mk` | edited | `6e35a5fd04` raofflineproxy: package RAOfflineProxy's Linux service natively (#165) | the fork's change stays (upstream did not touch it) |
| 33 | `wayland/compositor/sway/autostart/111-sway-init` | edited | `ca39dd3519` GENERIC_X64 - sway - use software cursor on virtual displays | conflict (content): see § The conflict set |
| 34 | `wayland/compositor/sway/package.mk` | edited | `c6afa31db1` sway: wait for usable Wayland before starting ES | the fork's change stays (upstream did not touch it) |
| 35 | `wayland/compositor/sway/scripts/sway-ready` | added | `c6afa31db1` sway: wait for usable Wayland before starting ES | stays: no upstream copy |

- **Same change on both sides:** `NetworkManager.conf` (`hostname-mode=none`): drop ours' comment-only hunk at the merge.
- **An override that could be smaller:** `cairo`'s, once upstream's sourcing override lands (its own comment says the version line becomes redundant).
- **A constraint without its reason:** `gcc`'s 15.2.0 (F-09's note).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- **`device-builds.md` § After rebasing:** read a modify/delete conflict on an override against the generic copy's pin before taking the deletion (F-11). The sentence, for the coordinator: *a deletion upstream of an override the fork has bumped puts the generic pin back; compare the two before resolving.*

### Codification Gaps (needs-new-rule)

- **The pre-merge read of the fork-edited ∩ upstream-changed set**, by `git merge-tree` with each orphan's pin before and after, is what this slice did by hand. It belongs in `rc-preflight`'s step-0 base check, as the brief's ladder proposes (an issue the coordinator files).

### Recommended Action Sequence

1. #852's stream (this slice).
2. #890's packet ahead of T5 (done, the coordinator's).
3. The conflict list and the orphan table read at the base merge (the integration).
4. `cairo`'s Backlog bump.
5. The rest at their owners (#585, #657).

## Second opinion (Phase 4.6)

**Pending at the time of writing:** one GPT-6 Astra seat at `max` through the Facilitator, a probe and then one refutation over one bounded packet (`second-opinions/gpt-brief.md`). Its size and sha256 are recorded in `00`. Each item will be graded here against its artifact.

## Quality Self-Check

- **Tables:** every row of the coverage, currency, orphan and conflict tables comes from `tools/t8-tables.py`, which asserts 485 and 260 and that each conflict's kind equals `merge-tree`'s.
- **Times:** every time is a `date -u` reading or a file a command wrote.
- **The brief's deltas** are named in `03` § 3.3.
- **What was not read** is in § Coverage Boundary, and no row claims it.

## q4-table.md (whole)

# Q4 currency table — M6.P2 T8 (#655)

The 260 recipes at `8ebaf8daad`'s bytes, generated by `tools/t8-tables.py q4`; `q4-pins.json` is the same rows with every field. **Pin (effective)** is `config/options <name>` for GENERIC_X64, H700 and SM8550; (a) is `upstream/next` `e0f9deb899` with the base `c445081a59` deciding orphan or fork-added; `make update` is RK3588's set (the Makefile's device); (c) is the project, read for the fork's recipes (the freshness tool, or by hand where it cannot see them) and the GitHub hash pins (`compare`), and `not read` elsewhere. The disposition names the mover.

| Recipe path | Name | Pin (effective: GENERIC_X64, H700, SM8550) | Shape | (a) upstream/next | make update | (c) the project | Disposition (the mover) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/ROCKNIX/packages/apps/commander/package.mk` | `commander` | `b3c008cac3bf` | hash | differs | - | at the default branch's HEAD | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/apps/control-gen/package.mk` | `control-gen` | `1.0` | version | identical | in the set, blocklisted | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/gamecontrollerdb/package.mk` | `gamecontrollerdb` | `42f28e22d207` | hash | identical | in the set (never run) | 30 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/gamepadtester/package.mk` | `gamepadtester` | `6ac49e67aa98` | hash | differs | - | at the default branch's HEAD | follows the base merge: upstream's pin `b06fef21d7e6` |
| `projects/ROCKNIX/packages/apps/gamescope-glm/package.mk` | `gamescope-glm` | `0af55ccecd98` | hash | absent: fork-added | - | PINNED (latest `119`) | pinned on purpose: follows subprojects/glm.wrap at gamescope's pinned commit |
| `projects/ROCKNIX/packages/apps/gamescope-stb/package.mk` | `gamescope-stb` | `5736b15f7ea0` | hash | absent: fork-added | - | PINNED (latest `88`) | pinned on purpose: follows subprojects/stb.wrap at gamescope's pinned commit |
| `projects/ROCKNIX/packages/apps/gamescope/package.mk` | `gamescope` | `fa0b4d334207` | hash | differs | - | 197 behind the default branch | follows the base merge (auto-merges): different, keep ours: upstream bumps the pin to `6867f509...` (3.16.31), ours adds the glm/stb packages; the wraps at both commits name the same revisions, so the auto-merge builds (`:55` would stop it otherwise) |
| `projects/ROCKNIX/packages/apps/jstest-sdl/package.mk` | `jstest-sdl` | `f4fdf6daae68` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/list-guid/package.mk` | `list-guid` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/m8c/package.mk` | `m8c` | `v1.7.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/mako-notify/package.mk` | `mako-notify` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/mako-osd/package.mk` | `mako-osd` | `b131bc143f6b` | hash | identical | - | 23 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/mangohud-vulkan-headers/package.mk` | `mangohud-vulkan-headers` | `1.4.346` | version | absent: fork-added | - | PINNED (latest `1.4.366`) | pinned on purpose: follows subprojects/vulkan-headers.wrap at mangohud's pinned commit |
| `projects/ROCKNIX/packages/apps/mangohud-vulkan-utility-libraries/package.mk` | `mangohud-vulkan-utility-libraries` | `1.4.346` | version | absent: fork-added | - | PINNED (latest `1.4.366`) | pinned on purpose: follows subprojects/vulkan-utility-libraries.wrap at mangohud's pinned commit |
| `projects/ROCKNIX/packages/apps/mangohud/package.mk` | `mangohud` | `992103e4fb74` | hash | differs | - | 216 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/apps/moonlight/package.mk` | `moonlight` | `a6bf7154a743` | hash | differs | in the set (never run) | 16 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/oga_controls/package.mk` | `oga_controls` | `1604ee24150c` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/portmaster/package.mk` | `portmaster` | `2026.09.13-0343` | version | differs | in the set, blocklisted | not read: follows the base merge | follows the base merge: upstream's pin `2026.06.23-0` |
| `projects/ROCKNIX/packages/apps/qterminal/layer-shell-qt/package.mk` | `layer-shell-qt` | `v6.4.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/qterminal/lxqt-build-tools/package.mk` | `lxqt-build-tools` | `2.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/qterminal/package.mk` | `qterminal` | `2.2.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/qterminal/qtermwidget/package.mk` | `qtermwidget` | `2.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/rocknix-hotkey/package.mk` | `rocknix-hotkey` | `cc3a863199a7` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/rocknix-screenshot/package.mk` | `rocknix-screenshot` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/rocknix-touchscreen-keyboard/package.mk` | `rocknix-touchscreen-keyboard` | `v0.17` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/sdl2notify/package.mk` | `sdl2notify` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/sdl2text/package.mk` | `sdl2text` | `v1.0` | version | identical | in the set (never run) | not read: follows the base merge | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/sdljoytest/package.mk` | `sdljoytest` | `811d9875e0c1` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/sdltouchtest/package.mk` | `sdltouchtest` | `b62dae0d6233` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/audio/SDL2_mixer/package.mk` | `SDL2_mixer` | `2.8.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/alsa-lib/package.mk` | `alsa-lib` | `1.2.14` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/audio/alsa-ucm-conf/package.mk` | `alsa-ucm-conf` | `1.2.13` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/audio/alsa-utils/package.mk` | `alsa-utils` | `1.2.14` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/audio/espeak/package.mk` | `espeak` | `1.48.04-source` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/fluidsynth/package.mk` | `fluidsynth` | `2.5.7` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/ldacBT/package.mk` | `ldacBT` | `2.0.2.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libao/package.mk` | `libao` | `1.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libfreeaptx/package.mk` | `libfreeaptx` | `0.2.2` | sourcing override | absent: orphan | - | INHERITED | orphan: dropped by the base merge; the fork used it for its own `PKG_SHA256` over the generic URL; after it, 0.2.2; dependants resolve by name |
| `projects/ROCKNIX/packages/audio/libogg/package.mk` | `libogg` | `1.3.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libsndfile/package.mk` | `libsndfile` | `e486f20` | hash (short) | identical | - | 50 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libvorbis/package.mk` | `libvorbis` | `1.3.7` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libxmp/package.mk` | `libxmp` | `8201d26cf933` | hash | identical | - | 425 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/opus/package.mk` | `opus` | `1.5.2` | sourcing override (sets its own pin) | absent: orphan | - | UNKNOWN: no resolver for ftp.osuosl.org, or it did not answer | orphan: dropped by the base merge; the fork used it for 1.5.2 over the generic 1.6.1, from a xiph mirror; after it, 1.6.1; dependants resolve by name |
| `projects/ROCKNIX/packages/audio/pipewire/package.mk` | `pipewire` | `1.2.6` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `1.6.8` |
| `projects/ROCKNIX/packages/audio/pulseaudio/package.mk` | `pulseaudio` | `17.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/sndio/package.mk` | `sndio` | `1.10.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/wavpack/package.mk` | `wavpack` | `5.9.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/wireplumber/package.mk` | `wireplumber` | `0.5.7` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `0.5.15` |
| `projects/ROCKNIX/packages/compat/box64/package.mk` | `box64` | `2f130fab1d6e` | hash | identical | in the set (never run) | 429 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/compat/box86/package.mk` | `box86` | `39d3ed203323` | hash | differs | in the set (never run) | 7 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/compat/fex-emu/package.mk` | `fex-emu` | `e869aa644a16` | hash | differs | - | 522 behind the default branch | follows the base merge: upstream's pin `14c92681f4d6` |
| `projects/ROCKNIX/packages/compat/lib32/package.mk` | `lib32` | `1.0` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/compat/wine/package.mk` | `wine` | `11.0` | version | identical | in the set (never run) | not read: follows the base merge | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/compress/cabextract/package.mk` | `cabextract` | `1.11` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/gzip/package.mk` | `gzip` | `1.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/libarchive/package.mk` | `libarchive` | `3.8.9` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/libzip/package.mk` | `libzip` | `1.11.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/compress/p7zip/package.mk` | `p7zip` | `16.02` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/xz/package.mk` | `xz` | `5.8.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/compress/zip/package.mk` | `zip` | `3.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/zlib/package.mk` | `zlib` | `1.3.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/debug/apitrace/package.mk` | `apitrace` | `45a005875d34` | hash | identical | - | 84 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_gfx/package.mk` | `SDL2_gfx` | `29927b3` | hash (short) | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_image/package.mk` | `SDL2_image` | `2.8.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_net/package.mk` | `SDL2_net` | `2.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_ttf/package.mk` | `SDL2_ttf` | `2.20.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL3_ttf/package.mk` | `SDL3_ttf` | `3.2.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/boost/package.mk` | `boost` | `1.86.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/ccache/package.mk` | `ccache` | `4.13.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/cmake/package.mk` | `cmake` | `4.4.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/ecm/package.mk` | `ecm` | `v6.16.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/glib/package.mk` | `glib` | `2.89.3` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/glibc/package.mk` | `glibc` | `2.41` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `2.44` |
| `projects/ROCKNIX/packages/devel/json-glib/package.mk` | `json-glib` | `1.10.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/libaio/package.mk` | `libaio` | `0.3.113` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) (F-03) |
| `projects/ROCKNIX/packages/devel/libclc/package.mk` | `libclc` | `22.1.8` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libcom-err/package.mk` | `libcom-err` | `1.47.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libdatrie/package.mk` | `libdatrie` | `0.2.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libfmt/package.mk` | `libfmt` | GENERIC_X64 `9.1.0`; H700 `9.1.0`; SM8550 `12.2.0` | sourcing override (sets its own pin) | absent: orphan | - | INHERITED | orphan: dropped by the base merge; the fork used it for 9.1.0 on every plan but SM's (#877); after it, 12.2.0; dependants resolve by name |
| `projects/ROCKNIX/packages/devel/libpthread-stubs/package.mk` | `libpthread-stubs` | `0.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libserialport/package.mk` | `libserialport` | `21b3dfe5f68c` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libthai/package.mk` | `libthai` | `0.1.29` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/make/package.mk` | `make` | `4.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/ncurses/package.mk` | `ncurses` | `6.5` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/patchelf/package.mk` | `patchelf` | `0.18.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/rapidjson/package.mk` | `rapidjson` | `1.1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/readline/package.mk` | `readline` | `8.3` | sourcing override | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/shared-mime-info/package.mk` | `shared-mime-info` | `2.4` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/swig/package.mk` | `swig` | `4.1.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/xa/package.mk` | `xa` | `2.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/fonts/dejavu/package.mk` | `dejavu` | `2.37` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/fonts/noto-sans-cjk/package.mk` | `noto-sans-cjk` | `2.004` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/fonts/spleen-font/package.mk` | `spleen-font` | `2.0.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/SDL2/package.mk` | `SDL2` | `2.32.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/SDL3/package.mk` | `SDL3` | `3.4.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/armsx2-turnip/package.mk` | `armsx2-turnip` | `axfl1-011` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/cairo/package.mk` | `cairo` | `1.18.4` | version | differs | - | BEHIND (latest `1.18.6`, cairographics.org's listing) | conflict at the base merge (content): conflict: upstream's is a sourcing override too; take its shape, keep ours' xcb/xlib-xcb options; the version line becomes the generic's; and fork's: Backlog bump proposed (#839's shape), 1.18.4 -> 1.18.6 (F-05) |
| `projects/ROCKNIX/packages/graphics/capsimg/package.mk` | `capsimg` | `ed4cb0912fb1` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/fbgrab/package.mk` | `fbgrab` | `5c2481d2b67b` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/gdk-pixbuf/package.mk` | `gdk-pixbuf` | `2.42.10` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/glew/package.mk` | `glew` | `2.2.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/glfw/package.mk` | `glfw` | `e2c9264` | hash (short) | identical | - | 1055 behind the default branch, 627 not on it | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/glslang/package.mk` | `glslang` | `16.6.0` | version | absent: orphan | - | CURRENT (latest `16.6.0`) | orphan, a modify/delete conflict at the base merge: dropped by the base merge; the fork used it for 16.6.0, the fork's own bump (`b4fc2a28cf`); spirv-tools' pin follows its `known_good.json`; after it, 16.5.0; dependants resolve by name (F-11) |
| `projects/ROCKNIX/packages/graphics/grim/package.mk` | `grim` | `1.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/gtk2/package.mk` | `gtk2` | `2.24.33` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/gtk3/package.mk` | `gtk3` | `3.24.52` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/harfbuzz-icu/package.mk` | `harfbuzz-icu` | `14.3.0` | sourcing override | absent: fork-added | - | INHERITED | follows the generic recipe's pin (T7's row); the override adds options |
| `projects/ROCKNIX/packages/graphics/imagemagick/package.mk` | `imagemagick` | `7.1.2-29` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libdrm/package.mk` | `libdrm` | `2.4.133` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libepoxy/package.mk` | `libepoxy` | `1.5.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libglvnd/package.mk` | `libglvnd` | `1.7.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libjpeg-turbo/package.mk` | `libjpeg-turbo` | `3.2.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libpng/package.mk` | `libpng` | `1.6.40` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/librashader/package.mk` | `librashader` | `76462c030b75` | hash | identical | - | 85 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libwebp/package.mk` | `libwebp` | `1.6.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/lsfg-vk/package.mk` | `lsfg-vk` | `8b0da2661c6f` | hash | identical | - | unknown: compare found no common ancestor | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/mesa-demos/package.mk` | `mesa-demos` | `9.0.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/mesa/package.mk` | `mesa` | `26.2.2` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `26.2.4` |
| `projects/ROCKNIX/packages/graphics/plutosvg/package.mk` | `plutosvg` | `0.0.7` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/plutovg/package.mk` | `plutovg` | `1.3.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/qt6/package.mk` | `qt6` | `6.10.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/renderdoc/package.mk` | `renderdoc` | `v1.44` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/shaderc/package.mk` | `shaderc` | `2025.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/spirv-llvm-translator/package.mk` | `spirv-llvm-translator` | `22.1.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/spirv-tools/package.mk` | `spirv-tools` | `ef96ed763b43` | hash | differs | - | 73 behind the default branch | conflict at the base merge (content): conflict: upstream made it a sourcing override; ours pins `ef96ed76...` to glslang 16.6.0 with a GCC 12 diagnostic; resolve with glslang (F-11) |
| `projects/ROCKNIX/packages/graphics/tiff/package.mk` | `tiff` | `4.7.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/vulkan/vulkan-headers/package.mk` | `vulkan-headers` | `1.4.347` | version | absent: orphan | - | BEHIND (latest `1.4.366`) | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.4.359; dependants resolve by name |
| `projects/ROCKNIX/packages/graphics/vulkan/vulkan-loader/package.mk` | `vulkan-loader` | `1.4.347` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/vulkan/vulkan-tools/package.mk` | `vulkan-tools` | `1.4.347` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/waffle/package.mk` | `waffle` | `5f1f48287e80` | hash | differs | - | unknown: gitlab.freedesktop.org is not GitHub | follows the base merge: upstream's pin `3b20e4d7bccc` |
| `projects/ROCKNIX/packages/graphics/wxwidgets/package.mk` | `wxwidgets` | `db1005db3dea` | hash | differs | - | 1631 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/lang/gcc/package.mk` | `gcc` | `15.2.0` | sourcing override (sets its own pin) | differs | - | not read: the tool lists only recipes added since the base | conflict at the base merge (content): conflict: ours enables libatomic for x86_64; upstream restructured it for aarch64 only and dropped the 15.2.0 hold (the generic is 16.2.0); keep the x86_64 case and decide the hold |
| `projects/ROCKNIX/packages/lang/go/package.mk` | `go` | `1.21.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/lang/llvm/package.mk` | `llvm` | `22.1.8` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/lang/lua54/package.mk` | `lua54` | `5.4.6` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/lang/luajit/package.mk` | `luajit` | `1edc3e52b67e` | hash | identical | - | 31 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/lang/nasm/package.mk` | `nasm` | `2.16.01` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/misc/modules/package.mk` | `modules` | `1.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/ffmpeg/package.mk` | `ffmpeg` | `7.1.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `9.0` |
| `projects/ROCKNIX/packages/multimedia/gmu/package.mk` | `gmu` | `3aed18be8a50` | hash | identical | - | 31 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-libav/package.mk` | `gst-libav` | `1.29.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-bad/package.mk` | `gst-plugins-bad` | `1.29.2` | sourcing override | absent: fork-added | - | INHERITED | follows the generic recipe's pin (T7's row); the override adds options |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-base/package.mk` | `gst-plugins-base` | `1.29.2` | sourcing override | differs | - | not read: the tool lists only recipes added since the base | conflict at the base merge (content): conflict: both enable GL; ours keeps the install WebKit needs (#228); take upstream's GLES/EGL options and keep ours' install |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-good/package.mk` | `gst-plugins-good` | `1.29.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gstreamer/package.mk` | `gstreamer` | `1.29.2` | sourcing override | differs | - | not read: the tool lists only recipes added since the base | conflict at the base merge (add/add): conflict: added on both sides; ours enables the plugin registry WebKit needs, upstream's removes `/usr/share`; keep ours, check upstream's removal against the registry |
| `projects/ROCKNIX/packages/multimedia/libdvbpsi/package.mk` | `libdvbpsi` | `1.3.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/libplacebo/package.mk` | `libplacebo` | `05ac2cca6571` | hash | differs | - | unknown: code.videolan.org is not GitHub | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/libvpx/package.mk` | `libvpx` | `df655cf4fb6c` | hash | differs | - | 794 behind the default branch | follows the base merge: upstream's pin `1.16.0` |
| `projects/ROCKNIX/packages/multimedia/mpv/package.mk` | `mpv` | `41f6a6450684` | hash | differs | - | 1293 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/opusfile/package.mk` | `opusfile` | `9d718345ce03` | hash | differs | - | 19 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/vlc/package.mk` | `vlc` | `3.0.23` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/x264/package.mk` | `x264` | `0480cb05fa18` | sourcing override | identical | - | unknown: code.videolan.org is not GitHub | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/avahi/package.mk` | `avahi` | `0.8` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/bluez/package.mk` | `bluez` | `5.83` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/enet/package.mk` | `enet` | `v1.3.18` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/fping/package.mk` | `fping` | `5.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/iwd/package.mk` | `iwd` | `3.12` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/libndp/package.mk` | `libndp` | `1.9` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/libpcap/package.mk` | `libpcap` | `1.10.4` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/libslirp/package.mk` | `libslirp` | `4.7.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/networkmanager/package.mk` | `networkmanager` | `1.51.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/nfs-utils/package.mk` | `nfs-utils` | `2.6.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/openssh/package.mk` | `openssh` | `9.8p1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/samba/package.mk` | `samba` | `4.21.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `4.24.5` |
| `projects/ROCKNIX/packages/network/simple-http-server/package.mk` | `simple-http-server` | `0.8.0` | version | identical | - | not read: follows the base merge | #890: filed and fixed in a packet ahead of T5 (`fix-tree`); follows the base merge |
| `projects/ROCKNIX/packages/network/sixaxis/package.mk` | `sixaxis` | `f53b0ca28c35` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/network/speedtest-cli/package.mk` | `speedtest-cli` | `v2.1.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/syncthing/package.mk` | `syncthing` | `2.0.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/tailscale/package.mk` | `tailscale` | `1.98.8` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/zerotier-one/package.mk` | `zerotier-one` | `1.16.0` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/print/poppler/package.mk` | `poppler` | `23.05.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/python/devel/pyxel/package.mk` | `pyxel` | `2.9.9` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/rust/cargo/package.mk` | `cargo` | `1.94.1` | version | absent: orphan | - | LOCAL | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, $(get_pkg_version rust); dependants resolve by name |
| `projects/ROCKNIX/packages/rust/rust/package.mk` | `rust` | `1.94.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/security/gnutls/package.mk` | `gnutls` | `3.8.13` | sourcing override | absent: fork-added | - | INHERITED | follows the generic recipe's pin (T7's row); the override adds options |
| `projects/ROCKNIX/packages/security/libgpg-error/package.mk` | `libgpg-error` | `1.61` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/security/openssl/package.mk` | `openssl` | `3.6.3` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/bdf2psf/package.mk` | `bdf2psf` | `1.249` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/expat/package.mk` | `expat` | `2.8.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/icu/package.mk` | `icu` | `74.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/textproc/inih/package.mk` | `inih` | `r62` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/jsoncpp/package.mk` | `jsoncpp` | `1.9.8` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/libiconv/package.mk` | `libiconv` | `1.19` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/textviewer/package.mk` | `textviewer` | `fcbda2d1708e` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/at-spi2-atk/package.mk` | `at-spi2-atk` | `2.38.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/at-spi2-core/package.mk` | `at-spi2-core` | `2.45.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/tools/atf/package.mk` | `atf` | GENERIC_X64 `2.10.0`; H700 `2.12.0`; SM8550 `2.10.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `2.12.0` |
| `projects/ROCKNIX/packages/tools/batteryplus/package.mk` | `batteryplus` | `1c31e89ec182` | hash | differs | - | 2 behind the default branch | follows the base merge: upstream's pin `31a3b629bc22` |
| `projects/ROCKNIX/packages/tools/bin2c/package.mk` | `bin2c` | `1.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/coreutils/package.mk` | `coreutils` | `9.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/dialog/package.mk` | `dialog` | `1.3-20231002` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/empty/package.mk` | `empty` | `0.6.23c` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/entware/package.mk` | `entware` | - | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/freeimage/package.mk` | `freeimage` | `3180` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk` | `gamepadcalibration` | `2077e7af7e9a` | hash | differs | - | 1 behind the default branch, 8 not on it | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/tools/inputplumber/package.mk` | `inputplumber` | `v0.79.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `0.82.0` |
| `projects/ROCKNIX/packages/tools/installer/package.mk` | `installer` | `1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/joyutils/package.mk` | `joyutils` | `b6703ebf04c8` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/miniupnpc/package.mk` | `miniupnpc` | `2.3.3` | version | absent: orphan | - | UNKNOWN: no resolver for miniupnp.free.fr, or it did not answer | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 2.3.3; dependants resolve by name |
| `projects/ROCKNIX/packages/tools/mkbootimg/package.mk` | `mkbootimg` | `d2bb0af5ba6d` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/procps-ng/package.mk` | `procps-ng` | `4.0.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/pyudev/package.mk` | `pyudev` | `5e00141` | hash (short) | identical | - | 133 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/qcom-abl/package.mk` | `qcom-abl` | `1.0` | local payload (no `PKG_URL`) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk` | `rocknix-abl` | `1.2` | version | absent: orphan | - | UNKNOWN: no resolver for github.com, or it did not answer | orphan, a modify/delete conflict at the base merge: dropped by the base merge; the fork used it for SM8550's bootloader payload (`9aa7affee9`, #600); after it, none: replaced by `openabl` (`71d8932b33`); dependants resolve by name (F-04) |
| `projects/ROCKNIX/packages/tools/rocknix-splash/package.mk` | `rocknix-splash` | `8c71126ceef7` | hash | differs | - | at the default branch's HEAD | current |
| `projects/ROCKNIX/packages/tools/six/package.mk` | `six` | `02c3bca` | hash (short) | identical | - | 21 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/socat/package.mk` | `socat` | `1.7.4.4` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `1.8.1.3` |
| `projects/ROCKNIX/packages/tools/sound/libvorbisidec/package.mk` | `libvorbisidec` | `a76e41f6ece9` | hash | identical | - | 19 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/sound/mpg123/package.mk` | `mpg123` | `1.33.7` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/sound/soundfont-generaluser/package.mk` | `soundfont-generaluser` | `8fe2798` | hash (short) | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/arm/package.mk` | `arm` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/debug/package.mk` | `debug` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/es-themes/package.mk` | `es-themes` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/gamesupport/package.mk` | `gamesupport` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/image/package.mk` | `image` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) (F-02, #852) |
| `projects/ROCKNIX/packages/virtual/initramfs/package.mk` | `initramfs` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/libc/package.mk` | `libc` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/linux-drivers/package.mk` | `linux-drivers` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/linux-firmware/package.mk` | `linux-firmware` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/network/package.mk` | `network` | - | virtual (no source) | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/virtual/swaywm-env/package.mk` | `swaywm-env` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/synctools/package.mk` | `synctools` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/compositor/sway/package.mk` | `sway` | `1.11` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream's pin `1.9` |
| `projects/ROCKNIX/packages/wayland/lib/fcft/package.mk` | `fcft` | `3.1.9` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/wayland/lib/libdecor/package.mk` | `libdecor` | `0.2.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/lib/seatd/package.mk` | `seatd` | `0.9.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/lib/tllist/package.mk` | `tllist` | `1.1.0` | version | absent: orphan | - | CURRENT (latest `1.1.0`) | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.1.0; dependants resolve by name |
| `projects/ROCKNIX/packages/wayland/lib/wlroots/package.mk` | `wlroots` | `0.19.3` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's pin `132e31cfe19f` |
| `projects/ROCKNIX/packages/wayland/libinput/package.mk` | `libinput` | `1.26.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/libxkbcommon/package.mk` | `libxkbcommon` | `1.8.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/mtdev/package.mk` | `mtdev` | `1.1.6` | version | absent: orphan | - | UNKNOWN: no resolver for sources.buildroot.net, or it did not answer | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.1.7; dependants resolve by name |
| `projects/ROCKNIX/packages/wayland/util/bemenu/package.mk` | `bemenu` | `0.6.15` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/util/foot/package.mk` | `foot` | `1.19.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/wayland/util/swaybg/package.mk` | `swaybg` | `1.2.1` | version | absent: orphan | - | BEHIND (latest `1.2.2`) | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.2.2; dependants resolve by name |
| `projects/ROCKNIX/packages/wayland/util/swayimg/package.mk` | `swayimg` | `v2.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/util/wlr-randr/package.mk` | `wlr-randr` | `0.4.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/web/curl/package.mk` | `curl` | `8.21.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/app/xterm/package.mk` | `xterm` | `410` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libICE/package.mk` | `libICE` | `1.1.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libSM/package.mk` | `libSM` | `1.2.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXau/package.mk` | `libXau` | `1.0.12` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXaw/package.mk` | `libXaw` | `1.0.16` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXcursor/package.mk` | `libXcursor` | `1.2.3` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXdmcp/package.mk` | `libXdmcp` | `1.1.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXft/package.mk` | `libXft` | `2.3.9` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXinerama/package.mk` | `libXinerama` | `1.1.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXmu/package.mk` | `libXmu` | `1.3.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXpm/package.mk` | `libXpm` | `3.5.19` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXres/package.mk` | `libXres` | `1.2.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXt/package.mk` | `libXt` | `1.3.1` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXxf86vm/package.mk` | `libXxf86vm` | `1.1.7` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libfontenc/package.mk` | `libfontenc` | `1.1.9` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libxcb-cursor/package.mk` | `libxcb-cursor` | `7b0fa99aa130` | hash | identical | - | unknown: gitlab.freedesktop.org is not GitHub | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libxkbfile/package.mk` | `libxkbfile` | `1.2.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-image/package.mk` | `xcb-util-image` | `0.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-keysyms/package.mk` | `xcb-util-keysyms` | `0.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-renderutil/package.mk` | `xcb-util-renderutil` | `0.3.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-wm/package.mk` | `xcb-util-wm` | `0.4.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util/package.mk` | `xcb-util` | `0.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/xserver/xwayland/package.mk` | `xwayland` | `24.1.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/gamescope-glm/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  PKG_NAME="gamescope-glm"
    4  # The revision gamescope's own subprojects/glm.wrap names ([wrap-git],
    5  # revision below is the wrap's, byte for byte), carried as a source so the
    6  # build never clones it: gamescope's meson.build calls subproject('glm')
    7  # unconditionally, and scripts/build refuses meson's own download
    8  # (--wrap-mode=nodownload, the rule a build fetches no dependency of its own).
    9  # gamescope's recipe copies this tree to subprojects/glm before it configures
   10  # and lays the wrap's packagefiles (the meson.build glm lacks) over it. Source
   11  # only: nothing here is built or installed on its own.
   12  # freshness: pinned -- follows subprojects/glm.wrap at gamescope's pinned commit (bump both together)
   13  PKG_VERSION="0af55ccecd98d4e5a8d1fad7de25ba429d60e863"
   14  PKG_SHA256="e7f187d83523f505eb38dd25d297ea6c0d4ed856d733e808f18253f5a8fa88a0"
   15  PKG_LICENSE="MIT"
   16  PKG_SITE="https://github.com/g-truc/glm"
   17  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   18  PKG_SOURCE_NAME="glm-${PKG_VERSION}.tar.gz"
   19  PKG_DEPENDS_TARGET="toolchain"
   20  PKG_LONGDESC="OpenGL Mathematics at the revision gamescope's meson wrap pins, as a source for gamescope's subprojects."
   21  PKG_TOOLCHAIN="manual"
   22  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/gamescope-stb/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  PKG_NAME="gamescope-stb"
    4  # The revision gamescope's own subprojects/stb.wrap names ([wrap-git],
    5  # revision below is the wrap's, byte for byte), carried as a source so the
    6  # build never clones it: gamescope's meson.build calls subproject('stb')
    7  # unconditionally, and scripts/build refuses meson's own download
    8  # (--wrap-mode=nodownload). gamescope's recipe copies this tree to
    9  # subprojects/stb before it configures and lays the wrap's packagefiles (the
   10  # meson.build stb lacks) over it. Source only: nothing here is built or
   11  # installed on its own.
   12  # freshness: pinned -- follows subprojects/stb.wrap at gamescope's pinned commit (bump both together)
   13  PKG_VERSION="5736b15f7ea0ffb08dd38af21067c314d6a3aae9"
   14  PKG_SHA256="d00921d49b06af62aa6bfb97c1b136bec661dd11dd4eecbcb0da1f6da7cedb4c"
   15  PKG_LICENSE="MIT"
   16  PKG_SITE="https://github.com/nothings/stb"
   17  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   18  PKG_SOURCE_NAME="stb-${PKG_VERSION}.tar.gz"
   19  PKG_DEPENDS_TARGET="toolchain"
   20  PKG_LONGDESC="the stb single-file libraries at the revision gamescope's meson wrap pins, as a source for gamescope's subprojects."
   21  PKG_TOOLCHAIN="manual"
   22  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/gamescope/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="gamescope"
    5  PKG_VERSION="fa0b4d3342078f01eadff0193e09c3b561f40c03"
    6  PKG_GIT_CLONE_BRANCH="master"
    7  PKG_LICENSE="BSD-2-Clause"
    8  PKG_SITE="https://github.com/ValveSoftware/gamescope"
    9  PKG_URL="${PKG_SITE}.git"
   10  PKG_DEPENDS_TARGET="toolchain wayland wayland-protocols libdrm libinput libxkbcommon pixman systemd \
   11                      libcap luajit libdecor libX11 libXext libXfixes libXdamage libXcomposite \
   12                      libXrender libXxf86vm libXtst libXi libXcursor libXmu libXres libxcb \
   13                      xcb-util-wm seatd hwdata:host SDL2 pipewire gamescope-glm gamescope-stb"
   14  PKG_LONGDESC="SteamOS session compositing window manager (micro-compositor for games / nested Wayland)."
   15  PKG_TOOLCHAIN="meson"
   16  
   17  if [ "${VULKAN_SUPPORT}" = "yes" ]; then
   18    PKG_DEPENDS_TARGET+=" ${VULKAN}"
   19  fi
   20  
   21  PKG_MESON_OPTS_TARGET="-Ddrm_backend=enabled \
   22                         -Dpipewire=enabled \
   23                         -Denable_openvr_support=false \
   24                         -Davif_screenshots=disabled \
   25                         -Dbenchmark=disabled \
   26                         -Dinput_emulation=disabled \
   27                         -Drt_cap=enabled \
   28                         -Denable_tests=false \
   29                         -Dsdl2_backend=enabled"
   30  
   31  pre_configure_target() {
   32    # Subprojects (libliftoff tests, wlroots) use -Werror; distro GCC is stricter than upstream CI.
   33    # - libdrm_mock.c: unused-but-set-variable
   34    # - wlroots xwm.c: return-type (control reaches end of non-void function)
   35    export TARGET_CFLAGS="${TARGET_CFLAGS} -Wno-error=unused-variable -Wno-error=unused-but-set-variable -Wno-error=return-type"
   36    export TARGET_CXXFLAGS="${TARGET_CXXFLAGS} -Wno-error=unused-variable -Wno-error=unused-but-set-variable -Wno-error=return-type"
   37  
   38    # glm and stb: from the fork's source packages, never from a clone.
   39    # gamescope's meson.build calls subproject('glm') and subproject('stb')
   40    # unconditionally, and both wraps are [wrap-git] at a pinned revision that
   41    # meson would clone at configure; the build refuses that (scripts/build,
   42    # --wrap-mode=nodownload, fork #226). The two trees come in as sources
   43    # through gamescope-glm and gamescope-stb, pinned to the wraps' revisions
   44    # and hash-checked at download, and are put where each wrap's directory
   45    # says, with the wrap's packagefiles (the meson.build each needs) laid
   46    # over them, which meson does only for a tree it fetched itself. The wrap
   47    # and the package must agree, or the build stops here and says which to
   48    # bump. The other subprojects are git submodules the clone carries.
   49    local sub dir rev src
   50    for sub in glm stb; do
   51      dir=$(sed -n 's/^directory = //p' ${PKG_BUILD}/subprojects/${sub}.wrap)
   52      rev=$(sed -n 's/^revision = //p' ${PKG_BUILD}/subprojects/${sub}.wrap)
   53      src=$(get_build_dir gamescope-${sub})
   54      [ -n "${dir}" ] && [ -n "${rev}" ] || die "gamescope: subprojects/${sub}.wrap names no directory or revision"
   55      [ "${rev}" = "$(get_pkg_version gamescope-${sub})" ] || die "gamescope: subprojects/${sub}.wrap pins ${rev} and the gamescope-${sub} package carries $(get_pkg_version gamescope-${sub}) -- bump the package to the wrap's revision"
   56      [ -d "${src}" ] || die "gamescope: the gamescope-${sub} package's tree is not at ${src}"
   57      rm -rf ${PKG_BUILD}/subprojects/${dir}
   58      cp -a ${src} ${PKG_BUILD}/subprojects/${dir}
   59      if [ -d ${PKG_BUILD}/subprojects/packagefiles/${dir} ]; then
   60        cp -a ${PKG_BUILD}/subprojects/packagefiles/${dir}/. ${PKG_BUILD}/subprojects/${dir}/
   61      fi
   62    done
   63  }
   64  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/m8c/config/GENERIC_X64/config.ini

```
    1  [graphics]
    2  fullscreen=false
    3  use_gpu=true
    4  idle_ms=10
    5  wait_for_device=true
    6  wait_packets=1024
    7  [audio]
    8  audio_enabled=false
    9  audio_buffer_size=1024
   10  audio_device_name=Default
   11  [keyboard]
   12  ;Ref: https://wiki.libsdl.org/SDL2/SDL_Scancode
   13  key_up=82
   14  key_left=80
   15  key_down=81
   16  key_right=79
   17  key_select=225
   18  key_select_alt=29
   19  key_start=44
   20  key_start_alt=27
   21  key_opt=226
   22  key_opt_alt=4
   23  key_edit=224
   24  key_edit_alt=22
   25  key_delete=76
   26  key_reset=21
   27  key_jazz_inc_octave=85
   28  key_jazz_dec_octave=84
   29  key_jazz_inc_velocity=86
   30  key_jazz_dec_velocity=69
   31  key_toggle_audio=69
   32  [gamepad]
   33  gamepad_up=11
   34  gamepad_left=13
   35  gamepad_down=12
   36  gamepad_right=14
   37  gamepad_select=4 ; Select
   38  gamepad_start=6  ; Start
   39  gamepad_opt=0    ; B
   40  gamepad_edit=1   ; A
   41  gamepad_quit=5   ; Menu/Guide
   42  gamepad_reset=7  ; R2
   43  gamepad_analog_threshold=30000
   44  gamepad_analog_invert=false
   45  gamepad_analog_axis_updown=1
   46  gamepad_analog_axis_leftright=0
   47  gamepad_analog_axis_select=4
   48  gamepad_analog_axis_start=5
   49  gamepad_analog_axis_opt=-1
   50  gamepad_analog_axis_edit=-1
   51  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/mangohud-vulkan-headers/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="mangohud-vulkan-headers"
    5  # The release mangohud's own subprojects/vulkan-headers.wrap names (source_url,
    6  # source_filename and source_hash below are the wrap's, byte for byte), carried
    7  # as a source so the build never fetches it: mangohud's meson.build calls
    8  # subproject('vulkan-headers') unconditionally, and scripts/build refuses meson's
    9  # own download (--wrap-mode=nodownload, the rule a build fetches no dependency
   10  # of its own). mangohud's recipe copies this tarball into meson's
   11  # subprojects/packagecache before it configures; meson unpacks it from there
   12  # and applies the wrap's packagefiles. Source only: nothing here is built or
   13  # installed on its own.
   14  # freshness: pinned -- follows subprojects/vulkan-headers.wrap at mangohud's pinned commit (bump both together)
   15  PKG_VERSION="1.4.346"
   16  PKG_SHA256="5bb77f5d7b460e255a9e51affc00d64354986b55cf577d8eab28529cad01fc80"
   17  PKG_LICENSE="Apache-2.0"
   18  PKG_SITE="https://github.com/KhronosGroup/Vulkan-Headers"
   19  PKG_URL="${PKG_SITE}/archive/v${PKG_VERSION}.tar.gz"
   20  PKG_SOURCE_NAME="vulkan-headers-${PKG_VERSION}.tar.gz"
   21  PKG_DEPENDS_TARGET="toolchain"
   22  PKG_LONGDESC="the Vulkan headers at the release mangohud's meson wrap pins, as a source for mangohud's subproject cache."
   23  PKG_TOOLCHAIN="manual"
   24  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/mangohud-vulkan-utility-libraries/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="mangohud-vulkan-utility-libraries"
    5  # The release mangohud's own subprojects/vulkan-utility-libraries.wrap names (source_url,
    6  # source_filename and source_hash below are the wrap's, byte for byte), carried
    7  # as a source so the build never fetches it: mangohud's meson.build calls
    8  # subproject('vulkan-utility-libraries') unconditionally, and scripts/build refuses meson's
    9  # own download (--wrap-mode=nodownload, the rule a build fetches no dependency
   10  # of its own). mangohud's recipe copies this tarball into meson's
   11  # subprojects/packagecache before it configures; meson unpacks it from there
   12  # and applies the wrap's packagefiles. Source only: nothing here is built or
   13  # installed on its own.
   14  # freshness: pinned -- follows subprojects/vulkan-utility-libraries.wrap at mangohud's pinned commit (bump both together)
   15  PKG_VERSION="1.4.346"
   16  PKG_SHA256="372eb525103ecb4e3a04d030b2a9778ebc67853bbdc82ce6747de3757d432ad9"
   17  PKG_LICENSE="Apache-2.0"
   18  PKG_SITE="https://github.com/KhronosGroup/Vulkan-Utility-Libraries"
   19  PKG_URL="${PKG_SITE}/archive/v${PKG_VERSION}.tar.gz"
   20  PKG_SOURCE_NAME="vulkan-utility-libraries-${PKG_VERSION}.tar.gz"
   21  PKG_DEPENDS_TARGET="toolchain"
   22  PKG_LONGDESC="the Vulkan utility libraries at the release mangohud's meson wrap pins, as a source for mangohud's subproject cache."
   23  PKG_TOOLCHAIN="manual"
   24  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/apps/mangohud/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="mangohud"
    5  PKG_VERSION="992103e4fb744897826de04ea00a2f71e7018214" # v0.8.4
    6  PKG_SHA256="edd61f4716710681a9e3b535556831ee0c6187b7b6f90d29f8d8ac234448f4a5"
    7  PKG_LICENSE="GPL"
    8  PKG_SITE="https://github.com/flightlessmango/MangoHud"
    9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_TARGET="toolchain glslang mesa Python3 wayland libxcb dbus mangohud-vulkan-headers mangohud-vulkan-utility-libraries"
   11  PKG_LONGDESC="A Vulkan and OpenGL overlay for monitoring FPS, temperatures, CPU/GPU load and more."
   12  
   13  PKG_PATCH_DIRS+=" common"
   14  
   15  case ${DEVICE} in
   16    SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
   17      PKG_PATCH_DIRS+=" qualcomm"
   18    ;;
   19  esac
   20  
   21  [ "${BATTERYPLUS_SUPPORT}" = "yes" ] && PKG_PATCH_DIRS+=" batteryplus"
   22  
   23  PKG_PATCH_DIRS+=" ${DEVICE}"
   24  
   25  if [ "${OPENGL_SUPPORT}" = "yes" ]; then
   26    PKG_DEPENDS_TARGET+=" ${OPENGL}"
   27  fi
   28  
   29  if [ "${VULKAN_SUPPORT}" = "yes" ]
   30  then
   31    PKG_DEPENDS_TARGET+=" ${VULKAN}"
   32  fi
   33  
   34  pre_configure_target() {
   35    PKG_MESON_OPTS_TARGET+=" -Dwith_xnvctrl=disabled \
   36                             -Dwith_x11=enabled \
   37                             -Dmangoplot=disabled \
   38                             -Dwith_wayland=enabled \
   39                             -Dmangoapp=true \
   40                             -Dwith_fex=true"
   41  
   42    # Download Sub Modules
   43    mkdir -p ${PKG_BUILD}/subprojects/
   44  
   45    ### vulkan-headers and vulkan-utility-libraries: from meson's package cache,
   46    # never from the network. mangohud's meson.build calls subproject() for both
   47    # unconditionally, and its own wraps name the release each needs (1.4.346
   48    # at v0.8.4; the 1.3.283 tarball this hook used to fetch and unpack sat
   49    # unused beside them, since the wrap's directory named another). The build
   50    # refuses meson's download (scripts/build, --wrap-mode=nodownload), so the
   51    # two tarballs come in as sources through the mangohud-vulkan-headers and
   52    # mangohud-vulkan-utility-libraries packages, hash-checked at download, and
   53    # are copied under the file name the wrap expects; meson unpacks them from
   54    # there and applies the wrap's packagefiles. The wrap and the package must
   55    # agree, or the build stops here and says which to bump.
   56    mkdir -p ${PKG_BUILD}/subprojects/packagecache
   57    local wrap want have
   58    for wrap in vulkan-headers vulkan-utility-libraries; do
   59      want=$(sed -n 's/^source_filename = //p' ${PKG_BUILD}/subprojects/${wrap}.wrap)
   60      have=$(sed -n 's/^source_hash = //p' ${PKG_BUILD}/subprojects/${wrap}.wrap)
   61      [ -n "${want}" ] && [ -f "${SOURCES}/mangohud-${wrap}/${want}" ] || die "mangohud: subprojects/${wrap}.wrap wants '${want:-?}' and the mangohud-${wrap} package does not supply it -- bump that package to the wrap's version"
   62      [ "$(sha256sum "${SOURCES}/mangohud-${wrap}/${want}" | cut -d' ' -f1)" = "${have}" ] || die "mangohud: the mangohud-${wrap} tarball's hash is not the wrap's source_hash -- the package and the wrap disagree"
   63      cp "${SOURCES}/mangohud-${wrap}/${want}" ${PKG_BUILD}/subprojects/packagecache/${want}
   64    done
   65  
   66    ### imgui
   67    curl -Lo ${PKG_BUILD}/subprojects/imgui.tar.gz https://github.com/ocornut/imgui/archive/refs/tags/v1.91.6.tar.gz
   68    tar -xvf ${PKG_BUILD}/subprojects/imgui.tar.gz -C ${PKG_BUILD}/subprojects/
   69    #curl -Lo ${PKG_BUILD}/subprojects/imgui_patch_1.91.6-3.zip https://wrapdb.mesonbuild.com/v2/imgui_1.91.6-3/get_patch
   70    #unzip -o ${PKG_BUILD}/subprojects/imgui_patch_1.91.6-3.zip -d ${PKG_BUILD}/subprojects
   71    unzip -o ${PKG_DIR}/meson-patches/imgui_patch_1.91.6-3.zip -d ${PKG_BUILD}/subprojects
   72    rm -rf ${PKG_BUILD}/subprojects/imgui.tar.gz
   73    rm -rf ${PKG_BUILD}/subprojects/imgui_patch_1.91.6-3.zip
   74  
   75    ### implot
   76    curl -Lo ${PKG_BUILD}/subprojects/implot.zip https://github.com/epezent/implot/archive/refs/tags/v0.16.zip
   77    unzip -o ${PKG_BUILD}/subprojects/implot.zip -d ${PKG_BUILD}/subprojects
   78    #curl -Lo ${PKG_BUILD}/subprojects/implot_patch_0.16-1.zip https://wrapdb.mesonbuild.com/v2/implot_0.16-1/get_patch
   79    #unzip -o ${PKG_BUILD}/subprojects/implot_patch_0.16-1.zip -d ${PKG_BUILD}/subprojects
   80    unzip -o ${PKG_DIR}/meson-patches/implot_patch_0.16-1.zip -d ${PKG_BUILD}/subprojects
   81    rm -rf ${PKG_BUILD}/subprojects/implot.zip
   82    rm -rf ${PKG_BUILD}/subprojects/implot_patch_0.16-1.zip
   83  
   84    ### spdlog
   85    curl -Lo ${PKG_BUILD}/subprojects/spdlog.tar.gz https://github.com/gabime/spdlog/archive/refs/tags/v1.14.1.tar.gz
   86    tar -xvf ${PKG_BUILD}/subprojects/spdlog.tar.gz -C ${PKG_BUILD}/subprojects/
   87    #curl -Lo ${PKG_BUILD}/subprojects/spdlog_patch_1.14.1-1.zip https://wrapdb.mesonbuild.com/v2/spdlog_1.14.1-1/get_patch
   88    #unzip -o ${PKG_BUILD}/subprojects/spdlog_patch_1.14.1-1.zip -d ${PKG_BUILD}/subprojects
   89    unzip -o ${PKG_DIR}/meson-patches/spdlog_patch_1.14.1-1.zip -d ${PKG_BUILD}/subprojects
   90    rm -rf ${PKG_BUILD}/subprojects/spdlog.tar.gz
   91    rm -rf ${PKG_BUILD}/subprojects/spdlog_patch_1.14.1-1.zip
   92  }
   93  
   94  post_makeinstall_target() {
   95    mkdir -p ${INSTALL}/usr/bin
   96    cp -rf ${PKG_DIR}/sources/* ${INSTALL}/usr/bin
   97    chmod +x ${INSTALL}/usr/bin/*
   98  
   99    mkdir -p ${INSTALL}/usr/config/MangoHud
  100    cp -rf ${PKG_DIR}/config/* ${INSTALL}/usr/config/MangoHud
  101  
  102    # Customize config per platform, eg set font size for display resolution
  103    case ${DEVICE} in
  104      RK3326)
  105        sed -e "s/@FONT_SIZE@/30/g" -i ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  106      ;;
  107      S922X)
  108        # Compact, horizontal display with smaller font works well
  109        sed -e "s/@FONT_SIZE@/15/g" -i ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  110        sed -i 's/^\# hud_no_margin/\hud_no_margin/g' ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  111        sed -i 's/^\# hud_compact/\hud_compact/g' ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  112        sed -i 's/^\# horizontal/\horizontal/g' ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  113  
  114        # No GPU temperature sensor or battery life estimate available
  115        sed -i 's/^gpu_temp/\# gpu_temp/g' ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  116        sed -i 's/^battery_time/\# battery_time/g' ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  117      ;;
  118      SM8250)
  119        sed -e "s/@FONT_SIZE@/40/g" -i ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  120        
  121        # No battery life estimate available
  122        sed -i 's/^battery_time/\# battery_time/g' ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  123      ;;
  124      *)
  125        sed -e "s/@FONT_SIZE@/40/g" -i ${INSTALL}/usr/config/MangoHud/MangoHud.conf
  126      ;;
  127    esac
  128  }
  129  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/compat/box86/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    3  
    4  PKG_NAME="box86"
    5  PKG_VERSION="39d3ed203323000c11f47b780f7468fa24a7185d"
    6  PKG_SHA256="0b01cfe0c7e1af14f52d8ebcc36fe8b47ff2d8d6a06cb423f3e4069ac4466f56"
    7  PKG_LICENSE="MIT"
    8  PKG_SITE="https://github.com/ptitSeb/box86"
    9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_TARGET="toolchain ncurses SDL2 libXdmcp libXft libXcomposite cups libogg"
   11  PKG_LONGDESC="Box86 lets you run x86 Linux programs (such as games) on non-x86 Linux systems, like ARM."
   12  PKG_TOOLCHAIN="cmake"
   13  
   14  PKG_CMAKE_OPTS_TARGET="-DCMAKE_BUILD_TYPE=Release \
   15                         -DARM_DYNAREC=On \
   16                         -DCMAKE_C_FLAGS=\"-w\""
   17  
   18  case ${TARGET_ARCH} in
   19    aarch64)
   20      PKG_DEPENDS_TARGET=""
   21      unpack() {
   22        true
   23      }
   24      configure_target() {
   25        true
   26      }
   27      make_target() {
   28        true
   29      }
   30      ;;
   31  esac
   32  
   33  case ${DEVICE} in
   34    RK3588)
   35      PKG_CMAKE_OPTS_TARGET+=" -DRK3588=On"
   36      ;;
   37    SM4450)
   38      PKG_CMAKE_OPTS_TARGET+=" -DSD888=On"
   39      ;;
   40    SM8250)
   41      PKG_CMAKE_OPTS_TARGET+=" -DSD865=On"
   42      ;;
   43    SM8550)
   44      PKG_CMAKE_OPTS_TARGET+=" -DSD8G2=On"
   45      ;;
   46    RK3399)
   47      PKG_CMAKE_OPTS_TARGET+=" -DRK3399=On"
   48      ;;
   49    RK3326)
   50      PKG_CMAKE_OPTS_TARGET+=" -DGOA_CLONE=On"
   51      ;;
   52    S922X|SM6115)
   53      PKG_CMAKE_OPTS_TARGET+=" -DODROIDN2=On"
   54      ;;
   55  esac
   56  
   57  makeinstall_target() {
   58    case ${TARGET_ARCH} in
   59      arm)
   60        mkdir -p ${INSTALL}/usr/share/box86/lib
   61          cp ${PKG_BUILD}/x86lib/* ${INSTALL}/usr/share/box86/lib
   62  
   63        mkdir -p ${INSTALL}/usr/bin
   64          cp ${PKG_BUILD}/.${TARGET_NAME}/box86 ${INSTALL}/usr/bin/
   65          cp ${PKG_BUILD}/tests/bash ${INSTALL}/usr/bin/bash-x86
   66  
   67        mkdir -p ${INSTALL}/etc/binfmt.d
   68        cp ${PKG_BUILD}/.${TARGET_NAME}/system/box86.conf ${INSTALL}/etc/binfmt.d
   69        ;;
   70      aarch64)
   71        mkdir -p ${INSTALL}/usr/share/box86/lib
   72          cp -vP ${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/${PKG_NAME}-*/usr/share/box86/lib/* ${INSTALL}/usr/share/box86/lib
   73  
   74        mkdir -p ${INSTALL}/usr/bin
   75          cp -vP ${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/${PKG_NAME}-*/usr/bin/* ${INSTALL}/usr/bin
   76  
   77        mkdir -p ${INSTALL}/usr/config
   78          cp -vP ${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/${PKG_NAME}-*/usr/config/box86.box86rc ${INSTALL}/usr/config/box86.box86rc
   79  
   80        mkdir -p ${INSTALL}/etc/binfmt.d
   81          cp -vP ${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/${PKG_NAME}-*/etc/binfmt.d/box86.conf ${INSTALL}/etc/binfmt.d
   82        ;;
   83    esac
   84  
   85    mkdir -p ${INSTALL}/usr/config
   86      cp ${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/build/${PKG_NAME}-*/system/box86.box86rc ${INSTALL}/usr/config/box86.box86rc
   87  
   88    mkdir -p ${INSTALL}/etc
   89      ln -sf /storage/.config/box86.box86rc ${INSTALL}/etc/box86.box86rc
   90  }
   91  
   92  if [ ! "${ENABLE_32BIT}" == "true" ]; then
   93    makeinstall_target() {
   94      true
   95    }
   96  fi
   97  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/compat/lib32/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2021-present 351ELEC (https://github.com/351ELEC)
    3  
    4  PKG_NAME="lib32"
    5  PKG_VERSION="1.0"
    6  PKG_ARCH="aarch64"
    7  PKG_LICENSE="GPLv2"
    8  PKG_DEPENDS_TARGET="toolchain retroarch SDL2 libsndfile libmodplug"
    9  PKG_LONGDESC="ARM 32bit bundle for aarch64"
   10  PKG_TOOLCHAIN="manual"
   11  PKG_BUILD_FLAGS="-strip"
   12  
   13  makeinstall_target() {
   14    case ${TARGET_ARCH} in
   15      aarch64)
   16        LIBARCH="arm"
   17        LDSO="ld-linux-armhf.so.3"
   18        ;;
   19    esac
   20  
   21    cd ${PKG_BUILD}
   22    LIBROOT="${ROOT}/build.${DISTRONAME}-${DEVICE}.${LIBARCH}/image/system/"
   23    mkdir -p ${INSTALL}/usr/lib32
   24    rsync -al ${LIBROOT}/usr/lib/* ${INSTALL}/usr/lib32 >/dev/null 2>&1
   25    rsync -al ${LIBROOT}/usr/lib32/* ${INSTALL}/usr/lib32 >/dev/null 2>&1
   26    mkdir -p ${INSTALL}/usr/lib
   27    ln -s /usr/lib32/${LDSO} ${INSTALL}/usr/lib/${LDSO}
   28  
   29    mkdir -p "${INSTALL}/etc/ld.so.conf.d"
   30    echo "/usr/lib32" > "${INSTALL}/etc/ld.so.conf.d/${LIBARCH}-lib32.conf"
   31  
   32    if [ -d "${LIBROOT}/usr/share/vulkan/icd.d" ]; then
   33      mkdir -p ${INSTALL}/usr/share/vulkan/icd.d
   34      for json in ${LIBROOT}/usr/share/vulkan/icd.d/*.json; do
   35        [ -f "${json}" ] || continue
   36        grep -q '"library_path"[^"]*"[^"]*/' "${json}" || continue
   37        sed -e 's#"/usr/lib/#"/usr/lib32/#g' -e 's#"library_arch": *"64"#"library_arch": "32"#' \
   38          "${json}" > "${INSTALL}/usr/share/vulkan/icd.d/$(basename "${json}" .json).lib32.json"
   39      done
   40    fi
   41  
   42    mkdir -p ${INSTALL}/usr/bin
   43    cp ${LIBROOT}/usr/bin/ldd ${INSTALL}/usr/bin/ldd32
   44  }
   45  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/graphics/cairo/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
    4  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    5  
    6  PKG_NAME="cairo"
    7  # Why this override exists beside packages/graphics/cairo: the generic recipe
    8  # builds cairo for x11 alone (libXrender/libX11 under DISPLAYSERVER=x11, xcb
    9  # disabled); ROCKNIX's Wayland devices need the xcb and xlib-xcb surfaces,
   10  # and the meson options below turn those on. (cairo 1.18 has no GL or GLES
   11  # backend: the OPENGL/OPENGLES dependencies in configure_package order the
   12  # build and select nothing.) The version is the release the generic
   13  # recipe would have too -- 1.18.4 is what pango 1.58 requires (1e5b87963a;
   14  # upstream PR 3359 carries the same bump) -- so once that PR merges the
   15  # version line here is redundant and only the options keep the override.
   16  PKG_VERSION="1.18.4"
   17  PKG_SHA256="445ed8208a6e4823de1226a74ca319d3600e83f6369f99b14265006599c32ccb"
   18  PKG_LICENSE="LGPL-2.1-or-later OR MPL-1.1"
   19  PKG_SITE="https://cairographics.org/"
   20  PKG_URL="https://cairographics.org/releases/${PKG_NAME}-${PKG_VERSION}.tar.xz"
   21  PKG_DEPENDS_TARGET="toolchain zlib freetype fontconfig glib libpng pixman"
   22  PKG_LONGDESC="Cairo is a vector graphics library with cross-device output support."
   23  
   24  configure_package() {
   25    if [ "${OPENGL}" != "no" ]; then
   26      PKG_DEPENDS_TARGET+=" ${OPENGL}"
   27    fi
   28  
   29    if [ "${OPENGLES}" != "no" ]; then
   30      PKG_DEPENDS_TARGET+=" ${OPENGLES}"
   31    fi
   32  
   33    case ${DISPLAYSERVER} in
   34      "x11"|"wl")
   35        PKG_DEPENDS_TARGET+=" libxcb libXrender libX11 mesa"
   36      ;;
   37    esac
   38  
   39  }
   40  
   41  pre_configure_target() {
   42    PKG_MESON_OPTS_TARGET="-Ddwrite=disabled \
   43                           -Dfontconfig=enabled \
   44                           -Dfreetype=enabled \
   45                           -Dpng=enabled \
   46                           -Dquartz=disabled \
   47                           -Dtee=disabled \
   48                           -Dtests=disabled \
   49                           -Dzlib=enabled \
   50                           -Dgtk2-utils=disabled \
   51                           -Dglib=enabled \
   52                           -Dspectre=disabled \
   53                           -Dsymbol-lookup=disabled \
   54                           -Dgtk_doc=false"
   55  
   56    case ${DISPLAYSERVER} in
   57      "x11"|"wl")
   58        PKG_MESON_OPTS_TARGET+=" -Dxlib=enabled \
   59                                 -Dxcb=enabled \
   60                                 -Dxlib-xcb=enabled"
   61      ;;
   62      *)
   63        PKG_MESON_OPTS_TARGET+=" -Dxlib=disabled \
   64                                 -Dxcb=disabled \
   65                                 -Dxlib-xcb=disabled"
   66      ;;
   67    esac
   68    # ipc_rmid_deferred_release comes from the meson cross file
   69    # (create_meson_conf_target in config/functions sets it to true).
   70  }
   71  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/graphics/glslang/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2021-present Frank Hartung (supervisedthinking (@) gmail.com)
    3  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
    4  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    5  
    6  PKG_NAME="glslang"
    7  # The SPIRV-Tools & SPIRV-Headers pkg_version/s need to match the compatible (known_good) glslang pkg_version.
    8  # https://raw.githubusercontent.com/KhronosGroup/glslang/${PKG_VERSION}/known_good.json
    9  # When updating glslang pkg_version please update to the known_good spirv-tools & spirv-headers pkg_version/s.
   10  PKG_VERSION="16.6.0"
   11  PKG_SHA256="9c09b901149c729df745057dafa815278aaa101b84d2b6e14f16a42de52f97f2"
   12  PKG_LICENSE="BSD-3-Clause AND BSD-2-Clause AND MIT AND Apache-2.0"
   13  PKG_SITE="https://github.com/KhronosGroup/glslang"
   14  PKG_URL="https://github.com/KhronosGroup/glslang/archive/${PKG_VERSION}.tar.gz"
   15  PKG_DEPENDS_HOST="toolchain:host Python3:host"
   16  PKG_DEPENDS_TARGET="toolchain Python3"
   17  PKG_LONGDESC="Khronos-reference front end for GLSL/ESSL, partial front end for HLSL, and a SPIR-V generator."
   18  PKG_DEPENDS_UNPACK="spirv-headers spirv-tools"
   19  
   20  PKG_CMAKE_OPTS_COMMON="-DBUILD_EXTERNAL=ON \
   21                         -DENABLE_GLSLANG_JS=OFF \
   22                         -DENABLE_RTTI=OFF \
   23                         -DENABLE_EXCEPTIONS=OFF \
   24                         -DENABLE_OPT=ON \
   25                         -DENABLE_PCH=ON \
   26                         -DGLSLANG_TESTS=OFF \
   27                         -Wno-dev"
   28  
   29  post_unpack() {
   30    # Enables SPIR-V optimzer capability needed for ENABLE_OPT CMake build option
   31    mkdir -p ${PKG_BUILD}/External/spirv-tools
   32      tar --strip-components=1 \
   33        -xf "${SOURCES}/spirv-tools/spirv-tools-$(get_pkg_version spirv-tools).tar.gz" \
   34        -C "${PKG_BUILD}/External/spirv-tools"
   35    mkdir -p ${PKG_BUILD}/External/spirv-tools/external/spirv-headers
   36      tar --strip-components=1 \
   37        -xf "${SOURCES}/spirv-headers/spirv-headers-$(get_pkg_version spirv-headers).tar.gz" \
   38        -C "${PKG_BUILD}/External/spirv-tools/external/spirv-headers"
   39  }
   40  
   41  pre_configure_host() {
   42    PKG_CMAKE_OPTS_HOST+="${PKG_CMAKE_OPTS_COMMON} \
   43                          -DBUILD_SHARED_LIBS=OFF"
   44  
   45  }
   46  
   47  pre_configure_target() {
   48    PKG_CMAKE_OPTS_TARGET+="${PKG_CMAKE_OPTS_COMMON} \
   49                            -DBUILD_SHARED_LIBS=ON \
   50                            -DENABLE_GLSLANG_BINARIES=OFF"
   51  }
   52  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/graphics/harfbuzz-icu/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  . ${ROOT}/packages/addons/addon-depends/chrome-depends/harfbuzz-icu/package.mk
    5  
    6  # The chrome-depends recipe builds this for an addon, so it carries
    7  # PKG_BUILD_FLAGS="-sysroot" and installs nowhere anything can link against.
    8  # WebKit calls hb_icu_script_to_script() directly, so it needs the real
    9  # library in the sysroot -- the build otherwise fails at configure with
   10  # "The following HarfBuzz libraries were not found: ICU", which reads like
   11  # harfbuzz is missing when in fact it was built and then withheld.
   12  unset PKG_BUILD_FLAGS
   13  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/graphics/spirv-tools/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2021-present Frank Hartung (supervisedthinking (@) gmail.com)
    3  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
    4  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    5  
    6  PKG_NAME="spirv-tools"
    7  # The SPIRV-Tools pkg_version needs to match the compatible (known_good) glslang pkg_version.
    8  # https://raw.githubusercontent.com/KhronosGroup/glslang/${PKG_VERSION}/known_good.json
    9  # When updating glslang pkg_version please update to the known_good spirv-tools pkg_version.
   10  # freshness: pinned -- follows glslang16.6.0 known_good.json; SPIRV-Tools DEPS names the same headers (#386)
   11  PKG_VERSION="ef96ed763b43b59b33b31b362f09a02b729fa1c9"
   12  PKG_SHA256="82c62146083fd558735a3171cf97cfc47903ca7d368482e87f94bd44883c0f00"
   13  PKG_LICENSE="Apache-2.0"
   14  PKG_SITE="https://github.com/KhronosGroup/SPIRV-Tools"
   15  PKG_URL="https://github.com/KhronosGroup/SPIRV-Tools/archive/${PKG_VERSION}.tar.gz"
   16  PKG_DEPENDS_HOST="toolchain:host"
   17  PKG_DEPENDS_TARGET="toolchain"
   18  PKG_DEPENDS_UNPACK="spirv-headers"
   19  PKG_LONGDESC="The SPIR-V Tools project provides an API and commands for processing SPIR-V modules."
   20  
   21  PKG_CMAKE_OPTS_HOST="-DSPIRV_SKIP_TESTS=ON"
   22  PKG_CMAKE_OPTS_TARGET="-DSPIRV_SKIP_TESTS=ON \
   23                         -DSPIRV_SKIP_EXECUTABLES=ON \
   24                         -DBUILD_SHARED_LIBS=ON"
   25  
   26  pre_configure_host() {
   27    # The pinned build container uses GCC 12, outside upstream's GCC 15 floor.
   28    # Its optimized vector diagnostic is a false positive (#495): keep it
   29    # visible without making it fatal. Other warnings and target flags stay on.
   30    # https://github.com/KhronosGroup/SPIRV-Tools/issues/6919
   31    case "$(${CXX} -dumpversion)" in
   32      12|12.*) CXXFLAGS+=" -Wno-error=free-nonheap-object" ;;
   33    esac
   34  }
   35  
   36  post_unpack() {
   37    mkdir -p ${PKG_BUILD}/external/spirv-headers
   38      tar --strip-components=1 \
   39        -xf "${SOURCES}/spirv-headers/spirv-headers-$(get_pkg_version spirv-headers).tar.gz" \
   40        -C "${PKG_BUILD}/external/spirv-headers"
   41  }
   42  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/initramfs/config/initramfs.x86_64.conf

```
    1  # x86_64 glibc hardcodes the ELF interpreter path /lib64/ld-linux-x86-64.so.2.
    2  # The base initramfs.conf only provides /lib, /bin and /sbin usrmerge symlinks
    3  # (enough for aarch64, whose loader lives at /lib/ld-linux-aarch64.so.1), so
    4  # without /lib64 the kernel cannot exec the dynamically-linked /init (busybox)
    5  # and panics with "Failed to execute /init (error -2)". Provide the symlink.
    6  slink lib64 usr/lib 0777 0 0
    7  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/lang/gcc/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  . ${ROOT}/packages/lang/gcc/package.mk
    5  
    6  PKG_VERSION="15.2.0"
    7  PKG_SHA256="438fd996826b0c82485a29da03a72d71d6e3541a83ec702df4271f6fe025d24e"
    8  PKG_URL="https://ftpmirror.gnu.org/gcc/${PKG_NAME}-${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}.tar.xz"
    9  
   10  case ${TARGET_ARCH} in
   11    arm|aarch64|x86_64)
   12      OPTS_LIBATOMIC="--enable-libatomic"
   13      ;;
   14    *)
   15      OPTS_LIBATOMIC="--disable-libatomic"
   16      ;;
   17  esac
   18  
   19  GCC_COMMON_CONFIGURE_OPTS="--target=${TARGET_NAME} \
   20                             --with-sysroot=${SYSROOT_PREFIX} \
   21                             --with-gmp=${TOOLCHAIN} \
   22                             --with-mpfr=${TOOLCHAIN} \
   23                             --with-mpc=${TOOLCHAIN} \
   24                             --with-zstd=${TOOLCHAIN} \
   25                             --with-gnu-as \
   26                             --with-gnu-ld \
   27                             --enable-plugin \
   28                             --enable-lto \
   29                             --enable-gold \
   30                             --enable-ld=default \
   31                             --with-linker-hash-style=gnu \
   32                             --disable-multilib \
   33                             --disable-nls \
   34                             --enable-checking=release \
   35                             --without-ppl \
   36                             --without-cloog \
   37                             --disable-libada \
   38                             --disable-libmudflap \
   39                             --disable-libitm \
   40                             --disable-libquadmath \
   41                             --enable-libgomp \
   42                             --disable-libmpx \
   43                             --disable-libssp \
   44                             --disable-static \
   45                             --enable-shared \
   46                             --disable-werror \
   47                             --enable-__cxa_atexit"
   48  
   49  PKG_CONFIGURE_OPTS_BOOTSTRAP="${GCC_COMMON_CONFIGURE_OPTS} \
   50                                --enable-cloog-backend=isl \
   51                                --disable-decimal-float \
   52                                --disable-gcov \
   53                                --enable-languages=c \
   54                                --disable-libatomic \
   55                                --disable-libgomp \
   56                                --disable-libsanitizer \
   57                                --disable-shared \
   58                                --disable-threads \
   59                                --without-headers \
   60                                --with-newlib \
   61                                ${TARGET_ARCH_GCC_OPTS}"
   62  
   63  PKG_CONFIGURE_OPTS_HOST="${GCC_COMMON_CONFIGURE_OPTS} \
   64                           --enable-languages=c,c++ \
   65                           ${OPTS_LIBATOMIC} \
   66                           --enable-decimal-float \
   67                           --enable-tls \
   68                           --enable-shared \
   69                           --disable-static \
   70                           --enable-long-long \
   71                           --enable-threads=posix \
   72                           --disable-libstdcxx-pch \
   73                           --enable-libstdcxx-time \
   74                           --enable-clocale=gnu \
   75                           ${TARGET_ARCH_GCC_OPTS}"
   76  
   77  makeinstall_target() {
   78    mkdir -p ${INSTALL}/usr/lib
   79      cp -P ${PKG_BUILD}/.${HOST_NAME}/${TARGET_NAME}/libgcc/libgcc_s.so* ${INSTALL}/usr/lib
   80      cp -P ${PKG_BUILD}/.${HOST_NAME}/${TARGET_NAME}/libstdc++-v3/src/.libs/libstdc++.so* ${INSTALL}/usr/lib
   81      cp -P ${PKG_BUILD}/.${HOST_NAME}/${TARGET_NAME}/libgomp/.libs/*.so* ${INSTALL}/usr/lib
   82      cp -P ${PKG_BUILD}/.${HOST_NAME}/${TARGET_NAME}/libsanitizer/asan/.libs/*.so* ${INSTALL}/usr/lib
   83      cp -P ${PKG_BUILD}/.${HOST_NAME}/${TARGET_NAME}/libsanitizer/ubsan/.libs/*.so* ${INSTALL}/usr/lib
   84      if [ "${OPTS_LIBATOMIC}" = "--enable-libatomic" ]; then
   85        cp -P ${PKG_BUILD}/.${HOST_NAME}/${TARGET_NAME}/libatomic/.libs/libatomic.so* ${INSTALL}/usr/lib
   86      fi
   87  }
   88  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml

```
    1  <?xml version="1.0"?>
    2  <gameList>
    3      <game>
    4          <path>./commander.sh</path>
    5          <name>File Manager</name>
    6          <desc>Browse files on your device and copy files to or from external drives.</desc>
    7          <developer>Tardigrade and ROCKNIX</developer>
    8          <publisher>ROCKNIX</publisher>
    9          <rating>5.0</rating>
   10          <releasedate>2022</releasedate>
   11          <genre>Tool</genre>
   12          <players>1</players>
   13          <image>./images/file-manager.svg</image>
   14      </game>
   15      <game>
   16          <path>./Start M8C.sh</path>
   17          <name>M8C</name>
   18          <desc>Cross-platform M8 tracker headless client.</desc>
   19          <developer>ROCKNIX</developer>
   20          <publisher>ROCKNIX</publisher>
   21          <rating>5.0</rating>
   22          <releasedate>2022</releasedate>
   23          <genre>Tool</genre>
   24          <players>1</players>
   25          <image>./images/m8c.svg</image>
   26      </game>
   27      <game>
   28          <path>./Start FEXConfig.sh</path>
   29          <name>FEXConfig</name>
   30          <desc>FEX: Emulate x86 Programs on ARM64.</desc>
   31          <developer>FEX-Emu</developer>
   32          <publisher>FEX-Emu</publisher>
   33          <rating>5.0</rating>
   34          <releasedate>2026</releasedate>
   35          <genre>Tool</genre>
   36          <players>1</players>
   37          <image>./images/fexemu.svg</image>
   38      </game>
   39      <game>
   40          <path>./Install ROCKNIX.sh</path>
   41          <name>Install pixelelated</name>
   42          <desc>Install pixelelated to your device's local storage. This erases all data on the drive you select.</desc>
   43          <developer>ROCKNIX</developer>
   44          <publisher>ROCKNIX</publisher>
   45          <rating>5.0</rating>
   46          <releasedate>2022</releasedate>
   47          <genre>Tool</genre>
   48          <players>1</players>
   49          <image>./images/install-rocknix.svg</image>
   50      </game>
   51      <game>
   52          <path>./Start PortMaster.sh</path>
   53          <name>PortMaster</name>
   54          <desc>Download game ports for pixelelated and other supported devices. Learn more at portmaster.games.</desc>
   55          <developer>Portmaster</developer>
   56          <publisher>Portmaster</publisher>
   57          <rating>5.0</rating>
   58          <releasedate>2022</releasedate>         
   59          <genre>Tool</genre>
   60          <players>1</players>
   61          <image>./images/portmaster.svg</image>
   62      </game>
   63      <game>
   64          <path>./cloud_backup.sh</path>
   65          <name>RCLONE Backup</name>
   66          <desc>Back up saves to your cloud storage. Set up your cloud account in Game Settings &gt; Cloud Settings first.</desc>
   67          <developer>ROCKNIX</developer>
   68          <publisher>ROCKNIX</publisher>
   69          <rating>5.0</rating>
   70          <releasedate>2024</releasedate>
   71          <genre>Script</genre>
   72          <players>1</players>
   73          <image>./images/rclone-backup.svg</image>
   74      </game>
   75      <game>
   76          <path>./cloud_restore.sh</path>
   77          <name>RCLONE Restore</name>
   78          <desc>Restore saves from your cloud storage. Set up your cloud account in Game Settings &gt; Cloud Settings first.</desc>
   79          <developer>ROCKNIX</developer>
   80          <publisher>ROCKNIX</publisher>
   81          <rating>5.0</rating>
   82          <releasedate>2024</releasedate>
   83          <genre>Script</genre>
   84          <players>1</players>
   85          <image>./images/rclone-restore.svg</image>
   86      </game>
   87      <game>
   88          <path>./Remove ._ Files.sh</path>
   89          <name>Remove ._ Files</name>
   90          <desc>This tool will remove hidden ._ files created by the MacOS filesystem</desc>
   91          <developer>ROCKNIX</developer>
   92          <publisher>ROCKNIX</publisher>
   93          <rating>5.0</rating>
   94          <releasedate>2021</releasedate>
   95          <genre>Script</genre>
   96          <players>1</players>
   97          <image>./images/remove-mac-files.svg</image>
   98      </game>
   99      <game>
  100          <path>./qterminal.sh</path>
  101          <name>QTerminal</name>
  102          <desc>QTerminal is a lightweight Qt terminal emulator. USB keyboard required.</desc>
  103          <developer>LXQT</developer>
  104          <publisher>LXQTX</publisher>
  105          <rating>5.0</rating>
  106          <releasedate>2025</releasedate>
  107          <genre>Tool</genre>
  108          <players>1</players>
  109          <image>./images/qterminal.svg</image>
  110      </game>
  111      <game>
  112          <path>./Install Steam.sh</path>
  113          <name>Install Steam</name>
  114          <desc>This tool is to install/update Steam.</desc>
  115          <developer>Valve</developer>
  116          <publisher>Valve</publisher>
  117          <rating>5.0</rating>
  118          <releasedate>2026</releasedate>
  119          <genre>Tool</genre>
  120          <players>1</players>
  121          <image>./images/steam.svg</image>
  122      </game>
  123      <game>
  124          <path>./Uninstall Steam.sh</path>
  125          <name>Uninstall Steam</name>
  126          <desc>Removes the Steam client and runtime. Keeps installed games (steamapps), saves (userdata), and depot download cache.</desc>
  127          <developer>ROCKNIX</developer>
  128          <publisher>ROCKNIX</publisher>
  129          <rating>5.0</rating>
  130          <releasedate>2026</releasedate>
  131          <genre>Tool</genre>
  132          <players>1</players>
  133          <image>./images/steam.svg</image>
  134      </game>
  135      <game>
  136          <path>./Install Heroic Games Launcher.sh</path>
  137          <name>Install Heroic</name>
  138          <desc>Downloads and installs the Heroic Games Launcher. Launch Heroic from the EmulationStation Heroic section after installing.</desc>
  139          <developer>Heroic Games Launcher</developer>
  140          <publisher>Heroic Games Launcher</publisher>
  141          <rating>5.0</rating>
  142          <releasedate>2026</releasedate>
  143          <genre>Tool</genre>
  144          <players>1</players>
  145          <image>./images/heroic.svg</image>
  146      </game>
  147      <game>
  148          <path>./Uninstall Heroic Games Launcher.sh</path>
  149          <name>Uninstall Heroic</name>
  150          <desc>Removes the Heroic app install. Keeps Heroic config under /storage/.config/heroic and per-game scripts in roms (delete manually if desired).</desc>
  151          <developer>ROCKNIX</developer>
  152          <publisher>ROCKNIX</publisher>
  153          <rating>5.0</rating>
  154          <releasedate>2026</releasedate>
  155          <genre>Tool</genre>
  156          <players>1</players>
  157          <image>./images/heroic.svg</image>
  158      </game>
  159      <game>
  160          <path>./Scan Heroic Games.sh</path>
  161          <name>Scan Heroic Games</name>
  162          <desc>Creates launchers for installed Heroic games in the Heroic EmulationStation section.</desc>
  163          <developer>ROCKNIX</developer>
  164          <publisher>ROCKNIX</publisher>
  165          <rating>5.0</rating>
  166          <releasedate>2026</releasedate>
  167          <genre>Script</genre>
  168          <players>1</players>
  169          <image>./images/heroic.svg</image>
  170      </game>
  171      <game>
  172          <path>./Start AetherSX2.sh</path>
  173          <name>Start AetherSX2</name>
  174          <desc>Opens the AetherSX2 GUI (PS2) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse 
  175  and keyboard to modify settings.</desc>
  176          <developer>ROCKNIX</developer>
  177          <publisher>ROCKNIX</publisher>
  178          <rating>5.0</rating>
  179          <releasedate>2021</releasedate>
  180          <genre>Emulator</genre>
  181          <players>1</players>
  182          <image>./images/aethersx2.svg</image>
  183      </game>
  184      <game>
  185          <path>./Start Azahar.sh</path>
  186          <name>Start Azahar</name>
  187          <desc>Opens the Azahar GUI (3DS) to enable global configuration changes to be made directly to the emulator. Although mouse control is enabled via gptokeyb, 
  188  it's recommended to have a mouse and keyboard to modify settings.</desc>
  189          <developer>ROCKNIX</developer>
  190          <publisher>ROCKNIX</publisher>
  191          <rating>5.0</rating>
  192          <releasedate>2026</releasedate>
  193          <genre>Emulator</genre>
  194          <players>1</players>
  195          <image>./images/azahar.svg</image>
  196      </game>
  197      <game>
  198          <path>./Start BigPEmu.sh</path>
  199          <name>Start BigPEmu</name>
  200          <desc>Opens the BigPEmu GUI (Jaguar) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard to modify settings.</desc>
  201          <developer>ROCKNIX</developer>
  202          <publisher>ROCKNIX</publisher>
  203          <rating>5.0</rating>
  204          <releasedate>2025</releasedate>
  205          <genre>Emulator</genre>
  206          <players>1</players>
  207          <image>./images/bigpemu.svg</image>
  208      </game>
  209      <game>
  210          <path>./Start CEMU.sh</path>
  211          <name>Start Cemu</name>
  212          <desc>Opens the Cemu GUI (WiiU) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings.</desc>
  213          <developer>ROCKNIX</developer>
  214          <publisher>ROCKNIX</publisher>
  215          <rating>5.0</rating>
  216          <releasedate>2023</releasedate>
  217          <genre>Emulator</genre>
  218          <players>1</players>
  219          <image>./images/cemu.svg</image>
  220      </game>
  221      <game>
  222          <path>./Start DaedalusX64.sh</path>
  223          <name>Start DaedalusX64</name>
  224          <desc>Opens the DaedalusX64 GUI (N64) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings.</desc>
  225          <developer>ROCKNIX</developer>
  226          <publisher>ROCKNIX</publisher>
  227          <rating>5.0</rating>
  228          <releasedate>2024</releasedate>
  229          <genre>Emulator</genre>
  230          <players>1</players>
  231          <image>./images/daedalusx64.svg</image>
  232      </game>
  233      <game>
  234          <path>./Start Dolphin.sh</path>
  235          <name>Start Dolphin</name>
  236          <desc>Opens the Dolphin GUI (Gamecube / Wii) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings.</desc>
  237          <developer>ROCKNIX</developer>
  238          <publisher>ROCKNIX</publisher>
  239          <rating>5.0</rating>
  240          <releasedate>2024</releasedate>
  241          <genre>Emulator</genre>
  242          <players>1</players>
  243          <image>./images/dolphin.svg</image>
  244      </game>
  245      <game>
  246          <path>./Start Duckstation.sh</path>
  247          <name>Start Duckstation</name>
  248          <desc>Opens the Duckstation GUI (PS1) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard to modify settings.</desc>
  249          <developer>ROCKNIX</developer>
  250          <publisher>ROCKNIX</publisher>
  251          <rating>5.0</rating>
  252          <releasedate>2024</releasedate>
  253          <genre>Emulator</genre>
  254          <players>1</players>
  255          <image>./images/duckstation.svg</image>
  256      </game>
  257      <game>
  258          <path>./Start Flycast.sh</path>
  259          <name>Start Flycast</name>
  260          <desc>Opens the Flycast GUI (Dreamcast / Naomi / Atomiswave) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard to modify settings.</desc>
  261          <developer>ROCKNIX</developer>
  262          <publisher>ROCKNIX</publisher>
  263          <rating>5.0</rating>
  264          <releasedate>2025</releasedate>
  265          <genre>Emulator</genre>
  266          <players>1</players>
  267          <image>./images/flycast.svg</image>
  268      </game>
  269      <game>
  270          <path>./Start HATARISA.sh</path>
  271          <name>Start Hatari</name>
  272          <desc>Opens the Hatari GUI to enable global configuration changes to be made directly. Hatari is an Atari ST/STE/TT/Falcon emulator for GNU/Linux, BSD, Mac OS X, Windows and other systems which are supported by the SDL library. The Atari ST was a 16/32 bit computer system which was first released by Atari in 1985. Using the Motorola 68000 CPU, it was a very popular computer having quite a lot of CPU power at that time. Unlike many other Atari ST emulators which try to give you a good environment for running GEM applications, Hatari tries to emulate the hardware of a ST as close as possible so that it is able to run most of the old ST games and demos. Hatari is open source software and is distributed under the terms of the GNU General Public License (GPL).</desc>
  273          <developer>ROCKNIX</developer>
  274          <publisher>ROCKNIX</publisher>
  275          <rating>5.0</rating>
  276          <releasedate>2023</releasedate>
  277          <genre>Emulator</genre>
  278          <players>1</players>
  279          <image>./images/hatari.svg</image>
  280      </game>
  281      <game>
  282          <path>./Start MelonDS.sh</path>
  283          <name>Start MelonDS</name>
  284          <desc>Opens the MelonDS GUI (Nintendo DS) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard to modify settings.</desc>
  285          <developer>ROCKNIX</developer>
  286          <publisher>ROCKNIX</publisher>
  287          <rating>5.0</rating>
  288          <releasedate>2024</releasedate>
  289          <genre>Emulator</genre>
  290          <players>1</players>
  291          <image>./images/melonds.svg</image>
  292      </game>
  293      <game>
  294          <path>./Start Moonlight.sh</path>
  295          <name>Start Moonlight</name>
  296          <desc>Opens the Moonlight GUI to enable global configuration changes to be made directly. Moonlight (formerly Limelight) is an open source implementation of NVIDIA's GameStream protocol. We implemented the protocol used by the NVIDIA Shield and wrote a set of 3rd party clients. You can stream your collection of PC games from your GameStream-compatible PC to any supported device and play them remotely. Moonlight is perfect for gaming on the go without sacrificing the graphics and game selection available on PC.</desc>
  297          <developer>ROCKNIX</developer>
  298          <publisher>ROCKNIX</publisher>
  299          <rating>5.0</rating>
  300          <releasedate>2023</releasedate>
  301          <genre>Game Stream</genre>
  302          <players>1</players>
  303          <image>./images/moonlight.svg</image>
  304      </game>
  305      <game>
  306          <path>./Start ARMSX2.sh</path>
  307          <name>Start ARMSX2</name>
  308          <desc>Opens the ARMSX2 GUI (PS2) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. ARMSX2 is an ARM64 PlayStation 2 (PS2) emulator, a fork of PCSX2. Its purpose is to emulate the PS2's hardware, using a combination of MIPS CPU Interpreters, Recompilers and a Virtual Machine which manages hardware states and PS2 system memory.</desc>
  309          <developer>ROCKNIX</developer>
  310          <publisher>ROCKNIX</publisher>
  311          <rating>5.0</rating>
  312          <releasedate>2021</releasedate>
  313          <genre>Emulator</genre>
  314          <players>1</players>
  315          <image>./images/pcsx2.svg</image>
  316      </game>
  317      <game>
  318          <path>./Start PPSSPP.sh</path>
  319          <name>Start PPSSPP</name>
  320          <desc>Opens the PPSSPP GUI (PSP) to enable global configuration changes to be made directly to the emulator. PPSSPP can run your PSP games on your PC or Android phone in full HD resolution or even higher. It can also upscale textures to make them sharper, and you can enable post-processing shaders to adjust color and brightness the way you like, and other effects.</desc>
  321          <developer>ROCKNIX</developer>
  322          <publisher>ROCKNIX</publisher>
  323          <rating>5.0</rating>
  324          <releasedate>2021</releasedate>
  325          <genre>Emulator</genre>
  326          <players>1</players>
  327          <image>./images/ppsspp.svg</image>
  328      </game>
  329      <game>
  330          <path>./Start SkyEmu.sh</path>
  331          <name>Start SkyEmu</name>
  332          <desc>Opens the SkyEmu GUI (GB / GBC / GBA / NDS) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard to modify settings.</desc>
  333          <developer>ROCKNIX</developer>
  334          <publisher>ROCKNIX</publisher>
  335          <rating>5.0</rating>
  336          <releasedate>2025</releasedate>
  337          <genre>Emulator</genre>
  338          <players>1</players>
  339          <image>./images/skyemu.svg</image>
  340      </game>
  341      <game>
  342          <path>./Start 32bit Retroarch.sh</path>
  343          <name>Start RetroArch (32-bit)</name>
  344          <desc>Opens the RetroArch GUI (32-bit version) to enable global configuration changes to be made directly to the emulator. RetroArch is a frontend for emulators, game engines and media players.</desc>
  345          <developer>ROCKNIX</developer>
  346          <publisher>ROCKNIX</publisher>
  347          <rating>5.0</rating>
  348          <releasedate>2021</releasedate>
  349          <genre>Emulator</genre>
  350          <players>1</players>
  351          <image>./images/retroarch-32.svg</image>
  352      </game>
  353      <game>
  354          <path>./Start 64bit Retroarch.sh</path>
  355          <name>Start RetroArch (64-bit)</name>
  356          <desc>Opens the RetroArch GUI (64-bit version) to enable global configuration changes to be made directly to the emulator. RetroArch is a frontend for emulators, game engines and media players.</desc>
  357          <developer>ROCKNIX</developer>
  358          <publisher>ROCKNIX</publisher>
  359          <rating>5.0</rating>
  360          <releasedate>2021</releasedate>
  361          <genre>Emulator</genre>
  362          <players>1</players>
  363          <image>./images/retroarch-64.svg</image>
  364      </game>
  365      <game>
  366          <path>./Start RPCS3.sh</path>
  367          <name>Start RPCS3</name>
  368          <desc>Opens the RPCS3 GUI (PS3) to enable configuration changes to be made directly to the emulator. You can use this to set up firmware, update controls and install packages. It's recommended to have a mouse and keyboard available to modify settings. RPCS3 is a multi-platform open-source Sony PlayStation 3 emulator and debugger written in C++ for Windows, Linux, macOS and FreeBSD.</desc>
  369          <developer>ROCKNIX</developer>
  370          <publisher>ROCKNIX</publisher>
  371          <rating>5.0</rating>
  372          <releasedate>2021</releasedate>
  373          <genre>Emulator</genre>
  374          <players>1</players>
  375          <image>./images/rpcs3.svg</image>
  376      </game>
  377      <game>
  378          <path>./Start ScummVM.sh</path>
  379          <name>Start ScummVM</name>
  380          <desc>Opens the ScummVM GUI to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. ScummVM is a program which allows you to run certain classic graphical adventure and role-playing games, provided you already have their data files. The clever part about this: ScummVM just replaces the executables shipped with the games, allowing you to play them on systems for which they were never designed! ScummVM is a complete rewrite of these games' executables and is not an emulator.</desc>
  381          <developer>ROCKNIX</developer>
  382          <publisher>ROCKNIX</publisher>
  383          <rating>5.0</rating>
  384          <releasedate>2021</releasedate>
  385          <genre>Emulator</genre>
  386          <players>1</players>
  387          <image>./images/scummvm.svg</image>
  388      </game>
  389      <game>
  390          <path>./Start touchHLE.sh</path>
  391          <name>Start touchHLE</name>
  392          <desc>Opens the touchHLE GUI (iOS) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. A free and open-source application that emulates iOS games compatible with iOS 2 &amp; 3, enabling people to play their iOS games on Windows, macOS, and Linux systems.</desc>
  393          <developer>ROCKNIX</developer>
  394          <publisher>ROCKNIX</publisher>
  395          <rating>5.0</rating>
  396          <releasedate>2026</releasedate>
  397          <genre>Emulator</genre>
  398          <players>1</players>
  399          <image>./images/touchhle.svg</image>
  400      </game>
  401      <game>
  402          <path>./Start Vita3K.sh</path>
  403          <name>Start Vita3K</name>
  404          <desc>Opens the Vita3K GUI (PS Vita) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. Vita3K is a free and open-source PlayStation Vita emulator for Windows, macOS, and Linux systems.</desc>
  405          <developer>ROCKNIX</developer>
  406          <publisher>ROCKNIX</publisher>
  407          <rating>5.0</rating>
  408          <releasedate>2023</releasedate>
  409          <genre>Emulator</genre>
  410          <players>1</players>
  411          <image>./images/vita3k.svg</image>
  412      </game>
  413      <game>
  414          <path>./Start Xemu.sh</path>
  415          <name>Start Xemu</name>
  416          <desc>Opens the Xemu GUI (Xbox) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. A free and open-source application that emulates the original Microsoft Xbox game console, enabling people to play their original Xbox games on Windows, macOS, and Linux systems.</desc>
  417          <developer>ROCKNIX</developer>
  418          <publisher>ROCKNIX</publisher>
  419          <rating>5.0</rating>
  420          <releasedate>2023</releasedate>
  421          <genre>Emulator</genre>
  422          <players>1</players>
  423          <image>./images/xemu.svg</image>
  424      </game>
  425      <game>
  426          <path>./Scan id Tech Games.sh</path>
  427          <name>Scan id Tech Games</name>
  428          <desc>Creates launchers for id software games</desc>
  429          <developer>ROCKNIX</developer>
  430          <publisher>ROCKNIX</publisher>
  431          <rating>5.0</rating>
  432          <releasedate>2023</releasedate>
  433          <genre>Script</genre>
  434          <players>1</players>
  435          <image>./images/idtech.svg</image>
  436      </game>
  437      <game>
  438          <path>./Scan ScummVM Games.sh</path>
  439          <name>Scan ScummVM Games</name>
  440          <desc>Creates launchers for ScummVM games</desc>
  441          <developer>ROCKNIX</developer>
  442          <publisher>ROCKNIX</publisher>
  443          <rating>5.0</rating>
  444          <releasedate>2021</releasedate>
  445          <genre>Emulator</genre>
  446          <players>1</players>
  447          <image>./images/scummvm.svg</image>
  448      </game>
  449      <game>
  450          <path>./Test Gamepad.sh</path>
  451          <name>Test Gamepad</name>
  452          <desc>A simple SDL GUI gamepad tester to help validate gamepad inputs.</desc>
  453          <developer>ROCKNIX</developer>
  454          <publisher>ROCKNIX</publisher>
  455          <rating>5.0</rating>
  456          <releasedate>2024</releasedate>
  457          <genre>tool</genre>
  458          <players>1</players>
  459          <image>./images/test-gamepad.svg</image>
  460      </game>
  461      <game>
  462          <path>./Test Touchscreen.sh</path>
  463          <name>Test Touchscreen</name>
  464          <desc>A simple SDL GUI touchscreen tester to help validate touchscreen inputs.</desc>
  465          <developer>ROCKNIX</developer>
  466          <publisher>ROCKNIX</publisher>
  467          <rating>5.0</rating>
  468          <releasedate>2024</releasedate>
  469          <genre>tool</genre>
  470          <players>1</players>
  471          <image>./images/test-touchscreen.svg</image>
  472      </game>
  473      <game>
  474          <path>./GPcal.sh</path>
  475          <name>Calibrate Gamepad</name>
  476          <desc>A gamepad tool that enables the user to calibrate the analog sticks and triggers on the Retroid Pocket 5 and Mini.</desc>
  477          <developer>CDELETRE</developer>
  478          <publisher>ROCKNIX</publisher>
  479          <rating>5.0</rating>
  480          <releasedate>2024</releasedate>
  481          <genre>tool</genre>
  482          <players>1</players>
  483          <image>./images/calibrate-gamepad.svg</image>
  484      </game>
  485      <game>
  486          <path>./Mount NFS.sh</path>
  487          <name>Mount NFS</name>
  488          <desc>Mounts an NFS share at a location defined in /storage/.nfs-mount and creates a merged storage with the games-internal card as the upper/writeable location</desc>
  489          <developer>ROCKNIX</developer>
  490          <publisher>ROCKNIX</publisher>
  491          <rating>5.0</rating>
  492          <releasedate>2024</releasedate>
  493          <genre>tool</genre>
  494          <players>1</players>
  495          <image>./images/nfs.svg</image>
  496       </game>
  497  </gameList>
  498  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-bad/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  . ${ROOT}/packages/multimedia/gstreamer/gst-plugins-bad/package.mk
    5  
    6  # Upstream builds this for nothing in our images and throws every library
    7  # away. webkitgtk 2.54 links gstreamer-mpegts -- the library, not the
    8  # demuxer plugin -- as a hard requirement of the video it cannot build
    9  # without (fork #228, D-WORKFLOW-038), so this override turns the mpegts
   10  # pieces on and keeps their library, and nothing else changes.
   11  #
   12  # The option string is upstream's own: the generic recipe builds it inside
   13  # pre_configure_target, so that function is kept under another name and
   14  # called first, and only the two mpegts options are flipped in what it
   15  # produced. Reading the string out of the recipe's text instead (as this
   16  # override once did) broke on a quoted value ending a line. If either flip
   17  # finds nothing to flip, the generic string has changed shape and the
   18  # package stops rather than configuring without the library WebKit needs.
   19  eval "gst_plugins_bad_generic_$(declare -f pre_configure_target)"
   20  
   21  pre_configure_target() {
   22    gst_plugins_bad_generic_pre_configure_target
   23    PKG_MESON_OPTS_TARGET="${PKG_MESON_OPTS_TARGET/-Dmpegtsdemux=disabled/-Dmpegtsdemux=enabled}"
   24    PKG_MESON_OPTS_TARGET="${PKG_MESON_OPTS_TARGET/-Dmpegtsmux=disabled/-Dmpegtsmux=enabled}"
   25    case "${PKG_MESON_OPTS_TARGET}" in
   26      *-Dmpegtsdemux=enabled*) ;;
   27      *) die "gst-plugins-bad: the generic option string has no -Dmpegtsdemux to enable" ;;
   28    esac
   29    case "${PKG_MESON_OPTS_TARGET}" in
   30      *-Dmpegtsmux=enabled*) ;;
   31      *) die "gst-plugins-bad: the generic option string has no -Dmpegtsmux to enable" ;;
   32    esac
   33  }
   34  
   35  post_makeinstall_target() {
   36    # Only libgstmpegts-1.0 is kept, and it has to be there: WebKit cannot
   37    # start without it, so its absence fails the package here rather than
   38    # the sign-in window at load. The name checked is the one the loader
   39    # asks for, the soname libgstmpegts-1.0.so.0, and it has to resolve to a
   40    # file -- a link whose file is missing matches a glob and loads nothing --
   41    # before the keep and again in what was kept.
   42    local keep="${PKG_BUILD}/.rocknix-keep"
   43    [ -f "${INSTALL}/usr/lib/libgstmpegts-1.0.so.0" ] \
   44      || die "gst-plugins-bad: libgstmpegts-1.0 was not built -- WebKit needs it"
   45    rm -rf "${keep}" && mkdir -p "${keep}/lib"
   46    cp -a ${INSTALL}/usr/lib/libgstmpegts-1.0.so* "${keep}/lib"/
   47    safe_remove ${INSTALL}
   48    mkdir -p ${INSTALL}/usr/lib
   49    cp -a "${keep}/lib"/. ${INSTALL}/usr/lib/
   50    rm -rf "${keep}"
   51    [ -f "${INSTALL}/usr/lib/libgstmpegts-1.0.so.0" ] \
   52      || die "gst-plugins-bad: libgstmpegts-1.0 was not kept -- WebKit needs it"
   53  }
   54  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-base/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  . ${ROOT}/packages/multimedia/gstreamer/gst-plugins-base/package.mk
    5  
    6  # GL needs the EGL/GLES headers and wayland-client in the sysroot before
    7  # meson looks for them (fork #228).
    8  PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} mesa wayland"
    9  
   10  # Upstream throws the whole install away -- this package exists there only to
   11  # populate the sysroot so other things can link. That works right up until
   12  # something links it and then has to *run*: WebKit pulls in libgstapp, audio,
   13  # video, tag, pbutils, allocators and fft, and without them
   14  # cloud-signin-window dies at load with "cannot open shared object file".
   15  #
   16  # So keep the shared libraries and nothing else. The plugins, headers,
   17  # pkg-config files and tools stay build-time only, as before.
   18  # WebKit builds its media pipeline out of appsrc/appsink, and upstream
   19  # disables that plugin because nothing else in the image wanted it. Without
   20  # it WebKit asks the registry for "appsink", gets NULL, and segfaults
   21  # dereferencing it -- taking the whole web process down a second after every
   22  # page load, which presents as keystrokes not reaching the page rather than
   23  # as anything to do with media.
   24  #
   25  # Restated in full rather than patched: the generic recipe builds this string
   26  # from scratch inside pre_configure_target, so a substitution at global scope
   27  # is overwritten before configure sees it, and there is no configure hook to
   28  # chain onto. Only -Dapp differs from upstream; keep the rest in step when
   29  # rebasing.
   30  pre_configure_target() {
   31    PKG_MESON_OPTS_TARGET="-Dgl=enabled \
   32                           -Dgl_platform=egl \
   33                           -Dgl_winsys=wayland \
   34                           -Dadder=disabled \
   35                           -Dapp=enabled \
   36                           -Daudioconvert=disabled \
   37                           -Daudiomixer=disabled \
   38                           -Daudiorate=disabled \
   39                           -Daudioresample=disabled \
   40                           -Daudiotestsrc=disabled \
   41                           -Dcompositor=disabled \
   42                           -Dencoding=disabled \
   43                           -Dgio=disabled \
   44                           -Dgio-typefinder=disabled \
   45                           -Doverlaycomposition=disabled \
   46                           -Dpbtypes=disabled \
   47                           -Dplayback=disabled \
   48                           -Drawparse=enabled \
   49                           -Dsubparse=enabled \
   50                           -Dtcp=disabled \
   51                           -Dtypefind=disabled \
   52                           -Dvideoconvertscale=disabled \
   53                           -Dvideorate=disabled \
   54                           -Dvideotestsrc=disabled \
   55                           -Dvolume=disabled \
   56                           -Dalsa=disabled \
   57                           -Dcdparanoia=disabled \
   58                           -Dlibvisual=disabled \
   59                           -Dogg=disabled \
   60                           -Dopus=disabled \
   61                           -Dpango=disabled \
   62                           -Dtheora=disabled \
   63                           -Dtremor=disabled \
   64                           -Dvorbis=disabled \
   65                           -Dx11=disabled \
   66                           -Dxshm=disabled \
   67                           -Dxi=disabled \
   68                           -Dxvideo=disabled \
   69                           -Dexamples=disabled \
   70                           -Dtests=disabled \
   71                           -Dtools=disabled \
   72                           -Dintrospection=disabled \
   73                           -Dnls=disabled \
   74                           -Dorc=disabled \
   75                           -Dglib_debug=disabled \
   76                           -Dglib_assert=false \
   77                           -Dglib_checks=false \
   78                           -Dpackage-name=gst-plugins-base \
   79                           -Dpackage-origin=LibreELEC.tv \
   80                           -Ddoc=disabled"
   81  }
   82  
   83  post_makeinstall_target() {
   84    # The libraries and plugins, not the libraries alone: see the appsink
   85    # paragraph above. What WebKit loads and cannot start without -- the
   86    # libraries it links and the plugin that provides appsink -- has to be
   87    # there, so its absence fails the package here rather than the sign-in
   88    # window at load or a second after it. Each is checked by the name the
   89    # loader asks for -- a library's soname, lib<name>-1.0.so.0, and the
   90    # plugin's own file -- resolving to a file, before the keep and again in
   91    # what was kept: a link whose file is missing matches a glob and loads
   92    # nothing, and neither does a file whose name only starts the same way.
   93    local keep="${PKG_BUILD}/.rocknix-keep" f
   94    local needs="libgstapp-1.0.so.0 libgstaudio-1.0.so.0 libgstvideo-1.0.so.0 libgsttag-1.0.so.0
   95                 libgstpbutils-1.0.so.0 libgstallocators-1.0.so.0 libgstfft-1.0.so.0 gstreamer-1.0/libgstapp.so"
   96    for f in ${needs}; do
   97      [ -f "${INSTALL}/usr/lib/${f}" ] || die "gst-plugins-base: ${f##*/} was not built -- WebKit needs it"
   98    done
   99    rm -rf "${keep}" && mkdir -p "${keep}/lib" "${keep}/plugins"
  100    cp -a ${INSTALL}/usr/lib/libgst*.so* "${keep}/lib"/
  101    cp -a ${INSTALL}/usr/lib/gstreamer-1.0/*.so "${keep}/plugins"/
  102    safe_remove ${INSTALL}
  103    mkdir -p ${INSTALL}/usr/lib/gstreamer-1.0
  104    cp -a "${keep}/lib"/. ${INSTALL}/usr/lib/
  105    cp -a "${keep}/plugins"/. ${INSTALL}/usr/lib/gstreamer-1.0/
  106    rm -rf "${keep}"
  107    for f in ${needs}; do
  108      [ -f "${INSTALL}/usr/lib/${f}" ] || die "gst-plugins-base: ${f##*/} was not kept -- WebKit needs it"
  109    done
  110  }
  111  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/multimedia/gstreamer/gstreamer/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  . ${ROOT}/packages/multimedia/gstreamer/gstreamer/package.mk
    5  
    6  # The plugin registry, which upstream disables.
    7  #
    8  # Without it GStreamer does no dynamic plugin discovery at all: elements can
    9  # only be found if something linked them in directly. So WebKit asks for
   10  # "appsink", the registry that would have found it does not exist, it gets
   11  # NULL back and segfaults dereferencing it -- killing the web process a
   12  # second after every page load. Shipping the plugin made no difference, and
   13  # neither did GST_PLUGIN_PATH, because nothing was scanning.
   14  #
   15  # Restated in full rather than patched: the generic recipe builds this string
   16  # inside pre_configure_target, so a substitution at global scope is
   17  # overwritten before configure sees it. Registry and tools differ from
   18  # upstream: tools also builds the external plugin scanner (#572). Keep the
   19  # remaining options in step when rebasing.
   20  pre_configure_target() {
   21    PKG_MESON_OPTS_TARGET="-Dgst_debug=false \
   22                           -Dgst_parse=true \
   23                           -Dregistry=true \
   24                           -Dtracer_hooks=false \
   25                           -Doption-parsing=true \
   26                           -Dpoisoning=false \
   27                           -Dcheck=disabled \
   28                           -Dlibunwind=disabled \
   29                           -Dlibdw=disabled \
   30                           -Ddbghelp=disabled \
   31                           -Dbash-completion=disabled \
   32                           -Dcoretracers=disabled \
   33                           -Dexamples=disabled \
   34                           -Dtests=disabled \
   35                           -Dbenchmarks=disabled \
   36                           -Dtools=enabled \
   37                           -Ddoc=disabled \
   38                           -Dintrospection=disabled \
   39                           -Dnls=disabled \
   40                           -Dglib_debug=disabled \
   41                           -Dglib_assert=false \
   42                           -Dglib_checks=false \
   43                           -Dextra-checks=disabled \
   44                           -Dpackage-name="gstreamer"
   45                           -Dpackage-origin="LibreELEC.tv"
   46                           -Ddoc=disabled"
   47  }
   48  
   49  post_makeinstall_target() {
   50    # Keep libgstcontroller for GL and libgstnet for the installed UDP, RTP,
   51    # RTSP and adaptive-demux plugins from gst-plugins-good (#572).
   52    safe_remove ${INSTALL}/usr/share
   53  }
   54  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/multimedia/libplacebo/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    3  
    4  PKG_NAME="libplacebo"
    5  PKG_VERSION="05ac2cca6571c04d06369a26825d207781b73f32"
    6  PKG_LICENSE="GPLv2+"
    7  PKG_SITE="https://code.videolan.org/videolan/libplacebo"
    8  PKG_URL="${PKG_SITE}.git"
    9  PKG_DEPENDS_TARGET="toolchain ffmpeg SDL2 luajit libass"
   10  PKG_LONGDESC="The core rendering algorithms and ideas of mpv rewritten as an independent library."
   11  
   12  # Build only the library; the bundled demo programs fail to link on x86_64 and
   13  # aren't needed by our consumers (mpv/vlc).
   14  PKG_MESON_OPTS_TARGET="-Ddemos=false"
   15  
   16  if [ "${VULKAN_SUPPORT}" = "yes" ]; then
   17    PKG_DEPENDS_TARGET+=" ${VULKAN} glslang spirv-tools"
   18    PKG_MESON_OPTS_TARGET+=" -Dvulkan=enabled -Dglslang=enabled"
   19  else
   20    PKG_MESON_OPTS_TARGET+=" -Dvulkan=disabled -Dglslang=disabled"
   21  fi
   22  
   23  pre_configure_target() {
   24    if [ "${VULKAN_SUPPORT}" = "yes" ]; then
   25      # meson does not automatically link libglslang
   26      export TARGET_LDFLAGS="${LDFLAGS} -lglslang -lSPIRV-Tools-opt -lSPIRV-Tools"
   27    fi
   28  }
   29  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/multimedia/opusfile/package.mk

```
    1  ################################################################################
    2  #      This file is part of OpenELEC - http://www.openelec.tv
    3  #      Copyright (C) 2009-2012 Stephan Raue (stephan@openelec.tv)
    4  #
    5  #  This Program is free software; you can redistribute it and/or modify
    6  #  it under the terms of the GNU General Public License as published by
    7  #  the Free Software Foundation; either version 2, or (at your option)
    8  #  any later version.
    9  #
   10  #  This Program is distributed in the hope that it will be useful,
   11  #  but WITHOUT ANY WARRANTY; without even the implied warranty of
   12  #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   13  #  GNU General Public License for more details.
   14  #
   15  #  You should have received a copy of the GNU General Public License
   16  #  along with OpenELEC.tv; see the file COPYING.  If not, write to
   17  #  the Free Software Foundation, 51 Franklin Street, Suite 500, Boston, MA 02110, USA.
   18  #  http://www.gnu.org/copyleft/gpl.html
   19  ################################################################################
   20  
   21  PKG_NAME="opusfile"
   22  PKG_VERSION="9d718345ce03b2fad5d7d28e0bcd1cc69ab2b166"
   23  PKG_LICENSE="BSD-3-Clause"
   24  PKG_SHA256="7ccef70b05119a6842634eaddb8932400ad16b808c13b6dc78ab56c4cbbf5cf6"
   25  PKG_SITE="https://github.com/xiph/opusfile"
   26  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.zip"
   27  PKG_DEPENDS_TARGET="toolchain opus openssl"
   28  PKG_LONGDESC="Stand-alone decoder library for .opus streams"
   29  PKG_TOOLCHAIN="autotools"
   30  
   31  #pre_configure_target() {
   32  #  cd ${BUILD_DIR}
   33  #  ./autogen.sh
   34  #}
   35  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/network/avahi/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
    4  
    5  PKG_NAME="avahi"
    6  PKG_VERSION="0.8"
    7  PKG_SHA256="c15e750ef7c6df595fb5f2ce10cac0fee2353649600e6919ad08ae8871e4945f"
    8  PKG_LICENSE="GPL"
    9  PKG_SITE="http://avahi.org/"
   10  PKG_URL="https://github.com/lathiat/avahi/archive/v${PKG_VERSION}.tar.gz"
   11  PKG_DEPENDS_TARGET="autotools:host gcc:host expat libdaemon dbus gettext"
   12  PKG_LONGDESC="Service Discovery for Linux using mDNS/DNS-SD, compatible with Bonjour."
   13  PKG_TOOLCHAIN="configure"
   14  
   15  PKG_CONFIGURE_OPTS_TARGET="py_cv_mod_gtk_=yes \
   16                             py_cv_mod_dbus_=yes \
   17                             ac_cv_func_chroot=no \
   18                             --with-distro=none \
   19                             --disable-glib \
   20                             --disable-gobject \
   21                             --disable-qt3 \
   22                             --disable-qt4 \
   23                             --disable-qt5 \
   24                             --disable-gtk \
   25                             --disable-gtk3 \
   26                             --enable-dbus \
   27                             --disable-dbm \
   28                             --disable-gdbm \
   29                             --enable-libdaemon \
   30                             --disable-python \
   31                             --disable-python-dbus \
   32                             --disable-mono \
   33                             --disable-monodoc \
   34                             --disable-autoipd \
   35                             --disable-doxygen-doc \
   36                             --disable-doxygen-dot \
   37                             --disable-doxygen-man \
   38                             --disable-doxygen-rtf \
   39                             --disable-doxygen-xml \
   40                             --disable-doxygen-chm \
   41                             --disable-doxygen-chi \
   42                             --disable-doxygen-html \
   43                             --disable-doxygen-ps \
   44                             --disable-doxygen-pdf \
   45                             --disable-core-docs \
   46                             --disable-manpages \
   47                             --disable-xmltoman \
   48                             --disable-tests \
   49                             --disable-libevent \
   50                             --enable-compat-libdns_sd \
   51                             --disable-compat-howl \
   52                             --disable-rpath \
   53                             --with-xml=expat \
   54                             --with-avahi-user=avahi \
   55                             --with-avahi-group=avahi \
   56                             --disable-nls"
   57  
   58  pre_configure_target() {
   59    NOCONFIGURE=1 ./autogen.sh
   60  }
   61  
   62  post_configure_target() {
   63    libtool_remove_rpath libtool
   64  }
   65  
   66  post_makeinstall_target() {
   67    # disable wide-area
   68    sed -e "s,^.*enable-wide-area=.*$,enable-wide-area=no,g" -i ${INSTALL}/etc/avahi/avahi-daemon.conf
   69    # publish-hinfo
   70    sed -e "s,^.*publish-hinfo=.*$,publish-hinfo=no,g" -i ${INSTALL}/etc/avahi/avahi-daemon.conf
   71    # publish-workstation
   72    sed -e "s,^.*publish-workstation=.*$,publish-workstation=no,g" -i ${INSTALL}/etc/avahi/avahi-daemon.conf
   73    # browse domains?
   74    sed -e "s,^.*browse-domains=.*$,# browse-domains=,g" -i ${INSTALL}/etc/avahi/avahi-daemon.conf
   75    # set root user as default
   76    sed -e "s,<port>22</port>,<port>22</port>\n    <txt-record>path=/storage</txt-record>\n    <txt-record>u=root</txt-record>,g" -i ${INSTALL}/etc/avahi/services/sftp-ssh.service
   77  
   78    rm -rf ${INSTALL}/etc/avahi/avahi-dnsconfd.action
   79    if [ ! ${SFTP_SERVER} = "yes" ]; then
   80      rm -rf ${INSTALL}/etc/avahi/services/ssh.service
   81      rm -rf ${INSTALL}/etc/avahi/services/sftp-ssh.service
   82    fi
   83    # avahi's own units go, as in the generic recipe: scripts/install copies
   84    # this package's system.d/ into the image first and extracts the package's
   85    # make-install tree over it, so with these left in place the stock
   86    # avahi-daemon.service (socket-activated, no ordering, no off-switch)
   87    # replaced the fork's and the daemon published whatever the kernel was
   88    # called when the socket woke it -- ROCKNIX.local on a device named
   89    # GENERIC-X64-0964 (#151 PL-01). This line was the one the override lacked.
   90    rm -rf ${INSTALL}/usr/lib/systemd
   91    rm -f ${INSTALL}/usr/share/dbus-1/system-services/org.freedesktop.Avahi.service
   92    rm -f ${INSTALL}/usr/sbin/avahi-dnsconfd
   93    rm -f ${INSTALL}/usr/bin/avahi-bookmarks
   94    rm -f ${INSTALL}/usr/bin/avahi-publish*
   95    rm -f ${INSTALL}/usr/bin/avahi-resolve*
   96    rm -f ${INSTALL}/usr/lib/libdns_sd*
   97  
   98    mkdir -p ${INSTALL}/usr/share/services
   99      cp -P ${PKG_DIR}/default.d/*.conf ${INSTALL}/usr/share/services
  100  }
  101  
  102  post_install() {
  103    add_user avahi x 70 70 "avahi-daemon" "/var/run/avahi-daemon" "/bin/sh"
  104    add_group avahi 70
  105  
  106    enable_service avahi-defaults.service
  107    # The responder is on (fork #50, D-NET-003, the maintainer's call of
  108    # 2026-09-13): with it off since the first ROCKNIX commit a device could
  109    # resolve other .local names (nss-mdns) but never answer for its own, and
  110    # two same-family units on one network were addressable by neither name
  111    # nor lease. It publishes the kernel hostname, which network-base-setup
  112    # has made this unit's own by the time the daemon starts (the unit orders
  113    # after it, and network-base-setup tells a daemon that is somehow already
  114    # up). Off is two files: remove /storage/.cache/services/avahi.conf and
  115    # create avahi.disabled beside it -- the unit conditions on the conf, and
  116    # avahi-defaults.service (pulled in by Requires=, no [Install] of its own)
  117    # re-creates the conf at the next start unless .disabled is there.
  118    enable_service avahi-daemon.service
  119  }
  120  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/network/avahi/system.d/avahi-daemon.service

```
    1  [Unit]
    2  Description=Avahi Daemon
    3  # After network-base.service by name: network.target does not order after
    4  # the units wanted by it, and the daemon publishes whatever the kernel is
    5  # called when it starts (fork #50).
    6  After=network.target network-base.service avahi-defaults.service
    7  Requires=avahi-defaults.service
    8  ConditionPathExists=/storage/.cache/services/avahi.conf
    9  
   10  [Service]
   11  Restart=on-failure
   12  EnvironmentFile=-/run/rocknix/debug/avahi.conf
   13  ExecStart=/usr/sbin/avahi-daemon -s $AVAHI_DEBUG
   14  ExecReload=/usr/sbin/avahi-daemon -r
   15  TimeoutStopSec=1s
   16  RestartSec=2
   17  StartLimitInterval=60
   18  StartLimitBurst=10
   19  
   20  [Install]
   21  WantedBy=multi-user.target
   22  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/network/enet/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
    3  
    4  PKG_NAME="enet"
    5  PKG_VERSION="v1.3.18"
    6  PKG_SHA256="28603c895f9ed24a846478180ee72c7376b39b4bb1287b73877e5eae7d96b0dd"
    7  PKG_SITE="https://github.com/lsalzman/enet"
    8  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
    9  PKG_LICENSE="MIT"
   10  PKG_DEPENDS_TARGET="toolchain"
   11  PKG_LONGDESC="A network communication layer on top of UDP (User Datagram Protocol)."
   12  PKG_TOOLCHAIN="autotools"
   13  
   14  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/network/networkmanager/config/NetworkManager.conf

```
    1  # ROCKNIX: NetworkManager owns Ethernet and Wi-Fi; Wi-Fi uses iwd as backend.
    2  
    3  [main]
    4  auth-polkit=false
    5  plugins=keyfile
    6  dhcp=internal
    7  dns=systemd-resolved
    8  # The hostname is system.hostname's, applied by network-base-setup. Left to
    9  # itself NetworkManager claims a static hostname the moment it starts (ROCKNIX,
   10  # from its own fallback), before that script has run on H700, and hostnamed
   11  # then re-applies it over the name the player chose; which one stuck differed
   12  # per boot (fork #106, 2026-09-10).
   13  hostname-mode=none
   14  
   15  [device]
   16  wifi.backend=iwd
   17  
   18  [keyfile]
   19  path=/storage/.config/NetworkManager/system-connections
   20  # ROCKNIX USB gadget not DHCP to a router.
   21  unmanaged-devices=interface-name:gadget;interface-name:usb0;interface-name:usbnet;interface-name:rndis0
   22  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/network/tailscale/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2022-present kkoshelev (https://github.com/kkoshelev)
    3  # Copyright (C) 2022-present fewtarius (https://github.com/fewtarius)
    4  
    5  PKG_NAME="tailscale"
    6  PKG_VERSION="1.98.8"
    7  # Primary project; embedded dependencies retain their own terms (#528).
    8  PKG_LICENSE="BSD-3-Clause"
    9  PKG_SHA256="53eb3ce89d062fd34e393d24a6c8ec08c769fede8eb77fe9c6e347ad4ae00f84"
   10  PKG_SITE="https://tailscale.com/"
   11  PKG_DEPENDS_TARGET="toolchain wireguard-tools"
   12  PKG_LONGDESC="Zero config VPN. Installs on any device in minutes, manages firewall rules for you, and works from anywhere."
   13  PKG_TOOLCHAIN="manual"
   14  
   15  case ${TARGET_ARCH} in
   16    aarch64)
   17      TS_ARCH="_arm64"
   18      PKG_SHA256="53eb3ce89d062fd34e393d24a6c8ec08c769fede8eb77fe9c6e347ad4ae00f84"
   19    ;;
   20    x86_64)
   21      TS_ARCH="_amd64"
   22      PKG_SHA256="3a55b5900dd7e11e09b6c74d1e46d223d549dfbefbdc1f044a8ab7bdbafb933c"
   23    ;;
   24  esac
   25  
   26  PKG_URL="https://pkgs.tailscale.com/stable/tailscale_${PKG_VERSION}${TS_ARCH}.tgz"
   27  
   28  pre_unpack() {
   29    mkdir -p ${PKG_BUILD}
   30    tar --strip-components=1 -xf $SOURCES/${PKG_NAME}/${PKG_NAME}-${PKG_VERSION}.tgz -C ${PKG_BUILD} tailscale_${PKG_VERSION}${TS_ARCH}
   31  }
   32  
   33  makeinstall_target() {
   34    mkdir -p ${INSTALL}/usr/sbin/
   35      cp ${PKG_BUILD}/tailscale ${INSTALL}/usr/sbin/
   36      cp ${PKG_BUILD}/tailscaled ${INSTALL}/usr/sbin/
   37  
   38    mkdir -p ${INSTALL}/usr/config
   39      cp -R ${PKG_DIR}/config/tailscaled.defaults ${INSTALL}/usr/config
   40  }
   41  
   42  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/network/zerotier-one/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2022-present kkoshelev (https://github.com/kkoshelev)
    3  # Copyright (C) 2022-present fewtarius (https://github.com/fewtarius)
    4  # Copyright (C) 2023-present NeoTheFox (https://github.com/NeoTheFox)
    5  
    6  PKG_NAME="zerotier-one"
    7  PKG_VERSION="1.16.0"
    8  # Core code only; ext/ has separate terms. Nonfree controller omitted (#528).
    9  PKG_LICENSE="MPL-2.0"
   10  PKG_SHA256="aa9de313d365bf0efb3871aaa56f2d323a08f46df47b627c4eff4f4203fa7fc5"
   11  PKG_SITE="https://www.zerotier.com"
   12  PKG_URL="https://github.com/zerotier/ZeroTierOne/archive/refs/tags/${PKG_VERSION}.tar.gz"
   13  PKG_DEPENDS_TARGET="toolchain nlohmann-json"
   14  PKG_LONGDESC="A Smart Ethernet Switch for Earth"
   15  PKG_TOOLCHAIN="manual"
   16  
   17  
   18  unpack() {
   19      # The client does not build the separately licensed controller (#528).
   20      # Override extraction once so its headers cannot enter the build tree.
   21      mkdir -p "${PKG_BUILD}"
   22      tar --strip-components=1 --exclude="ZeroTierOne-${PKG_VERSION}/nonfree" \
   23          -xf "${SOURCES}/${PKG_NAME}/${PKG_NAME}-${PKG_VERSION}.tar.gz" \
   24          -C "${PKG_BUILD}" "ZeroTierOne-${PKG_VERSION}"
   25      [ ! -e "${PKG_BUILD}/nonfree" ] && [ ! -L "${PKG_BUILD}/nonfree" ]
   26  }
   27  
   28  
   29  make_target() {
   30      # Build libnatpmp for target
   31      make -C ${PKG_BUILD}/ext/libnatpmp CC=${CC}
   32  
   33  	# Build zerotier-one
   34      cd ${PKG_BUILD}
   35      CPPFLAGS="${CPPFLAGS} -I${PKG_BUILD}/ext/libnatpmp" \
   36      LDLIBS="${LDLIBS} -L${PKG_BUILD}/ext/libnatpmp" \
   37      make -f make-linux.mk ZT_SSO_SUPPORTED=0 one
   38  }
   39  
   40  makeinstall_target() {
   41      make DESTDIR=${INSTALL} install
   42      rm -rf ${INSTALL}/usr/share/man/
   43  
   44      install -Dm755 ${PKG_DIR}/scripts/zerotier-join.sh ${INSTALL}/usr/sbin/
   45      mkdir -p ${INSTALL}/usr/lib/systemd/system
   46      install -Dm644 ${PKG_DIR}/system.d/zerotier-one.service ${INSTALL}/usr/lib/systemd/system/
   47  }
   48  
   49  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/security/gnutls/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  . ${ROOT}/packages/security/gnutls/package.mk
    5  
    6  # GnuTLS resolves its trust store at build time, and upstream's recipe names
    7  # none -- so it reports "GnuTLS was not configured with a system trust" and
    8  # every certificate fails to verify, even though the image ships three copies
    9  # of the CA bundle. Nothing noticed until something other than rclone needed
   10  # HTTPS: rclone carries its own roots inside the Go binary.
   11  PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET} \
   12                             --with-default-trust-store-file=/etc/ssl/certs/ca-certificates.crt"
   13  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/tools/installer/scripts/installer

```
    1  #!/bin/sh
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
    5  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
    6  
    7  # some DOCs:
    8  
    9  # list devices:
   10  # cat /proc/partitions | sed -n "s/\ *[0-9][0-9]*\ *[0-9][0-9]*\ *[0-9][0-9]*\ \([a-z]*\)$/\1/p"
   11  
   12  # list all partitionnumbers from /dev/sda:
   13  # parted -m /dev/sda print | grep -v ^/dev | grep -v ^BYT | cut -f1 -d ":"
   14  
   15  # list device data from /dev/sda:
   16  # parted -m /dev/sda print | grep /dev/sda
   17  
   18  # list mounted partitions:
   19  # mount | grep ^/dev
   20  
   21  # list modelnumber:
   22  # parted -m /dev/sda print | grep /dev/sda | cut -f7 -d ":" | sed "s/;//"
   23  # list size:
   24  # parted -m /dev/sda print | grep /dev/sda | cut -f2 -d ":"
   25  
   26  # exclude mounted partitions
   27  # for i in `cat /proc/mounts | grep ^/dev/ | cut -f1 -d " " | sed "s/[0-9]//"`; do TEST="$TEST `echo "| grep -v $i"`"; done
   28  
   29  # disable Ctrl+C - can be very dangerous
   30  trap '' 2
   31  
   32  # Don't execute if installer.conf doesn't exist
   33  [ -f /etc/installer.conf ] && . /etc/installer.conf || exit 0
   34  
   35  # Bring in OS variables.
   36  . /etc/os-release
   37  
   38  # Initialize controller input
   39  /usr/bin/control-gen_init.sh
   40  source /storage/.config/gptokeyb/control.ini
   41  get_controls
   42  
   43  if [ -f "/etc/installer.gptk" ]
   44  then
   45    cp /etc/installer.gptk /storage/.config/gptokeyb/installer.gptk
   46    ${GPTOKEYB} "installer" -c "/storage/.config/gptokeyb/installer.gptk" &
   47  fi
   48  
   49  dbglg() {
   50    # Acts just like echo cmd, with automatic redirection
   51  
   52    echo "" >> $LOGFILE
   53    echo "#################################################################" >> $LOGFILE
   54    echo "# $@" >> $LOGFILE
   55    echo "#################################################################" >> $LOGFILE
   56    echo "" >> $LOGFILE
   57  }
   58  
   59  log_system_status() {
   60    echo "# cat /proc/mounts"
   61    cat /proc/mounts
   62    echo
   63  
   64    echo "# df"
   65    df
   66    echo
   67  
   68    echo "# df -h"
   69    df -h
   70    echo
   71  
   72    echo "# parted -s -m -l"
   73    parted -s -m -l
   74    echo
   75  
   76    echo "# blkid"
   77    blkid
   78    echo
   79  
   80    echo "# UEFI (if directory exists)"
   81    ls -la /sys/firmware/efi
   82    echo
   83  
   84    echo "# Disk sizes (bytes)"
   85    grep . /sys/block/*/size
   86    echo
   87  }
   88  
   89  unmount_devices() {
   90    # Unmount anything we didn't boot from so we can use it.
   91    for DEVICE in $(mount | awk '/\/flash |\/storage |\/loop/ {next;} /^\/dev/ {print $1}')
   92    do
   93      EDEVICE=$(echo ${DEVICE} | sed "s#/#-#g")
   94      systemctl stop udevil-mount@${EDEVICE}.service >> $LOGFILE 2>&1
   95      umount $(grep "${DEVICE}" /proc/mounts 2>/dev/null | awk '{print $2}') >> $LOGFILE 2>&1
   96    done
   97  }
   98  
   99  get_device_unmount() {
  100    # get all unmounted devices
  101    # usage: get_devices_unmount
  102    # uses:     -
  103    # provides: DEVICES
  104  
  105    DEVICES=""
  106    DEVICES=$(parted -s -m -l 2>/dev/null | grep -E '^/dev/sd|^/dev/mmcblk|^/dev/nvme' | grep -E -v '.?rpmb|.?boot?' | cut -f1 -d ":")
  107  
  108    for i in $(cat /proc/mounts | grep -E '^/dev/sd' | cut -f1 -d " " | sed "s/[0-9].*$//"); do
  109      DEVICES=$(echo ${DEVICES} | sed -e "s|$i||")
  110    done
  111  
  112    for i in $(cat /proc/mounts | grep -E '^/dev/mmcblk' | cut -f1 -d " " | sed "s/p.*$//"); do
  113      DEVICES=$(echo ${DEVICES} | sed -e "s|$i||")
  114    done
  115  
  116    for i in $(cat /proc/mounts | grep -E '^/dev/nvme' | cut -f1 -d " " | sed "s/p.*$//"); do
  117      DEVICES=$(echo ${DEVICES} | sed -e "s|$i||")
  118    done
  119  }
  120  
  121  get_partition() {
  122    # get all partitions of a specifed device
  123    # usage:    get_partitions /dev/sda
  124    # uses:     -
  125    # provides: PARTITIONS
  126  
  127    PARTITIONS=$(parted -s -m $1 print | grep -v ^/dev | grep -v BYT | cut -f1 -d ":")
  128  }
  129  
  130  create_device_list() {
  131    # creates device list to use in menus
  132    # usage:    create_devices_list
  133    # uses:     get_device_unmount
  134    # provides: DEVICE_MODEL, DEVICE_SIZE, DEVICE_LIST, DEVICE_NAME,
  135    #           DEVICES (get_device_unmount)
  136  
  137    DEVICE_MODEL=""
  138    DEVICE_SIZE=""
  139    DEVICE_LIST=""
  140    DEVICE_NAME=""
  141  
  142    unmount_devices
  143    get_device_unmount
  144  
  145    if [ "${DEVICES}" = "" ]; then
  146      msg_no_device
  147      return 1
  148    fi
  149  
  150    for i in ${DEVICES}; do
  151      DEVICE_MODEL=$(parted -s $i -m print | grep ^$i | cut -f7 -d ":" | sed "s/;//")
  152      DEVICE_SIZE=$(parted -s $i -m print | grep ^$i | cut -f2 -d ":")
  153      DEVICE_NAME=$(echo ${DEVICE_MODEL} ${DEVICE_SIZE} | sed 's/ /_/g')
  154      DEVICE_LIST="${DEVICE_LIST} $i ${DEVICE_NAME}"
  155    done
  156    return 0
  157  }
  158  
  159  do_install_quick() {
  160    # show menu
  161    MSG_TITLE="QUICK INSTALL MENU"
  162    MSG_MENU="\nUse the up/down arrows to select the device you wish to install to.\n\nPlease select a device:"
  163    MSG_CANCEL="Back"
  164  
  165    create_device_list || return
  166  
  167    whiptail --backtitle "$BACKTITLE" --cancel-button "$MSG_CANCEL" \
  168      $DIALOG_OPTIONS --title "$MSG_TITLE" --menu "$MSG_MENU" 20 50 5 \
  169      ${DEVICE_LIST} 2> $TMPDIR/device_for_install
  170    [ $? -ne 0 ] && return
  171  
  172    # now we must do everything
  173    INSTALL_DEVICE=$(cat "$TMPDIR/device_for_install")
  174    INSTALL_DEVICE_FULL=$(echo ${DEVICE_LIST} | sed "s|.*${INSTALL_DEVICE} \([^ ]*\).*|${INSTALL_DEVICE} \1|")
  175  
  176    case ${INSTALL_DEVICE} in
  177      "/dev/mmcblk"*|"/dev/nvme"*)
  178        PARTID="p"
  179        ;;
  180    esac
  181  
  182    prompt_gpt
  183    prompt_backup_unpack
  184  
  185    # check for confirmation (twice!)
  186    MSG_TITLE="Confirmation before installing"
  187    MSG_DETAIL="\nIf you continue the contents of the target disk will be wiped out:\n\n${INSTALL_DEVICE_FULL}\n\n"
  188    DIALOG_OPTIONS="--defaultno"
  189    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" \
  190      $DIALOG_OPTIONS --yesno "$MSG_DETAIL" 0 0
  191    [ $? -ne 0 ] && return
  192  
  193    MSG_TITLE="Confirmation before installing"
  194    MSG_DETAIL="\nThis is last chance to abort the installation!\n\nIf you continue the target disk will be wiped out:\n\n${INSTALL_DEVICE_FULL}\n\n\n"
  195    DIALOG_OPTIONS="--defaultno"
  196    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" \
  197      $DIALOG_OPTIONS --yesno "$MSG_DETAIL" 0 0
  198    [ $? -ne 0 ] && return
  199  
  200    # start the progress bar (whiptail --gauge)
  201    {
  202      # remove all partitions
  203      msg_progress_install "1" "Get all partitions ${INSTALL_DEVICE}"
  204      get_partition ${INSTALL_DEVICE} 2>>$LOGFILE
  205  
  206      msg_progress_install "5" "Wiping disk ${INSTALL_DEVICE}"
  207      dd if=/dev/zero of=${INSTALL_DEVICE} bs=4096 count=1024 2>>$LOGFILE
  208  
  209      # create 2 new partitions (first $PARTSIZE_SYSTEM, second rest)
  210      msg_progress_install "7"  "Creating label on ${INSTALL_DEVICE}"
  211      if [ "$GPT" = "1" ]; then
  212        parted -s ${INSTALL_DEVICE} mklabel gpt >> $LOGFILE 2>&1
  213      else
  214        parted -s ${INSTALL_DEVICE} mklabel msdos >> $LOGFILE 2>&1
  215      fi
  216  
  217      case ${HW_ARCH} in
  218        arm|aarch64)
  219          if [ -e "/usr/share/bootloader/rkspi_loader.img" ]
  220          then
  221            msg_progress_install "8" "Installing Rockchip SPI Loader to ${INSTALL_DEVICE}"
  222            dd if=/usr/share/bootloader/rkspi_loader.img of=${INSTALL_DEVICE} conv=notrunc >> $LOGFILE 2>&1
  223            msg_progress_install "9" "Tell the kernel we have a new partition table on ${INSTALL_DEVICE}"
  224            partprobe ${INSTALL_DEVICE} >> $LOGFILE 2>&1
  225            printf "fix " | parted  ---pretend-input-tty ${INSTALL_DEVICE} print >> $LOGFILE 2>&1
  226            PART1=7
  227            INSTALL_UBOOT=false
  228          fi
  229        ;;
  230        *)
  231          msg_progress_install "9" "Writing Master Boot Record on ${INSTALL_DEVICE}"
  232          PART1=0
  233          if [ "$GPT" = "1" ]; then
  234            cat /usr/share/syslinux/gptmbr.bin > ${INSTALL_DEVICE}
  235          else
  236            cat /usr/share/syslinux/mbr.bin > ${INSTALL_DEVICE}
  237          fi
  238        ;;
  239      esac
  240  
  241      partsize_system_start=$PARTSIZE_SYSTEM_OFFSET
  242      partsize_system_end=$(((PARTSIZE_SYSTEM * 1024 * 1024 / 512) + partsize_system_start - 1))
  243      partsize_storage_start=$((partsize_system_end + 1))
  244      partsize_storage_end=-1024
  245  
  246      PART1=$(( ${PART1} + 1 ))
  247      BOOT_PART=${PART1}
  248  
  249      msg_progress_install "10" "Creating flash partition on ${INSTALL_DEVICE}${PARTID}${PART1}"
  250      if [ "$GPT" = "1" ]; then
  251        parted -s ${INSTALL_DEVICE} unit s mkpart $DISKLABEL_SYSTEM fat32 -- $partsize_system_start $partsize_system_end >> $LOGFILE 2>&1
  252      else
  253        parted -s ${INSTALL_DEVICE} unit s mkpart primary fat32 -- $partsize_system_start $partsize_system_end >> $LOGFILE 2>&1
  254      fi
  255  
  256      PART2=$(( ${PART1} + 1 ))
  257      msg_progress_install "13" "Creating storage partition on ${INSTALL_DEVICE}${PARTID}${PART2}"
  258      if [ "$GPT" = "1" ]; then
  259        parted -s ${INSTALL_DEVICE} unit s mkpart $DISKLABEL_STORAGE ext4 -- $partsize_storage_start $partsize_storage_end >> $LOGFILE 2>&1
  260      else
  261        parted -s ${INSTALL_DEVICE} unit s mkpart primary ext4 -- $partsize_storage_start $partsize_storage_end >> $LOGFILE 2>&1
  262      fi
  263  
  264      msg_progress_install "16" "Setup bootflag on partition ${BOOT_PART} of ${INSTALL_DEVICE}"
  265      parted -s ${INSTALL_DEVICE} set ${BOOT_PART} boot on >> $LOGFILE 2>&1
  266  
  267      case ${HW_ARCH} in
  268        i686|x86_64)
  269          if [ "$GPT" = "1" ]; then
  270            parted -s ${INSTALL_DEVICE} set ${BOOT_PART} legacy_boot on >> $LOGFILE 2>&1
  271          fi
  272        ;;
  273      esac
  274  
  275      msg_progress_install "20" "Tell the kernel we have a new partition table on ${INSTALL_DEVICE}"
  276      partprobe ${INSTALL_DEVICE} >> $LOGFILE 2>&1
  277  
  278      # create filesystem
  279      msg_progress_install "23" "Creating filesystem on ${INSTALL_DEVICE}1"
  280      mkfs.vfat ${INSTALL_DEVICE}${PARTID}${PART1} >> $LOGFILE 2>&1
  281  
  282      msg_progress_install "25" "Set uuid and disklabel $DISKLABEL_SYSTEM on ${INSTALL_DEVICE}${PART1}"
  283      dosfslabel ${INSTALL_DEVICE}${PARTID}${PART1}  $DISKLABEL_SYSTEM >> $LOGFILE 2>&1
  284  
  285      msg_progress_install "28" "Creating filesystem on ${INSTALL_DEVICE}${PARTID}${PART2}"
  286      mke2fs -t ext4 -m 0 ${INSTALL_DEVICE}${PARTID}${PART2} >> $LOGFILE 2>&1
  287  
  288      msg_progress_install "30" "Set uuid and disklabel $DISKLABEL_STORAGE on ${INSTALL_DEVICE}${PARTID}${PART2}"
  289      tune2fs -U random -L $DISKLABEL_STORAGE  ${INSTALL_DEVICE}${PARTID}${PART2} >> $LOGFILE 2>&1
  290  
  291      UUID_SYSTEM="$(blkid --output udev ${INSTALL_DEVICE}${PARTID}${PART1} | grep ^ID_FS_UUID= | cut -d= -f2)"
  292      UUID_STORAGE="$(blkid --output udev ${INSTALL_DEVICE}${PARTID}${PART2} | grep ^ID_FS_UUID= | cut -d= -f2)"
  293  
  294      echo "" >> $LOGFILE
  295      echo "UUID_SYSTEM : ${UUID_SYSTEM}" >> $LOGFILE
  296      echo "UUID_STORAGE: ${UUID_STORAGE}" >> $LOGFILE
  297  
  298      # mount system partition
  299      msg_progress_install "35" "Creating $TMPDIR/part1"
  300      mkdir -p $TMPDIR/part1 >> $LOGFILE 2>&1
  301  
  302      msg_progress_install "40" "Mounting ${INSTALL_DEVICE}${PART1} to $TMPDIR/part1"
  303      mount -t vfat ${INSTALL_DEVICE}${PARTID}${PART1} $TMPDIR/part1 >> $LOGFILE 2>&1
  304  
  305      case ${HW_ARCH} in
  306        arm|aarch64)
  307          if [ ! "${INSTALL_UBOOT}" = false ]
  308          then
  309            msg_progress_install "50" "Installing bootloader to $TMPDIR/part1"
  310            BOOT_DISK="${INSTALL_DEVICE}" BOOT_ROOT="/flash" /usr/share/bootloader/update.sh
  311            mount -o remount,rw $TMPDIR/part1
  312          fi
  313        ;;
  314        i686|x86_64)
  315          # installing syslinux
  316          msg_progress_install "50" "Installing syslinux to $TMPDIR/part1"
  317          syslinux -i ${INSTALL_DEVICE}${PARTID}${PART1} >> $LOGFILE 2>&1
  318  
  319          # configuring bootloader
  320          msg_progress_install "80" "Setup bootloader with boot label = $DISKLABEL_SYSTEM and disk label = $DISKLABEL_STORAGE"
  321          mkdir -p $TMPDIR/part1/EFI/BOOT
  322          cat << EOF > $TMPDIR/part1/syslinux.cfg
  323  DEFAULT linux
  324  PROMPT 0
  325  
  326  LABEL linux
  327   KERNEL /KERNEL
  328   APPEND boot=LABEL=${DISKLABEL_SYSTEM} disk=LABEL=${DISKLABEL_STORAGE} ${EXTRA_CMDLINE}
  329  EOF
  330  
  331          # uefi boot (syslinux only, 64-bit UEFI)
  332          cp /usr/share/syslinux/bootx64.efi $TMPDIR/part1/EFI/BOOT
  333          cp /usr/share/syslinux/ldlinux.e64 $TMPDIR/part1/EFI/BOOT
  334        ;;
  335      esac
  336  
  337      # install system files
  338      msg_progress_install "60" "Installing boot files"
  339      cp -r /flash/* $TMPDIR/part1/ >> $LOGFILE 2>&1
  340      sync
  341  
  342      sync
  343  
  344      # umount system partition, remove mountpoint
  345      msg_progress_install "85" "Unmount $TMPDIR/part1"
  346      umount $TMPDIR/part1 >> $LOGFILE 2>&1
  347  
  348      msg_progress_install "87" "Remove $TMPDIR/part1"
  349      rmdir $TMPDIR/part1 >> $LOGFILE 2>&1
  350  
  351      if [ "$BACKUP_UNPACK" = "1" ]; then
  352        # mount storage partition
  353        msg_progress_install "89" "Creating $TMPDIR/part2"
  354        mkdir -p $TMPDIR/part2 >> $LOGFILE 2>&1
  355  
  356        msg_progress_install "90" "Mounting ${INSTALL_DEVICE}${PARTID}${PART2} to $TMPDIR/part2"
  357        mount -t ext4 ${INSTALL_DEVICE}${PARTID}${PART2} $TMPDIR/part2 >> $LOGFILE 2>&1
  358  
  359        msg_progress_install "92" "Restoring backup"
  360        [ -f /flash/backup.tar.bz2 ] && tar -xjf /flash/backup.tar.bz2 -C $TMPDIR/part2 >> $LOGFILE 2>&1
  361        [ -f /flash/backup.zip ] && unzip -qq /flash/backup.zip -d $TMPDIR/part2 >> $LOGFILE 2>&1
  362        sync
  363  
  364        # umount system partition, remove mountpoint
  365        msg_progress_install "97" "Unmount $TMPDIR/part2"
  366        umount $TMPDIR/part2 >> $LOGFILE 2>&1
  367  
  368        msg_progress_install "100" "Remove $TMPDIR/part2"
  369        rmdir $TMPDIR/part2 >> $LOGFILE 2>&1
  370      fi
  371    } | whiptail --backtitle "$BACKTITLE" --gauge "Please wait while your system is being setup ..." 6 73 0
  372  
  373    # install complete
  374    MSG_TITLE="pixelelated Install Complete"
  375    MSG_DETAIL="You may now remove the install media and shutdown.\n"
  376    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" --msgbox "$MSG_DETAIL" 7 73
  377  }
  378  
  379  msg_no_device() {
  380    # show a warning dialog if we dont find not mounted devices for install and return to main menu
  381    MSG_TITLE="WARNING"
  382    MSG_INFOBOX=" No devices were found. "
  383  
  384    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" --msgbox "$MSG_INFOBOX" 9 73
  385  }
  386  
  387  msg_progress_install() {
  388    # update the whiptail gauge window
  389  
  390    dbglg "$2"
  391    sleep .3
  392    echo XXX
  393    echo $1
  394    echo "$2 ..."
  395    echo XXX
  396  }
  397  
  398  prompt_gpt() {
  399    case ${HW_ARCH} in
  400      arm|aarch64)
  401        BOOT_DEVICE=$(blkid | awk 'BEGIN {FS=":"} /'$(cat /proc/cmdline | sed -e 's~^.*disk=LABEL=~~g; s~\ .*$~~g')'/ {print $1}' | sed 's~p[0-9].*$~~g')
  402        BOOT_LABEL="$(blkid ${BOOT_DEVICE} | grep -Eo 'PTTYPE=".*"' | sed 's~PTTYPE=~~g; s~"~~g')"
  403        case ${BOOT_LABEL} in
  404          gpt)
  405            GPT="1"
  406          ;;
  407          *)
  408            GPT="0"
  409          ;;
  410        esac
  411        UEFI="0"
  412      ;;
  413      *)
  414       GPT="0"
  415       UEFI="0"
  416       # Get size in GB.
  417       # 2^41 bytes is the DOS limit (2199023255552 bytes, 2.2TB). Use GUID Partition Table.>= 2200GB
  418       INSTALL_DEVICE_SIZE=$(($(cat /sys/block/${INSTALL_DEVICE#/dev/}/size)*512/1000/1000/1000))
  419       if [ "${INSTALL_DEVICE_SIZE}" -ge 2200 ] 2>/dev/null; then
  420         GPT="1"
  421       fi
  422       # force gpt + uefi in uefi boot mode
  423       if [ -d /sys/firmware/efi ]; then
  424         UEFI="1"
  425         GPT="1"
  426       fi
  427      ;;
  428    esac
  429  }
  430  
  431  prompt_backup_unpack() {
  432    # Prompt for unpacking backup files to /storage
  433    # usage:    prompt_backup_unpack
  434    # uses:
  435    # provides: BACKUP_UNPACK
  436    BACKUP_UNPACK="0"
  437    if [ -f /flash/backup.tar.bz2 -o -f /flash/backup.zip ]; then
  438      MSG_TITLE="Restore backup files"
  439      MSG_DETAIL="Restore backup files to storage partition.\nFile backup.tar.bz2 or/and backup.zip exist on\ninstallation USB stick."
  440      DIALOG_OPTIONS="--defaultno"
  441      if whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" $DIALOG_OPTIONS --yesno "$MSG_DETAIL" 0 0; then
  442        BACKUP_UNPACK="1"
  443      fi
  444    fi
  445  }
  446  
  447  menu_main() {
  448    # show the mainmenu
  449    MSG_TITLE="MAIN MENU"
  450    MSG_MENU="\nWelcome to pixelelated installation tool! \
  451  \n
  452  This tool is used to copy pixelelated from the installation media \
  453  to your disk or other device. You'll be up and running in no time! \
  454  Please note that the contents of the disk you choose will be wiped \
  455  out during the installation. \
  456  \n\nPlease select:"
  457    MSG_CANCEL="Close"
  458  
  459    whiptail --backtitle "$BACKTITLE" --cancel-button "$MSG_CANCEL" \
  460      --title "$MSG_TITLE" --menu "$MSG_MENU" 18 73 4 \
  461        1 "Install pixelelated" \
  462        2 "View installation log" \
  463        3 "Save installation log" \
  464        4 "Shutdown" 2> $TMPDIR/mainmenu
  465  
  466    case $? in
  467      0)
  468        ITEM_MAINMENU=$(cat "$TMPDIR/mainmenu")
  469        case $ITEM_MAINMENU in
  470          1) do_install_quick;;
  471          2) logfile_show;;
  472          3) logfile_save;;
  473          4) do_poweroff;;
  474        esac
  475        ;;
  476      1|255)
  477        do_poweroff
  478        ;;
  479    esac
  480  }
  481  
  482  logfile_show() {
  483    whiptail --textbox "$LOGFILE" 20 73 --scrolltext --backtitle "$BACKTITLE"
  484  }
  485  
  486  logfile_save() {
  487    mount -o remount,rw /flash
  488  
  489    mkdir -p $(dirname $LOGBACKUP)
  490    cp $LOGFILE $LOGBACKUP
  491    sync
  492  
  493    mount -o remount,ro /flash
  494  
  495    MSG_TITLE="pixelelated Log Saved"
  496    MSG_DETAIL="Log location: ${LOGBACKUP}\n"
  497    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" --msgbox "$MSG_DETAIL" 7 52
  498  }
  499  
  500  do_poweroff() {
  501    # powerdown on request
  502    clear
  503    sync
  504    poweroff -f
  505  }
  506  
  507  # setup needed variables
  508  OS_VERSION=$(lsb_release)
  509  BACKTITLE="pixelelated Installer - ${OS_VERSION}"
  510  
  511  TMPDIR="/tmp/installer"
  512  LOGFILE="$TMPDIR/install.log"
  513  LOGBACKUP="/flash/logs/$(date +%Y%m%d%H%M%S).log"
  514  
  515  export COLORTERM="1"
  516  export NEWT_COLORS="$WHIPTAIL_COLORS"
  517  
  518  IMAGE_KERNEL="KERNEL"
  519  IMAGE_SYSTEM="SYSTEM"
  520  for arg in $(cat /proc/cmdline); do
  521    case $arg in
  522      BOOT_IMAGE=*)
  523        IMAGE_KERNEL="${arg#*=}"
  524        [ "${IMAGE_KERNEL:0:1}" = "/" ] && IMAGE_KERNEL="${IMAGE_KERNEL:1}"
  525        ;;
  526      SYSTEM_IMAGE=*)
  527        IMAGE_SYSTEM="${arg#*=}"
  528        [ "${IMAGE_SYSTEM:0:1}" = "/" ] && IMAGE_SYSTEM="${IMAGE_SYSTEM:1}"
  529        ;;
  530    esac
  531  done
  532  
  533  # prepare temporary directory
  534  rm -rf $TMPDIR
  535  mkdir -p $TMPDIR
  536  
  537  #create log file
  538  echo "pixelelated Installer - ${OS_VERSION} started at:" > $LOGFILE
  539  date >> $LOGFILE
  540  
  541  dbglg "System status"
  542  log_system_status >> $LOGFILE 2>&1
  543  
  544  # generate the en_US.UTF-8 locale to enable line drawing
  545  mkdir -p $TMPDIR/locale
  546  echo "Please wait, configuring en_US.UTF-8."
  547  localedef -i en_US -f UTF-8 $TMPDIR/locale/en_US.UTF-8
  548  export LOCPATH=$TMPDIR/locale
  549  export LC_ALL=en_US.UTF-8
  550  
  551  # main
  552  
  553  while true; do
  554    clear
  555    menu_main
  556  done
  557  
  558  kill -9 $(pidof gptokeyb) 2>/dev/null
  559  
  560  # exit cleanly
  561  exit 0
  562  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/tools/rocknix-abl/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="rocknix-abl"
    5  PKG_VERSION="1.2"
    6  PKG_SHA256="64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7"
    7  PKG_SITE="https://github.com/ROCKNIX/abl"
    8  PKG_URL="https://github.com/ROCKNIX/abl/releases/download/v${PKG_VERSION}/rocknix-abl-v${PKG_VERSION}.tar.gz"
    9  PKG_LONGDESC="ROCKNIX ABL."
   10  PKG_TOOLCHAIN="manual"
   11  
   12  makeinstall_target() {
   13    mkdir -p ${INSTALL}/usr/share/bootloader/rocknix_abl
   14      cp -a ${PKG_BUILD}/abl_signed-${DEVICE}.elf ${INSTALL}/usr/share/bootloader/rocknix_abl/abl_signed-${DEVICE}.elf
   15      cp -a ${PKG_DIR}/sources/* ${INSTALL}/usr/share/bootloader/rocknix_abl
   16      mv ${INSTALL}/usr/share/bootloader/rocknix_abl/flash_abl.sh.template ${INSTALL}/usr/share/bootloader/rocknix_abl/flash_abl.sh
   17      sed -i "s/%DEVICE%/${DEVICE}/g" ${INSTALL}/usr/share/bootloader/rocknix_abl/flash_abl.sh
   18  }
   19  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/tools/rocknix-splash/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="rocknix-splash"
    5  PKG_VERSION="8c71126ceef702528c87a4c49625e64988609f26"
    6  PKG_SHA256="6a24b287920ad553cbe1e2ecf66fac7a4fb2e3756ba1b98473ca201f3abebcba"
    7  PKG_LICENSE="GPL"
    8  PKG_SITE="https://github.com/pixelelated/splash"
    9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_INIT="toolchain"
   11  PKG_LONGDESC="pixelelated splash screen application"
   12  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/virtual/network/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2018-present Team CoreELEC (https://coreelec.org)
    4  
    5  PKG_NAME="network"
    6  PKG_VERSION=""
    7  PKG_LICENSE="various"
    8  PKG_SITE="https://libreelec.tv"
    9  PKG_URL=""
   10  PKG_DEPENDS_TARGET="toolchain iwd networkmanager netbase ethtool openssh iw wireless-regdb rsync tailscale avahi miniupnpc nss-mdns speedtest-cli"
   11  # The offline RetroAchievements proxy (fork #165): a loopback service the
   12  # emulators talk to, off until the player turns it on.
   13  PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} raofflineproxy"
   14  PKG_SECTION="virtual"
   15  PKG_LONGDESC="Metapackage for various packages to install network support"
   16  
   17  if [ "${BLUETOOTH_SUPPORT}" = "yes" ]; then
   18    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} bluez dbussy"
   19  fi
   20  
   21  if [ "${SAMBA_SERVER}" = "yes" ] || [ "$SAMBA_SUPPORT" = "yes" ]; then
   22    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} samba"
   23  fi
   24  
   25  if [ "${SIMPLE_HTTP_SERVER}" = "yes" ]; then
   26    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} simple-http-server"
   27  fi
   28  
   29  if [ "${OPENVPN_SUPPORT}" = "yes" ]; then
   30    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} openvpn"
   31  fi
   32  
   33  if [ "${WIREGUARD_SUPPORT}" = "yes" ]; then
   34    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} wireguard-tools"
   35  fi
   36  
   37  if [ "${ZEROTIER_SUPPORT}" = "yes" ]; then
   38    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} zerotier-one"
   39  fi
   40  
   41  # nss needed by inputstream.adaptive, chromium etc.
   42  if [ "${TARGET_ARCH}" = "x86_64" ] || [ "${TARGET_ARCH}" = "arm" ]; then
   43    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} nss"
   44  fi
   45  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2024 JELOS (https://github.com/JustEnoughLinuxOS)
    4  # Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
    5  
    6  . /etc/profile
    7  
    8  export SWAY_HOME=/storage/.config/sway/
    9  export SWAY_CONFIG_KIOSK=/usr/share/sway/config.kiosk
   10  export SWAY_CONFIG_DESKTOP=/usr/share/sway/config.desktop
   11  
   12  if [ ! -d "$SWAY_HOME" ]
   13  then
   14    mkdir $SWAY_HOME
   15  fi
   16  
   17  # Copy base config, we are overwriting any user config
   18  UIMODE=$(get_setting desktop.enabled)
   19  if [ "${UIMODE}" = "1" ]; then
   20      cp $SWAY_CONFIG_DESKTOP $SWAY_HOME/config
   21      # Shouldn't need to mask, but disable wouldn't do it.
   22      systemctl mask essway.service
   23      set_setting desktop.enabled "0"
   24  else
   25      cp $SWAY_CONFIG_KIOSK $SWAY_HOME/config
   26      systemctl unmask essway.service
   27  fi
   28  # get the card number, this may not be a safe way to derive it...
   29  # "Virtual" matches the virtio-gpu connector (card0-Virtual-1) used by VMs
   30  # (QEMU/QEMU KVM), so GENERIC_X64 finds its GPU; real panels use DP/HDMI/DSI/eDP.
   31  card_no=$(ls /sys/class/drm/ | grep -E "DP|HDMI|DSI|eDP|Virtual" | head -n 1 | cut -b 5)
   32  
   33  env_file=/storage/.config/profile.d/095-sway
   34  
   35  # Write wlroots env vars
   36  rm -f ${env_file}
   37  echo "WLR_DRM_DEVICES=/dev/dri/card${card_no}" >> ${env_file}
   38  echo "WLR_BACKENDS=drm,libinput" >> ${env_file}
   39  
   40  # Scan connectors
   41  card=/sys/class/drm/card${card_no}
   42  connected_cons=()
   43  for connector in ${card}/card${card_no}*/
   44  do
   45      status=$(cat ${connector}/status)
   46      if [ "$status" = "connected" ]; then
   47          # If device has a connected DSI or eDP port, store that device.
   48          if [[ $connector == *"DSI"* || $connector == *"eDP"* ]]; then
   49              internal=$(basename "$connector")
   50              internal=${internal: +6}
   51          fi
   52      # Simply prioritize later connectors, meaning HDMI/DP priority
   53  	con=$(basename $connector)
   54  	con=${con: +6}
   55  	connected_cons+=("$con")
   56      fi
   57  done
   58  
   59  # QEMU/UTM virtio-gpu can present the hardware cursor plane upside down even
   60  # though the primary display plane and pointer coordinates are correct.
   61  if [[ ${con} == Virtual* ]]; then
   62      echo "WLR_NO_HARDWARE_CURSORS=1" >> ${env_file}
   63  fi
   64  
   65  # If dsi / eDP check rotation
   66  if [[ $con == DSI* || $con == eDP* ]]; then
   67      rot=$(cat /sys/class/graphics/fbcon/rotate)
   68      case $rot in
   69          1) angle="90";;
   70          2) angle="180";;
   71          3) angle="270";;
   72          *) angle="0";;
   73      esac
   74  else
   75      # Main output not internal and internal display is connected, then disable it
   76      if [[ -n $internal ]]; then
   77          echo "$internal"
   78          echo "output ${internal} disable" >> "$SWAY_HOME/config"
   79      fi
   80      angle="0"
   81  fi
   82  
   83  if [ "${QUIRK_DEVICE}" = "AYN Thor Lite" ]; then
   84      con="DSI-1"
   85  fi
   86  
   87  # Main output string base
   88  output="output ${con}"
   89  echo "${output} transform ${angle}" >> $SWAY_HOME/config
   90  echo "WLR_CON=${con}" >> ${env_file}
   91  # Force HDMI to 1080p60hz
   92  if [[ $con == HDMI* ]]; then
   93      echo "${output} mode 1920x1080@60Hz" >> "$SWAY_HOME/config"
   94  fi
   95  # check refresh rate
   96  DISPLAY_MODE=$(get_setting system.display_mode)
   97  if [ "${DISPLAY_MODE}" ]; then
   98      # we only need to specify this if we have user set display mode
   99      # if not specified we just use default decided by the panel driver
  100      RR=$(echo ${DISPLAY_MODE} | tr -cd '[[:digit:]].')
  101      if [[ $rot =~ 1|3 ]]; then
  102          echo "${output} mode $(fbheight)x$(fbwidth)@${RR}Hz" >> $SWAY_HOME/config
  103      else
  104          echo "${output} mode $(fbwidth)x$(fbheight)@${RR}Hz" >> $SWAY_HOME/config
  105      fi
  106  fi
  107  echo "${output} bg #000000 solid_color" >> $SWAY_HOME/config
  108  echo "${output} allow_tearing yes" >> $SWAY_HOME/config
  109  echo "${output} max_render_time off" >> $SWAY_HOME/config
  110  
  111  # Retroid Dual Screen Add-on
  112  # Check the display exists first before we do anything
  113  if hexdump -C /sys/class/drm/card0-DP-1/edid | grep -q "Lontium"; then
  114    echo "output DP-1 transform 270" >> $SWAY_HOME/config
  115    echo "output DP-1 bg #000000 solid_color" >> $SWAY_HOME/config
  116    echo "output DP-1 allow_tearing yes"  >> $SWAY_HOME/config
  117    echo "output DP-1 max_render_time off" >> $SWAY_HOME/config
  118    echo "output DP-1 scale 1" >> $SWAY_HOME/config
  119    echo "output DP-1 position 0 0" >> $SWAY_HOME/config
  120    echo "input \"0:0:generic_ft5x06_(a0)\" map_to_output DSI-1" >> $SWAY_HOME/config
  121    echo "input \"0:0:generic_ft5x06_(a0)\" events disabled" >> $SWAY_HOME/config
  122    echo "input \"0:0:generic_ft5x06_(8d)\" map_to_output DSI-1" >> $SWAY_HOME/config
  123    echo "input \"0:0:generic_ft5x06_(8d)\" events disabled" >> $SWAY_HOME/config
  124    echo "input \"8746:1:RetroidPocket_RDS_Touchscreen\" map_to_output DP-1" >> $SWAY_HOME/config
  125    echo "input \"8746:1:RetroidPocket_RDS_Touchscreen\" calibration_matrix 0 1 0 -1 0 1" >> $SWAY_HOME/config
  126    echo 'for_window [app_id="emulationstation"] focus output DP-1' >> $SWAY_HOME/config
  127    con="DP-1"
  128  else
  129    # Any other DP-1 display (AR glasses, external monitor):
  130    # Assign workspace 1 to prefer DP-1 with DSI-1 as fallback.
  131    # Sway automatically moves workspace 1 to DP-1 when it appears
  132    # and back to DSI-1 when it disconnects.
  133    echo "workspace 1 output DP-1 ${con}" >> $SWAY_HOME/config
  134    echo 'for_window [app_id="emulationstation"] move output DP-1' >> $SWAY_HOME/config
  135  fi
  136  
  137  # Start the external display monitor on any device that has DP or HDMI
  138  # hardware where the driver does not emit DRM hotplug uevents.
  139  if ls /sys/class/drm/card*-DP-* /sys/class/drm/card*-HDMI-A-* 2>/dev/null | grep -q .; then
  140    echo "exec /usr/bin/output_monitor" >> $SWAY_HOME/config
  141  fi
  142  
  143  if [ "${QUIRK_DEVICE}" = "AYANEO Pocket DS" ]; then
  144    con="DSI-1"
  145    echo 'for_window [app_id="emulationstation"] focus output DSI-1' >> $SWAY_HOME/config
  146    echo 'for_window [app_id="emulationstation"] reload' >> $SWAY_HOME/config
  147    echo 'input "1046:967:Goodix_Capacitive_TouchScreen" map_to_output DSI-2' >> $SWAY_HOME/config
  148    echo 'input "0:0:generic_ft5x06_(44)" map_to_output DSI-1' >> $SWAY_HOME/config
  149    echo 'output DSI-2 power off' >> $SWAY_HOME/config
  150    echo "exec_always sh -c 'pgrep -x /usr/bin/wvkbd-mobintl >/dev/null && swaymsg output DSI-2 power on'"  >> $SWAY_HOME/config
  151    echo "exec_always swaymsg 'seat seat1 attach 1046:967:Goodix_Capacitive_TouchScreen'" >> $SWAY_HOME/config
  152    echo "exec_always swaymsg 'seat seat1 attach 0:0:generic_ft5x06_(44)'" >> $SWAY_HOME/config
  153    echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] output DSI-2 power on, output DSI-2 transform 270' >> $SWAY_HOME/config
  154  fi
  155  
  156  # Move the secondary window to the second output and apply vertical orientation for applicable cases
  157  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
  158    second_con=$([[ "${connected_cons[0]}" == "$con" ]] && echo "${connected_cons[1]}" || echo "${connected_cons[0]}")
  159    echo "SDL_VIDEO_DISPLAY_PRIORITY=${con},${second_con}" >> ${env_file}
  160    echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] move window to output '"${second_con}" >> $SWAY_HOME/config
  161    echo 'for_window [title="RetroArch.*"] exec /usr/bin/vertical-check' >> $SWAY_HOME/config
  162  
  163    echo 'for_window [app_id="lowerdeck"] floating enable, fullscreen enable, move window to output '"${second_con}" >> $SWAY_HOME/config
  164    echo 'no_focus [app_id="lowerdeck"]' >> $SWAY_HOME/config
  165    # Required for the touch keyboard to both accept inputs on bottom screen and sent those events to the top screen
  166    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat0 attach \"0:0:wlr_virtual_keyboard_v1\"" >> $SWAY_HOME/config
  167    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"0:0:wlr_virtual_keyboard_v1\"" >> $SWAY_HOME/config
  168  fi
  169  
  170  # AYN Thor touchscreen setup
  171  if [ "${QUIRK_DEVICE}" = "AYN Thor" ]; then
  172    echo "output ${second_con} power off" >> $SWAY_HOME/config
  173    echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] output '"${second_con}"' power on' >> $SWAY_HOME/config
  174    echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] exec swaymsg input "0:0:bottom_touchscreen" events enabled' >> $SWAY_HOME/config
  175    echo 'for_window [app_id="emulationstation"] reload' >> $SWAY_HOME/config
  176    echo 'for_window [app_id="emulationstation"] exec "sleep 1 && swaymsg seat seat1 cursor press button1 && swaymsg seat seat1 cursor release button1"' >> $SWAY_HOME/config
  177    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' focus output ${con}, output ${second_con} power off" >> $SWAY_HOME/config
  178    echo 'exec_always swaymsg input "0:0:top_touchscreen" map_to_output DSI-2' >> $SWAY_HOME/config
  179    echo 'exec_always swaymsg input "0:0:bottom_touchscreen" map_to_output DSI-1' >> $SWAY_HOME/config
  180    echo 'exec_always swaymsg input "0:0:bottom_touchscreen" events disabled' >> $SWAY_HOME/config
  181    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"0:0:top_touchscreen\"" >> $SWAY_HOME/config
  182    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"0:0:bottom_touchscreen\"" >> $SWAY_HOME/config
  183    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"4660:22136:InputPlumber_Keyboard\"" >> $SWAY_HOME/config
  184  fi
  185  
  186  if [ "${QUIRK_DEVICE}" = "AYN Thor Lite" ]; then
  187      echo "output ${second_con} power off" >> $SWAY_HOME/config
  188      echo 'input "0:0:top_touchscreen" calibration_matrix 0 -1 1 1 0 0' >> $SWAY_HOME/config
  189      echo 'input "0:0:bottom_touchscreen" calibration_matrix 0 -1 1 1 0 0' >> $SWAY_HOME/config
  190      echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] output '"${second_con}"' power on' >> $SWAY_HOME/config
  191      echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] exec swaymsg input "0:0:bottom_touchscreen" events enabled' >> $SWAY_HOME/config
  192      echo 'for_window [app_id="emulationstation"] reload' >> $SWAY_HOME/config
  193      echo 'for_window [app_id="emulationstation"] exec "sleep 1 && swaymsg seat seat1 cursor press button1 && swaymsg seat seat1 cursor release button1"' >> $SWAY_HOME/config
  194      echo "exec_always swaymsg '[app_id=\"emulationstation\"]' focus output ${con}, output ${second_con} power off" >> $SWAY_HOME/config
  195      echo 'exec_always swaymsg input "0:0:top_touchscreen" map_to_output DSI-1' >> $SWAY_HOME/config
  196      echo 'exec_always swaymsg input "0:0:bottom_touchscreen" map_to_output DSI-2' >> $SWAY_HOME/config
  197      echo 'exec_always swaymsg input "0:0:bottom_touchscreen" events disabled' >> $SWAY_HOME/config
  198      echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"0:0:top_touchscreen\"" >> $SWAY_HOME/config
  199      echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"0:0:bottom_touchscreen\"" >> $SWAY_HOME/config
  200      echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"4660:22136:InputPlumber_Keyboard\"" >> $SWAY_HOME/config
  201  fi
  202  
  203  # AYANEO Pocket S: force primary output to the internal DSI panel.
  204  # Some panel stacks expose extra connectors and sway can pick the wrong one.
  205  if [ "${QUIRK_DEVICE}" = "AYANEO Pocket S 2K" ]; then
  206    if [ -n "${internal}" ]; then
  207      con="${internal}"
  208      echo "output ${con} transform ${angle}" >> $SWAY_HOME/config
  209      echo "output ${con} bg #000000 solid_color" >> $SWAY_HOME/config
  210      echo "output ${con} allow_tearing yes" >> $SWAY_HOME/config
  211      echo "output ${con} max_render_time off" >> $SWAY_HOME/config
  212      echo "WLR_CON=${con}" >> ${env_file}
  213    fi
  214  fi
  215  
  216  # Anbernic RG DS touchscreen setup
  217  if [[ "${QUIRK_DEVICE}" == "Anbernic RG DS" || "${QUIRK_DEVICE}" == "Anbernic RG DS Plus" ]]; then
  218    echo 'for_window [title=".*(Secondary|\[w2\]|Sub|Bottom|Screen 2|GamePad).*"] output '"${second_con}"' power on' >> $SWAY_HOME/config
  219    echo 'for_window [app_id="drastic"] output '"${second_con}"' power on, input "1046:911:Goodix_Capacitive_TouchScreen" map_to_output '"${con}" >> $SWAY_HOME/config
  220    echo 'for_window [app_id="emulationstation"] reload' >> $SWAY_HOME/config
  221    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' focus output ${con}, output ${second_con} power off" >> $SWAY_HOME/config
  222    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 attach \"1046:911:Goodix_Capacitive_TouchScreen\"" >> $SWAY_HOME/config
  223    echo "exec_always swaymsg '[app_id=\"emulationstation\"]' seat seat1 fallback yes" >> $SWAY_HOME/config
  224  fi
  225  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/wayland/compositor/sway/package.mk

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
    3  
    4  PKG_NAME="sway"
    5  PKG_LICENSE="MIT"
    6  PKG_SITE="https://swaywm.org/"
    7  PKG_DEPENDS_TARGET="toolchain bash busybox jq wlr-randr glib wayland wayland-protocols libdrm libxkbcommon libinput cairo pango libjpeg-turbo dbus json-c wlroots gdk-pixbuf swaybg foot bemenu xcb-util-wm xwayland xkbcomp xterm libthai"
    8  PKG_LONGDESC="i3-compatible Wayland compositor"
    9  PKG_TOOLCHAIN="meson"
   10  PKG_PATCH_DIRS+="${DEVICE}"
   11  
   12  case ${DEVICE} in
   13    RK3588)
   14      PKG_VERSION="1.9"
   15      PKG_URL="https://github.com/swaywm/sway/archive/${PKG_VERSION}.zip"
   16      ;;
   17    *)
   18      PKG_VERSION="1.11"
   19      PKG_SHA256="0e37a55b7c3379230e97e1ad982542b75016a0c7d6676198604e557f9b373dae"
   20      PKG_URL="https://github.com/swaywm/sway/releases/download/${PKG_VERSION}/sway-${PKG_VERSION}.tar.gz"
   21      ;;
   22  esac
   23  
   24  # to enable xwayland package: https://gitlab.freedesktop.org/xorg/lib/libxcb-wm/-/tree/master/icccm?<query cut>
   25  
   26  PKG_MESON_OPTS_TARGET="-Ddefault-wallpaper=false \
   27                         -Dzsh-completions=false \
   28                         -Dbash-completions=false \
   29                         -Dfish-completions=false \
   30                         -Dswaybar=true \
   31                         -Dswaynag=true \
   32                         -Dtray=disabled \
   33                         -Dgdk-pixbuf=enabled \
   34                         -Dman-pages=disabled \
   35                         -Dsd-bus-provider=auto"
   36  
   37  pre_configure_target() {
   38    # sway does not build without -Wno flags as all warnings being treated as errors
   39    export TARGET_CFLAGS=$(echo "${TARGET_CFLAGS} -Wno-unused-variable")
   40  }
   41  
   42  post_makeinstall_target() {
   43    mkdir -p ${INSTALL}/usr/lib/sway
   44    mkdir -p ${INSTALL}/usr/bin
   45      cp ${PKG_DIR}/scripts/sway.sh     ${INSTALL}/usr/bin
   46      cp ${PKG_DIR}/scripts/sway-ready  ${INSTALL}/usr/bin
   47      cp ${PKG_DIR}/scripts/sway-config ${INSTALL}/usr/lib/sway
   48    mkdir -p ${INSTALL}/usr/lib/autostart/common
   49      cp ${PKG_DIR}/autostart/111-sway-init     ${INSTALL}/usr/lib/autostart/common
   50      cp ${PKG_DIR}/scripts/sway-touch.sh     ${INSTALL}/usr/bin
   51  
   52    chmod +x ${INSTALL}/usr/bin/sway*
   53  
   54    # install config & wallpaper
   55    mkdir -p ${INSTALL}/usr/share/sway
   56      cp ${PKG_DIR}/config/* ${INSTALL}/usr/share/sway
   57  
   58    # clean up
   59    safe_remove ${INSTALL}/etc
   60    safe_remove ${INSTALL}/usr/share/wayland-sessions
   61  
   62    case ${DEVICE} in
   63      RK3588)
   64        sed -i '/allow_tearing/d' ${INSTALL}/usr/lib/autostart/common/111-sway-init
   65        ;;
   66    esac
   67  }
   68  
   69  post_install() {
   70    enable_service sway-touch.service
   71  }
   72  
```

## fork-own file, whole, at 8ebaf8daad: projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-ready

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # essway's After=sway.service orders process startup, not Wayland readiness.
    6  # Use the same session environment as start_es.sh, including local overrides.
    7  . /etc/profile
    8  
    9  for command in swaymsg wlr-randr jq timeout; do
   10    command -v "$command" >/dev/null 2>&1 || {
   11      echo "sway-ready: required command unavailable: $command" >&2
   12      exit 1
   13    }
   14  done
   15  
   16  case "${WAYLAND_DISPLAY:-wayland-1}" in
   17    /*) display_socket="${WAYLAND_DISPLAY}" ;;
   18    *) display_socket="${XDG_RUNTIME_DIR:-/var/run/0-runtime-dir}/${WAYLAND_DISPLAY:-wayland-1}" ;;
   19  esac
   20  ipc_socket="${SWAYSOCK:-${XDG_RUNTIME_DIR:-/var/run/0-runtime-dir}/sway-ipc.0.sock}"
   21  deadline=$((SECONDS + 15))
   22  
   23  # Socket existence alone can precede the compositor's event loop. Require an
   24  # Wayland round trip, then an active output with a mode before starting SDL.
   25  # Bound each round trip too: a hung compositor must not hold startup forever.
   26  while (( SECONDS < deadline )); do
   27    if [[ -S "$display_socket" ]] &&
   28       timeout -k 1 1 wlr-randr >/dev/null 2>&1 &&
   29       outputs=$(timeout -k 1 1 swaymsg -s "$ipc_socket" -r -t get_outputs 2>/dev/null) &&
   30       jq -e 'type == "array" and any(.[]; .active == true and
   31         (.current_mode.width // 0) > 0 and (.current_mode.height // 0) > 0)'        <<<"$outputs" >/dev/null 2>&1; then
   32      exit 0
   33    fi
   34    sleep 0.1
   35  done
   36  
   37  echo "sway-ready: timed out waiting for a responsive compositor and active output" >&2
   38  exit 1
   39  
```

## the upstream-carried paths that differ from upstream/next (64): `git diff upstream/next 8ebaf8daad -- <path>` (minus is upstream's, plus is the fork's tree)

```
diff --git a/projects/ROCKNIX/packages/apps/commander/package.mk b/projects/ROCKNIX/packages/apps/commander/package.mk
index b5c146c804..8e201af36f 100644
--- a/projects/ROCKNIX/packages/apps/commander/package.mk
+++ b/projects/ROCKNIX/packages/apps/commander/package.mk
@@ -19,11 +19,4 @@ makeinstall_target() {
 
   mkdir -p ${INSTALL}/usr/share/commander
     cp -a ${PKG_BUILD}/res ${INSTALL}/usr/share/commander
-
-  # Non-InputPlumber platforms require custom input mapping
-  case ${DEVICE} in
-    H700|RK3326|RK3399|RK3588|S922X)
-      cp -a ${PKG_DIR}/config/commander.cfg ${INSTALL}/usr/share/commander
-      ;;
-  esac
 }
diff --git a/projects/ROCKNIX/packages/apps/gamepadtester/package.mk b/projects/ROCKNIX/packages/apps/gamepadtester/package.mk
index 634e21b34c..3272cd956c 100644
--- a/projects/ROCKNIX/packages/apps/gamepadtester/package.mk
+++ b/projects/ROCKNIX/packages/apps/gamepadtester/package.mk
@@ -2,8 +2,10 @@
 # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
 
 PKG_NAME="gamepadtester"
+PKG_VERSION="6ac49e67aa98fe3dd5c27f73306d65d4b7a82daa"
+PKG_SHA256="dcba71ac2e673b7714a6cac12661d56e61a2eb861136bf7d74a42165d6a69be6"
 PKG_LICENSE="GPLv3"
-PKG_SITE="https://github.com/ROCKNIX/GamepadTester"
+PKG_SITE="https://github.com/timre13/GamepadTester"
 PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
 PKG_DEPENDS_TARGET="toolchain SDL2 SDL2_gfx gamecontrollerdb"
 PKG_LONGDESC="A simple SDL GUI Gamepad tester"
@@ -11,20 +13,14 @@ PKG_TOOLCHAIN="cmake"
 PKG_PATCH_DIRS+="${DEVICE}"
 
 case ${DEVICE} in
-  SM8650|SM8750|SM8550|SM8250|RK3576|RK3566)
-    PKG_VERSION="b06fef21d7e67aa95bbadb6021ed5a22d2aa6c76"
-    PKG_SHA256="c0a52037946e7b0a7314896a7b4a9316a38eae8253e8cc457385dfb7cd78ac6c"
-  ;;
+  SM8650|SM8750|SM8550|SM8250)
+    PKG_PATCH_DIRS+=" xbox"
+    ;;
   *)
-    PKG_VERSION="6ac49e67aa98fe3dd5c27f73306d65d4b7a82daa"
-    PKG_SHA256="dcba71ac2e673b7714a6cac12661d56e61a2eb861136bf7d74a42165d6a69be6"
-    PKG_SITE="https://github.com/timre13/GamepadTester"
     PKG_PATCH_DIRS+=" legacy"
     ;;
 esac
 
-PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
-
 makeinstall_target() {
   mkdir -p ${INSTALL}/usr/bin
     cp -a ${PKG_BUILD}/.${TARGET_NAME}/gamepad_test ${INSTALL}/usr/bin/gamepad-tester
diff --git a/projects/ROCKNIX/packages/apps/moonlight/package.mk b/projects/ROCKNIX/packages/apps/moonlight/package.mk
index 855ca6bba3..6ba88ec925 100644
--- a/projects/ROCKNIX/packages/apps/moonlight/package.mk
+++ b/projects/ROCKNIX/packages/apps/moonlight/package.mk
@@ -6,8 +6,8 @@ PKG_LICENSE="GPLv3"
 PKG_SITE="https://github.com/moonlight-stream/moonlight-"
 PKG_DEPENDS_TARGET="toolchain opus SDL2 libevdev alsa curl enet avahi ffmpeg"
 PKG_LONGDESC="Moonlight is an open source implementation of NVIDIA's GameStream, as used by the NVIDIA Shield, but built for Linux."
-GET_HANDLER_SUPPORT="git"
-PKG_PATCH_DIRS+=" ${DEVICE}"
+
+PKG_PATCH_DIRS+="${DEVICE}"
 
 if [ "${TARGET_ARCH}" = "null" ]
 then
@@ -31,11 +31,10 @@ then
 else
   PKG_SITE+="embedded"
   PKG_URL="${PKG_SITE}.git"
-  PKG_VERSION="775444287305849ebdf4736c75298ad0713e2d5d"
+  PKG_VERSION="a6bf7154a743d4f74a1b377e730f188352a1b80c"
   PKG_TOOLCHAIN="cmake"
 
   PKG_CMAKE_OPTS_TARGET+=" -DENABLE_CEC=OFF"
-  PKG_CMAKE_OPTS_TARGET+=" -DCMAKE_C_STANDARD_LIBRARIES=-lcrypto"
 
   post_makeinstall_target() {
     mkdir -p ${INSTALL}/usr/config/moonlight
@@ -45,9 +44,9 @@ else
   }
 fi
 
-if [[ "${DEVICE}" == RK3588* ]]
+if [[ "${DEVICE}" == RK* ]]
 then
-  PKG_DEPENDS_TARGET+=" rkmpp"
+  PKG_DEPENDS_TARGET+=" librga rkmpp"
 fi
 
 if [ ! "${OPENGL}" = "no" ]; then
diff --git a/projects/ROCKNIX/packages/apps/portmaster/package.mk b/projects/ROCKNIX/packages/apps/portmaster/package.mk
index 7b0a21fed4..5e81daa974 100644
--- a/projects/ROCKNIX/packages/apps/portmaster/package.mk
+++ b/projects/ROCKNIX/packages/apps/portmaster/package.mk
@@ -2,8 +2,8 @@
 # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 
 PKG_NAME="portmaster"
-PKG_VERSION="2026.06.23-0015"
-PKG_SHA256="772f2d56fc1abfbf79a3404ca78f240776c81c5a5b92786a0a748ae554339b7b"
+PKG_VERSION="2026.09.13-0343"
+PKG_SHA256="2afda49a51b5760c14fda0a12dc543694a6b6a4b4e9ae9d4e11659996382d80a"
 PKG_LICENSE="MIT"
 PKG_SITE="https://github.com/PortsMaster/PortMaster-GUI"
 PKG_URL="${PKG_SITE}/releases/download/${PKG_VERSION}/PortMaster.zip"
diff --git a/projects/ROCKNIX/packages/audio/alsa-lib/package.mk b/projects/ROCKNIX/packages/audio/alsa-lib/package.mk
index 7d89e3688d..7322d484db 100644
--- a/projects/ROCKNIX/packages/audio/alsa-lib/package.mk
+++ b/projects/ROCKNIX/packages/audio/alsa-lib/package.mk
@@ -1,12 +1,31 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/audio/alsa-lib/package.mk
-
-PKG_DEPENDS_TARGET+=" alsa-ucm-conf alsa-topology-conf"
+PKG_NAME="alsa-lib"
+PKG_VERSION="1.2.14"
+PKG_SHA256="be9c88a0b3604367dd74167a2b754a35e142f670292ae47a2fdef27a2ee97a32"
+PKG_LICENSE="GPL"
+PKG_SITE="http://www.alsa-project.org/"
+PKG_URL="https://www.alsa-project.org/files/pub/lib/alsa-lib-${PKG_VERSION}.tar.bz2"
+PKG_DEPENDS_TARGET="toolchain alsa-ucm-conf alsa-topology-conf"
+PKG_LONGDESC="ALSA (Advanced Linux Sound Architecture) is the next generation Linux Sound API."
+PKG_TOOLCHAIN="autotools"
+PKG_BUILD_FLAGS="+pic"
 PKG_PATCH_DIRS+=" ${DEVICE}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--disable-largefile/}"
 
-post_makeinstall_target() {
-  rm -rf ${INSTALL}/usr/bin
+if build_with_debug; then
+  PKG_ALSA_DEBUG=--with-debug
+else
+  PKG_ALSA_DEBUG=--without-debug
+fi
+
+PKG_CONFIGURE_OPTS_TARGET+="${PKG_ALSA_DEBUG} \
+                           --disable-dependency-tracking \
+                           --with-plugindir=/usr/lib/alsa \
+                           --disable-python"
+
+post_configure_target() {
+  sed -i 's/.*PKGLIBDIR.*/#define PKGLIBDIR ""/' include/config.h
 }
+
diff --git a/projects/ROCKNIX/packages/audio/alsa-ucm-conf/package.mk b/projects/ROCKNIX/packages/audio/alsa-ucm-conf/package.mk
index 2aa924a85a..1da5bd9c45 100644
--- a/projects/ROCKNIX/packages/audio/alsa-ucm-conf/package.mk
+++ b/projects/ROCKNIX/packages/audio/alsa-ucm-conf/package.mk
@@ -1,6 +1,19 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
-
-. ${ROOT}/packages/audio/alsa-ucm-conf/package.mk
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)
 
+PKG_NAME="alsa-ucm-conf"
+PKG_VERSION="1.2.13"
+PKG_SHA256="4483b6e3983cca08fd326a73fbae449b5036e444fb1a07c0dee74b504b7ab5af"
+PKG_LICENSE="BSD-3c"
+PKG_SITE="http://www.alsa-project.org/"
+PKG_URL="https://www.alsa-project.org/files/pub/lib/alsa-ucm-conf-${PKG_VERSION}.tar.bz2"
+PKG_LONGDESC="ALSA Use Case Manager configuration (and topologies)"
+PKG_TOOLCHAIN="manual"
 PKG_PATCH_DIRS+=" ${DEVICE}"
+
+makeinstall_target() {
+  mkdir -p ${INSTALL}/usr/share/alsa/
+  cp -PR ${PKG_BUILD}/ucm2 ${INSTALL}/usr/share/alsa/
+  # work around scripts/build removing empty directories, this leads to errors in ucm
+  touch ${INSTALL}/usr/share/alsa/ucm2/conf.virt.d/.dont_remove_this_dir
+}
diff --git a/projects/ROCKNIX/packages/audio/alsa-utils/package.mk b/projects/ROCKNIX/packages/audio/alsa-utils/package.mk
index ba9f4f4179..9a58119720 100644
--- a/projects/ROCKNIX/packages/audio/alsa-utils/package.mk
+++ b/projects/ROCKNIX/packages/audio/alsa-utils/package.mk
@@ -1,9 +1,26 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
+# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 
-. ${ROOT}/packages/audio/alsa-utils/package.mk
+PKG_NAME="alsa-utils"
+PKG_VERSION="1.2.14"
+PKG_SHA256="0794c74d33fed943e7c50609c13089e409312b6c403d6ae8984fc429c0960741"
+PKG_LICENSE="GPL"
+PKG_SITE="http://www.alsa-project.org/"
+PKG_URL="https://www.alsa-project.org/files/pub/utils/alsa-utils-${PKG_VERSION}.tar.bz2"
+PKG_DEPENDS_TARGET="toolchain alsa-lib ncurses systemd alsa-ucm-conf"
+PKG_LONGDESC="This package includes the utilities for ALSA, like alsamixer, aplay, arecord, alsactl, iecset and speaker-test."
+PKG_TOOLCHAIN="autotools"
 
-PKG_DEPENDS_TARGET+=" alsa-ucm-conf"
+PKG_CONFIGURE_OPTS_TARGET="--disable-alsaconf \
+                           --disable-alsaloop \
+                           --enable-alsatest \
+                           --disable-bat \
+                           --disable-dependency-tracking \
+                           --disable-nls \
+                           --disable-rst2man \
+                           --disable-xmlto"
 
 post_makeinstall_target() {
   rm -rf ${INSTALL}/lib ${INSTALL}/var
diff --git a/projects/ROCKNIX/packages/audio/pipewire/package.mk b/projects/ROCKNIX/packages/audio/pipewire/package.mk
index 08e556c9d6..bcbdf5cc51 100644
--- a/projects/ROCKNIX/packages/audio/pipewire/package.mk
+++ b/projects/ROCKNIX/packages/audio/pipewire/package.mk
@@ -2,12 +2,12 @@
 # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
 PKG_NAME="pipewire"
-PKG_VERSION="1.6.8"
-PKG_SHA256="8181172a1d95131f6af8bbc0b98f90b2a33349b042b84c3ce57dd5d11348cc58"
-PKG_LICENSE="MIT"
+PKG_VERSION="1.2.6"
+PKG_SHA256="8d9b4e95dba33d218c760fecbb71672c86a56917f803e96fe6c3af62fa783a95"
+PKG_LICENSE="LGPL"
 PKG_SITE="https://pipewire.org"
 PKG_URL="https://github.com/PipeWire/pipewire/archive/${PKG_VERSION}.tar.gz"
-PKG_DEPENDS_TARGET="toolchain libpthread-stubs dbus glib ncurses alsa-lib pulseaudio systemd libsndfile libusb"
+PKG_DEPENDS_TARGET="toolchain libpthread-stubs dbus ncurses alsa-lib pulseaudio systemd libsndfile libusb"
 PKG_LONGDESC="PipeWire is a server and user space API to deal with multimedia pipeline"
 PKG_PATCH_DIRS+=" ${DEVICE}"
 
@@ -28,9 +28,9 @@ fi
 
 if [ "${VULKAN_SUPPORT}" = "yes" ]; then
   PKG_DEPENDS_TARGET+=" vulkan-loader vulkan-headers"
-  PKG_PIPEWIRE_VULKAN="-Dvulkan=enabled"
-else
-  PKG_PIPEWIRE_VULKAN="-Dvulkan=disabled"
+  PKG_PIPEWIRE_VULKAN+="-Dvulkan=enabled \
+                        -Dx11=disabled \
+                        -Dx11-xfixes=disabled"
 fi
 
 PKG_MESON_OPTS_TARGET="-Ddocs=disabled \
@@ -40,7 +40,7 @@ PKG_MESON_OPTS_TARGET="-Ddocs=disabled \
                        -Dinstalled_tests=disabled \
                        -Dgstreamer=disabled \
                        -Dgstreamer-device-provider=disabled \
-                       -Dlibsystemd=enabled \
+                       -Dsystemd=enabled \
                        -Dsystemd-system-service=enabled \
                        -Dsystemd-user-service=disabled \
                        -Dpipewire-alsa=enabled \
@@ -66,8 +66,6 @@ PKG_MESON_OPTS_TARGET="-Ddocs=disabled \
                        -Dvideotestsrc=disabled \
                        -Dvolume=enabled \
                        ${PKG_PIPEWIRE_VULKAN} \
-                       -Dx11=disabled \
-                       -Dx11-xfixes=disabled \
                        -Dpw-cat=enabled \
                        -Dudev=enabled \
                        -Dudevrulesdir=/usr/lib/udev/rules.d \
@@ -84,50 +82,11 @@ PKG_MESON_OPTS_TARGET="-Ddocs=disabled \
                        -Dlibcanberra=disabled \
                        -Dlegacy-rtkit=false"
 
-case ${DEVICE} in
-  SM6115|SM8550|SM8650|SM8750)
-    PKG_PIPEWIRE_QUANTUM="960"
-    PKG_PIPEWIRE_PULSE_QUANTUM="960"
-    ;;
-  SM8250)
-    PKG_PIPEWIRE_PULSE_QUANTUM="1024"
-    PKG_MESON_OPTS_TARGET+=" -Drtprio-client=99"
-    ;;
-esac
-
 pre_configure_target() {
   export TARGET_CFLAGS="${TARGET_CFLAGS} -Wno-error=float-conversion"
   export TARGET_LDFLAGS="${TARGET_LDFLAGS} -lncursesw -ltinfow"
 }
 
-post_makeinstall_target() {
-  cp ${PKG_DIR}/system.d/pipewire-pulse.service ${PKG_DIR}/system.d/pipewire-pulse.socket \
-     ${INSTALL}/usr/lib/systemd/system
-
-  mkdir -p ${INSTALL}/usr/share/dbus-1/system.d
-    cp ${PKG_DIR}/config/pipewire-pulse-dbus.conf ${INSTALL}/usr/share/dbus-1/system.d
-
-  if [ -n "${PKG_PIPEWIRE_QUANTUM}" ]; then
-    mkdir -p ${INSTALL}/usr/share/pipewire/pipewire.conf.d
-    cat >${INSTALL}/usr/share/pipewire/pipewire.conf.d/50-rocknix-latency.conf <<EOF
-context.properties = {
-    default.clock.min-quantum = ${PKG_PIPEWIRE_QUANTUM}
-}
-EOF
-  fi
-
-  if [ -n "${PKG_PIPEWIRE_PULSE_QUANTUM}" ]; then
-    mkdir -p ${INSTALL}/usr/share/pipewire/pipewire-pulse.conf.d
-    cat >${INSTALL}/usr/share/pipewire/pipewire-pulse.conf.d/50-rocknix-latency.conf <<EOF
-pulse.properties = {
-    pulse.min.req     = ${PKG_PIPEWIRE_PULSE_QUANTUM}/48000
-    pulse.min.frag    = ${PKG_PIPEWIRE_PULSE_QUANTUM}/48000
-    pulse.min.quantum = ${PKG_PIPEWIRE_PULSE_QUANTUM}/48000
-}
-EOF
-  fi
-}
-
 post_install() {
   add_user pipewire x 982 980 "pipewire-daemon" "/var/run/pipewire" "/bin/sh"
   add_group pipewire 980
diff --git a/projects/ROCKNIX/packages/audio/pipewire/system.d/pipewire-pulse.service b/projects/ROCKNIX/packages/audio/pipewire/system.d/pipewire-pulse.service
index 4fa047a8ba..720c70450d 100644
--- a/projects/ROCKNIX/packages/audio/pipewire/system.d/pipewire-pulse.service
+++ b/projects/ROCKNIX/packages/audio/pipewire/system.d/pipewire-pulse.service
@@ -4,8 +4,6 @@ Requires=pipewire-pulse.socket
 After=pipewire.service wireplumber.service
 
 [Service]
-MemoryLow=12M
-OOMScoreAdjust=-500
 User=root
 Type=simple
 ExecStart=/usr/bin/pipewire-pulse
diff --git a/projects/ROCKNIX/packages/audio/wireplumber/package.mk b/projects/ROCKNIX/packages/audio/wireplumber/package.mk
index af034c0881..2a819a4f96 100644
--- a/projects/ROCKNIX/packages/audio/wireplumber/package.mk
+++ b/projects/ROCKNIX/packages/audio/wireplumber/package.mk
@@ -2,8 +2,8 @@
 # Copyright (C) 2022-present Team LibreELEC (https://libreelec.tv)
 
 PKG_NAME="wireplumber"
-PKG_VERSION="0.5.15"
-PKG_SHA256="baa121bc918df5fa0e0e70755bb1c99ffab0ab107225ecf99aa470e2c6ba5e7b"
+PKG_VERSION="0.5.7"
+PKG_SHA256="8cd43a582f68368ee5a915e97bf9dadc44d2dfe8c7bb4f96bb7b40ea2ed7848f"
 PKG_LICENSE="MIT"
 PKG_SITE="https://gitlab.freedesktop.org/pipewire/wireplumber"
 PKG_URL="https://gitlab.freedesktop.org/pipewire/wireplumber/-/archive/${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}.tar.gz"
diff --git a/projects/ROCKNIX/packages/compat/fex-emu/package.mk b/projects/ROCKNIX/packages/compat/fex-emu/package.mk
index da0d9ca7e2..ba6541009b 100644
--- a/projects/ROCKNIX/packages/compat/fex-emu/package.mk
+++ b/projects/ROCKNIX/packages/compat/fex-emu/package.mk
@@ -2,7 +2,7 @@
 # Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
 
 PKG_NAME="fex-emu"
-PKG_VERSION="14c92681f4d62cf84d901460e0358de09c8847a7"
+PKG_VERSION="e869aa644a16e4332cdc15c1ea0b4d13d482385d"
 PKG_LICENSE="MIT"
 PKG_SITE="https://github.com/FEX-Emu/FEX"
 PKG_URL="https://github.com/FEX-Emu/FEX.git"
@@ -89,12 +89,6 @@ make_target() {
       ;;
   esac
 
-  # thunkgen host parse headers, which the guest parse's later --sysroot overrides
-  local cxxdir
-  cxxdir=$(ls -d "${TOOLCHAIN}/${TARGET_NAME}/include/c++/"* | sort -V | tail -n1)
-  # --target keeps x86_64 build hosts from parsing the aarch64 sysroot as x86_64
-  export THUNKGEN_EXTRA_FLAGS="--target=${TARGET_NAME} --sysroot ${SYSROOT_PREFIX} -isystem ${cxxdir} -isystem ${cxxdir}/${TARGET_NAME}"
-
   local -a tgt_opts=(
     -G Ninja
     -S "${PKG_BUILD}"
diff --git a/projects/ROCKNIX/packages/compress/libzip/package.mk b/projects/ROCKNIX/packages/compress/libzip/package.mk
index 5799781f7c..e2cb06a8b1 100644
--- a/projects/ROCKNIX/packages/compress/libzip/package.mk
+++ b/projects/ROCKNIX/packages/compress/libzip/package.mk
@@ -1,12 +1,12 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/addons/addon-depends/libzip/package.mk
-
-PKG_DEPENDS_TARGET+=" gnutls openssl zstd"
-PKG_CMAKE_OPTS_TARGET="${PKG_CMAKE_OPTS_TARGET/-DENABLE_GNUTLS=OFF/-DENABLE_GNUTLS=ON}"
-PKG_CMAKE_OPTS_TARGET="${PKG_CMAKE_OPTS_TARGET/-DENABLE_OPENSSL=OFF/-DENABLE_OPENSSL=ON}"
-PKG_CMAKE_OPTS_TARGET="${PKG_CMAKE_OPTS_TARGET/-DBUILD_SHARED_LIBS=OFF/-DBUILD_SHARED_LIBS=ON}"
-PKG_CMAKE_OPTS_TARGET="${PKG_CMAKE_OPTS_TARGET/-DENABLE_ZSTD=OFF/-DENABLE_ZSTD=ON}"
-
-unset -f post_makeinstall_target
+PKG_NAME="libzip"
+PKG_VERSION="1.11.1"
+PKG_SHA256="721e0e4e851073b508c243fd75eda04e4c5006158a900441de10ce274cc3b633"
+PKG_LICENSE="GPL"
+PKG_SITE="https://libzip.org/download"
+PKG_URL="${PKG_SITE}/${PKG_NAME}-${PKG_VERSION}.tar.xz"
+PKG_DEPENDS_TARGET="toolchain zlib gnutls openssl"
+PKG_LONGDESC="A C library for reading, creating, and modifying zip archives."
diff --git a/projects/ROCKNIX/packages/compress/xz/package.mk b/projects/ROCKNIX/packages/compress/xz/package.mk
index 8e52098cba..f156fe0f74 100644
--- a/projects/ROCKNIX/packages/compress/xz/package.mk
+++ b/projects/ROCKNIX/packages/compress/xz/package.mk
@@ -1,13 +1,23 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
-
-. ${ROOT}/packages/compress/xz/package.mk
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
+# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 
+PKG_NAME="xz"
+PKG_VERSION="5.8.1"
+PKG_SHA256="0b54f79df85912504de0b14aec7971e3f964491af1812d83447005807513cd9e"
+PKG_LICENSE="GPL"
+PKG_SITE="https://tukaani.org/xz/"
+PKG_URL="https://github.com/tukaani-project/xz/releases/download/v${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}.tar.xz"
 PKG_DEPENDS_HOST="ccache:host"
+PKG_DEPENDS_TARGET="toolchain"
+PKG_LONGDESC="A free general-purpose data compression software with high compression ratio."
 PKG_BUILD_FLAGS="+pic +pic:host"
+PKG_TOOLCHAIN="configure"
 
-PKG_CONFIGURE_OPTS_HOST="--disable-shared \
-                         --enable-static \
+# never build shared or k0p happens when building
+# on fedora due to host selinux/liblzma
+PKG_CONFIGURE_OPTS_HOST="--disable-shared --enable-static \
                          --disable-lzmadec \
                          --disable-lzmainfo \
                          --enable-lzma-links \
@@ -16,8 +26,8 @@ PKG_CONFIGURE_OPTS_HOST="--disable-shared \
                          --enable-symbol-versions=no"
 
 PKG_CONFIGURE_OPTS_TARGET="--enable-shared \
-                           --disable-static \
-                           --enable-symbol-versions=yes"
+                          --disable-static \
+                          --enable-symbol-versions=yes"
 
 post_makeinstall_target() {
   rm -rf ${INSTALL}/usr/bin
diff --git a/projects/ROCKNIX/packages/devel/boost/package.mk b/projects/ROCKNIX/packages/devel/boost/package.mk
index 57f9f819ff..56f7627876 100644
--- a/projects/ROCKNIX/packages/devel/boost/package.mk
+++ b/projects/ROCKNIX/packages/devel/boost/package.mk
@@ -1,33 +1,69 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
+# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 
-. ${ROOT}/packages/devel/boost/package.mk
+PKG_NAME="boost"
+PKG_VERSION="1.86.0"
+PKG_SHA256="1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b"
+PKG_LICENSE="OSS"
+PKG_SITE="http://www.boost.org/"
+PKG_URL="https://archives.boost.io/release/${PKG_VERSION}/source/${PKG_NAME}_${PKG_VERSION//./_}.tar.bz2"
+PKG_DEPENDS_HOST="toolchain:host"
+PKG_DEPENDS_TARGET="toolchain boost:host Python3 zlib bzip2"
+PKG_LONGDESC="boost: Peer-reviewed STL style libraries for C++"
+PKG_TOOLCHAIN="manual"
+PKG_BUILD_FLAGS="+pic"
+PKG_B2_PARAM=" binary-format=elf link=static threading=multi toolset=gcc "
+if [ "${TARGET_ARCH}" = "aarch64" ]; then
+	PKG_B2_PARAM+=" abi=aapcs address-model=64 architecture=arm "
+fi
 
-PKG_DEPENDS_TARGET+=" icu"
+make_host() {
+  cd tools/build/src/engine
+    sh build.sh
+}
 
-makeinstall_target() {
-  local b2_arch=""
-  if [ "${TARGET_ARCH}" = "aarch64" ]; then
-    b2_arch="abi=aapcs address-model=64 architecture=arm"
-  fi
+makeinstall_host() {
+  mkdir -p ${TOOLCHAIN}/bin
+    cp b2 ${TOOLCHAIN}/bin
+}
+
+pre_configure_target() {
+  export CFLAGS="${CFLAGS} -I${SYSROOT_PREFIX}/usr/include/${PKG_PYTHON_VERSION}"
+  export CXXFLAGS="${CXXFLAGS} -I${SYSROOT_PREFIX}/usr/include/${PKG_PYTHON_VERSION}"
+}
+
+configure_target() {
+  sh bootstrap.sh --prefix=/usr \
+                  --with-bjam=${TOOLCHAIN}/bin/b2 \
+                  --with-python=${TOOLCHAIN}/bin/python \
+                  --with-python-root=${SYSROOT_PREFIX}/usr
 
-  ${TOOLCHAIN}/bin/b2 -d2 --ignore-site-config \
-                      --layout=system \
-                      --prefix=${SYSROOT_PREFIX}/usr \
-                      --toolset=gcc link=static \
-                      binary-format=elf threading=multi ${b2_arch} \
-                      --with-chrono \
-                      --with-context \
-                      --with-date_time \
-                      --with-filesystem \
-                      --with-iostreams \
-                      --with-locale \
-                      --with-nowide \
-                      --with-program_options \
-                      --with-python \
-                      --with-random \
-                      --with-regex -sICU_PATH="${SYSROOT_PREFIX}/usr" \
-                      --with-serialization \
-                      --with-thread \
-                      install
+  echo "using gcc : $(${CC} -v 2>&1  | tail -n 1 |awk '{print $3}') : ${CXX}  : <compileflags>\"${CFLAGS}\" <linkflags>\"${LDFLAGS}\" ;" \
+    > tools/build/src/user-config.jam
+  echo "using python : ${PKG_PYTHON_VERSION/#python} : ${TOOLCHAIN} : ${SYSROOT_PREFIX}/usr/include : ${SYSROOT_PREFIX}/usr/lib ;" \
+    >> tools/build/src/user-config.jam
+}
+makeinstall_target() {
+  ln -sf ${TOOLCHAIN}/bin/b2 ${TOOLCHAIN}/bin/bjam
+  ${TOOLCHAIN}/bin/bjam -d2 --ignore-site-config \
+                          ${PKG_B2_PARAM} \
+                          --layout=system \
+                          --prefix=${SYSROOT_PREFIX}/usr \
+                          --with-chrono \
+                          --with-date_time \
+                          --with-filesystem \
+                          --with-iostreams \
+                          --with-program_options \
+                          --with-python \
+                          --with-locale \
+                          --with-random \
+                          --with-regex -sICU_PATH="${SYSROOT_PREFIX}/usr" \
+                          --with-serialization \
+                          --with-system \
+                          --with-thread \
+                          --with-nowide \
+			  --with-context \
+                          install
 }
diff --git a/projects/ROCKNIX/packages/devel/glibc/package.mk b/projects/ROCKNIX/packages/devel/glibc/package.mk
index 73070f872e..7dc225296b 100644
--- a/projects/ROCKNIX/packages/devel/glibc/package.mk
+++ b/projects/ROCKNIX/packages/devel/glibc/package.mk
@@ -3,19 +3,16 @@
 # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
 
 PKG_NAME="glibc"
-PKG_VERSION="2.44"
-PKG_SHA256="37f600f2bef3c5e8300147059568b2a2e40a7ad6ccc65ce942556d49429cc667"
-PKG_LICENSE="LGPL-2.1-or-later"
+PKG_VERSION="2.41"
+PKG_SHA256="a5a26b22f545d6b7d7b3dd828e11e428f24f4fac43c934fb071b6a7d0828e901"
+PKG_LICENSE="GPL"
 PKG_SITE="https://www.gnu.org/software/libc/"
 PKG_URL="https://ftp.gnu.org/pub/gnu/glibc/${PKG_NAME}-${PKG_VERSION}.tar.xz"
-# ROCKNIX: pigz:host added
 PKG_DEPENDS_TARGET="ccache:host autotools:host linux:host gcc:bootstrap pigz:host Python3:host"
 PKG_DEPENDS_INIT="glibc"
 PKG_LONGDESC="The Glibc package contains the main C library."
-# ROCKNIX: force bfd, no gold
 PKG_BUILD_FLAGS="+bfd -gold"
 
-# ROCKNIX: lowest kernel across supported devices (RK3588 runs a 6.1 BSP)
 case "${DEVICE}" in
   RK3588)
     OPT_ENABLE_KERNEL=6.1.0
@@ -25,6 +22,12 @@ case "${DEVICE}" in
     ;;
 esac
 
+case ${TARGET_ARCH} in
+  arm|aarch64)
+    PKG_PATCH_DIRS="widevine-arm"
+    ;;
+esac
+
 PKG_CONFIGURE_OPTS_TARGET="BASH_SHELL=/bin/sh \
                            ac_cv_path_PERL=no \
                            ac_cv_prog_MAKEINFO= \
@@ -46,9 +49,6 @@ PKG_CONFIGURE_OPTS_TARGET="BASH_SHELL=/bin/sh \
                            --disable-nscd \
                            --disable-timezone-tools"
 
-# ROCKNIX: new-compiler warning churn must not break the build
-PKG_CONFIGURE_OPTS_TARGET+=" --disable-werror"
-
 if build_with_debug; then
   PKG_CONFIGURE_OPTS_TARGET+=" --enable-debug"
 else
@@ -60,10 +60,7 @@ post_unpack() {
 }
 
 pre_configure_target() {
-  # Filter out some problematic *FLAGS
-  # ROCKNIX: build glibc at -O3
-  export CFLAGS=$(echo ${CFLAGS} | sed -e "s|-ffast-math||g")
-  export CFLAGS=$(echo ${CFLAGS} | sed -e "s|-Ofast|-O3|g")
+# Filter out some problematic *FLAGS
   export CFLAGS=$(echo ${CFLAGS} | sed -e "s|-O.|-O3|g")
 
   export CFLAGS=$(echo ${CFLAGS} | sed -e "s|-Wunused-but-set-variable||g")
@@ -73,8 +70,6 @@ pre_configure_target() {
     export CFLAGS=$(echo ${CFLAGS} | sed -e "s|${PROJECT_CFLAGS}||g")
   fi
 
-  export LDFLAGS=$(echo ${LDFLAGS} | sed -e "s|-ffast-math||g")
-  export LDFLAGS=$(echo ${LDFLAGS} | sed -e "s|-Ofast|-O3|g")
   export LDFLAGS=$(echo ${LDFLAGS} | sed -e "s|-O.|-O3|g")
 
   export LDFLAGS=$(echo ${LDFLAGS} | sed -e "s|-Wl,--as-needed||")
@@ -113,14 +108,12 @@ post_makeinstall_target() {
     cp -a ${INSTALL}/usr/share/i18n/locales ${INSTALL}/.noinstall
     mv ${INSTALL}/usr/share/i18n/charmaps ${INSTALL}/.noinstall
 
-  # ROCKNIX: keep all glibc programs (no GLIBC_INCLUDE_BIN cleanup)
-
   safe_remove ${INSTALL}/usr/lib/audit
   safe_remove ${INSTALL}/usr/lib/glibc
   safe_remove ${INSTALL}/usr/lib/*.o
   safe_remove ${INSTALL}/var
 
-  # add UTF-8 charmap
+# add UTF-8 charmap
   mkdir -p ${INSTALL}/usr/share/i18n/charmaps
     cp -PR ${INSTALL}/.noinstall/charmaps/UTF-8.gz ${INSTALL}/usr/share/i18n/charmaps
 
@@ -131,12 +124,11 @@ post_makeinstall_target() {
       cp -PR ${PKG_BUILD}/localedata/locales/POSIX ${INSTALL}/usr/share/i18n/locales
   fi
 
-  # create default configs
+# create default configs
   mkdir -p ${INSTALL}/etc
     cp ${PKG_DIR}/config/nsswitch-target.conf ${INSTALL}/etc/nsswitch.conf
     cp ${PKG_DIR}/config/host.conf ${INSTALL}/etc
     cp ${PKG_DIR}/config/gai.conf ${INSTALL}/etc
-    # ROCKNIX: writable ld.so.cache location
     cp ${PKG_DIR}/config/ld.so.conf ${INSTALL}/etc
 
   ln -sf /storage/.cache/ld.so.cache ${INSTALL}/etc/ld.so.cache
@@ -182,7 +174,7 @@ makeinstall_init() {
 }
 
 post_makeinstall_init() {
-  # create default configs
+# create default configs
   mkdir -p ${INSTALL}/etc
     cp ${PKG_DIR}/config/nsswitch-init.conf ${INSTALL}/etc/nsswitch.conf
 }
diff --git a/projects/ROCKNIX/packages/devel/json-glib/package.mk b/projects/ROCKNIX/packages/devel/json-glib/package.mk
index d96413d028..299eeac4a0 100644
--- a/projects/ROCKNIX/packages/devel/json-glib/package.mk
+++ b/projects/ROCKNIX/packages/devel/json-glib/package.mk
@@ -1,6 +1,16 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/devel/json-glib/package.mk
+PKG_NAME="json-glib"
+PKG_VERSION="1.10.0"
+PKG_SHA256="447890f9de2a04c312871768208f6c8aeec4069392af7605bc77e61165dcb374"
+PKG_LICENSE="LGPL-2.1"
+PKG_SITE="https://github.com/GNOME/json-glib"
+PKG_URL="https://github.com/GNOME/json-glib/archive/${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain glib glib:host"
+PKG_LONGDESC="JSON-GLib implements a full suite of JSON-related tools using GLib and GObject."
 
-PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} glib:host"
+PKG_MESON_OPTS_TARGET="-Dintrospection=disabled \
+                       -Dgtk_doc=disabled \
+                       -Dman=false \
+                       -Dtests=false"
diff --git a/projects/ROCKNIX/packages/devel/ncurses/package.mk b/projects/ROCKNIX/packages/devel/ncurses/package.mk
index 20ca9eeb79..4024b29258 100644
--- a/projects/ROCKNIX/packages/devel/ncurses/package.mk
+++ b/projects/ROCKNIX/packages/devel/ncurses/package.mk
@@ -1,30 +1,98 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
+# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 
-. ${ROOT}/packages/devel/ncurses/package.mk
+PKG_NAME="ncurses"
+PKG_VERSION="6.5"
+PKG_SHA256="136d91bc269a9a5785e5f9e980bc76ab57428f604ce3e5a5a90cebc767971cc6"
+PKG_LICENSE="MIT"
+PKG_SITE="http://www.gnu.org/software/ncurses/"
+PKG_URL="http://invisible-mirror.net/archives/ncurses/ncurses-${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_HOST="ccache:host"
+PKG_DEPENDS_TARGET="autotools:host gcc:host zlib ncurses:host"
+PKG_LONGDESC="A library is a free software emulation of curses in System V Release 4.0, and more."
+PKG_BUILD_FLAGS="+pic"
 
-PKG_URL="https://ftpmirror.gnu.org/ncurses/ncurses-${PKG_VERSION}.tar.gz"
+PKG_CONFIGURE_OPTS_TARGET="--without-ada \
+                           --without-cxx \
+                           --without-cxx-binding \
+                           --disable-db-install \
+                           --without-manpages \
+                           --without-progs \
+                           --without-tests \
+                           --with-shared \
+                           --with-normal \
+                           --without-debug \
+                           --without-profile \
+                           --with-termlib \
+                           --without-ticlib \
+                           --without-gpm \
+                           --without-dbmalloc \
+                           --without-dmalloc \
+                           --disable-rpath \
+                           --disable-database \
+                           --with-fallbacks=linux,screen,xterm,xterm-color,dumb,st-256color \
+                           --with-termpath=/storage/.config/termcap \
+                           --disable-big-core \
+                           --enable-termcap \
+                           --enable-getcap \
+                           --disable-getcap-cache \
+                           --enable-symlinks \
+                           --disable-bsdpad \
+                           --without-rcs-ids \
+                           --enable-ext-funcs \
+                           --disable-const \
+                           --enable-no-padding \
+                           --enable-pc-files \
+                           --with-pkg-config-libdir=/usr/lib/pkgconfig \
+                           --enable-tcap-names \
+                           --without-develop \
+                           --disable-hard-tabs \
+                           --disable-xmc-glitch \
+                           --disable-hashmap \
+                           --disable-safe-sprintf \
+                           --disable-scroll-hints \
+                           --enable-widec \
+                           --disable-echo \
+                           --disable-warnings \
+                           --enable-home-terminfo \
+                           --enable-lib-suffixes \
+                           --disable-assertions \
+                           --enable-leaks \
+                           --enable-sigwinch \
+                           --cache-file=config.cache"
 
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--without-shared/--with-shared}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--without-termlib/--with-termlib}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--disable-sigwinch/}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--disable-tcap-names/--enable-tcap-names}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--enable-hashmap/--disable-hashmap}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--disable-home-terminfo/--enable-home-terminfo}"
-PKG_CONFIGURE_OPTS_TARGET+=" --enable-lib-suffixes"
-PKG_CONFIGURE_OPTS_HOST+=" --without-tests"
+PKG_CONFIGURE_OPTS_HOST="--enable-termcap \
+                         --with-termlib \
+                         --with-shared \
+                         --enable-pc-files \
+                         --without-tests \
+                         --without-manpages"
 
-eval "core_$(declare -f pre_configure_target)"
 pre_configure_target() {
-  core_pre_configure_target
+  cat >config.cache <<EOF
+cf_cv_builtin_bool=yes
+cf_cv_header_stdbool_h=yes
+EOF
+
   CFLAGS="${CFLAGS} -std=gnu17"
 }
 
-eval "core_$(declare -f post_makeinstall_target)"
 post_makeinstall_target() {
-  core_post_makeinstall_target
-  ln -sf libtinfow.a ${SYSROOT_PREFIX}/usr/lib/libtinfo.a
-  ln -sf tinfow.pc ${SYSROOT_PREFIX}/usr/lib/pkgconfig/tinfo.pc
+  local f
+  cp misc/ncurses-config ${TOOLCHAIN}/bin
+  chmod +x ${TOOLCHAIN}/bin/ncurses-config
+  sed -e "s:\(['=\" ]\)/usr:\\1${PKG_ORIG_SYSROOT_PREFIX}/usr:g" -i ${TOOLCHAIN}/bin/ncurses-config
+  rm -f ${TOOLCHAIN}/bin/ncurses6-config
+  rm -rf ${INSTALL}/usr/bin
+  # create links to be compatible with any ncurses include path and lib names
+  ln -sf . ${SYSROOT_PREFIX}/usr/include/ncursesw
+  ln -sf . ${SYSROOT_PREFIX}/usr/include/ncurses
+  for f in form menu ncurses panel tinfo; do
+    ln -sf lib${f}w.a ${SYSROOT_PREFIX}/usr/lib/lib${f}.a
+    ln -sf ${f}w.pc ${SYSROOT_PREFIX}/usr/lib/pkgconfig/${f}.pc
+  done
   cd ${INSTALL}/usr/lib
   for LIB in *w*.so*
   do
diff --git a/projects/ROCKNIX/packages/devel/patchelf/package.mk b/projects/ROCKNIX/packages/devel/patchelf/package.mk
index 29f3301849..5205689e11 100644
--- a/projects/ROCKNIX/packages/devel/patchelf/package.mk
+++ b/projects/ROCKNIX/packages/devel/patchelf/package.mk
@@ -1,6 +1,14 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
-
-. ${ROOT}/packages/devel/patchelf/package.mk
+# SPDX-License-Identifier: GPL-2.0-only
+# Copyright (C) 2023-present Team LibreELEC (https://libreelec.tv)
 
+PKG_NAME="patchelf"
+PKG_VERSION="0.18.0"
+PKG_SHA256="1952b2a782ba576279c211ee942e341748fdb44997f704dd53def46cd055470b"
+PKG_LICENSE="GPL-3.0-or-later"
+PKG_SITE="https://github.com/NixOS/patchelf"
+PKG_URL="https://github.com/NixOS/patchelf/releases/download/${PKG_VERSION}/patchelf-${PKG_VERSION}.tar.bz2"
+PKG_DEPENDS_HOST="autotools:host"
 PKG_DEPENDS_TARGET="toolchain"
+PKG_LONGDESC="A small utility to modify the dynamic linker and RPATH of ELF executables"
+PKG_TOOLCHAIN="autotools"
+PKG_BUILD_FLAGS="-cfg-libs:host"
diff --git a/projects/ROCKNIX/packages/devel/readline/package.mk b/projects/ROCKNIX/packages/devel/readline/package.mk
index 4d2a9486a9..367454ad14 100644
--- a/projects/ROCKNIX/packages/devel/readline/package.mk
+++ b/projects/ROCKNIX/packages/devel/readline/package.mk
@@ -6,5 +6,4 @@
 PKG_CONFIGURE_OPTS_TARGET="bash_cv_wcwidth_broken=no \
                            --enable-shared \
                            --disable-static \
-                           --with-curses \
-                           --with-shared-termcap-library=-ltinfow"
+                           --with-curses"
diff --git a/projects/ROCKNIX/packages/devel/shared-mime-info/package.mk b/projects/ROCKNIX/packages/devel/shared-mime-info/package.mk
index 9fc1bb372d..ebb50f0712 100644
--- a/projects/ROCKNIX/packages/devel/shared-mime-info/package.mk
+++ b/projects/ROCKNIX/packages/devel/shared-mime-info/package.mk
@@ -1,12 +1,32 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/devel/shared-mime-info/package.mk
+PKG_NAME="shared-mime-info"
+PKG_VERSION="2.4"
+PKG_SHA256="32dc32ae39ff1c1bf8434dd3b36770b48538a1772bc0298509d034f057005992"
+PKG_LICENSE="GPL-2.0-only"
+PKG_SITE="https://freedesktop.org/wiki/Software/shared-mime-info/"
+PKG_URL="https://gitlab.freedesktop.org/xdg/${PKG_NAME}/-/archive/${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}.tar.bz2"
+PKG_DEPENDS_HOST="toolchain:host glib:host libxml2:host gettext:host itstool:host"
+PKG_DEPENDS_TARGET="toolchain glib libxml2 gettext shared-mime-info:host"
+PKG_LONGDESC="The shared-mime-info package contains the core database of common types."
+PKG_BUILD_FLAGS="-parallel"
+
+configure_package() {
+  # Sway Support
+  if [ ! "${WINDOWMANAGER}" = "sway" ]; then
+    PKG_BUILD_FLAGS+=" -sysroot"
+  fi
+}
+
+PKG_MESON_OPTS_HOST="-Dupdate-mimedb=false"
+PKG_MESON_OPTS_TARGET="-Dupdate-mimedb=false"
 
 post_makeinstall_target() {
   mkdir -p ${SYSROOT_PREFIX}/usr/lib/pkgconfig
     cp shared-mime-info.pc ${SYSROOT_PREFIX}/usr/lib/pkgconfig
 
+  # Create /usr/share/mime/mime.cache
   if [ "${WINDOWMANAGER}" = "sway" ]; then
     ${TOOLCHAIN}/bin/update-mime-database ${INSTALL}/usr/share/mime
   fi
diff --git a/projects/ROCKNIX/packages/devel/swig/package.mk b/projects/ROCKNIX/packages/devel/swig/package.mk
index da78bc8737..829c79652d 100644
--- a/projects/ROCKNIX/packages/devel/swig/package.mk
+++ b/projects/ROCKNIX/packages/devel/swig/package.mk
@@ -1,8 +1,45 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
-
-. ${ROOT}/packages/devel/swig/package.mk
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
 
+PKG_NAME="swig"
 PKG_VERSION="4.1.1"
 PKG_SHA256="2af08aced8fcd65cdb5cc62426768914bedc735b1c250325203716f78e39ac9b"
-PKG_URL="https://downloads.sourceforge.net/project/swig/swig/swig-${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}.tar.gz"
+PKG_LICENSE="GPL"
+PKG_SITE="http://www.swig.org"
+PKG_URL="${SOURCEFORGE_SRC}/swig/${PKG_NAME}-${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_HOST="ccache:host"
+PKG_LONGDESC="SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages."
+PKG_TOOLCHAIN="configure"
+
+PKG_CONFIGURE_OPTS_HOST="--program-suffix=4.0 \
+                         --with-pcre-prefix=${TOOLCHAIN} \
+                         --with-boost=no \
+                         --without-pcre \
+                         --without-x \
+                         --without-tcl \
+                         --without-python \
+                         --without-python3 \
+                         --without-perl5 \
+                         --without-octave \
+                         --without-java \
+                         --without-gcj \
+                         --without-android \
+                         --without-guile \
+                         --without-mzscheme \
+                         --without-ruby \
+                         --without-php \
+                         --without-ocaml \
+                         --without-pike \
+                         --without-chicken \
+                         --without-csharp \
+                         --without-lua \
+                         --without-allegrocl \
+                         --without-clisp \
+                         --without-r \
+                         --without-go \
+                         --without-d"
+
+post_makeinstall_host() {
+  ln -sf swig4.0 ${TOOLCHAIN}/bin/swig
+}
diff --git a/projects/ROCKNIX/packages/graphics/gdk-pixbuf/package.mk b/projects/ROCKNIX/packages/graphics/gdk-pixbuf/package.mk
index 367dbf2d88..eade5b1f4a 100644
--- a/projects/ROCKNIX/packages/graphics/gdk-pixbuf/package.mk
+++ b/projects/ROCKNIX/packages/graphics/gdk-pixbuf/package.mk
@@ -1,20 +1,31 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2012 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/graphics/gdk-pixbuf/package.mk
+PKG_NAME="gdk-pixbuf"
+PKG_VERSION="2.42.10"
+PKG_SHA256="ee9b6c75d13ba096907a2e3c6b27b61bcd17f5c7ebeab5a5b439d2f2e39fe44b"
+PKG_LICENSE="OSS"
+PKG_SITE="http://www.gtk.org/"
+PKG_URL="https://www.mirrorservice.org/sites/ftp.gnome.org//pub/GNOME/sources/gdk-pixbuf/${PKG_VERSION:0:4}/gdk-pixbuf-${PKG_VERSION}.tar.xz"
+PKG_DEPENDS_TARGET="toolchain glib libjpeg-turbo libpng jasper shared-mime-info tiff zlib"
+PKG_DEPENDS_CONFIG="shared-mime-info"
+PKG_LONGDESC="GdkPixbuf is a a GNOME library for image loading and manipulation."
 
-PKG_DEPENDS_TARGET+=" zlib"
+configure_package() {
+  if [ "${DISPLAYSERVER}" = "x11" ]; then
+    PKG_DEPENDS_TARGET+=" libX11"
+  fi
+}
 
 pre_configure_target() {
   PKG_MESON_OPTS_TARGET="--wrap-mode=nodownload \
-                         -Ddocumentation=false \
+                         -Dgtk_doc=false \
+                         -Ddocs=false \
                          -Dintrospection=disabled \
                          -Dman=false \
                          -Drelocatable=false \
                          -Dinstalled_tests=false \
-                         -Dglycin=disabled \
-                         -Dothers=enabled \
-                         -Dlegacy_xpm=enabled \
                          -Dtests=false"
 
   if [ "${DISPLAYSERVER}" != "x11" ]; then
diff --git a/projects/ROCKNIX/packages/graphics/glew/package.mk b/projects/ROCKNIX/packages/graphics/glew/package.mk
index 46479b507c..97772276d0 100644
--- a/projects/ROCKNIX/packages/graphics/glew/package.mk
+++ b/projects/ROCKNIX/packages/graphics/glew/package.mk
@@ -1,9 +1,14 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
-
-. ${ROOT}/packages/graphics/glew/package.mk
-
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
+
+PKG_NAME="glew"
+PKG_VERSION="2.2.0"
+PKG_SHA256="d4fc82893cfb00109578d0a1a2337fb8ca335b3ceccf97b97e5cc7f08e4353e1"
+PKG_LICENSE="BSD"
+PKG_SITE="http://glew.sourceforge.net/"
+PKG_URL="${SOURCEFORGE_SRC}/glew/glew/${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}.tgz"
 PKG_DEPENDS_TARGET="toolchain"
+PKG_LONGDESC="GLEW - The OpenGL Extension Wrangler Library"
 PKG_TOOLCHAIN="cmake"
 
 PKG_CMAKE_OPTS_TARGET="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
@@ -17,16 +22,14 @@ if [ ! "${OPENGL}" = "no" ]; then
   PKG_DEPENDS_TARGET+=" ${OPENGL} glu libglvnd"
 fi
 
-unset -f make_target makeinstall_target
-
 pre_configure() {
   PKG_CMAKE_SCRIPT=${PKG_BUILD}/build/cmake/CMakeLists.txt
 }
 
 pre_configure_target() {
-  PKG_CMAKE_OPTS_TARGET+=" -DBUILD_UTILS=OFF \
-                           -DGLEW_REGAL=OFF \
-                           -DGLEW_OSMESA=OFF \
-                           -DGLEW_EGL=ON \
-                           -DBUILD_SHARED_LIBS=ON"
+  PKG_CMAKE_OPTS_TARGET+="      -DBUILD_UTILS=OFF \
+				-DGLEW_REGAL=OFF \
+				-DGLEW_OSMESA=OFF \
+				-DGLEW_EGL=ON \
+				-DBUILD_SHARED_LIBS=ON"
 }
diff --git a/projects/ROCKNIX/packages/graphics/libpng/package.mk b/projects/ROCKNIX/packages/graphics/libpng/package.mk
index 79e9bb50a0..4709d9860a 100644
--- a/projects/ROCKNIX/packages/graphics/libpng/package.mk
+++ b/projects/ROCKNIX/packages/graphics/libpng/package.mk
@@ -1,6 +1,36 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
 
-. ${ROOT}/packages/graphics/libpng/package.mk
+PKG_NAME="libpng"
+PKG_VERSION="1.6.40"
+PKG_SHA256="535b479b2467ff231a3ec6d92a525906fb8ef27978be4f66dbe05d3f3a01b3a1"
+PKG_LICENSE="LibPNG2"
+PKG_SITE="http://www.libpng.org/"
+PKG_URL="${SOURCEFORGE_SRC}/libpng/${PKG_NAME}-${PKG_VERSION}.tar.xz"
+PKG_DEPENDS_HOST="zlib:host"
+PKG_DEPENDS_TARGET="toolchain zlib"
+PKG_LONGDESC="An extensible file format for the lossless, portable, well-compressed storage of raster images."
+PKG_TOOLCHAIN="configure"
+PKG_BUILD_FLAGS="+pic +pic:host"
 
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--disable-shared/--enable-shared}"
+PKG_CONFIGURE_OPTS_TARGET="ac_cv_lib_z_zlibVersion=yes \
+                           --enable-static \
+                           --enable-shared"
+
+PKG_CONFIGURE_OPTS_HOST="--enable-static --disable-shared"
+
+pre_configure_host() {
+  export CPPFLAGS="$CPPFLAGS -I${TOOLCHAIN}/include"
+}
+
+pre_configure_target() {
+  export CPPFLAGS="${CPPFLAGS} -I${SYSROOT_PREFIX}/usr/include"
+}
+
+post_makeinstall_target() {
+  sed -e "s:\([\"'= ]\)/usr:\\1${SYSROOT_PREFIX}/usr:g" \
+      -e "s:libs=\"-lpng16\":libs=\"-lpng16 -lz\":g" \
+      -i ${SYSROOT_PREFIX}/usr/bin/libpng*-config
+
+  rm -rf ${INSTALL}/usr/bin
+}
diff --git a/projects/ROCKNIX/packages/graphics/mesa/package.mk b/projects/ROCKNIX/packages/graphics/mesa/package.mk
index b18d2f26e7..a770defd3e 100644
--- a/projects/ROCKNIX/packages/graphics/mesa/package.mk
+++ b/projects/ROCKNIX/packages/graphics/mesa/package.mk
@@ -3,8 +3,8 @@
 # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
 
 PKG_NAME="mesa"
-PKG_VERSION="26.2.4"
-PKG_SHA256="89d4c3bf09fac8968f4198d00a6328e5e0df02f18d4b17b8eedc6b1a5773ae6b"
+PKG_VERSION="26.2.2"
+PKG_SHA256="9b6850189d4b4a595b1718d57d462412090fab820d3e235e2c1d122c1cf9e9bc"
 PKG_LICENSE="OSS"
 PKG_SITE="http://www.mesa3d.org/"
 PKG_URL="https://gitlab.freedesktop.org/mesa/mesa/-/archive/mesa-${PKG_VERSION}/mesa-mesa-${PKG_VERSION}.tar.gz"
diff --git a/projects/ROCKNIX/packages/graphics/vulkan/vulkan-loader/package.mk b/projects/ROCKNIX/packages/graphics/vulkan/vulkan-loader/package.mk
index 31bfef4d2e..6cf1d0457f 100644
--- a/projects/ROCKNIX/packages/graphics/vulkan/vulkan-loader/package.mk
+++ b/projects/ROCKNIX/packages/graphics/vulkan/vulkan-loader/package.mk
@@ -1,19 +1,26 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2018-present Frank Hartung (supervisedthinking (@) gmail.com)
+# Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/graphics/vulkan/vulkan-loader/package.mk
-
-PKG_DEPENDS_TARGET+=" libxcb libX11 libXrandr"
+PKG_NAME="vulkan-loader"
+PKG_VERSION="1.4.347"
+PKG_SHA256="4b6002e4200d59d76bad1058b677fdbfab9abdb2ef3b3856a31026bc445341f0"
+PKG_LICENSE="Apache-2.0"
+PKG_SITE="https://github.com/KhronosGroup/Vulkan-Loader"
+PKG_URL="https://github.com/KhronosGroup/Vulkan-Loader/archive/v${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain Python3:host vulkan-headers libxcb libX11 libXrandr wayland"
+PKG_LONGDESC="Vulkan Installable Client Driver (ICD) Loader."
 
 pre_configure_target() {
   PKG_CMAKE_OPTS_TARGET="-DBUILD_TESTS=OFF \
                          -DCMAKE_BUILD_TYPE=Release"
 
   # GAS / GNU Assembler is only supported by aarch64 & x86_64
-  case $(uname -m) in
-    arm|aarch64)
-      PKG_CMAKE_OPTS_TARGET+=" -DUSE_GAS=OFF"
-      ;;
+  HOST_ARCH=$(uname -m)
+  case ${HOST_ARCH} in
+     arm|aarch64)
+       PKG_CMAKE_OPTS_TARGET+=" -DUSE_GAS=OFF"
+     ;;
   esac
 
   if [ "${DISPLAYSERVER}" = "x11" ]; then
diff --git a/projects/ROCKNIX/packages/graphics/vulkan/vulkan-tools/package.mk b/projects/ROCKNIX/packages/graphics/vulkan/vulkan-tools/package.mk
index 74ffe1d7b3..f839a7c512 100644
--- a/projects/ROCKNIX/packages/graphics/vulkan/vulkan-tools/package.mk
+++ b/projects/ROCKNIX/packages/graphics/vulkan/vulkan-tools/package.mk
@@ -1,7 +1,24 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2018-present Frank Hartung (supervisedthinking (@) gmail.com)
+# Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/graphics/vulkan/vulkan-tools/package.mk
+PKG_NAME="vulkan-tools"
+PKG_VERSION="1.4.347"
+PKG_SHA256="4ed73bd973069633ef2b830c7b9f3ebcb7bc8aaac5783b9e5aa36c888e687a78"
+PKG_LICENSE="Apache-2.0"
+PKG_SITE="https://github.com/KhronosGroup/Vulkan-Tools"
+PKG_URL="https://github.com/KhronosGroup/Vulkan-tools/archive/v${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain vulkan-loader glslang:host Python3:host volk wayland"
+PKG_LONGDESC="This project provides Khronos official Vulkan Tools and Utilities."
+
+configure_package() {
+  # Displayserver Support
+  if [ "${DISPLAYSERVER}" = "x11" ]; then
+    PKG_DEPENDS_TARGET+=" libxcb libX11"
+  elif [ "${DISPLAYSERVER}" = "wl" ]; then
+    PKG_DEPENDS_TARGET+=" wayland"
+  fi
+}
 
 pre_configure_target() {
   PKG_CMAKE_OPTS_TARGET="-DVULKAN_HEADERS_INSTALL_DIR=${SYSROOT_PREFIX}/usr \
@@ -33,3 +50,14 @@ pre_configure_target() {
                              -DCUBE_WSI_SELECTION=DISPLAY"
   fi
 }
+
+pre_make_target() {
+  # Fix cross compiling
+  find ${PKG_BUILD} -name flags.make -exec sed -i  "s:isystem :I:g" \{} \;
+  find ${PKG_BUILD} -name build.ninja -exec sed -i "s:isystem :I:g" \{} \;
+}
+
+post_makeinstall_target() {
+  # Clean up - two graphic test tools are superflous
+  safe_remove ${INSTALL}/usr/bin/vkcubepp
+}
diff --git a/projects/ROCKNIX/packages/graphics/waffle/package.mk b/projects/ROCKNIX/packages/graphics/waffle/package.mk
index a8fede31be..4ca1a3e75a 100644
--- a/projects/ROCKNIX/packages/graphics/waffle/package.mk
+++ b/projects/ROCKNIX/packages/graphics/waffle/package.mk
@@ -1,9 +1,9 @@
 # SPDX-License-Identifier: GPL-2.0-or-later
 # Copyright (C) 2024-present ROCKNIX (https://rocknix.org)
 PKG_NAME="waffle"
-PKG_VERSION="3b20e4d7bccc5471fe54db21e1b75022fa47d7d8"
-PKG_SHA256="47f63cfad51f6f7f8d27f2fde06e1b7aef9376db5db2c7906e51385be8e84deb"
 PKG_LICENSE="BSD"
+PKG_VERSION="5f1f48287e806544d745e9a8f5aed47234c61292"
+PKG_SHA256="4a3584b56fc2bb98466eb64f2578a13b75d67328ae16c95b320fa55cbc6afe00"
 PKG_SITE="https://waffle.freedesktop.org/"
 PKG_URL="https://gitlab.freedesktop.org/mesa/waffle/-/archive/${PKG_VERSION}.tar.gz"
 PKG_DEPENDS_TARGET="toolchain wayland mesa Python3"
@@ -16,8 +16,3 @@ PKG_MESON_OPTS_TARGET+=" -Dwayland=enabled \
                        -Dsurfaceless_egl=enabled \
                        -Dglx=enabled \
                        -Dbuild-examples=false"
-
-pre_configure_target() {
-  # meson reads CMAKE as the cmake program, but setup_toolchain exports a whole command line
-  unset CMAKE
-}
diff --git a/projects/ROCKNIX/packages/graphics/wxwidgets/package.mk b/projects/ROCKNIX/packages/graphics/wxwidgets/package.mk
index 6594f222be..ccbdc50200 100644
--- a/projects/ROCKNIX/packages/graphics/wxwidgets/package.mk
+++ b/projects/ROCKNIX/packages/graphics/wxwidgets/package.mk
@@ -11,5 +11,4 @@ PKG_LONGDESC="wxWidgets is a free and open source cross-platform C++ framework f
 
 pre_configure_target(){
   PKG_CMAKE_OPTS_TARGET+=" -DCMAKE_SYSROOT=${SYSROOT_PREFIX} -DCMAKE_POLICY_VERSION_MINIMUM=3.5"
-  PKG_CMAKE_OPTS_TARGET+=" -DwxUSE_LIBSDL=OFF"
 }
diff --git a/projects/ROCKNIX/packages/lang/lua54/package.mk b/projects/ROCKNIX/packages/lang/lua54/package.mk
index a63dcf25ae..5d5015b494 100644
--- a/projects/ROCKNIX/packages/lang/lua54/package.mk
+++ b/projects/ROCKNIX/packages/lang/lua54/package.mk
@@ -1,8 +1,29 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2022-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/lang/lua54/package.mk
+PKG_NAME="lua54"
+PKG_VERSION="5.4.6"
+PKG_SHA256="7d5ea1b9cb6aa0b59ca3dde1c6adcb57ef83a1ba8e5432c0ecd06bf439b3ad88"
+PKG_LICENSE="MIT"
+PKG_SITE="https://www.lua.org"
+PKG_URL="http://www.lua.org/ftp/lua-${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain"
+PKG_LONGDESC="Lua is a powerful, efficient, lightweight, embeddable scripting language."
 
-post_makeinstall_target() {
-  cp src/lua.hpp ${SYSROOT_PREFIX}/usr/include/lua$(get_pkg_version_maj_min)
+make_target() {
+  make CC=${CC} AR="${AR} rcu" MYCFLAGS="-fPIC" posix
+}
+
+makeinstall_target() {
+  mkdir -p ${SYSROOT_PREFIX}/usr/include/lua$(get_pkg_version_maj_min)
+  cp src/lua.hpp src/lua.h src/luaconf.h src/lualib.h src/lauxlib.h ${SYSROOT_PREFIX}/usr/include/lua$(get_pkg_version_maj_min)
+
+  mkdir -p ${SYSROOT_PREFIX}/usr/lib
+  cp src/liblua.a ${SYSROOT_PREFIX}/usr/lib/liblua$(get_pkg_version_maj_min).a
+
+  mkdir -p ${SYSROOT_PREFIX}/usr/lib/pkgconfig
+  cp ${PKG_DIR}/config/lua54.pc ${SYSROOT_PREFIX}/usr/lib/pkgconfig
+  sed -e "s/@@VERSION@@/${PKG_VERSION}/g" \
+      -e "s/@@VERSION_MM@@/$(get_pkg_version_maj_min)/g" \
+      -i ${SYSROOT_PREFIX}/usr/lib/pkgconfig/lua54.pc
 }
diff --git a/projects/ROCKNIX/packages/lang/nasm/package.mk b/projects/ROCKNIX/packages/lang/nasm/package.mk
index fbc0c3cb26..b698b773db 100644
--- a/projects/ROCKNIX/packages/lang/nasm/package.mk
+++ b/projects/ROCKNIX/packages/lang/nasm/package.mk
@@ -1,6 +1,16 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
+# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/lang/nasm/package.mk
+PKG_NAME="nasm"
+PKG_VERSION="2.16.01"
+PKG_SHA256="c77745f4802375efeee2ec5c0ad6b7f037ea9c87c92b149a9637ff099f162558"
+PKG_LICENSE="BSD"
+PKG_SITE="https://www.nasm.us/"
+PKG_URL="https://gstreamer.freedesktop.org/src/mirror/nasm-${PKG_VERSION}.tar.xz"
+PKG_DEPENDS_HOST="ccache:host"
+PKG_LONGDESC="The Netwide Assembler, NASM, is an 80x86 and x86-64 assembler designed for portability and modularity."
 
-unset PKG_ARCH
+pre_configure_host() {
+  HOST_CONFIGURE_OPTS=$(echo ${HOST_CONFIGURE_OPTS} | sed -e "s|--disable-static||" -e "s|--enable-shared||")
+}
diff --git a/projects/ROCKNIX/packages/misc/modules/package.mk b/projects/ROCKNIX/packages/misc/modules/package.mk
index b8f3b23615..e61021f0d2 100644
--- a/projects/ROCKNIX/packages/misc/modules/package.mk
+++ b/projects/ROCKNIX/packages/misc/modules/package.mk
@@ -11,7 +11,7 @@ PKG_LONGDESC="OS Modules Package"
 PKG_TOOLCHAIN="manual"
 
 case ${DEVICE} in
-  RK3399|RK3588|SM8250|SM8550|SM8650|SM8750|SM4450|SM6115|RK3566|RK3576)
+  RK3399|RK3588|SM8250|SM8550|SM8650|SM8750|SM4450|SM6115)
     PKG_DEPENDS_TARGET+=" gamepadtester qterminal"
     ;;
 esac
diff --git a/projects/ROCKNIX/packages/misc/modules/sources/Mount NFS.sh b/projects/ROCKNIX/packages/misc/modules/sources/Mount NFS.sh
index 00acccb08e..747527fde6 100755
--- a/projects/ROCKNIX/packages/misc/modules/sources/Mount NFS.sh	
+++ b/projects/ROCKNIX/packages/misc/modules/sources/Mount NFS.sh	
@@ -31,7 +31,7 @@ log_msg() {
 # Ensure we cleanup background processes on exit
 cleanup() {
     # Restore cursor
-    printf '\033[?25h' > /dev/tty 2>/dev/null
+    tput cnorm > /dev/tty 2>/dev/null
 }
 trap cleanup EXIT
 
@@ -48,7 +48,7 @@ show_ui_message() {
     local pid_monitor=""
       
     # Hide Cursor for cleaner UI
-    printf '\033[?25l' > /dev/tty 2>/dev/null
+    tput civis > /dev/tty 2>/dev/null
 
     # Force a sane terminal type
     if [[ -z "$TERM" || "$TERM" == "dumb" ]]; then
@@ -102,7 +102,7 @@ show_ui_message() {
     # Clean up the monitor if dialog timed out naturally
     kill $pid_monitor >/dev/null 2>&1
       
-    printf '\033[?25h' > /dev/tty 2>/dev/null
+    tput cnorm > /dev/tty 2>/dev/null
 }
 
 # --- 3. Configuration & Connectivity Checks ---
diff --git a/projects/ROCKNIX/packages/misc/modules/sources/commander.sh b/projects/ROCKNIX/packages/misc/modules/sources/commander.sh
index 024a06484c..438f7c214c 100755
--- a/projects/ROCKNIX/packages/misc/modules/sources/commander.sh
+++ b/projects/ROCKNIX/packages/misc/modules/sources/commander.sh
@@ -8,9 +8,4 @@ set_kill set "commander"
 
 sway_fullscreen "commander" &
 
-PRELUDE="/usr/share/commander/commander.cfg"
-if [ -f "${PRELUDE}" ]; then
-  /usr/bin/commander --config-prelude "${PRELUDE}"
-else
-  /usr/bin/commander
-fi
+/usr/bin/commander
diff --git a/projects/ROCKNIX/packages/multimedia/ffmpeg/package.mk b/projects/ROCKNIX/packages/multimedia/ffmpeg/package.mk
index d7a892a81a..aaf495c8c2 100644
--- a/projects/ROCKNIX/packages/multimedia/ffmpeg/package.mk
+++ b/projects/ROCKNIX/packages/multimedia/ffmpeg/package.mk
@@ -3,16 +3,18 @@
 # Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
 
 PKG_NAME="ffmpeg"
-PKG_LICENSE="LGPL-3.0-or-later"
+PKG_LICENSE="LGPLv2.1+"
 PKG_SITE="https://ffmpeg.org"
 PKG_DEPENDS_TARGET="toolchain zlib bzip2 openssl speex"
 PKG_LONGDESC="FFmpeg is a complete, cross-platform solution to record, convert and stream audio and video."
 
-PKG_VERSION="9.0"
-PKG_SHA256="7f607a00dd0d28a729d5a4811205812eef01cf6ef6155025febb6f36a9062d52"
+PKG_VERSION="7.1.1"
+PKG_SHA256="733984395e0dbbe5c046abda2dc49a5544e7e0e1e2366bba849222ae9e3a03b1"
 PKG_URL="http://ffmpeg.org/releases/ffmpeg-${PKG_VERSION}.tar.xz"
 PKG_PATCH_DIRS="libreelec"
 
+PKG_PATCH_DIRS+=" v4l2-request v4l2-drmprime"
+
 post_unpack() {
   # Fix FFmpeg version
   if [ "${DEVICE}" = "S922X" ]; then
@@ -30,18 +32,13 @@ PKG_FFMPEG_HWACCEL="--enable-hwaccels"
 case ${DEVICE} in
   RK3588*)
     V4L2_SUPPORT=no
-    PKG_DEPENDS_TARGET+=" rkmpp libdrm"
-    PKG_NEED_UNPACK+=" $(get_pkg_directory libdrm)"
-    PKG_FFMPEG_RKMPP="--enable-rkmpp --enable-libdrm"
-  ;;
-  RK3326*|RK3399*)
-    PKG_PATCH_DIRS+=" v4l2-request vf-deinterlace-v4l2m2m"
-  ;;
-  RK*)
-    PKG_PATCH_DIRS+=" v4l2-request detlev vf-deinterlace-v4l2m2m"
   ;;
   *)
-    PKG_PATCH_DIRS+=" v4l2-request"
+    case ${DEVICE} in
+      RK*)
+        PKG_PATCH_DIRS+=" vf-deinterlace-v4l2m2m"
+      ;;
+    esac
   ;;
 esac
 
@@ -63,14 +60,11 @@ if [ "${V4L2_SUPPORT}" = "yes" ]; then
     PKG_DEPENDS_TARGET+=" systemd"
     PKG_NEED_UNPACK+=" $(get_pkg_directory systemd)"
     PKG_FFMPEG_V4L2+=" --enable-libudev --enable-v4l2-request"
-  elif listcontains "${PKG_PATCH_DIRS}" "v4l2-request"; then
+  else
     PKG_FFMPEG_V4L2+=" --disable-libudev --disable-v4l2-request"
   fi
 else
-  PKG_FFMPEG_V4L2="--disable-v4l2_m2m"
-  if listcontains "${PKG_PATCH_DIRS}" "v4l2-request"; then
-    PKG_FFMPEG_V4L2+=" --disable-libudev --disable-v4l2-request"
-  fi
+  PKG_FFMPEG_V4L2="--disable-v4l2_m2m --disable-libudev --disable-v4l2-request"
 fi
 
 if [ "${VAAPI_SUPPORT}" = "yes" ]; then
@@ -111,6 +105,12 @@ if [ "${TARGET_ARCH}" = "x86_64" ]; then
   PKG_DEPENDS_TARGET+=" nasm:host"
 fi
 
+case ${DEVICE} in
+  RK*)
+    PKG_DEPENDS_TARGET+=" rkmpp"
+  ;;
+esac
+
 if target_has_feature "(neon|sse)"; then
   PKG_DEPENDS_TARGET+=" dav1d"
   PKG_NEED_UNPACK+=" $(get_pkg_directory dav1d)"
@@ -164,6 +164,7 @@ configure_target() {
               --enable-avcodec \
               --enable-avformat \
               --enable-swscale \
+              --enable-postproc \
               --enable-avfilter \
               --disable-devices \
               --enable-pthreads \
@@ -173,7 +174,6 @@ configure_target() {
               --enable-swscale-alpha \
               --disable-small \
               ${PKG_FFMPEG_V4L2} \
-              ${PKG_FFMPEG_RKMPP} \
               ${PKG_FFMPEG_VAAPI} \
               ${PKG_FFMPEG_VDPAU} \
               --enable-runtime-cpudetect \
diff --git a/projects/ROCKNIX/packages/multimedia/libvpx/package.mk b/projects/ROCKNIX/packages/multimedia/libvpx/package.mk
index 44d03ed1db..7426e54845 100644
--- a/projects/ROCKNIX/packages/multimedia/libvpx/package.mk
+++ b/projects/ROCKNIX/packages/multimedia/libvpx/package.mk
@@ -3,11 +3,11 @@
 # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 
 PKG_NAME="libvpx"
-PKG_VERSION="1.16.0"
-PKG_SHA256="7a479a3c66b9f5d5542a4c6a1b7d3768a983b1e5c14c60a9396edc9b649e015c"
-PKG_LICENSE="BSD-3-Clause"
+PKG_VERSION="df655cf4fb6c2a23b964544acd015cc715752830" # 1.13.1
+PKG_SHA256="1d1094ad5a8058b3015ee40bfb1bfa8e0bd68d655f76ac852315b98e365218bd"
+PKG_LICENSE="BSD"
 PKG_SITE="https://github.com/webmproject/libvpx"
-PKG_URL="${PKG_SITE}/archive/v${PKG_VERSION}.tar.gz"
+PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
 PKG_DEPENDS_HOST="toolchain nasm:host"
 PKG_DEPENDS_TARGET="toolchain"
 PKG_LONGDESC="WebM VP8/VP9 Codec"
@@ -77,7 +77,5 @@ configure_target() {
 }
 
 post_makeinstall_target() {
-  local vpx_lib=$(basename "$(readlink -f "${INSTALL}/usr/lib/libvpx.so")")
-  [ -f "${INSTALL}/usr/lib/${vpx_lib}" ] || die "libvpx: no installed library to point libvpx.so.6 at"
-  ln -sfv "${vpx_lib}" "${INSTALL}/usr/lib/libvpx.so.6"
+  ln -sf libvpx.so.8.0.1 ${INSTALL}/usr/lib/libvpx.so.6
 }
diff --git a/projects/ROCKNIX/packages/multimedia/mpv/package.mk b/projects/ROCKNIX/packages/multimedia/mpv/package.mk
index 3efdd2c254..4e8ca8a850 100644
--- a/projects/ROCKNIX/packages/multimedia/mpv/package.mk
+++ b/projects/ROCKNIX/packages/multimedia/mpv/package.mk
@@ -9,13 +9,15 @@ PKG_SHA256="068960e89211f2adc80af03f637fa393fb5e407d3dd23592c8fe8c5490bb7ae4"
 PKG_LICENSE="GPLv2+"
 PKG_SITE="https://github.com/mpv-player/mpv"
 PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
-PKG_DEPENDS_TARGET="toolchain ffmpeg SDL2 luajit libass libplacebo libdrm"
+PKG_DEPENDS_TARGET="toolchain ffmpeg SDL2 luajit libass libplacebo"
 PKG_LONGDESC="Video player based on MPlayer/mplayer2 https://mpv.io"
 
 if [ "${OPENGLES_SUPPORT}" = yes ]; then
   PKG_DEPENDS_TARGET+=" ${OPENGLES}"
-  PKG_MESON_OPTS_TARGET+=" -Dgl=enabled -Degl=enabled"
-elif [ "${OPENGL_SUPPORT}" = "yes" ]; then
+  PKG_MESON_OPTS_TARGET+=" -Dgl=disabled -Degl=enabled"
+fi
+
+if [ "${OPENGL_SUPPORT}" = "yes" ]; then
   PKG_DEPENDS_TARGET+=" ${OPENGL} glu libglvnd"
   PKG_MESON_OPTS_TARGET+=" -Dgl=enabled -Degl=disabled"
 fi
@@ -26,33 +28,14 @@ else
   PKG_MESON_OPTS_TARGET+=" -Dwayland=disabled"
 fi
 
-PKG_MESON_OPTS_TARGET+=" -Dsdl2-audio=enabled -Dsdl2-video=enabled -Dsdl2-gamepad=enabled"
-
-if [ "${TARGET_ARCH}" = "x86_64" ]; then
-  PKG_DEPENDS_TARGET+=" libva"
-  PKG_MESON_OPTS_TARGET+=" -Dvaapi=enabled"
-fi
+PKG_MESON_OPTS_TARGET+=" -Dsdl2-gamepad=enabled"
 
-PKG_MESON_OPTS_TARGET+=" -Ddrm=enabled"
+# Vulkan has issues on S922X so disable
+[ "${DEVICE}" == "S922X" ] && PKG_MESON_OPTS_TARGET+=" -Dvulkan=disabled"
 
 post_makeinstall_target() {
   cp ${PKG_DIR}/scripts/* ${INSTALL}/usr/bin
   chmod 0755 ${INSTALL}/usr/bin/* 2>/dev/null ||:
   mkdir -p ${INSTALL}/usr/config/mpv
   cp -rf ${PKG_DIR}/config/* ${INSTALL}/usr/config/mpv/
-
-  mkdir -p ${INSTALL}/etc/mpv
-    cp ${PKG_DIR}/config/mpv.conf ${INSTALL}/etc/mpv/
-
-  case ${DEVICE} in
-    RK3326|RK3399|RK3566)
-      sed -i 's/^hwdec=.*/&\nhwdec-codecs=all/' ${INSTALL}/etc/mpv/mpv.conf ${INSTALL}/usr/config/mpv/mpv.conf
-    ;;
-    RK3588*)
-      sed -i 's/^hwdec=.*/hwdec=rkmpp,rkmpp-copy,auto/' ${INSTALL}/etc/mpv/mpv.conf ${INSTALL}/usr/config/mpv/mpv.conf
-    ;;
-    S922X|SM*)
-      sed -i 's/^hwdec=.*/hwdec=v4l2m2m-copy,auto/' ${INSTALL}/etc/mpv/mpv.conf ${INSTALL}/usr/config/mpv/mpv.conf
-    ;;
-  esac
 }
diff --git a/projects/ROCKNIX/packages/multimedia/mpv/scripts/start_mplayer.sh b/projects/ROCKNIX/packages/multimedia/mpv/scripts/start_mplayer.sh
index 1f55838de7..a3f3c7fc11 100755
--- a/projects/ROCKNIX/packages/multimedia/mpv/scripts/start_mplayer.sh
+++ b/projects/ROCKNIX/packages/multimedia/mpv/scripts/start_mplayer.sh
@@ -16,6 +16,6 @@ else
   RES="${FBHEIGHT}x${FBWIDTH}"
 fi
 
-/usr/bin/mpv --fullscreen --geometry=${RES} --input-gamepad=yes --input-ipc-server=/tmp/mpvsocket "${1}"
+/usr/bin/mpv --fullscreen --geometry=${RES} --hwdec=auto-safe --input-gamepad=yes --input-ipc-server=/tmp/mpvsocket "${1}"
 systemctl stop mpv
 exit 0
diff --git a/projects/ROCKNIX/packages/network/libpcap/package.mk b/projects/ROCKNIX/packages/network/libpcap/package.mk
index bd3c5eceb8..fbc970249d 100644
--- a/projects/ROCKNIX/packages/network/libpcap/package.mk
+++ b/projects/ROCKNIX/packages/network/libpcap/package.mk
@@ -1,10 +1,32 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/addons/addon-depends/network-tools-depends/depends/libpcap/package.mk
+PKG_NAME="libpcap"
+PKG_VERSION="1.10.4"
+PKG_SHA256="ed19a0383fad72e3ad435fd239d7cd80d64916b87269550159d20e47160ebe5f"
+PKG_LICENSE="GPL"
+PKG_SITE="http://www.tcpdump.org/"
+PKG_URL="http://www.tcpdump.org/release/libpcap-${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain"
+PKG_LONGDESC="A portable framework for low-level network monitoring."
+# use configure, not cmake. review cmake in future release.
+PKG_TOOLCHAIN="configure"
 
-PKG_BUILD_FLAGS="${PKG_BUILD_FLAGS/-cfg-libs/}"
-PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_TARGET/--disable-shared/--disable-static}"
+PKG_CONFIGURE_OPTS_TARGET="LIBS=-lpthread \
+                           ac_cv_header_libusb_1_0_libusb_h=no \
+                           --disable-static \
+                           --with-pcap=linux \
+                           --disable-bluetooth \
+                           --disable-can \
+                           --without-libnl \
+                           --disable-dbus \
+                           --disable-canusb"
+
+pre_configure_target() {
+# When cross-compiling, configure can't set linux version
+# forcing it
+  sed -i -e 's/ac_cv_linux_vers=unknown/ac_cv_linux_vers=2/' ../configure
+}
 
 post_makeinstall_target() {
   ln -sfv /usr/lib/libpcap.so.1 ${INSTALL}/usr/lib/libpcap.so.0.8
diff --git a/projects/ROCKNIX/packages/network/openssh/system.d/sshd.service b/projects/ROCKNIX/packages/network/openssh/system.d/sshd.service
index fb849129b2..5417e4ae5d 100644
--- a/projects/ROCKNIX/packages/network/openssh/system.d/sshd.service
+++ b/projects/ROCKNIX/packages/network/openssh/system.d/sshd.service
@@ -1,16 +1,21 @@
 [Unit]
-Description=OpenSSH server
+Description=OpenSSH server daemon
+After=network.target
 ConditionKernelCommandLine=|ssh
 ConditionPathExists=|/storage/.cache/services/sshd.conf
-Requires=sshd.socket
-After=sshd.socket
-PropagatesStopTo=sshd.socket
-Wants=sshd-keygen.service
 
 [Service]
-Type=oneshot
-RemainAfterExit=yes
-ExecStart=/bin/true
+Restart=on-failure
+EnvironmentFile=-/storage/.cache/services/sshd.conf
+ExecStartPre=-/bin/sh -c 'mkdir -p /storage/.cache/ssh'
+ExecStartPre=/usr/bin/ssh-keygen -A
+ExecStartPre=-/bin/sh -c 'chmod 600 /storage/.cache/ssh/ssh_host_*'
+ExecStartPre=-/bin/sh -c 'chmod 644 /storage/.cache/ssh/ssh_host_*.pub'
+ExecStart=/usr/sbin/sshd -D $SSH_ARGS
+ExecReload=/bin/kill -HUP $MAINPID
+TimeoutStopSec=1s
+RestartSec=2
+StartLimitInterval=0
 
 [Install]
 WantedBy=multi-user.target
diff --git a/projects/ROCKNIX/packages/network/samba/package.mk b/projects/ROCKNIX/packages/network/samba/package.mk
index b28429170e..c09e609398 100644
--- a/projects/ROCKNIX/packages/network/samba/package.mk
+++ b/projects/ROCKNIX/packages/network/samba/package.mk
@@ -3,8 +3,8 @@
 # Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
 
 PKG_NAME="samba"
-PKG_VERSION="4.24.5"
-PKG_SHA256="6d5d7ee82f5ce9da4135086c9b184e47a58b4b023565f58abbb1f8c8a922306b"
+PKG_VERSION="4.21.0"
+PKG_SHA256="09bb56db4ce003cafdbebe9bad368c4f4ff1945f732d18077d52f36ab20cef88"
 PKG_LICENSE="GPLv3+"
 PKG_SITE="https://www.samba.org"
 PKG_URL="https://download.samba.org/pub/samba/stable/${PKG_NAME}-${PKG_VERSION}.tar.gz"
@@ -87,6 +87,9 @@ pre_configure_target() {
   cd ${PKG_BUILD}
     rm -rf .${TARGET_NAME}
 
+# work around link issues
+  export LDFLAGS="${LDFLAGS} -lreadline -lncursesw"
+
 # support 64-bit offsets and seeks on 32-bit platforms
   if [ "${TARGET_ARCH}" = "arm" ]; then
     export CFLAGS+=" -D_FILE_OFFSET_BITS=64 -D_OFF_T_DEFINED_ -Doff_t=off64_t -Dlseek=lseek64"
diff --git a/projects/ROCKNIX/packages/network/samba/system.d/nmbd.service b/projects/ROCKNIX/packages/network/samba/system.d/nmbd.service
index 8e73595f2f..a2dc1b35a2 100644
--- a/projects/ROCKNIX/packages/network/samba/system.d/nmbd.service
+++ b/projects/ROCKNIX/packages/network/samba/system.d/nmbd.service
@@ -6,7 +6,6 @@ ConditionPathExists=!/storage/.cache/services/samba.disabled
 ConditionPathExists=/run/samba/smb.conf
 
 [Service]
-Slice=background.slice
 Type=forking
 PIDFile=/run/samba/nmbd.pid
 ExecStart=/usr/sbin/nmbd
diff --git a/projects/ROCKNIX/packages/network/samba/system.d/smbd.service b/projects/ROCKNIX/packages/network/samba/system.d/smbd.service
index 06b0455991..5ce9c0875e 100644
--- a/projects/ROCKNIX/packages/network/samba/system.d/smbd.service
+++ b/projects/ROCKNIX/packages/network/samba/system.d/smbd.service
@@ -6,7 +6,6 @@ ConditionPathExists=!/storage/.cache/services/samba.disabled
 ConditionPathExists=/run/samba/smb.conf
 
 [Service]
-Slice=background.slice
 Type=forking
 PIDFile=/run/samba/smbd.pid
 LimitNOFILE=16384
diff --git a/projects/ROCKNIX/packages/network/simple-http-server/system.d/simple-http-server.service b/projects/ROCKNIX/packages/network/simple-http-server/system.d/simple-http-server.service
index d66a531881..f88fb527ae 100644
--- a/projects/ROCKNIX/packages/network/simple-http-server/system.d/simple-http-server.service
+++ b/projects/ROCKNIX/packages/network/simple-http-server/system.d/simple-http-server.service
@@ -4,7 +4,6 @@ Wants=network-pre.target
 After=network-pre.target
 
 [Service]
-Slice=background.slice
 ExecStart=/usr/bin/bash -c "source /etc/profile.d/001-functions && /usr/bin/simple-http-server -i -p 80 -a root:$(get_setting root.password) -s -u /storage"
 Restart=always
 KillMode=process
diff --git a/projects/ROCKNIX/packages/network/syncthing/system.d/syncthing.service b/projects/ROCKNIX/packages/network/syncthing/system.d/syncthing.service
index 893045e878..e7dc9e2f5c 100644
--- a/projects/ROCKNIX/packages/network/syncthing/system.d/syncthing.service
+++ b/projects/ROCKNIX/packages/network/syncthing/system.d/syncthing.service
@@ -3,7 +3,6 @@ Description=Start SyncThing
 After=rocknix.service
 
 [Service]
-Slice=background.slice
 Type=simple
 ExecStart=/usr/bin/start_syncthing.sh
 
diff --git a/projects/ROCKNIX/packages/python/devel/pyxel/package.mk b/projects/ROCKNIX/packages/python/devel/pyxel/package.mk
index cac4f6f73c..e922df2519 100644
--- a/projects/ROCKNIX/packages/python/devel/pyxel/package.mk
+++ b/projects/ROCKNIX/packages/python/devel/pyxel/package.mk
@@ -5,8 +5,8 @@ PKG_NAME="pyxel"
 PKG_VERSION="2.9.9"
 PKG_SHA256="2a8c896dd8854eede7992c22878903333a69b6acfabb874f8aefbdee519c2ca1"
 PKG_LICENSE="MIT"
-PKG_SITE="https://pypi.org/project/pyxel"
-PKG_URL="https://files.pythonhosted.org/packages/cp311/p/${PKG_NAME}/${PKG_NAME}-${PKG_VERSION}-cp311-abi3-manylinux_2_28_aarch64.whl"
+PKG_SITE="https://github.com/kitao/pyxel"
+PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/${PKG_NAME}-${PKG_VERSION}-cp311-abi3-manylinux_2_28_aarch64.whl"
 PKG_DEPENDS_TARGET="toolchain Python3"
 PKG_LONGDESC="Pyxel is a retro game engine for Python"
 PKG_TOOLCHAIN="manual"
diff --git a/projects/ROCKNIX/packages/rust/rust/package.mk b/projects/ROCKNIX/packages/rust/rust/package.mk
index e4390a439b..548ed3f629 100644
--- a/projects/ROCKNIX/packages/rust/rust/package.mk
+++ b/projects/ROCKNIX/packages/rust/rust/package.mk
@@ -1,10 +1,131 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/rust/rust/package.mk
+PKG_NAME="rust"
+PKG_VERSION="1.94.1"
+PKG_SHA256="4c142a625f12e3cdf716c68ae19f4f60d98ad1482627b08579b15838e95ad514"
+PKG_LICENSE="MIT"
+PKG_SITE="https://www.rust-lang.org"
+PKG_URL="https://static.rust-lang.org/dist/rustc-${PKG_VERSION}-src.tar.gz"
+PKG_DEPENDS_HOST="toolchain llvm:host"
+PKG_DEPENDS_UNPACK="rustc-snapshot rust-std-snapshot cargo-snapshot"
+PKG_LONGDESC="A systems programming language that prevents segfaults, and guarantees thread safety."
+PKG_TOOLCHAIN="manual"
 
-# ROCKNIX: our cargo packages read the linker setup from the toolchain cargo home
-post_configure_host() {
-  mkdir -p ${TOOLCHAIN}/cargo_home
-    cp -a ${PKG_BUILD}/cargo_home/config.toml ${TOOLCHAIN}/cargo_home
+pre_configure_host() {
+  "$(get_build_dir rustc-snapshot)/install.sh" --prefix="${PKG_BUILD}/rust-snapshot" --disable-ldconfig
+  "$(get_build_dir rust-std-snapshot)/install.sh" --prefix="${PKG_BUILD}/rust-snapshot" --disable-ldconfig
+  "$(get_build_dir cargo-snapshot)/install.sh" --prefix="${PKG_BUILD}/rust-snapshot" --disable-ldconfig
+}
+
+configure_host() {
+
+  mkdir -p ${PKG_BUILD}/targets
+
+  case "${TARGET_ARCH}" in
+    "arm")
+      # the arm target is special because we specify the subarch. ie armv8a
+      cp -a ${PKG_DIR}/targets/arm-libreelec-linux-gnueabihf.json ${PKG_BUILD}/targets/${TARGET_NAME}.json
+      ;;
+    "aarch64" | "x86_64")
+      cp -a ${PKG_DIR}/targets/${TARGET_NAME}.json ${PKG_BUILD}/targets/${TARGET_NAME}.json
+      ;;
+  esac
+
+  cat >${PKG_BUILD}/config.toml  <<END
+change-id = 148671
+
+[llvm]
+download-ci-llvm = false
+
+[target.${TARGET_NAME}]
+llvm-config = "${TOOLCHAIN}/bin/llvm-config"
+cxx = "${TARGET_PREFIX}g++"
+cc = "${TARGET_PREFIX}gcc"
+
+[target.${RUST_HOST}]
+llvm-config = "${TOOLCHAIN}/bin/llvm-config"
+cxx = "${CXX}"
+cc = "${CC}"
+
+[rust]
+rpath = true
+channel = "stable"
+codegen-tests = false
+optimize = true
+download-rustc = false
+
+[build]
+submodules = false
+docs = false
+profiler = true
+vendor = true
+
+rustc = "${PKG_BUILD}/rust-snapshot/bin/rustc"
+cargo = "${PKG_BUILD}/rust-snapshot/bin/cargo"
+
+target = [
+  "${TARGET_NAME}",
+  "${RUST_HOST}"
+]
+
+host = [
+  "${RUST_HOST}"
+]
+
+build = "${RUST_HOST}"
+
+[install]
+prefix = "${TOOLCHAIN}"
+bindir = "${TOOLCHAIN}/bin"
+libdir = "${TOOLCHAIN}/lib"
+datadir = "${TOOLCHAIN}/share"
+mandir = "${TOOLCHAIN}/share/man"
+
+END
+
+  CARGO_HOME="${TOOLCHAIN}/cargo_home"
+  mkdir -p "${CARGO_HOME}"
+
+  cat >${CARGO_HOME}/config.toml <<END
+[target.${TARGET_NAME}]
+linker = "${TARGET_PREFIX}gcc"
+
+[target.${RUST_HOST}]
+linker = "${CC}"
+rustflags = ["-C", "link-arg=-Wl,-rpath,${TOOLCHAIN}/lib"]
+
+[build]
+target-dir = "${PKG_BUILD}/target"
+
+[term]
+progress.when = 'always'
+progress.width = 80
+
+END
+}
+
+make_host() {
+  cd ${PKG_BUILD}
+
+  unset CFLAGS
+  unset CXXFLAGS
+  unset CPPFLAGS
+  unset LDFLAGS
+
+  export RUST_TARGET_PATH="${PKG_BUILD}/targets/"
+  export HOST_CMAKE="${TOOLCHAIN}/bin/cmake"
+  export HOST_CMAKE_TOOLCHAIN_FILE="${CMAKE_CONF}"
+
+  python3 src/bootstrap/bootstrap.py -j ${CONCURRENCY_MAKE_LEVEL} build --stage 2 --verbose
+}
+
+makeinstall_host() {
+  mkdir -p ${TOOLCHAIN}/bin
+    cp -a build/${RUST_HOST}/stage2/bin/* ${TOOLCHAIN}/bin
+
+  mkdir -p ${TOOLCHAIN}/lib/rustlib
+    cp -a build/${RUST_HOST}/stage2/lib/* ${TOOLCHAIN}/lib
+
+    cp -a ${PKG_BUILD}/targets/*.json ${TOOLCHAIN}/lib/rustlib/
 }
diff --git a/projects/ROCKNIX/packages/textproc/icu/package.mk b/projects/ROCKNIX/packages/textproc/icu/package.mk
index de2d2cabca..132f2de5b6 100644
--- a/projects/ROCKNIX/packages/textproc/icu/package.mk
+++ b/projects/ROCKNIX/packages/textproc/icu/package.mk
@@ -1,9 +1,18 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/addons/addon-depends/icu/package.mk
+PKG_NAME="icu"
+PKG_VERSION="74.1"
+PKG_SHA256="86ce8e60681972e60e4dcb2490c697463fcec60dd400a5f9bffba26d0b52b8d0"
+PKG_LICENSE="Custom"
+PKG_SITE="http://www.icu-project.org"
+PKG_URL="https://github.com/unicode-org/icu/releases/download/release-${PKG_VERSION//./-}/icu4c-${PKG_VERSION//./_}-src.tgz"
+PKG_DEPENDS_HOST="toolchain:host"
+PKG_DEPENDS_TARGET="toolchain icu:host"
+PKG_LONGDESC="International Components for Unicode library."
+PKG_TOOLCHAIN="configure"
 
-unset PKG_BUILD_FLAGS
+#PKG_BUILD_FLAGS="-sysroot"
 
 configure_package() {
   PKG_CONFIGURE_SCRIPT="${PKG_BUILD}/source/configure"
@@ -17,4 +26,6 @@ configure_package() {
 
   PKG_CONFIGURE_OPTS_TARGET="${PKG_CONFIGURE_OPTS_HOST} \
                              --with-cross-build=${PKG_BUILD}/.${HOST_NAME}"
+
 }
+
diff --git a/projects/ROCKNIX/packages/tools/at-spi2-core/package.mk b/projects/ROCKNIX/packages/tools/at-spi2-core/package.mk
index c6dafcd1ac..2f0935f147 100644
--- a/projects/ROCKNIX/packages/tools/at-spi2-core/package.mk
+++ b/projects/ROCKNIX/packages/tools/at-spi2-core/package.mk
@@ -1,14 +1,20 @@
-# SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# SPDX-License-Identifier: GPL-2.0-or-later
+# Copyright (C) 2017 Escalade
+# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/addons/addon-depends/chrome-depends/at-spi2-core/package.mk
+PKG_NAME="at-spi2-core"
+PKG_VERSION="2.45.1"
+PKG_SHA256="ba95f346e93108fbb3462c62437081d582154db279b4052dedc52a706828b192"
+PKG_LICENSE="OSS"
+PKG_SITE="http://www.gnome.org/"
+PKG_URL="https://download.gnome.org/sources/at-spi2-core/${PKG_VERSION:0:4}/at-spi2-core-${PKG_VERSION}.tar.xz"
+PKG_DEPENDS_TARGET="toolchain atk dbus glib libXtst libXext libXi"
+PKG_LONGDESC="Protocol definitions and daemon for D-Bus at-spi."
 
-PKG_DEPENDS_TARGET+=" libXext libXi"
+PKG_MESON_OPTS_TARGET="-Ddocs=false \
+                       -Dintrospection=no \
+                       -Ddbus_daemon=/usr/bin/dbus-daemon"
 
 pre_configure_target() {
-  PKG_MESON_OPTS_TARGET="-Ddocs=false \
-                         -Dintrospection=disabled \
-                         -Ddbus_daemon=/usr/bin/dbus-daemon"
-
   TARGET_LDFLAGS="${TARGET_LDFLAGS} -lXi -lXext"
 }
diff --git a/projects/ROCKNIX/packages/tools/atf/package.mk b/projects/ROCKNIX/packages/tools/atf/package.mk
index 605b46dd7f..87f59f453e 100644
--- a/projects/ROCKNIX/packages/tools/atf/package.mk
+++ b/projects/ROCKNIX/packages/tools/atf/package.mk
@@ -15,18 +15,17 @@ PKG_PATCH_DIRS+="${DEVICE}"
 case ${DEVICE} in
   H700)
     PKG_VERSION="2.12.0"
-    PKG_SHA256="d95aaf292792c98035910d7e6c64ebfb297c897fef510415db1612f6d39f9223"
     PKG_DEPENDS_TARGET+=" h700-suspend-stub"
     # BL31 embeds the stubs; rebuild when they change
     PKG_NEED_UNPACK+=" $(get_pkg_directory h700-suspend-stub) ${SYSROOT_PREFIX}/usr/share/h700-suspend-stub"
   ;;
   *)
     PKG_VERSION="2.10.0"
-    PKG_SHA256="6b1d5e89c311c5e7eaeb062713953311464c0378ab3e4ebc7ede72a746964bb1"
+    PKG_SHA256="696b8e53923aac4474532da7dd681f0bd044b329732facd65aeabea3e61adca9"
     ;;
 esac
 
-PKG_URL="https://github.com/TrustedFirmware-A/trusted-firmware-a/archive/v${PKG_VERSION}.tar.gz"
+PKG_URL="https://github.com/ARM-software/arm-trusted-firmware/archive/v${PKG_VERSION}.tar.gz"
 
 
 [ -n "${KERNEL_TOOLCHAIN}" ] && PKG_DEPENDS_TARGET+=" gcc-${KERNEL_TOOLCHAIN}:host"
diff --git a/projects/ROCKNIX/packages/tools/batteryplus/package.mk b/projects/ROCKNIX/packages/tools/batteryplus/package.mk
index ec54dc925a..f03a220b48 100644
--- a/projects/ROCKNIX/packages/tools/batteryplus/package.mk
+++ b/projects/ROCKNIX/packages/tools/batteryplus/package.mk
@@ -2,8 +2,8 @@
 # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
 
 PKG_NAME="batteryplus"
-PKG_VERSION="31a3b629bc221bada24526cb6a91ded2d781c40e" # v1.2.1
-PKG_SHA256="bd03303e2c4e63772aba50b512708c5acf5a56a07c90052bbc7191b35607fb48"
+PKG_VERSION="1c31e89ec1828d51710ad35a607bdfad7e18464e"
+PKG_SHA256="1619da9e945746ea589edb70efd1095b07d21207be3fa43a4c1598be5c2a2089"
 PKG_LICENSE="GPL"
 PKG_SITE="https://github.com/Mikhailzrick/knubat.components"
 PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
diff --git a/projects/ROCKNIX/packages/tools/entware/system.d/entware.service b/projects/ROCKNIX/packages/tools/entware/system.d/entware.service
index dc458be049..124d90134f 100644
--- a/projects/ROCKNIX/packages/tools/entware/system.d/entware.service
+++ b/projects/ROCKNIX/packages/tools/entware/system.d/entware.service
@@ -6,7 +6,6 @@ Requires=network-online.target
 ConditionPathExists=/opt/etc/init.d/rc.unslung
 
 [Service]
-Slice=background.slice
 Type=oneshot
 ExecStart=/opt/etc/init.d/rc.unslung start
 ExecStop=/opt/etc/init.d/rc.unslung stop
diff --git a/projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk b/projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk
index 9ca7ef9be6..d3d5edcbd3 100644
--- a/projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk
+++ b/projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk
@@ -27,8 +27,7 @@ makeinstall_target() {
       sed -i 's|/sys/module/retroid/parameters|/sys/module/rsinput/parameters|g' ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
       ;;
     SM6115)
-      sed -i 's|^PARAMETERS_DIR_PATH=.*|import os\nPARAMETERS_DIR_PATH = "/sys/module/mangmi/parameters" if os.path.exists("/sys/module/mangmi/parameters") else "/sys/module/rsinput/parameters"|' \
-        ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
+      sed -i 's|/sys/module/retroid/parameters|/sys/module/mangmi/parameters|g' ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
       ;;
   esac
 
diff --git a/projects/ROCKNIX/packages/tools/inputplumber/package.mk b/projects/ROCKNIX/packages/tools/inputplumber/package.mk
index aebfacb57f..4d8f3eeeaf 100644
--- a/projects/ROCKNIX/packages/tools/inputplumber/package.mk
+++ b/projects/ROCKNIX/packages/tools/inputplumber/package.mk
@@ -2,12 +2,12 @@
 # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
 
 PKG_NAME="inputplumber"
-PKG_VERSION="0.82.0"
-PKG_SHA256="aaee9b65b47a21756169eb1c49eb258ecdd1896fb8dd4996c2b50d11af049d21"
+PKG_VERSION="v0.79.0"
+PKG_SHA256="123c858139d3b78e3f075158ce16b8fdc8067a10e31a93cb1e7f2aea816106bd"
 PKG_LICENSE="GPLv3"
 PKG_SITE="https://github.com/ShadowBlip/InputPlumber"
-PKG_URL="${PKG_SITE}/archive/refs/tags/v${PKG_VERSION}.tar.gz"
-PKG_DEPENDS_TARGET="toolchain cargo:host cargo rust llvm:host systemd libevdev libiio polkit"
+PKG_URL="https://github.com/ShadowBlip/InputPlumber/releases/download/${PKG_VERSION}/inputplumber-aarch64.tar.gz"
+PKG_DEPENDS_TARGET="toolchain systemd libevdev libiio polkit"
 PKG_LONGDESC="Open source input router and remapper daemon for Linux"
 PKG_TOOLCHAIN="manual"
 
@@ -17,12 +17,10 @@ PKG_TOOLCHAIN="manual"
 # files would compete for the same source devices. Drop them.
 PKG_DROP_DEVICE_CONFIGS="
   50-ayaneo_pocket_s2.yaml
-  50-ayaneo_pocket_ds.yaml
   50-ayn_odin2.yaml
   50-ayn_odin2_mini.yaml
   50-ayn_odin3.yaml
   50-ayn_thor.yaml
-  50-ayn_thor_lite.yaml
   50-konkr_pocket_fit.yaml
   50-konkr_pocket_fit_elite.yaml
   50-retroid_pocket5.yaml
@@ -34,26 +32,13 @@ PKG_DROP_DEVICE_CONFIGS="
 
 post_unpack() {
   for config in ${PKG_DROP_DEVICE_CONFIGS}; do
-    rm -f ${PKG_BUILD}/rootfs/usr/share/inputplumber/devices/${config}
+    rm -f ${PKG_BUILD}/usr/share/inputplumber/devices/${config}
   done
 }
 
-make_target() {
-  export LIBCLANG_PATH=${TOOLCHAIN}/lib
-  export LD_LIBRARY_PATH=${TOOLCHAIN}/lib:${LD_LIBRARY_PATH}
-  export BINDGEN_EXTRA_CLANG_ARGS="--sysroot=${SYSROOT_PREFIX} -isystem ${SYSROOT_PREFIX}/usr/include"
-
-  cargo build \
-    --target ${TARGET_NAME} \
-    --release
-}
-
 makeinstall_target() {
-  mkdir -p ${INSTALL}/usr/bin
-  cp ${PKG_BUILD}/.${TARGET_NAME}/target/${TARGET_NAME}/release/inputplumber ${INSTALL}/usr/bin/
-
   mkdir -p ${INSTALL}/usr
-  rsync -ar ${PKG_BUILD}/rootfs/usr/ ${INSTALL}/usr/
+  rsync -ar ${PKG_BUILD}/usr/ ${INSTALL}/usr/
 
   # sources/ is overlaid with cp, so pin the mode udev needs to run the shim.
   chmod 0755 ${INSTALL}/usr/lib/inputplumber/setfacl-shim/setfacl
diff --git a/projects/ROCKNIX/packages/tools/socat/package.mk b/projects/ROCKNIX/packages/tools/socat/package.mk
index 0a6722d1d9..7768bd7cda 100644
--- a/projects/ROCKNIX/packages/tools/socat/package.mk
+++ b/projects/ROCKNIX/packages/tools/socat/package.mk
@@ -3,8 +3,8 @@
 # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 
 PKG_NAME="socat"
-PKG_VERSION="1.8.1.3"
-PKG_SHA256="25bc6476292b2e614220989c77b0b6fca87bb2525d9747b31a6639b1fb602418"
+PKG_VERSION="1.7.4.4"
+PKG_SHA256="fbd42bd2f0e54a3af6d01bdf15385384ab82dbc0e4f1a5e153b3e0be1b6380ac"
 PKG_LICENSE="GPLv2+"
 PKG_SITE="http://www.dest-unreach.org/socat/download"
 PKG_URL="${PKG_SITE}/${PKG_NAME}-${PKG_VERSION}.tar.bz2"
@@ -16,8 +16,3 @@ PKG_CONFIGURE_OPTS_TARGET+="	--disable-libwrap \
 				--disable-readline \
 				--enable-termios"
 
-
-pre_makeinstall_target() {
-  # 1.8 installs helper scripts from the source tree, and we build out of tree
-  cp -f ${PKG_BUILD}/*.sh ${PKG_BUILD}/.${TARGET_NAME}/ 2>/dev/null || true
-}
diff --git a/projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-config b/projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-config
index 2a013b0712..65c0ee2b3a 100755
--- a/projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-config
+++ b/projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-config
@@ -45,14 +45,3 @@ if [ -f ${SWAY_CONFIG_DAEMON} ] ; then
 fi
 
 echo SWAY_DAEMON_ARGS=\"${SWAY_DAEMON_CONF} ${SWAY_DAEMON_ARGS}\" > ${SWAY_CONFIG_RUN}
-
-# Rotate on the primary plane what fits it, composite the rest.
-. /etc/profile
-if plane_rotation; then
-  echo WLR_OUTPUT_ROTATE_PLANE=1 >> ${SWAY_CONFIG_RUN}
-  ROTATE_MAX=$(plane_rotation_max_height)
-  [ -n "${ROTATE_MAX}" ] && echo WLR_OUTPUT_ROTATE_PLANE_MAX_HEIGHT=${ROTATE_MAX} >> ${SWAY_CONFIG_RUN}
-fi
-
-# Per-game fractional scale hint from runemu.
-echo WLR_FULLSCREEN_SCALE_HINT_FILE=/run/rocknix/fullscreen-scale-hint >> ${SWAY_CONFIG_RUN}
diff --git a/projects/ROCKNIX/packages/wayland/compositor/sway/system.d/sway.service b/projects/ROCKNIX/packages/wayland/compositor/sway/system.d/sway.service
index 65c730085e..e05ea6466b 100644
--- a/projects/ROCKNIX/packages/wayland/compositor/sway/system.d/sway.service
+++ b/projects/ROCKNIX/packages/wayland/compositor/sway/system.d/sway.service
@@ -5,8 +5,6 @@ After=multi-user.target rocknix-automount.service
 ConditionKernelCommandLine=!installer
 
 [Service]
-MemoryLow=96M
-OOMScoreAdjust=-500
 Environment=HOME=/storage
 Environment=XDG_RUNTIME_DIR=/var/run/0-runtime-dir
 Environment=WLR_BACKENDS=drm,libinput
diff --git a/projects/ROCKNIX/packages/wayland/lib/fcft/package.mk b/projects/ROCKNIX/packages/wayland/lib/fcft/package.mk
index eeadd9c208..3e21b29e2c 100644
--- a/projects/ROCKNIX/packages/wayland/lib/fcft/package.mk
+++ b/projects/ROCKNIX/packages/wayland/lib/fcft/package.mk
@@ -1,7 +1,21 @@
 # SPDX-License-Identifier: GPL-2.0
 # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/wayland/lib/fcft/package.mk
+PKG_NAME="fcft"
+PKG_VERSION="3.1.9"
+PKG_SHA256="ae6872d42c96e6ca4fa35e4e6ef86e2458e4119fc7393dadd06a36c86bb3def2"
+PKG_LICENSE="MIT"
+PKG_SITE="https://codeberg.org/dnkl/fcft"
+PKG_URL="https://codeberg.org/dnkl/fcft/archive/${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain pixman fontconfig freetype tllist"
+PKG_LONGDESC="A simple library for font loading and glyph rasterization using FontConfig, FreeType and pixman."
 
-# codeberg regenerated this tag's archive, so core's checksum no longer matches upstream
-PKG_SHA256="b0c0f4a599f43723736c8565b8b84337c4195077f07f1bb8bb3252bb13a2306a"
+PKG_MESON_OPTS_TARGET="-Ddocs=disabled \
+                       -Dgrapheme-shaping=disabled \
+                       -Drun-shaping=disabled \
+                       -Dtest-text-shaping=false \
+                       -Dexamples=false"
+
+pre_configure_target() {
+export TARGET_CFLAGS="${TARGET_CFLAGS} -Wno-error=maybe-uninitialized"
+}
diff --git a/projects/ROCKNIX/packages/wayland/lib/wlroots/package.mk b/projects/ROCKNIX/packages/wayland/lib/wlroots/package.mk
index a0eeca06b4..016c1dc648 100644
--- a/projects/ROCKNIX/packages/wayland/lib/wlroots/package.mk
+++ b/projects/ROCKNIX/packages/wayland/lib/wlroots/package.mk
@@ -10,10 +10,11 @@ PKG_TOOLCHAIN="meson"
 
 case ${DEVICE} in
   RK3326|RK3566|RK3576|S922X)
-    # wlroots 0.19.3 with libmali hacks
-    PKG_VERSION="132e31cfe19f51b478301aa5aab1e6c4be3f8874"
-    PKG_SHA256="96aa6240e72b8ff4dc9943fc5b080e264a5fbf8b94fe8da10e1d6befa552b8fc"
-    PKG_URL="https://github.com/rocknix/rockchip-wlroots/archive/${PKG_VERSION}.tar.gz"
+    # despite the '-rk' indication this is a wlroots version with libmali hacks
+    PKG_VERSION="0.19.3-rk"
+    PKG_SHA256="5385dc105f2c4c5fe3157e0b0299d6508765086d605fe4efe3ae437d4f18a5d9"
+    PKG_PATCH_DIRS+=" libmali"
+    PKG_URL="https://github.com/rocknix/rockchip-wlroots/archive/refs/tags/${PKG_VERSION}.tar.gz"
     ;;
   RK3588)
     PKG_VERSION="0.17.4-rk"
diff --git a/projects/ROCKNIX/packages/wayland/util/foot/config/foot.ini b/projects/ROCKNIX/packages/wayland/util/foot/config/foot.ini
index 1fb96c1b6a..8c8608e416 100644
--- a/projects/ROCKNIX/packages/wayland/util/foot/config/foot.ini
+++ b/projects/ROCKNIX/packages/wayland/util/foot/config/foot.ini
@@ -18,7 +18,7 @@ font=monospace:size=12
 # vertical-letter-offset=0
 # underline-offset=<font metrics>
 # box-drawings-uses-font-glyphs=no
-dpi-aware=no
+dpi-aware=auto
 
 # initial-window-size-pixels=700x500  # Or,
 # initial-window-size-chars=<COLSxROWS>
@@ -55,6 +55,7 @@ dpi-aware=no
 
 [cursor]
 style=beam
+color=000000 eeeeee
 blink=yes
 # beam-thickness=1.5
 # underline-thickness=<font underline thickness>
@@ -63,11 +64,10 @@ blink=yes
 # hide-when-typing=no
 # alternate-scroll-mode=yes
 
-[colors-dark]
+[colors]
 alpha=0.95
 background=000000
 foreground=eeeeee
-cursor=000000 eeeeee
 regular0=1c1c1c  # black
 regular1=af005f  # red
 regular2=5faf00  # green
diff --git a/projects/ROCKNIX/packages/wayland/util/foot/package.mk b/projects/ROCKNIX/packages/wayland/util/foot/package.mk
index 90d8b166d6..939f678eea 100644
--- a/projects/ROCKNIX/packages/wayland/util/foot/package.mk
+++ b/projects/ROCKNIX/packages/wayland/util/foot/package.mk
@@ -1,8 +1,35 @@
 # SPDX-License-Identifier: GPL-2.0
 # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
-# PKG_DIR resolves here, so this shadow keeps copies of core's scripts/ and config/
-. ${ROOT}/packages/wayland/util/foot/package.mk
+PKG_NAME="foot"
+PKG_VERSION="1.19.0"
+PKG_SHA256="aa537908dff8a573adb68137974f8b317eed3b779d3e6954da84e0baff7b13a0"
+PKG_LICENSE="MIT"
+PKG_SITE="https://codeberg.org/dnkl/foot/"
+PKG_URL="https://codeberg.org/dnkl/foot/archive/${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain ncurses wayland wayland-protocols pixman fontconfig libxkbcommon fcft"
+PKG_LONGDESC="A fast, lightweight and minimalistic Wayland terminal emulator"
 
-# codeberg regenerated this tag's archive, so core's checksum no longer matches upstream
-PKG_SHA256="f5917cad2d7b723b99873e53d78fd10ea202923d189aed5086591fc53b70b7e3"
+PKG_MESON_OPTS_TARGET="-Ddocs=disabled \
+                       -Dthemes=false \
+                       -Dime=false \
+                       -Dgrapheme-clustering=auto \
+                       -Dterminfo=disabled \
+                       -Ddefault-terminfo=xterm"
+
+pre_configure_target() {
+  export TARGET_CFLAGS=$(echo "${TARGET_CFLAGS} -Wno-error=switch")
+}
+
+post_makeinstall_target(){
+  # clean up
+  safe_remove ${INSTALL}/usr/share/*
+
+  # install scripts
+  mkdir -p ${INSTALL}/usr/bin
+    cp ${PKG_DIR}/scripts/foot.sh ${INSTALL}/usr/bin
+
+  # install config
+  mkdir -p ${INSTALL}/usr/share/foot
+    cp ${PKG_DIR}/config/foot.ini ${INSTALL}/usr/share/foot
+}
diff --git a/projects/ROCKNIX/packages/wayland/util/foot/scripts/foot.sh b/projects/ROCKNIX/packages/wayland/util/foot/scripts/foot.sh
index 79e0af5e53..7e30579dc0 100755
--- a/projects/ROCKNIX/packages/wayland/util/foot/scripts/foot.sh
+++ b/projects/ROCKNIX/packages/wayland/util/foot/scripts/foot.sh
@@ -9,8 +9,6 @@ FOOT_LOG_FILE=/var/log/foot.log
 if [ ! -f ${FOOT_CONFIG_DIR}/foot.ini ]; then
   mkdir -p ${FOOT_CONFIG_DIR}
     cp ${FOOT_CONFIG_DEFAULT} ${FOOT_CONFIG_DIR}
-elif grep -qE '^(\[colors\]|dpi-aware=auto|color=)' ${FOOT_CONFIG_DIR}/foot.ini; then
-  sed -i -e 's/^\[colors\]/[colors-dark]/' -e 's/^dpi-aware=auto/dpi-aware=no/' -e '/^\[cursor\]/,/^\[/{/^color=/d}' ${FOOT_CONFIG_DIR}/foot.ini
 fi
 
 if [ -z "${LOCPATH}" ]; then
diff --git a/projects/ROCKNIX/packages/wayland/util/wlr-randr/package.mk b/projects/ROCKNIX/packages/wayland/util/wlr-randr/package.mk
index f080c75b8b..7291543443 100644
--- a/projects/ROCKNIX/packages/wayland/util/wlr-randr/package.mk
+++ b/projects/ROCKNIX/packages/wayland/util/wlr-randr/package.mk
@@ -1,4 +1,11 @@
 # SPDX-License-Identifier: GPL-2.0
-# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
+# Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
 
-. ${ROOT}/packages/wayland/util/wlr-randr/package.mk
+PKG_NAME="wlr-randr"
+PKG_VERSION="0.4.1"
+PKG_SHA256="8af085aeed3132f7442a05bafeadfd0ea30e9a4818af1a91e161f7d560f2cd93"
+PKG_LICENSE="MIT"
+PKG_SITE="https://git.sr.ht/~emersion/wlr-randr"
+PKG_URL="https://git.sr.ht/~emersion/wlr-randr/archive/v${PKG_VERSION}.tar.gz"
+PKG_DEPENDS_TARGET="toolchain wayland"
+PKG_LONGDESC="Utility to manage outputs of a Wayland compositor."
diff --git a/projects/ROCKNIX/packages/wayland/util/wlr-randr/profile.d/010-wlr-randr b/projects/ROCKNIX/packages/wayland/util/wlr-randr/profile.d/010-wlr-randr
index c12496d803..1f51007da7 100755
--- a/projects/ROCKNIX/packages/wayland/util/wlr-randr/profile.d/010-wlr-randr
+++ b/projects/ROCKNIX/packages/wayland/util/wlr-randr/profile.d/010-wlr-randr
@@ -7,7 +7,7 @@
 set_refresh_rate() {
   DISPLAY_MODE="$1"
   DISPLAY_OUTPUT=$(/usr/bin/wlr-randr | awk 'NR==1{print $1;}')
-  RESOLUTION=$(/usr/bin/wlr-randr | awk -v o="${DISPLAY_OUTPUT}" '$1==o{h=1;next} /^[^ ]/{h=0} h&&f{print $1;exit} h&&/Modes:/{f=1}')
-  /usr/bin/wlr-randr --output "${DISPLAY_OUTPUT}" --mode "${RESOLUTION}@$(echo ${DISPLAY_MODE} | tr -cd '[[:digit:]].')"
+  RESOLUTION=$(/usr/bin/wlr-randr --output ${DISPLAY_OUTPUT} | awk 'f{print $1;f=0}/Modes/{f=1}')
+  /usr/bin/wlr-randr --output ${DISPLAY_OUTPUT} --mode ${RESOLUTION}@$(echo ${DISPLAY_MODE} | tr -cd '[[:digit:]].')
 }
 
```

## excerpt: projects/ROCKNIX/packages/network/simple-http-server/package.mk (whole)

```
    1  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    2  # Copyright (C) 2023-present NeoTheFox (https://github.com/NeoTheFox)
    3  
    4  PKG_NAME="simple-http-server"
    5  PKG_VERSION="0.8.0"
    6  PKG_LICENSE="MIT"
    7  PKG_SITE="https://github.com/TheWaWaR/simple-http-server"
    8  PKG_DEPENDS_TARGET="toolchain"
    9  PKG_LONGDESC="Simple http server in Rust"
   10  PKG_TOOLCHAIN="manual"
   11  
   12  case ${ARCH} in
   13    x86_64)
   14      PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/x86_64-unknown-linux-musl-simple-http-server"
   15      ;;
   16    arm)
   17      PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/armv7-unknown-linux-musleabihf-simple-http-server"
   18      ;;
   19    aarch64)
   20      PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/aarch64-unknown-linux-musl-simple-http-server"
   21      PKG_SHA256="88a523d339fa412575e497ee1741ffa4a7b6bdcfa23681a82eac7b8cd2bdf815"
   22      ;;
   23  esac
   24  
   25  unpack() {
   26    mkdir -p ${PKG_BUILD}
   27    cp ${SOURCES}/${PKG_NAME}/${PKG_NAME}-${PKG_VERSION}.${ARCH}*${PKG_NAME} ${PKG_BUILD}/simple-http-server
   28  }
   29  
   30  makeinstall_target() {
   31    mkdir -p ${INSTALL}/usr/bin
   32    install -Dm755 ${PKG_BUILD}/simple-http-server ${INSTALL}/usr/bin
   33  
   34    mkdir -p ${INSTALL}/usr/lib/systemd/system
   35    install -Dm644 ${PKG_DIR}/system.d/simple-http-server.service ${INSTALL}/usr/lib/systemd/system
   36  }
   37  
```

## excerpt: projects/ROCKNIX/packages/virtual/image/package.mk:89-113

```
   89  
   90  # Devtools... (not for Release)
   91  [ "${TESTING}" = "yes" ] && PKG_DEPENDS_TARGET+=" testing"
   92  
   93  # OEM packages
   94  [ "${OEM_SUPPORT}" = "yes" ] && PKG_DEPENDS_TARGET+=" oem"
   95  
   96  # htop
   97  [ "${HTOP_TOOL}" = "yes" ] && PKG_DEPENDS_TARGET+=" htop"
   98  
   99  # btop
  100  [ "${BTOP_TOOL}" = "yes" ] && PKG_DEPENDS_TARGET+=" btop"
  101  
  102  # modules packages
  103  [ "${MODULES_PKG}" = "yes" ] && PKG_DEPENDS_TARGET+=" modules"
  104  
  105  # Batteryplus voltage-based battery percentage daemon
  106  [ "${BATTERYPLUS_SUPPORT}" = "yes" ] && PKG_DEPENDS_TARGET+=" batteryplus"
  107  
  108  # Entware support
  109  mkdir -p ${INSTALL}
  110  ln -sf /storage/.opt ${INSTALL}/opt
  111  PKG_DEPENDS_TARGET+=" entware"
  112  
  113  true
```

## excerpt: projects/ROCKNIX/packages/apps/moonlight/package.mk (whole)

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    3  
    4  PKG_NAME="moonlight"
    5  PKG_LICENSE="GPLv3"
    6  PKG_SITE="https://github.com/moonlight-stream/moonlight-"
    7  PKG_DEPENDS_TARGET="toolchain opus SDL2 libevdev alsa curl enet avahi ffmpeg"
    8  PKG_LONGDESC="Moonlight is an open source implementation of NVIDIA's GameStream, as used by the NVIDIA Shield, but built for Linux."
    9  
   10  PKG_PATCH_DIRS+="${DEVICE}"
   11  
   12  if [ "${TARGET_ARCH}" = "null" ]
   13  then
   14    PKG_SITE+="qt"
   15    PKG_URL="${PKG_SITE}.git"
   16    PKG_VERSION="8a87a09947f27dd2fe4bee7ae9faabe86873a5c4"
   17    PKG_DEPENDS_TARGET+=" qt6"
   18    PKG_TOOLCHAIN="manual"
   19    make_target() {
   20      qmake6 "CONFIG+=embedded" moonlight-qt.pro
   21      make release
   22    }
   23    post_makeinstall_target() {
   24      mkdir -p ${INSTALL}/usr/bin
   25      mkdir -p ${INSTALL}/usr/config/modules
   26      cp ${PKG_BUILD}/app/moonlight ${INSTALL}/usr/bin/
   27      cp ${PKG_BUILD}/start_moonlight.sh ${INSTALL}/usr/bin/
   28      chmod +x ${INSTALL}/usr/bin/*
   29      mv ${INSTALL}/usr/bin/start_moonlight.sh ${INSTALL}/usr/config/modules/Start\ Moonlight.sh
   30    }
   31  else
   32    PKG_SITE+="embedded"
   33    PKG_URL="${PKG_SITE}.git"
   34    PKG_VERSION="a6bf7154a743d4f74a1b377e730f188352a1b80c"
   35    PKG_TOOLCHAIN="cmake"
   36  
   37    PKG_CMAKE_OPTS_TARGET+=" -DENABLE_CEC=OFF"
   38  
   39    post_makeinstall_target() {
   40      mkdir -p ${INSTALL}/usr/config/moonlight
   41      cp -R ${PKG_BUILD}/moonlight.conf ${INSTALL}/usr/config/moonlight
   42      rm ${INSTALL}/usr/etc/moonlight.conf
   43      rm ${INSTALL}/usr/share/moonlight/gamecontrollerdb.txt
   44    }
   45  fi
   46  
   47  if [[ "${DEVICE}" == RK* ]]
   48  then
   49    PKG_DEPENDS_TARGET+=" librga rkmpp"
   50  fi
   51  
   52  if [ ! "${OPENGL}" = "no" ]; then
   53    PKG_DEPENDS_TARGET+=" ${OPENGL} glu libglvnd"
   54  fi
   55  
   56  if [ "${OPENGLES_SUPPORT}" = yes ]; then
   57    PKG_DEPENDS_TARGET+=" ${OPENGLES}"
   58  fi
   59  
   60  if [ "${VULKAN_SUPPORT}" = "yes" ]
   61    then
   62    PKG_DEPENDS_TARGET+=" ${VULKAN}"
   63  fi
   64  
```

## excerpt: projects/ROCKNIX/packages/x11/xserver/xwayland/package.mk (whole)

```
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="xwayland"
    5  #PKG_VERSION="c5a47fda896aeefbf1d06a73e392a294344f9e1a" #24.1.13
    6  PKG_VERSION="24.1.13"
    7  PKG_SHA256="173aea3d6f79609164c04528e1c8e4c9b60fcd59391c3c9dad4667297d727fb6"
    8  PKG_LICENSE="OSS"
    9  PKG_SITE="https://gitlab.freedesktop.org/xorg/xserver"
   10  #PKG_URL="${PKG_SITE}.git"
   11  #PKG_GIT_CLONE_BRANCH="xwayland-24.1"
   12  PKG_URL="https://www.x.org/releases/individual/xserver/${PKG_NAME}-${PKG_VERSION}.tar.xz"
   13  PKG_DEPENDS_TARGET="toolchain util-macros font-util xorgproto libpciaccess libX11 libXfont2 libXinerama libxcvt libxshmfence libxkbfile libdrm openssl freetype pixman systemd xorg-launch-helper wayland libglvnd"
   14  PKG_NEED_UNPACK="$(get_pkg_directory xf86-video-nvidia)"
   15  PKG_LONGDESC="X.Org Server is the free and open-source implementation of the X Window System display server."
   16  
   17  get_graphicdrivers
   18  
   19  pre_configure_target() {
   20  export TARGET_CFLAGS="${TARGET_CFLAGS} -Wno-error=incompatible-pointer-types"
   21  }
   22  
   23  PKG_MESON_OPTS_TARGET+=" -Dxvfb=false \
   24                         -Dbuilder_addr=${BUILDER_NAME} \
   25                         -Ddefault_font_path="/usr/share/fonts/misc,built-ins" \
   26                         -Dxdmcp=false \
   27                         -Dxdm-auth-1=false \
   28                         -Dsecure-rpc=false \
   29                         -Dipv6=false \
   30                         -Dinput_thread=true \
   31                         -Dxkb_dir=${XORG_PATH_XKB} \
   32                         -Dxkb_output_dir="/var/cache/xkb" \
   33                         -Dvendor_name="ROCKNIX" \
   34                         -Dvendor_name_short="ROCKNIX" \
   35                         -Dvendor_web="https://rocknix.org" \
   36                         -Dlisten_tcp=false \
   37                         -Dlisten_unix=true \
   38                         -Dlisten_local=false \
   39                         -Ddpms=true \
   40                         -Dxf86bigfont=false \
   41                         -Dscreensaver=false \
   42                         -Dxres=true \
   43                         -Dxace=true \
   44                         -Dxselinux=false \
   45                         -Dxinerama=true \
   46                         -Dxcsecurity=false \
   47                         -Dxv=true \
   48                         -Dmitshm=true \
   49                         -Dsha1="libcrypto" \
   50                         -Ddri3=true \
   51                         -Ddrm=true \
   52                         -Dlibunwind=false \
   53                         -Ddocs=false \
   54                         -Ddevel-docs=false"
   55  
   56  if [ ! "${OPENGL}" = "no" ]; then
   57    PKG_DEPENDS_TARGET+=" ${OPENGL} libepoxy"
   58    PKG_MESON_OPTS_TARGET+=" -Dglx=true \
   59                             -Dglamor=true"
   60  else
   61    PKG_MESON_OPTS_TARGET+=" -Dglx=false \
   62                             -Dglamor=false"
   63  fi
   64  
   65  if [ "${COMPOSITE_SUPPORT}" = "yes" ]; then
   66    PKG_DEPENDS_TARGET+=" libXcomposite"
   67  fi
   68  
   69  post_makeinstall_target() {
   70    rm -rf ${INSTALL}/var/cache/xkb
   71  
   72  }
   73  
```

## excerpt: projects/ROCKNIX/packages/x11/xserver/xwayland/system.d/xorg-configure@.service (whole)

```
    1  [Unit]
    2  Description=configure Xorg Server for %i
    3  
    4  ConditionKernelCommandLine=!installer
    5  
    6  [Service]
    7  Type=oneshot
    8  ExecStart=/usr/lib/xorg/xorg-configure %i
    9  RemainAfterExit=yes
   10  
```

## excerpt: projects/ROCKNIX/packages/x11/xserver/xwayland/udev.d/97-xorg.rules (whole)

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
    4  
    5  ACTION!="add|change", GOTO="end_video"
    6  
    7  # xorg_start only does something for subsystem "pci" and "video" class.
    8  SUBSYSTEM=="pci", ATTR{class}=="0x030000", GOTO="subsystem_pci"
    9  GOTO="end_video"
   10  
   11  # check for drivers using the pci substem
   12  LABEL="subsystem_pci"
   13  DRIVER=="i915", ENV{xorg_driver}="i915", TAG+="systemd", ENV{SYSTEMD_WANTS}+="xorg-configure@i915.service"
   14  DRIVER=="amdgpu", ENV{xorg_driver}="amdgpu", TAG+="systemd", ENV{SYSTEMD_WANTS}+="xorg-configure@amdgpu.service"
   15  DRIVER=="radeon", ENV{xorg_driver}="radeon", TAG+="systemd", ENV{SYSTEMD_WANTS}+="xorg-configure@radeon.service"
   16  DRIVER=="vmwgfx", ENV{xorg_driver}="vmware", TAG+="systemd", ENV{SYSTEMD_WANTS}+="xorg-configure@vmware.service"
   17  DRIVER=="virtio-pci", ENV{xorg_driver}="modesetting", TAG+="systemd", ENV{SYSTEMD_WANTS}+="xorg-configure@modesetting.service"
   18  GOTO="end_video"
   19  
   20  LABEL="end_video"
   21  
```

## excerpt: projects/ROCKNIX/packages/devel/libaio/package.mk (whole)

```
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2017 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
    4  
    5  PKG_NAME="libaio"
    6  PKG_VERSION="0.3.113"
    7  PKG_SHA256="716c7059703247344eb066b54ecbc3ca2134f0103307192e6c2b7dab5f9528ab"
    8  PKG_LICENSE="GPL"
    9  PKG_SITE="https://pagure.io/libaio"
   10  PKG_URL="https://pagure.io/${PKG_NAME}/archive/${PKG_NAME}-${PKG_VERSION}/${PKG_NAME}-${PKG_NAME}-${PKG_VERSION}.tar.gz"
   11  PKG_DEPENDS_TARGET="toolchain"
   12  PKG_LONGDESC="Kernel Asynchronous I/O (AIO) Support for Linux."
   13  PKG_BUILD_FLAGS="-lto"
   14  
   15  make_target() {
   16    make -C src
   17  }
   18  
```

## excerpt: upstream/next:packages/graphics/vulkan/glslang/package.mk:1-24

```
    1  # SPDX-License-Identifier: GPL-2.0-only
    2  # Copyright (C) 2021-present Frank Hartung (supervisedthinking (@) gmail.com)
    3  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
    4  
    5  PKG_NAME="glslang"
    6  # The SPIRV-Tools & SPIRV-Headers pkg_version/s need to match the compatible (known_good) glslang pkg_version.
    7  # https://raw.githubusercontent.com/KhronosGroup/glslang/${PKG_VERSION}/known_good.json
    8  # When updating glslang pkg_version please update to the known_good spirv-tools & spirv-headers pkg_version/s.
    9  PKG_VERSION="16.5.0"
   10  PKG_SHA256="01af17195fbeb59e39e31e9506de35bb39dfd35807ea0c9a1a99d7d1183ddd45"
   11  PKG_LICENSE="BSD-3-Clause AND BSD-2-Clause AND MIT AND Apache-2.0"
   12  PKG_SITE="https://github.com/KhronosGroup/glslang"
   13  PKG_URL="https://github.com/KhronosGroup/glslang/archive/${PKG_VERSION}.tar.gz"
   14  PKG_DEPENDS_HOST="toolchain:host Python3:host"
   15  PKG_DEPENDS_TARGET="toolchain Python3"
   16  PKG_LONGDESC="Khronos-reference front end for GLSL/ESSL, partial front end for HLSL, and a SPIR-V generator."
   17  PKG_DEPENDS_UNPACK="spirv-headers spirv-tools"
   18  
   19  PKG_CMAKE_OPTS_COMMON="-DBUILD_EXTERNAL=ON \
   20                         -DENABLE_GLSLANG_JS=OFF \
   21                         -DENABLE_RTTI=OFF \
   22                         -DENABLE_EXCEPTIONS=OFF \
   23                         -DENABLE_OPT=ON \
   24                         -DENABLE_PCH=ON \
```

## excerpt: 8ebaf8daad:scripts/update_packages (whole)

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  # Based on work by ToKe79 and Shanti Gilbert
    6  
    7  OPTIONS="distributions/ROCKNIX/options"
    8  PACKAGES=("projects/ROCKNIX/packages/virtual/emulators/package.mk" \
    9            "projects/ROCKNIX/packages/virtual/es-themes/package.mk" \
   10            "projects/ROCKNIX/packages/virtual/gamesupport/package.mk" )
   11  BLOCKLIST="config/blocklist"
   12  
   13  update_packages() {
   14    for p in $PACKAGES_ALL
   15    do
   16      PKG_PATH="./projects/ROCKNIX/packages"
   17      echo "Operating on ${p}"
   18      f=$(find ${PKG_PATH} -type d -name "${p}")
   19      if [ "$(grep ${p} ${BLOCKLIST})" ]
   20      then
   21        echo "Skipping ${p}"
   22        continue
   23      fi
   24      f="${f}/package.mk"
   25      echo "${p}: ${f}"
   26      if [ ! "${p}" ] && [ ! "${f}" ]
   27      then
   28        echo "Package not found, skipping."
   29        continue
   30      fi
   31      source config/options "${p}"
   32      source "${f}"
   33      PKG_SITE=$(echo ${PKG_URL} | sed 's/\/archive.*//g')
   34      [ -n "${PKG_GIT_BRANCH}" ] && PKG_GIT_CLONE_BRANCH="${PKG_GIT_BRANCH}"
   35      [ -n "${PKG_GIT_CLONE_BRANCH}" ] && GIT_HEAD="heads/${PKG_GIT_CLONE_BRANCH}" || GIT_HEAD="HEAD"
   36       UPS_VERSION=`git ls-remote ${PKG_SITE} | grep ${GIT_HEAD}$ | awk '{ print substr($1,1,40) }'`
   37      if [ "${UPS_VERSION}" == "${PKG_VERSION}" ]; then
   38        echo "${PKG_NAME} is up to date (${UPS_VERSION})"
   39      else
   40        if [ "${UPS_VERSION}" ]; then
   41          echo "${PKG_NAME} updated from ${PKG_VERSION} to ${UPS_VERSION}"
   42          sed -i "s/PKG_VERSION=\"${PKG_VERSION}/PKG_VERSION=\"${UPS_VERSION}/" $f
   43        else
   44          echo "Could not find version, not updating ${PKG_NAME}."
   45        fi
   46      fi
   47  
   48      if [[ ! "${PKG_URL}" =~ git$ ]]
   49      then
   50       if grep -q PKG_SHA256 "${f}"; then
   51         echo "PKG_SHA256 exists on ${f}, clearing"
   52         sed -i "/PKG_SHA256=.*\$/d" ${f}
   53       fi
   54       source "${f}"
   55       ./scripts/get "${PKG_NAME}" >/dev/null
   56       if [ "${p}" != "linux" ]; then
   57         SHA=$(cat ./${SOURCES}/${PKG_NAME}/${PKG_NAME}-${UPS_VERSION}.*.sha256 2>/dev/null ||:)
   58       else
   59         SHA=$(cat ./${SOURCES}/${PKG_NAME}/linux-$LINUX-${UPS_VERSION}.tar.gz.sha256 2>/dev/null ||:)
   60       fi
   61       sed -e "/PKG_VERSION=\"${UPS_VERSION}\"/{ N; s/PKG_VERSION=\"${UPS_VERSION}\".*PKG_SHA256=\"\"/PKG_VERSION=\"${UPS_VERSION}\"\nPKG_SHA256=\"${SHA}\"/;}" -i ${f}
   62     else
   63       sed "/^PKG_SHA256=/d" -i ${f}
   64     fi
   65    done
   66  }
   67  
   68  
   69  source "${OPTIONS}"
   70  
   71  if [ ! "${1}" ]
   72  then
   73    for package in "${PACKAGES[@]}"
   74    do
   75      source "${package}"
   76      PACKAGES_ALL=" ${PKG_DEPENDS_TARGET}"
   77      update_packages
   78    done
   79  else
   80    PACKAGES_ALL="$*"
   81    update_packages
   82  fi
   83  
```

## excerpt: 8ebaf8daad:scripts/get_archive:1-60

```
    1  # SPDX-License-Identifier: GPL-2.0-only
    2  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    3  
    4  _get_file_already_downloaded() {
    5    { [ ! -f "${PACKAGE}" ] || [ ! -f "${STAMP_URL}" ] || [ ! -f "${STAMP_SHA}" ]; } && return 1
    6    { [ -n "${PKG_SHA256}" ] && [ "$(cat ${STAMP_SHA} 2>/dev/null)" != "${PKG_SHA256}" ]; } && return 1
    7    return 0
    8  }
    9  
   10  # Latest file already present, exit now...
   11  _get_file_already_downloaded && exit 0
   12  
   13  lock_source_dir "${1}"
   14  
   15  # Check again in case of concurrent access - if nothing needs to be downloaded, exit now...
   16  _get_file_already_downloaded && exit 0
   17  
   18  # At this point, we need to download something...
   19  build_msg "CLR_GET" "GET" "${1} (archive)" "indent"
   20  
   21  pkg_lock_status "GETPKG" "${PKG_NAME}" "unpack" "downloading package..."
   22  
   23  PACKAGE_MIRROR="${DISTRO_MIRROR}/${PKG_SOURCE_NAME}"
   24  [ "${VERBOSE}" != "yes" ] && WGET_OPT=-q
   25  WGET_CMD="wget --secure-protocol=TLSv1_2 --output-file=- --timeout=30 --tries=3 --passive-ftp --no-check-certificate -c ${WGET_OPT} --progress=bar:force --retry-connrefused --waitretry=5 --retry-on-http-error=429,500,502,503,504 --show-progress -O ${PACKAGE}"
   26  
   27  # unset LD_LIBRARY_PATH to stop wget from using toolchain/lib and loading libssl.so/libcrypto.so instead of host libraries
   28  unset LD_LIBRARY_PATH
   29  
   30  rm -f "${STAMP_URL}" "${STAMP_SHA}"
   31  
   32  PKG_URLS="${PKG_URL}"
   33  if [ -n "${PACKAGE_MIRROR}" ]
   34  then
   35    PKG_URLS="${PKG_URL} ${PACKAGE_MIRROR}"
   36  fi
   37  
   38  NBWGET=10
   39  while [ ${NBWGET} -gt 0 ]; do
   40    for url in ${PKG_URLS}; do
   41      rm -f "${PACKAGE}"
   42      if ${WGET_CMD} "${url}"; then
   43        CALC_SHA256=$(sha256sum "${PACKAGE}" | cut -d" " -f1)
   44  
   45        [ -z "${PKG_SHA256}" -o "${PKG_SHA256}" = "${CALC_SHA256}" ] && break 2
   46  
   47        build_msg "CLR_WARNING" "WARNING" "Incorrect checksum calculated on downloaded file: got ${CALC_SHA256} wanted ${PKG_SHA256}"
   48      fi
   49    done
   50    NBWGET=$((NBWGET - 1))
   51  done
   52  
   53  if [ ${NBWGET} -eq 0 ]; then
   54    die "\nCannot get ${1} sources : ${PKG_URL}\nTry later!"
   55  else
   56    build_msg "CLR_INFO" "INFO" "Calculated checksum: ${CALC_SHA256}"
   57    echo "${PKG_URL}" > "${STAMP_URL}"
   58    echo "${CALC_SHA256}" > "${STAMP_SHA}"
   59  fi
   60  
```

## excerpt: 52e6794ba7:scripts/get_archive:1-20 (T5's branch, merging before this one)

```
    1  # SPDX-License-Identifier: GPL-2.0-only
    2  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    3  
    4  # An archive is used only when its bytes match the recipe's PKG_SHA256, and it is
    5  # fetched over verified TLS: a recipe without a checksum fails here, before the
    6  # cache or the network is consulted (D-WORKFLOW-193, #834).
    7  if [ -z "${PKG_SHA256}" ]; then
    8    die "\nCannot get ${1} sources: its recipe has no PKG_SHA256, so the archive cannot be verified (D-WORKFLOW-193)"
    9  fi
   10  
   11  _get_file_already_downloaded() {
   12    { [ ! -f "${PACKAGE}" ] || [ ! -f "${STAMP_URL}" ] || [ ! -f "${STAMP_SHA}" ]; } && return 1
   13    [ "$(cat ${STAMP_SHA} 2>/dev/null)" != "${PKG_SHA256}" ] && return 1
   14    return 0
   15  }
   16  
   17  # Latest file already present, exit now...
   18  _get_file_already_downloaded && exit 0
   19  
   20  lock_source_dir "${1}"
```

## excerpt: 8ebaf8daad:distributions/ROCKNIX/options:180-190

```
  180    HTOP_TOOL="yes"
  181  
  182  # btop tool (yes / no)
  183    BTOP_TOOL="yes"
  184  
  185  # Distribution Specific source location
  186    DISTRO_MIRROR="https://github.com/ROCKNIX/distribution-sources/releases/download/sources-v2"
  187    DISTRO_SRC="https://sources.libreelec.tv/$DISTRO_VERSION"
  188  
  189  # Default size of system partition, in MB, eg. 512
  190    SYSTEM_SIZE=2048
```

## excerpt: 8ebaf8daad:tools/fork-package-freshness:36-101

```
   36  #   # freshness: pinned -- <why>
   37  # and is reported PINNED. A recipe with no PKG_VERSION of its own sources
   38  # upstream's generic recipe (INHERITED); one with no PKG_URL is ours (LOCAL).
   39  set -uo pipefail
   40  
   41  ROOT=$(cd "$(dirname "$0")/.." && pwd)
   42  HEAD_REF=${FRESHNESS_HEAD:-next}
   43  BASE_REF=${FRESHNESS_BASE:-upstream/next}
   44  EXTRA_PACKAGES="projects/ROCKNIX/packages/network/rclone"
   45  
   46  var() { grep -m1 "^${2}=" "$1" | cut -d'"' -f2; }
   47  newest() { sort -V | tail -1; }
   48  release_only() { grep -E '^[0-9]+(\.[0-9]+)+$'; }          # no rc, alpha, beta
   49  tag_version() { sed -E 's/^[^0-9]*//; s/_/./g'; }          # v1.2.0, libpsl-0.21.0, v3_3_12
   50  github_repo() { sed -nE 's#^https?://github\.com/([^/]+/[^/#?]+).*#\1#p' <<<"$1" | sed 's/\.git$//'; }
   51  
   52  latest_github() {  # <owner/repo>
   53      local v
   54      v=$(gh api "repos/$1/releases/latest" --jq .tag_name 2>/dev/null | tag_version | release_only)
   55      [ -n "$v" ] && { echo "$v"; return; }
   56      gh api "repos/$1/tags?per_page=50" --jq '.[].name' 2>/dev/null | tag_version | release_only | newest
   57  }
   58  latest_codeberg() {  # <owner/repo>
   59      local tags
   60      tags=$(curl -fsSL --max-time 30 "https://codeberg.org/api/v1/repos/$1/tags?<query cut> 2>/dev/null) || return 1
   61      python3 -c 'import json, sys; print("\n".join(tag["name"] for tag in json.load(sys.stdin)))' <<<"$tags" 2>/dev/null \
   62          | tag_version | release_only | newest
   63  }
   64  latest_gnome() {  # <module>
   65      curl -fsSL --max-time 30 "https://download.gnome.org/sources/$1/cache.json" 2>/dev/null | python3 -c '
   66  import json, sys, re
   67  d = json.load(sys.stdin); p = sys.argv[1]
   68  vs = [v for v in d[2].get(p, []) if re.fullmatch(r"\d+\.\d+(\.\d+)?", v)]
   69  vs = [v for v in vs if int(v.split(".")[1]) % 2 == 0]
   70  vs.sort(key=lambda s: [int(x) for x in s.split(".")])
   71  print(vs[-1] if vs else "")' "$1"
   72  }
   73  latest_listing() {  # <directory url> <name>
   74      curl -fsSL --max-time 30 "$1" 2>/dev/null | grep -oE "$2-[0-9]+(\.[0-9]+)+\.tar" | sed -E "s/^$2-//; s/\.tar$//" | newest
   75  }
   76  latest_webkitgtk() {
   77      curl -fsSL --max-time 30 https://webkitgtk.org/releases/ 2>/dev/null \
   78          | grep -oE 'webkitgtk-2\.[0-9]*[02468]\.[0-9]+\.tar\.xz' | sed -E 's/^webkitgtk-//; s/\.tar\.xz$//' | newest
   79  }
   80  latest_ruby() {  # <recipe version, or a series X.Y> -- newest in that minor series
   81      local series=$1
   82      [[ $series =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] && series=${series%.*}
   83      gh api "repos/ruby/ruby/tags?per_page=100" --jq '.[].name' 2>/dev/null | grep -E "^v${series//./_}_[0-9]+$" | tag_version | newest
   84  }
   85  commits_behind() {  # <owner/repo> <sha>
   86      gh api "repos/$1/compare/$2...HEAD" --jq 'if .ahead_by == 0 then "0 behind"
   87          else "\(.ahead_by) behind \(.commits[-1].sha[0:10]) (\(.commits[-1].commit.committer.date[0:10]))" end' 2>/dev/null
   88  }
   89  packages() {
   90      # Only build-engine recipe roots; docs/ holds immutable historical fixtures.
   91      git -C "$ROOT" diff --name-only --diff-filter=A "$BASE_REF" "$HEAD_REF" -- packages projects | sed -n 's|/package.mk$||p'
   92      for p in $EXTRA_PACKAGES; do echo "$p"; done
   93  }
   94  
   95  if [ "${1:-}" = "--list" ]; then packages; exit 0; fi
   96  
   97  rc=0
   98  printf '%-26s %-14s %-14s %s\n' PACKAGE RECIPE LATEST VERDICT
   99  while read -r d; do
  100      name=$(basename "$d")
  101      if [ $# -gt 0 ]; then case " $* " in *" $name "*) ;; *) continue ;; esac; fi
```

## excerpt: 8ebaf8daad:tools/pkgcheck:134-170

```
  134      if [ "${intertwined}" = "N" -a -z "${funcname}" -a ${fc} -ge 1 ]; then
  135        log "${filename}" ${lc} "WARN" "intertwined vars & funcs" "${line}"
  136        intertwined=Y
  137      fi
  138  
  139      [[ "${line}" =~ ^[[:space:]]*PKG_.*=\" ]] && isassign=Y
  140  
  141      process_line "$1" "${lc}" "${line}" "${isassign}" "${funcname}"
  142  
  143      [[ "${line}" =~ (\"$|\"[[:space:]]*$|\"[[:space:]]*#.*$) ]] && isassign=N
  144      [[ "${line}" =~ (^}|^[[:space:]]*}) ]] && funcname=
  145    done <"${filename}"
  146  
  147    # Duplicate function check
  148    while read -r count line; do
  149      [ -n "${line}" ] && log "${filename}" 0 "FAIL" "duplicate function def" "${line}"
  150    done <<<"$(grep -E ".*() {" "${filename}" | sed 's/[[:space:]]*{.*//' | sort | uniq -c | grep -v ^[[:space:]]*1[[:space:]])"
  151  }
  152  
  153  TARGET_FUNCS="$(init_target_funcs)"
  154  
  155  if [ $# -ne 0 ]; then
  156    for arg in ${@}; do
  157      for p in $(find packages projects -type f -path */${arg}/package.mk | sort); do
  158        echo -en "${TXCLR}${p}...\r" >&2
  159        process_pkg "${p}"
  160      done
  161    done
  162  else
  163    for p in $(find packages projects -type f -name package.mk | sort); do
  164      echo -en "${TXCLR}${p}...\r" >&2
  165      process_pkg "${p}"
  166    done
  167  fi
  168  echo -en "${TXCLR}" >&2
  169  [ ${FAILS} -eq 0 ]
  170  
```

## output: effective.txt: every row whose checksum is empty or unset beside a non-git URL

```
GENERIC_X64 libfmt version=[9.1.0] sha=[] shaset=yes arch=[any] url=[https://github.com/fmtlib/fmt/archive/9.1.0.tar.gz]
GENERIC_X64 simple-http-server version=[0.8.0] sha=[] shaset= arch=[any] url=[https://github.com/TheWaWaR/simple-http-server/releases/download/v0.8.0/x86_64-unknown-linux-musl-simple-http-server]
H700 libfmt version=[9.1.0] sha=[] shaset=yes arch=[any] url=[https://github.com/fmtlib/fmt/archive/9.1.0.tar.gz]
H700 atf version=[2.12.0] sha=[] shaset= arch=[arm aarch64] url=[https://github.com/ARM-software/arm-trusted-firmware/archive/v2.12.0.tar.gz]
```

## output: effective.txt: the rows whose pin differs between the three plans

```
GENERIC_X64 libfmt version=[9.1.0] sha=[] shaset=yes arch=[any] url=[https://github.com/fmtlib/fmt/archive/9.1.0.tar.gz]
H700 libfmt version=[9.1.0] sha=[] shaset=yes arch=[any] url=[https://github.com/fmtlib/fmt/archive/9.1.0.tar.gz]
SM8550 libfmt version=[12.2.0] sha=[8b852bb5aa6e7d8564f9e81394055395dd1d1936d38dfd3a17792a02bebd7af0] shaset=yes arch=[any] url=[https://github.com/fmtlib/fmt/archive/12.2.0.tar.gz]
```

## output: probe/head.txt: every row that did not answer 200 or a redirect

```
libaio 404  716c7059703247344eb066b54ecbc3ca2134f0103307192e6c2b7dab5f9528ab https://pagure.io/libaio/archive/libaio-0.3.113/libaio-libaio-0.3.113.tar.gz
rocknix-abl 404  64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7 https://github.com/ROCKNIX/abl/releases/download/v1.2/rocknix-abl-v1.2.tar.gz
samba 000  09bb56db4ce003cafdbebe9bad368c4f4ff1945f732d18077d52f36ab20cef88 https://download.samba.org/pub/samba/stable/samba-4.21.0.tar.gz
```

## output: probe/head.txt: the status-code histogram

```
1 000
82 200
25 301
118 302
2 404
```

## output: probe/controls.txt

```
control 404 https://github.com/zhang-ray/portaudio/archive/64d1bf913433d7a2835526b80a93487d5038cb8e.tar.gz
control 200 https://www.kernel.org/pub/software/utils/pciutils/pciutils-3.15.0.tar.xz
```

## output: probe/fetch.txt: every redirected archive that did not match

```
atf NO-SHA got=30abf4da07418ad0f840369c3e64dc6a0bc6a936d53a213ce10783f3d1a3430f
libfmt NO-SHA got=5dea48d1fcddc3ec571ce2058e13910a0d4a6bab4cc09a809d8b1dd1c88ae6f2
simple-http-server NO-SHA got=a16d73db4b33edc6aada0bb54088773dba8cb4d02eaa13364559552072d628cd
(and 140 rows `sha-match`)
```

## output: probe/git.txt

```
apitrace rc=0 refs=588 pin-is-a-ref-tip=0 pin=45a005875d34 https://github.com/apitrace/apitrace.git
fex-emu rc=0 refs=5126 pin-is-a-ref-tip=1 pin=e869aa644a16 https://github.com/FEX-Emu/FEX.git
gamescope rc=0 refs=1478 pin-is-a-ref-tip=1 pin=fa0b4d334207 https://github.com/ValveSoftware/gamescope.git
gmu rc=0 refs=21 pin-is-a-ref-tip=0 pin=3aed18be8a50 https://github.com/jhe2/gmu.git
libplacebo rc=0 refs=241 pin-is-a-ref-tip=0 pin=05ac2cca6571 https://code.videolan.org/videolan/libplacebo.git
librashader rc=0 refs=2506 pin-is-a-ref-tip=0 pin=76462c030b75 https://github.com/SnowflakePowered/librashader.git
libxcb-cursor rc=0 refs=20 pin-is-a-ref-tip=1 pin=7b0fa99aa130 https://gitlab.freedesktop.org/xorg/lib/libxcb-cursor.git
moonlight rc=0 refs=288 pin-is-a-ref-tip=0 pin=a6bf7154a743 https://github.com/moonlight-stream/moonlight-embedded.git
textviewer rc=0 refs=4 pin-is-a-ref-tip=2 pin=fcbda2d1708e https://github.com/ROCKNIX/TvTextViewer.git
wxwidgets rc=0 refs=7234 pin-is-a-ref-tip=1 pin=db1005db3dea https://github.com/wxWidgets/wxWidgets.git
```

## output: base-merge.txt: the CONFLICT lines (the whole tree; 9 of them on this slice's paths)

```
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/emulators/libretro/fbalpha2012-lr/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/emulators/libretro/fbalpha2019-lr/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/emulators/libretro/fbneo-lr/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/emulators/libretro/mame2003-plus-lr/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/emulators/libretro/mame2010-lr/package.mk
CONFLICT (modify/delete): projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/package.mk deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/package.mk left in tree.
CONFLICT (implicit dir rename): Existing file/dir at projects/ROCKNIX/packages/emulators/standalone/azahar-sa/config/GENERIC_X64 in the way of implicit directory rename(s) putting the following path(s) there: projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/config/GENERIC_X64.
CONFLICT (modify/delete): projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/config/RK3566/settings.ini deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/config/RK3566/settings.ini left in tree.
CONFLICT (file/directory): directory in the way of projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/config/RK3566 from upstream/next; moving it to projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/config/RK3566~upstream_next instead.
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/graphics/cairo/package.mk
CONFLICT (modify/delete): projects/ROCKNIX/packages/graphics/glslang/package.mk deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/graphics/glslang/package.mk left in tree.
CONFLICT (modify/delete): projects/ROCKNIX/packages/graphics/spirv-headers/package.mk deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/graphics/spirv-headers/package.mk left in tree.
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/graphics/spirv-tools/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/lang/gcc/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-base/package.mk
CONFLICT (add/add): Merge conflict in projects/ROCKNIX/packages/multimedia/gstreamer/gstreamer/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/network/networkmanager/config/NetworkManager.conf
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/rocknix/config/system/configs/system.cfg
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/rocknix/profile.d/001-functions
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/rocknix/sources/post-update
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/rocknix/sources/scripts/factoryreset
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh
CONFLICT (modify/delete): projects/ROCKNIX/packages/rust/cbindgen/package.mk deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/rust/cbindgen/package.mk left in tree.
CONFLICT (modify/delete): projects/ROCKNIX/packages/sysutils/busybox/sysctl.d/99-coredump.conf deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/sysutils/busybox/sysctl.d/99-coredump.conf left in tree.
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/input_sense
CONFLICT (modify/delete): projects/ROCKNIX/packages/sysutils/systemd/config/sysctl.d/rocknix.conf deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/sysutils/systemd/config/sysctl.d/rocknix.conf left in tree.
CONFLICT (modify/delete): projects/ROCKNIX/packages/tools/rocknix-abl/package.mk deleted in upstream/next and modified in 8ebaf8daad.  Version 8ebaf8daad of projects/ROCKNIX/packages/tools/rocknix-abl/package.mk left in tree.
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/ui/emulationstation/package.mk
CONFLICT (content): Merge conflict in projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init
```

## output: pkgcheck: the FAIL lines, the tree's copy then T6's

```
FAIL rc=1 moonlight [FAIL] ---: projects/ROCKNIX/packages/apps/moonlight/package.mk: duplicate function def : post_makeinstall_target();
FAIL rc=1 wireplumber [FAIL] ---: packages/audio/wireplumber/package.mk : duplicate function def : main =;[FAIL] ---: packages/audio/wireplumber/package.mk : duplicate function def : wireplumber.profiles =;[FAIL] 099: projects/ROCKNIX/packages/audio/wireplumber/package.mk: late binding violation : ref PKG_DIR;[FAIL] 100: projects/ROCKNIX/packages/audio/wireplumber/package.mk: late binding violation : ref PKG_DIR;[F
--
FAIL rc=1 moonlight [FAIL] ---: projects/ROCKNIX/packages/apps/moonlight/package.mk: duplicate function def : post_makeinstall_target();
FAIL rc=1 wireplumber [FAIL] 040: packages/audio/wireplumber/package.mk : late binding violation : ref INSTALL;[FAIL] 048: packages/audio/wireplumber/package.mk : late binding violation : ref INSTALL;[FAIL] ---: packages/audio/wireplumber/package.mk : duplicate function def : main =;[FAIL] ---: packages/audio/wireplumber/package.mk : duplicate function def : wireplumber.profiles =;[FAIL] 043: projects/ROCKNIX/pack
FAIL rc=1 image [FAIL] 109: projects/ROCKNIX/packages/virtual/image/package.mk: late binding violation : ref INSTALL;[FAIL] 110: projects/ROCKNIX/packages/virtual/image/package.mk: late binding violation : ref INSTALL;
```

## output: units-exec.txt

```
ABSENT /opt/etc/init.d/rc.unslung  (projects/ROCKNIX/packages/tools/entware/system.d/entware.service)
ABSENT /usr/bin/batteryplus-init  (projects/ROCKNIX/packages/tools/batteryplus/system.d/batteryplus.service)
ABSENT /usr/bin/batteryplus  (projects/ROCKNIX/packages/tools/batteryplus/system.d/batteryplus.service)
ABSENT /usr/bin/inputplumber  (projects/ROCKNIX/packages/tools/inputplumber/sources/usr/lib/systemd/system/inputplumber.service)
ABSENT /usr/lib/xorg/xorg-configure  (projects/ROCKNIX/packages/x11/xserver/xwayland/system.d/xorg-configure@.service)
present /bin/kill
present /bin/mkdir
present /bin/sh
present /usr/bin/bash
present /usr/bin/fluidsynth
present /usr/bin/installer
present /usr/bin/mpv_sense
present /usr/bin/openssl-config
present /usr/bin/pipewire-pulse
present /usr/bin/rocknix-bluetooth
present /usr/bin/rocknix-touchscreen-keyboard
present /usr/bin/seatd
present /usr/bin/sixaxis-helper.sh
present /usr/bin/ssh-keygen
present /usr/bin/start_syncthing.sh
present /usr/bin/sway.sh
present /usr/bin/sway-touch.sh
present /usr/bin/xorg-launch
present /usr/lib/bluetooth/bluetoothd
present /usr/lib/iwd
present /usr/lib/sway/sway-config
present /usr/sbin/avahi-daemon
present /usr/sbin/NetworkManager
present /usr/sbin/nmbd
present /usr/sbin/smbd
present /usr/sbin/sshd
present /usr/sbin/tailscaled
present /usr/sbin/zerotier-join.sh
present /usr/sbin/zerotier-one
```

## output: update-set: this slice's names in RK3588's set, then config/blocklist

```
box64
box86
control-gen
gamecontrollerdb
jstest-sdl
moonlight
portmaster
rocknix-hotkey
sdl2text
sdljoytest
sdltouchtest
sixaxis
wine
--
aethersx2-sa # package is EOL
amiberry # Updating breaks build packages
control-gen # package does not update
dolphin-sa # Wayland patch is now broken upstream
drastic-sa # Package is closed source bin
duckstation-lr # Libretro support removed from upstream.
duckstation-sa # Patches need to be reworked.
flycast-sa # Patched need to rebased
gptokeyb # Newer versions break hotkeys
gzdoom-sa # Stick to release versions.
idtech-lr # Just a dummy package
kronos-sa # Using the release version of kronos had better results.
melonds-sa # Broken OpenGL renderer upstream
minivmac-lr # Upstream Makefile change breaks build
mupen64plus-sa-ui-console # Causes segfaults
nanoboyadvance-sa # SDL version removed after this commit
np2kai # Last major commit before hiatus is broken.
openbor # Newer versions break controls, needs research.
pico-8 # Metapackage, doesn't need to update
portmaster # Manually update version
ppsspp-sa # Manually update to release versions.
retroarch # Manually update to release versions.
rpcs3-sa # Need to update to llvm 16
scummvm-sa # Updating breaks build packages
tic80-lr # patches need to be rebased
vice-lr # Updating breaks build patches
vice-sa # Doesn't support updating with the script.
vita3k-sa # Should be manually updated.
mupen64plus-nx-lr #Upstream brakes video out. 
```

## output: q4c.txt (the freshness tool, rc 2)

```
PACKAGE                    RECIPE         LATEST         VERDICT
gamescope-glm              0af55ccecd98d4 119            PINNED: follows subprojects/glm.wrap at gamescope's pinned commit (bump both together) (119 behind 6f14f4792a (2026-04-07))
gamescope-stb              5736b15f7ea0ff 88             PINNED: follows subprojects/stb.wrap at gamescope's pinned commit (bump both together) (88 behind 003501f6d7 (2026-10-23))
mangohud-vulkan-headers    1.4.346        1.4.366        PINNED: follows subprojects/vulkan-headers.wrap at mangohud's pinned commit (bump both together) (latest 1.4.366)
mangohud-vulkan-utility-libraries 1.4.346        1.4.366        PINNED: follows subprojects/vulkan-utility-libraries.wrap at mangohud's pinned commit (bump both together) (latest 1.4.366)
libfreeaptx                                              INHERITED
opus                       1.5.2                         UNKNOWN: no resolver for ftp.osuosl.org, or it did not answer
strace                                                   UNKNOWN: PKG_URL without a PKG_VERSION
libfmt                                                   INHERITED
aethersx2-sa               1.5-3606                      UNKNOWN: no resolver for github.com, or it did not answer
glslang                    16.6.0         16.6.0         CURRENT
harfbuzz-icu                                             INHERITED
spirv-headers              496543121ce641 7              PINNED: follows glslang16.6.0 known_good.json; SPIRV-Tools DEPS names the same headers (#386) (7 behind fbf86836a9 (2026-10-21))
vulkan-headers             1.4.347        1.4.366        BEHIND
gst-plugins-bad                                          INHERITED
cloud-signin-window                                      LOCAL
raofflineproxy-libchdr     607694ca0812ed 2              PINNED: follows the third_party/libchdr submodule commit RAOfflineProxy names (fork #179) (2 behind 47d794151b (2026-10-11))
raofflineproxy-rcheevos    1433173220a7ea 15             PINNED: follows the third_party/rcheevos submodule commit RAOfflineProxy names (fork #179) (15 behind dfdc64ea03 (2026-10-17))
raofflineproxy             c7ebd1b6e777f3 15             BEHIND: 15 behind 45726b18c6 (2026-10-22)
cargo-snapshot             $(get_pkg_vers                LOCAL
cargo                      $(get_pkg_vers                LOCAL
cbindgen                   0.29.4         0.29.4         CURRENT
rust-std-snapshot          $(get_pkg_vers                LOCAL
rustc-snapshot             $(get_pkg_vers                LOCAL
gnutls                                                   INHERITED
file                       c5eb6d6        5.48           AHEAD of upstream's latest
i2c-tools                  4.3                           UNKNOWN: no resolver for www.kernel.org, or it did not answer
grub                       2.14-rc1                      UNKNOWN: no resolver for git.savannah.gnu.org, or it did not answer
miniupnpc                  2.3.3                         UNKNOWN: no resolver for miniupnp.free.fr, or it did not answer
qemu                       10.0.2                        UNKNOWN: no resolver for download.qemu.org, or it did not answer
rocknix-abl                1.2                           UNKNOWN: no resolver for github.com, or it did not answer
tllist                     1.1.0          1.1.0          CURRENT
mtdev                      1.1.6                         UNKNOWN: no resolver for sources.buildroot.net, or it did not answer
swaybg                     1.2.1          1.2.2          BEHIND
rclone                     1.75.2         1.75.2         CURRENT
```

## output: q4c-hash.txt (the hash pins' compare)

```
SDL2_gfx 29927b3 jjYBdx4IL/SDL2_gfx [jjYBdx4IL/SDL2_gfx master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
apitrace 45a005875d348b055d5b88dca285c109dee90457 apitrace/apitrace [apitrace/apitrace master fork=false archived=false] ahead ahead_by=84 behind_by=0 newest=2026-10-22
batteryplus 1c31e89ec1828d51710ad35a607bdfad7e18464e Mikhailzrick/knubat.components [Mikhailzrick/knubat.components main fork=false archived=false] ahead ahead_by=2 behind_by=0 newest=2026-10-15
box64 2f130fab1d6e1a4ee8a71dc60cfdfcc839ad192a ptitSeb/box64 [ptitSeb/box64 main fork=false archived=false] ahead ahead_by=429 behind_by=0 newest=2026-10-23
box86 39d3ed203323000c11f47b780f7468fa24a7185d ptitSeb/box86 [ptitSeb/box86 master fork=false archived=false] ahead ahead_by=7 behind_by=0 newest=2026-10-20
capsimg ed4cb0912fb1a2a0d5203111c6f6abd50d411b56 FrodeSolheim/capsimg [FrodeSolheim/capsimg master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
commander b3c008cac3bff9de54a3542cecc53cc271058744 ROCKNIX/commander [ROCKNIX/commander main fork=true archived=false] identical ahead_by=0 behind_by=0 newest=-
fbgrab 5c2481d2b67b634e4e611610c33d30ef796afe5d GunnarMonell/fbgrab [GunnarMonell/fbgrab master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
fex-emu e869aa644a16e4332cdc15c1ea0b4d13d482385d FEX-Emu/FEX [FEX-Emu/FEX main fork=false archived=false] ahead ahead_by=522 behind_by=0 newest=2026-10-24
gamecontrollerdb 42f28e22d20761e7004e8db91c4ad86402fdf600 gabomdq/SDL_GameControllerDB [mdqinc/SDL_GameControllerDB master fork=false archived=false] ahead ahead_by=30 behind_by=0 newest=2026-10-19
gamepadcalibration 2077e7af7e9a8c1df54af6f1959cb92daea03207 cdeletre/GPcal [cdeletre/GPcal main fork=false archived=false] diverged ahead_by=1 behind_by=8 newest=2024-12-21
gamepadtester 6ac49e67aa98fe3dd5c27f73306d65d4b7a82daa timre13/GamepadTester [timre13/GamepadTester master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
gamescope fa0b4d3342078f01eadff0193e09c3b561f40c03 ValveSoftware/gamescope [ValveSoftware/gamescope master fork=true archived=false] ahead ahead_by=197 behind_by=0 newest=2026-10-23
gamescope-glm 0af55ccecd98d4e5a8d1fad7de25ba429d60e863 g-truc/glm [g-truc/glm master fork=true archived=false] diverged ahead_by=119 behind_by=6 newest=2026-04-07
gamescope-stb 5736b15f7ea0ffb08dd38af21067c314d6a3aae9 nothings/stb [nothings/stb master fork=false archived=false] ahead ahead_by=88 behind_by=0 newest=2026-10-23
glfw e2c9264 glfw/glfw [glfw/glfw master fork=false archived=false] diverged ahead_by=1055 behind_by=627 newest=2026-08-03
gmu 3aed18be8a50873ccfb31d2b135b0d22442ded59 jhe2/gmu [jhe2/gmu sdl20 fork=false archived=false] ahead ahead_by=31 behind_by=0 newest=2026-08-02
joyutils b6703ebf04c839fc47f9e490b68c4d5d885f32f9 datrh/joyutils [datrh/joyutils master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
jstest-sdl f4fdf6daae687d19b303d8ba8809ff5a68bc33a4 ROCKNIX/jstest-sdl [ROCKNIX/jstest-sdl master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
libplacebo unknown: code.videolan.org is not GitHub
librashader 76462c030b75c4f2d56e5386c3d4d7d1128318b8 SnowflakePowered/librashader [SnowflakePowered/librashader master fork=false archived=false] ahead ahead_by=85 behind_by=0 newest=2026-10-11
libserialport 21b3dfe5f68c205be4086469335fd2fc2ce11ed2 sigrokproject/libserialport [sigrokproject/libserialport master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
libsndfile e486f20 libsndfile/libsndfile [libsndfile/libsndfile master fork=false archived=false] ahead ahead_by=50 behind_by=0 newest=2026-09-01
libvorbisidec a76e41f6ece93d10deac5f9ef3a84dce5b9c2a84 sezero/tremor [sezero/tremor sezero fork=false archived=false] ahead ahead_by=19 behind_by=0 newest=2025-10-12
libvpx df655cf4fb6c2a23b964544acd015cc715752830 webmproject/libvpx [webmproject/libvpx main fork=false archived=false] ahead ahead_by=794 behind_by=0 newest=2026-10-23
libxcb-cursor unknown: gitlab.freedesktop.org is not GitHub
libxmp 8201d26cf933688a8be64292457c429fd8e654ab libxmp/libxmp [libxmp/libxmp master fork=false archived=false] ahead ahead_by=425 behind_by=0 newest=2026-10-10
lsfg-vk 8b0da2661c6f3473a7fccc8ba643880050e71642 PancakeTAS/lsfg-vk [PancakeTAS/lsfg-vk migration fork=false archived=false] {"message":"No common ancestor between 8b0da2661c6f3473a7fccc8ba643880050e71642 and HEAD.","documentation_url":"https://docs.github.com/rest/commits/commits#compare-two-commits","status":"404"}compare-failed
luajit 1edc3e52b67eaf6ce5f809be8e17d6862594b8bc LuaJIT/LuaJIT [LuaJIT/LuaJIT v2.1 fork=false archived=false] ahead ahead_by=31 behind_by=0 newest=2026-10-21
mako-osd b131bc143f6b0f24d650f16bb88a11c7cb011c20 emersion/mako [emersion/mako master fork=false archived=false] ahead ahead_by=23 behind_by=0 newest=2026-06-30
mangohud 992103e4fb744897826de04ea00a2f71e7018214 flightlessmango/MangoHud [flightlessmango/MangoHud master fork=false archived=false] ahead ahead_by=216 behind_by=0 newest=2026-10-24
mkbootimg d2bb0af5ba6d3198a3e99529c97eda1be0b5a093 jbeich/platform_system_tools_mkbootimg [jbeich/platform_system_tools_mkbootimg master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
moonlight a6bf7154a743d4f74a1b377e730f188352a1b80c moonlight-stream/moonlight-embedded [moonlight-stream/moonlight-embedded master fork=false archived=false] ahead ahead_by=16 behind_by=0 newest=2026-06-06
mpv 41f6a645068483470267271e1d09966ca3b9f413 mpv-player/mpv [mpv-player/mpv master fork=false archived=false] ahead ahead_by=1293 behind_by=0 newest=2026-10-23
oga_controls 1604ee24150c1c5bb7c66bc4670919c2ad8f0064 christianhaitian/oga_controls [christianhaitian/oga_controls universal fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
opusfile 9d718345ce03b2fad5d7d28e0bcd1cc69ab2b166 xiph/opusfile [xiph/opusfile main fork=false archived=false] ahead ahead_by=19 behind_by=0 newest=2026-03-28
pyudev 5e00141 pyudev/pyudev [pyudev/pyudev master fork=false archived=false] ahead ahead_by=133 behind_by=0 newest=2026-10-06
rocknix-hotkey cc3a863199a71a350db05e9d0d0e646a8411332c ROCKNIX/rocknix-hotkey [ROCKNIX/rocknix-hotkey main fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
rocknix-splash 8c71126ceef702528c87a4c49625e64988609f26 pixelelated/splash [pixelelated/splash master fork=true archived=false] identical ahead_by=0 behind_by=0 newest=-
sdljoytest 811d9875e0c13e0c87d93351e69169bf74d28270 Wintermute0110/sdljoytest [Wintermute0110/sdljoytest master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
sdltouchtest b62dae0d6233869a4c70a9472bc1e93dec391f94 realchonk/sdl2-touch-test [realchonk/sdl2-touch-test master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
six 02c3bca benjaminp/six [benjaminp/six main fork=false archived=false] ahead ahead_by=21 behind_by=0 newest=2026-02-23
sixaxis f53b0ca28c35ebd71b54190f33eadcb8c3267186 RetroPie/sixaxis [RetroPie/sixaxis master fork=true archived=false] identical ahead_by=0 behind_by=0 newest=-
soundfont-generaluser 8fe2798 ROCKNIX/generaluser-gs [ROCKNIX/generaluser-gs main fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
spirv-tools ef96ed763b43b59b33b31b362f09a02b729fa1c9 KhronosGroup/SPIRV-Tools [KhronosGroup/SPIRV-Tools main fork=false archived=false] ahead ahead_by=73 behind_by=0 newest=2026-10-23
textviewer fcbda2d1708e9e2c650abc589ea8e7f1fe1d04d8 ROCKNIX/TvTextViewer [ROCKNIX/TvTextViewer master fork=false archived=false] identical ahead_by=0 behind_by=0 newest=-
waffle unknown: gitlab.freedesktop.org is not GitHub
wxwidgets db1005db3dea2c37a46fb455a9a02e37aa360751 wxWidgets/wxWidgets [wxWidgets/wxWidgets master fork=false archived=false] ahead ahead_by=1631 behind_by=0 newest=2026-10-23
x264 unknown: code.videolan.org is not GitHub
```

## output: record-stamps.txt: names with no stamp in any root (empty means none)

```
(none)
```

## output: grep-fixture.sh and each pattern's count on it (1 each)

```
eval "$cmd"
echo "$list" | xargs rm
if [ "$a" > 3 ]; then
rm -f /x; ln -s /y /x
echo ok >> /tmp/log
counts: eval 1, xargs 1, redirection 1, rm-then-ln 1
```
