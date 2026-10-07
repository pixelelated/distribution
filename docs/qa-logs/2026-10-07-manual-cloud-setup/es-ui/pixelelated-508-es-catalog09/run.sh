#!/bin/bash
set -euo pipefail
O=/tmp/pixelelated-508-es-catalog09
E=/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup
B=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64
trap 'rc=$?; printf "%s\n" "$rc" > "$O/inner.rc"' EXIT
"$B/toolchain/bin/msgfmt" --check --check-format -o "$O/artifacts/fr.mo" "$E/locale/lang/fr/LC_MESSAGES/emulationstation2.po"
git -C "$E" diff --check
python3 - <<'PY'
from pathlib import Path
import gettext,hashlib,json
p=Path('/tmp/pixelelated-508-es-catalog09/artifacts/fr.mo');g=gettext.GNUTranslations(p.open('rb'));strings=['CLOUD SETUP','YOUR CLOUD FOLDERS COULD NOT BE CREATED','CHECK YOUR CONNECTION, THEN TRY AGAIN.','USE CHANGE CLOUD FOLDER ON EACH DEVICE.','CONTINUE','COPY ROMS INTO THE ROMS FOLDER AND BIOS FILES INTO THE BIOS FOLDER.','CLOUD SETTINGS ARE NOW AVAILABLE IN GAME SETTINGS.','SET UP FOR YOU IN YOUR CLOUD ACCOUNT, IF NOT ALREADY THERE:','BACK UP SETTINGS AND SAVES NOW']
for s in strings:assert g.gettext(s)!=s,s
(p.parent/'catalog.json').write_text(json.dumps({'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lookups':{s:g.gettext(s) for s in strings}},ensure_ascii=False,indent=2)+'\n')
print('PASS all new completion and failure copy resolves to French')
PY
