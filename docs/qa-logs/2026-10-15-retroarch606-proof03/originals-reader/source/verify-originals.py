#!/usr/bin/env python3
"""#606 exact completed03 originals reader. No VM, guest, archive or payload execution."""
import argparse,base64,hashlib,json,os,re,resource,signal,stat,struct,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
out=args.output.absolute();assert out.parent==Path('/tmp') and out.name.startswith('pix-m7-retroarch606-originals-result-') and not out.exists()
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(2*1024**2,2*1024**2));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def expire(*_):raise TimeoutError('30-second originals-only reader bound')
signal.signal(signal.SIGALRM,expire);signal.alarm(30)
started=time.monotonic();read_bytes=0;cache={};result={'status':'FAIL','producer_original_result_unchanged':True}
def require(ok,message):
 if not ok:raise AssertionError(message)
def read(path,limit=8*1024**2):
 global read_bytes
 path=Path(path);require(path.is_absolute(),'absolute original locator');require(not any(q.is_symlink() for q in [path,*path.parents]),'original link refused')
 s=path.stat();require(stat.S_ISREG(s.st_mode) and 0<=s.st_size<=limit,'selected input size/type')
 with path.open('rb') as f:b=f.read(limit+1)
 a=path.stat();require(len(b)==s.st_size and (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns),'original changed')
 read_bytes+=len(b);require(read_bytes<=64*1024**2,'64MiB total original read bound');return b
def sha(b):return hashlib.sha256(b).hexdigest()
def decoded(row):
 b=base64.b64decode(row['bytes_b64'],validate=True);require(len(b)==row['bytes'] and sha(b)==row['sha256'],'embedded original bytes');return b
def j(name):return json.loads(cache['owner/'+name])
def identity(row):
 raw=row['stat'];parts=raw.rsplit(')',1)[1].split();require(int(raw.split(' ',1)[0])==row['pid'] and int(parts[19])==row['start_ticks'] and int(parts[1])==row['ppid'] and parts[0]==row['state'],'raw proc stat identity');return row['pid'],row['start_ticks']
def live(rows):return [r for r in rows if Path(r['exe']).name in ['retroarch','retroarch32']]
def runemu(rows):return [r for r in rows if '/usr/bin/runemu.sh' in r['argv']]
def state_map(report):
 rows=report['observation']['states'];require(len(rows)==7,'exact selected state inventory');out={Path(x['path']).name:x for x in rows};require(len(out)==7,'unique state names')
 for r in rows:
  if r.get('exists') and 'bytes_b64' in r:decoded(r)
 return out
