# Analysis — M6.P2 T7, the generic packages the image builds

## Executive summary

The 243 generic recipes that a shipped or test image builds were read against three sources. **Every pin has a named mover:**

| Source | Rows | Mover |
| --- | ---: | --- |
| (a) ROCKNIX | 227 byte-identical to `upstream/next`; 16 the fork's own | the base merge |
| (b) LibreELEC master | 230 read: 61 behind it, 7 at the same version with different bytes, and 13 absent there (the 13 fork-added) | ROCKNIX's next LibreELEC merge, then the base merge |
| (c) the project | read for the 13 fork-introduced: **4 BEHIND, 9 CURRENT**; and for the 7 GitHub hash pins | the fork, for those 13 |

No pin moved; nothing under `packages/` changed.

**One defect would break builds:**
- **F-01:** `libfmt`'s ROCKNIX override empties `PKG_SHA256` for every plan but SM8550's.
- At `8ebaf8daad` the archive is fetched unverified.
- At T5's tip, which merges before this branch, GENERIC_X64 and H700 builds die at `libfmt`.
- The fix is one line: the checksum the live fetch, the cache stamp and ROCKNIX's mirror all agree on. Alternatively, the next base merge deletes the override: it is an orphan that ROCKNIX removed on 2026-10-11 (`6103571f67`).

**Four primary URLs are gone, and ROCKNIX's mirror covers each one (F-02 to F-05):**
- `wsdd2`'s repository was deleted;
- `newt`'s release host serves nothing;
- `libmpeg2`'s site answers 404;
- savannah's new cgit host refuses `configtools`' snapshot.

The rest:
- **F-06 to F-09:** four fork-introduced recipes are one patch release behind: `brotli`, `ruby`, `glib-networking`, `webkitgtk`.
- **F-10:** the sixteen fork-own recipes get proposed #645 rows.
- **F-11:** the record contradicts one plan entry: `btrfs-progs` is absent from the M7 GENERIC_X64 root and image.
- **F-12:** the inventory cannot see an override's pin.
- **F-13 to F-15:** three modernization rows:
  - two latent URL series cuts (F-13);
  - 22 http URLs (F-14);
  - five GitHub URLs on renamed, archived or forked repositories (F-15).

## Acceptance-criteria scorecard

| Bucket | Criteria | Met at stage C | Open (later stage) |
| --- | ---: | ---: | ---: |
| the folder, the lint, the plan file | 3 | 1 | 2 |
| the punch list at Phase 7, the hashes, the status | 2 | 0 | 2 |
| `01` § Scope | 1 | 1 | 0 |
| `02`'s coverage, checks, sweep, #644, proofs | 5 | 5 | 0 |
| `04`'s Q4, Q6 and Q7 | 2 | 2 | 0 |
| no `packages/` change, no deletion, `question:` on every item | 2 | 2 | 0 |
| the retro, the checkers | 2 | 0 | 2 |
| **Total** | 17 | 11 | 6 |

