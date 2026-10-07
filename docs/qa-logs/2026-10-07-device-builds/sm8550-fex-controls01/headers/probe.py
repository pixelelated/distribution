from pathlib import Path
import datetime,json,os,subprocess
j=json.loads(Path('/out/inputs.json').read_text())
assert os.environ['ROOTFS']==j['expected_rootfs'], (os.environ.get('ROOTFS'),j['expected_rootfs'])
records=[]
for number,original in enumerate(j['commands']):
    compiler=original[0]
    assert Path(compiler).is_file(),compiler
    for label,args in [('original',original),('without-arm64-root',[v for v in original if v!='-I'+j['aarch64_include']])]:
        assert len(original)-len(args)==(label!='original')
        command=[*args,'-H']
        p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd=Path(j['fex'])/'.aarch64-rocknix-linux-gnu/Guest_32',timeout=180)
        Path(f'/out/{number}-{label}.log').write_text(p.stdout)
        records.append({'source':original[-1],'case':label,'command':command,'exit':p.returncode,
            'arm64_floatn_included':j['aarch64_include']+'/bits/floatn.h' in p.stdout,
            'bit_cast_error':"size of '__builtin_bit_cast'" in p.stdout})
        print(json.dumps({k:v for k,v in records[-1].items() if k!='command'}),flush=True)
        if label=='original':
            assert p.returncode!=0 and records[-1]['bit_cast_error'] and records[-1]['arm64_floatn_included']
        else:
            assert p.returncode==0 and not records[-1]['arm64_floatn_included']
result={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rootfs':os.environ['ROOTFS'],'records':records,
        'scope':'two exact failed i686 translation units, syntax controls only; full package/build verification remains'}
Path('/out/control-result.json').write_text(json.dumps(result,indent=2)+'\n')
