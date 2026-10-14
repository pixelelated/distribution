#!/usr/bin/env python3
"""UNRUN. readelf inventory + bounded public bundle; never runs target or loader."""
import argparse
from pathlib import Path
import re
import shutil
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import command, read, require, safe_member, sha, verify_packet, write
from loader_resolution import resolve_interpreter

MAX_BYTES=512*1024**2


def library_name(name):
    require(re.fullmatch('[A-Za-z0-9_+.-]+',name) and name not in ('.','..'),'unsafe library name')
    return name


def metadata(header,text,program):
    require(len(header)==64 and header[:7]==b'\x7fELF\x02\x01\x01'
            and struct.unpack_from('<H',header,18)[0]==62,'not target ELF64 little-endian x86_64')
    kind=struct.unpack_from('<H',header,16)[0]
    require(kind in ((2,3) if program else (3,)),'unsupported ELF type')
    require(not any('('+tag+')' in text for tag in ('FILTER','AUXILIARY','AUDIT','DEPAUDIT','CONFIG')),
            'unsupported loader indirection')
    needed=re.findall(r'\(NEEDED\).*?\[([^\]]+)\]',text)
    require(len(needed)==len(set(needed)) and text.count('(NEEDED)')==len(needed),'duplicate/unparsed DT_NEEDED')
    for name in needed:library_name(name)
    interpreters=re.findall(r'Requesting program interpreter: ([^\]]+)\]',text)
    require((not program or len(interpreters)==1) and len(interpreters)<=1,
            'unexpected interpreter count')
    require(text.count('Requesting program interpreter:')==len(interpreters),'unparsed interpreter')
    if interpreters:
        path=Path(interpreters[0])
        require(path.is_absolute() and '..' not in path.parts and str(path)==interpreters[0], 'unsafe interpreter')
        library_name(path.name)
    paths={}
    for tag in ('RUNPATH','RPATH','SONAME'):
        values=re.findall(r'\('+tag+r'\).*?\[([^\]]*)\]',text)
        require(text.count('('+tag+')')==len(values) and len(values)<=1,'unparsed/duplicate '+tag)
        paths[tag.lower()]=values[0] if values else None
    if paths['soname'] is not None:library_name(paths['soname'])
    # Preserve raw readelf output as well as parsing version-name requirements.
    definitions=set();requirements={};section=None;current=None
    for line in text.splitlines():
        if line.startswith('Version definition section '):section='definitions';current=None
        elif line.startswith('Version needs section '):section='needs';current=None
        elif line.startswith('Version symbols section '):section=None;current=None
        elif section=='definitions':
            match=re.search(r'\bName: (\S+)',line)
            if match:definitions.add(match[1])
        elif section=='needs':
            match=re.search(r'\bFile: (\S+)\s+Cnt: (\d+)',line)
            if match:
                current=library_name(match[1]);require(current not in requirements,'duplicate version-needed file')
                requirements[current]={'count':int(match[2]),'names':[]}
            else:
                match=re.search(r'\bName: (\S+)',line)
                if match:
                    require(current is not None,'version name without provider')
                    requirements[current]['names'].append(match[1])
    for name,row in requirements.items():
        require(name in needed and len(row['names'])==row['count'] and len(set(row['names']))==row['count'],
                'unparsed/duplicate version needs or non-DT_NEEDED provider')
    return {'needed':needed,'interpreter':interpreters[0] if interpreters else None,**paths,
            'version_definitions':sorted(definitions),'version_needs':requirements}


def resolve_library(name,search,tc):
    library_name(name);found={};aliases={}
    for directory in search:
        candidate=directory/name
        if not candidate.exists() and not candidate.is_symlink():continue
        real=candidate.resolve(strict=True)
        require(real.is_file() and real.is_relative_to(tc),'library escaped retained toolchain')
        found[str(real)]=sha(real);aliases[str(candidate)]=str(real)
    require(found and len(set(found.values()))==1,'missing/ambiguous retained dependency: '+name)
    selected=sorted(found)[0]
    return Path(selected),{'candidates':found,'aliases':aliases,'selected':selected}


def version_contract(objects):
    checked=[]
    for name,row in objects.items():
        for provider,required in row['version_needs'].items():
            require(provider in objects,'missing version provider: '+provider)
            missing=set(required['names'])-set(objects[provider]['version_definitions'])
            require(not missing,'version definitions absent: '+name+' -> '+provider+' '+','.join(sorted(missing)))
            checked.append({'consumer':name,'provider':provider,'names':required['names']})
    return checked


