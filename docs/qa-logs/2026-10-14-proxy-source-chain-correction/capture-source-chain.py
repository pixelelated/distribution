#!/usr/bin/env python3
"""UNRUN bounded readback of completed proxy build; no compiler/import/strip is executed."""
import argparse,hashlib,json,re,stat,struct,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
for name in ['checkout','build-root','build-owner','run','verified-root','verification-receipt','output']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();tree=a.checkout.resolve(strict=True);build=a.build_root.resolve(strict=True);out=a.output.absolute();assert not out.exists();out.mkdir(mode=0o700)
def sha(f):
    with f.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def write(f,obj):f.write_text(json.dumps(obj,indent=2)+'\n')
def row(f):return {'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f)}
def retained(f,name,limit=32*1024**2):
    assert f.is_file() and f.stat().st_size<=limit
    dest=out/name;dest.write_bytes(f.read_bytes());return row(dest)
def pycs(root):
    bases=list((root/'usr/lib').glob('python*/site-packages/raofflineproxy'));assert len(bases)==1
    base=bases[0];files=list(base.rglob('*'));assert len(files)<=2048 and not any(f.is_symlink() for f in files) and not list(base.rglob('*.py'))
    results={}
    for f in sorted(base.rglob('*.pyc')):
        data=f.read_bytes();assert len(data)>=16
        results[str(f.relative_to(root))]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'mode':f.stat().st_mode&0o7777,
          'header_hex':data[:16].hex(),'magic_hex':data[:4].hex(),'flags_little_endian':int.from_bytes(data[4:8],'little'),'marshal_not_loaded':True}
    assert 30<=len(results)<=112;return results
def elf(path):
    assert path.stat().st_size<=128*1024**2;data=path.read_bytes();assert data[:6]==b'\x7fELF\x02\x01'
    h=struct.unpack_from('<16sHHIQQQIHHHHHH',data);shoff=h[6];entsize,n,strings=h[11:14];assert entsize==64 and 0<n<=1024 and strings<n
    entries=[struct.unpack_from('<IIQQQQIIQQ',data,shoff+i*64) for i in range(n)]
    names=entries[strings];table=data[names[4]:names[4]+names[5]];sections={}
    for e in entries:
        name=table[e[0]:].split(b'\0',1)[0].decode()
        if e[2]&2:
            assert name not in sections
            raw=b'' if e[1]==8 else data[e[4]:e[4]+e[5]]
            assert e[1]==8 or len(raw)==e[5]
            sections[name]={'type':e[1],'flags':e[2],'address':e[3],'bytes':e[5],'content_sha256':hashlib.sha256(raw).hexdigest()}
    return {'file':row(path),'class':64,'little_endian':True,'machine':h[2],'type':h[1],'allocated_sections':sections}
commit=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
binding=json.loads((HERE/'chain-binding.json').read_text());assert commit==binding['distribution_commit']
assert sha(HERE/'prepared112.json')==binding['prepared112_sha256']
verification=json.loads(a.verification_receipt.read_text());assert verification['status']=='PASS' and verification['source']==commit
owner=json.loads((a.build_owner/'owner-result.json').read_text());assert owner['status']=='PASS' and not owner.get('cleanup_error') and not owner.get('signals') and not any(owner.get('surviving_host_command_groups',{}).values())
assert (a.run/'build.rc').read_text().strip()=='0';runner=json.loads((a.run/'runner-result.json').read_text());assert runner['runner_rc']==runner['command_rc']==runner['monitor_rc']==0
inputs=json.loads((a.build_owner/'build-inputs.json').read_text());assert inputs['commit']==commit and Path(inputs['checkout']).resolve()==tree and build==tree/inputs['build_root']
assert verification['es_commit']==inputs['es_commit']
image_stage=json.loads((a.build_owner/'stages/image/inner-result.json').read_text());assert image_stage['original_command_rc']==image_stage['wrapper_rc']==0 and not image_stage['signals']
evidence=[retained(f,name) for f,name in [(a.build_owner/'owner-result.json','build-owner-result.json'),(a.build_owner/'build-inputs.json','build-inputs.json'),(a.run/'runner-result.json','build-runner-result.json'),(a.build_owner/'stages/image/inner-result.json','image-inner-result.json'),(a.verification_receipt,'image-verification-original.json')]]
pins={'raofflineproxy':'c7ebd1b6e777f3751ff0ecdf8aba54045844e00d','rcheevos':'1433173220a7eaede6a9ed7a18e94117be1821e0','libchdr':'607694ca0812edfc9cc2030c64634fc2393668de'}
for key,pin in pins.items():
    package='raofflineproxy' if key=='raofflineproxy' else 'raofflineproxy-'+key
    recipe=tree/'projects/ROCKNIX/packages/network'/package/'package.mk';assert re.search(r'^PKG_VERSION="([0-9a-f]+)"$',recipe.read_text(),re.M).group(1)==pin
    evidence.append(retained(recipe,package+'-package.mk'))
    evidence.append(retained(build/'.stamps'/package/'build_target',package+'-build_target'))
    evidence.append(retained(build/'build'/(package+'-'+pin)/'.rocknix-unpack',package+'-unpack-stamp'))
    clean=a.build_owner/'stages'/('clean-'+package)/'host-result.json'
    clean_result=json.loads(clean.read_text());assert clean_result['original_host_make_rc']==0 and clean_result['container_observed'] and clean_result['observation_handshake']
    evidence.append(retained(clean,'clean-'+package+'-host-result.json'))
