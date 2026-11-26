# #1111/#1115 phase D, guest helper: a second connection through the installed
# module (never a stanza appended behind its back: cal-640-en's s08 did that,
# left the profile out of date and the rest of the batch in review), and the
# state each screen starts from.
#   python3 conn.py add-two | remove-two | state | repair
import configparser, subprocess, sys
sys.path.insert(0, '/usr/bin')
import cloud_connections as c


def qa_settings():
    cp = configparser.RawConfigParser()
    cp.read_string(c.CONFIG.read_text())
    out = []
    for k, v in cp.items('qa-cloud'):
        if k == 'type':
            continue
        if k == 'pass':
            v = subprocess.run(['/usr/bin/rclone', 'reveal', v], stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, timeout=20).stdout.decode().strip()
        out.append((k, v))
    return out


def state():
    info = c.setup_info()
    cp = configparser.RawConfigParser()
    cp.read_string(c.CONFIG.read_text())
    return f"STATE={info['STATE']} CONNECTION={info['CONNECTION']} SECTIONS={','.join(cp.sections())} SYNC={info['SYNC_STARTUP']}/{info['SYNC_GAMEEXIT']}"


cmd = sys.argv[1]
if cmd == 'add-two':
    c.save('qa-two', 'webdav', qa_settings())
elif cmd == 'remove-two':
    c.remove('qa-two')
elif cmd == 'repair':
    cp = configparser.RawConfigParser()
    cp.read_string(c.CONFIG.read_text())
    if 'qa-two' in cp.sections():
        c.select('qa-cloud')
        c.remove('qa-two')
    c.select('qa-cloud')
print(state())
