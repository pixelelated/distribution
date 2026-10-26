# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2026 pixelelated
"""Local connection transactions. No cloud mutations; only bounded listings.

One active connection is persisted separately from credentials. Missing selection
preserves the legacy first remote; an explicit empty selection never falls back.
All writers share the transfer lock. New credentials are verified in a private
config and only then installed; failed/cancelled attempts leave old bytes intact.
"""
import configparser
import contextlib
import fcntl
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

RCLONE = '/usr/bin/rclone'
CONFIG = Path('/storage/.config/rclone/rclone.conf')
ACTIVE = CONFIG.with_name('active-connection')
LOCK = Path('/var/run/cloud_sync.lock')
SYSTEM = Path('/storage/.config/system/configs/system.cfg')

class Refused(Exception):
    pass


def read_config(path= None):
    path = CONFIG if path is None else path
    raw = path.read_bytes() if path.exists() else b''
    parser = configparser.RawConfigParser(strict=True)
    parser.optionxform = str
    try:
        parser.read_string(raw.decode('utf-8'))
    except (UnicodeError, configparser.Error):
        # rclone can read encrypted configurations using its normal password
        # mechanism. Keep that existing capability; never echo the dump.
        import json
        try:
            result = subprocess.run([RCLONE, '--config', str(path), 'config', 'dump'],
                                    capture_output=True, text=True, timeout=8)
            if result.returncode:
                raise ValueError()
            data = json.loads(result.stdout)
            parser = configparser.RawConfigParser(interpolation=None)
            parser.optionxform = str
            parser.read_dict(data)
        except (ValueError, configparser.Error, subprocess.TimeoutExpired):
            raise Refused('Cloud connection settings could not be read.')
    return raw, parser


def active(config=None):
    if config is None:
        _, config = read_config()
    if ACTIVE.exists():
        value = ACTIVE.read_text().removesuffix('\n')
        if value and not config.has_section(value):
            raise Refused('The selected connection is missing. Choose a connection first.')
        return value
    return next(iter(sorted(config.sections())), '')


def selection_reason():
    """Safe player-facing reason when no usable selected account was resolved."""
    _, config = read_config()
    return ("CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS." if config.sections()
            else "YOUR CLOUD STORAGE ISN'T SET UP YET")


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def restore_selection(previous, written):
    # Only undo our write; never clobber an outside settings writer.
    if written is None or not ACTIVE.exists() or ACTIVE.read_bytes() != written:
        return
    if previous is not None:
        atomic(ACTIVE, previous)
    else:
        ACTIVE.unlink()
        directory = os.open(ACTIVE.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)


@contextlib.contextmanager
def locked():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open('a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Refused('A cloud operation is running. Wait for it to finish, then try again.')
        yield


def require_manual():
    # Same literal keys as ES. Read text, never execute system.cfg.
    values = {}
    if SYSTEM.exists():
        for line in SYSTEM.read_text().splitlines():
            key, sep, value = line.partition('=')
            if sep:
                values[key.strip()] = value.strip()
    if any(values.get(k) == '1' for k in ('cloudsaves.startup', 'cloudsaves.gameexit')):
        raise Refused('Turn off both automatic save sync options before changing this connection.')


def run(args):
    try:
        result = subprocess.run([RCLONE] + args, capture_output=True, text=True, timeout=40)
    except subprocess.TimeoutExpired:
        raise Refused('The connection stopped answering. Your settings were not changed.')
    if result.returncode:
        # Never forward provider diagnostics: they may contain credentials.
        raise Refused('The connection could not be verified. Your settings were not changed.')
    return result.stdout


# A setting's key is an rclone option name. Joined as key=value into rclone's
# arguments, a key shaped like a flag was a flag: --config=<path> wrote the new
# connection, secret and all, to <path>, and --log-file= was honoured too
# (#1131, T17's F-20, found by both seats). Option names are lowercase words.
OPTION_KEY = re.compile(r'[a-z0-9_]+')


def sweep_staging():
    """An earlier save or remove killed before its cleanup (SIGKILL, power)
    left its private copy, with the old or new credentials, beside rclone.conf,
    and nothing removed it (#1131, T17's F-06). Called under the lock, which
    every writer of these names holds, so none of them is in use."""
    if not CONFIG.parent.is_dir():
        return
    prefixes = ('.' + CONFIG.name + '-', '.' + ACTIVE.name + '-')
    for entry in CONFIG.parent.iterdir():
        if entry.name.startswith('.connection-') and entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry, ignore_errors=True)
        elif entry.name.startswith(prefixes) and (entry.is_file() or entry.is_symlink()):
            entry.unlink(missing_ok=True)


