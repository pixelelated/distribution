# #574 exact zstd test-alias omission — prospective, UNRUN

This new packet supersedes only export's blanket no-link assumption in sealed
7d4366c2b85213f2b41fa6cafbaac0e0a6dffb5c. The old packet and original FAIL remain
unchanged. `evidence/` preserves original child/container/attach/launcher failure
and successful cleanup/watchdog receipts, bound by `correction.json`. Export
refused during header inspection before creating the source root.

The exact 213471628-byte archive, SHA256
4867bee5dbd4129e6eea095fe8f8e9725563998710cc9620190e90529ef8931b,
contains 33835 members and 897821359 regular-file bytes. Two members are symlinks:
`3rdparty/zstd/tests/cli-tests/bin/unzstd` and `zstdcat`, each target `zstd`,
size 0, mode 0777. The original `special_members` classification excluded links;
it did not establish their absence. The new static header receipt verifies this
exact complete link set and rechecks the pinned GENie template hashes/excerpts.

Only those two exact zstd CLI test aliases are omitted from the private chdman
build tree. They are not created, followed or converted into fake regular files.
Every other member must pass the unchanged directory/regular-file checks. Missing,
additional, changed-target/type/size/mode aliases fail before source extraction.
All regular content, counts, hashes, canonical path/traversal rules, exact patch,
source-before/after checks and generated-file checks remain unchanged. Export
writes `omitted-test-aliases.json`; the source inventory includes both the exact
omissions and receipt SHA. This is a chdman build source subset, not a complete
MAME archive reconstruction or a runnable zstd CLI test tree.

`common.py`, `docker_owner.py`, `watchdog.py`, `plan.py`, `run-stage.py`, `inner.py`,
`mame.py`, the sealed plan, `build-stage.sh`, and shared-libstdcxx patch are exact
copies. No compiler/configuration predicate changed. The old explanatory README
is retained as `prior-runner-README.md` for input/lifecycle details; this note
replaces its no-link export claim. `static-result.json` and
`alias-static-result.json` record only AST/hash/bash-parser/header checks. No
export, generator, compiler, container or target was run by this worker.

For the coordinator only, after a fresh family admission, use the unchanged
plan/admission/submit sequence in `prior-runner-README.md`, substituting:

```sh
PIX574_REPO=/workspace/repos/rocknix.worktrees/m7-player-setup
PIX574_PACKET=$PIX574_REPO/docs/qa-logs/2026-10-14-chdman-export-alias-source
PIX574_OWNER=/workspace/tmp/pix574-chdman-build-20261014-02
PIX574_STAGE=chdman-export
python3 -I -S -B "$PIX574_PACKET/plan.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
```

The proposed owner must be new. Never reuse/reset the failed family's clock.
All four prospective stages must use this same packet manifest; consume each
original result before selecting the next. The unchanged one-family 1800-second
clock includes all stages; 1 compiler job, 4 GiB RAM, 2 CPUs, 6 GiB scratch ceiling,
offline container, read-only toolchain at the old prefix, and no host target
execution remain binding. This command is prepared, not allocated or executed.