(`02` § Phase 2 lists the seventeen; the six open ones are stages D to H's by construction.)

## Code Quality Assessment

### Strengths

- **Checksums:** 235 of 235 archive recipes carry a top-level `PKG_SHA256`. 129 of the 132 redirected archives were fetched again today and matched it.
- **The fork's own recipes are documented in place:**
  - `woff2`'s two stale-upstream fixes;
  - `ruby`'s `# freshness: series 3.3` line with its reason;
  - `libyaml`'s seven-line ordering comment;
  - `webkitgtk`'s per-option reasons and its `-j4` memory cap.
- **The freshness tool's set equals the fork-added recipes exactly** (no orphans here).

### Concerns

- **An override can silently change a recipe's checksum to nothing** (F-01). No check reads the effective `PKG_SHA256` per plan. `pkgcheck` reads one file. The inventory reads reach.
- **The fetch's resilience is ROCKNIX's mirror, not the recipes:** four recipes would fail from an empty cache without it.

### Complexity Hotspots

`packages/web/webkitgtk/package.mk` (114 lines, the sign-in window's engine, #576) is the only fork-own recipe of size. Its options are each explained.

## Risk Assessment

| Risk | Likelihood | Impact | Where |
| --- | --- | --- | --- |
| GENERIC_X64 and H700 builds die at `libfmt` once T5's `get_archive` merges | certain, if T5 merges first and nothing changes | every build of two of the three images | F-01 |
| ROCKNIX drops a file from `sources-v2`, or the release moves | low | four recipes fail from an empty cache; the shared cache still holds each (D-INFRA-022) | F-02 to F-05 |
| a fork-introduced recipe ships a known-fixed bug of its patch release | low | per recipe | F-06 to F-09 |
| the PR series meets `packages/**` | certain at the first bucket | the series refused | F-10, #645 |

## Coverage Boundary

- **Read:** the 266 paths at `8ebaf8daad` (every row of `02` § Coverage table); `upstream/next`; LibreELEC master for all 266 paths; the 13 projects through the freshness tool; the 7 GitHub hash pins; one HEAD per effective URL; one streamed fetch per redirect; the mirror for five archives; the cache's stamps; the five M7 roots' `build/` and `.stamps/` listings; `viewplan` for five plans.
- **Not read:** the project release of the 227 untouched upstream-carried recipes. Their (c) cell says so, and their disposition names the base merge rather than claiming currency. Also not read:
  - the three non-GitHub hash pins' projects (`x264`, `configtools`, `dbussy`): `unknown`;
  - the 101 URLs that answered 200, whose bytes were not fetched (the brief's rule: the cache stamp and the recipe's checksum stand);
  - patches: T42's and T43's rows;
  - the overrides under `projects/` beyond their effect on a pin: T8's.
- **Not run:** a build, a guest, `make update`, `update-pkg`, `update-scan`.

## Finding Verification (Phase 4.5)

Each finding is attacked with what would make it wrong, and what was checked.

- **F-01** (`libfmt`'s empty checksum).
  - *Wrong if* `libfmt` is not in those plans: `viewplan` lists `install libfmt` and `build libfmt:host` in GENERIC_X64, H700 and SM8550, and the M7 roots have `libfmt-9.1.0` built for GENERIC_X64 and H700.
  - *Wrong if* the effective value is not empty: the per-plan expansion through `config/options libfmt` prints `-` for `PKG_SHA256` in three plans.
  - *Wrong if* T5's guard does not reach it: `scripts/get:24-53` dispatches an `http*` URL to `get_archive`, whose line 7 at `52e6794ba7` tests `-z "${PKG_SHA256}"` before `_get_file_already_downloaded`.
  - **Confirmed.** Severity **High**: certain to stop two images' builds once T5 merges, and a one-line fix.
- **F-02** (`wsdd2`).
  - *Wrong if* the 404 is HEAD-specific: a ranged GET is 404, and so is `gh api repos/Netgear/wsdd2`.
  - *Wrong if* the build fails: it does not (the mirror).
  - **Confirmed as a gone primary source, not a build failure.** Low.
- **F-03** (`newt`), **F-04** (`libmpeg2`), **F-05** (`configtools`).
  - *Wrong if* transient: `newt` 404 on HEAD and on a ranged GET; `libmpeg2` 404 after both redirects; `configtools` 400, 502 and 400 across three reads over six minutes.
  - **F-05 is the weakest:** a cgit host returning 400 may recover. Its bug says *refused on three reads*, not *gone*.
  - **Confirmed.** Low.
- **F-06 to F-09** (BEHIND).
  - *Wrong if* the tool misread the host: `ruby` follows its declared series (3.3.13 is in 3.3); `webkitgtk`'s listing and GNOME's `cache.json` are the hosts the tool names.
  - The CURRENT side was spot-checked on `libsoup` and `qrencode`.
  - **Confirmed.** Low (a patch release each, no known defect named).
- **F-10:** a disposition table, not a defect. **Confirmed** as #645's input.
- **F-11** (`btrfs-progs`).
  - *Wrong if* the M7 root is not the GENERIC_X64 build of the plan: it is `m7-signin-build-20261022-07` at `069fc27044`, whose image tar of 2026-10-23 is in its `target/`.
  - *Wrong if* the M7 tree's image recipe lacks the dependency: its `image/package.mk:14` names `btrfs-progs`.
  - The cause is not found by reading. **Confirmed as a contradiction, unexplained.** Low, a note for the coordinator (Q6's rule).
- **F-12** (the inventory and sourcing overrides).
  - *Wrong if* the inventory has an effective-pin column: it does not (its columns are `tree`, `path`, `area`, `tier`, `tier_note`, `overlap`, `language`, `lines`, `patches`, `last_fork_commit`, `last_upstream_commit`, `reach`, `reachable_by`, `buildable_by`, `shadowed_by`).
  - **Confirmed.** Low.
- **F-13** (the series cut).
  - *Wrong if* the versions cannot reach two digits: GNOME's libsoup minor is at 8, and `${PKG_VERSION:0:3}` of `3.10.0` is `3.1`; ruby's `3.3` series path is the same shape.
  - **Confirmed as latent.** Low.
- **F-14** (http).
  - *Wrong if* integrity rests on transport: it rests on `PKG_SHA256`, which every one of the 22 carries and which matched for each one fetched.
  - So it is a modernization row, not a defect. Low.
- **F-15** (renamed, archived and forked).
  - *Wrong if* the bytes changed: all five matched (the renamed three by fetch; `oniguruma` and `populatefs` by fetch, since both redirect).
  - **Confirmed as modernization.** Low.

Rule 4, asked of every PASS above (what would have made it a FAIL, and was it seen):
- (a) said *differs* or *absent* on exactly the 16;
- the probe said 301 and 404 on the two controls;
- `pkgcheck` said 1 on `sameboy-lr`;
- the stamp loop said *differs* on 19 old files and on `libfmt`;
- the fetch said `SHA-DIFFERS` on `libfmt`;
- the freshness tool said BEHIND on four.

## Renovation face

### Q1 Modernize

Every finding below is `Renovation`.
- **F-14:** 22 recipes fetch over http: `libyaml`, `usb-modeswitch`, `lzo`, `memtester`, `attr`, `configtools`, `fakeroot`, `intltool`, `libdaemon`, `pkg-config`, `popt`, `libmpeg2`, `libmnl`, `netbase`, `dmidecode`, `usbutils`, `itstool`, `syslinux`, `libSM`, `libXtst`, `libXxf86vm`, `xorg-launch-helper`. `glu`'s https URL is redirected to http (`mesa3d.org`).
  - Integrity holds by `PKG_SHA256`.
  - Two are the fork's to change: `dmidecode` (its recipe) and `syslinux` (its edited copy keeps upstream's URL).
  - The rest are upstream's (#585 candidates, D-WORKFLOW-164; submission held, D-WORKFLOW-165).
- **F-15:**
  - three URLs name renamed GitHub repositories (`lm_sensors`, `libfreeaptx`, `nss-mdns`);
  - one names an archived repository (`kkos/oniguruma`, last push 2025-04-24);
  - one names a personal fork (`kfix/populatefs`, a fork of `lipnitsk/populatefs`: portaudio's shape, #849).
  - LibreELEC master carries all five as they are, so they follow the base merge.
- **Neither class appears:**
  - no python2-era helper (the python group is `Python3`, `meson`, `setuptools` and their build tools);
  - no SourceForge download that fails except `libmpeg2`'s project site (F-04); the other five SourceForge redirects (`mpg123`, `libmodplug`, `soxr`, `libtirpc`, `rpcbind`) went to a mirror and matched.
- **The 16 fork-own recipes against `packages/README.md`:** each has the required fields. None needs a modernization; F-13 is a clarity row.

### Q2 Standards and best practices

- **`tools/pkgcheck` over the 243:** **243 PASS, 0 FAIL** with the tree's copy and with T6's widened copy (`44f64842b6`), as the brief expected. The baseline equals the result, so there is no delta to explain.
- `packaging-and-patches.md`'s required fields hold for every archive recipe. The one checksum rule broken is broken in an override (F-01).
- T6's two leads (`jre.zulu`, `mesa-reusable`) are T23's (#670); `wireplumber`'s parser case is #657's. None is read here.

### Q3 Bugs

**Five `bug`s, filed at stage D:**

| F | Recipe | The defect | Builds from an empty cache today | Copies of the bytes |
| --- | --- | --- | --- | --- |
| F-01 | `libfmt` (its override) | `PKG_SHA256=""` for 9.1.0 on every plan but SM8550's | yes, unverified; **no**, after T5's `get_archive` | live fetch, cache stamp, mirror: `5dea48d1...` |
| F-02 | `wsdd2` | `Netgear/wsdd2` deleted | yes, from the mirror | the mirror and the cache: `b0b6b315...` |
| F-03 | `newt` | `releases.pagure.org/newt/` serves no archive | yes, from the mirror | mirror, cache: `ef0ca9ee...` |
| F-04 | `libmpeg2` | the SourceForge project site's file is 404 | yes, from the mirror | mirror, cache: `dee22e89...` |
| F-05 | `configtools` | savannah's new cgit refuses the snapshot (400) | yes, from the mirror | mirror, cache: `6e4ebaa2...` |

**Nothing else:**
- no recipe whose `PKG_VERSION` and `PKG_URL` disagree (every URL interpolates `${PKG_VERSION}`, or for `gcc` and `opus` the override's);
- no archive recipe without a checksum at the recipe level;
- no stamp that disagrees with its recipe by URL, except `libfmt`'s empty value.

### Q4 Package currency

**The table, 243 rows**, also `q4-table.md` and `q4-pins.json`.

Dispositions:
- `follows the base merge; LibreELEC master at <v>`: **223** (61 with LibreELEC ahead);
- `follows the base merge; LibreELEC master carries it`: 6, the virtual packages;
- `... inherits harfbuzz`: 1;
- `current`: **9**, every one with (c) read;
- `fork's: Backlog bump proposed (#839's shape)`: **4** (F-06 to F-09).

No row reads `current` beside a `not read`. Seven same-version rows differ from LibreELEC master in bytes. Three are the fork's edits. Four are LibreELEC's commits after ROCKNIX's last LibreELEC merge, read from the API:
- `lz4` and `lzo` build shared libraries (2026-09-05);
- `gcc` names its compiler to ccache by the toolchain key (2026-10-12);
- `virtual/debug` reads `VALGRIND_SUPPORT` (2026-10-02).

Each arrives with the next base merge.

| Recipe path | Name | Pin (effective) | Shape | (a) upstream/next | (b) LibreELEC master | (c) the project | Disposition (the mover) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `packages/addons/addon-depends/chrome-depends/atk/package.mk` | `atk` | `2.38.0` | version | identical | `2.38.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.38.0` |
| `packages/addons/addon-depends/chrome-depends/cups/package.mk` | `cups` | `2.4.19` | version | identical | `2.4.20` (ours `2.4.19`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.4.20` |
| `packages/addons/addon-depends/chrome-depends/gtk3/package.mk` | `gtk3` | `3.24.52` | version | identical | `3.24.52` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.24.52` |
| `packages/addons/addon-depends/chrome-depends/harfbuzz-icu/package.mk` | `harfbuzz-icu` | `14.3.0` | inherited (sources harfbuzz) | identical | inherits harfbuzz (master `15.0.0`); recipe identical | not read: follows LibreELEC | follows the base merge; LibreELEC master inherits harfbuzz `15.0.0` |
| `packages/addons/addon-depends/chrome-depends/libXcursor/package.mk` | `libXcursor` | `1.2.3` | version | identical | `1.2.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.3` |
| `packages/addons/addon-depends/chrome-depends/libxss/package.mk` | `libxss` | `1.2.5` | version | identical | `1.2.5` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.5` |
| `packages/addons/addon-depends/chrome-depends/scrnsaverproto/package.mk` | `scrnsaverproto` | `1.2.2` | version | identical | `1.2.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.2` |
| `packages/addons/addon-depends/faad2/package.mk` | `faad2` | `2.11.2` | version | identical | `2.11.4` (ours `2.11.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.11.4` |
| `packages/addons/addon-depends/ffmpegx-depends/x264/package.mk` | `x264` | `0480cb05fa18` | hash | identical | `0480cb05fa18` (identical) | unknown: code.videolan.org is not GitHub | follows the base merge; LibreELEC master at `0480cb05fa18` |
| `packages/addons/addon-depends/ffmpegx-depends/x265/package.mk` | `x265` | `4.2` | version | identical | `4.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.2` |
| `packages/addons/addon-depends/hidapi/package.mk` | `hidapi` | `0.15.0` | version | identical | `0.15.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.15.0` |
| `packages/addons/addon-depends/jre-depends/apache-ant/package.mk` | `apache-ant` | `1.10.17` | version | identical | `1.10.18` (ours `1.10.17`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.10.18` |
| `packages/addons/addon-depends/libXft/package.mk` | `libXft` | `2.3.9` | version | identical | `2.3.9` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.3.9` |
| `packages/addons/addon-depends/multimedia-tools-depends/mpg123/package.mk` | `mpg123` | `1.33.7` | version | identical | `1.33.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.33.7` |
| `packages/addons/addon-depends/ntfs-3g_ntfsprogs/package.mk` | `ntfs-3g_ntfsprogs` | `2022.10.3` | version | identical | `2022.10.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2022.10.3` |
| `packages/addons/addon-depends/polkit/package.mk` | `polkit` | `127` | version | identical | `128` (ours `127`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `128` |
| `packages/addons/addon-depends/rsyslog-depends/libyaml/package.mk` | `libyaml` | `0.2.5` | version | differs (fork edit) | `0.2.5` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.2.5` |
| `packages/addons/addon-depends/snapcast-depends/libsodium/package.mk` | `libsodium` | `1.0.22` | version | identical | `1.0.22` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.22` |
| `packages/addons/addon-depends/system-tools-depends/depends/oniguruma/package.mk` | `oniguruma` | `6.9.10` | version | identical | `6.9.10` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.9.10` |
| `packages/addons/addon-depends/system-tools-depends/evtest/package.mk` | `evtest` | `1.36` | version | identical | `1.36` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.36` |
| `packages/addons/addon-depends/system-tools-depends/htop/package.mk` | `htop` | `3.5.2` | version | identical | `3.5.3` (ours `3.5.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.5.3` |
| `packages/addons/addon-depends/system-tools-depends/jq/package.mk` | `jq` | `1.8.2` | version | identical | `1.8.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.8.2` |
| `packages/addons/addon-depends/system-tools-depends/lm_sensors/package.mk` | `lm_sensors` | `3.6.2` | version | identical | `3.6.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.6.2` |
| `packages/addons/addon-depends/system-tools-depends/usb-modeswitch/package.mk` | `usb-modeswitch` | `2.6.2` | version | identical | `2.6.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.6.2` |
| `packages/addons/tools/btrfs-progs/package.mk` | `btrfs-progs` | `7.1` | version | identical | `7.3` (ours `7.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `7.3` |
| `packages/audio/alsa-topology-conf/package.mk` | `alsa-topology-conf` | `1.2.5.1` | version | identical | `1.2.5.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.5.1` |
| `packages/audio/fdk-aac/package.mk` | `fdk-aac` | `2.0.3` | version | identical | `3.0.0` (ours `2.0.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.0.0` |
| `packages/audio/flac/package.mk` | `flac` | `1.5.0` | version | identical | `1.5.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.5.0` |
| `packages/audio/fluidsynth/package.mk` | `fluidsynth` | `2.5.7` | version | identical | `2.6.1` (ours `2.5.7`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.6.1` |
| `packages/audio/ldacBT/package.mk` | `ldacBT` | `2.0.2.6` | version | identical | `2.0.2.6` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.0.2.6` |
| `packages/audio/libfreeaptx/package.mk` | `libfreeaptx` | `0.2.2` | version | identical | `0.2.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.2.2` |
| `packages/audio/libmodplug/package.mk` | `libmodplug` | `0.8.9.0` | version | identical | `0.8.9.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.8.9.0` |
| `packages/audio/libogg/package.mk` | `libogg` | `1.3.6` | version | identical | `1.3.6` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.6` |
| `packages/audio/libsamplerate/package.mk` | `libsamplerate` | `0.2.2` | version | differs (fork edit) | `0.2.2` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.2.2` |
| `packages/audio/openal-soft/package.mk` | `openal-soft` | `1.25.2` | version | identical | `1.25.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.25.2` |
| `packages/audio/opus/package.mk` | `opus` | `1.5.2` (a ROCKNIX override's; the generic recipe `1.6.1`) | version | identical | `1.6.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.6.1` |
| `packages/audio/sbc/package.mk` | `sbc` | `2.2` | version | identical | `2.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.2` |
| `packages/audio/soxr/package.mk` | `soxr` | `0.1.3` | version | identical | `96a8a450f46e` (ours `0.1.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `96a8a450f46e` |
| `packages/audio/speex/package.mk` | `speex` | `1.2.1` | version | identical | `1.2.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.1` |
| `packages/audio/speexdsp/package.mk` | `speexdsp` | `1.2.1` | version | identical | `1.2.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.1` |
| `packages/audio/wavpack/package.mk` | `wavpack` | `5.9.0` | version | identical | `5.9.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `5.9.0` |
| `packages/compress/7-zip/package.mk` | `7-zip` | `26.02` | version | identical | `26.05` (ours `26.02`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `26.05` |
| `packages/compress/brotli/package.mk` | `brotli` | `1.2.0` | version | absent (fork-added) | absent | BEHIND (latest `1.2.1`) | fork's: Backlog bump proposed (#839's shape), 1.2.0 -> 1.2.1 (F-06) |
| `packages/compress/bzip2/package.mk` | `bzip2` | `1.0.8` | version | identical | `1.0.8` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.8` |
| `packages/compress/libarchive/package.mk` | `libarchive` | `3.8.9` | version | identical | `3.8.10` (ours `3.8.9`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.8.10` |
| `packages/compress/lz4/package.mk` | `lz4` | `1.10.0` | version | identical | `1.10.0` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.10.0` |
| `packages/compress/lzo/package.mk` | `lzo` | `2.10` | version | identical | `2.10` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.10` |
| `packages/compress/pigz/package.mk` | `pigz` | `2.8` | version | identical | `2.8` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.8` |
| `packages/compress/zlib/package.mk` | `zlib` | `1.3.2` | version | identical | `1.3.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.2` |
| `packages/compress/zstd/package.mk` | `zstd` | `1.5.7` | version | identical | `1.5.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.5.7` |
| `packages/databases/sqlite/package.mk` | `sqlite` | `3.53.4` | version | identical | `3.54.1` (ours `3.53.4`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.54.1` |
| `packages/debug/gdb/package.mk` | `gdb` | `17.2` | version | identical | `18.1` (ours `17.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `18.1` |
| `packages/debug/libunwind/package.mk` | `libunwind` | `1.8.3` | version | identical | `1.8.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.8.3` |
| `packages/debug/memtester/package.mk` | `memtester` | `4.7.1` | version | identical | `4.7.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.7.1` |
| `packages/devel/arm-mem/package.mk` | `arm-mem` | `ee8ac1d56adb` | hash | identical | `ee8ac1d56adb` (identical) | at the default branch's HEAD | follows the base merge; LibreELEC master at `ee8ac1d56adb` |
| `packages/devel/asn1c/package.mk` | `asn1c` | `0.9.29` | version | identical | `0.9.29` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.9.29` |
| `packages/devel/attr/package.mk` | `attr` | `2.6.0` | version | identical | `2.6.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.6.0` |
| `packages/devel/autoconf-archive/package.mk` | `autoconf-archive` | `2024.10.16` | version | identical | `2024.10.16` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2024.10.16` |
| `packages/devel/autoconf/package.mk` | `autoconf` | `2.73` | version | identical | `2.73` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.73` |
| `packages/devel/automake/package.mk` | `automake` | `1.18.1` | version | identical | `1.19` (ours `1.18.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.19` |
| `packages/devel/binutils/package.mk` | `binutils` | `2.47` | version | identical | `2.47` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.47` |
| `packages/devel/bison/package.mk` | `bison` | `3.8.2` | version | identical | `3.8.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.8.2` |
| `packages/devel/ccache/package.mk` | `ccache` | `4.13.6` | version | identical | `4.14.2` (ours `4.13.6`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.14.2` |
| `packages/devel/cmake/package.mk` | `cmake` | `4.4.2` | version | identical | `4.4.4` (ours `4.4.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.4.4` |
| `packages/devel/configtools/package.mk` | `configtools` | `28ea239c53a2` | hash | identical | `28ea239c53a2` (identical) | unknown: git.savannah.gnu.org is not GitHub | follows the base merge; LibreELEC master at `28ea239c53a2` (F-05) |
| `packages/devel/crossguid/package.mk` | `crossguid` | `ca1bf4b810e2` | hash | identical | `ca1bf4b810e2` (identical) | at the default branch's HEAD | follows the base merge; LibreELEC master at `ca1bf4b810e2` |
| `packages/devel/elfutils/package.mk` | `elfutils` | `0.195` | version | identical | `0.197` (ours `0.195`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.197` |
| `packages/devel/fakeroot/package.mk` | `fakeroot` | `2.1.4` | version | identical | `2.1.4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.1.4` |
| `packages/devel/flex/package.mk` | `flex` | `2.6.4` | version | identical | `2.6.4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.6.4` |
| `packages/devel/fribidi/package.mk` | `fribidi` | `1.0.16` | version | identical | `1.0.17` (ours `1.0.16`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.17` |
| `packages/devel/gcem/package.mk` | `gcem` | `1.18.0` | version | identical | `1.18.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.18.0` |
| `packages/devel/gettext/package.mk` | `gettext` | `1.0` | version | identical | `1.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0` |
| `packages/devel/glib/package.mk` | `glib` | `2.89.3` | version | identical | `2.90.1` (ours `2.89.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.90.1` |
| `packages/devel/gmp/package.mk` | `gmp` | `6.3.0` | version | identical | `6.3.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.3.0` |
| `packages/devel/heimdal/package.mk` | `heimdal` | `f4faaeaba371` | hash | identical | `f4faaeaba371` (identical) | 727 commits behind the default branch | follows the base merge; LibreELEC master at `f4faaeaba371` |
| `packages/devel/hwdata/package.mk` | `hwdata` | `0.410` | version | identical | `0.412` (ours `0.410`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.412` |
| `packages/devel/intltool/package.mk` | `intltool` | `0.51.0` | version | identical | `0.51.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.51.0` |
| `packages/devel/json-c/package.mk` | `json-c` | `0.19` | version | identical | `0.19` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.19` |
| `packages/devel/libcap/package.mk` | `libcap` | `2.78` | version | identical | `2.78` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.78` |
| `packages/devel/libdaemon/package.mk` | `libdaemon` | `0.14` | version | identical | `0.14` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.14` |
| `packages/devel/libdisplay-info/package.mk` | `libdisplay-info` | `0.4.0` | version | identical | `0.4.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.4.0` |
| `packages/devel/libevent/package.mk` | `libevent` | `2.1.13` | version | identical | `2.1.13` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.1.13` |
| `packages/devel/libffi/package.mk` | `libffi` | `3.8.0` | version | identical | `3.8.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.8.0` |
| `packages/devel/libfmt/package.mk` | `libfmt` | GENERIC_X64-x86_64 `9.1.0`; H700-aarch64 `9.1.0`; H700-arm `9.1.0`; SM8550-aarch64 `12.2.0`; SM8550-arm `12.2.0` (a ROCKNIX override's case; the generic recipe `12.2.0`) | version | identical | `12.2.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `12.2.0` (F-01) |
| `packages/devel/libtool/package.mk` | `libtool` | `2.6.2` | version | identical | `2.6.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.6.2` |
| `packages/devel/m4/package.mk` | `m4` | `1.4.21` | version | identical | `1.4.21` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.4.21` |
| `packages/devel/mpc/package.mk` | `mpc` | `1.4.1` | version | identical | `1.4.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.4.1` |
| `packages/devel/mpdecimal/package.mk` | `mpdecimal` | `4.0.1` | version | identical | `4.0.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.0.1` |
| `packages/devel/mpfr/package.mk` | `mpfr` | `4.2.2` | version | identical | `4.2.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.2.2` |
| `packages/devel/pax-utils/package.mk` | `pax-utils` | `1.3.11` | version | identical | `1.3.11` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.11` |
| `packages/devel/pcre2/package.mk` | `pcre2` | `10.47` | version | identical | `10.49` (ours `10.47`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `10.49` |
| `packages/devel/pkg-config/package.mk` | `pkg-config` | `0.29.2` | version | identical | `0.29.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.29.2` |
| `packages/devel/popt/package.mk` | `popt` | `1.19` | version | identical | `1.19` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.19` |
| `packages/devel/readline/package.mk` | `readline` | `8.3` | version | identical | `8.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `8.3` |
| `packages/devel/ruby/package.mk` | `ruby` | `3.3.12` | version | absent (fork-added) | absent | BEHIND (latest `3.3.13`) | fork's: Backlog bump proposed (#839's shape), 3.3.12 -> 3.3.13 (F-07) |
| `packages/devel/slang/package.mk` | `slang` | `2.3.3` | version | identical | `2.3.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.3.3` |
| `packages/devel/talloc/package.mk` | `talloc` | `2.5.0` | version | identical | `2.5.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.5.0` |
| `packages/devel/unifdef/package.mk` | `unifdef` | `2.12` | version | absent (fork-added) | absent | CURRENT (latest `2.12`) | current |
| `packages/devel/xxHash/package.mk` | `xxHash` | `0.8.3` | version | identical | `0.8.4` (ours `0.8.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.8.4` |
| `packages/graphics/assimp/package.mk` | `assimp` | `6.0.5` | version | identical | `6.0.5` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.0.5` |
| `packages/graphics/glm/package.mk` | `glm` | `1.0.3` | version | identical | `1.0.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.3` |
| `packages/graphics/glmark2/package.mk` | `glmark2` | `2023.01` | version | identical | `2023.01` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2023.01` |
| `packages/graphics/glu/package.mk` | `glu` | `9.0.3` | version | identical | `9.0.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `9.0.3` |
| `packages/graphics/harfbuzz/package.mk` | `harfbuzz` | `14.3.0` | version | identical | `15.0.0` (ours `14.3.0`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `15.0.0` |
| `packages/graphics/jasper/package.mk` | `jasper` | `4.2.9` | version | identical | `4.2.9` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.2.9` |
| `packages/graphics/kmsxx/package.mk` | `kmsxx` | `bfb041620d8e` | hash | identical | `bfb041620d8e` (identical) | 4 commits behind the default branch | follows the base merge; LibreELEC master at `bfb041620d8e` |
| `packages/graphics/lcms2/package.mk` | `lcms2` | `2.19.1` | version | identical | `2.19.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.19.1` |
| `packages/graphics/libjpeg-turbo/package.mk` | `libjpeg-turbo` | `3.2.0` | version | identical | `3.2.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.2.0` |
| `packages/graphics/libraw/package.mk` | `libraw` | `0.22.2` | version | identical | `0.22.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.22.2` |
| `packages/graphics/openjpeg/package.mk` | `openjpeg` | `2.5.4` | version | absent (fork-added) | absent | CURRENT (latest `2.5.4`) | current |
| `packages/graphics/pango/package.mk` | `pango` | `1.58.2` | version | identical | `1.58.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.58.2` |
| `packages/graphics/tiff/package.mk` | `tiff` | `4.7.2` | version | identical | `4.7.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.7.2` |
| `packages/graphics/vulkan/vkmark/package.mk` | `vkmark` | `2025.01` | version | identical | `2025.01` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2025.01` |
| `packages/graphics/vulkan/volk/package.mk` | `volk` | `1.4.350` | version | identical | `1.4.350` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.4.350` |
| `packages/graphics/woff2/package.mk` | `woff2` | `1.0.2` | version | absent (fork-added) | absent | CURRENT (latest `1.0.2`) | current |
| `packages/lang/Python3/package.mk` | `Python3` | `3.14.7` | version | identical | `3.14.8` (ours `3.14.7`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.14.8` |
| `packages/lang/gcc/package.mk` | `gcc` | `15.2.0` (a ROCKNIX override's; the generic recipe `16.2.0`) | version | identical | `16.2.0` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `16.2.0` |
| `packages/multimedia/aom/package.mk` | `aom` | `3.14.1` | version | identical | `3.15.2` (ours `3.14.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.15.2` |
| `packages/multimedia/dav1d/package.mk` | `dav1d` | `1.5.4` | version | identical | `1.5.4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.5.4` |
| `packages/multimedia/gstreamer/gst-plugins-bad/package.mk` | `gst-plugins-bad` | `1.29.2` | version | identical | `1.29.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.29.2` |
| `packages/multimedia/gstreamer/gst-plugins-base/package.mk` | `gst-plugins-base` | `1.29.2` | version | identical | `1.29.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.29.2` |
| `packages/multimedia/gstreamer/gstreamer/package.mk` | `gstreamer` | `1.29.2` | version | identical | `1.29.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.29.2` |
| `packages/multimedia/libass/package.mk` | `libass` | `0.17.5` | version | identical | `0.17.5` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.17.5` |
| `packages/multimedia/libmpeg2/package.mk` | `libmpeg2` | `0.5.1` | version | identical | `0.5.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.5.1` (F-04) |
| `packages/network/ethtool/package.mk` | `ethtool` | `7.1` | version | identical | `7.2` (ours `7.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `7.2` |
| `packages/network/glib-networking/package.mk` | `glib-networking` | `2.90.0` | version | absent (fork-added) | absent | BEHIND (latest `2.90.1`) | fork's: Backlog bump proposed (#839's shape), 2.90.0 -> 2.90.1 (F-08) |
| `packages/network/iw/package.mk` | `iw` | `6.17` | version | identical | `6.17` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.17` |
| `packages/network/iwd/package.mk` | `iwd` | `3.12` | version | identical | `3.12` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.12` |
| `packages/network/libmnl/package.mk` | `libmnl` | `1.0.5` | version | identical | `1.0.5` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.5` |
| `packages/network/libnl/package.mk` | `libnl` | `3.12.0` | version | identical | `3.12.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.12.0` |
| `packages/network/libtirpc/package.mk` | `libtirpc` | `1.3.7` | version | identical | `1.3.8` (ours `1.3.7`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.8` |
| `packages/network/netbase/package.mk` | `netbase` | `6.5` | version | identical | `6.6` (ours `6.5`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.6` |
| `packages/network/nss-mdns/package.mk` | `nss-mdns` | `0.15.1` | version | identical | `0.15.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.15.1` |
| `packages/network/rpcbind/package.mk` | `rpcbind` | `1.2.9` | version | identical | `1.3.1` (ours `1.2.9`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.1` |
| `packages/network/rsync/package.mk` | `rsync` | `3.4.4` | version | identical | `3.5.1` (ours `3.4.4`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.5.1` |
| `packages/network/wireguard-tools/package.mk` | `wireguard-tools` | `1.0.20260223` | version | identical | `1.0.20260223` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.20260223` |
| `packages/network/wireless-regdb/package.mk` | `wireless-regdb` | `2026.05.30` | version | identical | `2026.09.03` (ours `2026.05.30`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2026.09.03` |
| `packages/network/wsdd2/package.mk` | `wsdd2` | `1.8.7` | version | identical | `1.9.2` (ours `1.8.7`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.9.2` (F-02) |
| `packages/print/freetype/package.mk` | `freetype` | `2.14.3` | version | identical | `2.15.0` (ours `2.14.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.15.0` |
| `packages/python/devel/Jinja2/package.mk` | `Jinja2` | `3.1.6` | version | identical | `3.1.6` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.1.6` |
| `packages/python/devel/Mako/package.mk` | `Mako` | `1.4.1` | version | identical | `1.4.3` (ours `1.4.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.4.3` |
| `packages/python/devel/MarkupSafe/package.mk` | `MarkupSafe` | `3.0.3` | version | identical | `3.0.4` (ours `3.0.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.0.4` |
| `packages/python/devel/flit/package.mk` | `flit` | `4.0.2` | version | identical | `4.1.0` (ours `4.0.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.1.0` |
| `packages/python/devel/lxml/package.mk` | `lxml` | `6.1.1` | version | identical | `6.1.3` (ours `6.1.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.1.3` |
| `packages/python/devel/meson/package.mk` | `meson` | `1.11.2` | version | identical | `1.12.1` (ours `1.11.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.12.1` |
| `packages/python/devel/ninja/package.mk` | `ninja` | `1.13.2` | version | identical | `1.13.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.13.2` |
| `packages/python/devel/pybuild/package.mk` | `pybuild` | `1.5.1` | version | identical | `1.6.1` (ours `1.5.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.6.1` |
| `packages/python/devel/pyelftools/package.mk` | `pyelftools` | `0.33` | version | identical | `0.33` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.33` |
| `packages/python/devel/pyinstaller/package.mk` | `pyinstaller` | `1.0.1` | version | identical | `1.1.0` (ours `1.0.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.0` |
| `packages/python/devel/pypackaging/package.mk` | `pypackaging` | `26.3` | version | identical | `26.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `26.3` |
| `packages/python/devel/pyproject-hooks/package.mk` | `pyproject-hooks` | `1.2.0` | version | identical | `1.3.3` (ours `1.2.0`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.3` |
| `packages/python/devel/pyyaml/package.mk` | `pyyaml` | `6.0.3` | version | identical | `6.0.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.0.3` |
| `packages/python/devel/setuptools/package.mk` | `setuptools` | `84.0.0` | version | identical | `84.2.1` (ours `84.0.0`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `84.2.1` |
| `packages/python/system/dbussy/package.mk` | `dbussy` | `bd4a5c3ddd2a` | hash | identical | `bd4a5c3ddd2a` (identical) | unknown: gitlab.com is not GitHub | follows the base merge; LibreELEC master at `bd4a5c3ddd2a` |
| `packages/security/gnutls/package.mk` | `gnutls` | `3.8.13` | version | identical | `3.8.13` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.8.13` |
| `packages/security/libgcrypt/package.mk` | `libgcrypt` | `1.12.2` | version | identical | `1.12.4` (ours `1.12.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.12.4` |
| `packages/security/libgpg-error/package.mk` | `libgpg-error` | `1.61` | version | identical | `1.61` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.61` |
| `packages/security/libtasn1/package.mk` | `libtasn1` | `4.21.0` | version | absent (fork-added) | absent | CURRENT (latest `4.21.0`) | current |
| `packages/security/libxcrypt/package.mk` | `libxcrypt` | `4.5.2` | version | identical | `4.5.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.5.2` |
| `packages/security/nettle/package.mk` | `nettle` | `4.0` | version | identical | `4.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.0` |
| `packages/security/nspr/package.mk` | `nspr` | `4.39` | version (unpacks from nss) | identical | `4.39` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.39` |
| `packages/security/nss/package.mk` | `nss` | `3.126` | version | identical | `3.132` (ours `3.126`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.132` |
| `packages/security/openssl/package.mk` | `openssl` | `3.6.3` | version | identical | `3.6.5` (ours `3.6.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.6.5` |
| `packages/sysutils/dbus/package.mk` | `dbus` | `1.16.2` | version | identical | `1.16.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.16.2` |
| `packages/sysutils/dmidecode/package.mk` | `dmidecode` | `3.7` | version | absent (fork-added) | absent | CURRENT (latest `3.7`) | current |
| `packages/sysutils/dosfstools/package.mk` | `dosfstools` | `4.2` | version | identical | `4.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.2` |
| `packages/sysutils/e2fsprogs/package.mk` | `e2fsprogs` | `1.47.4` | version | identical | `1.47.4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.47.4` |
| `packages/sysutils/exfatprogs/package.mk` | `exfatprogs` | `1.4.2` | version | identical | `1.4.3` (ours `1.4.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.4.3` |
| `packages/sysutils/fuse/package.mk` | `fuse` | `5a43d0f724c5` | hash | identical | `5a43d0f724c5` (identical) | the head of `fuse_2_9_bugfix`, the 2.9 series (`master` is 1885 commits ahead and lacks 47 of the pin's) | follows the base merge; LibreELEC master at `5a43d0f724c5` |
| `packages/sysutils/keyutils/package.mk` | `keyutils` | `1.6.3` | version | identical | `1.6.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.6.3` |
| `packages/sysutils/libevdev/package.mk` | `libevdev` | `1.13.6` | version | identical | `1.14.0` (ours `1.13.6`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.14.0` |
| `packages/sysutils/libusb/package.mk` | `libusb` | `1.0.30` | version | identical | `1.0.30` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.30` |
| `packages/sysutils/parted/package.mk` | `parted` | `3.7` | version | identical | `3.8` (ours `3.7`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.8` |
| `packages/sysutils/pciutils/package.mk` | `pciutils` | `3.15.0` | version | identical | `3.15.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.15.0` |
| `packages/sysutils/qrencode/package.mk` | `qrencode` | `4.1.1` | version | absent (fork-added) | absent | CURRENT (latest `4.1.1`) | current |
| `packages/sysutils/ryzenadj/package.mk` | `ryzenadj` | `0.19.0` | version | absent (fork-added) | absent | CURRENT (latest `0.19.0`) | current |
| `packages/sysutils/sed/package.mk` | `sed` | `4.10` | version | identical | `4.10` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.10` |
| `packages/sysutils/tz/package.mk` | `tz` | `2026c` | version | identical | `2026e` (ours `2026c`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2026e` |
| `packages/sysutils/udevil/package.mk` | `udevil` | `666e443c3618` | hash | identical | `666e443c3618` (identical) | at the default branch's HEAD | follows the base merge; LibreELEC master at `666e443c3618` |
| `packages/sysutils/usbutils/package.mk` | `usbutils` | `019` | version | identical | `020` (ours `019`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `020` |
| `packages/textproc/expat/package.mk` | `expat` | `2.8.2` | version | identical | `2.9.0` (ours `2.8.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.9.0` |
| `packages/textproc/itstool/package.mk` | `itstool` | `2.0.7` | version | identical | `2.0.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.0.7` |
| `packages/textproc/jsoncpp/package.mk` | `jsoncpp` | `1.9.8` | version | identical | `1.9.8` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.9.8` |
| `packages/textproc/libiconv/package.mk` | `libiconv` | `1.19` | version | identical | `1.19` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.19` |
| `packages/textproc/libidn2/package.mk` | `libidn2` | `2.3.8` | version | identical | `2.3.8` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.3.8` |
| `packages/textproc/libxml2/package.mk` | `libxml2` | `2.15.3` | version | identical | `2.15.4` (ours `2.15.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.15.4` |
| `packages/textproc/libxslt/package.mk` | `libxslt` | `1.1.45` | version | identical | `1.1.45` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.45` |
| `packages/textproc/nlohmann-json/package.mk` | `nlohmann-json` | `3.12.0` | version | identical | `3.12.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `3.12.0` |
| `packages/textproc/pugixml/package.mk` | `pugixml` | `1.16` | version | identical | `1.16` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.16` |
| `packages/textproc/xmlstarlet/package.mk` | `xmlstarlet` | `1.6.1` | version | identical | `1.7.0` (ours `1.6.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.7.0` |
| `packages/tools/mtools/package.mk` | `mtools` | `4.0.49` | version | identical | `4.0.49` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.0.49` |
| `packages/tools/nano/package.mk` | `nano` | `9.2` | version | identical | `9.3` (ours `9.2`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `9.3` |
| `packages/tools/newt/package.mk` | `newt` | `0.52.25` | version | identical | `0.52.25` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.52.25` (F-03) |
| `packages/tools/populatefs/package.mk` | `populatefs` | `fa7279f8e6af` | hash | identical | `fa7279f8e6af` (identical) | at the default branch's HEAD | follows the base merge; LibreELEC master at `fa7279f8e6af` |
| `packages/tools/procps-ng/package.mk` | `procps-ng` | `4.0.6` | version | identical | `4.0.7` (ours `4.0.6`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4.0.7` |
| `packages/tools/syslinux/package.mk` | `syslinux` | `6.03` | version | differs (fork edit) | `6.03` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.03` |
| `packages/virtual/alsa/package.mk` | `alsa` | - | virtual (no source) | identical | no version (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master carries it (no version) |
| `packages/virtual/autotools/package.mk` | `autotools` | - | virtual (no source) | identical | no version (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master carries it (no version) |
| `packages/virtual/corefonts/package.mk` | `corefonts` | - | virtual (no source) | identical | no version (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master carries it (no version) |
| `packages/virtual/debug/package.mk` | `debug` | - | virtual (no source) | identical | `` (same version, recipe differs) | not read: follows LibreELEC | follows the base merge; LibreELEC master carries it (no version) |
| `packages/virtual/misc-packages/package.mk` | `misc-packages` | - | virtual (no source) | identical | no version (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master carries it (no version) |
| `packages/virtual/toolchain/package.mk` | `toolchain` | - | virtual (no source) | identical | no version (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master carries it (no version) |
| `packages/wayland/wayland-protocols/package.mk` | `wayland-protocols` | `1.49` | version | identical | `1.49` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.49` |
| `packages/wayland/wayland/package.mk` | `wayland` | `1.26.0` | version | identical | `1.26.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.26.0` |
| `packages/web/curl/package.mk` | `curl` | `8.21.0` | version | identical | `8.23.0` (ours `8.21.0`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `8.23.0` |
| `packages/web/libpsl/package.mk` | `libpsl` | `0.23.3` | version | absent (fork-added) | absent | CURRENT (latest `0.23.3`) | current |
| `packages/web/libsoup/package.mk` | `libsoup` | `3.8.0` | version | absent (fork-added) | absent | CURRENT (latest `3.8.0`) | current |
| `packages/web/nghttp2/package.mk` | `nghttp2` | `1.70.0` | version | identical | `1.70.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.70.0` |
| `packages/web/webkitgtk/package.mk` | `webkitgtk` | `2.54.1` | version | absent (fork-added) | absent | BEHIND (latest `2.54.2`) | fork's: Backlog bump proposed (#839's shape), 2.54.1 -> 2.54.2 (F-09) |
| `packages/x11/app/xkbcomp/package.mk` | `xkbcomp` | `1.5.0` | version | identical | `1.5.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.5.0` |
| `packages/x11/app/xrandr/package.mk` | `xrandr` | `1.5.4` | version | identical | `1.5.4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.5.4` |
| `packages/x11/data/xkeyboard-config/package.mk` | `xkeyboard-config` | `2.48` | version | identical | `2.48` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.48` |
| `packages/x11/font/font-util/package.mk` | `font-util` | `1.4.2` | version | identical | `1.4.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.4.2` |
| `packages/x11/font/liberation-fonts-ttf/package.mk` | `liberation-fonts-ttf` | `2.1.5` | version | identical | `2.1.5` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.1.5` |
| `packages/x11/lib/libICE/package.mk` | `libICE` | `1.1.2` | version | identical | `1.1.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.2` |
| `packages/x11/lib/libSM/package.mk` | `libSM` | `1.2.6` | version | identical | `1.2.6` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.6` |
| `packages/x11/lib/libX11/package.mk` | `libX11` | `1.8.13` | version | identical | `1.8.14` (ours `1.8.13`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.8.14` |
| `packages/x11/lib/libXau/package.mk` | `libXau` | `1.0.12` | version | identical | `1.0.12` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.0.12` |
| `packages/x11/lib/libXcomposite/package.mk` | `libXcomposite` | `0.4.7` | version | identical | `0.4.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.4.7` |
| `packages/x11/lib/libXdamage/package.mk` | `libXdamage` | `1.1.7` | version | identical | `1.1.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.7` |
| `packages/x11/lib/libXext/package.mk` | `libXext` | `1.3.7` | version | identical | `1.3.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.7` |
| `packages/x11/lib/libXfixes/package.mk` | `libXfixes` | `6.0.2` | version | identical | `6.0.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `6.0.2` |
| `packages/x11/lib/libXfont2/package.mk` | `libXfont2` | `2.0.9` | version | identical | `2.0.9` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.0.9` |
| `packages/x11/lib/libXi/package.mk` | `libXi` | `1.8.3` | version | identical | `1.8.4` (ours `1.8.3`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.8.4` |
| `packages/x11/lib/libXinerama/package.mk` | `libXinerama` | `1.1.6` | version | identical | `1.1.6` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.6` |
| `packages/x11/lib/libXrandr/package.mk` | `libXrandr` | `1.5.5` | version | identical | `1.5.5` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.5.5` |
| `packages/x11/lib/libXrender/package.mk` | `libXrender` | `0.9.12` | version | identical | `0.9.13` (ours `0.9.12`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.9.13` |
| `packages/x11/lib/libXt/package.mk` | `libXt` | `1.3.1` | version | identical | `1.3.1` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.1` |
| `packages/x11/lib/libXtst/package.mk` | `libXtst` | `1.2.5` | version | identical | `1.2.6` (ours `1.2.5`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.6` |
| `packages/x11/lib/libXxf86vm/package.mk` | `libXxf86vm` | `1.1.7` | version | identical | `1.1.7` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.7` |
| `packages/x11/lib/libfontenc/package.mk` | `libfontenc` | `1.1.9` | version | identical | `1.1.9` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.1.9` |
| `packages/x11/lib/libpciaccess/package.mk` | `libpciaccess` | `0.19` | version | identical | `0.19` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.19` |
| `packages/x11/lib/libxcb/package.mk` | `libxcb` | `1.17.0` | version | identical | `1.17.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.17.0` |
| `packages/x11/lib/libxcvt/package.mk` | `libxcvt` | `0.1.3` | version | identical | `0.1.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.1.3` |
| `packages/x11/lib/libxkbfile/package.mk` | `libxkbfile` | `1.2.0` | version | identical | `1.2.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.2.0` |
| `packages/x11/lib/libxshmfence/package.mk` | `libxshmfence` | `1.3.3` | version | identical | `1.3.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.3.3` |
| `packages/x11/lib/pixman/package.mk` | `pixman` | `0.46.4` | version | identical | `0.46.4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `0.46.4` |
| `packages/x11/lib/xtrans/package.mk` | `xtrans` | `1.6.0` | version | identical | `1.6.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.6.0` |
| `packages/x11/other/fontconfig/package.mk` | `fontconfig` | `2.18.3` | version | identical | `2.18.3` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2.18.3` |
| `packages/x11/proto/xcb-proto/package.mk` | `xcb-proto` | `1.17.0` | version | identical | `1.17.0` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.17.0` |
| `packages/x11/proto/xorgproto/package.mk` | `xorgproto` | `2025.1` | version | identical | `2026.1` (ours `2025.1`) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `2026.1` |
| `packages/x11/util/util-macros/package.mk` | `util-macros` | `1.20.2` | version | identical | `1.20.2` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `1.20.2` |
| `packages/x11/util/xorg-launch-helper/package.mk` | `xorg-launch-helper` | `4` | version | identical | `4` (identical) | not read: follows LibreELEC | follows the base merge; LibreELEC master at `4` |

### Q5 Efficiency

**Not measured:** no build runs. What the 16 fork-own recipes ask of a build, read:
- `webkitgtk` caps its own parallelism (`PKG_MAKE_OPTS_TARGET="-j4"`, `:39`) for the memory a cold build has (`device-builds.md`);
- `ruby` is a host build only and never reaches an image;
- `libyaml`'s added `PKG_DEPENDS_HOST="ccache:host"` orders one host build;
- `syslinux`'s two `cp` lines copy one file twice.

No recipe here disables the compile cache. A `PKG_SHA256` sweep would restamp none here: upstream's sweep is in the past and every archive recipe carries one. Each of F-06 to F-09's bumps, when it lands, rebuilds its recipe and its dependants (`device-builds.md` § A metadata-only upstream change still rebuilds everything). `webkitgtk`'s is the costly one.

### Q6 Dead ends

Within the set everything is reached (the inventory's rule). **The class here is "claimed shipped, built in none of the five recorded roots": six names, not seven.**

| Name | Reach | Built? | How settled |
| --- | --- | --- | --- |
| `alsa`, `autotools`, `corefonts`, `debug`, `misc-packages`, `toolchain` | shipped | a virtual package has no build directory by construction; each root's `.stamps` holds them where the plan does | the stamps against each plan's `reachable_by` |
| `ntfs-3g_ntfsprogs` | shipped (GENERIC_X64, H700-aarch64, SM8550-aarch64) | **yes, in all three**: `build/ntfs-3g_ntfsprogs-2022.10.3` and its stamp | `viewplan` for each: `install ntfs-3g_ntfsprogs (wants: toolchain, fuse, libgcrypt)`, and `image`'s wants carry it. The brief's `sed` cut the name to `ntfs` (`03` § 3.3) |

**F-11, the one contradiction by stamps:**
- `btrfs-progs` is in GENERIC_X64's plan (`install btrfs-progs (wants: toolchain, util-linux, zlib, systemd, lzo)`, and `image`'s wants).
- The M7 GENERIC_X64 root (`069fc27044`) has no build directory, no stamp and no `mkfs.btrfs` in `image/system`.
- The H700 and SM8550 roots have all three.

It is a note for the inventory's owner and the M7 lane (the coordinator files it under #657's epic, brief § 4 Q6), not a change here.

### Q7 Clarity and structure

**The sixteen proposed rows for #645's move table (F-10):**

| # | Path | Provenance | Proposed disposition for #645 | Reason |
| ---: | --- | --- | --- | --- |
| 1 | `packages/addons/addon-depends/rsyslog-depends/libyaml/package.mk` | upstream recipe the fork edited | propose the hunk to ROCKNIX through #585 (a `PKG_DEPENDS_HOST="ccache:host"` line on the generic recipe), else a `projects/ROCKNIX/packages/.../libyaml` override that sources the generic and adds the line | a cold-tree ordering fix (`071fef34ed`); only `ruby:host` needs `libyaml:host`, and ruby is the fork's, so the override is the fallback |
| 2 | `packages/audio/libsamplerate/package.mk` | upstream recipe the fork edited | propose the hunk to ROCKNIX through #585 (`--with-pic`), else a ROCKNIX override that sources the generic and appends the option | a one-option build fix; LibreELEC master is the same version without it |
| 3 | `packages/compress/brotli/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/compress/brotli` | the sign-in window's chain (#576, woff2's dependency); no upstream copy, so the move shadows nothing |
| 4 | `packages/devel/ruby/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/devel/ruby` | a host interpreter only WebKit's generators need (#576); no upstream copy |
| 5 | `packages/devel/unifdef/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/devel/unifdef` | a host tool only WebKit's build needs (#576); no upstream copy |
| 6 | `packages/graphics/openjpeg/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/graphics/openjpeg` | WebKit's JPEG 2000 decoder (#576); no upstream copy |
| 7 | `packages/graphics/woff2/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/graphics/woff2`, with its `patches/` | WebKit's web-font decoder (#576); the patch moves with it (#645's 21 files count it) |
| 8 | `packages/network/glib-networking/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/network/glib-networking` | libsoup's TLS backend (#576); no upstream copy |
| 9 | `packages/security/libtasn1/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/security/libtasn1` | WebKit's ASN.1 parser (#576); no upstream copy |
| 10 | `packages/sysutils/dmidecode/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/sysutils/dmidecode` | GENERIC_X64's hardware report (`test` reach); no upstream copy |
| 11 | `packages/sysutils/qrencode/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/sysutils/qrencode` | the cloud setup's QR code (shipped); no upstream copy |
| 12 | `packages/sysutils/ryzenadj/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/sysutils/ryzenadj` | GENERIC_X64's power tool (`test` reach); no upstream copy |
| 13 | `packages/tools/syslinux/package.mk` | upstream recipe the fork edited | propose the hunk to ROCKNIX through #585 (the two `ldlinux.c32` lines), else a `projects/ROCKNIX/packages/tools/syslinux` override | GENERIC_X64's BIOS boot (`a6b28a469f`, `test` reach); syslinux 6.x needs `ldlinux.c32` beside the loader |
| 14 | `packages/web/libpsl/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/web/libpsl` | libsoup's cookie scoping (#576); no upstream copy |
| 15 | `packages/web/libsoup/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/web/libsoup` | WebKit's network backend (#576); no upstream copy |
| 16 | `packages/web/webkitgtk/package.mk` | added by the fork, absent upstream | move to `projects/ROCKNIX/packages/web/webkitgtk`, with its two `patches/` | the sign-in window (#576); the patches move with it |

- **None of the 16 is a recipe upstream has**, so a move under `projects/ROCKNIX/packages/` shadows nothing.
- **The three edited upstream recipes** are proposed to ROCKNIX through #585 first, since a contained fix in a generic recipe is a contribution (D-WORKFLOW-164; submission held, D-WORKFLOW-165). The override is each one's fallback.
- **The rest:**
  - **F-12:** the inventory records reach, not the pin. The 47 sourcing overrides need an effective-pin column, or a note on the generic row. A lead for #657 (P1's tool).
  - **F-13:** `libsoup` and `ruby` derive the release series from the version with `${PKG_VERSION:0:3}`, which reads `3.1` for a `3.10.x`. `glib-networking`'s `${PKG_VERSION%.*}` is the shape that does not break.
  - There are no two recipes for one library (`shadowed_by` 0, and the 47 sourcing overrides are layers, not copies).
  - `PKG_SITE` names the project for every fork-own row.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- `device-builds.md` § After rebasing item 3 says to read an override's *effective* `PKG_VERSION`. The same is true of `PKG_SHA256`, and no rule says it. F-01 is the case. The proposed sentence, for the coordinator: *read the effective `PKG_SHA256` per plan through `config/options <pkg>`; an empty value in an override's branch is a missing checksum.*

### Codification Gaps (needs-new-rule)

- **A count over recipes is a count over effective values** (D-WORKFLOW-194's shape, one step further). The guard is a tool: #844's fetch check, run per plan with `config/options`, would have printed `libfmt`'s empty checksum. That is a proposal to fold into #844's scope, not a new rule.

### Recommended Action Sequence

1. F-01 before T5's branch merges (a stream brief; the coordinator's call whether it lands on T5's branch or this one).
2. The #645 rows posted (F-10).
3. The Backlog bumps filed (F-06 to F-09).
4. The rest at their owners.

## Second opinion (Phase 4.6)

**Not applicable:**
- the depth is **Local** (D-WORKFLOW-184: *Local (the executor alone; the lint and the counts are the check) for a dead-end table, a provenance table or a doctrine read*);
- `slices.json` `k: 7`'s `depth_reason` is *a currency table*;
- `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184`;
- no Facilitator call, no provenance file.

## Quality Self-Check

- **The two table row counts:** every row of both tables comes from `tools/t7-tables.py`, which asserts 266 paths and 243 recipes and fails on a result file that misses a recipe. `grep -c -E '^\| `packages/'` gives 266 in `02` and 243 in `q4-table.md`.
- **Times:** every time in `00` and `02` is a `date -u` reading or a file the command wrote (`probe/started`, `probe/fetch-started` and their pairs).
- **The brief's claims that did not hold** are named: `ntfs-3g_ntfsprogs`, and the count behind D-WORKFLOW-194.
- **What was not read** is in § Coverage Boundary, and no row claims it.
