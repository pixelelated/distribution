import importlib.util,sys
from pathlib import Path
s=importlib.util.spec_from_file_location("before",Path(__file__).with_name("ceremony-check-before.py"))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.ROOT=str(Path.cwd());sys.argv=["ceremony-check-before"]
sys.exit(m.main())
