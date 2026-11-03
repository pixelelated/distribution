#!/usr/bin/env python3
"""Bounded T46 documentary reader. No record text is executed; no traversal."""
import argparse,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[2]
PREP=REPO/'docs/qa-logs/2026-11-03-m6-records-preparation'
SOURCE='d707c82ab8c48b674acc1f95a9571f0cb24d226a'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def blob(path):return git('show',SOURCE+':'+path)
def mask(line):
    # Conservative line mask: metadata carries only line numbers, never a sensitive spelling.
    return '[MASKED sensitive-labelled line; not read unredacted]' if re.search(r'credential|secret|password|passwd|private.key|\btoken\b|\bpsk\b|api.key',line,re.I) else line
spec=importlib.util.spec_from_file_location('t46_day_range',PREP/'day-range.py');day=importlib.util.module_from_spec(spec);spec.loader.exec_module(day)
def selected(path):
    raw=blob(path);text=raw.decode('utf-8');lines=text.splitlines()
    if path.startswith('docs/work-logs/') and path!='docs/work-logs/INDEX.md':
        r=day.select(text); ranges=[[r['start_inclusive'],r['end_exclusive']]];kind='bounded-day-entry'
    elif path=='docs/work-logs/INDEX.md':
        ranges=[[i,i+1] for i,l in enumerate(lines,1) if re.match(r'^#{1,6}\s',l) or re.search(r'\]\([^)]*\)',l)];r={'headings_links_only':True};kind='index-metadata'
    elif path=='docs/reviews/inventory.json':
        obj=json.loads(text);r={'top_keys':list(obj),'metadata':{k:v for k,v in obj.items() if not isinstance(v,list) and k not in ['files','paths','entries','inventory']},'row_collections':{k:len(v) for k,v in obj.items() if isinstance(v,list)}};ranges=[];kind='inventory-schema-only'
    elif path=='.github/sessions/saved-session-state-next.md':
        # Explicit whole-file route: title/frontmatter and navigation/status, not embedded transcripts.
        ranges=[[1,min(len(lines)+1,121)]];r={'selection':'front-matter/start-here/status first120; remaining bodies unread'};kind='historical-pointer'
    else:ranges=[[1,len(lines)+1]];r={'selection':'named-prose-entrypoint'};kind='prose-entrypoint'
    indexes=[n for start,end in ranges for n in range(start,end)]
    masked=[n for n in indexes if mask(lines[n-1])!=lines[n-1]]
    return {'path':path,'source':SOURCE,'oid':git('rev-parse',SOURCE+':'+path).decode().strip(),'sha256':sha(raw),'bytes':len(raw),'logical_lines':len(lines),'ranges':ranges,'kind':kind,'selector':r,'masked_lines':masked,'whole_file_read':False,'read_status':'pending-human-reading'},lines

def prepare():
    routes=json.loads((PREP/'reader-routes.json').read_text());entries=json.loads((PREP/'p1-routes/entrypoints.json').read_text())
    paths=list(dict.fromkeys([x['path'] for x in entries]+routes['summary']['paths']))
    rows=[]
    for path in paths:
        if path=='docs/retros':
            rows.append({'path':path,'source':SOURCE,'oid':git('rev-parse',SOURCE+':'+path).decode().strip(),'kind':'directory-metadata','ranges':[],'whole_file_read':False,'read_status':'metadata-only','purpose':'Historical retro directory; named README separately inspected; descendants not traversed'});continue
        r,_=selected(path);rows.append(r)
    out=ROOT/'stage-b';out.mkdir(exist_ok=True)
    (out/'ranges.json').write_text(json.dumps(rows,indent=2)+'\n')
    (out/'route-inputs.json').write_text(json.dumps(routes,indent=2)+'\n')
    print('Prepared',len(rows),'distinct entrypoint/target records; source',SOURCE)
    for i,r in enumerate(rows):print(i,r['path'],r['kind'],str(r.get('ranges'))[:100],r.get('selector',{}).get('truncated',False))
def show(ids,start,end):
    rows=json.loads((ROOT/'stage-b/ranges.json').read_text())
    for i in ids:
        old=rows[i];print('\nTARGET',i,old['path'],old['kind'])
        if old['kind']=='directory-metadata':print(json.dumps(old));continue
        row,lines=selected(old['path']);assert row['sha256']==old['sha256']
        print('IDENTITY',row['oid'],row['sha256'],'RANGES',row['ranges'],'MASKED',row['masked_lines'])
        if row['kind']=='inventory-schema-only':print(json.dumps(row['selector'],indent=2));continue
        for a,b in row['ranges']:
            for n in range(max(a,start),min(b,end)):
                l=lines[n-1]
                if row['kind']=='index-metadata' and not l.startswith('#'):
                    # Render destinations only; suppress narrative titles beyond heading metadata.
                    l='LINKS '+str(re.findall(r'\]\(([^)]*)\)',l))
                print(str(n)+': '+mask(l))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','show']);ap.add_argument('ids',nargs='*',type=int);ap.add_argument('--start',type=int,default=1);ap.add_argument('--end',type=int,default=1000000);args=ap.parse_args()
    if args.action=='prepare':prepare()
    else:show(args.ids,args.start,args.end)
