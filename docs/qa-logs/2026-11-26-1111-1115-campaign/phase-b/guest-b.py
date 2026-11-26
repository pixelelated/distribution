# #1111/#1115 phase B, the guest half: the installed connection and folder
# scripts on build 12, driven through their own module and commands. Ported
# from docs/qa-logs/2026-10-26-cloud-profiles-installed-component/payload/
# guest.py (which staged an overlay on bcc866f1); here the image ships the
# scripts, so nothing is staged.
#
#   python3 guest-b.py clean|retained
#
# Writes /storage/m7-qa/result-<phase>.json and witness-<label>.json. A
# witness holds rclone.conf section names and types, the selection, a hash of
# the profile store, the three pointers, the two sync switches and payload
# hashes -- never a credential value. QA guest only.
import configparser, fcntl, hashlib, json, os, signal, subprocess, sys, time, traceback
from pathlib import Path

ROOT = Path('/storage/m7-qa')
PHASE = sys.argv[1]
RESULT = {'phase': PHASE, 'status': 'FAIL', 'checks': []}
sys.path.insert(0, '/usr/bin')
import cloud_connections as c
import cloud_connection_profiles as p


def check(name, criteria, value, detail=''):
    RESULT['checks'].append({'name': name, 'criteria': criteria, 'pass': bool(value), 'detail': str(detail)[:400]})


def call(*args, timeout=90):
    r = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return r.returncode, r.stdout.decode(errors='replace')


def refused(fn, *a, **k):
    try:
        fn(*a, **k)
    except c.Refused as exc:
        return str(exc) or 'refused'
    except Exception as exc:
        return type(exc).__name__ + ': ' + str(exc)
    return ''


def hashes(base):
    base = Path(base)
    if not base.exists():
        return {}
    return {str(q.relative_to(base)): hashlib.sha256(q.read_bytes()).hexdigest()
            for q in sorted(base.rglob('*')) if q.is_file()}


def tree(base):
    base = Path(base)
    return sorted(str(q.relative_to(base)) for q in base.rglob('*')) if base.exists() else []


def pointers():
    out = {}
    if c.SYNC.exists():
        for line in c.SYNC.read_text().splitlines():
            k, sep, v = line.partition('=')
            if sep and k.strip() in ('SAVES_REMOTE', 'SETTINGS_REMOTE', 'CONTENT_REMOTE'):
                out[k.strip()] = v.strip().strip('"')
    return out


def switches():
    out = {}
    if c.SYSTEM.exists():
        for line in c.SYSTEM.read_text().splitlines():
            k, sep, v = line.partition('=')
            if sep and k.strip() in ('cloudsaves.startup', 'cloudsaves.gameexit'):
                out[k.strip()] = v.strip()
    return out


def sections():
    cp = configparser.RawConfigParser()
    if c.CONFIG.exists():
        cp.read_string(c.CONFIG.read_text())
    return {s: cp.get(s, 'type', fallback='?') for s in cp.sections()}


