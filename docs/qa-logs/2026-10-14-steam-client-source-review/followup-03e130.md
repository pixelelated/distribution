# #582 remediation review — October 14, source only

Reviewed exact `a057a2a7e94c372642fd66ff9795125487f1fa75` →
`03e130e4b3c244337f2e6d782b392a2c444c28e7`, including the sealed
`2026-10-14-steam-client-corrections-source` packet, acceptance intake, retained
attempt01 failure, installer delta, and fixture delta. **Both findings from
8aec3a are addressed in source. No additional concrete defect found in this
scoped delta.** Runtime acceptance remains UNRUN. This supplements, and does not
change, the [historical review](README.md).

Installer SHA256:
`fab7cdb4ad8adbcea147be54092bb7ce2005010447be4ab8192c94d8bbe9229d`.
[Bindings and static checks](followup-03e130.json) identify the exact inputs.
Product line references below are to `Install Steam.sh` at 03e130.

| Finding | Source disposition | Remaining executable evidence |
| --- | --- | --- |
| S582-1, optional child census and cleanup under unknown quiescence | Addressed: numeric `/proc/PID/stat` census, PPID/start-time recheck after pidfd open, and durable transfer hold | `detached-transfer-child`, `proc-census-error`, then separately allocated `transport-timeout` |
| S582-2, symlink target normalized before parent traversal | Addressed: component resolution before `..`, with destination revalidation | `fresh-profile-parent-alias`, `existing-profile-parent-alias` |

At lines 1758–1830, disappeared processes are distinguished from unreadable live
identities; malformed/denied census reads propagate failure. Only this
subreaper's direct/adopted children qualify for pidfd signaling. Leader wait and
post-leader census/reaping retain separate five-second bounds; kernel ECHILD is
the successful completion condition. No optional task/children file is read.

At lines 1945–1950, `transfer-start` is fsynced before launch. The matching stop
record follows successful `terminate_group`, including on transfer failure
(1864–1872). `check_owned_state` rejects unmatched records before cleanup
(2184–2187), and recovery calls that check before profile execution. A failed
census or spawn therefore holds staging on this invocation and later attempts.
The v2 policy deliberately refuses historical v1 state without deleting it.
The error control observes the retained archive inode while its detached holder
is alive; that holder's independent exit 77 is correctly distinguished from
product-owned quiescence.

At lines 1597–1647, relative symlink targets retain the resolved parent, absolute
targets restart at `/`, and `..` applies after preceding links. The reported
`profile -> link/../support` layout selects `/storage/elsewhere/support`.
Missing-before-parent paths refuse. Saved identities/link targets and logical
destination are rechecked; metadata creation additionally checks storage mounts
(2106–2130). Fresh and existing controls preserve an independently seeded lexical
decoy and require registry and aliases in the actual destination.

Existing-client structural admission, channels/custom aliases, self-update
handling, install/recovery selection, and removal functions are AST-identical to
a057. Everything outside the client heredoc is byte-identical, including the
root/runtime/FEX/Proton helpers, profile timing and whole caller. The pre-profile
client check/post-profile support check remains explicit; arbitrary profile
effects and the existing registry copy are not made transactional by this fix.

The corrected `exec-guard.py:71–90` replaces main-loop polling with blocking
`waitpid(__WALL)` and a raising SIGALRM armed for the remaining original deadline.
The exact execve/execveat target denial and EACCES register edits are
AST-identical; tracing options, fork tracking and EXITKILL are unchanged.
Failure cleanup remains separately bounded to five seconds (137–166), records
cleanup exits separately, and retains any remaining tracees. The fixture refuses
those survivors and preserves a null original caller result on guard failure.
The mandatory idle control requires the actual blocked-wait marker, deadline
failure, cleanup exits and no survivors; the busy control requires 4000 syscall
stops. Neither is a measured performance or containment result yet.

Static AST/hash/source checks passed (review command exit 0): all 26 correction
manifest entries, exact helper/installer bindings, unchanged allocation limits,
and unchanged historical review hashes. No fixture was imported or executed.
Attempt01 remains FAIL with original caller exit null. Coordinator owns fresh
VM allocation: the corrected packet's initial `fresh-client-real-root` command
runs its mandatory exec controls first. Native ARM64/client self-update,
real-archive installation, concurrent native consumers, power loss and installed
image qualification remain outside this source disposition.
