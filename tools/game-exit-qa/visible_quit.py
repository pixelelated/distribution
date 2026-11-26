"""PB's frame-bound approval and original save checks for the one ordinary #1433 exit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import struct
import time
import zlib

# The existing operator CLI runs with -I. Use its own frozen code directory.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import menu_timing as T

ROUTE = {
    "game": {"game": ("f1", "layout")},
    "layout": {"quick-menu-resume": ("backspace", "main"), "main-first": ("up", "quit"),
               "quit-highlighted": ("ret", "confirmation")},
    "main": {"main-first": ("up", "quit"), "quit-highlighted": ("ret", "confirmation")},
    "quit": {"quit-highlighted": ("ret", "confirmation")},
    "confirmation": {"quit-confirmation": ("ret", "finished")},
}
IDENTITY = ("boot_id", "attempt", "pid", "start_ticks")
EXPECTED = {"bytes": 8192, "sha256": "7ed86290f40c659086adb6003b521e17291745626c2f3f89a949e7c042f605db"}
SAVE = "gb/ExitProbe.srm"
CURRENT = "m7-1433/Saves/" + SAVE


def require(test, reason):
    if not test:
        raise ValueError(reason)


def original(path, limit):
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_size <= limit, "nonregular or oversized original")
        raw = stream.read(limit+1)
        after = os.fstat(stream.fileno())
    key = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    require(len(raw) == before.st_size and key(before) == key(after) == key(path.lstat()), "file changed during read")
    return raw


def document(path, limit=128*1024):
    return json.loads(original(path, limit))


def digest(path, limit):
    raw = original(path, limit)
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def frame(path):
    raw = original(path, 8*1024**2)
    require(raw.startswith(b"\x89PNG\r\n\x1a\n"), "visual tool returned no PNG")
    return hashlib.sha256(raw).hexdigest()


# Only the measured 640x480 Dark Ozone Resume footprint. The bright
# and dark references are RGB at bottom green 230 and 145 in owner14.
RESUME_RUNS = (
    (22, 27, 28, (39,96,124), (86,138,142)),
    *((y, 27, 28, (40,97,125), (87,139,143)) for y in range(23,33)),
    *((y, 612, 613, (37,93,121), (83,136,139)) for y in range(22,33)),
    (33, 27, 28, (48,62,68), (59,72,73)),
    (33, 612, 613, (46,59,65), (56,69,69)),
)
SCANLINE = 1 + 640*3
PNG = b"\x89PNG\r\n\x1a\n"


def resume_raster(raw):
    """Decode only the pinned visual tool's bounded stdlib RGB8 output."""
    require(raw.startswith(PNG), "not a PNG frame")
    cursor = len(PNG)
    chunks = {}
    for expected in (b"IHDR", b"IDAT", b"IEND"):
        require(cursor+12 <= len(raw), "truncated PNG frame")
        count, kind = struct.unpack_from(">I4s", raw, cursor)
        start = cursor + 8
        end = start + count
        require(kind == expected and end+4 <= len(raw), "unsupported PNG frame encoding")
        body = raw[start:end]
        require(zlib.crc32(kind+body) == struct.unpack_from(">I",raw,end)[0], "PNG frame CRC mismatch")
        chunks[kind] = body
        cursor = end + 4
    require(cursor == len(raw) and chunks[b"IEND"] == b"" and
            chunks[b"IHDR"] == struct.pack(">IIBBBBB",640,480,8,2,0,0,0), "unsupported Resume scanout")
    decompressor = zlib.decompressobj()
    try:
        pixels = decompressor.decompress(chunks[b"IDAT"],SCANLINE*480+1)
    except zlib.error as error:
        raise ValueError("invalid compressed PNG frame") from error
    require(len(pixels) == SCANLINE*480 and decompressor.eof and not decompressor.unused_data and
            pixels[::SCANLINE] == bytes(480), "unsupported Resume raster")
    return bytearray(pixels)


def remove_resume_outline(raw):
    pixels = resume_raster(raw)
    start = 33*SCANLINE + 1 + 28*3
    stop = 33*SCANLINE + 1 + 612*3
    center = pixels[start:start+3]
    green = center[1]

    def palette(rgb, lo, hi, low_green, high_green):
        span = high_green-low_green
        # Two RGB levels allow rounding of the theme gradient and texture blend.
        return all(abs(c*span-(a*span+(green-low_green)*(b-a))) <= 2*span
                   for c,a,b in zip(rgb,lo,hi))

    require(138 <= green <= 241 and palette(center,(25,138,198),(137,241,242),138,241) and
            pixels[start:stop] == center*584, "unknown or nonuniform Resume outline")
    for y,x0,x1,lo,hi in RESUME_RUNS:
        first, last = y*SCANLINE+1+x0*3, y*SCANLINE+1+x1*3
        require(palette(pixels[first:last],lo,hi,145,230), "unknown Resume outline shading")
        pixels[first:last] = bytes(last-first)
    pixels[start:stop] = bytes(stop-start)
    return pixels


