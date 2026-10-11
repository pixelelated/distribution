# VM startup failure and runtime root — #545

The first upgrade19 owner ended1 at18:30:25UTC. QEMU could not write its PID
files under /tmp; vm-pair discarded the launch status and claimed up with an
empty PID. Neither guest booted. The exact failed wait was stopped; the parent
recorded failure and stopped its local backend. No firmware failure is inferred.

vm-pair now probes runtime writes, propagates launch errors and requires a live
QEMU PID owning the expected disk before saying up. Serial failure returns even
inside a conditional. VM_QEMU_RUNTIME_DIR lets vm-pair/vm-qa share a short owned
socket/PID directory on /workspace. The default remains /tmp. Nine real-function
controls pass; original-source failure control returns0 and falsely says up,
which makes the new test fail as intended. CI runs this regression on future pushes.

The five-file scratch-retirement proposal is NOT executed: some process
references require root readback. No quota recovery or cleanup is claimed.
#493 owns that separate dependency work. Fresh upgrade19b instead uses its owned
runtime directory on /workspace, with both changed host tools hash-sealed beside
the unchanged firmware input seal. Its actual paired launch passes; the subsequent early save-read failure is #546. Both guest processes and the local backend exited. Fresh upgrade19c carries the corrected readiness wait.
