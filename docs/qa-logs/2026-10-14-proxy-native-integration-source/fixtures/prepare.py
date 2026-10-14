#!/usr/bin/env python3
"""HELD: adapt the qualified small source preparer; no proxy import or build."""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import tarfile

PACKET=Path(__file__).resolve().parents[1]
BINDINGS_SHA256='d66230e0c13c527b20b00d305b2fd9da4b0f65585aa4591a2a8bd29a1add2682'
QUALIFIED_TRANSCRIPT=PACKET/'preparation-offset-followup/qualified-source.json'
QUALIFIED_TRANSCRIPT_SHA256='bbd19421935929cda116124199b0e81d0023cb8eb78ce627f3379ec76d61e3d6'


def need(value,message):
    if not value:raise RuntimeError(message)


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ('repo','archive','output'):parser.add_argument('--'+flag,type=Path,required=True)
    args=parser.parse_args();out=args.output.absolute()
    need(not out.exists() and not out.is_symlink(),'fresh preparation directory required')
    need(sha(PACKET/'bindings.json')==BINDINGS_SHA256,'packet binding changed')
    b=json.loads((PACKET/'bindings.json').read_text())
    need(sha(QUALIFIED_TRANSCRIPT)==QUALIFIED_TRANSCRIPT_SHA256,'qualified preparation transcript changed')
    qualified=json.loads(QUALIFIED_TRANSCRIPT.read_text())
    need(all(qualified[key]==b[key] for key in ('pin','archive_sha256','recipe_sha256','baseline')),
         'qualified preparation belongs to different source')
    transcript={row['name']:row for row in qualified['patches']}
    need(len(transcript)==len(qualified['patches']) and
         {name:row['sha256'] for name,row in transcript.items()}==b['patches'],
         'qualified preparation patch identities differ')
    for path,digest in b['evidence_sha256'].items():need(sha(PACKET/path)==digest,'reference changed: '+path)
    package=args.repo/'projects/ROCKNIX/packages/network/raofflineproxy'
    need(sha(package/'package.mk')==b['recipe_sha256'],'recipe changed')
    patches=sorted((package/'patches').glob('*.patch'))
    need({f.name:sha(f) for f in patches}==b['patches'],'current patch set changed')
    need(sha(args.archive)==b['archive_sha256'],'pinned archive changed')
    out.mkdir(parents=True);tree=out/'tree';tree.mkdir()
    report={'status':'FAIL','runtime':'source preparation only','patches':[],'bindings_sha256':BINDINGS_SHA256,
            'qualified_transcript_sha256':QUALIFIED_TRANSCRIPT_SHA256,
            'argv':sys.argv,'python':sys.version,'interpreter':{'path':sys.executable,'sha256':sha(sys.executable)}}
    def expired(*_):raise TimeoutError('45-second source preparation limit')
    signal.signal(signal.SIGALRM,expired);signal.alarm(45)
    try:
        version=subprocess.run(['patch','--version'],capture_output=True,text=True,timeout=3)
        report['patch_version']={'original_exit':version.returncode,'stdout':version.stdout,'stderr':version.stderr}
        need(version.returncode==0 and 'GNU patch' in version.stdout,'GNU patch required: prepare on host if absent in guest')
        invocation=shutil.which('patch');identity=Path(invocation).resolve(strict=True)
        report['patch_executable']={'invocation':invocation,'resolved_identity':str(identity),'sha256':sha(identity)}
        total=0
        with tarfile.open(args.archive) as archive:
            for member in archive:
                parts=PurePosixPath(member.name).parts
                need(parts and parts[0]=='RAOfflineProxy-'+b['pin'],'unexpected archive root')
                rel=PurePosixPath(*parts[1:]);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe archive member')
                if not (member.isfile() and rel.suffix=='.py' and str(rel).startswith(('linux/raofflineproxy/','linux/tests/'))):continue
                total+=member.size;need(total<10*1024*1024,'source budget exceeded')
                dest=tree/str(rel);need(not dest.exists(),'duplicate source member')
                dest.parent.mkdir(parents=True,exist_ok=True)
                with archive.extractfile(member) as source:dest.write_bytes(source.read())
        for patch in patches:
            got=subprocess.run(['patch','--batch','--fuzz=0','-p1'],input=patch.read_bytes(),cwd=tree,capture_output=True,timeout=5)
            row={'name':patch.name,'sha256':sha(patch),'original_exit':got.returncode,'stdout':got.stdout.decode(),'stderr':got.stderr.decode()};report['patches'].append(row)
            diagnostics=row['stdout']+row['stderr']
            need(got.returncode==0 and not re.search(r'fuzz|FAILED|Reversed',diagnostics,re.I),'patch failed or fuzzy/reversed: '+patch.name)
            if re.search(r'offset',diagnostics,re.I):
                need(row['stdout']==transcript[patch.name]['output'] and not row['stderr'],
                     'offset diagnostics differ from qualified transcript: '+patch.name)
                row['offsets_match_qualified_transcript']=True
        manifest=lambda:{str(f.relative_to(tree)):sha(f) for f in sorted(tree.rglob('*.py'))}
        need(manifest()==b['baseline'],'patched tree differs from qualified baseline')
        (tree/'linux/raofflineproxy/rvz_datasource.py').write_bytes((PACKET/'evidence/rvz_datasource.py').read_bytes())
        need(manifest()==b['candidate'],'reviewed padding composition differs')
        for f in tree.rglob('*.py'):ast.parse(f.read_bytes(),filename=str(f))
        (out/'scanner.py').write_bytes((PACKET/'evidence/list_jobs.py').read_bytes())
        (out/'raofflineproxy-ctl').write_bytes((PACKET/'evidence/raofflineproxy-ctl').read_bytes())
        report.update(status='PASS',pin=b['pin'],archive_sha256=b['archive_sha256'],recipe_sha256=b['recipe_sha256'],source_bytes=total,files=b['candidate'],scanner_sha256=sha(out/'scanner.py'),ctl_sha256=sha(out/'raofflineproxy-ctl'))
    except BaseException as error:
        report['error']=type(error).__name__+': '+str(error);raise
    finally:
        signal.alarm(0);(out/'source.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'status':report['status'],'receipt':str(out/'source.json')}))


if __name__=='__main__':main()
