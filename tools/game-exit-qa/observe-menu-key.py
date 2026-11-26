"""Record one reviewed ordinary menu key HMP submission. This records host I/O only."""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path


VISUAL_SHA256 = '81565f39ce5bdbdce05fc7ec7b27f40ca1d95051430382c5e13f1ef58434cd06'
PROMPT = b'(qemu) '
STREAM_CAP = 8192
CONTROL_SECONDS = 5.0
DRAIN_SECONDS = 1.0
HOLD_MS = 120
HELD_KEYS = {"f1", "backspace", "ret"}
ANSI_CSI = re.compile(rb'\x1b\[[0-?]*[ -/]*[@-~]')
DIAGNOSTIC = re.compile(rb'^(error|unknown|invalid|failed|could not|cannot|unsupported)\b', re.I)


class Refusal(RuntimeError):
    pass


def error_info(error):
    return {'class':type(error).__name__,'errno':getattr(error,'errno',None),'message':str(error)[:512]}


def visual_monitor(path):
    with path.open('rb') as file:
        source = file.read(128*1024+1)
    if len(source)>128*1024 or hashlib.sha256(source).hexdigest() != VISUAL_SHA256:
        raise Refusal('visual helper source differs from the pinned original')
    module = {'__name__':'bound_visual_monitor','__file__':str(path)}
    exec(compile(source, str(path), 'exec'), module)
    return module['Monitor']


def selected_request(key):
    if key in HELD_KEYS:
        return f"sendkey {key} {HOLD_MS}"
    if key == "up":
        return "sendkey "+key
    raise Refusal("unsupported one-key navigation request")


def observed_monitor(base, key, send_before_host_ns):
    request = selected_request(key)
    class ObservedMonitor(base):
        def __init__(self, path, record, deadline):
            self.record = record
            self.deadline = deadline
            self.index = 0
            try:
                super().__init__(path, timeout=min(2.0, deadline-time.monotonic()))
            except BaseException:
                if hasattr(self, 'sock'):
                    self.sock.close()
                raise

        def cmd(self, text, settle=0.3):
            if text != request or self.index >= 1 or settle != 0.1:
                raise Refusal('only one bound menu key is supported')
            left = self.deadline-time.monotonic()
            if left <= 0:
                raise Refusal('controller deadline before next submission')
            self.sock.settimeout(left)
            self.index += 1
            self.send_returned = False
            self.record('send-intent', index=self.index,
                        request_base64=base64.b64encode((text+'\n').encode()).decode())
            left = min(self.deadline-time.monotonic(), (send_before_host_ns-time.monotonic_ns())/10**9)
            if left <= 0:
                raise Refusal('fresh host submission deadline expired before send')
            self.sock.settimeout(left)
            try:
                return super().cmd(text, settle)
            except OSError as error:
                if self.send_returned:
                    raise
                # sendall may have written some bytes before reporting an error.
                self.record('send-error', index=self.index, error=error_info(error))
                raise Refusal('submission status unknown') from error

        def _drain(self, quiet):
            if self.index:
                # The pinned Monitor.cmd reaches _drain only after sendall returns.
                self.send_returned = True
                self.record('send-return', index=self.index)
            began = time.monotonic()
            end = min(self.deadline, began+DRAIN_SECONDS)
            raw = bytearray()
            socket_error = None
            while True:
                left = end-time.monotonic()
                if left <= 0:
                    stop = 'deadline'
                    break
                try:
                    self.sock.settimeout(min(quiet,left))
                    data = self.sock.recv(min(4096, STREAM_CAP+1-len(raw)))
                except TimeoutError:
                    stop = 'quiet' if quiet < left and time.monotonic() < end else 'deadline'
                    break
                except OSError as error:
                    stop = 'read-error'
                    socket_error = error_info(error)
                    break
                if not data:
                    stop = 'eof'
                    break
                raw.extend(data)
                if len(raw)>STREAM_CAP:
                    stop = 'byte-cap'
                    break
            sample = bytes(raw[:STREAM_CAP])
            lines = re.split(rb'[\r\n]+', ANSI_CSI.sub(b'', sample))
            diagnostics = [line[:256].decode('utf-8','replace') for line in lines
                           if DIAGNOSTIC.match(line.strip().removeprefix(PROMPT))]
            prompted = sample.endswith(PROMPT)
            self.record('reply' if self.index else 'greeting', index=self.index,
                        read_begin_monotonic_ns=int(began*1e9), quiet_seconds=quiet,
                        end_reason=stop, trailing_prompt=prompted, retained_bytes=len(sample),
                        truncated=len(raw)>STREAM_CAP, raw_base64=base64.b64encode(sample).decode(),
                        diagnostics=diagnostics[:8], diagnostic_count=len(diagnostics), error=socket_error)
            if stop!='quiet' or not prompted or diagnostics:
                raise Refusal(f'HMP {"reply" if self.index else "greeting"} {stop} without a clean observed prompt')
            return sample.decode('utf-8','replace')

    return ObservedMonitor


def observe(args):
    # Reserve before connecting. An interrupted partial file is an occupied attempt.
    with args.hmp_receipt.open('x', encoding='utf-8') as out:
        def record(event, **data):
            row = {'event':event,'monotonic_ns':time.monotonic_ns(),**data}
            out.write(json.dumps(row, separators=(',',':'))+'\n')
            out.flush()
            os.fsync(out.fileno())

        record('episode', attempt=args.attempt, guest_boot_id=args.boot_id, monitor=args.monitor,
               visual_source=str(args.visual_source), visual_sha256=VISUAL_SHA256, key=args.keyname, count=1,
               raw_limit_per_read=STREAM_CAP, controller_seconds=CONTROL_SECONDS,
               send_before_host_ns=args.send_before_host_ns,
               **({"hold_ms":HOLD_MS} if args.keyname in HELD_KEYS else {}))
        deadline = time.monotonic()+CONTROL_SECONDS
        mon = None
        try:
            if time.monotonic_ns() >= args.send_before_host_ns:
                raise Refusal('fresh host submission deadline expired before connect')
            base = visual_monitor(args.visual_source)
            mon = observed_monitor(base,args.keyname,args.send_before_host_ns)(args.monitor, record, deadline)
            if args.keyname in HELD_KEYS:
                # As in the held #1427 control, QEMU schedules one release.
                mon.cmd(selected_request(args.keyname),settle=.1)
                time.sleep(.15)
            else:
                mon.sendkey(args.keyname,args.times)
        except (Refusal,OSError,ValueError) as error:
            record('result', status='HMP_OBSERVATION_INCOMPLETE', error=error_info(error))
            return 2
        finally:
            if mon is not None:
                mon.close()
        record('result', status='HMP_ONE_REPLY_PROMPT_OBSERVED')
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--visual-source',type=Path,required=True)
    parser.add_argument('--monitor',required=True)
    parser.add_argument('--attempt',required=True)
    parser.add_argument('--boot-id',required=True)
    parser.add_argument('--hmp-receipt',type=Path,required=True)
    parser.add_argument('--send-before-host-ns',type=int,required=True)
    parser.add_argument('command',choices=['key'])
    parser.add_argument('keyname',choices=["f1","backspace","up","ret"])
    parser.add_argument('--times',type=int,choices=[1],required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9a-f]{32}',args.attempt) or not re.fullmatch(
            r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',args.boot_id):
        parser.error('expected a bound attempt and boot ID')
    os.umask(0o077)
    try:
        return observe(args)
    except OSError as error:
        print(f'HMP receipt I/O refusal: {error}',file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