def lock_free():
    with open(c.LOCK, 'a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
        fcntl.flock(handle, fcntl.LOCK_UN)
        return True


def safe_active():
    try:
        return c.active() or ''
    except Exception as exc:
        return 'refused: ' + str(exc)


def setting(key, value):
    # set_setting is a shell function from /etc/profile, not a binary.
    return call('sh', '-c', f'. /etc/profile >/dev/null 2>&1; set_setting {key} {value}')


def context():
    try:
        return c.folder_context()
    except Exception as exc:
        return {'error': type(exc).__name__ + ': ' + str(exc)}


def witness(label):
    store = c.profile_store().snapshot()
    w = {'label': label, 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
         'sections': sections(), 'active_file': c.ACTIVE.read_text().strip() if c.ACTIVE.exists() else None,
         'active': safe_active(), 'state': c.setup_info().get('STATE'),
         'profile_store_sha256': hashlib.sha256(json.dumps(store, sort_keys=True, default=str).encode()).hexdigest(),
         'paths': context().get('paths'), 'pointers': pointers(), 'switches': switches(),
         'local_saves': hashes('/storage/roms/savestates'), 'remote_a': hashes(ROOT / 'remote-a'),
         'remote_b': hashes(ROOT / 'remote-b'), 'remote_a_dirs': tree(ROOT / 'remote-a'),
         'remote_b_dirs': tree(ROOT / 'remote-b')}
    (ROOT / f'witness-{label}.json').write_text(json.dumps(w, indent=1, sort_keys=True) + '\n')
    return w


def payload(w):
    return {k: w[k] for k in ('local_saves', 'remote_a', 'remote_b', 'remote_a_dirs', 'remote_b_dirs')}


def webdav_settings():
    # The QA backend's stanza, copied here by the host for this run; read,
    # never printed, and deleted by the host afterwards.
    cp = configparser.RawConfigParser()
    cp.read_string((ROOT / 'qa-webdav.conf').read_text())
    s = cp.sections()[0]
    out = []
    for k, v in cp.items(s):
        if k == 'type':
            continue
        if k == 'pass':
            # The stanza holds rclone's obscured form; the page hands save()
            # what the player typed, which save() obscures. Reveal it here, on
            # the guest, so it is obscured once (run-1529Z failed on twice).
            r = subprocess.run(['/usr/bin/rclone', 'reveal', v], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=20)
            v = r.stdout.decode().strip()
        out.append((k, v))
    return out


def alias(name):
    (ROOT / name).mkdir(exist_ok=True)
    return [('remote', str(ROOT / name))]


try:
    osr = Path('/etc/os-release').read_text()
    RESULT['build_id'] = next((l.split('=', 1)[1].strip('"') for l in osr.splitlines() if l.startswith('BUILD_ID=')), '')
    RESULT['rclone'] = call('/usr/bin/rclone', 'version')[1].splitlines()[0]
    check('disposable-guest', '-', 'GENERIC_X64' in osr)
    if PHASE == 'clean':
        # Payload a management step must never touch: local saves and a
        # synthetic file in each alias account.
        Path('/storage/roms/savestates/gb').mkdir(parents=True, exist_ok=True)
        Path('/storage/roms/savestates/gb/Probe.state1').write_bytes(os.urandom(4096))
        for n in ('remote-a', 'remote-b'):
            (ROOT / n / 'keep').mkdir(parents=True, exist_ok=True)
            (ROOT / n / 'keep' / 'owner-file.bin').write_bytes(os.urandom(2048))
        w0 = witness('0-fresh')
        check('fresh-no-connections', 'C01', w0['sections'] == {} and w0['state'] == 'no-connections', w0['state'])
        check('fresh-autosync-off', 'C06', switches().get('cloudsaves.startup', '0') != '1' and switches().get('cloudsaves.gameexit', '0') != '1', switches())

        # 1. the first link on a fresh install is In use; the defaults; sync stays off
        c.save('QA_A', 'alias', alias('remote-a'))
        w1 = witness('1-first')
        check('first-link-in-use', 'C01', c.active() == 'QA_A' and w1['state'] == 'selected', (c.active(), w1['state']))
        check('first-link-defaults', 'C04', w1['paths'] == p.DEFAULTS, w1['paths'])
        check('first-link-sync-off', 'C06', w1['switches'] == w0['switches'], w1['switches'])
        check('first-link-no-payload-change', 'C07', payload(w1) == payload(w0))

        # 2. a failed link selects nothing and leaves nothing
        dead = refused(c.save, 'QA_DEAD', 'webdav', [('url', 'http://10.0.2.2:9/'), ('vendor', 'other')])
        w2 = witness('2-failed-link')
        check('failed-link-refused', 'C01,C06', dead != '', dead)
        check('failed-link-nothing-kept', 'C01,C06', 'QA_DEAD' not in w2['sections'] and c.active() == 'QA_A', (sorted(w2['sections']), c.active()))
        check('failed-link-profile-unchanged', 'C06', w2['profile_store_sha256'] == w1['profile_store_sha256'])

        # 3. this connection's own folders; a second connection keeps the selection
        c.set_folders(c.folder_context()['context_id'], {'saves': '/Custom/Saves'})
        check('custom-folder-projected', 'C02', p.legacy_paths(c.SYNC.read_bytes())['saves'] == '/Custom/Saves', pointers())
        c.save('QA_B', 'alias', alias('remote-b'))
        w3 = witness('3-second')
        check('second-link-keeps-selection', 'C01,C05', c.active() == 'QA_A', c.active())
        check('second-link-keeps-active-paths', 'C05', w3['paths']['saves'] == '/Custom/Saves', w3['paths'])
        token = c.folder_context()['context_id']
        c.select('QA_B')
        w4 = witness('4-switched-to-b')
        check('switch-b-defaults', 'C02,C04', w4['paths'] == p.DEFAULTS, w4['paths'])
        stale = refused(c.set_folders, token, {'saves': '/Wrong'})
        check('stale-editor-refused', 'C14,C06', stale != '', stale)
        c.select('QA_A')
        w5 = witness('5-switched-back')
        check('switch-a-keeps-its-folders', 'C02', w5['paths']['saves'] == '/Custom/Saves', w5['paths'])
        c.save('QA_A', 'alias', alias('remote-a'), replace=True)
        w6 = witness('6-renewed')
        check('renewal-keeps-folders', 'C05', w6['paths']['saves'] == '/Custom/Saves' and c.active() == 'QA_A', w6['paths'])
        check('switching-no-payload-change', 'C07', payload(w6) == payload(w0))

        # 4. busy and automatic sync refuse management, and leave nothing half-done
        # The holder and its sleep child in a session of their own: killing
        # flock alone leaves sleep holding the lock (run-1526Z, where the next
        # step was refused as busy and two autosync checks passed on the lock).
        holder = subprocess.Popen(['flock', str(c.LOCK), 'sleep', '60'], start_new_session=True)
        time.sleep(1)
        check('lock-held-for-busy', 'C06', not lock_free(), 'the lock was free')
        busy = refused(c.select, 'QA_B')
        busy_defaults = refused(c.set_folders, c.folder_context()['context_id'], None, True)
        os.killpg(holder.pid, signal.SIGTERM); holder.wait()
        for _ in range(20):
            if lock_free():
                break
            time.sleep(0.5)
        check('lock-released-after-busy', 'C06', lock_free(), 'the lock is still held')
        w7 = witness('7-busy')
        check('busy-select-refused', 'C06', 'operation is running' in busy, busy)
        check('busy-defaults-refused', 'C06,C22', 'operation is running' in busy_defaults, busy_defaults)
        check('busy-nothing-changed', 'C06', c.active() == 'QA_A' and w7['paths'] == w6['paths'] and w7['profile_store_sha256'] == w6['profile_store_sha256'])
        setting('cloudsaves.gameexit', '1')
        auto = refused(c.select, 'QA_B')
        auto_remove = refused(c.remove, 'QA_B')
        setting('cloudsaves.gameexit', '0')
        w8 = witness('8-autosync')
        check('autosync-select-refused', 'C06', 'automatic save sync' in auto, auto)
        check('autosync-remove-refused', 'C06', 'automatic save sync' in auto_remove and 'QA_B' in w8['sections'], auto_remove)
        check('autosync-nothing-changed', 'C06', c.active() == 'QA_A' and w8['paths'] == w6['paths'])

        # 5. USE pixelelated DEFAULTS on A only; B keeps its own
        c.select('QA_B')
        c.set_folders(c.folder_context()['context_id'], {'saves': '/B/Saves'})
        c.select('QA_A')
        c.set_folders(c.folder_context()['context_id'], defaults=True)
        w9 = witness('9-defaults')
        check('defaults-applied-to-selected', 'C21', w9['paths'] == p.DEFAULTS, w9['paths'])
        c.select('QA_B')
        check('defaults-left-other-alone', 'C21', c.folder_context()['paths']['saves'] == '/B/Saves', c.folder_context()['paths'])
        check('defaults-no-cloud-folders-created', 'C07,C21', payload(witness('9b-other')) == payload(w0))

        # 6. removing the active connection while another remains selects nothing
        c.remove('QA_B')
        w10 = witness('10-removed-active')
        check('remove-active-no-fallback', 'C01', w10['state'] == 'unselected' and 'QA_A' in w10['sections'], (w10['state'], w10['active_file']))
        ctx = context()
        check('no-selection-actionable', 'C10', w10['state'] == 'unselected' and ('error' in ctx or ctx.get('paths') is None), ctx)
        c.select('QA_A')
        w11 = witness('11-selected-again')
        check('explicit-select-restores-rows', 'C10', w11['state'] == 'selected' and w11['paths'] == w9['paths'], w11['paths'])

        # 7. remove all; re-add: same name, a new name, a different backend
        c.set_folders(c.folder_context()['context_id'], {'saves': '/Gone/Saves', 'settings': '/Gone/Backups'})
        c.remove('QA_A')
        w12 = witness('12-none')
        check('remove-all-unselected-or-empty', 'C01', w12['sections'] == {} and w12['state'] == 'no-connections', w12['state'])
        c.save('QA_A', 'alias', alias('remote-a'))
        w13 = witness('13-readd-same')
        check('readd-same-name-in-use', 'C01', c.active() == 'QA_A', c.active())
        check('readd-same-name-defaults', 'C04', w13['paths'] == p.DEFAULTS, w13['paths'])
        c.save('QA_C', 'alias', alias('remote-b'))
        c.select('QA_C')
        check('new-name-defaults', 'C04', c.folder_context()['paths'] == p.DEFAULTS, c.folder_context()['paths'])
        dav = ''
        try:
            c.save('QA_W', 'webdav', webdav_settings())
        except Exception as exc:
            dav = type(exc).__name__ + ': ' + str(exc)
        check('webdav-link', 'C04', dav == '' and sections().get('QA_W') == 'webdav', dav or sections())
        if dav == '':
            c.select('QA_W')
            w14 = witness('14-webdav')
            check('different-backend-defaults', 'C04', w14['paths'] == p.DEFAULTS, w14['paths'])
            check('deleted-paths-not-reused', 'C04', '/Gone/Saves' not in json.dumps(w14['paths']) and '/Gone/Saves' not in json.dumps(w14['pointers']), w14['pointers'])
        c.select('QA_A')
        w15 = witness('15-end-clean')
        check('management-no-payload-change', 'C07', payload(w15) == payload(w0))
        check('autosync-never-enabled', 'C06', not any(v == '1' for v in w15['switches'].values()), w15['switches'])

        # 8. the settings-backup pointer under the new wording: the default is /pixelelated/Backups
        check('settings-backup-default', 'C25', w15['paths'].get('settings') == '/pixelelated/Backups', w15['paths'])

        # for the retained phase: custom folders on A, B-account C keeps defaults
        c.set_folders(c.folder_context()['context_id'], {'saves': '/Retained/Saves'})
        (ROOT / 'expected-retained.json').write_text(json.dumps({'active': c.active(), 'paths': c.folder_context()['paths'],
                                                                  'sections': sections()}))
        witness('16-before-reboot')
    else:
        exp = json.loads((ROOT / 'expected-retained.json').read_text())
        r0 = witness('20-after-reboot')
        check('retained-selection', 'C09', c.active() == exp['active'], c.active())
        check('retained-paths', 'C09', r0['paths'] == exp['paths'], r0['paths'])
        check('retained-sections', 'C09', r0['sections'] == exp['sections'], sorted(r0['sections']))
        # a restored global pointer that disagrees with the profile is review, not adoption
        original = c.SYNC.read_bytes()
        c.SYNC.write_bytes(p.project(original, {**p.DEFAULTS, 'saves': '/Restored/Other'}))
        state = c.setup_info()['STATE']
        check('restored-pointer-needs-review', 'C10,C11', state == 'review-folders', state)
        c.select(exp['active'])
        check('explicit-select-repairs-pointer', 'C10', c.setup_info()['STATE'] == 'selected' and p.legacy_paths(c.SYNC.read_bytes())['saves'] == '/Retained/Saves', pointers())
        # the validator, bound to the current configuration, on the selected account
        for rel in ('pixelelated/Backups',):
            (ROOT / 'remote-a' / rel).mkdir(parents=True, exist_ok=True)
        (ROOT / 'remote-a' / 'Retained' / 'Saves').mkdir(parents=True, exist_ok=True)
        rc, raw = call('/usr/bin/cloud_folder_validate', 'saves,settings', 'phaseb01')
        (ROOT / 'validator-empty.json').write_text(raw)
        try:
            v = json.loads(raw)
        except ValueError:
            v = {}
        check('validator-bound-to-config', 'C11,1115C05', v.get('config_id') == c.validation_context().get('config_id'), (rc, raw[:200]))
        check('validator-empty-accessible', '1115C02,1115C05', all(r.get('state') == 'empty' and r.get('access') == 'accessible' for r in v.get('categories', [])) and len(v.get('categories', [])) == 2, raw[:300])
        # an entry limit in settings: accessible, inspection limited; saves still complete
        big = ROOT / 'remote-a' / 'pixelelated' / 'Backups' / 'many'
        big.mkdir(parents=True, exist_ok=True)
        for i in range(4097):
            (big / f'f{i:05d}.bin').write_bytes(b'x')
        (ROOT / 'remote-a' / 'Retained' / 'Saves' / 'gb').mkdir(parents=True, exist_ok=True)
        (ROOT / 'remote-a' / 'Retained' / 'Saves' / 'gb' / 'Game.srm').write_bytes(b'save')
        before = hashes(ROOT / 'remote-a')
        rc2, raw2 = call('/usr/bin/cloud_folder_validate', 'saves,settings', 'phaseb02', timeout=120)
        (ROOT / 'validator-limited.json').write_text(raw2)
        try:
            v2 = json.loads(raw2)
        except ValueError:
            v2 = {}
        rows = {r.get('category'): r for r in v2.get('categories', [])}
        check('limited-settings-still-accessible', '1115C02', rows.get('settings', {}).get('access') == 'accessible' and not v2.get('complete', True), json.dumps(rows.get('settings', {}))[:300])
        check('saves-result-survives-limit', '1115C02', rows.get('saves', {}).get('state') == 'present', json.dumps(rows.get('saves', {}))[:300])
        check('validator-read-only', '1115C03', hashes(ROOT / 'remote-a') == before)
        RESULT['validator_limited_rc'] = rc2
        # the other backend: the WebDAV account, selected, its folders checked read-only
        if 'QA_W' in sections():
            c.select('QA_W')
            rc3, raw3 = call('/usr/bin/cloud_folder_validate', 'saves,settings', 'phaseb03', timeout=120)
            (ROOT / 'validator-webdav.json').write_text(raw3)
            try:
                v3 = json.loads(raw3)
            except ValueError:
                v3 = {}
            check('webdav-validator-answers', '1115C05', rc3 in (0, 5) and v3.get('config_id') == c.validation_context().get('config_id'), (rc3, raw3[:200]))
            c.select(exp['active'])
        w = witness('21-end-retained')
        check('retained-end-selection', 'C09', c.active() == exp['active'], c.active())
    check('no-pending-journal', 'C22', not c.CONFIG.with_name('settings-transaction.json').exists())
    RESULT['status'] = 'PASS' if all(x['pass'] for x in RESULT['checks']) else 'FAIL'
except BaseException as exc:
    RESULT['error'] = type(exc).__name__ + ': ' + str(exc)
    RESULT['traceback'] = traceback.format_exc()
finally:
    (ROOT / f'result-{PHASE}.json').write_text(json.dumps(RESULT, indent=1) + '\n')
    print(json.dumps({'phase': PHASE, 'status': RESULT['status'], 'failed': [x['name'] for x in RESULT['checks'] if not x['pass']],
                      'error': RESULT.get('error', '')}))
sys.exit(0 if RESULT['status'] == 'PASS' else 1)
