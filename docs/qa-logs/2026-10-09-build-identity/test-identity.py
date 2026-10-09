#!/usr/bin/env python3
"""Host controls for #530; only disposable fixtures, no release/device actions."""
import hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[3]
OUT=Path(os.environ['PROOF_OUT']); OUT.mkdir(parents=True,exist_ok=True)
results=[]
def run(args,**kw):
    return subprocess.run(args,check=True,text=True,capture_output=True,**kw)
def ok(name): results.append(name); print('PASS '+name,flush=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='pix530-host-') as tmp:
    t=Path(tmp);repo=t/'repo';repo.mkdir();(repo/'config').mkdir()
    shutil.copyfile(R/'config/build-identity',repo/'config/build-identity')
    run(['git','init','-q',str(repo)])
    run(['git','-C',str(repo),'add','.'])
    run(['git','-C',str(repo),'-c','user.name=QA','-c','user.email=qa@example.invalid','commit','-qm','Synthetic fixture'])
    commit=run(['git','-C',str(repo),'rev-parse','HEAD']).stdout.strip()
    def derive(**changes):
        env=os.environ.copy();env.update(OS_VERSION='0.0.1',BUILD_TIMESTAMP='20261009T180000Z');env.update(changes)
        cmd='. config/build-identity; pixelelated_build_identity || exit $?; python3 -c \'import os,json;print(json.dumps({k:os.environ[k] for k in ("RELEASE_VERSION","BUILD_VERSION","BUILD_DATE","BUILD_TIMESTAMP","BUILD_DIRTY","GIT_HASH","OS_BUILD")}))\''
        return subprocess.run(['bash','-c',cmd],cwd=repo,env=env,text=True,capture_output=True)
    first=derive(); assert first.returncode==0,first.stderr;a=json.loads(first.stdout)
    assert a['BUILD_VERSION']==f'0.0.1-dev+20261009T180000Z.g{commit[:12]}' and a['BUILD_DIRTY']=='no';ok('default semantic identity')
    b=json.loads(derive(BUILD_TIMESTAMP='20261009T180001Z').stdout);assert a['BUILD_VERSION']!=b['BUILD_VERSION'];ok('same source next second has distinct identity')
    for q in ('alpha.1','beta.2','rc.3',''):
        d=json.loads(derive(BUILD_QUALIFIER=q).stdout);assert d['RELEASE_VERSION']=='0.0.1'+('-'+q if q else '');ok('explicit qualifier '+(q or 'stable'))
    for changes in ({'OS_VERSION':'01.0.1'},{'BUILD_QUALIFIER':'rc.01'},{'BUILD_QUALIFIER':'bad/'},{'BUILD_TIMESTAMP':'20260230T120000Z'},{'BUILD_TIMESTAMP':'20261009T180000+00'},{'CUSTOM_VERSION':'bad'},{'CUSTOM_IMAGE_NAME':'wrong'},{'CUSTOM_GIT_HASH':'a'*40}):
        result=derive(**changes);assert result.returncode!=0,changes;ok('refuses '+repr(changes))
    (repo/'local-edit').write_text('fixture');assert json.loads(derive().stdout)['BUILD_VERSION'].endswith('.dirty');(repo/'local-edit').unlink();ok('dirty tree labelled explicitly')
    # Execute the actual image identity/naming block, not a rewritten naming model.
    image=(R/'scripts/image').read_text()
    block=image[image.index('# One identity'):image.index('# Setup fakeroot')]
    stage=t/'assembly';stage.mkdir()
    env=os.environ.copy();env.update(ROOT=str(repo),OS_VERSION='0.0.1',BUILD_TIMESTAMP='20261009T180000Z',DEVICE='H700',PROJECT='ROCKNIX',TARGET_ARCH='aarch64',DISTRONAME='pixelelated',IMAGE_SUFFIX='from-ROCKNIX',BUILD=str(stage),TARGET_IMG=str(stage))
    run(['git','-C',str(repo),'remote','add','origin','https://github.com/pixelelated/distribution.git'])
    got=run(['bash','-c','die(){ echo "$*" >&2;exit 1; }; show_config(){ :; };\n'+block+'\nprintf "%s\\n" "$IMAGE_NAME"'],cwd=repo,env=env).stdout.strip()
    assert got==f"pixelelated-H700.aarch64-{a['BUILD_VERSION']}-from-ROCKNIX";ok('actual image naming keeps adoption suffix and semantic identity')
    (stage/(got+'-DDR4.img.gz')).write_bytes(b'prior bytes')
    collision=subprocess.run(['bash','-c','die(){ echo "$*" >&2;exit 1; }; show_config(){ :; };\n'+block],cwd=repo,env=env,text=True,capture_output=True)
    assert collision.returncode!=0 and (stage/(got+'-DDR4.img.gz')).read_bytes()==b'prior bytes';ok('actual image assembly refuses reused identity without replacing bytes')
    # Execute the image's actual sidecar and os-release emitters with frozen identity.
    env.update(INSTALL=str(stage),HOME_URL='https://pixelelated.com',GIT_ORGANIZATION='pixelelated',GIT_REPO='distribution',ARCH='aarch64')
    (stage/'etc').mkdir()
    sidecar=image[image.index('# Record the identity'):image.index('# Create legacy sym links')]
    metadata=image[image.index('# Create /etc/os-release'):image.index('if [ -n "${HW_CPU}" ]')]
    derive_block=block[:block.index('# A frozen timestamp')]
    run(['bash','-c','die(){ exit 1; }; show_config(){ :; };\n'+derive_block+sidecar+metadata],cwd=repo,env=env)
    produced=json.loads((stage/(got+'.identity.json')).read_text())
    assert produced['build_version']==a['BUILD_VERSION'] and produced['build_commit']==commit
    fields=dict(line.split('=',1) for line in (stage/'etc/os-release').read_text().splitlines())
    assert fields['OS_VERSION']=='"0.0.1-dev"' and fields['BUILD_VERSION']=='"'+a['BUILD_VERSION']+'"'
    assert fields['PRETTY_NAME']=='"pixelelated 0.0.1-dev"' and fields['BUILD_DATE']=='"2026-10-09T18:00:00Z"'
    (OUT/'staged-identity.json').write_text(json.dumps(produced,indent=2)+'\n')
    (OUT/'staged-os-release.txt').write_text((stage/'etc/os-release').read_text())
    ok('actual sidecar and os-release emitters agree with frozen identity')
    # Run both recipe post_install hooks, compare actual generated defaults.
    package='projects/ROCKNIX/packages/rocknix/package.mk'
    old=t/'old-package.mk';old.write_text(run(['git','-C',str(R),'show','HEAD:'+package]).stdout)
    cfg=[]
    for label,recipe,extra in [('before',old,{'OS_BUILD':'community'}),('after',R/package,{'DEVELOPMENT_DEFAULTS':'yes'}),('opt-out',R/package,{'DEVELOPMENT_DEFAULTS':'no'})]:
        dest=t/label
        for d in ('etc','usr/lib/systemd/system','usr/config','usr/bin','usr/share'): (dest/d).mkdir(parents=True,exist_ok=True)
        shutil.copytree(R/'projects/ROCKNIX/packages/rocknix/config',dest/'usr/config',dirs_exist_ok=True)
        env=os.environ.copy();env.update(INSTALL=str(dest),PKG_DIR=str(R/'projects/ROCKNIX/packages/rocknix'),DEVICE='GENERIC_X64',TARGET_ARCH='x86_64',OS_VERSION='0.0.1',RELEASE_VERSION=a['RELEASE_VERSION'],BUILD_VERSION=a['BUILD_VERSION'],BUILD_DATE=a['BUILD_DATE']);env.update(extra)
        run(['bash','-e','-c','enable_service(){ :; }; . "$1"; post_install','test',str(recipe)],env=env)
        cfg.append((dest/'usr/config/system/configs/system.cfg').read_bytes())
        if label=='after':
            banner=(dest/'etc/issue').read_text();assert 'community' not in banner and a['BUILD_VERSION'] in banner
            (OUT/'staged-banner.txt').write_text(banner)
    assert cfg[0]==cfg[1];ok('actual post_install retains all fresh-install defaults')
    assert cfg[2]!=cfg[1];ok('fresh-install defaults independently configurable')
    # Genuine candidate store format and actual plan command, including negative controls.
    inputs={'distribution_commit':commit}
    base=got
    identity={'schema':1,'name':'pixelelated','release_version':a['RELEASE_VERSION'],'build_version':a['BUILD_VERSION'],'build_timestamp':a['BUILD_TIMESTAMP'],'build_commit':commit,'dirty':'no','device':'H700','arch':'aarch64','image_name':base}
    def bundle(identity, mutate=None):
        staging=t/'bundle-staging';staging.mkdir()
        (staging/(base+'.identity.json')).write_text(json.dumps(identity))
        img=base+'-DDR4.img.gz';(staging/img).write_bytes(b'SYNTHETIC FIRMWARE ONLY')
        (staging/(img+'.sha256')).write_text(sha(staging/img)+'  '+img+'\n')
        if mutate:mutate(staging)
        data={'schema':1,'inputs':inputs,'files':{f.name:{'sha256':sha(f),'bytes':f.stat().st_size} for f in staging.iterdir()}}
        mf=staging/'manifest.json';mf.write_text(json.dumps(data,sort_keys=True))
        dest=t/sha(mf)
        if dest.exists():shutil.rmtree(dest)
        staging.rename(dest);return dest
    def plan(b):return subprocess.run([str(R/'tools/fork-publish-release'),'--prepare',str(b)],text=True,capture_output=True)
    good=bundle(identity);result=plan(good);assert result.returncode==0,result.stderr
    data=json.loads(result.stdout);assert data['tag']=='v'+a['BUILD_VERSION'] and data['target_commitish']==commit and data['draft'] and not data['publication_performed'];(OUT/'release-plan-fixture.json').write_text(result.stdout);ok('manifest-bound draft GitHub naming without publication')
    for key,value in [('dirty','yes'),('build_commit','a'*40),('build_version','0.0.1'),('image_name','wrong')]:
        bad=dict(identity);bad[key]=value;assert plan(bundle(bad)).returncode!=0;ok('release preparation refuses '+key+' mismatch')
    assert plan(bundle(identity,lambda d:next(d.glob('*.sha256')).write_text('wrong\n'))).returncode!=0;ok('release preparation refuses checksum disagreement')
    assert plan(bundle(identity,lambda d:(d/'unrelated.tar').write_bytes(b'x'))).returncode!=0;ok('release preparation refuses unbound firmware')
    bad=bundle(identity);next(bad.glob('*.img.gz')).write_bytes(b'TAMPER');assert plan(bad).returncode!=0;ok('release preparation refuses modified manifest bytes')
    assert subprocess.run([str(R/'tools/fork-publish-release'),'H700','stable'],capture_output=True).returncode!=0;ok('legacy implicit publication refused')
(OUT/'host-results.json').write_text(json.dumps({'passed':len(results),'controls':results,'synthetic_fixtures':True},indent=2)+'\n')
