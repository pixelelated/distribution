#!/bin/bash
set -euo pipefail
TASK_PROXY=/tmp/pixelelated-proxy-ea9aba
TASK_REPO=/workspace/repos/rocknix.worktrees/conflict-resolution
cd "$TASK_PROXY/new-patched"
PYTHONPATH=. python3 -c 'import linux.raofflineproxy.storage; print("PASS actual-cwd imports")'
PYTHONPATH=.:linux/tests python3 -m unittest test_linux_award_parity test_linux_caching_queue test_linux_usage_stats test_linux_image_cache_shutdown test_linux_network test_linux_refresh_scope test_linux_rocknix test_linux_release_versions > "$TASK_PROXY/test-artifacts-02/upstream-tests.log" 2>&1
tail -4 "$TASK_PROXY/test-artifacts-02/upstream-tests.log"
cd "$TASK_REPO"
tools/raofflineproxy-integration-test --source "$TASK_PROXY/new-patched" --predecessor-source "$TASK_PROXY/old-patched" > "$TASK_PROXY/test-artifacts-02/fork-tests.log" 2>&1
tail -4 "$TASK_PROXY/test-artifacts-02/fork-tests.log"
tools/pkgcheck projects/ROCKNIX/packages/network/raofflineproxy
tools/rc-preflight --only proxy-schema
