"""Keep one owned test unit loaded so systemd retains original exit properties."""
import ctypes
import hashlib
import json
from pathlib import Path


class UnitReference:
    def __init__(self, unit, expected_sha):
        self.bus = ctypes.c_void_p()
        path = Path('/usr/lib/libsystemd.so.0.38.0')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected_sha:
            raise RuntimeError('installed libsystemd differs from immutable VM20 binding')
        self.lib = ctypes.CDLL(str(path))
        self.lib.sd_bus_open_system.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.lib.sd_bus_open_system.restype = ctypes.c_int
        self.lib.sd_bus_set_method_call_timeout.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
        self.lib.sd_bus_set_method_call_timeout.restype = ctypes.c_int
        self.lib.sd_bus_call_method.argtypes = [ctypes.c_void_p] + [ctypes.c_char_p] * 4 + [ctypes.c_void_p] * 2 + [ctypes.c_char_p]
        self.lib.sd_bus_call_method.restype = ctypes.c_int
        self.lib.sd_bus_flush_close_unref.argtypes = [ctypes.c_void_p]
        self.lib.sd_bus_flush_close_unref.restype = ctypes.c_void_p
        self.record = {'unit': unit, 'library': str(path), 'sha256': digest, 'calls': [], 'closed': False,
                       'scope': 'guest system AF_UNIX bus only; no product behavior/timer changes'}
        self.unit = unit.encode('ascii')
        try:
            self.check('sd_bus_open_system', self.lib.sd_bus_open_system(ctypes.byref(self.bus)))
            self.check('sd_bus_set_method_call_timeout', self.lib.sd_bus_set_method_call_timeout(self.bus, 5000000))
            self.call('RefUnit')
        except BaseException:
            self.close()
            raise

    def check(self, operation, result):
        self.record['calls'].append({'operation': operation, 'original_result': result})
        if result < 0:
            raise OSError(-result, operation)

    def call(self, name):
        self.check(name, self.lib.sd_bus_call_method(self.bus, b'org.freedesktop.systemd1',
                   b'/org/freedesktop/systemd1', b'org.freedesktop.systemd1.Manager', name.encode('ascii'),
                   None, None, b's', ctypes.c_char_p(self.unit)))

    def close(self):
        if self.bus.value:
            self.lib.sd_bus_flush_close_unref(self.bus)
            self.bus = ctypes.c_void_p()
        self.record['closed'] = True