# Measured geometry and SHA-256 of the actual 640x480 selected Main Menu.
MAIN_LABELS = ((7,90,3,16), (0,86,22,33), (100,230,23,32), (98,145,155,166))
MAIN_SIGNATURE = "c0051ae1a26de763efe38598ab60d52d8960092f07e88844e8d41ae97a9d44dd"
# Identical header/list geometry, with the actual last-row label and selection.
QUIT_LABELS = (*MAIN_LABELS[:3], (99,145,156,165))
QUIT_SIGNATURE = "3147cf78ea5fc1ba820fa2be1fd1422554e6d4cf393172937757a86296dd8e05"
QUIT_ROW_OFFSET = 133
MAIN_RUNS = (
    (22,95,(55,111,137),50),
    *((y,95,(56,112,138),50) for y in range(23,33)),
    *((y,632,(41,96,123),50) for y in range(22,33)),
    (33,95,(68,81,88),12),
    (33,632,(47,60,66),12),
)
CLOCK = (577,626,5,12)
MODAL_CENTER = (200,440,215,265)
# Last measured ordinary review was 14.2 s. Allow 5.8 s extra for two
# images, plus arrival, a fresh guard and key submission under the age cap.
RECHECK_REVIEW = 20
RECHECK_AGE = 32
NEEDS_REVIEW = "needs-paired-review"


def row_span(x0, x1, y):
    start = y*SCANLINE+1
    return slice(start+x0*3,start+x1*3)


def patch_bytes(pixels, box):
    x0,x1,y0,y1 = box
    return b"".join(pixels[row_span(x0,x1,y)] for y in range(y0,y1))


def main_outline(raw, *, selected_quit=False):
    pixels = resume_raster(raw)
    boxes, signature = (QUIT_LABELS,QUIT_SIGNATURE) if selected_quit else (MAIN_LABELS,MAIN_SIGNATURE)
    row_offset = QUIT_ROW_OFFSET if selected_quit else 0
    labels = b"".join(patch_bytes(pixels,box) for box in boxes)
    require(hashlib.sha256(labels).hexdigest() == signature,
            "Main Menu, Quick Menu or Quit label/selection changed")
    bottom = row_span(96,632,33+row_offset)
    center = pixels[bottom.start:bottom.start+3]
    green = center[1]

    def color_matches(rgb, lo, hi, low_green, high_green):
        span = high_green-low_green
        return all(abs(c*span-(a*span+(green-low_green)*(b-a))) <= 2*span
                   for c,a,b in zip(rgb,lo,hi))

    require(138 <= green <= 241 and color_matches(center,(25,138,198),(137,241,242),138,241)
            and pixels[bottom] == center*536, "Main Menu focus outline moved or is unsupported")
    # The same texture modulates the center and its composited edge. The
    # installed Main and Quit pairs share the side/corner alpha model.
    for y,x,base,alpha in MAIN_RUNS:
        span = row_span(x,x+1,y+row_offset)
        observed = pixels[span]
        require(all(abs(p*100-anchor*100-alpha*(stroke-ref)) <= 200
                    for p,anchor,stroke,ref in zip(observed,base,center,(40,151,204))),
                "unknown Main Menu outline shade")
        pixels[span] = bytes(3)
    pixels[bottom] = bytes(536*3)
    return pixels


# The dimmed Quit selection behind the native dialog uses the same 560
# outline pixels as the selected row. Validate the bottom palette and the
# composited side/corner texture before removing any of those pixels.
MODAL_RUNS = (
    (155, 95, (19,33,36), 50),
    *((y,95,(19,33,37),50) for y in range(156,166)),
    *((y,632,(15,29,33),50) for y in range(155,166)),
    (166,95,(18,22,23),12),
    (166,632,(13,16,17),12),
)


