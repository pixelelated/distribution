# device-build's checks before anything is written (#1510, #1512) and its source check (#1509), proven at 62b4883635

These were run by the chain `b27-sm8550.sh` (a copy is here) on 2026-11-28, while no build was running. Each step's log ends with `== exit N (want N)`, and the chain stopped on any other result.

| Step | Command | Result | Ticks |
| --- | --- | --- | --- |
| `p1.log` | H700 dry run, `--name m7-round-h700-20261128` (its owner folder holds `retention-plan.json`) | exit 2, "one owner folder per launch" | #1510 c1 |
| `p2.log` | SM8550 dry run, unused `--name m7-round-sm8550-20261128-02` | exit 0, "nothing was created or changed"; it lists H700's two roots for removal | #1510 c2, the control for #1512 c1 |
| `p3.log` | the same dry run, with `sleep 600` whose working directory is H700's `.ccache` | exit 2 after the 120 s wait, naming `3356027 cwd … (started 2026-11-28T06:36:23Z: sleep 600)` | #1512 c1 and the holder-naming criterion |
| `p4.log` | a real SM8550 launch on the used owner folder `m7-round-sm8550-20261128-owner` | exit 2, "one owner folder per launch"; the set file's mtime is 06:26:55.597531235 before and after | #1510 c3 |
| `p5.log` | a real SM8550 launch, unused `-02`, with the holder | exit 2 after the wait, naming the holder; set file unchanged; no `-02` owner folder plans or admission | #1512 c2 |
| `wait-scratch.out` | `wait-scratch.py` loads the tool's `wait_free` against a scratch tree | a holder that left after 10 s: proceeds; one that stayed: refused after the wait, named | #1512 c3 |
| `sm8550-launch.console` | the real launch, `-02` | `source-check: SM8550 at 6169621a4b -- every source is cached or can be fetched`; the users check passed; ES binary kept; both H700 roots removed (+106.1 and +25.9 GiB free); submitted at 06:48:43, run `20261128T064843Z-a7b15e8b` | #1512 c4, #1509 c4 |

Every dry run and launch ran `tools/source-check` in step 3, taking 59 to 102 s. The set file's 06:26:55 mtime is from the refused 06:24 launch, which wrote it before the owner check moved (#1510).
