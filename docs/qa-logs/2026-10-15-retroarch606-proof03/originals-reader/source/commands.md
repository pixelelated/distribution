# Later root-owned bounded originals readback — UNRUN

Use the existing host-only watched reader path after source review. No VM/preparer or new producer is involved. Inspect the actual original reader exit/result; do not alter run03's failed result or failed-investigated consumption.

```bash
TASK_READER=/tmp/pix-m7-retroarch606-originals-reader-20261015-01
TASK_RESULT=/tmp/pix-m7-retroarch606-originals-result-20261015-01
cd "$TASK_READER"
sha256sum -c SHA256SUMS
cd /workspace/repos/rocknix.worktrees/m7-player-setup
tools/watch-build --record-only -- python3 -I -S -B \
  "$TASK_READER/verify-originals.py" --output "$TASK_RESULT"
```

Root retains original watcher/tool/reader exits and result.json. PASS_RETAINED_ORIGINALS_WITH_FAILED_PRODUCER qualifies only the retained selected observations. A failed readback is retained separately without automatic retries, producer edits or VM replay. All455 original members and supplemental references must remain at their sealed original paths. The exact initial source image is never opened.
