#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Pure fixed-schema proof parser; does not decide overall provider usability."""
import argparse
import json
import math
from pathlib import Path
import re

# Inclusive numeric ranges. Invalid probe values (-1) fail closed.
COMMON = {'elapsed_ms': (0, 360000)}
SCHEMAS = {
    'QA616_REQUEST': dict(COMMON, resource=(1, 16), request=(1, 64), provider=(0, 4), redirect_status=(0, 599), ua_present=(0, 1), ua_sha256=None),
    'QA616_RESPONSE': dict(COMMON, resource=(1, 16), requests=(0, 64), provider=(0, 4), status=(0, 599), response_present=(0, 1)),
    'QA616_RESOURCE_ERROR': dict(COMMON, resource=(1, 16), provider=(0, 4), domain_class=(0, 3), code=(-2147483648, 2147483647)),
    'QA616_DOM_BINDING': dict(COMMON, document=(1, 1e16), resource_at_callback=(0, 16), provider=(0, 4), width=(1, 32768), height=(1, 32768), scale=(0.001, 32), ua_present=(0, 1), ua_sha256=None),
    'QA616_INPUT': dict(COMMON, document=(1, 1e16), resource_at_callback=(0, 16), sequence=(1, 8), trusted=(0, 1), eligible=(0, 1), focused=(0, 1), render_delta_ms=(0, 360000)),
    'QA616_BINDING_UNAVAILABLE': dict(COMMON, document=(1, 1e16), reason=(0, 1)),
    'QA616_PROOF_LIMIT': {'channel': (1, 2)},
}
FRACTIONAL = {'elapsed_ms', 'scale', 'render_delta_ms'}


def is_digest(value):
    return isinstance(value, str) and bool(re.fullmatch('[0-9a-f]{64}', value))


def validate(tag, value):
    if not isinstance(value, dict) or set(value) != set(SCHEMAS[tag]):
        raise ValueError('proof record schema mismatch')
    for key, bounds in SCHEMAS[tag].items():
        item = value[key]
        if bounds is None:
            if item != 'unknown' and not is_digest(item):
                raise ValueError('invalid digest field')
        elif type(item) not in (int, float) or not math.isfinite(item) or not bounds[0] <= item <= bounds[1] or (key not in FRACTIONAL and int(item) != item):
            raise ValueError('invalid numeric field')
    if 'ua_present' in value and bool(value['ua_present']) != is_digest(value['ua_sha256']):
        raise ValueError('digest availability mismatch')
    return {'tag': tag, **value}


def parse(text):
    if len(text.encode()) > 1048576:
        raise ValueError('input exceeds one MiB')
    records = []
    for line in text.splitlines():
        tag, _, body = line.partition(' ')
        if tag not in SCHEMAS:
            continue  # Never copy unrelated native/library diagnostics to output.
        if len(line) > 2048 or len(records) >= 256:
            raise ValueError('record bound exceeded')
        records.append(validate(tag, json.loads(body)))
    return records


def calibration_requests(text):
    if len(text.encode()) > 65536:
        raise ValueError('echo input exceeds bound')
    events = json.loads(text)
    if not isinstance(events, list) or len(events) > 64:
        raise ValueError('echo event bound')
    for index, event in enumerate(events, 1):
        if not isinstance(event, dict) or set(event) != {'sequence', 'route', 'elapsed_ms', 'ua_sha256'}:
            raise ValueError('echo schema mismatch')
        if type(event['sequence']) is not int or event['sequence'] != index or event['route'] not in ['original', 'final', 'error503', 'dropped', 'unknown']:
            raise ValueError('echo sequence or route invalid')
        if type(event['elapsed_ms']) not in (int, float) or not math.isfinite(event['elapsed_ms']) or not 0 <= event['elapsed_ms'] <= 242000:
            raise ValueError('echo time invalid')
        if event['ua_sha256'] != 'unknown' and not is_digest(event['ua_sha256']):
            raise ValueError('echo digest invalid')
    return events


def digest_comparison(pairs):
    if not pairs or any(not is_digest(a) or not is_digest(b) for a, b in pairs):
        return 'unknown'
    return 'matched' if all(a == b for a, b in pairs) else 'mismatched'


def summarise(records, echo=None):
    groups = {tag: [row for row in records if row['tag'] == tag] for tag in SCHEMAS}
    requests = groups['QA616_REQUEST']
    bindings = groups['QA616_DOM_BINDING']
    inputs = groups['QA616_INPUT']
    limits = bool(groups['QA616_PROOF_LIMIT'])
    # A single document and one navigation are a bounded observation, not a
    # cryptographic binding. Redirects remain request events on that resource.
    resource_ids = {row['resource'] for row in requests}
    single_navigation = len(resource_ids) == 1 and len(bindings) == 1 and bindings[0]['resource_at_callback'] in resource_ids
    binding_match = 'unknown'
    if single_navigation and requests[-1]['provider'] == bindings[0]['provider'] and not limits:
        binding_match = digest_comparison([(requests[-1]['ua_sha256'], bindings[0]['ua_sha256'])])
    calibration = 'not_supplied'
    if echo is not None:
        selected = [event for event in echo if event['route'] in ['original', 'final']]
        if not limits and len(requests) == 2 and len(resource_ids) == 1 and [e['route'] for e in selected] == ['original', 'final'] and all(r['provider'] == 1 for r in requests) and [r['request'] for r in requests] == [1, 2] and [r['redirect_status'] for r in requests] == [0, 302]:
            calibration = digest_comparison([(row['ua_sha256'], event['ua_sha256']) for row, event in zip(requests, selected)])
        else:
            calibration = 'unknown'
    documents = {row['document'] for row in bindings}
    proven_inputs = [row for row in inputs if row['document'] in documents and row['trusted'] == row['eligible'] == row['focused'] == 1]
    if len({(row['document'], row['sequence']) for row in inputs}) != len(inputs):
        raise ValueError('duplicate input sequence')
    return {
        'schema': 1,
        'proof_record_count': len(records),
        'bounded_record_limit_reached': limits,
        'local_original_redirect_header_calibration': calibration,
        'dom_request_hash_observation': binding_match,
        'provider_wire_ua_guaranteed': False,
        'single_navigation_observed': single_navigation,
        'ua_ranking_evidence': 'incomplete' if binding_match != 'matched' or limits else 'request_signal_and_dom_matched; calibration_and_run_review_required',
        'page_observations_retained': {
            'positive_geometry_documents': len(bindings),
            'trusted_eligible_focused_input_events': len(proven_inputs),
            'untrusted_input_events': sum(row['trusted'] == 0 for row in inputs),
            'input_two_raf_delta_ms': [row['render_delta_ms'] for row in proven_inputs],
            'http_statuses': [row['status'] for row in groups['QA616_RESPONSE'] if row['response_present']],
            'resource_errors': [{'domain_class': row['domain_class'], 'code': row['code']} for row in groups['QA616_RESOURCE_ERROR']],
        },
        'independent_checks_required': ['visible sign-in screen, not provider error/block/challenge',
            'reviewed native input and frame proof; two rAF is not actual paint latency',
            'normal broker handoff, config equality, pressure/deadline and cleanup receipt',
            'fixed-UA page/memory observations remain separately usable when UA ranking is unknown'],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--echo', type=Path)
    args = parser.parse_args()
    try:
        records = parse(args.log.read_text())
        echo = calibration_requests(args.echo.read_text()) if args.echo else None
        print(json.dumps(summarise(records, echo), indent=2))
    except (OSError, ValueError, TypeError, KeyError, OverflowError):
        parser.exit(2, 'proof parsing refused: invalid or incomplete record schema\n')
