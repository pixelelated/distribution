#!/usr/bin/env python3
"""UNRUN #577 synthetic backend controls; run only under coordinator allocation.

Execute a hash-bound copy of wifictl with exactly its /etc/profile source line
replaced by a shim. No real nmcli, iwctl, iw, settings, sysfs, or sleep calls.
The private PATH contains only the five text utilities used by these branches.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile


SHIM = r'''
record() { printf '%s\n' "$*" >> "${WIFI_FIXTURE_DIR}/calls"; }
counter() {
  local n=0
  if [[ -f "${WIFI_FIXTURE_DIR}/$1" ]]; then
    read -r n < "${WIFI_FIXTURE_DIR}/$1"
  fi
  COUNTER=$((n + 1))
  printf '%s\n' "${COUNTER}" > "${WIFI_FIXTURE_DIR}/$1"
}
get_setting() {
  case "$1" in
    wifi.country) printf '%s' "${FIX_COUNTRY}" ;;
    wifi.adhoc.enabled|wifi.adhoc.id|wifi.ssid|wifi.key) return 0 ;;
    *) record "UNEXPECTED get_setting $*"; return 99 ;;
  esac
}
command() {
  if [[ "$*" == '-v nmcli' ]]; then
    [[ "${FIX_NMCLI}" == 1 ]] || return 1
    printf '%s\n' nmcli
  else
    record "UNEXPECTED command $*"; return 99
  fi
}
ls() {
  [[ "$*" == /sys/class/net ]] || { record "UNEXPECTED ls $*"; return 99; }
  if [[ "${FIX_ADAPTER}" != none ]]; then printf '%s\n' wlan577; fi
}
function [() {
  if [[ $# == 3 && "$1" == -d && "$2" == /sys/class/net/wlan577 && "$3" == ']' ]]; then
    builtin [ "${FIX_ADAPTER}" = ok ]
  elif [[ $# == 4 && "$1" == '!' && "$2" == -d && "$3" == /sys/class/net/wlan577 && "$4" == ']' ]]; then
    builtin [ "${FIX_ADAPTER}" != ok ]
  else
    builtin [ "$@"
  fi
}
iwctl() {
  record "iwctl $*"
  [[ "$*" == 'device list' ]] || { record 'UNEXPECTED iwctl'; return 99; }
  counter iwd-count
  if (( COUNTER >= FIX_READY_AT )); then printf '%s\n' wlan577; fi
  return "${FIX_IWD_RC}"
}
iw() {
  record "iw $*"
  [[ "$*" == "reg set ${FIX_COUNTRY}" ]] || { record 'UNEXPECTED iw'; return 99; }
  return "${FIX_REG_RC}"
}
sleep() {
  record "sleep $*"
  case "$*" in 1|2) return 0 ;; *) record 'UNEXPECTED sleep'; return 99 ;; esac
}
nmcli() {
  record "nmcli $*"
  if [[ "$1" == -w && "$2" == 15 ]]; then shift 2; fi
  case "$*" in
    'dev wifi rescan ifname wlan577')
      counter rescan-count
      printf '%s' "${FIX_RESCAN_OUT}"
      if (( COUNTER == 1 )); then return "${FIX_RESCAN_RC}"; fi
      return "${FIX_SECOND_RC}"
      ;;
    '-t -f SSID dev wifi list ifname wlan577')
      printf '%s' "${FIX_ROWS}"
      return "${FIX_LIST_RC}"
      ;;
    *) record "UNEXPECTED nmcli $*"; return 99 ;;
  esac
}
'''


DEFAULTS = dict(ADAPTER='ok', NMCLI='1', COUNTRY='', READY_AT='1', IWD_RC='0',
                REG_RC='0', RESCAN_RC='0', SECOND_RC='0', LIST_RC='0', ROWS='',
                RESCAN_OUT='')
RAW = '\n Cafe\\: Guest \nCafe\\: Guest\nBack\\\\Slash\nCafe\\: Guest\nTabbed\tSSID\n'
DECODED = ' Cafe: Guest \nBack\\Slash\nCafe: Guest\nTabbed\tSSID\n'


def cases():
    """Expected results from source inspection, NOT execution receipts."""
    for command in ('list', 'scanlist'):
        scans = 1 if command == 'list' else 2
        # name, shim inputs, new rc, old stdout, new stdout, new iwctl/rescan/list counts
        variants = [
            ('empty', {}, 0, '', '', (1, scans, 1)),
            ('unescape', dict(ROWS=RAW), 0, DECODED, DECODED, (1, scans, 1)),
            ('adapter-absent', dict(ADAPTER='none'), 2, '', '', (0, 0, 0)),
            ('adapter-disappeared', dict(ADAPTER='gone'), 2, '', '', (0, 0, 0)),
            ('nmcli-missing', dict(NMCLI='0'), 2, '', '', (0, 0, 0)),
            ('readiness-exhausted', dict(READY_AT='6'), 1, '', '',
             (5, scans - 1, 0)),
            ('readiness-query-failed', dict(IWD_RC='9', READY_AT='6'), 9, '', '',
             (5, scans - 1, 0)),
            ('readiness-partial-failed', dict(IWD_RC='9'), 9, '', '',
             (5, scans - 1, 0)),
            ('readiness-recovers', dict(READY_AT='3'), 0, '', '', (3, scans, 1)),
            ('country-ok', dict(COUNTRY='US'), 0, '', '', (1, scans, 1)),
            ('country-failed', dict(COUNTRY='US', REG_RC='6'), 6, '', '',
             (1, scans - 1, 0)),
            ('rescan-failed', dict(RESCAN_RC='8'), 8, '', '',
             (1 if command == 'list' else 0, 1, 0)),
            ('rescan-timeout', dict(RESCAN_RC='3'), 3, '', '',
             (1 if command == 'list' else 0, 1, 0)),
            ('enumeration-failed', dict(LIST_RC='8'), 8, '', '', (1, scans, 1)),
            ('enumeration-timeout', dict(LIST_RC='3'), 3, '', '', (1, scans, 1)),
            ('enumeration-wrapper-timeout', dict(LIST_RC='124'), 124, '', '',
             (1, scans, 1)),
            ('enumeration-partial-failed', dict(LIST_RC='8', ROWS='Partial\\: SSID\n'),
             8, 'Partial: SSID\n', '', (1, scans, 1)),
            ('rescan-stdout', dict(RESCAN_OUT='diagnostic\n'), 0,
             'diagnostic\n' * scans, '', (1, scans, 1)),
        ]
        if command == 'scanlist':
            variants += [('second-rescan-failed', dict(SECOND_RC='10'), 10,
                          '', '', (1, 2, 0))]
        for name, inputs, rc, old_out, new_out, counts in variants:
            yield dict(name=f'{command}/{name}', command=command, inputs=inputs,
                       original=dict(rc=0, stdout=old_out),
                       current=dict(rc=rc, stdout=new_out, counts=counts))


def run_case(bash, adapted, env):
    # A regression cannot leave the shell's pipeline children running after the
    # fixture deadline. The coordinator's outer runner owns escaped processes.
    process = subprocess.Popen([bash, '--noprofile', '--norc', str(adapted),
                                env['WIFI_FIXTURE_COMMAND']], env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    try:
        out, err = process.communicate(timeout=5)
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        if process.poll() is None:
            process.wait(timeout=2)
        process.stdout.close()
        process.stderr.close()
    return process.returncode, out.decode(), err.decode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--version', choices=('original', 'current'), required=True)
    parser.add_argument('--tmp-root', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    binding = json.loads(Path(__file__).with_name('source-review.json').read_text())
    if digest != binding['sources'][args.version]['sha256']:
        raise SystemExit('Refusing source outside the recorded byte binding')
    original_line = b'\n. /etc/profile\n'
    if source.count(original_line) != 1:
        raise SystemExit('Refusing unexpected profile boundary')
    adapted_bytes = source.replace(original_line, b'\n. "${WIFI_FIXTURE_SHIM}"\n')
    bash = shutil.which('bash')
    if not bash:
        raise SystemExit('bash unavailable')
    utilities = {name: shutil.which(name) for name in ('grep', 'sed', 'sort', 'seq', 'tr')}
    if not all(utilities.values()):
        raise SystemExit('A required text utility is unavailable')
    failures = 0
    with tempfile.TemporaryDirectory(prefix='wifi577-backend-', dir=args.tmp_root) as tmp:
        root = Path(tmp)
        (root / 'bin').mkdir()
        for name, target in utilities.items():
            (root / 'bin' / name).symlink_to(target)
        shim = root / 'profile'
        shim.write_text(SHIM)
        adapted = root / 'wifictl'
        adapted.write_bytes(adapted_bytes)
        for number, case in enumerate(cases()):
            case_dir = root / str(number)
            case_dir.mkdir()
            env = dict(PATH=str(root / 'bin'), LC_ALL='C',
                       WIFI_FIXTURE_SHIM=str(shim), WIFI_FIXTURE_DIR=str(case_dir),
                       WIFI_FIXTURE_COMMAND=case['command'])
            env.update({'FIX_' + key: value for key, value in
                        dict(DEFAULTS, **case['inputs']).items()})
            rc, out, err = run_case(bash, adapted, env)
            calls_path = case_dir / 'calls'
            calls = calls_path.read_text().splitlines() if calls_path.exists() else []
            counts = (sum(c.startswith('iwctl ') for c in calls),
                      sum('dev wifi rescan' in c for c in calls),
                      sum('dev wifi list' in c for c in calls))
            expected = case[args.version]
            passed = rc == expected['rc'] and out == expected['stdout'] and not err
            passed &= not any('UNEXPECTED' in call for call in calls)
            if args.version == 'current':
                passed &= counts == expected['counts']
                passed &= all(c.startswith('nmcli -w 15 ') for c in calls
                              if 'dev wifi rescan' in c)
                passed &= not any('dev wifi list' in c for c in calls[:-1])
            result = dict(case=case['name'], version=args.version, sha256=digest,
                          adapted_sha256=hashlib.sha256(adapted_bytes).hexdigest(),
                          expected=expected, rc=rc, stdout=out, stderr=err, calls=calls,
                          result='PASS' if passed else 'FAIL')
            print(json.dumps(result, ensure_ascii=True), flush=True)
            failures += not passed
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