def save(name, backend, settings, replace=False, publish=None, check_current=None):
    if not name or name != name.strip() or any(c in name for c in ':[]\r\n\t') or name.startswith('-'):
        raise Refused('Give the connection a name without colons or brackets.')
    if any(not OPTION_KEY.fullmatch(key) for key, _ in settings):
        raise Refused("A setting for this connection can't be used. Your settings were not changed.")
    with locked():
        sweep_staging()
        existed = CONFIG.exists()
        original, config = read_config()
        exists = config.has_section(name)
        if replace != exists:
            raise Refused('Choose a different connection name.' if exists else 'This connection no longer exists.')
        if replace:
            require_manual()
            if config.get(name, 'type', fallback='') != backend:
                raise Refused('The connection provider changed. Open its settings again.')
        selected = active(config)
        previous_selection = ACTIVE.read_bytes() if ACTIVE.exists() else None
        written_selection = None
        CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.connection-', dir=CONFIG.parent) as directory:
            staged = Path(directory) / 'rclone.conf'
            staged.write_bytes(original)
            staged.chmod(0o600)
            args = ['--config', str(staged), 'config', 'update' if replace else 'create', name]
            if not replace:
                args.append(backend)
            args.extend('%s=%s' % pair for pair in settings)
            args += ['--non-interactive', '--obscure']
            if check_current:
                check_current()
            out = run(args)
            import json
            try:
                answer = json.loads(out or '{}')
            except ValueError:
                answer = {}
            if isinstance(answer, dict) and answer.get('State'):
                raise Refused('This provider needs additional setup. Use a computer to finish connecting it.')
            # Each subprocess is bounded. Cancellation between stages avoids
            # starting another full wait and lets private staging be cleaned.
            if check_current:
                check_current()
            run(['--config', str(staged), 'lsd', name + ':', '--contimeout', '10s', '--timeout', '20s', '--low-level-retries', '1', '--retries', '1'])
            if check_current:
                check_current()
            updated, result = read_config(staged)
            if not result.has_section(name):
                raise Refused('The connection was not saved.')

            def commit():
                nonlocal written_selection
                # Refuse an outside writer instead of overwriting its update.
                current = CONFIG.read_bytes() if CONFIG.exists() else b''
                if current != original:
                    raise Refused('Cloud settings changed during sign-in. Try again.')
                # Pin the old selection BEFORE making another name visible.
                # On a first connection the legacy fallback selects only it.
                if not ACTIVE.exists() and config.sections():
                    written_selection = (selected + '\n').encode()
                    atomic(ACTIVE, written_selection)
                atomic(CONFIG, updated)

            try:
                if publish:
                    publish(commit)
                else:
                    commit()
            except Exception:
                # A failed success-record write must not install credentials
                # that the interface reports as unsaved.
                if CONFIG.exists() and CONFIG.read_bytes() == updated:
                    if existed:
                        atomic(CONFIG, original)
                    else:
                        CONFIG.unlink()
                restore_selection(previous_selection, written_selection)
                raise
    return name


def select(name):
    with locked():
        require_manual()
        _, config = read_config()
        if not config.has_section(name):
            raise Refused('This connection no longer exists.')
        atomic(ACTIVE, (name + '\n').encode())


def remove(name):
    with locked():
        require_manual()
        original, config = read_config()
        if not config.has_section(name):
            raise Refused('This connection no longer exists.')
        # Removing a wrapper's underlying connection would break the wrapper.
        for other in config.sections():
            if other != name and any(re.search(r'(?<![\w.-])' + re.escape(name) + ':', v) for _, v in config.items(other)):
                raise Refused('Another connection uses this one. Change that connection first.')
        selected = active(config)
        with tempfile.TemporaryDirectory(prefix='.connection-', dir=CONFIG.parent) as directory:
            staged = Path(directory) / 'rclone.conf'
            staged.write_bytes(original)
            staged.chmod(0o600)
            run(['--config', str(staged), 'config', 'delete', name])
            updated, result = read_config(staged)
            if result.has_section(name):
                raise Refused('The connection settings could not be changed safely.')
        if CONFIG.read_bytes() != original:
            raise Refused('Cloud settings changed. Open this page again.')
        # Empty selection is a tombstone: never silently use another account.
        previous_selection = ACTIVE.read_bytes() if ACTIVE.exists() else None
        written_selection = (('' if selected == name else selected) + '\n').encode()
        try:
            atomic(ACTIVE, written_selection)
            atomic(CONFIG, updated)
        except Exception:
            if CONFIG.exists() and CONFIG.read_bytes() == updated:
                atomic(CONFIG, original)
            restore_selection(previous_selection, written_selection)
            raise
