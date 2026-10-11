# Container temporary-path scope — #549

Initial build20 stopped before compilation with original inner/outer/launcher2:
the host-only TMPDIR was forwarded into an unmounted container path. Pinned
nonroot controls reproduce failure there and success at container-local /tmp.
Build20b explicitly scopes Docker TMPDIR to /tmp. Its actual container completed
with exit0, all643 tasks and image assembly; the original wrapper remains1.
Its monitor incorrectly required Docker inspect to contain only one TMPDIR
entry. Docker retains both configured entries; actual runtime readback and
mktemp prove /tmp is effective. Container ID matches the build cidfile.

Independent watched build20-verify ended0 at19:50:49UTC. It verifies actual
container image/user/mount/runtime evidence, three refusal controls, frozen
source and every assembled mapping/identity. No product change, recompilation,
input substitution or original result overwrite. This composed acceptance is
explicit about the failed observer; it does not relabel either original owner.
Raw/update payload, installed-tree delta and clean/upgrade VM qualification
remain separate #548 requirements. No owner device/cloud was touched.
