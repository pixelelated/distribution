from pathlib import Path
import os,subprocess,json,hashlib,signal
p=Path(__file__).resolve().parent;r=Path.cwd();source=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20')
manifest=json.loads((p/'source-manifest.json').read_text())
for f,h in manifest.items():assert hashlib.sha256((r/f).read_bytes()).hexdigest()==h
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()=='1a026648442321609b2288c2c9c06803817f9df2'
env={**os.environ,'TMPDIR':str(p/'tmp'),'LAST_GOOD_SOURCE_ROOT':str(source),'QA_SYSTEM_ROOT':'/workspace/tmp/pixelelated-m7-image20/root','RETROARCH_SRC':str(source/'build.pixelelated-GENERIC_X64.x86_64'),'ES_SRC':'/home/max/Development/emulationstation-next.worktrees/qa-integration','PYTHONDONTWRITEBYTECODE':'1','PATH':'/workspace/tmp/pixelelated-m7-qa20/bin:'+os.environ['PATH']}
rows=[]
def test(name,args,expected=0,changes=None,input=None,timeout=30):
 q=subprocess.run(args,env={**env,**(changes or {})},input=input,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 (p/(name+'.log')).write_text(q.stdout)
 assert (q.returncode==0)==(expected==0),(name,q.returncode,q.stdout[-1500:])
 rows.append({'case':name,'returncode':q.returncode,'expected_success':expected==0})
 print('PASS',name,q.returncode,flush=True)
 (p/'controls.json').write_text(json.dumps(rows,indent=2)+'\n')
(p/'blocked').write_text('not a directory\n')
(p/'test.c').write_text('int main(void) { return 0; }\n')
for name,tmp,want in [('unusable',p/'blocked',1),('owned',p/'tmp',0)]:
 test('compiler-'+name,['cc','-o',str(p/('test-'+name)),str(p/'test.c')],want,{'TMPDIR':str(tmp)})
 d=p/('patch-'+name);d.mkdir();(d/'sample').write_text('before\n')
 patch='--- a/sample\n+++ b/sample\n@@ -1 +1 @@\n-before\n+after\n'
 test('patch-'+name,['patch','-d',str(d),'-p1','--dry-run'],want,{'TMPDIR':str(tmp)},patch)
bwrap=['bwrap','--die-with-parent','--tmpfs','/','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--dev','/dev','--proc','/proc','--tmpfs','/tmp']
test('namespace-host-path-refused',bwrap+['bash','-c','mktemp'],1)
test('namespace-private-tmp',bwrap+['--unsetenv','TMPDIR','bash','-c','x=$(mktemp) && test -f "$x" && rm "$x"'])
test('readiness-current',['python3',str(r/'tools/vm-upgrade-readiness-test'),'--rehearsal',str(source/'tools/vm-upgrade-rehearsal')])
text=(source/'tools/vm-upgrade-rehearsal').read_text()
for name,old,new in [('ignore-boot','[ "$observed" = "$expected_boot active" ]','[[ "$observed" = *" active" ]]'),('ignore-unit','[ "$observed" = "$expected_boot active" ]','[[ "$observed" = "$expected_boot "* ]]'),('wrong-query','systemctl is-active rocknix-autostart.service','systemctl is-active wrong.service')]:
 assert text.count(old)==1
 f=p/(name+'.sh');f.write_text(text.replace(old,new))
 test('readiness-reject-'+name,['python3',str(r/'tools/vm-upgrade-readiness-test'),'--rehearsal',str(f)],1)
signal.signal(signal.SIGINT,signal.SIG_DFL);signal.signal(signal.SIGPIPE,signal.SIG_DFL)
print('START full frozen-source regression',flush=True)
with (p/'regression.log').open('w') as f:
 q=subprocess.run([str(r/'tools/last-good-scripts-test')],env=env,stdout=f,stderr=subprocess.STDOUT)
(p/'regression.rc').write_text(str(q.returncode)+'\n')
for f,h in manifest.items():assert hashlib.sha256((r/f).read_bytes()).hexdigest()==h
text=(p/'regression.log').read_text(errors='replace')
result={'result':'PASS' if q.returncode==0 else 'FAIL','returncode':q.returncode,'passes':sum(x.lstrip().startswith('PASS ') for x in text.splitlines()),'failures':sum(x.lstrip().startswith('FAIL ') for x in text.splitlines()),'skips':sum(x.lstrip().startswith('SKIP ') for x in text.splitlines()),'source':'1a026648442321609b2288c2c9c06803817f9df2','tool_sha256':manifest}
(p/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
raise SystemExit(q.returncode)
