# #575 save-state capability handoff — source only

ES candidate **e87d0d1b4562adfb9e5b8b6882c0c655ed611afc**, from exact composed
base **a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20**, changes only
`es-app/src/guis/GuiMenu.cpp` (22 added lines, three scoped blocks). It clarifies
global preference/manager scope and offers optional support help for resolved
Dolphin/Flycast selections. Existing capability gates already omit unsupported
auto-save controls and the standalone manager; they are preserved.

The isolated branch is `feature/m7-save-capabilities-575` at
`/home/max/Development/emulationstation-next.worktrees/m7-save-capabilities-575`.
Coordinator's composed worktree and qa-integration were not touched. Integrate
only this ES commit and this new distribution packet's own commit. Previous #571,
#567/#578/#570, and clean-state packets remain immutable; do not merge the worker's
historical distribution ancestry.

## Delivered evidence and boundary

- [capability-map.md](capability-map.md) separates preference resolution, shipped
  launcher behavior, engine-native support, manager eligibility, paths, and
  hardcore constraints for the three requested families. Nova's actual selection
  remains unknown. A native Flycast auto-save option is not the ES global setting.
- [source.json](source.json) binds eight ES and eighteen distribution inputs;
  distribution bytes equal coordinator `c75b8d1dae`. [upstream-source.json](upstream-source.json)
  binds public Flycast/Dolphin engine excerpts to their exact package pins.
- [issue-intake.md](issue-intake.md) retains the complete coordinator-supplied
  #575 body. Its one complete comment was read from the live GitHub API.
  [archaeology.txt](archaeology.txt) comes from next's read-only tool; D-UI-057,
  D-UI-069, and D-UI-083 were read before editing. No #196 implementation is repeated.
- [flow-and-vm-fixtures.md](flow-and-vm-fixtures.md) gives the canonical flow/copy
  proposal, exact frame branches, and separate engine observations. Four EN/FR
  additions are in [copy.fr.po](copy.fr.po); catalogs are untouched.
- [capability_fixture.py](capability_fixture.py) and [capability-cases.json](capability-cases.json)
  prepare **64 UNRUN controls**: sixteen selections × four preference hierarchies.
  It extracts the actual selection methods, manager gate, and new menu block;
  only data storage/window/menu/layout availability are doubles. The copied
  callback is exercised after the mock parent is destroyed. Unknown source bytes
  refuse before compilation. It records compiler/runtime exits and original output.

The new help captures only Window, writes no setting, and performs no launch/file
operation. Existing save callbacks, launch argument generation, slots, storage,
hardcore behavior, all capability declarations, and ApiSystem are unchanged.
Help is resolved at page creation using the existing validated emulator getter;
the existing emulator-selection callback rebuilds the page. No recurring prompt
or engine autosave implementation was added.

## Actual static checks

[static-result.json](static-result.json) reports PASS for source hashes, Python
AST/literal parsing of the prepared fixture, XML declarations, and exact diff
scope. Removing the new help block and reverting the two guarded descriptions
reproduces the original GuiMenu bytes. The other seven bound ES files are
unchanged. The helper itself was not imported or launched, and the C++ was not
generated, parsed by a compiler, compiled, or executed.

Executed:

```sh
python3 docs/qa-logs/2026-10-13-save-capability-source/static_check.py \
  --es-src /home/max/Development/emulationstation-next.worktrees/m7-save-capabilities-575
git -C /home/max/Development/emulationstation-next.worktrees/m7-save-capabilities-575 diff --check
git diff --check
# From this packet directory:
sha256sum --check SHA256SUMS
```

No emulator/VM/compiler/service/device/account action, dependency install, test
suite, build, push, pin promotion, shared record edit, or delegation occurred.
Read-only public upstream/issue research occurred. No source or commit-approval
blocker remains. C++ compile, translations, behavior, and rendering are **UNRUN**.

## Next executable experiment — coordinator allocation required

Can this be done on the VM? **Yes**; the extracted source control can first run
under the coordinator's bounded host compiler allocation, followed by real ES/VM
proof. This command is prepared, **not run**, and is not an admission bypass:

```sh
python3 docs/qa-logs/2026-10-13-save-capability-source/capability_fixture.py \
  --es-src /home/max/Development/emulationstation-next.worktrees/m7-save-capabilities-575 \
  --output /workspace/tmp/pix575-capability-controls-20261013
```

Use a fresh owned output directory. It requires an already-installed C++17
compiler with ASan/UBSan, and does not install one. Expected evidence is process
exit 0, result.json PASS, `PASS 64/64`, and empty stderr; all are currently absent.
Source remains immutable while it runs. The fixture does not exercise real
GuiSettings persistence/rendering, installed layout parsing, or an emulator.

Then coordinator composes the ES commit/catalog additions, runs the standard
syntax/build qualification and EN/FR small/large flows, and allocates disposable
engine cases from the companion plan. Existing `last-good-scripts-test` section v
supplies #196 regression rather than a replacement test here. Required homebrew/
BIOS selection and actual native engine exits are not supplied by a fake ROM stub.

| Issue criterion | This delivery | Still unverified |
| --- | --- | --- |
| Selected emulator/core/effective settings receipt | Exact source mapping and 64 prepared synthetic controls | Actual Nova selection and installed guest resolution |
| Separate ordinary/manual/exit/manager observations | Concrete per-engine disposable matrix, engine source evidence | All emulator runtime outcomes |
| Correct unsupported UI implication | Scoped global help and selected-emulator support dialog; EN/FR copy/flow proposal | Compiler, visual branches, screenshots and actual settings preservation |
| Standalone integration contract | No new integration; precise native/launcher/manager distinction | Any future bridge's exit/load/slot/path/retained/hardcore proof |

No issue completion or candidate acceptance is claimed. In particular, inherited
launcher relinking may affect retained directories; this read-only source finding
is handed off explicitly and must not be hidden by the UI clarification.
