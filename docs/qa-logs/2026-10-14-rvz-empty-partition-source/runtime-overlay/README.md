# #574 additive RVZ generator binding for a fresh guest admission

This runtime packet reuses guest-run.py, guest-work.py, guest_support.py and
controls.py byte-for-byte from d92e127fa5. Only metadata/bindings are replaced.
The candidate generator initializes SHA1(empty) in Header2.partition_entries_hash;
its source is docs/qa-logs/2026-10-14-rvz-empty-partition-source/make-fixtures.py.
The matching oracle-source-bindings.json changes only original_generator_sha256.
Actual ELF hashes, loader/help checks, full independent decoding, original child
exits, sanitized environment, 240s total limit, 2GiB budget and cleanup are unchanged.

Original attempt01 remains FAIL1: decode-0 returned1; no later native format
commands ran. No repaired fixture is independently accepted until this new guest
admission passes the unchanged decoder and encoder/hash checks.

Assemble the exact input tree from the original independent-format-guest README,
using this runtime-overlay in packet/, the new generator in original/, and the
new oracle-source-bindings.json as oracle/source-bindings.json. Every other public
input remains exact. Use fresh empty executable tmpfs /run/pix574-scratch (0700,
max2GiB), read-only /tmp/pix-input, writable /tmp/pix-output, and no NIC except lo.
Coordinator alone creates/supervises/retires the new VM20. Python3.11+ is required.

    python3 -I -S -B /tmp/pix-input/pix574-format/packet/guest-run.py --run-id format02

All repaired-source controls and runtime are UNRUN by the source worker. The
prepared parser controls still do not prove actual cleanup. Sys lookup remains
unmeasured; help precedes user-directory initialization. Retain both independently
encoded RVZs and original receipt channels before coordinator retirement.
