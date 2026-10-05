from pathlib import Path
import hashlib,importlib.util,json,unittest
from raofflineproxy import rom_hashing
root=Path('/storage/.cache/pixelelated-native-12')
assert str(rom_hashing.__file__).startswith('/usr/lib/python3.14/site-packages/'),rom_hashing.__file__
lib=rom_hashing.load_rchash();assert lib is not None,rom_hashing._LIBRCHASH_ERROR
mapped={line.split()[-1] for line in Path('/proc/self/maps').read_text().splitlines() if 'libraproxy_rchash.so' in line}
assert mapped=={'/usr/lib/libraproxy_rchash.so'},mapped
library=Path(next(iter(mapped)))
spec=importlib.util.spec_from_file_location('installed_native_test',root/'test.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromModule(module);result=unittest.TextTestRunner(verbosity=2).run(suite)
r={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'module':str(rom_hashing.__file__),'library':str(library),'loader_name':str(lib._name),'library_sha256':hashlib.sha256(library.read_bytes()).hexdigest()}
(root/'result.json').write_text(json.dumps(r,indent=2)+'\n')
assert result.testsRun>=18 and result.wasSuccessful() and not result.skipped,r
print('PASS installed target native hashing format tests without skips',flush=True)