def remove_modal_outline(pixels):
    bottom = row_span(96,632,166)
    center = pixels[bottom.start:bottom.start+3]
    red,green,blue = center
    require(44 <= green <= 65 and abs(red-(20+green-47)) <= 2 and
            abs(2*(blue-55)-(green-47)) <= 4 and pixels[bottom] == center*536,
            "unknown or nonuniform dimmed Quit outline")
    for y,x,base,alpha in MODAL_RUNS:
        span = row_span(x,x+1,y)
        require(all(abs(p*100-anchor*100-alpha*(stroke-ref)) <= 200
                    for p,anchor,stroke,ref in zip(pixels[span],base,center,(20,47,55))),
                "unknown dimmed Quit outline shading")
    for y,x,_,_ in MODAL_RUNS:
        pixels[row_span(x,x+1,y)] = bytes(3)
    pixels[bottom] = bytes(536*3)
    return pixels


def without_clock(pixels):
    x0,x1,y0,y1 = CLOCK
    for y in range(y0,y1):
        pixels[row_span(x0,x1,y)] = bytes((x1-x0)*3)
    return pixels


def decoration_comparison(before, after, label):
    clock_changed = patch_bytes(before,CLOCK) != patch_bytes(after,CLOCK)
    if without_clock(before) != without_clock(after):
        return NEEDS_REVIEW
    return label+"-clock-masked" if clock_changed else label


def compare_frames(preview, confirmed, approved, phase, view):
    preview_raw = original(preview,8*1024**2)
    current_raw = original(confirmed,8*1024**2)
    require(preview_raw.startswith(PNG) and current_raw.startswith(PNG), "visual tool returned no PNG")
    expected = hashlib.sha256(preview_raw).hexdigest()
    current = hashlib.sha256(current_raw).hexdigest()
    require(expected == approved, "approved preview changed on disk")
    if view in {"main-first","quit-highlighted"}:
        selected_quit = view == "quit-highlighted"
        require(not selected_quit or phase in {"layout","main","quit"}, "Quit row is not a confirmation")
    a,b = (resume_raster(raw) for raw in (preview_raw,current_raw))
    same_raster = a == b
    if same_raster or without_clock(a.copy()) == without_clock(b.copy()):
        if view in {"main-first","quit-highlighted"}:
            try:
                main_outline(current_raw,selected_quit=view == "quit-highlighted")
            except ValueError:
                return current,NEEDS_REVIEW
        if same_raster:
            return current,"exact-png" if expected == current else "exact-raster"
        return current,"clock-masked"
    try:
        if view in {"main-first","quit-highlighted"}:
            a,b = (main_outline(raw,selected_quit=view == "quit-highlighted")
                   for raw in (preview_raw,current_raw))
        elif view == "quick-menu-resume":
            a,b = (remove_resume_outline(raw) for raw in (preview_raw,current_raw))
        elif view == "quit-confirmation":
            a,b = (remove_modal_outline(p) for p in (a,b))
        else:
            return current,NEEDS_REVIEW
    except ValueError:
        # An unrecognized pulse or layout cannot be treated as decoration.
        return current,NEEDS_REVIEW
    return current,decoration_comparison(a,b,"ozone-"+view+"-outline")


def modal_appeared(baseline, baseline_hash, capture):
    raw = original(baseline,8*1024**2)
    require(hashlib.sha256(raw).hexdigest() == baseline_hash, "prior Quit frame changed")
    # Ozone positions the native message box at the display centre.
    require(patch_bytes(resume_raster(raw),MODAL_CENTER) !=
            patch_bytes(resume_raster(original(capture,8*1024**2)),MODAL_CENTER),
            "native confirmation has no visible central change from the selected Quit frame")


# The previous timing plan already budgets two seconds for the first
# post-key guard and two for its preview. A six-second observation adds
# at most four seconds for each of the four navigation actions.
TRANSITION_OFFSETS = (0,3,5)
TRANSITION_WINDOW = 6
POST_KEY_GUARD = 2
TRANSITION_CUTOFF = POST_KEY_GUARD + TRANSITION_WINDOW
REQUIRED_START = (T.MAX_KEYS*T.PER_ACTION + (T.MAX_KEYS-1)*(TRANSITION_WINDOW-T.SHOT) + T.RETIRE_MARGIN)


def still_before_action(baseline, current, view):
    if baseline == current or resume_raster(baseline) == resume_raster(current):
        return True
    if view == "quit-highlighted":
        # A header/outline change alone is not a visible native confirmation.
        a,b = (resume_raster(raw) for raw in (baseline,current))
        return patch_bytes(a,MODAL_CENTER) == patch_bytes(b,MODAL_CENTER)
    try:
        if view == "quick-menu-resume":
            a,b = (remove_resume_outline(raw) for raw in (baseline,current))
            return decoration_comparison(a,b,"before-resume") != NEEDS_REVIEW
        if view == "main-first":
            # Still the selected Quick Menu row even if its clock changed.
            main_outline(current)
            return True
    except ValueError:
        # A changed frame is only a candidate for the existing human review.
        pass
    return False


