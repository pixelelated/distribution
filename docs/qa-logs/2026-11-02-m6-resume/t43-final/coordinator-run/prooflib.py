import pathlib,subprocess,json,hashlib,os,stat,datetime
P=pathlib.Path(__file__).resolve().parent
CWD='/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346'
ROOT='f1000e157c2f0248820e1b77055e81521b079a3f'
FINAL='8282cbcade3be32b437f7391be7e216d9a6b1074'
D='676115271e9bbaa9e8db81f6de73a7b49094c5b4'
SEED='601e4694f9726b2228d3571efdb5cfc061c6d442'
A='docs/audits/2026_11_02-epic-m6-patches-unshipped/'
EXT='/workspace/tmp/m6-t43/eh-publication'
sha=lambda b:hashlib.sha256(b).hexdigest()
def record(x):
 with (P/'observed-reads.jsonl').open('a') as f:f.write(json.dumps(x,sort_keys=True)+'\n')
def git(*args):
 assert args[0] in ('show','ls-tree','log','rev-parse','diff','merge-base','cat-file')
 argv=['git','-C',CWD,*args];t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(argv,capture_output=True,env=dict(os.environ,LC_ALL='C',GIT_OPTIONAL_LOCKS='0'))
 record(dict(kind='git',argv=argv,start=t,rc=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr),stdout_bytes=len(r.stdout)))
 if r.returncode:raise RuntimeError((argv,r.returncode,r.stderr.decode()))
 return r.stdout
def blob(path,ref=FINAL):return git('show',ref+':'+path)
def j(path,ref=FINAL):return json.loads(blob(path,ref))
def ext(name):
 parts=pathlib.PurePosixPath(name).parts
 assert parts and not name.startswith('/') and all(x not in ('..','.','') for x in parts)
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC)
 try:
  for part in EXT.strip('/').split('/')+list(parts[:-1]):
   child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=child
  f=os.open(parts[-1],os.O_RDONLY|os.O_CLOEXEC|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   st=os.fstat(f);assert stat.S_ISREG(st.st_mode);chunks=[]
   while b:=os.read(f,1024*1024):chunks.append(b)
   end=os.fstat(f);assert (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)==(end.st_dev,end.st_ino,end.st_size,end.st_mtime_ns)
   data=b''.join(chunks)
  finally:os.close(f)
 finally:os.close(fd)
 record(dict(kind='confined-NOFOLLOW-regular',name=name,bytes=len(data),sha256=sha(data),dev=st.st_dev,ino=st.st_ino,mode=oct(st.st_mode),mtime_ns=st.st_mtime_ns))
 return data
def shape(x,depth=1):
 if isinstance(x,dict):return {k:shape(v,depth-1) if depth>0 else (type(v).__name__+':'+str(len(v)) if isinstance(v,(dict,list,str)) else v) for k,v in x.items()}
 if isinstance(x,list):return {'length':len(x),'first':shape(x[0],depth-1) if x and depth>0 else None}
 return x
assert set(os.sched_getaffinity(0))==set(range(8,24))
