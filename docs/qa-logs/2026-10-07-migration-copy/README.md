# M7.P5 migration prompt copy proof — #502

The approved English and matching French are implemented in ES commit
`5d2fcb9b71f363cfa4813d5356f02c48ab58e139`, branch
`feature/m7-migration-copy`, based on
`72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`. Only the prompt's translatable
string and its French catalog entry changed. Migration behavior, button labels,
button order, automatic following, and confirmation conditions did not change.
The ES integration branch was fast-forwarded to this exact commit, and both
`feature/m7-migration-copy` and `test/qa-integration` were pushed through normal
hooks. Remote hashes were read back successfully. The distribution pin was not
moved by this lane.

`runs/pixelelated-m7-migration-copy-publish09/result.json` and its durable
watcher log retain the publication outcome. `process-exits.json` retains the
independent exit check. `cleanup.json` records removal of the seven named
owner runtime files, reclaiming 2,556,751,872 allocated bytes; accepted build
inputs and firmware are unchanged.

Can this be done on the VM? Yes: this is dialog copy and layout, with no
physical-device dependency. One disposable candidate16 guest used an rclone
alias pointing at a QA directory inside that guest. No personal cloud,
handheld, game launch, or remote provider was involved.

## Verified result

`acceptance.json` binds the source, image, and four directly reviewed frames.
English and French at **640x480 and 1280x800** show the full prompt, literal
typographic path quotes, lowercase `pixelelated`, and all three choices.
The prompt and a second frame five seconds later are byte-identical in each
accepted cell: no scrolling was needed. English retains the exact final
sentence: `IF FILES STILL NEED MOVING, YOU'LL BE ASKED TO CONFIRM.`

- English 640x480: `runs/pixelelated-m7-migration-copy-vm04/artifacts/640x480-en_US/01-prompt.png`
- French 640x480: `runs/pixelelated-m7-migration-copy-vm04/artifacts/640x480-fr_FR/01-prompt.png`
- English 1280x800: `runs/pixelelated-m7-migration-copy-vm04/artifacts/1280x800-en_US/01-prompt.png`
- French 1280x800: `runs/pixelelated-m7-migration-copy-vm08/artifacts/changed-fr/01-prompt.png`

The French 640x480 button row extends slightly outside the dialog background
but remains fully on screen. The same geometry is present in the original
source's French prompt, proved with the original installed ES and a catalog
compiled from its pinned source:
`runs/pixelelated-m7-migration-copy-vm08/artifacts/baseline-source-fr/01-prompt.png`.
This copy change does not introduce or repair that existing layout behavior.

`es-syntax-check`, vocabulary, `msgfmt --check --check-format`, actual
build-style `xgettext` extraction, `git diff --check`, and register citations
passed. The extracted English msgid resolves to the new French translation.
Raw curly-quote bytes were rejected by the existing xgettext invocation;
standard C++ `\u2018`/`\u2019` escapes preserve the exact displayed characters
and extract correctly without changing the build recipe.

The VM used one recompiled `GuiMenu.cpp` object and an owner-local relink with
candidate16's retained objects and libraries. No image, build stamp, or source
in the accepted build tree was changed. `inputs-before.json` and
`inputs-unchanged.json` retain explicit input hashes; `link-trace-inputs.json`
records all 164 paths observed in the successful linker trace. Installed
binary and catalog hashes, image identity, actual source-folder state, and
unchanged QA save bytes are in the corresponding `*-installed.log` files.
Back dismissed the prompt without moving the fixture in all four original
matrix cells. The final French capture changes focus only; it does not select
the highlighted KEEP action.

## Preserved failed attempts and fixture repairs

The original records remain under `runs/`; they are not relabeled successful.

- Host01: raw Unicode source bytes failed xgettext; Unicode escapes fixed it.
- Host02: syntax, vocabulary, catalog validation, and compilation passed;
  relinking failed because a copied toolchain's embedded sysroot referred to
  the older build path. Host03 explicitly selected the retained candidate16
  sysroot and redirected linker outputs into its own directory; link passed.
- VM04: three cells have valid reviewed frames. The nominal French large-screen
  capture contains a stale backdrop and is rejected as visual evidence.
- VM05/06: reusing a guest stopped without flushing its dirty writes exposed
  a zero-filled QA executable header and a damaged generated French locale.
  VM06 also failed because its continuation helper referenced the new owner's
  nonexistent QA key. These are harness failures, not product acceptance.
- VM07: restaged executable/catalog hashes passed, but the generated French
  locale still caused English fallback; its nominal French frames are rejected.
- VM08: before regeneration, the locale command could not load LC_CTYPE or
  LC_MESSAGES and reported ASCII despite the locale files existing. After
  regenerating only this guest's French locale, it reports UTF-8 and the live
  ES environment reports `fr_FR.UTF-8`. Explicit visible focus movement avoids
  accepting a stale static VNC surface. Both scoped French captures passed
  direct inspection. Guest writes were flushed before the owned QEMU stopped.

The durable watcher results, terminal process checks, and cleanup receipt
are retained with this record. A zero capture exit alone is not visual
acceptance; the accepted frame list above is the narrower, inspected result.
Temporary runtime disks and binaries are retired after compact proof capture;
this packet retains source/command identities, logs, frames, and outcomes.

Remaining integration work belongs to the parent lane: move the distribution
pin through its normal checks and include the change in the next appropriate
build. This scoped proof does not designate
an RC or claim that the currently installed H700 firmware has changed.
