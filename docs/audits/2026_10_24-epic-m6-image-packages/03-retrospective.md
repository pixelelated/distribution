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
