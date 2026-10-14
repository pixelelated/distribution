# #584 additive child-census correction — 2026-10-14

**Prepared only; UNRUN.** Original product and packet at
`c22554a4c0966d48ba405ef1640938d2a417817b` remain unchanged. This packet changes
only its prepared fixture supervision and final receipt handling. No proxy
fixture is rerun or modified;819/22cf remain unchanged.

The exact first-run trace is retained in `original-host01.stdout`, bound to its
host path/hash in `bindings.json`. The wrapper's original exit marker is1.
`/proc/self/task/4306/children` was absent both in the per-case census and in
`finally`; the second exception prevented publication of the result. This is a
fixture/kernel-interface mismatch. It supplies no routing or preservation
verdict, and the original failure is not rewritten into a pass.

The additive `fixtures/probe.py` keeps the original packet as its adjacent input.
It verifies the old fixture, binding and manifest identities, then the original
source-input hashes. Its retained report includes original and revised fixture
identities. `fixture-only.patch.gz` is the exact review delta from the original
fixture; `fixture-only.patch.sha256` names its uncompressed SHA256. No patch or
edit to the original packet is needed to stage this revision.

The replacement reads numeric `/proc/PID/stat` entries and selects only PPIDs
matching this fixture's subreaper. It extracts PID, PPID and start-time ticks;
process names are neither matched nor retained. A process disappearing during
inspection is ignored only when its proc directory is also confirmed absent.
Permission errors, malformed records, a missing stat file in a still-present
process directory, and directory-enumeration errors fail closed.

Before any cleanup signal, the fixture rechecks that exact identity and PPID,
opens a pidfd, rechecks the identity again, then signals the pidfd. An identity
change refuses the signal. A kernel-confirmed exit races harmlessly with the
pidfd operation; unrelated/reused numeric PIDs are never signaled by number.
All previous `killpg`/numeric `kill` calls are removed. Terminating a direct
child lets surviving descendants become this subreaper's adopted children;
the bounded cleanup loop censuses, signals and reaps those children in turn.
Python/Linux pidfd support is required; its absence is a failure before scripts.
No process-name scan, broad signal, optional `children` file or new CLI tool.

Cleanup/census exceptions now set FAIL and are retained independently of JSON
publication. The final child census starts as `null` (unknown), and remains null
if observation fails; an observation error never becomes an empty census.
Original errors and recorded shell exits survive cleanup errors. A filesystem
failure while writing the final JSON also emits the full FAIL receipt to the
coordinator's captured stdout before raising. This cannot guarantee persistence
if the owner is forcibly killed; the original external watched-owner boundary
still applies. Observation failures do not authorize an unsafe numeric kill.

All126 cases, source variants, original expectations, profile, queue tripwire,
resource limits and child isolation are unchanged. `static-result.json` records
AST identity for every original helper except the modified main, the complete
nested isolation function, and byte identity of the expectation tail. Static
AST/hash checks passed; the runtime fixture was neither imported nor executed.
The original source/receipt manifests and product hash were reverified.

Coordinator: stage this packet and the original
`2026-10-14-dolphin-proxy-routing-source` packet as adjacent directories; verify
both SHA256SUMS files. Under the same admitted disposable no-NIC GENERIC_X64 VM
and watched owner, from this new packet run once:

```sh
python3 -I -S -B fixtures/probe.py --output /run/pix584-route02
```

The fresh path is required. Preserve original exits and the first stopping case;
no automatic retry or unchanged component rerun. Limits remain60 seconds work,
50CPU seconds/256MiB owner address space,3seconds wait/2CPU seconds/64KiB output
per child,24MiB maximum runtime staging,32MiB asserted scratch and48MiB initial
free/reserve. Cleanup retains its3-second active-child wait and2-second census
loop. Keep the coordinator's75-second outer bound and finite process-scope
cleanup. The03:36UTC VM deadline is unchanged and does not authorize another run.

Product SHA256 remains
`e77cbee0b7cbe0765d4723f9ccc58459ef142f6987038512f75a06ee2ab22bec`.
Installed-image/native Dolphin, proxy login/cache/awards/reconnect and actual
cleanup/error-path behavior remain runtime qualification, not static acceptance.
