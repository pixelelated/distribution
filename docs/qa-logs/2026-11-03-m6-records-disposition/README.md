# T46 Stage-D reconciliation and stream disposition

Immutable lane D: a0d4c4fda7a0c16c04d57edf921ffeb741eff19b, source d707c82,
execution seed8710a621. The complete checkpoint is retained in
tracker-context.json; its body SHA256 is
82902258632b93462380a9c96a9d4060b975513907e2ee30b2356aa9a589760a.

source-disposition-inputs.json compares the one README at five immutable
tips and specifies its proposed exact paragraph replacement. It is a
bounded current-guidance comparison, not a repeat of the records audit.
candidate-binding.json runs only the new stream metadata block;
candidate-checks.json contains normal coordinator record checks and the
existing nonblocking ceremony warning.

publication/retention.json maps35 selected ordinary final publication and
checkpoint files to lossless UTF-8 JSON strings. Decode once to recover
the original bytes and verify the recorded original hash. Escaped hyphens
are representation only; no producer output or historical failure is
rewritten. The final manifest binds314 changed records; earlier failed
publication attempts remain separately preserved in the committed D packet.

P1's immutable reconciliation and T5's unfamiliar-executor stream proof
are separate bounded support assignments. Their returns and any root
corrections precede the final disposition/dispatch. Neither a proposed
brief nor retained publication receipts alone constitute D acceptance.
Final source correction, E–H acceptance, completion marker and actual
ordered integration remain separate stages with named evidence.