pkg=build/'build'/('raofflineproxy-'+pins['raofflineproxy']);stage=build/'install_pkg'/pkg.name;root=a.verified_root.resolve(strict=True)
expected=json.loads((HERE/'prepared112.json').read_text())['files'];assert len(expected)==112
actual={}
for source_root,count in binding['source_roots'].items():
    files=list((pkg/source_root).rglob('*.py'));assert len(files)==count and not any(f.is_symlink() for f in files)
    actual.update({str(f.relative_to(pkg)):sha(f) for f in files})
assert actual==expected
runtime_sources={name.removeprefix('linux/raofflineproxy/') for name in expected if name.startswith('linux/raofflineproxy/')}
assert len(runtime_sources)==45
write(out/'prepared112-actual.json',actual);evidence.append(row(out/'prepared112-actual.json'))
# DONE comes from pkgbuilder's actual subprocess returncode. Keep its original job lines/logs.
joblog=build/'.threads/joblog';assert joblog.stat().st_size<=8*1024**2
jobs=[]
for line in joblog.read_text().splitlines():
    fields=line.split()
    if len(fields)>=5 and fields[4] in ('raofflineproxy','raofflineproxy:target'):
        assert fields[0]=='DONE';jobs.append({'original_line':line,'task':fields[3],'sequence':fields[1]})
        log=build/'.threads/logs'/(str(int(fields[1]))+'.log')
        if not log.exists():log=build/'.threads/logs'/(fields[1]+'.log')
        evidence.append(retained(log,'package-'+fields[3]+'-'+fields[1]+'.log'))
original=binding['original_package_job']
assert jobs==[{key:original[key] for key in ['original_line','task','sequence']}]
assert sha(out/('package-'+original['task']+'-'+original['sequence']+'.log'))==original['log_sha256']
write(out/'package-jobs.json',jobs);evidence.append(row(out/'package-jobs.json'))
texts='\n'.join((out/('package-'+j['task']+'-'+j['sequence']+'.log')).read_text(errors='replace') for j in jobs)
plain=re.sub(r'\x1b\[[0-9;]*m','',texts)
for action in ['UNPACK','BUILD','INSTALL']:
    assert re.search(r'^'+action+r'\s+raofflineproxy(?:\s|$)',plain,re.M),action
compiled_paths=re.findall(r"^Compiling '([^']+)'\.\.\.$",plain,re.M)
compile_prefix=str(Path(inputs['container_checkout'])/inputs['build_root']/'install_pkg'/pkg.name/'usr/lib/python3.14/site-packages/raofflineproxy')+'/'
assert len(compiled_paths)==45 and all(path.startswith(compile_prefix) for path in compiled_paths)
assert {path[len(compile_prefix):] for path in compiled_paths}==runtime_sources
patch_prefix='projects/ROCKNIX/packages/network/raofflineproxy/patches/'
patches=sorted((tree/patch_prefix).glob('*.patch'));assert len(patches)==18
assert re.findall(r'^\s*APPLY PATCH \(common\)\s+(\S+)$',plain,re.M)==[patch_prefix+f.name for f in patches]
write(out/'package-patches.json',{str(f.relative_to(tree)):row(f) for f in patches});evidence.append(row(out/'package-patches.json'))
# Hash-binding preserves the exact source reviewed for fail-fast semantics,
# including the nested monitor exec, rather than inventing a build job/wait.
for name,identity in binding['chain_files'].items():
    assert sha(tree/name)==identity['sha256'],name
    evidence.append(retained(tree/name,name.replace('/','-')))
