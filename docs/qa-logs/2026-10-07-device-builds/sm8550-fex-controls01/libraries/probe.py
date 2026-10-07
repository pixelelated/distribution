from pathlib import Path
import hashlib,json,os,shutil,subprocess,time

out=Path('/out')
j=json.loads((out/'inputs.json').read_text())
fex=Path(j['fex']);build=fex.parent.parent
armroot=build/'toolchain/aarch64-rocknix-linux-gnu/sysroot'
env=dict(os.environ)
env.update(PKG_CONFIG_SYSROOT_DIR=str(armroot),PKG_CONFIG_LIBDIR=str(armroot/'usr/lib/pkgconfig')+':'+str(armroot/'usr/share/pkgconfig'),PKG_CONFIG_PATH='',CCACHE_DISABLE='1')
env['PATH']=str(build/'toolchain/bin')+':'+env['PATH']
for key in list(env):
    if key.startswith(('NIX_CFLAGS','NIX_LDFLAGS','NIX_CXXSTDLIB','NIX_CXXFLAGS')):
        del env[key]
cmake=str(build/'toolchain/bin/cmake')
source=out/'source'
(source/'ThunkLibs/GuestLibs').mkdir(parents=True)
for p in (fex/'ThunkLibs').iterdir():
    if p.name!='GuestLibs':
        (source/'ThunkLibs'/p.name).symlink_to(p,target_is_directory=p.is_dir())
shutil.copyfile(fex/'ThunkLibs/GuestLibs/CMakeLists.txt',source/'ThunkLibs/GuestLibs/CMakeLists.txt')
patch=out/'fix.patch'
subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(patch)],cwd=source,check=True)
records=[]
for label,bits,src in [('original32',32,fex/'ThunkLibs/GuestLibs'),('fixed32',32,source/'ThunkLibs/GuestLibs'),('fixed64',64,source/'ThunkLibs/GuestLibs')]:
    work=out/label
    toolchain=j['toolchain32'] if bits==32 else j['toolchain64']
    configure=[cmake,'-GNinja','-S',str(src),'-B',str(work),f'-DBITNESS={bits}',
        '-DCMAKE_BUILD_TYPE=RELEASE','-DBUILD_FEX_LINUX_TESTS=OFF','-DENABLE_CLANG_THUNKS=ON',
        '-DCMAKE_TOOLCHAIN_FILE:FILEPATH='+toolchain,'-DCMAKE_INSTALL_PREFIX=/usr',
        '-DFEX_PROJECT_SOURCE_DIR='+str(fex),'-DGENERATOR_EXE='+str(build/'toolchain/usr/bin/thunkgen'),
        '-DX86_DEV_ROOTFS='+j['expected_rootfs'],'-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY']
    with (out/(label+'-configure.log')).open('w') as log:
        p=subprocess.run(configure,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
    assert p.returncode==0,(label,'configure')
    commands=subprocess.check_output(['ninja','-C',str(work),'-t','commands'],env=env,text=True)
    (out/(label+'-commands.txt')).write_text(commands)
    contaminated=('-I'+str(armroot/'usr/include')+' ') in commands
    assert contaminated==(label=='original32'),(label,'include path',contaminated)
    with (out/(label+'-build.log')).open('w') as log:
        p=subprocess.run(['ninja','-C',str(work),'-j2'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900)
    output=(out/(label+'-build.log')).read_text()
    if label=='original32':
        assert p.returncode!=0 and "size of '__builtin_bit_cast'" in output,(label,'expected original failure')
        records.append({'case':label,'exit':p.returncode,'expected_failure':True,'arm64_system_include':contaminated})
    else:
        assert p.returncode==0,(label,'build')
        libs=sorted(work.glob('*.so'))
        assert len(libs)>3,(label,len(libs))
        files={}
        for lib in libs:
            header=subprocess.check_output(['readelf','-h',str(lib)],text=True)
            assert ('ELF32' if bits==32 else 'ELF64') in header
            assert ('Intel 80386' if bits==32 else 'Advanced Micro Devices X86-64') in header
            files[lib.name]={'sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'bytes':lib.stat().st_size,'bits':bits}
        records.append({'case':label,'exit':p.returncode,'arm64_system_include':contaminated,'libraries':files})
    print(json.dumps(records[-1]),flush=True)
    (out/'partial-results.json').write_text(json.dumps(records,indent=2)+'\n')
(out/'control-result.json').write_text(json.dumps({'result':'PASS','records':records,'scope':'actual guest CMake generation and complete32/64-bit guest library compile/link; full aarch64 package/firmware remains'},indent=2)+'\n')
