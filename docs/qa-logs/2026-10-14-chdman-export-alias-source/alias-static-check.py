#!/usr/bin/env python3
"""Read-only hashes, archive headers/templates and AST; no runner imports/export."""
import ast
import hashlib
import json
from pathlib import Path
import tarfile

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / '2026-10-14-chdman-build-runner'
sha = lambda b: hashlib.sha256(b).hexdigest()

def main():
    correction = json.loads((HERE / 'correction.json').read_text())
    assert sha((OLD / 'SHA256SUMS').read_bytes()) == correction['parent_manifest_sha256']
    unchanged = []
    for p in OLD.rglob('*'):
        if not p.is_file() or p.name in ('SHA256SUMS', 'README.md', 'static-result.json', 'export.py'):
            continue
        rel = p.relative_to(OLD)
        assert p.read_bytes() == (HERE / rel).read_bytes(), str(rel)
        unchanged.append(str(rel))
    # Nested sealed manifest is also byte-identical.
    assert (HERE/'plan/SHA256SUMS').read_bytes() == (OLD/'plan/SHA256SUMS').read_bytes()
    for p in HERE.glob('*.py'):
        ast.parse(p.read_bytes(), filename=str(p), feature_version=(3,10))
    tree = ast.parse((HERE/'export.py').read_bytes())
    aliases = ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)
                                  and any(isinstance(t,ast.Name) and t.id=='OMITTED_TEST_ALIASES' for t in n.targets)))
    assert aliases == {'3rdparty/zstd/tests/cli-tests/bin/unzstd':'zstd',
                       '3rdparty/zstd/tests/cli-tests/bin/zstdcat':'zstd'}
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
                   and n.func.attr in ('extract','extractall','symlink','symlink_to','link') for n in ast.walk(tree))
    binding = json.loads((HERE/'plan/input-bindings.json').read_text())['chdman']
    archive = Path(binding['archive']['path'])
    with archive.open('rb') as f:
        before = archive.stat()
        digest = hashlib.file_digest(f,'sha256').hexdigest()
    assert before.st_size == 213471628 and digest == binding['archive']['sha256']
    templates = json.loads((HERE/'template-evidence.json').read_text())['members']
    links = []; names=set()
    with tarfile.open(archive,'r:gz') as t:
        members=t.getmembers()
        assert len(members)==33835 and sum(m.size for m in members if m.isreg())==897821359
        for m in members:
            p=Path(m.name)
            assert not p.is_absolute() and '..' not in p.parts and str(p)==m.name.rstrip('/')
            assert p.parts[0]==binding['archive_root'] and m.name not in names
            names.add(m.name)
            rel=str(p.relative_to(binding['archive_root']))
            if m.issym():
                assert rel in aliases and m.linkname==aliases[rel] and m.size==0 and m.mode==0o777
                links.append({'path':rel,'target':m.linkname,'mode':m.mode,'bytes':m.size})
            else:
                assert (m.isreg() or m.isdir()) and not m.linkname and m.mode & ~0o777==0
                assert m.size>=0 and (m.isreg() or m.size==0)
            assert not m.issparse() and all(ord(c)>=32 and ord(c)!=127 for c in m.name)
            if rel in templates:
                raw=t.extractfile(m).read()
                assert len(raw)==templates[rel]['bytes'] and sha(raw)==templates[rel]['sha256']
                lines=raw.decode().splitlines()
                for excerpt in templates[rel]['excerpts']:
                    assert '\n'.join(lines[excerpt['first_line']-1:excerpt['last_line']])==excerpt['text']
        assert {r['path'] for r in links}==set(aliases) and len(links)==2
    after=archive.stat()
    assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    for row in correction['evidence']:
        raw=(HERE/row['copy']).read_bytes()
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    result=json.loads((HERE/'evidence/result.json').read_text())
    assert result['status']=='FAIL' and result['original_container_exit']==result['original_attach_exit']==1
    assert result['watchdog_original_exit']==0 and result['cleanup']['status']=='PASS'
    assert json.loads((HERE/'evidence/export.json').read_text())['original_exit']==1
    print(json.dumps({'status':'STATIC_ONLY_PASS','archive_sha256':digest,'archive_bytes':before.st_size,
        'archive_members':len(members),'regular_bytes':897821359,'exact_omissions':links,
        'selected_templates_rechecked':sorted(templates),'unchanged_files':sorted(unchanged),
        'original_failure_preserved':True,'runner_imported':False,'export_configure_build_runtime':'UNRUN'},indent=2))

if __name__=='__main__':main()
