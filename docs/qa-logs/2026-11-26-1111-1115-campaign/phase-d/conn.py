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


def two_hash():
    # The witness for "the existing connection was kept": a hash of qa-two's
    # section, never its values (they hold the account's credentials).
    import hashlib
    cp = configparser.RawConfigParser()
    cp.read_string(c.CONFIG.read_text())
    if 'qa-two' not in cp.sections():
        return 'TWO=absent'
    body = '\n'.join(f'{k}={v}' for k, v in sorted(cp.items('qa-two')))
    return 'TWO=' + hashlib.sha256(body.encode()).hexdigest()


cmd = sys.argv[1]
if cmd == 'add-two':
    c.save('qa-two', 'webdav', qa_settings())
elif cmd == 'break-two':
    # qa-two's endpoint moved to a port nothing answers, written behind the
    # module as a provider outage would leave it: an edit that re-verifies it
    # must fail and keep the section as it is (s19).
    import os, re
    text = c.CONFIG.read_text()
    head, sep, rest = text.partition('[qa-two]')
    if not sep:
        sys.exit('no qa-two section')
    nxt = rest.find('\n[')
    section, tail = (rest, '') if nxt < 0 else (rest[:nxt], rest[nxt:])
    section, n = re.subn(r'^(url = https?://[^:/\s]+):\d+', r'\g<1>:9011', section, flags=re.M)
    if n != 1:
        sys.exit('qa-two url not rewritten')
    tmp = c.CONFIG.with_suffix('.s19')
    tmp.write_text(head + sep + section + tail)
    os.chmod(tmp, 0o600)
    os.replace(tmp, c.CONFIG)
    print(two_hash())
elif cmd == 'add-oauth':
    # An OAuth-tier connection with no sign-in at all: enough for its page
    # to offer SIGN IN AGAIN (#1486); nothing credential-shaped is written.
    import os
    text = c.CONFIG.read_text()
    if '[qa-oauth]' in text:
        sys.exit('qa-oauth already present')
    tmp = c.CONFIG.with_suffix('.s29')
    tmp.write_text(text.rstrip('\n') + '\n\n[qa-oauth]\ntype = dropbox\n')
    os.chmod(tmp, 0o600)
    os.replace(tmp, c.CONFIG)
elif cmd == 'remove-oauth':
    import os
    text = c.CONFIG.read_text()
    head, sep, rest = text.partition('[qa-oauth]')
    if sep:
        nxt = rest.find('\n[')
        tmp = c.CONFIG.with_suffix('.s29')
        tmp.write_text(head.rstrip('\n') + '\n' + ('' if nxt < 0 else rest[nxt + 1:]))
        os.chmod(tmp, 0o600)
        os.replace(tmp, c.CONFIG)
elif cmd == 'two-hash':
    print(two_hash())
elif cmd == 'remove-two':
    c.remove('qa-two')
elif cmd == 'repair':
    if '[qa-oauth]' in c.CONFIG.read_text():
        import subprocess
        subprocess.run([sys.executable, __file__, 'remove-oauth'], check=True, stdout=subprocess.DEVNULL)
    cp = configparser.RawConfigParser()
    cp.read_string(c.CONFIG.read_text())
    if 'qa-two' in cp.sections():
        c.select('qa-cloud')
        c.remove('qa-two')
    c.select('qa-cloud')
print(state())