def publish(path, row, before_link=None):
    temporary = path.with_name(path.name+f".{os.getpid()}.new")
    try:
        with temporary.open("x") as stream:
            json.dump(row, stream, indent=2)
            stream.write("\n")
        try:
            if before_link is not None:
                before_link()
            os.link(temporary, path)
        finally:
            temporary.unlink()
    except FileExistsError as error:
        raise ValueError("receipt already occupied") from error


def host_clock_domain():
    return {"boot_id":Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
            "time_namespace":os.readlink("/proc/self/ns/time")}


def submit_approval(path, view, clock=time.monotonic_ns, clock_domain=host_clock_domain):
    match = re.fullmatch(r"1433-menu-(0[1-5])-(request|recheck)\.json", path.name)
    require(match and path.parent.name == "records" and path.resolve(strict=True) == path,
            "select a new PB owner's bound request")
    owner = path.parent.parent
    request = document(path,8192)
    expires = request["approval_expires_host_ns"]
    issued = request["issued_host_ns"]
    require(request["host_clock"] == clock_domain() and type(issued) is int and type(expires) is int and
            0 < expires-issued <= (RECHECK_REVIEW if match[2] == "recheck" else T.REVIEW)*T.NS, "unbound approval clock or review interval")

    def permitted():
        now = clock()
        require(not (owner/"worker-result.json").exists() and
                not (path.parent/"1433-armed.serial.json").exists(), "armed foreground already returned")
        require(issued <= now < expires, "approval deadline expired")
        return now

    permitted()
    require(request["step"] == int(match[1]) and view in request["views"], "invalid view for the active step")
    paired = match[2] == "recheck"
    stem = f"1433-menu-{match[1]}"
    suffix = "confirmed" if paired else "preview"
    require(request["png"] == f"{stem}-{suffix}.png", "unexpected request frame operand")
    require(frame(owner/"frames"/request["png"]) == request["png_sha256"], "reviewed frame changed")
    if paired:
        require(request["preview_png"] == f"{stem}-preview.png" and
                frame(owner/"frames"/request["preview_png"]) == request["preview_png_sha256"],
                "original reviewed frame changed")
    submitted = permitted()
    result = "reapproval" if paired else "approval"
    publish(path.with_name(f"{stem}-{result}.json"),
            {**request, "view":view, "submitted_host_ns":submitted}, before_link=permitted)


