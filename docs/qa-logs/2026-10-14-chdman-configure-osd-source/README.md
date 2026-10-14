# #574 owner03 OSD selection correction — prospective, UNRUN

Owner02's configure failure is a libretro OSD override, not an obsolete XInput
flag. This packet preserves the complete original failure, corrects only the
private build preparation, and keeps every requested target feature and option.
No product/pin/shared-record change, runtime, export, GENie, compiler, container,
VM, archive/binary download, converter execution or upstream submission occurred here.

## Exact source cause and smallest repair

The archive remains MAME/libretro `24cffe763621b164fc10be2ae3660f140be25182`,
213471628 bytes, SHA256
`4867bee5dbd4129e6eea095fe8f8e9725563998710cc9620190e90529ef8931b`.
Read-only gzip snapshots (exact uncompressed bytes/hashes) are in `evidence/source/` and
`evidence/source-members.json`; this is not an exported build tree.

1. `makefile:800–809` forwards NO_X11 and both XInput options independently.
   `scripts/src/osd/sdl.lua:129–174` declares all three unconditionally; their
   registration is not suppressed by NO_X11=1. The lightgun default is disabled,
   but that does not make its explicit argument invalid.
2. `scripts/genie.lua:1155–1164` computes the requested SDL project subdirectory
   and calls `toolchain`. At `scripts/toolchain.lua:583`, GENie's
   `configuration { "libretro*" }` selects a project-settings block. It does not
   conditionally execute Lua (`3rdparty/genie/src/base/api.lua:308–341`).
3. Consequently `toolchain.lua:645` changes `_OPTIONS["osd"]` to `retro` even
   for the selected SDL/release64 tool. Lines648/651 also set libretro-only BGFX
   and MIDI options. The subsequent `genie.lua:1449` loads retro.lua rather than
   sdl.lua; retro_modules.lua declares BGFX but neither SDL XInput option.
   GENie validates the resulting options after script loading
   (`src/_premake_main.lua:104–112`, `src/base/option.lua:83–113`). Lua table
   iteration is unordered; the reported invalid option need not be the only one.
4. Dropping XInput arguments would leave the wrong OSD. The selected tool links
   `ocore_` plus `_OPTIONS["osd"]` (`scripts/src/tools.lua:59–75`), contradicting
   the sealed `ocore_sdl` graph. Merely restoring OSD after toolchain would also
   leave the undeclared SDL-path NO_USE_BGFX value.

The two-line **scratch-only** patch wraps exactly the three libretro-only
assignments in `if _OPTIONS["osd"] == "retro" then ... end`. A requested retro
build still takes that block; the selected SDL build retains its supplied
options. Other toolchain configuration blocks and all converter/native GENie
sources remain unchanged. This adapts the libretro archive for the already
selected standalone tool; it is not a proposed change to the packaged core.

The new toolchain.lua hash is
`b45c6d1fa1d4d4a824d1f739ab749d2ae776dfb23b7a040b89bc4d2c67c2219b`.
The existing shared-C++ patch and patched genie.lua hash remain unchanged.
Export applies both separate patches with fuzz0 and requires exact final hashes.
Before/after inventory checks allow exactly these two files, retaining every
other original file, mode, alias refusal and generated-artifact check.

`option-review.json` maps **all43 make assignments and37 observed GENie options**
to exact declarations/uses, including17 enumerated value checks. None is removed.
TOOLS=1/EMULATOR=0/TESTS=0/BENCHMARKS=0, release64, O1, no LTO/OpenMP,
static bundled codecs, static libgcc/shared libstdc++, NO_X11, both XInput
disables, audio/network/debug options and compiler overrides are preserved.
`PLATFORM=x86` names the generator architecture family; the existing build still
selects `config=release64`. This static mapping does not prove generated output.

`upstream-followup.json` records the official MAME0.289 source comparison and
the exact-pin browser cache miss. The immutable local archive is authoritative.
The previous official converter/source checks remain in plan/upstream-check.json.
No upstream release/fix or generic libretro defect is claimed.

## What changed, and original outcomes

`changes.json` contains exact before/after hashes and small diffs against
`26a527f76527b1a4466404cbc8c07eee73524cd0`:

