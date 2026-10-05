from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile
root=Path(tempfile.mkdtemp(prefix='pixelelated-445-control-'));owner=root/'owner';owner.mkdir(mode=0o700);helper=owner/'prepare-dirs.py';shutil.copyfile('/tmp/pixelelated-prepare-owned-dirs.py',helper)
command=['ssh-keygen','-q','-t','ed25519','-N','','-f',str(owner/'pair/qa-key'),'-C','disposable-control']
first=subprocess.run(command,capture_output=True);assert first.returncode!=0 and not (owner/'pair/qa-key').exists()
subprocess.run(['python3','-I',str(helper)],check=True,capture_output=True)
good=subprocess.run(command,capture_output=True);assert good.returncode==0
assert (owner/'pair/qa-key').stat().st_mode&0o777==0o600
assert all((owner/n).stat().st_mode&0o777==0o700 for n in ['pair','artifacts'])
subprocess.run(['python3','-I',str(helper)],check=True,capture_output=True)
bad=root/'bad';bad.mkdir(mode=0o700);shutil.copyfile(helper,bad/'prepare-dirs.py');outside=root/'outside';outside.mkdir(mode=0o700);(bad/'pair').symlink_to(outside,target_is_directory=True)
refused=subprocess.run(['python3','-I',str(bad/'prepare-dirs.py')],capture_output=True);assert refused.returncode!=0 and not list(outside.iterdir())
result={'passed':True,'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'missing_directory_keygen_rc':first.returncode,'prepared_keygen_rc':good.returncode,'key_mode':'0600','directories_mode':'0700','repeat_setup_rc':0,'symlink_refusal_rc':refused.returncode,'outside_unchanged':True,'keys_retained':False}
shutil.rmtree(root);Path('/tmp/pixelelated-445-directory-controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
