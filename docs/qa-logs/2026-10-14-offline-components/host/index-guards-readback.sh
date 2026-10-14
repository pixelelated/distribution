set -e
cat /tmp/pix567-fsize-guard-controls01/controls-result.json
python3 -I -S -B -c 'import json; from pathlib import Path; r=json.loads(Path("/tmp/pix567-fsize-guard-controls01/controls-result.json").read_text()); assert r["passed"] and len(r["controls"])==9 and r["parent_mounts_unchanged"]; print("nine guard controls verified")'