class VisibleQuit:
    def __init__(self, ctx, qemu, owner, visual, ready, receipt, now=time.monotonic_ns, clock_domain=host_clock_domain):
        self.ctx, self.qemu, self.owner, self.visual, self.receipt = ctx, qemu, owner, visual, receipt
        self.clock = now
        self.host_clock = clock_domain()
        self.identity = {"boot_id": ready["boot_id"], "attempt": ready["attempt"],
                         "pid": ready["emulator"], "start_ticks": ready["start_ticks"]}
        self.state = "game"
        self.current = self.confirmation = self.recheck = self.quit_baseline = None
        self.transition = None
        self.latest = None
        self.sequence = self.sample_ns = self.after_ns = 0
        self.menu_until = None
        self.best_offset = None
        self.receipt["menu_commands"] = []
        self.receipt["menu_transitions"] = []
        self.receipt["input_route"] = "reviewed ordinary Ozone menu Quit"

    def refuse(self, error):
        if self.state not in {"finished", "refused"}:
            if self.transition is not None:
                pending = self.transition
                pending["reason"] = str(error)[:240]
                try:
                    self.finish_transition(pending.get("verdict","TRANSITION_REFUSED"))
                except (OSError,ValueError) as record_error:
                    pending["record_error"] = str(record_error)[:240]
            self.state = "refused"
            self.receipt["menu_refusal"] = str(error)[:240]

    def accept(self, row, received):
        if self.state in {"finished", "refused"}:
            return
        try:
            require(row["schema"] == "m7-1433-menu-guard-v1" and
                    all(row[k] == self.identity[k] for k in IDENTITY), "wrong menu guard identity")
            require(type(row["sequence"]) is int and row["sequence"] > self.sequence and
                    type(row["sample_ns"]) is int and row["sample_ns"] > self.sample_ns and
                    type(row["remaining_ms"]) is int, "stale or invalid menu guard")
            expires = row["menu_until_ns"]
            require(type(expires) is int and
                    (self.menu_until is None or expires == self.menu_until) and
                    row["remaining_ms"] == (expires-row["sample_ns"])//1_000_000 and
                    0 < row["remaining_ms"] <= T.MENU*1000, "unbound or expired guest menu window")
            self.menu_until = expires
            self.sequence, self.sample_ns = row["sequence"], row["sample_ns"]
            offset = received-self.sample_ns
            self.best_offset = offset if self.best_offset is None else min(offset, self.best_offset)
            age = offset-self.best_offset
            self.latest = None
            if row["state"] == "WAIT_SAVE" and self.state == "game" and self.current is None:
                return
            require(row["state"] == "READY", row.get("error", "fresh save or focus refused"))
            require(row["expected"] == EXPECTED and all(row["save"][k] == v for k,v in EXPECTED.items()),
                    "expected cartridge bytes absent")
            focus = row["focus"]
            require(focus["status"] == "SAMPLED" and
                    [n["pid"] for n in focus["focused"] if type(n["pid"]) is int and n["pid"] > 1]
                    == [self.identity["pid"]], "same RetroArch is not exclusively focused")
            if self.sample_ns+self.best_offset > self.after_ns and age <= 1_000_000_000:
                self.latest = (row, self.sample_ns+self.best_offset)
        except (ValueError, KeyError, TypeError) as error:
            self.refuse(error)

    def budget(self, seconds):
        row, at = self.latest
        age = self.clock()-at
        return (age <= 4*T.NS and row["remaining_ms"]*1_000_000-age >= seconds*T.NS
                and self.qemu.poll() is None)

    def check_confirmation_frame(self, path):
        if self.state == "confirmation":
            require(self.quit_baseline is not None, "no previously approved selected Quit frame")
            baseline, expected = self.quit_baseline
            modal_appeared(baseline,expected,path)

    def approval(self,path,expected):
        expires = expected["approval_expires_host_ns"]
        require(self.clock() < expires+T.APPROVAL_ARRIVAL*T.NS, "approval deadline expired")
        if not path.exists() and not path.is_symlink():
            return None
        registered = document(path,8192)
        view = registered.pop("view")
        submitted = registered.pop("submitted_host_ns")
        require(type(submitted) is int and submitted <= self.clock() and
                expected["issued_host_ns"] <= submitted < expires,
                "approval submitted outside its exact review window")
        require(registered == expected and view in expected["views"],
                "unbound or ambiguous frame approval")
        require(view != "boundary", "operator refused an ambiguous view")
        return view,submitted

    def finish_transition(self,verdict):
        observation = self.transition
        observation["verdict"] = verdict
        publish(self.owner/"records"/observation["record"],observation)
        self.transition = None

    def observe_transition(self,name,preview):
        observation = self.transition
        now = self.clock()
        at = observation["key_completed_host_ns"]
        end = observation["cutoff_host_ns"]
        samples = observation["frames"]
        index = len(samples)
        if now < at + TRANSITION_OFFSETS[index]*T.NS:
            return False
        if now+T.SHOT*T.NS > end:
            observation["verdict"] = "TRANSITION_TIMEOUT"
            raise ValueError("passive transition window ended before a current product frame")
        # Keep enough guest time for the current preview's existing approval
        # and input fences. Observations make no additional key submissions.
        if not self.budget(T.SHOT+T.APPROVAL_RESERVE+T.APPROVAL_ARRIVAL):
            return False
        before_path = self.owner/"frames"/observation["before_png"]
        baseline = original(before_path,8*1024**2)
        require(hashlib.sha256(baseline).hexdigest()==observation["before_png_sha256"],
                "approved pre-action frame changed")
        capture = preview.with_name(f"{name}-transition-{index+1:02d}.png")
        require(not capture.exists() and not capture.is_symlink(),"transition frame path is already occupied")
        self.ctx.command(f"{name}-transition-{index+1:02d}",self.visual+["shot",str(capture)],T.SHOT)
        complete = self.clock()
        raw = original(capture,8*1024**2)
        same = still_before_action(baseline,raw,observation["from_view"])
        sha = hashlib.sha256(raw).hexdigest()
        guard = self.latest[0]
        samples.append({"png":capture.name,"sha256":sha,"started_host_ns":now,
                        "captured_host_ns":complete,"guest_guard_sequence":guard["sequence"],
                        "appearance":"PRE_ACTION_VIEW" if same else "CHANGED_FRAME_CANDIDATE"})
        if complete >= end:
            observation["verdict"] = "TRANSITION_TIMEOUT"
            raise ValueError("passive transition capture completed outside its window")
        if index == 0 or same:
            if index+1 >= len(TRANSITION_OFFSETS):
                observation["verdict"] = "TRANSITION_TIMEOUT"
                raise ValueError("pre-action view persisted through passive transition samples")
            self.after_ns = complete
            self.latest = None
            return False
        self.check_confirmation_frame(capture)
        with preview.open("xb") as output:
            output.write(raw)
        require(frame(preview)==sha, "current transition preview readback changed")
        observation.update(offered_png=preview.name,offered_sha256=sha)
        same_earlier = samples[0]["sha256"]==sha
        self.finish_transition("EARLIER_FRAME_FOR_REVIEW" if same_earlier else "LATER_FRAME_FOR_REVIEW")
        return True

    def step(self):
        if self.state not in ROUTE:
            return
        try:
            if self.transition is not None and self.clock()>=self.transition["cutoff_host_ns"]:
                self.transition["verdict"] = "TRANSITION_TIMEOUT"
                raise ValueError("no current supported transition before the passive deadline")
            if self.latest is None or not self.budget(T.KEY+T.RETIRE_MARGIN):
                return
            number = len(self.receipt["menu_commands"])+1
            require(number <= T.MAX_KEYS, "menu key cap")
            name = f"1433-menu-{number:02d}"
            records = self.owner/"records"
            if self.current is None:
                if number == 1:
                    require(self.budget(REQUIRED_START),
                            "initial readiness left no budget for all five reviews")
                if not self.budget(T.APPROVAL_RESERVE+T.APPROVAL_ARRIVAL+T.SHOT):
                    return
                preview = self.owner/"frames"/(name+"-preview.png")
                require(not preview.exists() and not preview.is_symlink(), "preview path is already occupied")
                if self.transition is None:
                    self.ctx.command(name+"-preview", self.visual+["shot", str(preview)], T.SHOT)
                    self.check_confirmation_frame(preview)
                elif not self.observe_transition(name,preview):
                    return
                row, at = self.latest
                issued = self.clock()
                expiry = T.approval_cutoff(issued,self.menu_until+self.best_offset)
                require(expiry > issued, "no remaining bounded review opportunity")
                request = {**self.identity, "phase":self.state, "step":number, "png":preview.name,
                           "png_sha256":frame(preview), "views":[*ROUTE[self.state], "boundary"],
                           "host_sample_ns":at, "guest_guard":row, "host_clock":self.host_clock,
                           "issued_host_ns":issued, "approval_expires_host_ns":expiry}
                if self.receipt["menu_transitions"]:
                    observed = self.receipt["menu_transitions"][-1]
                    require(observed["offered_png"]==preview.name and observed["offered_sha256"]==request["png_sha256"],
                            "visual request differs from its current passive observation")
                    request["transition_verdict"] = observed["verdict"]
                    request["transition_record"] = observed["record"]
                    request["transition_record_sha256"] = digest(records/observed["record"],8192)["sha256"]
                publish(records/(name+"-request.json"), request)
                self.current = request
                self.after_ns = self.clock()
                self.latest = None
                return
            expected = self.current
            if self.confirmation is None:
                checked = self.approval(records/(name+"-approval.json"),expected)
                if checked is None or not self.budget(T.APPROVAL_RESERVE):
                    return
                view, submitted = checked
                confirmed = self.owner/"frames"/(name+"-confirmed.png")
                require(not confirmed.exists() and not confirmed.is_symlink(), "confirmed frame path is already occupied")
                self.ctx.command(name+"-confirmed", self.visual+["shot", str(confirmed)], T.SHOT)
                captured = self.clock()
                self.check_confirmation_frame(confirmed)
                sha, comparison = compare_frames(confirmed.parent/expected["png"], confirmed,
                                                 expected["png_sha256"], self.state, view)
                self.confirmation = (view,confirmed.name,sha,comparison,submitted,captured)
                if comparison == NEEDS_REVIEW:
                    guest_end = self.menu_until+self.best_offset
                    reserve = (T.APPROVAL_ARRIVAL+T.GUARD_AFTER_FRAME+T.KEY+T.RETIRE_MARGIN)*T.NS
                    expiry = min(captured+RECHECK_REVIEW*T.NS, guest_end-reserve)
                    require(captured < expiry, "no remaining review time for the recapture")
                    review = {**expected,"png":confirmed.name,"png_sha256":sha,"preview_png":expected["png"],
                              "preview_png_sha256":expected["png_sha256"],"views":["same-"+view,"boundary"],
                              "issued_host_ns":captured,"approval_expires_host_ns":expiry}
                    publish(records/(name+"-recheck.json"),review)
                    self.recheck = (review,None)
                self.after_ns = captured
                self.latest = None
                return
            view, confirmed, confirmed_sha, comparison, submitted, captured = self.confirmation
            recheck_receipt = None
            if self.recheck is not None:
                review,recheck_receipt = self.recheck
                require(self.clock()<captured+RECHECK_AGE*T.NS, "current paired capture expired")
                if recheck_receipt is None:
                    checked = self.approval(records/(name+"-reapproval.json"),review)
                    if checked is None:
                        return
                    self.recheck = (review,checked)
                    self.after_ns = self.clock()
                    self.latest = None
                    return
                before_raw = original(self.owner/"frames"/expected["png"],8*1024**2)
                after_raw = original(self.owner/"frames"/confirmed,8*1024**2)
                if view in {"main-first","quit-highlighted"}:
                    main_outline(after_raw,selected_quit=view == "quit-highlighted")
                elif view == "quick-menu-resume":
                    remove_resume_outline(after_raw)
                elif view == "quit-confirmation":
                    require(patch_bytes(resume_raster(before_raw),MODAL_CENTER) ==
                            patch_bytes(resume_raster(after_raw),MODAL_CENTER),
                            "native confirmation centre changed between reviewed captures")
                comparison = "operator-reviewed-full-pair"
            if "transition_record" in expected:
                require(digest(records/expected["transition_record"],8192)["sha256"]==expected["transition_record_sha256"],
                        "passive transition record changed before input")
            self.check_confirmation_frame(self.owner/"frames"/confirmed)
            require(frame(self.owner/"frames"/confirmed) == confirmed_sha and
                    frame(self.owner/"frames"/expected["png"]) == expected["png_sha256"],
                    "reviewed frames changed before key")
            require(self.clock()-self.after_ns <= T.GUARD_AFTER_FRAME*T.NS and self.budget(T.KEY+T.RETIRE_MARGIN),
                    "post-frame focus/save sample expired")
            key, successor = ROUTE[self.state][view]
            send_before = min(self.latest[1]+4*T.NS,
                              self.menu_until+self.best_offset-T.RETIRE_MARGIN*T.NS)
            if recheck_receipt is not None:
                send_before = min(send_before,captured+RECHECK_AGE*T.NS)
            require(self.clock()<send_before, "fresh key submission budget expired")
            hmp = records/(name+"-hmp.jsonl")
            provenance = {**self.identity, "view":view, "key":key, "png_sha256":expected["png_sha256"],
                          "guest_guard":self.latest[0], "confirmed_png":confirmed,
                          "confirmed_png_sha256":confirmed_sha, "frame_comparison":comparison,
                          "approval_submitted_host_ns":submitted,
                          "approval_expires_host_ns":expected["approval_expires_host_ns"],
                          "send_before_host_ns":send_before}
            if "transition_record" in expected:
                provenance.update(transition_record=expected["transition_record"],
                                  transition_record_sha256=expected["transition_record_sha256"])
            if self.state == "confirmation":
                provenance["selected_quit_png"] = self.quit_baseline[0].name
                provenance["selected_quit_png_sha256"] = self.quit_baseline[1]
            if recheck_receipt is not None:
                paired_view,reviewed = recheck_receipt
                provenance.update(paired_view=paired_view, paired_review_submitted_host_ns=reviewed,
                                  paired_review_expires_host_ns=review["approval_expires_host_ns"])
            publish(records/(name+"-intent.json"), provenance)
            self.receipt["menu_commands"].append({"key":key,"intent":name+"-intent.json","original_status":None})
            if successor == "finished":
                self.receipt["original_visual_input_sent"] = None
            runner = [*self.visual[:3], str(self.owner/"code/observe-menu-key.py"),
                      "--visual-source", self.visual[3], *self.visual[4:],
                      "--attempt", self.identity["attempt"], "--boot-id",self.identity["boot_id"],
                      "--hmp-receipt",str(hmp),"--send-before-host-ns",str(send_before)]
            result = self.ctx.command(name+"-key", runner+["key",key,"--times","1"], T.KEY)
            require(result["original_returncode"] == 0, "original one-key monitor control failed")
            self.receipt["menu_commands"][-1]["original_status"] = result["original_returncode"]
            if successor == "confirmation":
                self.quit_baseline = (self.owner/"frames"/confirmed,confirmed_sha)
            self.state = successor
            self.current = self.confirmation = self.recheck = self.latest = None
            self.after_ns = self.clock()
            if successor == "finished":
                self.receipt["original_visual_input_sent"] = True
            else:
                self.transition = {**self.identity,"key":key,"from_view":view,"next_phase":successor,
                                   "input_intent":name+"-intent.json","original_key_status":0,
                                   "record":f"1433-menu-{number+1:02d}-transition.json",
                                   "key_completed_host_ns":self.after_ns,
                                   "cutoff_host_ns":self.after_ns+TRANSITION_CUTOFF*T.NS,
                                   "before_png":confirmed,"before_png_sha256":confirmed_sha,"frames":[]}
                self.receipt["menu_transitions"].append(self.transition)
        except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
            self.refuse(error)


