"""D226 final gates. Embedded after receipt predicates; never run an accepted producer.
Only new final checks execute, in a fresh disposable local clone below ACCEPT_DIR.
Author: Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import datetime, time, tempfile, signal
TOOL_REF='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
TOOL_PATHS=['tools/lint-audit-artifacts','tools/rules-check','tools/register-check','tools/work-log-index','tools/ceremony-check','tools/box-check','tools/forbidden-terms-check']
SECRET_CMD='. .githooks/secret-patterns; /usr/bin/grep -a -c -E -e "${SECRET_PATTERNS}"'
CHECK_CMDS=[['tools/register-check'],['tools/work-log-index','--check'],['tools/rules-check','--quiet'],['tools/ceremony-check','--gate'],['.githooks/hooks-test']]
TOOL_AUTHOR={'harness':'Codex','model':'GPT-6','agent':'/root','pane':'wN:p5','session':'01a19d12-1c5f-7022-8053-102f6a94b7fe'}
ROOT_EXECUTOR={'harness':'Codex','model':'GPT-6-Astra','effort':'xhigh','session':'01a19d11-f5c8-7bb0-80f3-49ad28732af2','pane':'wN:p2','identity_source':'observed footer'}
DAY_LOG='docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
LOG_INDEX='docs/work-logs/INDEX.md'
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
        raw=os.environ.get('ACCEPT_EXECUTOR_JSON')
        if not raw:raise Cannot('mandatory actual executor identity missing: ACCEPT_EXECUTOR_JSON')
        self.executor=proof_json(raw)
        need(isinstance(self.executor,dict) and set(self.executor)==set(ROOT_EXECUTOR) and all(isinstance(v,str) and v.strip() for v in self.executor.values()),'executor metadata shape differs')
        need(bool(re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',self.executor['session'])) and bool(re.fullmatch(r'wN:p[0-9]+',self.executor['pane'])),'executor session/pane invalid')
        # Fixture processes must identify their actual author, not impersonate root.
        if not r.fixture:need(self.executor==ROOT_EXECUTOR,'final executor differs from the observed coordinator identity')
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
              'submodule.recurse':'false','core.quotePath':'true','core.whitespace':'blank-at-eol,blank-at-eof,space-before-tab'}
        self.env['GIT_CONFIG_COUNT']=str(len(opts))
        for i,(k,v) in enumerate(opts.items()):self.env['GIT_CONFIG_KEY_'+str(i)]=k;self.env['GIT_CONFIG_VALUE_'+str(i)]=v
    def command(self,label,argv,cwd=None,data=None,expect=(0,),last=None,env=None,timeout=120,raw_public=False):
        """Persist masked stdout/stderr plus hashes of actual bytes, argv/input/exit/time.
        Missing executable/timeouts => CANNOT; a completed wrong rc/output => FAIL.
        Never invoke a shell except the literal secret-patterns interface above.
        """
        need(type(timeout) in [int,float] and 0<timeout<=1200,'command timeout must be bounded at most 1200 seconds')
        if raw_public:need(argv[:3]==['git','diff','--check'],'raw evidence restricted to public Git whitespace diagnostics')
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
        record={'schema':2,'tool_author':dict(TOOL_AUTHOR),'executor':dict(self.executor),'label':label,'argv':argv,'cwd':str(cwd),
            'timeout_seconds':timeout,'start':started,'elapsed_seconds':round(time.monotonic()-start,6),'rc':rc,'timed_out':timed,'problem':problem,
            'stdin_sha256':None if data is None else sha(data),'stdin_bytes':0 if data is None else len(data),
            'stdout_sha256':sha(out),'stderr_sha256':sha(err),'stdout':stem+'.stdout','stderr':stem+'.stderr',
            'stdout_masked_sha256':sha(mask_log(out)),'stderr_masked_sha256':sha(mask_log(err)),
            'lane_tip':self.r.tip,'coordinator_tip':self.r.coord,'fixture':bool(self.r.fixture)}
        if raw_public:
            for kind,b in [('stdout',out),('stderr',err)]:
                filename=stem+'.raw.'+kind;record['raw_'+kind]=filename
                with private_path(self.root/filename).open('xb') as f:f.write(b)
        for suffix,content in [('stdout',mask_log(out)),('stderr',mask_log(err)),('json',(json.dumps(record,indent=2)+'\n').encode())]:
            path=private_path(self.root/(stem+'.'+suffix))
            with path.open('xb') as f:f.write(content)
        if raw_public:need(not err,'public Git whitespace diagnostics included unexpected stderr')
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
            self.integration_whitespace(dest,cached=False)
            _,rc=self.command('integration-merge',['git','-c','merge.autoStash=false','merge','--no-edit','--no-commit','--no-ff',r.tip],dest,expect=(0,1))
            if rc:self.merge_worklogs(dest)
            unmerged,_=self.command('integration-unmerged',['git','ls-files','-u'],dest)
            need(not unmerged,'integration contains unresolved entries')
            self.integration_whitespace(dest,cached=True)
        self.validate_clone_paths(dest)
        self.clones[key]=dest
        return dest

    def merge_worklogs(self,dest):
        """Resolve only whole appended entries, using immutable base and both tips.
        Never use conflict-marker text or a general ours/theirs strategy.
        """
        raw,_=self.command('append-unmerged',['git','ls-files','-u','-z'],dest)
        conflicts={x.split(b'\t',1)[1].decode() for x in raw.split(b'\0') if x}
        need(conflicts and conflicts<={DAY_LOG,LOG_INDEX},'integration conflict outside exact daily log/generated index')
        raw,_=self.command('append-base',['git','merge-base','--all',self.r.coord,self.r.tip],dest)
        bases=raw.decode().splitlines();need(len(bases)==1 and re.fullmatch('[0-9a-f]{40}',bases[0]),'append merge requires one exact merge-base')
        base=bases[0];bodies=[];identities=[]
        for label,ref in [('base',base),('coordinator',self.r.coord),('lane',self.r.tip)]:
            entry,_=self.command('append-'+label+'-identity',['git','ls-tree','-z',ref,'--',DAY_LOG],dest)
            rows=[x for x in entry.split(b'\0') if x]
            need(len(rows)==1 and rows[0].split(b'\t')[0].split()[:2]==[b'100644',b'blob'],'append log must exist as a regular 100644 file at base and both tips')
            b,_=self.command('append-'+label+'-bytes',['git','show',ref+':'+DAY_LOG],dest)
            bodies.append(b);identities.append(dict(ref=ref,entry=entry.decode(),sha256=sha(b)))
        merged,sequences=merge_append_bytes(*bodies)
        # Index conflicts are generated state, but every tip still needs a regular
        # index. Rebuild it after the immutable daily entries have been united.
        for ref in [base,self.r.coord,self.r.tip]:
            entry,_=self.command('append-index-identity',['git','ls-tree','-z',ref,'--',LOG_INDEX],dest)
            need(entry.split(b'\t')[0].split()[:2]==[b'100644',b'blob'],'append index is absent/nonregular')
        before,_=self.command('append-before-status',['git','status','--porcelain=v1','-z','--untracked-files=all'],dest)
        # Write only these two exact paths below this private simulation clone.
        day=private_path(dest/DAY_LOG);need(day.is_file() and not day.is_symlink(),'unsafe daily log destination')
        index=private_path(dest/LOG_INDEX);need(index.is_file() and not index.is_symlink(),'unsafe index destination')
        day.write_bytes(merged)
        # Bind the expected index to the tool's actual print interface before write.
        rendered,_=self.command('append-index-render',['tools/work-log-index'],dest)
        self.command('append-index-write',['tools/work-log-index','--write'],dest)
        need(day.read_bytes()==merged,'index tool changed whole daily append entries')
        need(index.read_bytes()==rendered,'index --write differs from its exact render')
        self.command('append-index-check',['tools/work-log-index','--check'],dest)
        after,_=self.command('append-after-status',['git','status','--porcelain=v1','-z','--untracked-files=all'],dest)
        # Guard file contents too, not just status membership: the reviewed index
        # tool has only this one output; a fixture trying any other write fails.
        def status_except(raw):return [x for x in raw.split(b'\0') if x and x[3:].decode() not in [DAY_LOG,LOG_INDEX]]
        need(status_except(before)==status_except(after),'index generation changed other path status')
        unstaged,_=self.command('append-other-unstaged',['git','diff','--name-only','-z','--','.',':(exclude,literal)'+DAY_LOG,':(exclude,literal)'+LOG_INDEX],dest)
        need(not unstaged,'index generation changed another tracked file')
        self.command('append-add',['git','add','--',DAY_LOG,LOG_INDEX],dest)
        unmerged,_=self.command('append-resolved',['git','ls-files','-u'],dest);need(not unmerged,'append merge left conflicts')
        staged,_=self.command('append-staged-bytes',['git','show',':'+DAY_LOG],dest)
        need(staged==merged,'staged append bytes differ')
        receipt=dict(schema=1,tool_author=TOOL_AUTHOR,executor=self.executor,base_and_tips=identities,
            path=DAY_LOG,merged_sha256=sha(merged),entry_sequences=sequences,index_sha256=sha(rendered),result='PASS')
        with private_path(self.root/'append-merge.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')

    def integration_whitespace(self,dest,cached=False):
        """Six exact public records only. Preserve full original rc/diagnostics,
        then require rc0 for every remaining path; never normalize evidence.
        """
        r=self.r;allowed=d228_overlay_paths(r)
        need(len(allowed)==2,'integration requires the exact current and retained D228 header inputs')
        for tail in ['01-research-notes.md','stage-a/order.out','stage-a/run/stage-a-extra.out','stage-a/run/stage-a.out']:
            path=r.af+'/'+tail;expected=r.tree(STAGE_D,path)
            need(bool(expected) and expected==r.tree(r.tip,path),'whitespace accepted record changed: '+path)
            allowed=dict(allowed,**expected)
        need(len(allowed)==6,'whitespace exception census differs')
        identities=[]
        for path,entry in sorted(allowed.items()):
            need(r.tree(r.tip,path)=={path:entry},'whitespace input mode/blob differs')
            identities.append(dict(path=path,mode_blob=entry,sha256=sha(r.blob(path))))
            if cached:
                raw,_=self.command('whitespace-index-identity',['git','ls-files','--stage','-z','--',path],dest)
                rows=[x.split(b'\t',1)[0].split() for x in raw.split(b'\0') if x]
                parts=entry.split();need(rows==[[parts[0].encode(),parts[2].encode(),b'0']],'integrated whitespace record differs from validated input')
        mode='cached' if cached else 'tips'
        base=['git','diff','--check','--no-ext-diff','--no-textconv']+(['--cached'] if cached else [r.coord,r.tip])
        full,rc=self.command('whitespace-'+mode+'-full',base,dest,expect=(0,2),raw_public=True)
        diagnostics={m.group(1) for m in re.finditer(r'^([^+\n][^\n]*?):[0-9]+: (?:trailing whitespace|space before tab|new blank line at EOF)\.',full.decode(),re.M)}
        need((rc==0 and full==b'') or (rc==2 and diagnostics and diagnostics<=set(allowed)),'whitespace diagnostics outside exact preserved inputs')
        if not cached:need(rc==2 and diagnostics==set(allowed),'immutable T41 whitespace diagnostic census differs from the measured six paths')
        rest=base+['--','.',*[':(exclude,literal)'+path for path in sorted(allowed)]]
        self.command('whitespace-'+mode+'-remaining',rest,dest,raw_public=True)
        receipt=dict(schema=1,tool_author=TOOL_AUTHOR,executor=self.executor,tip=r.tip,coordinator=r.coord,
            cached=cached,rc=rc,stdout_sha256=sha(full),excluded=identities,diagnostic_paths=sorted(diagnostics),remaining_rc=0)
        with private_path(self.root/('whitespace-'+mode+'.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')

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
        if whole:self.command(prefix+'-forbidden-tree',['tools/forbidden-terms-check'],dest,timeout=1200)
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


def merge_append_bytes(base,coordinator,lane):
    need(base.endswith(b'\n'),'append base must end at a line boundary')
    # Timestamp syntax is validated without normalizing any header/body byte.
    # Existing time-only, full-date UTC and ISO UTC forms are all published in
    # this exact daily log. Calendar/time ranges are checked separately below.
    stamp=(rb'(?:[0-9]{2}:[0-9]{2} UTC|'
           rb'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC|'
           rb'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|\+00:00))')
    heading=rb'^## (?P<stamp>'+stamp+rb') (?:--|\xe2\x80\x94|\xe2\x80\x93|-)+ .+\n'
    def valid_stamp(raw):
        text=raw.decode('ascii')
        try:
            if re.fullmatch(r'[0-9]{2}:[0-9]{2} UTC',text):
                datetime.datetime.strptime(text,'%H:%M UTC')
            elif text.endswith(' UTC'):
                datetime.datetime.strptime(text,'%Y-%m-%d %H:%M:%S UTC')
            else:
                value=datetime.datetime.fromisoformat(text.replace('Z','+00:00'))
                need(value.utcoffset()==datetime.timedelta(0),'append timestamp is not UTC')
        except ValueError:raise Invalid('append timestamp has an invalid calendar date or UTC time')
    def parse(raw):
        if not raw:return []
        starts=[m.start() for m in re.finditer(rb'^## ',raw,re.M)]
        need(starts and raw[:starts[0]] and not raw[:starts[0]].strip(b'\n') and raw.endswith(b'\n') and not raw.endswith(b'\n\n'),'append suffix lacks whole entries or exact terminal newline')
        boundaries=[0]
        for i in starts[1:]:
            j=i
            while j>0 and raw[j-1:j]==b'\n':j-=1
            need(i-j>=2,'appended entries lack blank-line separation')
            boundaries.append(j+1)  # retain one newline on the preceding body
        blocks=[raw[a:b] for a,b in zip(boundaries,boundaries[1:]+[len(raw)])]
        for block in blocks:
            body=block.lstrip(b'\n');m=re.match(heading,body)
            need(len(block)>len(body) and m is not None and block.endswith(b'\n') and body[len(m.group(0)):].strip(),'append entry heading/body/boundary invalid')
            valid_stamp(m.group('stamp'))
        return blocks
    base_headings={x for x in base.splitlines() if x.startswith(b'## ')}
    allblocks={};seqs=[]
    for tip in [coordinator,lane]:
        need(tip.startswith(base),'work-log changed pre-existing bytes instead of whole append')
        blocks=parse(tip[len(base):]);keys=[]
        for b in blocks:
            key=b.lstrip(b'\n').splitlines()[0];need(key not in base_headings and key not in keys,'duplicate append/base heading')
            need(key not in allblocks or allblocks[key]==b,'same append heading has conflicting entry bytes')
            allblocks[key]=b;keys.append(key)
        seqs.append(keys)
    edges={k:set() for k in allblocks};degree={k:0 for k in allblocks}
    for seq in seqs:
        for a,b in zip(seq,seq[1:]):
            if b not in edges[a]:edges[a].add(b);degree[b]+=1
    ordered=[]
    while degree:
        ready=sorted(k for k,v in degree.items() if v==0);need(ready,'append entry orders conflict')
        k=ready[0];ordered.append(k);degree.pop(k)
        for b in edges[k]:degree[b]-=1
    for seq in seqs:need([k for k in ordered if k in seq]==seq,'append sequence not preserved')
    merged=base+b''.join(allblocks[k] for k in ordered)
    need(parse(merged[len(base):])==[allblocks[k] for k in ordered],'whole append bytes lost')
    return merged,[[sha(allblocks[k]) for k in seq] for seq in seqs]
