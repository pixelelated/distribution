#!/usr/bin/env python3
"""AST/hash/source comparison only. No fixture/helper imports or execution."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE.parent / '2026-10-14-steam-client-corrections-source'
sha = lambda raw: hashlib.sha256(raw).hexdigest()


def main():
    assert sys.flags.optimize == 0
    binding = json.loads((HERE/'source.json').read_text())
    old_binding = json.loads((OLD/'source.json').read_text())
    installer = (ROOT/binding['installer_path']).read_bytes()
    assert sha(installer) == binding['installer_sha256'] == old_binding['installer_sha256']
    assert binding['helpers'] == old_binding['helpers'] and binding['limits'] == old_binding['limits']
    assert binding['cases'] == ['crc-failure-retry']
    assert binding['correction']['expected_original_caller_exits'] == [1,0]
    for path, digest in binding['preserved_packets'].items():
        assert sha((ROOT/path).read_bytes()) == digest
    for line in (OLD/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha((OLD/name).read_bytes()) == digest
    unchanged = ['python-boundary.py','exec-guard.py','transfer-child.py','client-helper.py',
                 'layout.json','route-cases.json','packaged/Config.json','packaged/steamwebhelper.json']
    for name in unchanged:
        assert (HERE/name).read_bytes() == (OLD/name).read_bytes(), name
    parsed = {p.name: ast.parse(p.read_bytes(), filename=str(p)) for p in HERE.glob('*.py')}
    old = (OLD/'boundary.py').read_text()
    first = old.index('\ndef event(row):'); last = old.index('\n\ndef main(', first)
    expected = old[:first] + '\nfrom event_records import event\n' + old[last:]
    assert (HERE/'boundary.py').read_text() == expected, 'Boundary logic changed outside event writer'
    expected = (OLD/'payload.py').read_text().replace("for name in ('payload.py', 'boundary.py'):",
        "for name in ('payload.py', 'boundary.py', 'event_records.py'):").replace(
        "    put(qa / 'events.ndjson', '')", "    put(qa / 'events.ndjson', '')\n    (qa / 'boundary-events').mkdir(mode=0o700)")
    assert (HERE/'payload.py').read_text() == expected, 'Payload/CRC generation changed'
    old_tree = ast.parse((OLD/'fixture.py').read_bytes())
    new_tree = parsed['fixture.py']
    original_read = ast.parse('[json.loads(line) for line in (output / "qa/events.ndjson").read_text().splitlines()]', mode='eval').body
    class RestoreReads(ast.NodeTransformer):
        count = 0
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == 'collect_events':
                assert ast.dump(node.args[0]) == ast.dump(ast.Name(id='output',ctx=ast.Load()))
                assert ast.literal_eval(node.args[1]) in ('events-controls','events-attempt-1','events-collected')
                self.count += 1
                return original_read
            return self.generic_visit(node)
    restore = RestoreReads()
    new_tree.body = [n for n in new_tree.body if not isinstance(n,ast.FunctionDef) or n.name != 'collect_events']
    restored = restore.visit(new_tree)
    assert restore.count == 3 and ast.dump(restored) == ast.dump(old_tree), 'Caller assertions/guards/timers changed'
    writer = parsed['event_records.py']
    values = {n.targets[0].id:ast.literal_eval(n.value) for n in writer.body if isinstance(n,ast.Assign)
              and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant)}
    assert values['PROCESS_BYTES'] == 4096 and values['MAX_PROCESSES'] == 512
    assert 'TOTAL_BYTES = 2 * 1024**2' in (HERE/'event_records.py').read_text()
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
                   and n.func.attr in ('setrlimit','signal','kill','killpg','Popen','run','system') for n in ast.walk(writer))
    intake = json.loads((HERE/'intake.json').read_text())
    for row in intake['members']:
        if 'copy' in row:
            raw = (HERE/row['copy']).read_bytes()
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    originals = [json.loads((HERE/f'evidence/attempt-{n}-result.json').read_text()) for n in (1,2)]
    assert [r['installer_exit'] for r in originals] == [1,1]
    assert all(r['trace']['status'] == 'RETURNED' and not r['trace']['remaining_traced'] for r in originals)
    assert 'CRC, length, or compressed stream verification failed' in (HERE/'evidence/installer-1.stderr').read_text()
    assert 'Steam client transfer failed (exit 1)' in (HERE/'evidence/installer-2.stderr').read_text()
    result = json.loads((HERE/'evidence/result.json').read_text())
    assert result['status'] == 'FAIL' and not result['remaining_descendants'] and result['supervision']['quiescent']
    for n in (1,2):
        storage = json.loads((HERE/f'evidence/attempt-{n}-storage.json').read_text())
        assert not any(k=='.local/share/Steam/.steam-client-update' or k.startswith('.local/share/Steam/.steam-client-update/') for k in storage)
    good = json.loads((HERE/'evidence/qa-client-good.json').read_text())
    bad = json.loads((HERE/'evidence/qa-client-bad.json').read_text())
    assert good['size'] == bad['size'] == 10676
    assert good['sha256'] == '870827a5e50cf1d3e4f6978ac6d60e8069b121963d099b1df5699f9b470235e5'
    assert bad['corruption'] == {'central_crc_offset':6731,'local_crc_offset':231,
        'member':'steamrtarm64/chromehtml.so','old_crc':3787868624,'wrong_crc':3787868625}
    offset = 0; manifest_end = None; by_pid = Counter(); rows = []
    for line in (HERE/'evidence/qa-events.ndjson').read_bytes().splitlines(keepends=True):
        row = json.loads(line); rows.append(row); offset += len(line); by_pid[row['pid']] += len(line)
        if row['pid'] == 67 and row['kind'] == 'boundary-exit':
            assert row['original_exit'] == 0; manifest_end = offset
    assert manifest_end == 10806 > good['size'] and not any(r['pid']==68 for r in rows)
    assert any(r['pid']==68 and r['exit']==1 for r in originals[1]['trace']['original_exits'])
    assert max(by_pid.values()) == 633 < 4096 < good['size']
    print(json.dumps({'status':'STATIC_ONLY_PASS','installer_sha256':sha(installer),
        'python_ast':sorted(parsed),'unchanged_copies':unchanged,
        'boundary_transport_main_and_result_wrapper_unchanged':True,
        'payload_crc_generator_unchanged':True,'caller_ast_unchanged_except_three_event_reads_and_collector':True,
        'limits_tls_exec_denial_assertions_unchanged':True,'old_packet_hashes_unchanged':True,
        'original_failure_caller_exits':[1,1],'original_archive_child_exit':1,
        'original_shared_event_offset_before_second_archive':manifest_end,'archive_child_fsize':good['size'],
        'original_max_event_bytes_per_pid':max(by_pid.values()),'proposed_per_process_event_cap':4096,
        'errno_in_original_receipt':None,'mechanism':'source-consistent FSIZE collision; direct errno not retained',
        'fixture_import_generation_or_runtime':False,'prepared_case':'crc-failure-retry',
        'expected_new_original_caller_exits':[1,0],'runtime':'UNRUN'},indent=2))


if __name__=='__main__':
    main()