try:
 B=json.loads(read(HERE/'bindings.json'));O=Path(B['owner']);RUN=Path(B['run']);refs={}
 for key,row in B['refs'].items():
  b=read(row['path']);require(len(b)==row['bytes'] and sha(b)==row['sha256'],'exact reference:'+key);refs[key]=b
 require(sha(refs['source-seal'])=='a7e679583a560db680b4371da9d615aca38617dccd6d09854a8c8dc1454c0d24','source03 seal')
 manifest=json.loads(refs['original-records.json']);require(len(manifest)==B['expected_original_files']==455 and sum(x['bytes'] for x in manifest)==B['expected_original_bytes']==5473653,'exact completed original inventory')
 for row in manifest:
  name=row['path'];part=Path(name);require(not part.is_absolute() and all(x not in ['.','..'] for x in part.parts) and part.parts[0] in ['owner','run'] and name not in cache,'member path/uniqueness')
  base=O if part.parts[0]=='owner' else RUN;b=read(base.joinpath(*part.parts[1:]));require(len(b)==row['bytes'] and sha(b)==row['sha256'],'original member:'+name);cache[name]=b
 cfg=j('config.json');require(cfg['commit']=='077197e6cd3ea31f33b28aaf3882a694b3423b53' and cfg['image']['sha256']=='c5de01b869c5bb28966ab5d654b95a8ed36581c38b380ed885a5946489009932','source/image')
 for name,h in cfg['code'].items():require(sha(cache['owner/'+name])==h,'actual copied code:'+name)
 require(cache['owner/guest.py']==refs['source-guest'] and cache['owner/vm-lifecycle.py']==refs['source-lifecycle'],'exact reviewed producer code')
 consumed=json.loads(refs['consumed']);runner=json.loads(cache['run/runner-result.json']);channels=json.loads(refs['host-exits.json'])
 require(consumed['state']=='consumed' and consumed['id']==B['producer_admission'] and consumed['run']==str(RUN),'consumed original')
 require(consumed['source']['head']==cfg['commit'] and consumed['original_result']==runner,'original source/outcomes')
 require([runner[x] for x in ['command_rc','monitor_rc','runner_rc']]==[1,0,1],'producer1 retained')
 require(consumed['evidence_sha256']==sha(refs['consumption-draft.json']) and json.loads(refs['consumption-draft.json'])['disposition']=='failed-investigated','failed original consumption')
 expected_channels={'launcher':1,'tool_wrapper':1,'build':1,'command':1,'monitor':0,'runner':1,'vm':1}
 require(channels['status']=='OWNERS_GONE' and channels['channels_coherent'] is True and channels['original_channels']==expected_channels,'original host closeout')
 vm=j('vm-result.json');require(vm['rc']==1 and len(vm['boots'])==1 and not any(vm[x] for x in ['cleanup_errors','forced_host_cleanup','remaining_host_children','surviving_host_processes','qemu_still_live']),'original lifecycle cleanup')
 require(channels['qemu_identities']==vm['boots'],'same QEMU closeout identities')
 require(all(r['original_returncode']==0 and not r['timed_out'] and not r.get('forced_host_cleanup') for r in vm['commands']),'transport/host original exits')
 require('-nic' in vm['boots'][0]['argv'] and vm['boots'][0]['argv'][vm['boots'][0]['argv'].index('-nic')+1]=='none','noNIC')
 clean=j('clean/report.json');require(clean['status']=='pass' and clean['mode']=='first-boot' and clean['blocked_count']==clean['error_count']==0,'untouched clean gate')
 require(any(r.get('category')=='boot-ready' and r.get('status')=='clear' and r.get('present') is True for r in clean['checks']),'clean boot readiness')
 retirement=json.loads(refs['retirement']);require(retirement['result']=='RETIRED_EXACT_CONSUMED_MEDIA' and retirement['admission']==consumed['id'] and retirement['original_rc']==1,'original retirement')
 require({x['path'] for x in retirement['targets']}=={str(O/'vm/disk.qcow2'),str(O/'vm/OVMF.fd')} and all(x['absent_after'] for x in retirement['targets']),'exact retired media')
 require(retirement['empty_tmpdir_removed']==str(O/'host-tmp'),'exact retired scratch')
 for n in [O/'vm/disk.qcow2',O/'vm/OVMF.fd',O/'host-tmp']:require(not n.exists() and not n.is_symlink(),'retired selected path reappeared')
 proof=j('records/retroarch-proof.json');provision=j('records/retroarch-provision.json');launch=proof['launch'];final=j('records/075-retroarch-finish-report.json')
 require(proof['status']=='FAIL' and final['status']=='FAIL' and final['error']=='RuntimeError: actual-launch-log' and not final['cleanup_errors'],'exact investigated failure only')
 require(proof['launch_count']==proof['save_count']==proof['quit_count']==1 and proof['slot_up_count']==2,'one original flow')
 require(proof['actions'][-1]['request']['operation']=='finish' and proof['actions'][-1]['status']=='FAIL' and all(a['status']=='PASS' for a in proof['actions'][:-1]),'only final bookkeeping action failed')
 engine=live(launch['observation']['processes'])[0];eid=identity(engine);fid=identity(provision['frontend_process']);require(eid==(3219,8818) and fid==(2126,2029),'actual recorded identities')
 rr=runemu(launch['observation']['processes']);require(len(rr)==1,'one runemu');rid=identity(rr[0]);argv=rr[0]['argv']
 require(argv.count('-state_slot')==1 and argv[argv.index('-state_slot')+1]=='-1' and argv[argv.index('-autosave')+1]=='1' and '--core=gambatte' in argv and '--emulator=retroarch' in argv and '/storage/roms/gb/ExitProbe.gb' in argv,'actual launcher argv')
 expected_settings=launch['effective_settings_expected'];require(not launch['effective_settings_mismatches'],'actual selected settings')
 require(expected_settings['state_slot']=='-1' and expected_settings['savestate_auto_save']=='true' and expected_settings['savestate_auto_index']=='false' and expected_settings['network_cmd_enable']=='true' and expected_settings['quit_press_twice']=='true','selected source-backed settings')
 require(launch['cpu_delta']>=30 and identity(launch['ready_process'])==eid,'original CPU progress')
 surface=launch['compositor_surface'];require(surface['pid']==eid[0] and surface['rect']['width']==640 and surface['rect']['height']==480 and surface['fullscreen_mode']>0 and surface['focused'] and surface['visible'],'full-panel focused surface')
 require(all(not r['exists'] for r in launch['observation']['states']),'empty initial state')
 reports={k:json.loads(v) for k,v in cache.items() if re.fullmatch(r'owner/records/\d+-retroarch-.+-report.json',k)};require(len(reports)>0,'original reports')
 boot=j('records/boot.json')['boot_id'];seen=[]
 for name,report in reports.items():
  require(report['boot_id']==boot and not report['cleanup_errors'],'same guest boot/cleanup')
  fail=name.endswith('/075-retroarch-finish-report.json');require(report['status']==('FAIL' if fail else 'PASS'),'exact original guest status')
  ex=json.loads(cache[name.replace('-report.json','-report-exit.json')]);require(ex['reported_statuses']==(['1'] if fail else ['0']) and ex['transport_returncode']==0,'actual guest marker versus transport')
  for cmd in report['original_commands']:require(cmd['original_returncode']==0 and not cmd['timed_out'] and not cmd['output_limit'] and not cmd.get('forced_cleanup'),'original guest command exit')
  for key in ['observation','last_observation']:
   obs=report.get(key)
   if not obs:continue
   front=[r for r in obs['processes'] if Path(r['exe']).name=='emulationstation'];require(len(front)==1 and identity(front[0])==fid,'same frontend every observation')
   for r in live(obs['processes']):
    require(identity(r)==eid and r['argv']==engine['argv'],'same engine every observation');seen.append(name)
    require(obs['core_loaded'] and obs['core_file']['sha256']==obs['core_installed_reference']['sha256']=='20ef4ad8f3e8d5c71dc05f6fb78ae5157d9ab12a31edf27c9e3b6005d622327f' and obs['core_file']['bytes']==obs['core_installed_reference']['bytes'],'actual selected installed core')
   for r in runemu(obs['processes']):require(identity(r)==rid and r['argv']==argv,'same runemu every observation')
 snapshots={n:j('records/snapshot-'+n+'.json') for n in ['manual','pre-exit','stopped']};manual=state_map(snapshots['manual']);pre=state_map(snapshots['pre-exit']);stopped=state_map(snapshots['stopped']);finish=state_map(final)
 for n in ['manual','pre-exit']:require([identity(r) for r in live(snapshots[n]['observation']['processes'])]==[eid],'live before quit')
 for r in [snapshots['stopped'],final]:require(not live(r['observation']['processes']) and not runemu(r['observation']['processes']),'observed engine/runemu absent')
 require(final['command_port_after']==[],'actual listener absence')
 for name in ['ExitProbe.srm','ExitProbe.state1','ExitProbe.state.auto']:require(finish[name]['exists'] and finish[name]['bytes']>0,'all separate saves')
 require(decoded(finish['ExitProbe.srm'])[0]==0x55,'actual SRAM sentinel')
 require(manual['ExitProbe.state1']['exists'] and not manual['ExitProbe.state.auto']['exists'] and not pre['ExitProbe.state.auto']['exists'] and stopped['ExitProbe.state.auto']['exists'],'AUTO only after quit')
 for k in ['sha256','bytes','mtime_ns']:require(len({r['ExitProbe.state1'][k] for r in [manual,pre,stopped,finish]})==1,'numbered state unchanged:'+k)
 for name in ['ExitProbe.state1','ExitProbe.state.auto']:
  require(decoded(stopped[name])==decoded(finish[name]),'stopped/final state bytes stable')
 controls=[a for a in proof['actions'] if a['request']['operation']=='engine-command'];require([a['request']['key'] for a in controls]==['slot-up','slot-up','save','quit'],'exact input actions')
 for a in controls:
  pr=a['protocol_result'];require(pr['status']=='PASS' and identity(pr['before_engine'])==eid,'control engine identity');listener=pr['command_listener'];require(identity(listener['engine'])==eid and len(listener['rows'])==1,'listener owner')
  row=listener['rows'][0];require(row['local']=='00000000:D83B' and 'socket:['+str(row['inode'])+']' in [x['target'] for x in listener['engine_socket_fds']],'named listener inode')
  expected=['GET_STATUS',{'slot-up':'STATE_SLOT_PLUS','save':'SAVE_STATE','quit':'QUIT'}[a['request']['key']]]
  if a['request']['key']=='quit':expected+=['GET_STATUS','QUIT']
  require([r['command'] for r in pr['protocol']]==expected,'fixed protocol without retries')
  for row in pr['protocol']:
   require(row['destination']==['127.0.0.1',55355] and row['sent_bytes']==len(row['command'])+1,'exact local datagram')
   if row['command']=='GET_STATUS':require(base64.b64decode(row['reply_b64'],validate=True).decode()==row['reply'] and row['reply']=='GET_STATUS PLAYING game_boy,ExitProbe,crc32=4324bdbf\n' and row['reply_monotonic']>=row['sent_monotonic'],'actual status response')
 quit=controls[-1]['protocol_result'];qs=[r for r in quit['protocol'] if r['command']=='QUIT'];delta=qs[1]['sent_monotonic']-qs[0]['sent_monotonic'];require(.6<=delta<2.5 and delta==quit['quit_send_interval_seconds'] and identity(quit['between_quit_engine'])==eid,'two timed quit requests')
 require(pre['ExitProbe.state1']['mtime_ns']<=qs[0]['sent_epoch_ns']<=finish['ExitProbe.state.auto']['mtime_ns']<=final['ended_ns'],'save/quit/auto ordering')
 logs={r['path']:decoded(r).decode() for r in final['logs']};ex=logs['/var/log/exec.log'];es=logs['/var/log/es_log.txt'];require(re.findall(r'Checking errors:\s*(-?\d+)',ex)==['0'],'raw engine shell wait0')
 require(' -state_slot -1' not in ex and ' -state_slot -1' in es and '--snapshot=-1' in ex,'wrong-log defect independently reproduced')
 lines=[line for line in es.splitlines() if '/usr/bin/runemu.sh /storage/roms/gb/ExitProbe.gb ' in line];require(len(lines)==1 and ' -autosave 1 -state_slot -1' in lines[0] and '--core=gambatte' in lines[0],'actual ES launcher log')
 require('Executing /usr/bin/retroarch -L /tmp/cores/gambatte_libretro.so ' in ex and 'Auto save state to "/storage/roms/savestates/gb/ExitProbe.state.auto" succeeded.' in ex and 'Saving state "/storage/roms/savestates/gb/ExitProbe.state1"' in ex,'actual engine/save logs')
 require(' --exit 0' in es and 'emulator ended by signal' not in ex and 'after the exit hotkey was pressed' not in ex,'un-normalized successful engine exit')
 required=['manager-before','slot-one','manual-saved','manager-after','es-return'];frame_review=json.loads(read(HERE/'source-worker-frame-review.json'))
 require(all(n in proof['reviews'] for n in required),'all original frame reviews')
 for label,row in proof['frames'].items():
  name='owner/'+str(Path(row['path']).relative_to(O));b=cache[name];require(sha(b)==row['sha256'] and len(b)==row['bytes'] and b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('!II',b[16:24])==(640,480),'actual original frame:'+label)
 for n in required:
  row=proof['reviews'][n];require(row['frame']==proof['frames'][n] and row['text'] and frame_review['frames'][n]['sha256']==row['frame']['sha256'],'reviewed frame identity')
 for n in ['manager-before','manager-after','es-return']:require(not live(proof['frames'][n]['observation']['processes']),'manager/frontend frame after engine absence')
 result.update(status='PASS_RETAINED_ORIGINALS_WITH_FAILED_PRODUCER',source=cfg['commit'],image_sha256=cfg['image']['sha256'],producer_run=str(RUN),producer_admission=consumed['id'],producer_original_channels=expected_channels,producer_disposition='failed-investigated; unchanged',original_members_verified=len(manifest),original_member_bytes=sum(r['bytes'] for r in manifest),engine_identity=eid,frontend_identity=fid,runemu_identity=rid,engine_observations=len(seen),raw_engine_shell_wait=0,quit_send_interval_seconds=delta,states={n:{k:v for k,v in finish[n].items() if k!='bytes_b64'} for n in ['ExitProbe.srm','ExitProbe.state1','ExitProbe.state.auto']},frame_hashes={n:proof['frames'][n]['sha256'] for n in required},actual_ES_launch_line=lines[0],all_original_owners_gone_receipt_sha256=B['refs']['host-exits.json']['sha256'],retirement_receipt_sha256=B['refs']['retirement']['sha256'],marker_limit='Direct guest marker absence check was not reached. Source runemu consumes marker before its0 return; raw engine wait0 excludes nonzero marker normalization. No direct marker stat or universal post-return absence claim.',limits=['Original VM/guest producer remains1 due wrong-log assertion. This reader qualifies retained observations only.','No independent ES waitpid interception, internal RetroArch poll counters, default-keyboard success, device/runtime replay or broad audit completion claim.','Root retains acceptance authority; this script does not mutate producer/export/tracker or consume an admission.'])
except BaseException as exc:result['error']=type(exc).__name__+': '+str(exc)
finally:
 signal.alarm(0);result['elapsed_seconds']=time.monotonic()-started;result['read_bytes']=read_bytes
 out.mkdir(mode=0o700);raw=json.dumps(result,indent=2).encode()+b'\n';require(len(raw)<=1024**2,'result bound')
 with (out/'result.json').open('xb') as f:f.write(raw)
 print(json.dumps({'status':result['status'],'result':str(out/'result.json'),'sha256':sha(raw),'elapsed_seconds':result['elapsed_seconds'],'read_bytes':read_bytes}))
raise SystemExit(0 if result['status']=='PASS_RETAINED_ORIGINALS_WITH_FAILED_PRODUCER' else 1)
