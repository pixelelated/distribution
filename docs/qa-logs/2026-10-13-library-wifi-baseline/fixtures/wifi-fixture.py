#!/usr/bin/python3
# Synthetic VM-only Wi-Fi enumeration; never runs NetworkManager or joins a network.
import json,sys,time
from pathlib import Path
r=Path('/storage/qa-m7-baseline');command=sys.argv[1] if len(sys.argv)>1 else ''
if command in ['list','scanlist']:
 mode=json.loads((r/'wifi-mode.json').read_text());started=time.time()
 with (r/'wifi-calls.jsonl').open('a') as f:f.write(json.dumps({'phase':'start','time':started,'command':command,'mode':mode})+'\n')
 time.sleep(mode.get('delay',0))
 rc=2 if mode.get('outcome')=='failure' else 0
 if mode.get('outcome')=='networks':
  for i in range(mode.get('count',3)):print('Test network %02d'%(i+1))
 with (r/'wifi-calls.jsonl').open('a') as f:f.write(json.dumps({'phase':'end','time':time.time(),'command':command,'rc':rc})+'\n')
 raise SystemExit(rc)
if command=='current':raise SystemExit(1)
if command=='saved':raise SystemExit(0)
if command=='has_ap_mode':raise SystemExit(1)
if command=='security':print('open');raise SystemExit(0)
# Unsupported operations fail closed; this fixture cannot change network state.
raise SystemExit(2)