def pinned_libraries(binding,extra,tc):
    """Use sealed plan inputs plus the already observed retained C/C++ runtime."""
    physical=Path(binding['toolchain']['physical_root']);expected={}
    def visit(row):
        if isinstance(row,dict):
            if 'path' in row and 'sha256' in row:
                path=Path(row['path'])
                require(path.is_relative_to(physical),'sealed input outside retained toolchain')
                expected[str(tc/path.relative_to(physical))]={'sha256':row['sha256'],'bytes':row['bytes']}
            for child in row.values():visit(child)
        elif isinstance(row,list):
            for child in row:visit(child)
    visit(binding['toolchain'])
    for name,row in extra['retained_runtime'].items():
        path=str(tc/safe_member(name))
        require(path not in expected or expected[path]==row,'conflicting retained runtime binding')
        expected[path]=row
    return expected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path('/plan/input-bindings.json'))
    parser.add_argument('--work',type=Path,default=Path('/work/format-tools'))
    parser.add_argument('--build-records',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();here=Path(__file__).resolve().parent
    verify_packet(here);extra=read(here/'bindings.json')
    require(sha(args.plan)==extra['sealed_input_sha256'],'sealed owner03 OSD-corrected input binding changed')
    binding=read(args.plan);work=args.work;build=args.build_records;records=args.output
    tc=Path(binding['toolchain']['required_container_root']);sysroot=tc/'x86_64-rocknix-linux-gnu/sysroot'
    for path in (work,build,records,tc):
        require(path.is_absolute() and path.resolve()==path,'real absolute input/output path required')
    require(not records.exists() and not any(records.is_relative_to(p) or p.is_relative_to(records)
            for p in (work,build,tc,here)),'fresh output must be separate from read-only inputs')
    records.mkdir()
    build_files=[build/'target-artifact.json',build/'selected-stage.json',build/'container-result.json',
                 build/'generated-after.json',work/'source-inventory.json',args.plan]
    build_hashes={str(path):sha(path) for path in build_files}
    expected=read(build/'target-artifact.json');child=read(build/'selected-stage.json')
    result=read(build/'container-result.json');inventory=read(work/'source-inventory.json')
    require(result['stage']=='chdman-build' and result['status']=='PASS'
            and result['source_before']==result['source_after'] and result['sampler_exited']
            and not result['monitor_errors'],'original build/source/resource contract did not pass')
    require(result['children']==[child] and child['label']=='selected-stage'
            and child['argv']==['bash','/plan/build-stage.sh','chdman-build']
            and child['original_exit']==0 and child['reaped'] and not child.get('forced_group_stop'),
            'original selected build child did not pass')
    require(inventory['family']=='chdman' and inventory['archive_sha256']==binding['chdman']['archive']['sha256']
            and result['source_after']['inventory_sha256']==sha(work/'source-inventory.json'),
            'build source inventory binding changed')
    # Bind both source-only adjustments to this successful build and actual scratch bytes.
    for plan_key,inventory_key,receipt_key in (
            ('private_source_adjustment','adjustment','one_documented_link_policy_patch'),
            ('private_osd_adjustment','osd_adjustment','documented_osd_selection_patch')):
        patch=binding['chdman'][plan_key];row=inventory['files'][patch['file']]
        path=work/safe_member(binding['chdman']['archive_root'])/safe_member(patch['file'])
        require(inventory[inventory_key]==patch and result['source_after'][receipt_key]==patch['file']
                and row['sha256']==patch['after_sha256'] and path.resolve()==path and path.is_file()
                and path.stat().st_size==row['bytes'] and path.stat().st_mode&0o7777==row['mode']
                and sha(path)==patch['after_sha256'],'owner03 patch receipt/actual source differs')
        build_hashes[str(path)]=patch['after_sha256']
    binary=work/safe_member(binding['chdman']['archive_root'])/'chdman'
    require(expected['path']==str(binary) and binary.resolve()==binary and binary.is_file()
            and sha(binary)==expected['sha256'] and 0<binary.stat().st_size==expected['bytes']<=256*1024**2,
            'actual target differs from post-build receipt')
    generated=read(build/'generated-after.json')
    require(generated==result['generated_after'] and generated['chdman']['sha256']==expected['sha256']
            and generated['chdman']['bytes']==expected['bytes'],'post-build generated target differs')
    readelf=tc/safe_member(extra['readelf']['relative_path'])
    require(readelf.resolve()==readelf and sha(readelf)==extra['readelf']['sha256'],'readelf changed/aliased')
    pinned=pinned_libraries(binding,extra,tc)
    search=[sysroot/'lib',sysroot/'usr/lib',sysroot/'lib64',sysroot/'usr/lib64',tc/'x86_64-rocknix-linux-gnu/lib']
    resolutions={};objects={};queue=[('@program',binary)];total=0;interpreter=None;program_loader=None
    loader_binding=read(here/'loader-binding.json')
    canonical=loader_binding['canonical']
    pinned[str(tc/safe_member(canonical['relative_to_toolchain']))]={k:canonical[k] for k in ('sha256','bytes')}
    while queue:
        name,path=queue.pop(0)
        if name in objects:
            require(sha(path)==objects[name]['sha256'],'same library name resolved to different bytes');continue
        size=path.stat().st_size;total+=size
        require(len(objects)<128 and 0<size<=256*1024**2 and total<=MAX_BYTES,'ELF closure budget exceeded')
        before=sha(path)
        if name!='@program':
            require(pinned.get(str(path))=={'bytes':size,'sha256':before},'dependency lacks exact retained byte binding')
        with path.open('rb') as stream:header=stream.read(64)
        label='elf-'+str(len(objects))
        code,out,err=command(records/label,[readelf,'--wide','--file-header','--program-headers','--dynamic','--version-info','--notes',path],30,
                             env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C'})
        require(code==0 and not err,'original readelf failure/diagnostic')
        details=metadata(header,out.decode('utf-8'),name=='@program')
        require(sha(path)==before,'ELF changed while inspected')
        if name=='@program':interpreter=details['interpreter']
        if details['interpreter']:
            loader,resolution=resolve_interpreter(details['interpreter'],sysroot,tc,loader_binding)
            if name=='@program':program_loader=loader
            require(loader==program_loader,'library interpreter resolves to different loader')
            details['interpreter_resolution']=resolution
            queue.append((loader.name,loader))
        if name!='@program':require(details['soname'] in (None,name),'dependency basename and SONAME disagree')
        objects[name]={'source':str(path),'bytes':size,'sha256':before,**details,
                       'readelf_receipt':label+'.json','readelf_stdout_sha256':sha(records/(label+'.stdout'))}
        for needed in details['needed']:
            selected,receipt=resolve_library(needed,search,tc);resolutions[needed]=receipt
            queue.append((needed,selected))
    versions=version_contract(objects)
    bundle=records/'vm20-bundle';bundle.mkdir();members={};bundle_bytes=0
    loader_name=Path(interpreter).name
    require(loader_name!='chdman','loader/program filename collision')
    for name,row in objects.items():
        destination='chdman' if name=='@program' else name if name==loader_name else 'lib/'+name
        path=Path(row['source']);target=bundle/safe_member(destination)
        require(destination not in members and path.is_file() and path.resolve()==path,'duplicate/linked bundle input')
        require(path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'bundle input changed')
        bundle_bytes+=row['bytes'];require(bundle_bytes<=MAX_BYTES,'512MiB closure bundle ceiling')
        target.parent.mkdir(parents=True,exist_ok=True)
        with path.open('rb') as source_stream,target.open('xb') as dest:shutil.copyfileobj(source_stream,dest,1024*1024)
        require(sha(target)==row['sha256'],'bundle copy mismatch');target.chmod(0o755)
        members[destination]={'sha256':row['sha256'],'bytes':row['bytes'],'mode':0o755,'source':str(path)}
    for name,receipt in resolutions.items():
        require(resolve_library(name,search,tc)[1]==receipt,'retained library bytes/aliases changed')
    require(resolve_interpreter(interpreter,sysroot,tc,loader_binding)[0]==program_loader,'retained loader changed')
    require(all(sha(Path(row['source']))==row['sha256'] for row in objects.values()),'ELF inputs changed')
    require(sha(readelf)==extra['readelf']['sha256'] and all(sha(Path(p))==h for p,h in build_hashes.items()),
            'readelf or original build receipts changed')
    closure={'status':'STATIC_CLOSURE_ONLY','objects':objects,'library_resolution':resolutions,'version_name_checks':versions,
             'total_elf_bytes':total,'build_receipt_hashes':build_hashes,'expected_binary':expected,
             'source_commit':binding['chdman']['commit'],'loader_binding_sha256':sha(here/'loader-binding.json'),
             'readelf_sha256':sha(readelf),'runner_manifest_sha256':sha(here/'SHA256SUMS'),
             'limitations':'Flat explicit candidate set, not ld.so search emulation. Raw RPATH/RUNPATH and version-info retained. Version names checked, not individual symbols/relocations. No dlopen/NSS/IFUNC/kernel/CPU, target loading/help or format execution proof. No Sys assets. Build admission/cleanup acceptance remains coordinator-owned.'}
    write(records/'elf-closure.json',closure)
    write(bundle/'manifest.json',{'schema':1,'status':'STAGED_NOT_EXECUTED','files':members,'bytes':bundle_bytes,
          'loader':loader_name,'program':'chdman','closure_sha256':sha(records/'elf-closure.json'),'expected_binary':expected,
          'source_commit':binding['chdman']['commit'],'runner_manifest_sha256':sha(here/'SHA256SUMS')})
    write(records/'bundle-receipt.json',{'path':str(bundle),'manifest_sha256':sha(bundle/'manifest.json'),
                                      'files':len(members),'bytes':bundle_bytes,'target_executed':False})


if __name__=='__main__':main()
