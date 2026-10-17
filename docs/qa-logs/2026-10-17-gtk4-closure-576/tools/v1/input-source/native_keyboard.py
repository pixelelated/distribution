# SPDX-License-Identifier: GPL-2.0-only
# Derived from pixelelated cloud_oauth; original ROCKNIX credits retained.
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
import os, fcntl, struct, time
UINPUT = "/dev/uinput"
def log(message):
    print("native keyboard status event", flush=True)

EV_SYN, EV_KEY = 0x00, 0x01
SYN_REPORT = 0
UI_SET_EVBIT, UI_SET_KEYBIT = 0x40045564, 0x40045565
UI_SET_RELBIT = 0x40045566
EV_REL = 0x02
REL_X, REL_Y, REL_WHEEL = 0x00, 0x01, 0x08
BTN_LEFT = 0x110
# vendor:product:name, as sway forms it -- 0x1209/0x0002 and the device name
# with spaces turned into underscores.
POINTER_ID = "4617:2:ROCKNIX_cloud_pointer"
UI_DEV_CREATE, UI_DEV_DESTROY = 0x5501, 0x5502

# US layout, which is what the on-screen keyboard and the browser both assume.
# Only what a sign-in needs: an address, a password, and the keys to correct
# and submit them.
KEYMAP = {}
for _i, _c in enumerate("abcdefghijklmnopqrstuvwxyz"):
    KEYMAP[_c] = ((30, 48, 46, 32, 18, 33, 34, 35, 23, 36, 37, 38, 50,
                   49, 24, 25, 16, 19, 31, 20, 22, 47, 17, 45, 21, 44)[_i], False)
for _i, _c in enumerate("1234567890"):
    KEYMAP[_c] = (2 + _i, False)
KEYMAP.update({
    " ": (57, False), "-": (12, False), "=": (13, False), "[": (26, False),
    "]": (27, False), "\\": (43, False), ";": (39, False), "'": (40, False),
    "`": (41, False), ",": (51, False), ".": (52, False), "/": (53, False),
})
for _plain, _shifted in zip("1234567890-=[]\\;',./`", '!@#$%^&*()_+{}|:"<>?~'):
    KEYMAP[_shifted] = (KEYMAP[_plain][0], True)
for _c in "abcdefghijklmnopqrstuvwxyz":
    KEYMAP[_c.upper()] = (KEYMAP[_c][0], True)

NAMED_KEYS = {"enter": 28, "backspace": 14, "tab": 15, "escape": 1,
              "left": 105, "right": 106, "up": 103, "down": 108,
              "home": 102, "end": 107, "delete": 111,
              "pageup": 104, "pagedown": 109,
              "f1": 59, "f2": 60, "f3": 61, "f4": 62}
KEY_LEFTSHIFT = 42

# How long a key is held, and the gap before the next one. Roughly 130 words
# per minute -- faster than anyone types, slow enough that a page's own input
# handling sees each keystroke as a separate event.
KEY_HOLD = 0.012
KEY_GAP = 0.022


class RemoteKeyboard:
    """A keyboard the phone can type on, for the window on the handheld.

    The player reads the provider's page on the device's own screen and types
    on the keyboard they already know how to use. Nothing is mirrored, so the
    only thing crossing the network is a keystroke -- which is why this
    replaced streaming the display.

    uinput rather than the Wayland virtual-keyboard protocol: it needs no
    Wayland client of our own, and sway picks the device up through libinput
    exactly as it would a keyboard someone plugged in.
    """

    def __init__(self):
        self.fd = None

    def open(self):
        if self.fd is not None:
            return True
        try:
            fd = os.open(UINPUT, os.O_WRONLY | os.O_NONBLOCK)
        except OSError as exc:
            log("no virtual keyboard: %s" % exc)
            return False
        try:
            fcntl.ioctl(fd, UI_SET_EVBIT, EV_KEY)
            fcntl.ioctl(fd, UI_SET_EVBIT, EV_SYN)
            for code in set(list(NAMED_KEYS.values())
                            + [c for c, _ in KEYMAP.values()] + [KEY_LEFTSHIFT]):
                fcntl.ioctl(fd, UI_SET_KEYBIT, code)
            # struct uinput_user_dev: name[80], id{bustype,vendor,product,
            # version}, ff_effects_max, then the absmin/max/fuzz/flat arrays.
            name = b"pixelelated cloud sign-in".ljust(80, b"\0")
            os.write(fd, name + struct.pack("HHHHi", 0x03, 0x1209, 0x0001, 1, 0)
                     + b"\0" * (4 * 64 * 4))
            fcntl.ioctl(fd, UI_DEV_CREATE)
        except OSError as exc:
            log("could not create the virtual keyboard: %s" % exc)
            os.close(fd)
            return False
        # udev and libinput need a moment to notice a new device.
        time.sleep(0.5)
        self.fd = fd
        log("virtual keyboard ready")
        return True

    def _emit(self, etype, code, value):
        now = time.time()
        os.write(self.fd, struct.pack("llHHi", int(now),
                                      int((now % 1) * 1000000), etype, code, value))

    def _tap(self, code, shift=False):
        """One keypress, reported the way a real keyboard reports it.

        Each state change is its own SYN_REPORT, and press and release are
        separated in time. Sending press and release in a single report, with
        zero timestamps, is not what any hardware does: libinput and the
        page's own input handling both read it as one indivisible blur, and a
        typed address arrived truncated -- six characters of sixteen. The
        delays below are what a fast typist produces, and cost nothing that
        matters when the whole point is to save somebody a minute on a d-pad.
        """
        if shift:
            self._emit(EV_KEY, KEY_LEFTSHIFT, 1)
            self._emit(EV_SYN, SYN_REPORT, 0)
            time.sleep(KEY_GAP)
        self._emit(EV_KEY, code, 1)
        self._emit(EV_SYN, SYN_REPORT, 0)
        time.sleep(KEY_HOLD)
        self._emit(EV_KEY, code, 0)
        self._emit(EV_SYN, SYN_REPORT, 0)
        if shift:
            time.sleep(KEY_GAP)
            self._emit(EV_KEY, KEY_LEFTSHIFT, 0)
            self._emit(EV_SYN, SYN_REPORT, 0)

    def type_text(self, text):
        """Send printable characters. Returns how many were sent."""
        if not self.open():
            return 0
        sent = 0
        for char in text:
            entry = KEYMAP.get(char)
            if entry is None:
                continue        # not on a US layout; silently skipped
            self._tap(*entry)
            time.sleep(KEY_GAP)
            sent += 1
        return sent

    def press(self, name):
        code = NAMED_KEYS.get(name)
        if code is None or not self.open():
            return False
        self._tap(code)
        return True

    def close(self):
        if self.fd is None:
            return
        try:
            fcntl.ioctl(self.fd, UI_DEV_DESTROY)
        except OSError:
            pass
        os.close(self.fd)
        self.fd = None
