# Actual RC2 partial-state recovery

Submissionbd4245=0 is separate from durable completion09:19:19/allfourrc0.
Host verification81b7e2=0 at09:20:06 found all owner/guest processes absent
and no QEMU. The actual upgraded QA13 backing disk remained hash-identical;
the source and candidate bundle were reverified after execution.

All65 assertions pass across five states produced by the actual RC2 migration
script on the upgraded guest's COW: interrupted backups, saves and content,
completed old layout, and content recovery interrupted again at marker
publication. Provider-operation failure injection was actually reached.

The installed candidate preserved every payload, recovered all pointers,
published exactly layout=2 only after successful recovery, cleared the local
recovery record, and preserved bytes/pointers on repeat. Marker failure kept
the retry record, published no completion marker, and offered retry both at
boot and through transfer scan. The installed migration script is unchanged.

The157-artifact inventory retains139 public files, including per-stage
commands/results, inherited/recovered hashes and all65 assertion records.
This uses owned local cloud data and synthetic payloads, not a personal cloud.
