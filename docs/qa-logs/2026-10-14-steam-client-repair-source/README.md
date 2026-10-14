# Steam client repair: classification decision before implementation

Source/static evidence only, 2026-10-14. This additive #582 packet leaves the c624
installer, every previous packet, and shared records unchanged. No archive access,
decode, fixture execution, native client, service, VM, build, or download occurred.

The coordinator's public-archive inspection resolves the format prerequisite:
55 members, 339,635,561 decoded bytes, five reviewed path mappings, three stored
links, and complete SHA/CRC/layout/ELF structural checks. Its copied original
[inspection](evidence/steam-inspection.json) says PASS, with native readiness,
signature authentication, and external dependency resolution explicitly unproven.
The accompanying [transport receipt](evidence/steam-inspection.transport.json)
records readback exit 0. It does not contain the base64 stream or an independent
full-run process receipt. The coordinator reports original 0/no intervention;
durable export of those originals remains coordinator-owned. This packet does
not manufacture a second runtime receipt or relabel the original download FAIL.

**The remaining blocking decision is the existing-client contract.** Neither a
folder, an executable/ELF header, `.installed`, nor a stale installer receipt proves
that an arbitrary self-updated client is complete. The live #582 criteria explicitly
require preservation and refusal of ambiguity before writes. The source also puts
`source /etc/profile` before the client check; that profile can write and execute
user code. See [concrete alternatives and caller seam](contract-alternatives.md).

Recommendation: permit a fresh, bounded transaction and read-only revalidation of
its complete recorded inventory; refuse unverified existing state before profile
execution, retaining every byte and alias. This deliberately stops setup on a
working legacy/self-updated client that cannot be verified. That compatibility
cost needs a choice before product code, as the assignment requested. A second
seam is `.steam` path selection: its current override can come from profile code.
Freezing it before profile execution changes that contract; checking it afterward
cannot promise zero prior writes. No choice is silently implemented here.

[controls.json](controls.json) specifies the whole-script regression/failure matrix
and exact observations needed after that choice. **These are UNRUN specifications,
not executable fixtures or prepared PASS results.** The new transaction and its
receipt/phase format do not yet exist, so inventing injection offsets or binding a
candidate command would misrepresent readiness. The earlier selected-function and
whole-caller packets remain immutable and do not become tests of a repair by
renaming them. No completed experiment is requested again.

Fresh primary-source reads and exact disposition are in
[upstream.md](upstream.md); source and evidence hashes are in [source.json](source.json).
[static-result.json](static-result.json) records only checks actually performed.
No #582 acceptance checkbox is newly closed here. The next executable experiment
is held until the policy and implementation exist: first one full-caller synthetic
fresh mixed-name/stored-link case, then separately allocated failure/retry controls,
each bound to the resulting complete installer and fixture hashes. There is no
honest repaired-installer runtime command to allocate from this packet yet.
