#!/usr/bin/env python3
"""Classify the existing finite extraction using root-supplied selectors.
Private packet reads only. No subprocess, Git, network or repository reads.
"""
import collections,hashlib,json,pathlib
OUT=pathlib.Path(__file__).parent
SOURCE=OUT.parent
INPUTS=['routes.json','target-metadata.json','entrypoints.json','summary.json','structural-findings.json','syntax-limits.md','extract.py']
EXPECTED={
 'routes.json':'78d636e1527994244c27d13f12e709d3c3eba188472e36e5c28bbb7ff5f74666',
 'extract.py':'be6fd1ce1d3a901ba942cbcfaca90b1357c5af97f3c8a2b4261cd469a22fdbe4'
}
def sha(b):return hashlib.sha256(b).hexdigest()
def js(b):return json.loads(b)
def write(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
    data={n:(SOURCE/n).read_bytes() for n in INPUTS}
    old_manifest={line.split(None,1)[1]:line.split(None,1)[0] for line in (SOURCE/'SHA256SUMS').read_text().splitlines()}
    assert sha((SOURCE/'SHA256SUMS').read_bytes())=='7471749cec9d4f3a6b9e3a3bb3e98d2a5041e1ec3a72ba262fa5575c96964f70'
    for n,b in data.items():assert sha(b)==old_manifest[n] and (n not in EXPECTED or sha(b)==EXPECTED[n]),n
    cfgb=(OUT/'records-roots.json').read_bytes();cfg=js(cfgb)
    roots=cfg['roots'];singletons=cfg['singletons'];assert len(roots)==9 and len(singletons)==1
    rows=js(data['routes.json']);metadata=js(data['target-metadata.json']);entrypoints=js(data['entrypoints.json']);summary=js(data['summary.json'])
    def match(path):
        if path in singletons:return path,'exact-singleton'
        for root in roots:
            if path==root.rstrip('/'):return root,'directory-root'
            if path.startswith(root):return root,'directory-descendant'
        return None,'outside-records'
    changed=0
    for row in rows:
        path=row.get('resolved_path')
        if path is None:continue
        assert row['classification']=='literal-root-classification-pending'
        scope,kind=match(path);row['records_root']=scope;row['selector_match']=kind
        row['classification']='literal-records-route' if scope else 'literal-context-outside-records';changed+=1
    assert changed==500 and len(rows)==796
    # Only classification/membership labels change; original syntax, spelling,
    # source coordinates, normalization, paths/anchors/suffixes and IDs stay exact.
    untouched=['entrypoint','line','column','spelling','syntax','context','heading','syntax_note','anchor','line_suffix','resolved_path','resolution_basis','example','id']
    before=js(data['routes.json'])
    assert all(all(a.get(k)==b.get(k) for k in untouched) for a,b in zip(rows,before))
    selected=[x for x in rows if x['classification']=='literal-records-route'];paths=sorted({x['resolved_path'] for x in selected})
    groups={}
    for group in roots+singletons:
        rr=[x for x in selected if x['records_root']==group];pp={x['resolved_path'] for x in rr}
        groups[group]={'occurrences':len(rr),'unique_targets':len(pp),'ordinary_files':sum(metadata[p].get('mode') in ['100644','100755'] for p in pp),'trees':sum(metadata[p].get('type')=='tree' for p in pp),'missing':sum(metadata[p].get('missing',False) for p in pp),'unique_target_blob_bytes':sum(metadata[p].get('bytes') or 0 for p in pp)}
    for e in entrypoints:
        root,kind=match(e['path']);e['records_root']=root;e['selector_match']=kind;e['entrypoint_in_records']=bool(root)
    result={
        'ref':summary['ref'],'classification_authority':cfg['authority'],
        'original_manifest_sha256':sha((SOURCE/'SHA256SUMS').read_bytes()),
        'original_inputs':{n:{'sha256':sha(b),'bytes':len(b)} for n,b in data.items()},
        'selector_input':{'sha256':sha(cfgb),'bytes':len(cfgb)},
        'occurrence_count':len(rows),'classified_literal_occurrences':changed,
        'by_class':dict(collections.Counter(x['classification'] for x in rows)),
        'records_occurrences':len(selected),'records_unique_targets':len(paths),
        'records_unique_ordinary_files':sum(metadata[p].get('mode') in ['100644','100755'] for p in paths),
        'records_unique_trees':sum(metadata[p].get('type')=='tree' for p in paths),
        'records_unique_missing':sum(metadata[p].get('missing',False) for p in paths),
        'records_unique_path_sha256':sha(('\n'.join(paths)+'\n').encode()),
        'records_unique_file_path_sha256':sha(('\n'.join(p for p in paths if metadata[p].get('type')=='blob')+'\n').encode()),
        'records_unique_blob_bytes':sum(metadata[p].get('bytes') or 0 for p in paths),
        'records_groups':groups,
        'entrypoints_in_records':[e['path'] for e in entrypoints if e['entrypoint_in_records']],
        'preserved_limitations':summary['limits'],
        'suppressed_occurrences':summary['suppressed_occurrences'],
        'suppressed_metadata_sha256':summary['suppressed_metadata_sha256'],
        'new_repository_or_target_body_reads':0,
        'checks':{'source_manifest_and_input_hashes_match':True,'same_796_occurrences':True,'exactly_500_literal_labels_classified':True,'all_original_route_evidence_unchanged':True,'singleton_uses_equality_not_prefix':True,'no_unresolved_shorthand_promoted':True}
    }
    write('routes.json',rows);write('entrypoints.json',entrypoints);write('results.json',result)
    write('record-targets.json',{p:metadata[p] for p in paths})
    cols=['entrypoint','line','column','spelling','syntax','context','resolution_basis','records_root','selector_match','resolved_path','anchor','line_suffix','mode','type','oid','bytes','tree_object_bytes','missing']
    lines=['\t'.join(cols)]
    for x in selected:
        v={**x,**metadata[x['resolved_path']]};lines.append('\t'.join(str(v.get(k,'')).replace('\t','\\t').replace('\n','\\n') for k in cols))
    (OUT/'record-routes.tsv').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['original_inputs','preserved_limitations']},indent=2))
if __name__=='__main__':main()
