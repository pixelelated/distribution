#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Classify prepared future provider evidence without turning errors into speed wins."""
import argparse
import json
from pathlib import Path
import re


def sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def classify(case):
    reasons = []
    outcome = case.get('outcome', 'unknown')
    provider = case.get('provider')
    if provider not in ['light', 'dropbox', 'drive', 'onedrive']:
        reasons.append('unknown_provider')
    expected = 'light_control' if provider == 'light' else 'unauthed_form'
    if outcome != expected:
        reasons.append('outcome_is_not_the_required_form')
    for forbidden in ['credentials_entered', 'consent_submitted', 'persistent_remote_created']:
        if case.get(forbidden) is not False:
            reasons.append(forbidden + '_not_proven_false')
    if case.get('normal_es_broker_handoff') is not True:
        reasons.append('normal_handoff_unproved')
    if case.get('guard_triggered') is not False or case.get('cleanup_complete') is not True:
        reasons.append('guard_or_cleanup_incomplete')
    binding = case.get('ua_binding', {})
    if not sha(binding.get('http_sha256')) or binding.get('http_sha256') != binding.get('dom_sha256'):
        reasons.append('actual_http_dom_ua_binding_missing')
    required_source = 'local_echo' if provider == 'light' else 'validated_sent_request_hook'
    if binding.get('http_source') != required_source or (provider != 'light' and not sha(binding.get('hook_calibration_receipt'))):
        reasons.append('request_header_provenance_inadequate')
    if case.get('unobscured_frame_reviewed') is not True or case.get('trusted_input_count', 0) < 1:
        reasons.append('usable_trusted_input_unproved')
    if not sha(case.get('input_frame_sha256')) or case.get('positive_input_render_delta_ms', 0) <= 0:
        reasons.append('input_to_frame_evidence_incomplete')
    if not sha(case.get('original_result_sha256')):
        reasons.append('original_result_unbound')
    comparable = not reasons
    return {'id': case.get('id'), 'provider': provider, 'outcome': outcome,
            'comparable_unauthed_form': comparable, 'reasons': reasons,
            'authentication_success': False, 'memory_fix_proven': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    values = json.loads(args.input.read_text())
    rows = [classify(value) for value in values]
    print(json.dumps({'cases': rows, 'all_comparable': bool(rows) and all(row['comparable_unauthed_form'] for row in rows)}, indent=2))
    # Exclusions are findings, not script crashes. Runtime success lives in
    # the original case result, separately from comparability.
