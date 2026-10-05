#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-sweep-08
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09
TASK_ROOT=/workspace/tmp/pixelelated-m7-image-11/root
TASK_BUILD="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64"
test ! -e "$TASK_OWNER/start"
test "$(cat /workspace/tmp/pixelelated-m7-image-11/outer.rc)" = 0
sha256sum -c "$TASK_OWNER/harness.sha256"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/start"
pwd > "$TASK_OWNER/execution-cwd"
printf '%s\n' "${RASTERATOPS_BUILD_RUN:?use shared watcher}" > "$TASK_OWNER/run.relative"
finish() { result=$?; trap - EXIT; printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"; exit "$result"; }
trap finish EXIT
python3 - <<'READABLE'
from pathlib import Path
import json,stat
p=Path('/workspace/tmp/pixelelated-m7-image-11/root/usr/cache/shadow')
mode=stat.S_IMODE(p.stat().st_mode)
assert mode==0
p.chmod(0o400)
Path('/workspace/tmp/pixelelated-m7-sweep-08/artifacts/extraction-read-permissions.json').write_text(json.dumps({'path':'usr/cache/shadow','original_mode':'0000','analysis_mode':'0400','scope':'owned extracted analysis copy only; immutable image unchanged'},indent=2)+'\n')
READABLE
python3 "$TASK_OWNER/check-controls.py" --scanner "$TASK_OWNER/scan-artifact.py" --patterns "$TASK_OWNER/secret-patterns" --output "$TASK_OWNER/artifacts/controls.json"
python3 -u "$TASK_OWNER/scan-artifact.py" --root "$TASK_ROOT" --allowlist "$TASK_OWNER/allowlist.json" --patterns "$TASK_OWNER/secret-patterns" --output "$TASK_OWNER/artifacts/artifact-report.json"
g++ -O2 -I "$TASK_BUILD/build/pugixml-1.16/src" "$TASK_OWNER/parse-theme.cpp" "$TASK_BUILD/build/pugixml-1.16/src/pugixml.cpp" -o "$TASK_OWNER/parse-theme"
"$TASK_OWNER/parse-theme" "$TASK_ROOT/usr/share/themes/es-theme-art-book-next/theme.xml" "$TASK_OWNER/artifacts/parsed-theme.xml"
python3 "$TASK_OWNER/reconcile-locales.py" --root "$TASK_ROOT" --es /home/max/Development/emulationstation-next.worktrees/qa-integration --es-build "$TASK_BUILD/build/emulationstation-f6f0c134212bc696f2f6a747c8d390a588f2f0ce" --tree "$TASK_TREE" --parsed-theme "$TASK_OWNER/artifacts/parsed-theme.xml" --output "$TASK_OWNER/artifacts/localisation.json"
python3 - <<'CHECK'
from pathlib import Path
import json
p=Path('/workspace/tmp/pixelelated-m7-sweep-08/artifacts');j=json.loads((p/'artifact-report.json').read_text());assert j['pass'];j=json.loads((p/'localisation.json').read_text());assert j['installed_tools_xml_valid'] and j['installed_tools_matches_corrected_source'] and not j['known_image_corrections']
print('PASS corrected image content sweeps and exact installed Tools XML')
CHECK
