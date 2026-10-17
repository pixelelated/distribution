#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Snapshot one case privately; export fixed-schema diagnostics only. No signals."""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/storage/qa616-provider')
HELPER_SHA = '8c3a9ba06dc78efffee68bb510b5f273f2fafc8d2ecbc8ee17227a3e4c1e3f0a'
ANALYSE_SHA = 'a6a16162cd828ff9f1d8c2499706a9ede3ba1b4e505743ce0dc35e970a7302e7'
ES_SHA = '76f18d97a46e9228ca4b7cb63a5406a4f0bb026f96763f3558d1ac942b1857c8'
SAMPLE = {'elapsed_ms':360000,'eval_roundtrip_ms':360000,'ready':2,'foreground':1,
    'width':32768,'height':32768,'scale':32,'visible_text_inputs':128,'hittable_text_inputs':128,
    'checked_inputs':129,'heartbeat_ticks':10000000,'last_gap_ms':3600000,'max_gap_ms':3600000}
REASONS = {'log-size','memory','deadline','children-outlived-helper','guard-followup','guard-exit'}


def sha(data): return hashlib.sha256(data).hexdigest()


def number(value, maximum=1e16, minimum=0):
    if type(value) not in (int,float) or not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError('numeric schema')
    return value


def identity(value):
    result = {'pid':number(value['pid'],4194304,1),'start':number(value['start'])}
    if 'ppid' in value: result['ppid']=number(value['ppid'],4194304)
    return result


def process(pid):
    try:
        fields=Path('/proc',str(int(pid)),'stat').read_text().rsplit(')',1)[1].split()
        if fields[0]=='Z': return None
        return {'pid':int(pid),'start':int(fields[19]),'ppid':int(fields[1])}
    except (FileNotFoundError,ProcessLookupError): return None


def same(value):
    current=process(value['pid'])
    return bool(current and current['start']==value['start'])


def read(path, maximum):
    descriptor=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        before=os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_uid!=0 or before.st_size>maximum:
            raise ValueError('private input bound or ownership')
        with os.fdopen(descriptor,'rb',closefd=False) as stream: data=stream.read(maximum+1)
        after=os.fstat(descriptor)
        if len(data)>maximum: raise ValueError('private input grew beyond bound')
        return data, before.st_size==after.st_size==len(data) and before.st_mtime_ns==after.st_mtime_ns
    finally: os.close(descriptor)


def obj(path,maximum=65536): return json.loads(read(path,maximum)[0])


def mkdir(path):
    if path.exists():
        metadata=path.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid!=0 or metadata.st_mode&0o077:
            raise ValueError('output directory is not private')
    else: path.mkdir(mode=0o700)


def write(path,value):
    with path.open('x') as stream:
        json.dump(value,stream,indent=2);stream.write('\n')


def receipt(value,case):
    expected={'schema','case','pid','start','helper_sha256','exec_argv0','private_oauth_url_recorded','page_replaced_for_light_control'}
    if set(value)!=expected or value['schema']!=1 or set(value['case'])!={'id','provider','ua','observer'}: raise ValueError('receipt schema')
    c=value['case']
    if c['id']!=case or c['provider'] not in ['light','dropbox','drive','onedrive'] or c['ua'] not in ['default','desktop'] or c['observer'] not in ['off','on']: raise ValueError('case schema')
    if value['helper_sha256']!=HELPER_SHA or value['exec_argv0']!='/usr/bin/cloud-signin-window' or value['private_oauth_url_recorded'] is not False or value['page_replaced_for_light_control'] is not (c['provider']=='light'): raise ValueError('receipt binding')
    return {'schema':1,'case':dict(c),**identity(value),'helper_sha256':HELPER_SHA,
        'exec_argv0':'/usr/bin/cloud-signin-window','private_oauth_url_recorded':False,
        'page_replaced_for_light_control':c['provider']=='light'}


