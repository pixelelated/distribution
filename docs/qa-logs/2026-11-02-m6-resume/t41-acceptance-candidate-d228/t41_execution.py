"""D226 final gates. Embedded after receipt predicates; never run an accepted producer.
Only new final checks execute, in a fresh disposable local clone below ACCEPT_DIR.
Author: Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import datetime, time, tempfile, signal
TOOL_REF='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
TOOL_PATHS=['tools/lint-audit-artifacts','tools/rules-check','tools/register-check','tools/work-log-index','tools/ceremony-check','tools/box-check','tools/forbidden-terms-check']
SECRET_CMD='. .githooks/secret-patterns; /usr/bin/grep -a -c -E -e "${SECRET_PATTERNS}"'
CHECK_CMDS=[['tools/register-check'],['tools/work-log-index','--check'],['tools/rules-check','--quiet'],['tools/ceremony-check','--gate'],['.githooks/hooks-test']]
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
def private_path(p):
    p=P.Path(p).absolute()
    need(p.is_relative_to(OWN) and p!=OWN and p.resolve()==p,'execution write path outside owned scratch or symlink')
    if p.exists() and p.is_file():need(p.stat().st_nlink==1,'execution write hardlink')
    return p

def mask_log(b):
    # Same two permitted masks as t36's outer filter, applied before persistence too.
    t=b.decode('utf-8',errors='replace')
    t=re.sub(r'((?:token|key|pass(?:w[a-z]*)?|psk|user) *[=:] *)[^ \n\r]*',r'\1***',t,flags=re.I)
    t=re.sub(r'(--(?:token|key|pass(?:w[a-z]*)?|psk|user)[= ]+)[^ \n\r]+',r'\1***',t,flags=re.I)
    return t.encode()

class FinalGates:
    def __init__(self,r):
        self.r=r;self.n=0;self.clones={};self.history_refs=None
        root=private_path(os.environ['ACCEPT_DIR']);root.mkdir(parents=True,exist_ok=True)
        self.root=private_path(tempfile.mkdtemp(prefix='final-gates-',dir=root))
        self.tmp=self.root/'tmp';self.tmp.mkdir()
        # Do not inherit ES_SRC, shell startup, Git overrides, arbitrary Python paths,
        # or credentials in argv. gh alone retains its existing authentication context.
        keep=['PATH','HOME','GH_TOKEN','GITHUB_TOKEN','GH_HOST','GH_CONFIG_DIR','XDG_CONFIG_HOME','SSL_CERT_FILE','SSL_CERT_DIR','FORBIDDEN_PATTERNS']
        self.env={k:os.environ[k] for k in keep if k in os.environ}
        self.env.update(LC_ALL='C',TMPDIR=str(self.tmp),TMP=str(self.tmp),TEMP=str(self.tmp),PYTHONDONTWRITEBYTECODE='1',
            GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0',
            GIT_AUTHOR_NAME='Codex acceptance simulation',GIT_AUTHOR_EMAIL='codex-acceptance@invalid',
            GIT_COMMITTER_NAME='Codex acceptance simulation',GIT_COMMITTER_EMAIL='codex-acceptance@invalid')
        opts={'core.hooksPath':'/dev/null','core.fsmonitor':'false','core.attributesFile':'/dev/null','init.templateDir':'',
              'commit.gpgsign':'false','tag.gpgsign':'false','protocol.allow':'never','protocol.file.allow':'always',
              'submodule.recurse':'false','core.quotePath':'true'}
        self.env['GIT_CONFIG_COUNT']=str(len(opts))
        for i,(k,v) in enumerate(opts.items()):self.env['GIT_CONFIG_KEY_'+str(i)]=k;self.env['GIT_CONFIG_VALUE_'+str(i)]=v
    def command(self,label,argv,cwd=None,data=None,expect=(0,),last=None,env=None,timeout=120):
        """Persist masked stdout/stderr plus hashes of actual bytes, argv/input/exit/time.
        Missing executable/timeouts => CANNOT; a completed wrong rc/output => FAIL.
        Never invoke a shell except the literal secret-patterns interface above.
        """
        need(re.fullmatch('[a-z0-9-]+',label),'invalid command receipt label')
        cwd=private_path(cwd or self.root);need(cwd.is_dir(),'command cwd absent')
        need(isinstance(argv,list) and all(isinstance(a,str) and '\x00' not in a for a in argv),'invalid argv')
        allowed={'git','gh','python3','bash',*TOOL_PATHS,'.githooks/hooks-test'}
        need(argv[0] in allowed,'unreviewed executable')
        if argv[0]=='bash':need(argv==['bash','--noprofile','--norc','-c',SECRET_CMD],'unreviewed shell program')
        if argv[0]=='python3':need(argv[1:4]==['-I','-m','py_compile'] and len(argv)==5,'producer execution forbidden')
        if argv[0]=='gh':need(argv[1]=='api' and len(argv)>2 and argv[2].startswith('repos/pixelelated/distribution/issues/'),'non-read GitHub command')
        e=dict(self.env);e.update(env or {})
        self.n+=1;stem=f'{self.n:04d}-{label}';started=datetime.datetime.now(datetime.timezone.utc).isoformat();start=time.monotonic()
        rc=None;out=b'';err=b'';problem=None;timed=False
        try:
            p=subprocess.Popen(argv,cwd=cwd,env=e,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            try:out,err=p.communicate(data,timeout=timeout)
            except subprocess.TimeoutExpired:
                timed=True;os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate();problem='command timed out'
            rc=p.returncode
        except OSError as x:problem='executable unavailable ('+type(x).__name__+')'
        record={'schema':1,'identity':'Codex (GPT-6), /root, wN:p5','label':label,'argv':argv,'cwd':str(cwd),
            'start':started,'elapsed_seconds':round(time.monotonic()-start,6),'rc':rc,'timed_out':timed,'problem':problem,
            'stdin_sha256':None if data is None else sha(data),'stdin_bytes':0 if data is None else len(data),
            'stdout_sha256':sha(out),'stderr_sha256':sha(err),'stdout':stem+'.stdout','stderr':stem+'.stderr',
            'stdout_masked_sha256':sha(mask_log(out)),'stderr_masked_sha256':sha(mask_log(err)),
            'lane_tip':self.r.tip,'coordinator_tip':self.r.coord,'fixture':bool(self.r.fixture)}
        for suffix,content in [('stdout',mask_log(out)),('stderr',mask_log(err)),('json',(json.dumps(record,indent=2)+'\n').encode())]:
            path=private_path(self.root/(stem+'.'+suffix))
            with path.open('xb') as f:f.write(content)
        if problem:raise Cannot(label+': '+problem+'; receipt '+str(self.root/(stem+'.json')))
        need(rc in expect,label+': unexpected rc '+str(rc)+'; receipt '+str(self.root/(stem+'.json')))
        if last is not None:need(out.decode(errors='replace').rstrip().splitlines()[-1:]==[last],label+': required final output line absent')
        return out,rc
    def verified_tools(self,ref):
        r=self.r
        paths=TOOL_PATHS+list(r.tree(TOOL_REF,'.githooks/'))
        for p in paths:
            expected=r.tree(TOOL_REF,p);actual=r.tree(ref,p)
            if not expected or expected!=actual:raise Cannot('final executable changed from reviewed '+TOOL_REF[:12]+': '+p)
        # Audit-local generator is syntax-checked only, never executed here.
    def clone(self,integrated=False):
        key='integration' if integrated else 'lane'
        if key in self.clones:return self.clones[key]
        r=self.r;r.final_artifacts();self.verified_tools(r.tip)
        if integrated:self.verified_tools(r.coord)
        repo=P.Path(r.repo).resolve();need(repo.is_dir(),'local object store absent')
        dest=self.root/key
        need(not dest.exists(),'simulation destination exists')
        self.command(key+'-clone',['git','clone','--quiet','--shared','--no-checkout','--no-hardlinks','--template=',str(repo),str(dest)])
        # ceremony-check's actual interface resolves next and upstream/next, not
        # HEAD. Snapshot those existing local refs once; never fetch or silently
        # rebind them to the lane. Both simulations get identical recorded hashes.
        if self.history_refs is None:
            self.history_refs={}
            for ref in ['refs/heads/next','refs/remotes/upstream/next']:
                out,rc=self.command('source-history-ref',['git','-C',str(repo),'rev-parse','--verify',ref+'^{commit}'],expect=tuple(range(256)))
                if rc:raise Cannot('ceremony-check required local history ref unavailable: '+ref)
                full=out.decode().strip();need(re.fullmatch('[0-9a-f]{40}',full),'history ref is not a full commit')
                self.history_refs[ref]=full
        for ref,full in self.history_refs.items():
            self.command(key+'-history-ref',['git','update-ref',ref,full],dest)
        self.command(key+'-checkout',['git','checkout','--quiet','--detach',r.coord if integrated else r.tip],dest)
        before,_=self.command(key+'-head-before',['git','rev-parse','HEAD'],dest)
        expected=r.git('rev-parse',(r.coord if integrated else r.tip)+'^{commit}').strip()
        need(before.strip()==expected,'checkout did not select exact immutable tip')
        if integrated:
            # No commit, no hooks, no live refs and no conflict auto-resolution.
            self.command('integration-merge',['git','-c','merge.autoStash=false','merge','--no-edit','--no-commit','--no-ff',r.tip],dest)
            unmerged,_=self.command('integration-unmerged',['git','ls-files','-u'],dest)
            need(not unmerged,'integration contains unresolved entries')
            self.command('integration-whitespace',['git','diff','--check','--cached'],dest)
        self.validate_clone_paths(dest)
        self.clones[key]=dest
        return dest
    def validate_clone_paths(self,dest):
        # Readers only traverse their checked record/tool roots. No symlink or held
        # output is allowed in those inputs, including nested audit evidence.
        for roof in ['docs','.claude','tools','.githooks']:
            d=dest/roof
            if not d.exists():continue
            for p in d.rglob('*'):
                if p.is_symlink():raise Cannot('checker input is a symlink: '+str(p.relative_to(dest)))
        for p in (dest/'docs/audits').rglob('*.held.json'):
            v=json.loads(p.read_text());reply=p.parent/v.get('reply','')
            need(reply.resolve().is_relative_to(p.parent.resolve()),'held declaration path escapes records')
            if reply.is_file():raise Cannot('held reply is present in checker input; no held read authorized')
    def lint(self,dest,prefix='lane'):
        n=os.environ.get('AUDIT_ISSUE','')
        if not n or n=='0':raise Absent('no final audit issue for resolution lint')
        need(n.isdigit(),'audit issue must be numeric')
        # Validate Local-only scope before invoking the checker.
        v=json.loads((dest/self.r.af/'second-opinions/review-plan.json').read_bytes())
        need(v.get('depth')=='local' and v.get('reviewers')==[] and v.get('tier_exception')=='D-WORKFLOW-184','not the authorized Local review')
        for suffix,args in [('default',[]),('issue',['--issue',n])]:
            self.command(prefix+'-lint-'+suffix,['tools/lint-audit-artifacts',self.r.af,*args],dest,last='PASS')
    def forbidden(self,dest,prefix='lane',whole=False):
        # The checker alone may read its normal private wordlist; it is never copied,
        # opened or sourced by this harness. Positive uses an explicitly public regex.
        self.command(prefix+'-forbidden-positive',['tools/forbidden-terms-check','--stdin'],dest,
            b'synthetic t41 sentinel\n',expect=(1,),last='forbidden-terms-check: 1 line(s) on stdin carry a listed word',env={'FORBIDDEN_PATTERNS':'synthetic[ ]t41[ ]sentinel'})
        if whole:self.command(prefix+'-forbidden-tree',['tools/forbidden-terms-check'],dest)
        paths=self.record_paths()
        for i,p in enumerate(paths):
            self.command(prefix+'-forbidden-record-'+str(i),['tools/forbidden-terms-check','--stdin'],dest,
                self.checked_record(dest,p),last='forbidden-terms-check: 0 hits on stdin')
    def record_paths(self):
        r=self.r;ps=r.git('diff','--name-only','--diff-filter=ACMR','-z',r.dispatch,r.tip).split(b'\0')
        paths=[p.decode() for p in ps if p]
        # Include complete final audit records even if unchanged from dispatch.
        paths=sorted(set(paths)|set(r.tree(r.tip,r.af+'/')))
        need(bool(paths),'no final records to scan')
        for p in paths:
            relpath(p);need(p.startswith(('docs/','.github/sessions/',r.af+'/')),'unexpected final changed path')
        return paths
    def checked_record(self,dest,p):
        q=dest/p;need(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(dest),'record absent or unsafe')
        need(not q.name.endswith('.held.json') and '/held/' not in p,'held input outside scope')
        return q.read_bytes()
    def secret(self,dest,prefix='lane'):
        cmd=['bash','--noprofile','--norc','-c',SECRET_CMD]
        self.command(prefix+'-secret-compile',cmd,dest,b'',expect=(1,),last='0')
        positive=('dev'+'password='+'QwErTyUiOpAsDfGh'+'\n').encode()
        self.command(prefix+'-secret-positive',cmd,dest,positive,last='1')
        for i,p in enumerate(self.record_paths()):self.command(prefix+'-secret-record-'+str(i),cmd,dest,self.checked_record(dest,p),expect=(1,),last='0')
    def checkers(self,dest,prefix='lane'):
        for cmd in CHECK_CMDS:
            self.command(prefix+'-'+P.PurePosixPath(cmd[0]).name,cmd,dest,last='PASS' if cmd[0]=='.githooks/hooks-test' else None,timeout=240)
        # --gate tolerates CI-only debt. Its text is retained for coordinator judgment;
        # its documented exit is the criterion, never a historical checker receipt.
        self.forbidden(dest,prefix,whole=True)
        self.lint(dest,prefix)
    def issues(self,n,comments=False):
        need(str(n).isdigit(),'invalid issue number')
        argv=['gh','api','repos/pixelelated/distribution/issues/'+str(n)+('/comments?per_page=100' if comments else '')]
        if comments:argv+=['--paginate','--slurp']
        raw,rc=self.command('live-'+str(n)+('-comments' if comments else ''),argv,expect=tuple(range(256)))
        if rc:raise Cannot('live issue read unavailable #'+str(n)+'; command/exit receipt retained')
        v=json.loads(raw)
        if comments:
            need(isinstance(v,list) and all(isinstance(x,list) for x in v),'invalid paginated comments')
            v=sum(v,[])
        else:need(isinstance(v,dict) and v.get('number')==int(n) and isinstance(v.get('body'),str),'invalid live issue response')
        return v

def final_gates(r):
    if not hasattr(r,'final'):r.final=FinalGates(r)
    return r.final

def executable_check(r,s):
    f=final_gates(r)
    if s in ['audit-boxes','bug-boxes','lane-boxes']:
        items=[r.audit_issue()] if s=='audit-boxes' else r.bugs() if s=='bug-boxes' else [r.issues(688)]
        # An inherited bug may remain open for the integration. box-check validates
        # its criteria; only the audit's Phase-7 outcomes must all be disposed.
        for i in items:
            if s=='audit-boxes':need(not re.search(r'^\s*- \[ \]',i['body'],re.M),'audit has unresolved outcome checkbox')
            num=i.get('number',i.get('issue_number'));need(isinstance(num,int),'issue number absent')
            d=f.clone();f.command('checkbox-'+str(num),['tools/box-check','--issue',str(num)],d)
        return 'live issue criteria and executable box-check receipts retained'
    d=f.clone(s=='merge')
    if s=='lint':f.lint(d)
    elif s=='forbidden':f.forbidden(d)
    elif s=='secret':f.secret(d)
    elif s in ['checkers','merge']:
        f.checkers(d,'integration' if s=='merge' else 'lane')
        if s=='merge':f.secret(d,'integration')
    elif s=='generators':
        # py_compile parses bytes without importing or executing the generator.
        f.command('generator-syntax',['python3','-I','-m','py_compile',str(d/r.af/'tools/t41-tables.py')],d)
    else:raise Invalid('unknown executable gate')
    return 'new final '+s+' commands completed; masked evidence '+str(f.root)
