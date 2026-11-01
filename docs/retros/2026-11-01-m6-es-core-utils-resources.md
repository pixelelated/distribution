# Mini Retro: T36 — es-core utils/resources audit slice (#683), stage E

**Completed:** 2026-11-01
**Scope:** the eleven streams S0–S10 (four PL + three held + the ruling-10/floor record), one ES commit each, recorded on `feature/m6-es-core-utils-resources-683`.
**Delta:** ES `16dbac5211` (pin) → `9c1bd5f09`; distribution records on the audit folder; `t36-build-tests` TOTAL 208 (es-unit-tests 185/185, utils-resources-tests 23/23).

## What worked well
- **Lift-vs-link, chosen per seam.** FileSystemUtil/StringUtil/ZipFile link whole with small doubles; Font/TimeUtil/TextureData methods lift verbatim at pin and tip via `t36-extract.py`. The extractor's first/last-line assertion caught every spec drift (S6's +3, S10's +3) before a case ran against the wrong lines.
- **FAIL-at-pin before every fix.** Each stream proved its defect at the pin first; the main binary (23/23) is the regression net.
- **The held discipline held.** S5/S6/S7 commit messages, case names and `02` rows carry only the bug number, the file and the phrase; inputs and reports stayed in `/workspace/tmp/m6-t36/held/`.

## What was harder than expected
- **Sanitizer visibility of SSO over-reads (G-7).** The `length()-N` underflow only triggers for length-0/1 strings, which are always short-string-optimized, so ASan sees nothing and a sub-granule poison is a no-op. Resolved by the coordinator's option 2: a synthetic lift over a raw heap buffer, with the behaviour case over `""`/`"a"` on the real function; #1358's checkbox stays partial.
- **The TextureData link surface (S9/G-20).** Driving `loadFromPdf`/`initSVGFromMemory` pulled Renderer, ImageIO, ResourceManager, vlc and nanosvg; the harness needed a full double set plus `nsvg-impl.cpp`.
- **The held-comment slip (S6).** The first FileSystemUtil comment named the mechanism; caught in review and amended to the neutral register.

## What we discovered
- `FileCache::fromStat64` follows the link, so `isSymlink` cannot see a dangling symlink — G-14's first fix (`&& !isSymlink`) was wrong; the robust fix is a direct `lstat64` guard.
- `-O1` dead-code-eliminated G-3's null-face deref; the Font harness needs `-O0`.
- `es-unit-tests` builds under g++15 only with `-Wno-template-body` (rapidjson 1.1.0's `-Wtemplate-body` is a default-error, not `-Werror`-promoted).

## Adjustments / what T37 inherits
- The extractor `SPECS` at the tip, the `san()`/sibling-binary shapes, `removeFile`'s lstat guard and the uncached thumbnail reads, the held-case shape, the collision owners (T20/T21/T26), the rule errata (L-08, L-13), and Backlog #1372. Full list in `02` § What T37 inherits.

## Time to play
The two numbers were not measured this slice (`03:26`, no device/guest timing window). The launch-path changes are S6's `run()` wrap (grouping + quoting only, no added process or wait) and S5's held function (per the held record's own reading); the rest is per-label, per-texture or per-copy work, priced on the integration image. `docs/vm-qa-log.md` carries no T36 row — a `CANNOT` with that reason.

**Stage E code-complete; hand-back posted on #683.**