def sanitise(raw,analyse):
    records=[];rejected=ignored=0
    for line in raw.decode('utf-8',errors='replace').splitlines():
        tag,_,body=line.partition(' ')
        if not line.startswith('QA616_'): ignored+=1;continue
        try:
            if len(line)>2048 or len(records)>=512: raise ValueError('record bound')
            if tag in analyse.SCHEMAS:
                records.append(analyse.validate(tag,json.loads(body)))
            elif tag=='QA616_SAMPLE':
                data=json.loads(body)
                if set(data)!=set(SAMPLE):raise ValueError('sample schema')
                records.append({'tag':tag,**{k:number(data[k],bound,-1) for k,bound in SAMPLE.items()}})
            elif tag=='QA616_CONFIG':
                m=re.fullmatch(r'ua=(default|desktop|custom) observer=(off|on) effective_ua_sha256=([0-9a-f]{64}) engine=([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})',body)
                if not m:raise ValueError('config schema')
                records.append({'tag':tag,'ua':m[1],'observer':m[2],'effective_ua_sha256':m[3],'engine':[int(m[4]),int(m[5]),int(m[6])]})
            elif tag=='QA616_PROOF_CONFIG':
                m=re.fullmatch(r'event_probe=on periodic_observer=(off|on) request_header=unvalidated',body)
                if not m:raise ValueError('probe schema')
                records.append({'tag':tag,'event_probe':'on','periodic_observer':m[1],'request_header':'unvalidated'})
            elif tag=='QA616_EVAL_ERROR':
                m=re.fullmatch(r'elapsed_ms=([0-9]+\.[0-9]{3}) eval_roundtrip_ms=([0-9]+\.[0-9]{3})',body)
                if not m:raise ValueError('error schema')
                records.append({'tag':tag,'elapsed_ms':number(float(m[1]),360000),'eval_roundtrip_ms':number(float(m[2]),360000)})
            else: rejected+=1
        except (ValueError,TypeError,KeyError,OverflowError): rejected+=1
    return records,rejected,ignored


def guard(case):
    result={'scope':'snapshot; not terminal guard acceptance','interventions':[],'samples':[]}
    heartbeat=ROOT/'guard-heartbeat.json'
    if heartbeat.exists():
        data=obj(heartbeat)
        selected={k:number(data[k]) for k in ['at','pid','start','verified_cases','interventions']}
        result['heartbeat']=selected;result['heartbeat_age_seconds']=max(0,time.monotonic()-selected['at'])
        result['guard_identity_live']=same(selected)
    samples=ROOT/'guard-samples.jsonl'
    if samples.exists():
        data,_=read(samples,4*1024**2)
        for line in data.splitlines():
            try:
                row=json.loads(line)
                selected=[c for c in row['cases'] if c['id']==case]
                if not selected:continue
                result['samples'].append({'at':number(row['at']),
                    'memory_kib':{k:number(row['mem'][k],1e12) for k in ['MemAvailable','MemFree','SwapTotal','SwapFree']},
                    'cases':[{'id':case,'identity':identity(c['identity']),
                              'verified_at':None if c['verified_at'] is None else number(c['verified_at']),
                              'owned_live':[identity(x) for x in c['owned_live']]} for c in selected]})
            except (ValueError,TypeError,KeyError):result['incomplete_sample_lines']=result.get('incomplete_sample_lines',0)+1
        if len(result['samples'])>1200:raise ValueError('guard sample bound')
    events=ROOT/'guards.jsonl'
    if events.exists():
        raw,_=read(events,1048576)
        for line in raw.splitlines():
            event=json.loads(line)
            if event.get('case')!=case:continue
            if event['action'] not in ['guard-TERM','guard-KILL'] or event['reason'] not in REASONS:raise ValueError('guard event schema')
            result['interventions'].append({'at':number(event['at']),'case':case,'reason':event['reason'],
                'identity':identity(event['identity']),'action':event['action']})
    terminal=ROOT/'guard-result.json'
    if terminal.exists():
        data=obj(terminal)
        errors={None,'AssertionError','TimeoutError','ValueError','OSError','RuntimeError','FileNotFoundError'}
        result['terminal']={'rc':number(data['rc'],1),'elapsed':number(data['elapsed'],1200),
            'error_present':data['error_class'] is not None,
            'known_error_class':data['error_class'] if data['error_class'] in errors else 'other',
            'survivors':[identity(x) for x in data['survivors']],
            'intervention_count':len(data['interventions'])}
    return result


