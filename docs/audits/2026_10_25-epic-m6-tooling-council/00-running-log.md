# Running log — M6.P2 T45, the council toolchain and runner (#692)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`).
- **Brief:** `docs/reviews/briefs/tooling-council.md`, version 2 (`fe43e15058`, the same bytes at the branch's `HEAD`).
- **Dispatch:** the coordinator's comment on #692, 02:54 UTC on 2026-10-25.
- **Depth:** Local. There is no reviewer seat, `tools/council/run invoke` is never run, and the lint and the counts are the check.
- **`reviewed-at`:** `32a34393dd`, the dispatch tip and the branch `HEAD` at stage A.
  - The read is of `8ebaf8daad`'s bytes for the 52 members.
  - The branch differs from the hash on exactly the ten files of `0ceb2994c5` and `033eb7ed23` (brief § 1).
- **The lens:** package currency. The provenance table (Q7) and the currency table (Q4) are the slice's output.
- **Keyless runs:**
  - Every `tools/council/run` call is made through `env -u FIREFLIES_API_KEY COUNCIL_ENV_FILE=/nonexistent`. The wrapper sources its env file only when the file is readable (`run:21-28`), so it sourced nothing.
  - `FIREFLIES_API_KEY` is the one credential-named variable in this session's environment. Only its name was read, and it is dropped from every run.
  - No `invoke`, no `--refresh`, and no read of any credential file.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t45/tmp`. The clone at the hash is `/workspace/tmp/m6-t45/at-hash`. The run outputs are under `.qa-scratch/t45/`, and copies are in `stage-a/`.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u`.

## [Stage A] 02:54 to 02:59 UTC — scope, host, the two trees' runs, currency

- **The first commands** (brief § 1):
  - fetch rc 0; branch `feature/m6-tooling-council-692` at `32a34393dd`, stacked on P1 (`2174265e9c`); `inventory.json` present.
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, exactly the dispatch's eight paths.
  - `df -i /tmp`: 40 % used. Nothing was written there.
  - `node --version` v24.21.0; npm 11.19.0.
  - `rules-check --quiet` rc 0; `register-check`: 680 IDs, every citation resolves.
  - `git check-ignore -v`: `tools/council/node_modules/` (`.gitignore:66`), `tools/council/package-lock.json` (`:67`) and `.qa-scratch/` (`:63`) are all ignored before the first install.
- **The host before anything ran:**
  - The host file's last line is the coordinator's 02:30 UTC acknowledgement of the M7 lane's FINAL RETURN (census `all=0 live=0`).
  - Census: `pgrep -x qemu-system-x86` gives 0.
  - This slice runs no guest.
- **Membership** (§ 2's block at `2174265e9c`; `stage-a/scope.out`, `stage-a/paths.txt`):
  - 52 paths, 25,848 lines, all fork-own;
  - 23 TypeScript, 22 JavaScript, 4 JSON, 1 text, 1 Python, 1 shell; reach `n/a` 52;
  - 30 more rows match the globs in `build-engine` (`stage-a/others.txt`).
- **Commits on the 52:**
  - 5 fork commits at the hash: `b3e5c92559`, `4796a78983`, `5f1b343d25`, `4bf31083c7`, `a9af618398`. None is on `upstream/next`.
  - Beyond the hash: exactly `0ceb2994c5` and `033eb7ed23`, which make `10 files changed, 356 insertions(+), 28 deletions(-)`.
  - Since the dispatch tip `32a34393dd`: none.
- **The bytes against the export's SUMS** (`stage-a/provenance-8ebaf8daad.txt`, `stage-a/provenance-HEAD.txt`; 94 SUMS lines, the file unchanged on the branch):

  | Tree | listed | equal | differ | unlisted |
  | --- | ---: | ---: | ---: | ---: |
  | `8ebaf8daad` | 50 | 41 | 9 | 2 |
  | the branch | 50 | 36 | 14 | 2 |

  - At the hash, the 9 that differ are the brief's 9.
  - Five more differ on the branch: `council-seat-efforts.json`, `scripts/lint-council-seat-efforts.ts`, and the three `scripts/lib/council-staged-*` files.
  - The two unlisted are `tools/council/run` and `tools/council/package.json`.
  - Both trees agree with the coordinator's figures.
- **The pins** (`stage-a/pins.out`, `stage-a/pins-delta.out`), `council-verifier-pins@2.0.0`:
  - 27 at the hash, 30 on the branch.
  - Added: the three `council-staged-*` files, at `2026-10-22T04:50:02`, with #636's reason naming *local Facilitator 1.14.1-pixelelated.1*.
  - Changed: `council-invoke.ts`, `council-seat-efforts.json` and `lint-council-seat-efforts.ts`, at `05:13:36`, with #638/#636's reason. None removed.
  - `FACILITATOR_VERSION` is `council-facilitator@1.14.0` at the hash (`:844`) and `council-facilitator@1.14.1-pixelelated.2` on the branch (`:855`).
- **The runs, on each tree** (`stage-a/runs-branch.txt`, `stage-a/runs-at-hash.txt`; outputs under `stage-a/branch/` and `stage-a/at-hash/`; the runner is `stage-a/runs.sh`):

  | Run | branch `32a34393dd` (02:56) | clone `8ebaf8daad8eaac6…` (02:56:58) |
  | --- | --- | --- |
  | `npm install --prefix tools/council` | rc 0, 1 s; 31 packages added (fresh `node_modules` at 02:56:05) | rc 0, 1 s |
  | resolved (`npm ls`) | `tsx@4.23.15`, `@aws-sdk/client-bedrock-runtime@3.1156.0` | the same |
  | `verify-pins` | rc 0: *verifier pins match current files and every re-pin is accountable* | rc 0, the same |
  | `drift` | rc 0: *no stale-blob regression detected* | rc 0, the same |
  | `efforts` (offline; no `--refresh`) | rc 0: 8 seats checked, 6 provider-pinned | rc 0: 7 seats, 5 provider-pinned |
  | `test` (28 s on each) | rc 0; per file 39 / 127 / 19 tests, 0 fail | rc 0; 39 / 109 / 19, 0 fail |

  - **npm warned** that esbuild 0.28.2's postinstall is not covered by `allowScripts` and was not run. `tsx` ran regardless (the routing file runs under it). This is a Q2 row.
  - **The test count:** at the hash the files read 39, 109 and 19, which equals the export commit's claim. The branch's routing file has 127 against the commits' claimed 119, and stage B reads that against `0ceb2994c5`.
  - **The `test` counter:** the first counter read `^ok ` lines and gave 0, because Node 24's spec reporter prints `✔` and `ℹ tests N`. The figures above come from the `ℹ` summaries, with 0 `✖` lines.
- **`lint`** over the recorded council runs (`stage-a/lint-*.out`):
  - The brief's literal command, on `docs/audits/2026_09_13-…/second-opinions`, exits 1 with `run_invalid`. That folder holds no `council-run-manifest.json`, and an explicitly named incomplete run fails by design (`lint-council-run.ts:427`).
  - **Every one of the four runs under `research/council-runs/` fails, on both trees.** On the branch, all four fail with `council_roster_invalid` (*run contract must match the installed Facilitator and recipe projection*). At the hash, the two 2026-09-05/11 runs fail the same way, and the two 2026-09-30 runs fail with `genesis_binding_mismatch` (*run identity, coordinator, or verifier pins changed*).
  - Each run exits 1. Whether a historical run is meant to pass (scaffold#944's *historical inventory by the contract it carries*) is stage B's question.
- **A misread, corrected at once:** a loop printed `rc=0` for those four lints because `$(basename $r)` ran inside the `echo` before `$?` expanded. The re-run captured `rc=$?` first and read 1 for each. Friction line 02:59 UTC, the third instance of the shape.
- **Currency** (`stage-a/currency.out`, read 02:58:34 UTC):
  - `tsx` latest 4.23.15 (2026-09-20) against `^4.22.4` (2026-05-31).
  - `@aws-sdk/client-bedrock-runtime` latest 3.1156.0 (2026-10-22) against `^3.1073.0` (2026-06-19).
  - `mistral-common` pinned 1.11.7 (2026-07-23); latest 1.12.0 (2026-09-22).
  - `numpy<2.4; python_version < "3.13"`; latest 2.5.4 (2026-10-10).
  - The seat-efforts `refreshed_at` is `2026-09-28T05:09:37Z` on both trees, although the branch re-pinned the file.
  - The scaffold checkout here is `20c0a77` (2026-08-29), corpus 3.29.1, and lacks the export commit `7be6721b`. Ours is 4.29.1, generated 2026-09-29.
- **The roster against the floor** (`stage-a/roster-*.txt`):
  - `OPENROUTER_SEATS` is identical on both trees:
    - claude `anthropic/claude-fable-5.1` `xhigh`;
    - gemini `google/gemini-3.8-flash` `high`;
    - gpt `openai/gpt-6-astra` `max`, pinned to `openai` with `allow_fallbacks: false`;
    - kimi `moonshotai/kimi-k3` `max`, pinned to four providers;
    - muse `meta/muse-spark-1.3` `max`, pinned to `meta`.
  - Claude and GPT meet `adversarial-council.md`'s floor (`:77-78`).
  - The branch adds `AUDIT_OPENROUTER_SEATS` with one seat outside the five: `gemini-argon`, `google/gemini-4-argon` at `high`, pinned to `google-vertex/global`.
- **Nothing written** under `/tmp`, `/workspace/repos/rocknix*` or `/home/max/Development/scaffold*`; no member file edited; no guest; no build.