- export.py applies the second exact patch and records it.
- mame.py permits exactly the two documented changed-source files and verifies
  both hashes; generated dependency, compiler, flags and output checks are exact
  copies. plan.py changes only its diagnostic name.
- plan/build-stage.sh adds the second post-patch hash precondition. Every command
  argument and native/bootstrap/converter path is byte-identical.
- plan/input-bindings.json adds the second patch contract; bindings.json points
  to this packet's revised plan and manifest, not the historical 1c0e93 plan.

common.py, docker_owner.py, watchdog.py, run-stage.py and inner.py are exact
26a527 copies. Resource, identity, no-network, predecessor, consumed-result,
clock, original-exit and cleanup enforcement is unchanged. Prior packets1c0e93,
7d4366 and26a527 are untouched. Their old README/static statements are retained
as historical evidence, not relabelled for this revision.

`evidence/owner02/` retains export and native bootstrap PASS0/consumption,
configure selected-make2, container/attach/launcher1, watchdog0 and cleanup PASS
with empty recorded descendants/cgroup. No configure acceptance is inferred.
Source-after verification in the original failure still passed. Coordinator
retired owner02's private work tree during this source inspection; no live host
process census or cleanup was performed by this worker.

## Exact fresh-family entry — coordinator only

Copy this packet byte-exact into the coordinator checkout, verify SHA256SUMS,
then use fresh owner03. This command only prepares the first stage's plan:

```sh
cd /workspace/repos/rocknix.worktrees/m7-player-setup
PIX574_REPO=$PWD
PIX574_PACKET=$PIX574_REPO/docs/qa-logs/2026-10-14-chdman-configure-osd-source
PIX574_OWNER=/workspace/tmp/pix574-chdman-build-20261014-03
PIX574_STAGE=chdman-export
python3 -I -S -B "$PIX574_PACKET/plan.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
```

For each individually selected stage, use the existing admission sequence:

```sh
PIX574_STAGE_ROOT=$PIX574_OWNER/stages/$PIX574_STAGE
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX574_STAGE_ROOT/retention-plan.json" \
  --output "$PIX574_STAGE_ROOT/retention-report.json"
# Consume original report/watcher channels and review fresh capacity first.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX574_STAGE_ROOT/admission-plan.json" \
  --output "$PIX574_STAGE_ROOT/admission.json"
tools/watch-build-submit --owner "$PIX574_STAGE_ROOT/submit" -- \
  --admission "$PIX574_STAGE_ROOT/admission.json" \
  --activity-dir "$PIX574_STAGE_ROOT/logs" -- \
  python3 -I -S -B "$PIX574_PACKET/run-stage.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
```

Consume each original stage/attach/container/monitor/launcher/cleanup result
through existing build-admission before explicitly planning the next stage:
export → bootstrap → configure → build. No loop, auto-advance or retry.
Export/bootstrap acceptance already exists for owner02; fresh owner03 must
recreate its now-retired private inputs. No copying old successful receipts,
changing owner02's manifest/clock or pretending it configured successfully.

All stages and review/admission gaps share **one1800-second family clock** from
first export. **One job,4GiB RAM/no swap,2 CPUs,6GiB sampled scratch ceiling**;
no kernel-disk-quota claim. Preserve the512MiB host free-space floor, exact
offline builder/read-only toolchain mounts and unchanged retirement waits.
An expired family refuses; no extension or synthetic clock reset.

## Verification and remaining limits

`static-check.py` only parses Python AST, checks source/packet hashes and the
zero-context text patch, compares exact runner deltas/options and invokes
`bash -n`. It imports no prepared runner module and runs no Lua/make/GENie.
`static-result.json` is source-only. New patch application, configure/generated
graph, target compilation and ELF/loader/CHD parity all remain **UNRUN**.

There may be later generator/toolchain or dependency failures; original exits
must remain failures. No memory/time-fit promise, native target execution,
functional codec qualification, final-image proof or source-pin promotion is
made. A successful compile still requires the coordinator's separately admitted
VM loader/format/independent-parity proof; old-image ELFs retain their existing
unverified current-source provenance.