evidence.append(retained(HERE/'chain-binding.json','chain-binding.json'))
evidence.append(retained(HERE/'prepared112.json','prepared112.expected.json'))
staged=pycs(stage);final=pycs(root);assert staged==final and len(final)==45
assert {name.split('/site-packages/raofflineproxy/',1)[1][:-1] for name in final}==runtime_sources
verified_pycs={name:item for name,item in verification['products'].items() if '/site-packages/raofflineproxy/' in name and name.endswith('.pyc')}
assert set(verified_pycs)==set(final)
for name,item in final.items():
    recorded=verified_pycs[name];assert item['sha256']==recorded['sha256'] and item['bytes']==recorded['bytes']
    assert stat.filemode((root/name).stat().st_mode)==recorded['mode']
write(out/'emitted-pyc.json',{'staged_root':str(stage),'verified_image_root':str(root),'files':final,'timestamp_headers_preserved':True,'interpreter_not_executed':True,'host_marshal_not_used':True});evidence.append(row(out/'emitted-pyc.json'))
recipe=(tree/'projects/ROCKNIX/packages/network/raofflineproxy/package.mk').read_text()
native_roots={'RC':build/'build'/('raofflineproxy-rcheevos-'+pins['rcheevos']),'CHDR':build/'build'/('raofflineproxy-libchdr-'+pins['libchdr']),'GLUE':pkg/'third_party/rcheevos_glue','LZMA_SDK':pkg/'third_party/lzma-sdk'}
compiled={}
for variable,relative in re.findall(r'"\$\{(RC|CHDR|GLUE|LZMA_SDK)\}(/[^"\n]+\.c)"',recipe):
    path=native_roots[variable]/relative.lstrip('/');compiled[variable+relative]=row(path)
for path in native_roots['LZMA_SDK'].glob('*.c'):compiled['LZMA_SDK/'+path.name]=row(path)
assert 30<=len(compiled)<=128
write(out/'native-compiled-inputs.json',{'compiled_c_files':compiled,'recipe_sha256':sha(tree/'projects/ROCKNIX/packages/network/raofflineproxy/package.mk'),'scope':'Exact literal recipe C list and LZMA glob; source/header provenance also uses actual unpack stamps, pinned recipes and original package log.'});evidence.append(row(out/'native-compiled-inputs.json'))
raw=list(pkg.glob('.*/libraproxy_rchash.so'));assert len(raw)==1
native={'pre_strip':elf(raw[0]),'staged':elf(stage/'usr/lib/libraproxy_rchash.so'),'final_verified_root':elf(root/'usr/lib/libraproxy_rchash.so')}
assert native['staged']['file']['sha256']==native['final_verified_root']['file']['sha256']
verified_native=verification['products']['usr/lib/libraproxy_rchash.so']
assert all(native['final_verified_root']['file'][key]==verified_native[key] for key in ['sha256','bytes'])
assert stat.filemode((root/'usr/lib/libraproxy_rchash.so').stat().st_mode)==verified_native['mode']
assert all(item['machine']==62 for item in native.values())
assert native['pre_strip']['allocated_sections']==native['staged']['allocated_sections']==native['final_verified_root']['allocated_sections']
native.update(original_strip_returncode=None,strip_status_reason='scripts/build masks strip return with || :; record actual bytes and allocated-section correspondence, not fabricated strip success')
write(out/'native-chain.json',native);evidence.append(row(out/'native-chain.json'))
receipt={'status':'REVIEW_REQUIRED','distribution_commit':commit,'startup_source_sha256':expected['linux/raofflineproxy/proxy_service.py'],'prepared_python_files':112,
 'package_task':'install','package_sequence':original['sequence'],'package_task_original_exit':0,
 'package_build_original_exit':0,'package_build_exit_basis':'inferred nested scripts/build success through original install309 DONE0, fresh BUILD log and reviewed unguarded fail-fast call chain; no standalone build wait',
 'python_compile_original_exit':0,'python_compile_exit_basis':'inferred original compileall success through install309 DONE0, exact reviewed set-e call chain, all45 original Compiling lines and emitted pycs; no independent child wait claimed',
 'standalone_build_wait_recorded':False,'standalone_compileall_wait_recorded':False,'final_files_match_image_verification':True,
 'post_strip_rchash_sha256':native['staged']['file']['sha256'],'pins':pins,'reviewed_source_to_bytecode_and_strip_chain':False,'clean_ready_report_verified':False,'evidence':evidence,
 'scope':'Bounded final build readback; coordinator must verify original image verification and source/compile/strip evidence before setting PASS/reviewed. No bytecode decompile, recompilation or native runtime.'}
write(out/'source-receipt.review-required.json',receipt)
print(json.dumps({'status':'CAPTURED_REVIEW_REQUIRED','output':str(out),'source_files':len(actual),'pyc_files':len(final),'original_strip_returncode':None}))
