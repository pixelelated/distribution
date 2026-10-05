# Measured checksum progress routing (#437)

The original replacement09 adapter wrote JSON while watch-job scans only
`*.log`. The fresh-context proof observed a legitimate suspected-stall warning
after 373 seconds without a watched write, alongside real rsync read advances.
Original observations and eventual checksum/inode success are retained here;
the original copy was not restarted or relabelled.

Run `python3 observe-checksum.py COPY_OWNER` from the actual host while an owned
copy is active. The adapter verifies the root owner and descendant rsync PIDs.
Only a positive read delta from the same PID/start identity appends the watched
`copy-artifacts/checksum-progress.log`. First, unchanged, restarted and regressed
counters create no activity. A delta proves reads, not checksum acceptance.

Actual tool12429 returned0. Six isolated controls use the actual watch-job:
JSON-only stalled; first sample silent; positive delta recognized at the exact
log path; unchanged, restarted and regressed samples preserve log bytes/mtime.
Counters are synthetic fixtures, not a repeated real-copy proof. Owned sandbox
processes6/7 were deliberately terminated and observed absent. This adapter is
ready for the next cache copy; it was not retrofitted into the completed owner.
No product, frozen input or executed shell owner changed. This does not provide
the disconnected notification delivery still tracked by #395.
