# T42 brief stranger proof — frozen version 1

Source/provenance and handoff-feasibility observations only. This is not an audit, acceptance, dispatch, or coordinator ruling.

Observed UTC: 2026-11-02T18:40:23.060664+00:00

## Frozen inputs and method

- Brief: `patches-shipped.md`, SHA256 `01913fbb1ed6fb7814062fec7ed8fa5bd35c682b23616a61e252cf06a56be784`.
- Helper: `t42-brief-inputs.py`, SHA256 `1e54c3e3794b53f85874b4aee77904e845db4fddbc10347094384622413a5f70`.
- Exact copies were made and hashed before reading, under `/tmp/t42-brief-proof-50os455x/`.
- Scratch clone: `/workspace/tmp/m6-coordinator/t42-brief-proof-50os455x/clone`, detached at `b6332dbc13f5929f05ec5ba23c44285c5ee56b38`. Local `git clone --shared --no-checkout`; no fetch. The only untracked clone files are the two candidate overlays. This clone shares read-only object access through alternates, so it is a same-host proof, not an independent/off-host retrieval proof.
- `df -i` preceded clone creation: /workspace 28% used, 177,102,303 free inodes; /tmp 8% used. No tree was placed in /tmp.
- Exactly ten `exec_command` shell invocations, including preparation and this report write. Git subprocesses and Python loops batch the read-only checks; two `write_stdin` calls only collected completion. No further shell invocation is required.
- VM rationale: these predicates concern Git bytes, source interfaces and scratch-clone startability; no guest can add evidence for them. No tracker write was authorized for this proof; coordinator owns that record.

## What worked

Both literal membership-helper invocations completed with rc=0. The source-ref and HEAD summaries are equal, including the ref because both presently name b6332dbc13. This establishes the draft baseline, not the future published dispatch seed.

Independently checked from emitted rows and Git bytes: 384 unique paths; 71,387 logical blob lines; 71,378 newline bytes; 3,809,748 bytes; 380 regular files/four links; 379 shipped/five test; twelve fork-written paths/498 lines; 172 package-prefix groups; 188 immediate directories; thirteen reachable-by sets; roots 79/4,936, 302/66,306 and 3/145; following each selected symlink gives 71,477 logical lines. Path-list SHA256 is `91e980f455611fa81bc84c8ff5548abd05437452d02038cc5595f5c1521e5f07`.

The inherited TSV has exactly 50 unique (patch, override) keys / 26 overrides; owner lead counts T8=43, T22=6, T27=1. SHA256 `b8d5b458f13e5d1d5c3b08e5c9214f9b8712ff7875097707c35380700aef9c5a`. The 24 exclusions and accepted recipe dispositions remain historical input, not newly accepted adoption conclusions.

All brief-named T40/T8/T22/T27 evidence objects resolve at their immutable tips. Their files were availability/hash checked; accepted audit suites and verdicts were not replayed. Current source/P1 inventory, areas, slices, selector-tool bytes and all four resolved referent bytes also compare equal. `/workspace/cache/rocknix-sources/` exists; no individual archive, recipe checksum or extracted source was qualified.

## Concrete corrections for the coordinator

1. **Q5 is the wrong question.** Brief §4 calls Q5 “instruction load” and excludes it; plan §4 defines Q5 as runtime efficiency (boot, memory, time to play and player steps), and `tools/lint-audit-artifacts:436–450` agrees. Keep source-only limits and unchanged measurements, but answer the actual efficiency question with known source consequences or explicitly missing measurements routed to owners. A provenance table is not itself evidence that the patches have no runtime cost. Merely having a Q5 heading can pass this part of lint while answering the wrong question.

2. **Application input must be the build's rendered patch.** `scripts/unpack:191–196` substitutes `@TARGET_CPU@` and `@DEVICE@` before ordinary patch application. Fourteen selected path identities (eleven regular member blobs plus the three vitaquake2 links) contain `@DEVICE@` after resolving links. For example, geolith's `000-platform.patch:8–9` adds a platform branch using that placeholder. Brief §5 specifies raw patch/source hashes and generic `patch -p1 -N --batch`, but never requires this rendering, its selected variable values, or its hash. An application can succeed while introducing literal `@DEVICE@`, so its receipt would not establish the shipped build input. Require literal-versus-rendered identities, static per-plan values and the rendered bytes in both diagnostic/normal copies; an unresolved value must remain open. The engine also has a `git apply` branch for binary/rename patches; none of the 384 native blobs matched its trigger in this proof, so that is context to inspect if extra stack siblings require it, not a discovered native blocker.

