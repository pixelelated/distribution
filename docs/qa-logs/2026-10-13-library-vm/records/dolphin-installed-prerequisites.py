from pathlib import Path
import json
from ui import out
r=Path(__file__).parent
result=out("python3 - <<'P'\nfrom pathlib import Path\nimport json\npaths=['/usr/bin/runemu.sh','/usr/bin/start_dolphin.sh','/usr/bin/start_dolphin_wii.sh','/usr/bin/dolphin-save-paths','/usr/config/dolphin-emu','/usr/share/themes/es-theme-art-book-next','/usr/config/locale/fr_FR']\nprint(json.dumps({p:{'exists':Path(p).exists(),'is_symlink':Path(p).is_symlink()} for p in paths},indent=2))\nprint(json.dumps([str(p) for p in Path('/run').glob('**/wayland-*') if p.is_socket()]))\nP")
(r/'records/dolphin-installed-prerequisites.txt').write_text(result)