def check_edges(outcome, receipt, boot, attempt):
    trace = outcome["quit_input"]
    commands = receipt["menu_commands"]
    require(trace["status"] == "ARMED" and trace["boot_id"] == boot and trace["attempt"] == attempt
            and all(trace["retroarch"] == outcome["core_readback"]["observed_retroarch"]["pid"] and
                    trace["start_ticks"] == outcome["core_readback"]["observed_retroarch"]["start_ticks"] and
                    command["original_status"] == 0 for command in commands), "wrong input original generation")
    edges = trace["edges"]
    require(3 <= len(commands) <= 5 and len({edge["node"] for edge in edges}) == 1 and
            [(edge["key"],edge["value"]) for edge in edges] ==
            [(command["key"],value) for command in commands for value in (1,0)], "ordered guest key edges missing")
    keys = [command["key"] for command in commands]
    require(keys[0]=="f1" and keys[-2:]==["ret","ret"] and keys.count("ret")==2,
            "one F1 followed by two distinct Return selections required")
    for key,down,up in zip(keys,edges[::2],edges[1::2]):
        if key in {"f1","backspace","ret"}:
            elapsed = ((up["kernel_sec"]-down["kernel_sec"])*1_000_000
                       + up["kernel_usec"]-down["kernel_usec"])
            require(80_000 <= elapsed <= 240_000,
                    f"original {key} down/up outside the single-hold acceptance band")
    device = next((d for d in trace["devices"] if d["node"] == edges[0]["node"]), {})
    require(device.get("open") == "READ_ONLY" and
            not any(k in device for k in ("dropped","read_error","edge_cap_reached")), "evdev original is incomplete")
    require(all((a["kernel_sec"],a["kernel_usec"]) < (b["kernel_sec"],b["kernel_usec"])
                for a,b in zip(edges,edges[1:])), "guest edge order ambiguous")
    require(trace["final_actor"].get("proc") == "ABSENT" or
            trace["final_actor"].get("same_generation") is False or
            trace["final_actor"].get("state") in ("Z","X","x"), "original emulator still live")