3. **The runnable identity guard is narrower than the stop contract.** Helper lines selecting P1's functions always load that P1 tool, compare the selected row dictionaries and native mode/blob table, and emit referent SHA256 values only in `symlinks.json`. They do not assert selector-file/tool identity or compare the out-of-slice MangoHud referent against P1/source. The brief only asks the executor to compare `summary.json` ignoring `ref`; that summary omits all referent identities. Thus a future selector change preserving these rows, or a changed T43 referent, can leave the prescribed checks green. No such drift exists now. Add explicit immutable selector comparisons and compare `symlinks.json` (or bind those identities in the asserted summary) before proceeding B. Record source versus actual dispatch seed, not only source versus today's same HEAD.

## Interfaces and remaining prerequisites

The declared Local epic-folder contract is supported by the current linter: schema_version=1, depth=`local`, primary fields harness/model/lab/identity_source, reviewers=[], tier_exception=`D-WORKFLOW-184`, and nonempty reason (`tools/lint-audit-artifacts:78–98`). Model must carry its lab prefix when known. A one-file second-opinions directory is compatible with that Local contract. No positive/negative Local fixture or audit lint was executed here.

The exact later commands, discovered from source rather than executed, are:

```sh
tools/lint-audit-artifacts docs/audits/2026_11_02-epic-m6-patches-shipped --phase pre-issue
tools/lint-audit-artifacts docs/audits/2026_11_02-epic-m6-patches-shipped --phase resolution
tools/lint-audit-artifacts docs/audits/2026_11_02-epic-m6-patches-shipped --phase resolution --issue AUDIT_ISSUE --repo pixelelated/distribution
```

Pre-issue success literally prints `PASS pre-issue artifacts (does not certify resolution)`; resolution prints `PASS`. AUDIT_ISSUE is the later audit child, not automatically #689.

The current draft correctly requires the coordinator's corrected published version, replaced #689 criteria, ownership row, futro addendum, concrete seed and explicit dispatch. Those have not been established by this proof and are not supplied by the successful membership run. No missing extra permission is inferred for the specified future source-only workflow. Source extraction, patch application, fixtures, package census, all Stage A–H acceptance predicates, tracker state and publication remain unperformed; the assignment expressly excluded them. Therefore this receipt establishes that an executor can reproduce membership and locate inputs/interfaces, not that the complete application/acceptance workflow has passed.

## Reproduce the tested first action

From the preserved proof clone (which contains the exact candidate overlays):

```sh
cd /workspace/tmp/m6-coordinator/t42-brief-proof-50os455x/clone
set -eu
export LC_ALL=C
SOURCE_REF=b6332dbc13f5929f05ec5ba23c44285c5ee56b38
INPUT_HELPER=docs/qa-logs/2026-11-02-m6-resume/t42-brief-inputs.py
INPUT_OUT=$(mktemp -d /tmp/m6-t42-inputs.XXXXXX)
python3 "$INPUT_HELPER" --repo "$PWD" --ref "$SOURCE_REF" --out "$INPUT_OUT/source"
python3 "$INPUT_HELPER" --repo "$PWD" --ref HEAD --out "$INPUT_OUT/seed"
```

Original outputs: /tmp/m6-t42-inputs.XW9AiG/{source,seed}/. Exact stdout and actual successful exits: `/tmp/t42-brief-proof-50os455x/membership-{source,seed}.{stdout,rc}`. Supplemental source/command receipt: `source-check-receipts.json`, SHA256 `8f0fb1a812184c2d44c29523572b450ea19e6a72826f297481e0c7a147565fc1`, beside this report. `rendered-patch-members.json` lists the fourteen affected path identities. Clone commands/exits are retained at `/workspace/tmp/m6-coordinator/t42-brief-proof-50os455x/clone-receipts.json`.

No shared repository/tracker/lane file was mutated. No extraction/application, configuration sourcing, build, runtime, old-audit replay, network fetch, provider, device/cloud action or permission answer was performed. This report stops at the coordinator hand-back.
