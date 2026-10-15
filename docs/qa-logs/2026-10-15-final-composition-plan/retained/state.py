#!/usr/bin/python3
"""Narrow inherited selected-state comparison around an ordinary update.
CONFIG, PHASE and CHECKER are provided by the hash-bound outer owner.
"""
import base64,hashlib,json,os,stat,types
from pathlib import Path
SYSTEM = Path('/storage/.config/system/configs/system.cfg')
ES = Path('/storage/.config/emulationstation/es_settings.cfg')
ROM = Path('/storage/roms/gb/pixelelated-installed-state.gb')
GAMELIST = ROM.with_name('gamelist.xml')
TOKEN = Path('/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat')
STAMP = Path('/storage/.cache/cloud_sync')
STATE = Path('/storage/.cache/pixelelated-installed-state-' + CONFIG['retained_id'])
BACKUPS = Path('/storage/roms/backup')
RA = {'global.retroachievements.username': 'synthetic-ra-user',
      'global.retroachievements.password': 'synthetic-ra-pass',
      'global.retroachievements.token': 'synthetic-ra-token',
      'global.retroachievements.key': 'synthetic-ra-key'}
SS = {'ScreenScraperUser': 'synthetic-ss-user', 'ScreenScraperPass': 'synthetic-ss-pass',
      'ScreenScraperDevId': 'synthetic-developer', 'ScreenScraperDevPass': 'synthetic-dev-pass'}
KNOBS = {'global.retroachievements': '0', 'global.retroachievements.offlineproxy': '0',
         'cloudsaves.startup': '0', 'cloudsaves.gameexit': '0',
         'rehearsal.installed-state': 'synthetic-preserved'}
ES_EXTRA = {'CollectionSystemsAuto': 'favorites,recent'}
ROM_BYTES = b'PIXELELATED SYNTHETIC METADATA FIXTURE\n'
TOKEN_BYTES = b'synthetic-standalone-token\n'
STAMPS = {'last-backup': b'1600000000 0\n', 'last-restore': b'1600000060 0\n'}
SECRET_BYTES = [v.encode() for k, v in {**RA, **SS}.items()
                if not k.endswith(('username', 'User', 'DevId'))] + [TOKEN_BYTES.strip()]

def require(ok, code):
    if not ok:
        raise RuntimeError(code)

def stable(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def data(path, maximum=1024 * 1024):
    path = Path(path)
    require(not path.is_symlink(), 'input-symlink')
    with path.open('rb') as f:
        before = os.fstat(f.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_size <= maximum, 'input-shape')
        result = f.read(maximum + 1)
        after = os.fstat(f.fileno())
    require(stable(before) == stable(after) and len(result) == before.st_size, 'input-changed')
    return result

def pairs(raw):
    return {key: value for section, key, value in GATE.pairs(raw) if not section}

def settings(raw):
    tree = GATE.xml(raw, 'config')
    out = {}
    for child in tree:
        name = child.attrib.get('name')
        require(name is not None and name not in out and 'value' in child.attrib, 'xml-shape')
        out[name] = child.attrib['value']
    return tree, out

def selected():
    conf = pairs(data(SYSTEM))
    _, es = settings(data(ES))
    require(all(conf.get(k) == v for k, v in {**RA, **KNOBS}.items()), 'retained-system-fields')
    require(all(es.get(k) == v for k, v in {**SS, **ES_EXTRA}.items()), 'retained-es-fields')
    require(data(ROM) == ROM_BYTES and data(TOKEN) == TOKEN_BYTES, 'retained-fixture-bytes')
    for name, value in STAMPS.items():
        require(data(STAMP / name) == value, 'retained-activity-stamp')
    root = GATE.xml(data(GAMELIST), 'gameList')
    rows = [g for g in root.findall('game') if g.findtext('path') == './' + ROM.name]
    require(len(rows) == 1, 'retained-gamelist-entry')
    require(rows[0].findtext('playcount') == '5' and rows[0].findtext('lastplayed') == '20260908T031024', 'retained-gamelist-fields')
    return {'ra_fields_equal': True, 'screenscraper_fields_equal': True,
            'automatic_operations_disabled': True, 'history_fields_equal': True,
            'activity_stamp_bytes_equal': True, 'standalone_token_equal': True}

GATE=types.ModuleType('bound_state_gate')
assert hashlib.sha256(CHECKER.encode()).hexdigest()==CONFIG['state_checker_sha256']
exec(compile(CHECKER,'<bound-state-check>','exec'),GATE.__dict__)
PRIVATE=Path('/storage/.cache/'+CONFIG['snapshot_name'])
REPORT={'status':'FAIL','phase':PHASE,'checks':{}}
def file_sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def capture():
    paths=[SYSTEM,ES,ROM,GAMELIST,TOKEN,Path('/storage/.config/cloud_sync.conf'),*(STAMP/x for x in STAMPS)]
    return {str(p):{'data':base64.b64encode(data(p)).decode(),'mode':stat.S_IMODE(p.stat().st_mode)} for p in paths}
try:
    require(PHASE in ['before','after'],'phase')
    boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip();REPORT['boot_id']=boot
    members=CONFIG['previous_members'] if PHASE=='before' else CONFIG['members']
    for name in ['etc/os-release','usr/bin/emulationstation']:
        require(file_sha('/'+name)==members[name]['sha256'],'installed-identity')
    require(sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'],'no-NIC')
    require(not any(Path('/storage/.update').iterdir()),'update-queue-empty')
    for name,h in CONFIG['retained_receipts'].items():require(file_sha(STATE/name)==h,'original-receipt')
    REPORT['checks'].update(selected());REPORT['checks']['original_retained_receipts_equal']=True
    actual=capture()
    if PHASE=='before':
        require(not PRIVATE.exists() and not PRIVATE.is_symlink(),'fresh-private-snapshot')
        PRIVATE.mkdir(mode=0o700)
        with (PRIVATE/'before.json').open('x') as f:
            os.fchmod(f.fileno(),0o600);json.dump({'boot':boot,'selected':actual},f)
    else:
        original=json.loads(data(PRIVATE/'before.json',16*1024**2))
        require(original['boot']!=boot,'boot-did-not-change')
        REPORT['changed_selected_paths']=sorted(n for n in set(original['selected'])|set(actual) if original['selected'].get(n)!=actual.get(n))
        require(not REPORT['changed_selected_paths'],'selected-bytes-or-modes-changed')
        policy=GATE.Check(GATE.Local(Path('/')),'retained-upgrade').run()
        require(policy['status']=='pass','retained-policy')
        REPORT['checks']['retained_policy_pass']=True
        REPORT['checks']['selected_bytes_and_modes_equal']=True
        REPORT['previous_boot_id']=original['boot']
        (PRIVATE/'before.json').unlink();PRIVATE.rmdir();REPORT['checks']['private_snapshot_removed']=True
    REPORT['status']='PASS'
except BaseException as error:REPORT['error']=type(error).__name__+': '+str(error)
finally:print('PIX_UPDATE_STATE='+json.dumps(REPORT,sort_keys=True),flush=True)
raise SystemExit(0 if REPORT['status']=='PASS' else 1)
