# #1513: build 26's EmulationStation, checked by the host suites run 20 had pointed at another tree

Standard run 20 (`/workspace/artifacts/rocknix-images/qa-6169621a4b-webdav-a-20261128-0206`) ran the host suites against `~/Development/emulationstation-next.worktrees/qa-integration` at `16dbac521`. The image ships ES `e67f28e1841579a401c2b4de9fe5f498ffa2b420`, the recipe's `source-commit`, and `16dbac521` does not contain it. The `*-run20.log` files are that run's logs.

The `*-e67f28e18.log` files are the same suites, run on 2026-11-28 with the round's tools (`build/m7-rc-round-20261125` at `6169621a4b`) against a detached checkout of `e67f28e18` (`/workspace/tmp/rocknix-session/es-e67f28e18`). The commands are `tools/vm-qa`'s own (`:224-233`, `:241`, `:243`, `:246`, `:251`), with `ES_SRC` set to that checkout. Every one exited 0.

| Suite | Run 20 judged (`16dbac521`) | Judged against the shipped ES |
| --- | --- | --- |
| lifetime | 10 PASS lines | 13 PASS lines, including `renew-phone`, `renew-keyboard` and `renew-no-browser` |
| vocabulary | 162 strings, 0 wrong | 179 strings, 0 wrong |
| french | 703 fork strings, 703 with French | 864 fork strings, 864 with French |
| quoting | 9 call sites, 9 quoted | 11 call sites, 11 quoted |
| menumap | 60 screens at `e67f28e18`, 0 missing | the same, because it already reads the pin |

## The runner's gate (`tools/vm-qa` on `next`)

`gate-proofs.txt` shows next's new runner in five cases:
- **T1, run 20's own condition** (`ES_SRC` at `16dbac521`, recipe at `e67f28e18`): refused with exit 2.
- **T2, no `ES_SRC`:** the runner checks out the pin as `pin-e67f28e18415` beside the other ES worktrees and passes the gate.
- **T3, the pin with a tracked file changed:** refused. The same checkout clean passes.
- **T4, next's `PKG_VERSION` recipe form:** a mismatch is refused.
- **T5, a suite that reads no ES:** meets no gate.

The fake tree in T1–T3 and T5 is next's new runner beside the round's recipe. It has no cloud backend, so a run past the gate stops there with exit 1 and touches no guest.

## The earlier runs

`earlier-runs.md` lists every run since November 20. All 19 read `16dbac521`, and none of their images pinned it. Only build 26 is a live candidate, and its own ES is now checked (the table above). The other builds are superseded, so their four host-suite PASS lines are history that describes `16dbac521`, not those images.
