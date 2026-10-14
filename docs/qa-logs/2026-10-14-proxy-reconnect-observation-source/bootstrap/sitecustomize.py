"""UNRUN boundary/observer. The unit still execs python3 -m raofflineproxy.main run-service."""
import atexit
import ctypes.util
import encodings.ascii
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import threading
import time


def install():
    if sys.flags.optimize != 0:
        raise RuntimeError('fixture assertions must remain enabled')
    packet = Path('/run/pix583-service-packet')
    prepared = Path('/run/pix583-service-inputs/prepared')
    state = Path('/storage/.config/raofflineproxy')
    binding = json.loads((packet / 'bindings.json').read_text())
    assert os.environ['RAOFFLINEPROXY_CONFIG_DIR'] == str(state)
    s = Path('/storage').stat()
    assert f'{s.st_dev}:{s.st_ino}' == os.environ['PIX583_STORAGE_ID'], 'synthetic storage bind missing'
    assert set(p.name for p in Path('/sys/class/net').iterdir()) == {'lo'}, 'no-NIC guest required'
    assert os.environ.get('DEVICE_HAS_DUAL_SCREEN') == 'false'
    assert not any(k.lower().endswith('_proxy') or k.startswith('LISTEN_') for k in os.environ)
    source = prepared / 'tree'
    for name, digest in binding['prepared_python_manifest'].items():
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == digest, name
    assert not list(source.rglob('*.pyc')), 'unbound bytecode'
    libraries = binding['libraries']
    for row in libraries.values():
        p = Path(row['path']).resolve(strict=True)
        assert str(p) == row['resolved_path']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']

    class Denied(BaseException):
        pass

    allowed_read = (Path('/storage'), packet, prepared, Path(sys.base_prefix) / 'lib', Path('/etc/ssl'))
    public = {str(Path(p).resolve()) for p in ('/etc/os-release', '/proc/self/stat', '/proc/self/maps', '/proc/net/route', '/proc/net/tcp')}
    native = {v[k] for v in libraries.values() for k in ('path', 'resolved_path', 'soname')}

    def audit(event, args):
        if event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.exec', 'os.fork',
                     'socket.sendto', 'socket.gethostbyname', 'socket.gethostbyaddr'):
            raise Denied(event)
        if event == 'socket.getaddrinfo' and (args[0] != '127.0.0.1' or args[1] not in (None, 8080, 18081)):
            raise Denied('external resolution')
        if event == 'socket.__new__' and args[1:3] != (socket.AF_INET, socket.SOCK_STREAM):
            raise Denied('socket family/type')
        if event in ('socket.bind', 'socket.connect') and args[1] not in (('127.0.0.1', 8080), ('127.0.0.1', 18081)):
            raise Denied('external endpoint')
        if event == 'ctypes.dlopen' and args[0] not in native:
            raise Denied('unbound native library')
        if event == 'sqlite3.connect':
            path = Path(str(args[0]).removeprefix('file:').split('?', 1)[0]).resolve()
            if not path.is_relative_to(state):
                raise Denied('non-synthetic database')
        if event == 'open' and not isinstance(args[0], int):
            path = Path(os.fsdecode(args[0])).resolve()
            writing = args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)
            if writing and not path.is_relative_to('/storage'):
                raise Denied('write outside synthetic storage: ' + str(path))
            if not writing and not (str(path) in public or str(path) in native or
                                    any(path.is_relative_to(p.resolve()) for p in allowed_read)):
                raise Denied('read outside fixture/runtime: ' + str(path))
        if event in ('os.remove', 'os.rmdir', 'os.mkdir', 'os.chmod'):
            if not Path(os.fsdecode(args[0])).resolve().is_relative_to('/storage'):
                raise Denied('mutation outside synthetic storage')
        if event in ('os.rename', 'os.replace'):
            if not all(Path(os.fsdecode(p)).resolve().is_relative_to('/storage') for p in args[:2]):
                raise Denied('rename outside synthetic storage')

    sys.addaudithook(audit)
    for event, args in [('socket.connect', (None, ('192.0.2.1', 443))),
                        ('socket.getaddrinfo', ('provider.invalid', 443, 0, 0, 0)),
                        ('sqlite3.connect', ('/tmp/forbidden.sqlite',)),
                        ('open', ('/etc/forbidden', 'w', os.O_WRONLY)),
                        ('open', ('/root/forbidden', 'r', 0)),
                        ('subprocess.Popen', ('false', [], None, None))]:
        try:
            sys.audit(event, *args)
        except Denied:
            continue
        raise AssertionError('guard negative failed: ' + event)

    lookup = {'raproxy_rchash': libraries['rchash']['path'], 'zstd': libraries['zstd']['path'],
              'crypto': libraries['crypto']['path']}

    def find_library(name):
        if name not in lookup:
            raise Denied('unbound native lookup: ' + name)
        return lookup[name]

    ctypes.util.find_library = find_library
    # Same explicit no-NIC/loopback substitution as the accepted native fixture.
    # Reachability probes, HTTP, timers, worker bodies and service signals remain real.
    from raofflineproxy import network
    network.has_active_network_interface = lambda: True
    target = state / ('observer-' + str(os.getpid()) + '.jsonl')
    lock = threading.Lock()
    count = 0

    def emit(kind, **fields):
        nonlocal count
        with lock:
            count += 1
            assert count <= 1024, 'observer record bound'
            row = {'kind': kind, 'pid': os.getpid(), 'tid': threading.get_native_id(),
                   'monotonic': time.monotonic(), **fields}
            raw = (json.dumps(row, sort_keys=True) + '\n').encode()
            assert len(raw) <= 16384
            with target.open('ab', buffering=0) as stream:
                assert stream.write(raw) == len(raw)

    watched = {'main', 'run_service_foreground', 'run_proxy_service', 'run', 'stop',
               'process_once', 'run_pass', 'stop_workers', 'close', 'flush_pending_awards', 'report_if_due', 'refresh_reachability'}
    worker_names = {'ConnectivityMonitor', 'PeriodicRefresh', 'CacheQueueWorker', 'FolderWatcher', 'UsageReporter'}

    def profile(frame, event, arg):
        if event not in ('call', 'return') or frame.f_code.co_name not in watched:
            return
        filename = frame.f_code.co_filename
        if not filename.startswith(str(source / 'linux/raofflineproxy') + '/'):
            return
        obj = frame.f_locals.get('self')
        cls = type(obj).__name__ if obj is not None else None
        name = frame.f_code.co_name
        if name in ('run', 'stop', 'process_once', 'run_pass') and cls not in worker_names:
            return
        if name == 'close' and cls != 'Storage':
            return
        fields = {'event': event, 'function': name, 'class': cls,
                  'source': filename.removeprefix(str(source) + '/'), 'thread': threading.current_thread().name}
        if name == 'run' and event == 'call':
            fields['timings'] = {key: getattr(obj, key) for key in
                                 ('interval_seconds', 'poll_seconds', 'initial_delay_seconds') if hasattr(obj, key)}
        if name == 'stop_workers' and event == 'return':
            fields['alive'] = {type(w).__name__: w.is_alive() for w in frame.f_locals['workers']}
        if name in ('process_once', 'report_if_due', 'refresh_reachability') and event == 'return':
            fields['result'] = str(arg)[:512]
        emit('trace', **fields)

    original_hook = threading.excepthook

    def thread_error(args):
        emit('thread-error', error=args.exc_type.__name__ + ': ' + str(args.exc_value))
        original_hook(args)

    threading.excepthook = thread_error
    sys.setprofile(profile)
    threading.setprofile(profile)
    emit('guard-ready', source_pins_verified=False, storage_identity=[s.st_dev, s.st_ino],
         argv=sys.argv, interpreter=sys.version, executable=sys.executable,
         substitutions=['installed-library-discovery', 'loopback-interface-only'], worker_timers_changed=False)
    atexit.register(lambda: emit('python-exit', threads=[t.name for t in threading.enumerate() if t is not threading.main_thread()]))


try:
    install()
except BaseException as error:
    # Python normally swallows Exception from sitecustomize. Refuse startup instead.
    os.write(2, ('pix583 boundary refused: ' + repr(error) + '\n').encode())
    os._exit(126)
