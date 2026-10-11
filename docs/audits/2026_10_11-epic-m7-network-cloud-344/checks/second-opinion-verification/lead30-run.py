from pathlib import Path
import importlib.util,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
O=Path('/tmp/pix537-lead-probe30')
v.scp(O/'guest.py','/storage/qa537/lead30.py')
print(v.remote('python3 /storage/qa537/lead30.py'),flush=True)
(O/'result.json').write_text(v.remote('cat /storage/qa537/lead30/result.json')+'\n')
