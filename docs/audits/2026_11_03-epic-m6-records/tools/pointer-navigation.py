from pathlib import Path
import importlib.util
p=Path(__file__).with_name("readers.py")
s=importlib.util.spec_from_file_location("reader",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
path=".github/sessions/saved-session-state-next.md"
lines=m.blob(path).decode().splitlines()
print("SOURCE",m.SOURCE,"PATH",path,"SHA256",m.sha(m.blob(path)),"RANGES",[[184,225],[308,len(lines)+1]])
for a,b in [(184,225),(308,len(lines)+1)]:
 for n in range(a,b):print(str(n)+": "+m.mask(lines[n-1]))
