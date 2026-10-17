#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Small pure preparation/parser controls; no browser, network or compiler."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import time


def module(path):
    spec = importlib.util.spec_from_file_location(path.stem.replace('-', '_'), path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main(args):
    started = time.monotonic()
    root = Path(__file__).resolve().parent
    analyse = module(root / 'analyse.py')
    prepare = module(root / 'prepare.py')
    passed = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        passed.append(name)

    def refuses(name, operation):
        try:
            operation()
        except (ValueError, FileExistsError):
            passed.append(name)
            return
        raise AssertionError(name)

    for path in root.glob('*.py'):
        ast.parse(path.read_text())
        passed.append('AST ' + path.name)
    digest = 'a' * 64
    request1 = dict(elapsed_ms=1, resource=1, request=1, provider=1, redirect_status=0, ua_present=1, ua_sha256=digest)
    request2 = dict(request1, elapsed_ms=2, request=2, redirect_status=302)
    dom = dict(elapsed_ms=3, document=12345, resource_at_callback=1, provider=1, width=640, height=457, scale=1, ua_present=1, ua_sha256=digest)
    trusted = dict(elapsed_ms=4, document=12345, resource_at_callback=1, sequence=1, trusted=1, eligible=1, focused=1, render_delta_ms=33.3)
    untrusted = dict(trusted, sequence=2, trusted=0)
    records = [analyse.validate(tag, row) for tag, row in [
        ('QA616_REQUEST', request1), ('QA616_REQUEST', request2), ('QA616_DOM_BINDING', dom),
        ('QA616_INPUT', trusted), ('QA616_INPUT', untrusted)]]
    echo = analyse.calibration_requests(json.dumps([
        dict(sequence=1, route='original', elapsed_ms=1, ua_sha256=digest),
        dict(sequence=2, route='final', elapsed_ms=2, ua_sha256=digest)]))
    good = analyse.summarise(records, echo)
    check('original and redirect calibration requires both matching hashes', good['local_original_redirect_header_calibration'] == 'matched')
    check('DOM and request match is explicitly not provider wire proof', good['dom_request_hash_observation'] == 'matched' and not good['provider_wire_ua_guaranteed'])
    check('untrusted negative control does not count as trusted input', good['page_observations_retained']['trusted_eligible_focused_input_events'] == 1 and good['page_observations_retained']['untrusted_input_events'] == 1)
    missing = copy.deepcopy(records)
    for row in missing[:2]:
        row.update(ua_present=0, ua_sha256='unknown')
    absent = analyse.summarise(missing, echo)
    check('missing request hash withholds only UA ranking', absent['local_original_redirect_header_calibration'] == 'unknown' and absent['ua_ranking_evidence'] == 'incomplete' and absent['page_observations_retained']['trusted_eligible_focused_input_events'] == 1)
    mismatch = copy.deepcopy(echo)
    mismatch[-1]['ua_sha256'] = 'b' * 64
    check('redirect echo mismatch cannot qualify UA signal', analyse.summarise(records, mismatch)['local_original_redirect_header_calibration'] == 'mismatched')
    check('missing request events retain positive geometry', analyse.summarise(records[2:])['page_observations_retained']['positive_geometry_documents'] == 1)
    hidden = copy.deepcopy(records)
    hidden[-2]['eligible'] = 0
    check('ineligible trusted event is not positive readiness proof', analyse.summarise(hidden)['page_observations_retained']['trusted_eligible_focused_input_events'] == 0)
    limited = records + [analyse.validate('QA616_PROOF_LIMIT', {'channel': 1})]
    check('bound reached withholds complete UA claim', analyse.summarise(limited, echo)['ua_ranking_evidence'] == 'incomplete')
    refuses('extra URL field refused', lambda: analyse.validate('QA616_REQUEST', dict(request1, url='sensitive')))
    refuses('raw UA field refused', lambda: analyse.validate('QA616_DOM_BINDING', dict(dom, ua='sensitive')))
    refuses('nonfinite geometry refused', lambda: analyse.validate('QA616_DOM_BINDING', dict(dom, width=float('nan'))))
    refuses('invalid digest refused', lambda: analyse.validate('QA616_REQUEST', dict(request1, ua_sha256='not-a-hash')))
    refuses('numeric boolean refused', lambda: analyse.validate('QA616_INPUT', dict(trusted, trusted=True)))
    refuses('duplicate input event refused', lambda: analyse.summarise(records + [records[-1]]))
    check('unrelated native log content is not copied', analyse.parse('native private content\n') == [])
    with tempfile.TemporaryDirectory(prefix='.controls-', dir=root) as temporary:
        scratch = Path(temporary)
        bad = scratch / 'tampered.c'
        bad.write_text('not the reviewed source')
        refuses('tampered source refused', lambda: prepare.checked(bad, prepare.PRODUCT))
        result = prepare.prepare(args.repo, scratch / 'fresh')
        check('pure exact-source preparation reproduces candidate', result['candidate_sha256'] == hashlib.sha256((root / 'prepared/cloud-signin-window.c').read_bytes()).hexdigest())
        refuses('existing prepared output refused', lambda: prepare.prepare(args.repo, scratch / 'fresh'))
    proof = (root / 'proof.js').read_text()
    check('field values cookies URLs and page writes absent from proof JS', not any(term in proof for term in ['.value', 'document.cookie', 'location.href', '.focus(', 'fetch(', 'XMLHttpRequest', 'localStorage', 'sessionStorage']))
    check('no raw GError message is emitted by C proof', 'error->message' not in (root / 'proof.c.in').read_text())
    result = {'schema': 1, 'scope': 'pure host AST/preparation/parser; target compile and all browser runtime UNRUN',
              'passed': passed, 'count': len(passed), 'seconds': time.monotonic() - started,
              'services_listeners_network_compilers_started': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    main(parser.parse_args())
