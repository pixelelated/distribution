# ZeroTier isolated compile: original extraction-helper failure

Run `20261015T150258Z-e90e5744` stopped before the compiler. Every archive
member matched the exact recorded index (3,764 entries, 59,336,122 bytes), but
the helper expected 21 excluded entries while that same index contains 22.
The failure is in the diagnostic helper; the product candidate was not tested.

Original command/monitor/runner exits are 1/0/1, attach/container exits are 1,
and the independent watchdog exited 0. Cleanup passed with no forced stop,
OOM or surviving owned process. A fresh successful daemon census verified the
exact container was absent. Admission `ca06eb56b44440c7b30aa11cd192780e`
was consumed as failed-investigated. No source archive or product file changed.

Retained here are the exact proposed source, original child/error and lifecycle
receipts, failure investigation and ordinary consumption. The 59 MB private
extracted scratch is held separately pending immediate verification disposition.
No nonfree header bodies are included. The correction belongs in a fresh packet
and owner; this outcome remains failed and makes no product compilation claim.
