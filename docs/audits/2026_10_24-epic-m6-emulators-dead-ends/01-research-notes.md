# Research notes — M6.P2 T24, emulator recipes and files no shipped image builds (#671)

## Scope

**Read hash:** `8ebaf8daad8eaac6331dff6fc048fb4411d7decb` (`next`). The branch at stage A is `81331b499e` (the dispatch's hash). `git diff --stat 8ebaf8daad HEAD -- <the 86>` is **empty**, so the membership's bytes are the hash's. Every line number in these artifacts is the hash's unless marked *branch*. The export is `.qa-scratch/t24/at-hash/` (`git archive 8ebaf8daad packages/emulation projects/ROCKNIX/packages/emulators/libretro`): 474 tracked paths, 3 of them symlinks. `upstream/next` at the read: `e0f9deb899` (the brief's), moved to `481c9d0d75` by the stage-A fetch (heroic only). The merge base is `c445081a59` for both.

**The filter** (brief § 2, run with `python3 -I` over `docs/reviews/inventory.json`, whose header names P1's `eb4763e3cc` with `upstream_head` `c1f1746828`). It keeps the rows with `tree == distribution`, `area == emulators-and-cores` and reach `unreached` or `unshipped`: the area's rows that T3 and T30 did not take. Output, 13:39 UTC:

```
paths 86 lines 2399 {'upstream-carried': 86} {'unreached': 84, 'unshipped': 2}
{'recipe': 85, 'cmake': 1}
recipes 85 under packages/emulation 81 under projects 5 with patches 12 shadowed 0 spaces 0
unshipped: [('boom3-lr', ['AMD64-x86_64']), ('vitaquake3-lr', ['AMD64-x86_64'])]
```

These are the brief's figures and #671's: **86 paths, 2,399 lines; 86 upstream-carried; 84 `unreached`, 2 `unshipped`; 85 recipes and one cmake file (`packages/emulation/rcheevos/source/CMakeLists.txt`, 64 lines).** No delta. Twelve recipes carry patches: `libretro-bsnes-hd`, `libretro-bsnes-mercury-performance`, `libretro-bsnes`, `libretro-cannonball`, `libretro-dosbox-pure`, `libretro-mame2010`, `libretro-mupen64plus-nx`, `libretro-picodrive`, `libretro-scummvm`, `libretro-stella`, `panda3ds-lr` and `play-lr`. Those patches are T40's rows, and this slice reads none of them. No path carries a space.

**The 86, by place:**
- **81 under `packages/emulation/`**, LibreELEC's:
  - 77 `libretro-*` cores, `libretro-2048` to `libretro-yabause`;
  - `cyclone68000`;
  - `libretro-common`;
  - `rcheevos`, its `package.mk` and the cmake file.

  That is 80 recipes and one cmake file.
- **5 under `projects/ROCKNIX/packages/emulators/libretro/`**, ROCKNIX's own:
  - `boom3-lr` and `vitaquake3-lr`, `unshipped`;
  - `mame2003-lr`, `panda3ds-lr` and `play-lr`, `unreached`.

**Provenance, by git.**
- `git diff --name-status c445081a59 8ebaf8daad -- <86>` prints nothing: **the fork changed none of the 86 since the base.**
- Against `upstream/next`: **81 identical and 5 differing (`M`)**, the same at `e0f9deb899` and at `481c9d0d75`.
- The five differ by upstream's single commit on these paths since the base, `af70bd435b` (*libretro-cores: add retroarch as PKG_DEPENDS_TARGET*). It touches exactly the five ROCKNIX recipes and meets no fork edit, so the base merge brings that hunk cleanly.
- `git log e0f9deb899..481c9d0d75 -- <86>` is empty.

**Last touches at the hash:**
- `libretro-snes9x`: `2dd698ba24` 2026-06-02.
- The latest among the 81 LibreELEC files: `e46157185c` 2026-07-22 (*libretro-cannonball: update to githash 65cb1f5*).
- The latest among all 86: `9cdcb3d437` 2026-09-03 (*libretro: update licenses*, on the five ROCKNIX recipes).

**The branch against the hash:** no hunk on any of the 86. P1 and the coordinator changed nothing here, so there is no owner to name.

**Interacting subsystems (read-only context):**
- the emulators metapackage `projects/ROCKNIX/packages/virtual/emulators/package.mk` (T3's): its `add_emu_core` rows;
- `tools/viewplan` and `config/options` (the plans);
- the ROCKNIX `*-lr` twins (T3's 137 recipes);
- the Kodi `game.libretro.*` addon recipes under `packages/mediacenter/` (the 81's only callers by name, unreached themselves);
- T40's patches under `packages/emulation/*/patches/`;
- `core-info`'s `.info` files under `usr/lib/libretro/` in the install trees (T3's `Already written:` note);
- the five M7 build roots, read by `ls` only.