def verify_saves(before, after, chain, originals, folder, boot, attempt):
    receipt = document(folder/"file-originals.json",8192)
    require(receipt["boot_id"] == after["boot_id"] == boot and receipt["attempt"] == attempt and
            not receipt["errors"], "same-attempt save originals incomplete")
    old_key = chain["replacement_set"]+"/"+SAVE
    require(re.fullmatch(r"m7-1433/Saves-replaced/\d{4}_\d{2}_\d{2}-\d{6}/gb/ExitProbe[.]srm", old_key)
            and old_key not in before["remote"], "history is not the new expected replacement")
    expected_old = {"bytes": 8192, "sha256":"9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47"}
    checks = {"local.srm": (after["local"][SAVE], EXPECTED), "current.srm": (after["remote"][CURRENT], EXPECTED),
              "old.srm": (after["remote"][old_key], expected_old)}
    output = {}
    for name,(fact,expected) in checks.items():
        actual = digest(folder/name,8192)
        require(actual == originals[name] == expected and all(fact[k] == v for k,v in actual.items()) and
                receipt["files"][name] == {**actual, "mtime_ns":fact["mtime_ns"]}, "save original mismatch: "+name)
        output[name] = receipt["files"][name]
    require(all(before["remote"][CURRENT][k] == v for k,v in expected_old.items()),
            "original current remote was not the approved old bytes")
    require(before["remote"][CURRENT]["mtime_ns"] == output["old.srm"]["mtime_ns"],
            "original old history mtime changed")
    require(output["local.srm"]["mtime_ns"] > before["local"][SAVE]["mtime_ns"], "local save generation stale")
    return {"boot_id":boot, "attempt":attempt, "current":CURRENT, "history":old_key, "originals":output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("view")
    args = parser.parse_args()
    submit_approval(args.request.absolute(),args.view)


if __name__ == "__main__":
    main()
