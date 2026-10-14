# Preparation transcript correction — #583 / #584

Source/static only; the corrected preparer and all protocol/native fixtures are
UNRUN. No product patch refresh or source-manifest change.

Coordinator attempt01 remains original **FAIL1**. Its exact `source.json`, log,
`build.rc`, and runner result are retained here unchanged from
`/workspace/tmp/pix583-native-prepared-20261014-01` and watched owner
`.build-runs/20261014T054658Z-e13647f6` in m7-player-setup. Both patch children
exited 0; the new preparer's blanket offset refusal stopped after patch002.
The patch002 output exactly matches qualified prior preparation:

```text
patching file linux/raofflineproxy/rom_cache.py
Hunk #1 succeeded at 40 (offset 3 lines).
Hunk #2 succeeded at 62 (offset 3 lines).
```

`qualified-source.json` is an exact copy of the previously accepted
`2026-10-13-proxy-memory-feasibility/source.json`, SHA256
`bbd19421935929cda116124199b0e81d0023cb8eb78ce627f3379ec76d61e3d6`.
It also contains qualified offsets for patches008, 010 and 015. The preparer
binds this complete receipt, checks its pin/archive/recipe/baseline and all 16
patch identities, and accepts offset-bearing output only when **all stdout
bytes equal that patch's prior output and stderr is empty**. New/moved offsets,
extra diagnostics, fuzz, reversed/failed patches and nonzero exits still refuse.
`--fuzz=0` and both final 112-file exact manifests remain unchanged. Historical
lazy-UI candidate fields in the copied receipt are not applied or accepted as
the RVZ candidate manifest.

The current packet's native runtime bindings and owner/runner source are
unchanged. `source.json` from a future preparation additionally records this
qualified transcript hash and each accepted offset match. No earlier receipt
or result is rewritten, and this is not a successful preparation claim.

Next preparation command uses the revised packet and a **fresh** coordinator
output such as `/workspace/tmp/pix583-native-prepared-20261014-02`, with the same
existing cached archive and source checkout. Do not reuse or erase attempt01.
Runtime/admission remain held independently.
