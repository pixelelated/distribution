# Research Notes — M6.P2 T7, the generic packages the image builds

## Scope

- **Read hash:** the slice's bytes are `next`'s at **`8ebaf8daad`**; **`reviewed-at:` `4ea87f17dd`**, the branch `HEAD` at stage A (stacked on P1's `2174265e9c`, the coordinator's tip `e7978a1ca5` merged at `65438eb0b3`, the pointer seeded at `4ea87f17dd`). `upstream/next` `e0f9deb899` at the fetch (2026-10-24 10:12 UTC).
- **The filter** (brief § 2), run on `docs/reviews/inventory.json` (`00ca350666`): the `generic-packages` area's rows under `packages/**` whose reach is `shipped`, `test` or `n/a`:

```
paths 266 lines 7612 {'upstream-carried': 250, 'fork-own': 16} {'n/a': 3, 'shipped': 256, 'test': 7}
{'markdown': 1, 'recipe': 243, 'shell': 4, 'text': 1, 'other': 6, 'cmake': 3, 'none': 2, 'udev': 2, 'config': 3, 'systemd': 1}
recipes 243 groups {'addons': 25, 'audio': 16, 'compress': 9, 'databases': 1, 'debug': 3, 'devel': 45, 'graphics': 16, 'lang': 2, 'multimedia': 7, 'network': 14, 'print': 1, 'python': 15, 'security': 9, 'sysutils': 17, 'textproc': 10, 'tools': 6, 'virtual': 6, 'wayland': 2, 'web': 5, 'x11': 34}
with patches 46 shadowed 0
```

  **All equal to the brief's figures: no delta.** The three `n/a` rows are `packages/README.md`, `packages/packages.mk.addon_template` and `packages/packages.mk.template`; the seven `test` rows are `lm_sensors`, `slang`, `dmidecode`, `pciutils`, `ryzenadj`, `newt`, `syslinux`. `.qa-scratch/t7/paths.txt` holds the 266 and `recipes.txt` the 243.
- **What else `packages/` holds:** 942 `package.mk` at `8ebaf8daad` outside `packages/{emulation,linux,linux-firmware,linux-driver-addons}/`; the 243 are those a shipped or test plan reaches; the other 699 are T23's (#670). T6's two late-binding leads (`jre.zulu:12`, `mesa-reusable:14`) are among T23's (the coordinator's 10:09 correction on #654) and are not read here.
- **Over the 266:** `git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t7/paths.txt)` is empty: P1 and the coordinator changed nothing under the slice.
- **Provenance, by git** (brief § 2's block, A4):

| Count | Command | Result |
| --- | --- | --- |
| added by the fork | `git diff --diff-filter=A --name-only c445081a59 8ebaf8daad -- $(cat recipes.txt)` | **13**, each absent on `upstream/next` (`git cat-file -e`): brotli, ruby, unifdef, openjpeg, woff2, glib-networking, libtasn1, dmidecode, qrencode, ryzenadj, libpsl, libsoup, webkitgtk |
| edited by the fork | `--diff-filter=M` | **3**: `libyaml`, `libsamplerate`, `syslinux` |
| untouched | the rest | **227** |
| against `upstream/next`, all of `packages/` | `git diff --name-status upstream/next 8ebaf8daad -- packages/` | 16 A, 5 M (#645's 21 files) |
| the freshness tool's set under `packages/` | `tools/fork-package-freshness --list` (rc 0) | 13; `diff` against the fork-added 13 empty |
| upstream's commits to `packages/` since the base | `git log c445081a59..upstream/next -- packages/` | 0 of 325 |

- **The M7 delta:** none on the 266. M7's tree is the legacy checkout's; the slice is read at `next`'s bytes.
