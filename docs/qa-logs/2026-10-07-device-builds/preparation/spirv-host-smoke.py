from pathlib import Path
import datetime,hashlib,json,subprocess
owner=Path(__file__).resolve().parent
def digest(path):
    result=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(4*1024*1024),b''):
            result.update(chunk)
    return result.hexdigest()
data=json.loads((owner/'inputs.json').read_text());root=Path(data['host_worktree'])/data['build_root']
out=owner/'artifacts/spirv-host';out.mkdir()
assert (root/'.stamps/spirv-tools/build_host').is_file()
build=next((root/'build').glob('spirv-tools-*'))/'.x86_64-linux-gnu'
cache=(build/'CMakeCache.txt').read_text()
assert 'SPIRV_WERROR:BOOL=ON' in cache
compile=json.loads((build/'compile_commands.json').read_text())
commands=[r['command'] for r in compile if r['file'].endswith('/source/val/validate_decorations.cpp')]
assert commands and all('-Wno-error=free-nonheap-object' in c and '-Werror' in c for c in commands)
(out/'compile-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
module='''OpCapability Shader
OpMemoryModel Logical GLSL450
OpEntryPoint GLCompute %main "main" %buffer
OpExecutionMode %main LocalSize 1 1 1
OpDecorate %outer Block
OpMemberDecorate %inner 0 Offset 0
OpMemberDecorate %outer 0 Offset 0
OpDecorate %buffer DescriptorSet 0
OpDecorate %buffer Binding 0
%void = OpTypeVoid
%function = OpTypeFunction %void
%uint = OpTypeInt 32 0
%inner = OpTypeStruct %uint
%outer = OpTypeStruct %inner
%pointer = OpTypePointer StorageBuffer %outer
%buffer = OpVariable %pointer StorageBuffer
%main = OpFunction %void None %function
%entry = OpLabel
OpReturn
OpFunctionEnd
'''
(out/'valid.spvasm').write_text(module)
(out/'invalid.spvasm').write_text(module.replace('OpMemberDecorate %inner 0 Offset 0\n',''))
results=[]
def run(name,tool,args,expected=0):
    cmd=[str(root/'toolchain/bin'/tool),*map(str,args)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    (out/(name+'.log')).write_text(r.stdout+r.stderr)
    assert (r.returncode==0)==(expected==0),(name,r.returncode,r.stderr)
    results.append({'case':name,'command':cmd,'returncode':r.returncode})
    return r
for name in ['valid','invalid']:
    run(name+'-assemble','spirv-as',['--target-env','vulkan1.2',out/(name+'.spvasm'),'-o',out/(name+'.spv')])
run('valid-validate','spirv-val',['--target-env','vulkan1.2',out/'valid.spv'])
r=run('invalid-layout-rejected','spirv-val',['--target-env','vulkan1.2',out/'invalid.spv'],1)
assert 'Offset' in r.stderr or 'explicit layout' in r.stderr
run('disassemble','spirv-dis',[out/'valid.spv','-o',out/'roundtrip.spvasm'])
run('reassemble','spirv-as',['--target-env','vulkan1.2',out/'roundtrip.spvasm','-o',out/'roundtrip.spv'])
run('roundtrip-validate','spirv-val',['--target-env','vulkan1.2',out/'roundtrip.spv'])
run('optimize','spirv-opt',['--target-env=vulkan1.2','-O',out/'valid.spv','-o',out/'optimized.spv'])
run('optimized-validate','spirv-val',['--target-env','vulkan1.2',out/'optimized.spv'])
hashes={str(p.relative_to(root)):digest(p) for p in [root/'.stamps/spirv-tools/build_host',*[root/'toolchain/bin'/n for n in ['spirv-as','spirv-val','spirv-dis','spirv-opt']]]}
payload={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','scope':'installed host package, nested struct layout acceptance/rejection and tool roundtrips','checks':results,'hashes':hashes}
(out/'result.json').write_text(json.dumps(payload,indent=2)+'\n');print('PASS installed SPIRV host package and nine shader controls',flush=True)
