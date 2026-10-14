Exact executed bytes are retained, not edited to satisfy whitespace lint.
execution-SHA256SUMS.txt is the original execution manifest. SHA256SUMS now
checks the storage form. Use ../2026-10-14-chd-native-runtime/coordinator/
materialize-execution-packet.py --source THIS --destination FRESH_TMP_PATH
to restore the original file set/manifest before preparing any new allocation.
The helper verifies bytes and runs no fixture or service.
