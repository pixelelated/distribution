# Research Notes — M6.P2 T8, the image's own packages (projects/ROCKNIX)

## Scope

- **Read hash:** the slice's bytes are `next`'s at **`8ebaf8daad`**; **`reviewed-at:` `caf1de3727`**, the branch `HEAD` at stage A (stacked on P1's `2174265e9c`, the coordinator's tip `dede8effec` merged at `ffec1e54b2`, the pointer seeded at `caf1de3727`). `upstream/next` `e0f9deb899` at the fetch (2026-10-24 12:10 UTC).
- **The filter** (brief § 2), run on `docs/reviews/inventory.json` (`00ca350666`): the `generic-packages` area's rows under `projects/ROCKNIX/**` less `projects/ROCKNIX/packages/virtual/emulators/**` whose reach is `shipped`, `test` or `n/a`:

```
paths 485 lines 20644 {'upstream-carried': 450, 'fork-own': 35} {'shipped': 478, 'n/a': 1, 'test': 6}
{'recipe': 260, 'shell': 45, 'make': 7, 'c++': 5, 'text': 4, 'config': 65, 'other': 11, 'systemd': 30, 'none': 8, 'script': 1, 'json': 5, 'symlink': 2, 'xml': 1, 'image': 38, 'python': 1, 'udev': 2}
recipes 260 fork-own recipes 27 groups {22 groups as the brief lists them}
with patches 60
```

  **All equal to the brief's figures: no delta.**
  - The `n/a` row is `projects/ROCKNIX/packages/initramfs/config/initramfs.x86_64.conf`.
  - The six `test` rows are the installer's (its recipe, config, gptk, script, service, target).
  - **14 paths contain spaces; no recipe does.**
  - `.qa-scratch/t8/paths.txt` holds the 485 and `recipes.txt` the 260.
- **Over the 485:** `tr '\n' '\0' < paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is empty.
- **Provenance, by git** (brief § 2's block):

| Count | Command | Result |
| --- | --- | --- |
| the fork's changes since the base | `xargs -0 git diff --name-status c445081a59 8ebaf8daad --` | **35**: 11 A, 24 M (27 recipes: 8 added, 19 edited; 8 other files) |
| against `upstream/next` | `xargs -0 git diff --name-status upstream/next 8ebaf8daad --` | 31 A, **87 M** |
| the recipes absent upstream | each A recipe checked at the base | **11 orphans** (`libfreeaptx`, `opus`, `libfmt`, `glslang`, `vulkan-headers`, `cargo`, `miniupnpc`, `rocknix-abl`, `tllist`, `mtdev`, `swaybg`), **7 fork-added** (`gamescope-glm`, `gamescope-stb`, `mangohud-vulkan-headers`, `mangohud-vulkan-utility-libraries`, `harfbuzz-icu`, `gst-plugins-bad`, `gnutls`) |
| upstream's changes on these paths since the base | `xargs -0 git log --oneline c445081a59..upstream/next --` | 40 commits; 66 recipes |
| the freshness tool's set under `projects/` | `fork-package-freshness --list` | 34 (its set is a diff, not a provenance, #644 finding 16) |
| the conflict set | `comm -12` of the fork's and upstream's changed paths since the base | **11**: the recipes of `gamescope`, `cairo`, `glslang`, `spirv-tools`, `gcc`, `gst-plugins-base`, `gstreamer/gstreamer` and `rocknix-abl`; `gamelist.xml`, `NetworkManager.conf`, `111-sway-init` |

- **The M7 delta:** none on the 485; the slice is read at `next`'s bytes.

## T7 erratum (found at T8's stage A)

T7's accepted audit says that six of the 47 ROCKNIX overrides sourcing one of its recipes are absent on `upstream/next` because ROCKNIX deleted them (#644 finding 16's orphans). It says so in `05-punch-list.md`'s PL-12 and `tools/punch-items.py`; its retro adds *six are orphans ROCKNIX has since deleted*. The provenance block here splits them by the base `c445081a59`:
- **orphans** (present at the base, deleted upstream): `audio/libfreeaptx`, `audio/opus`, `devel/libfmt`;
- **fork-added** (absent at the base too): `graphics/harfbuzz-icu`, `multimedia/gstreamer/gst-plugins-bad`, `security/gnutls`.

T7's check read `upstream/next` only. PL-12 is withdrawn, so no outcome changes. The sentence is wrong in three of six names, and the correction is the coordinator's to place.