def es_identity():
    executable=Path('/usr/bin/emulationstation')
    with executable.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    rows=[]
    for path in Path('/proc').iterdir():
        if not path.name.isdigit():continue
        try:
            # Exact executable identity, never process argv or environment.
            if os.readlink(path/'exe')!='/usr/bin/emulationstation':continue
            value=process(int(path.name))
            if value:rows.append(value)
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
    return {'installed_sha256':digest,'matches_clean_gate_sha256':digest==ES_SHA,'processes':rows,
        'renderer_resumed_or_normal_handoff_proven':False}


def main(args):
    if os.geteuid()!=0 or os.uname().machine!='x86_64':raise ValueError('disposable guest only')
    if not re.fullmatch('[a-z0-9-]{1,64}',args.case) or not re.fullmatch('[a-z0-9-]{1,24}',args.snapshot):raise ValueError('fixed identifier invalid')
    os.umask(0o077)
    analysis_path=Path(__file__).resolve().parent/'analyse.py'
    if sha(analysis_path.read_bytes())!=ANALYSE_SHA:raise ValueError('analysis source binding')
    spec=importlib.util.spec_from_file_location('reviewed_analysis',analysis_path)
    analyse=importlib.util.module_from_spec(spec);spec.loader.exec_module(analyse)
    value=receipt(obj(ROOT/'launches'/(args.case+'.json')),args.case)
    current=obj(Path('/run/qa616-provider/current.json'))
    if current!=value['case']:raise ValueError('selected case changed; archive attribution refused')
    for base in [ROOT/'private',ROOT/'sanitized']:
        mkdir(base);mkdir(base/args.case)
        (base/args.case/args.snapshot).mkdir(mode=0o700)
    private=ROOT/'private'/args.case/args.snapshot
    output=ROOT/'sanitized'/args.case/args.snapshot
    raw,stable=read(Path('/var/run/cloud_oauth/window.log'),2*1024**2)
    with (private/'window.log').open('xb') as stream:stream.write(raw)
    write(private/'receipt.json',value)
    if obj(Path('/run/qa616-provider/current.json'))!=current:raise ValueError('case changed during snapshot')
    records,rejected,ignored=sanitise(raw,analyse)
    with (output/'proof.jsonl').open('x') as stream:
        for row in records:stream.write(json.dumps(row,separators=(',',':'))+'\n')
    proof=[row for row in records if row['tag'] in analyse.SCHEMAS]
    try:summary=analyse.summarise(proof)
    except (ValueError,TypeError,KeyError):summary={'schema':1,'summary_refused':True,'reason':'inconsistent fixed-schema proof sequence'}
    write(output/'analysis.json',summary)
    write(output/'launch-receipt.json',value)
    write(output/'guard.json',guard(args.case))
    write(output/'es-identity.json',es_identity())
    meta={'schema':1,'case':args.case,'snapshot':args.snapshot,'raw_log_archived_privately':True,
        'raw_log_bytes':len(raw),'raw_log_sha256':sha(raw),'raw_log_stable_during_read':stable,
        'helper_identity_live_at_snapshot':same(value),'sanitized_records':len(records),
        'rejected_diagnostic_lines':rejected,'ignored_native_lines':ignored,
        'snapshot_is_terminal_result':False,'urls_pins_cookies_field_values_exported':False,
        'raw_log_must_not_be_exported':True}
    write(output/'snapshot.json',meta)
    files=sorted(p for p in output.iterdir() if p.is_file())
    (output/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in files))
    print(json.dumps({'status':'SNAPSHOT_WRITTEN','case':args.case,'snapshot':args.snapshot,
        'sanitized_records':len(records),'rejected_diagnostic_lines':rejected,
        'export_relative':'sanitized/'+args.case+'/'+args.snapshot,'raw_archive_private':True}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',required=True)
    parser.add_argument('--snapshot',default='capture01')
    try:main(parser.parse_args())
    except Exception as error:
        print(json.dumps({'status':'REFUSED','error_class':type(error).__name__}),file=sys.stderr)
        raise SystemExit(1)
