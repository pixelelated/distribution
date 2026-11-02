#!/usr/bin/env python3
"""Validate T43 source-bound table input and render exact native provenance/coverage."""
import collections,gzip,hashlib,json,pathlib,re,sys
R=pathlib.Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
 b=pathlib.Path(p).read_bytes();return json.loads(gzip.decompress(b) if str(p).endswith('.gz') else b)
def assert_input(rows):
 expected=load(R/'stage-b/observations.json');by={x['path']:x for x in expected};links={x['path']:x for x in load(R/'stage-b/links.json')['native']}
 assert len(rows)==432 and len({x['path'] for x in rows})==432 and set(x['path'] for x in rows)==set(by),'membership: exact 432 native keys'
 for x in rows:
  e=by[x['path']];assert x['kind']==e['kind'],'kind: '+x['path']
  assert (x['mode'],x['oid'],x['sha256'],x['lines'])==(e['mode'],e['oid'],e['sha256'],e['lines']),'source identity: '+x['path']
  if e['kind']=='symlink':assert x['link']==links[x['path']],'link/referent identity: '+x['path']
  else:assert x['link']=='not a symlink','link classification: '+x['path']
  assert x['header']==e['header'] and x['origin']==origin(e),'header attribution: '+x['path']
  assert x['disposition'] in ['keep','upstream-changed','upstream-moved','superseded-at-pin','inherited','bug','contribution-draft','open-item'],'disposition'
  for k in ['recipe_pins','selected_stack','origin','target_summary','application','upstream_status','backport_status','carrying_reason','next_owner','receipts','coverage']:
   assert isinstance(x[k],str) and x[k].strip(),'empty '+k+': '+x['path']
 assert sum(x['lines'] for x in rows)==328516,'line census'
def origin(e):
 h=e['header'];claimed=[f'L{n}: {t}' for n,t in h if re.match(r'From:|Author:|Subject:|Date:|Signed-off-by:|commit ',t)]
 if e['kind']=='config':return 'Generated source header: '+next((t for n,t in h if 'Kernel Configuration' in t),'header unknown')+'; generator/toolchain strings are source claims'
 if e['kind']=='symlink':return 'Literal symlink; attribution belongs to separately bound referent, not link filename'
 return ('Literal header claims: '+' / '.join(claimed) if claimed else 'No recognized mail/author/commit attribution in extracted header; original author not established')+'; no external origin verification'
def cell(v):return str(v).replace('|','\\|').replace('\n','<br>')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+''.join('| '+' | '.join(cell(c) for c in row)+' |\n' for row in rows)
def render(rows):
 out='# Forward audit — T43 patches-unshipped\n\nActual reader: Codex / GPT-6-Astra / xhigh (OpenAI), Local. Source afdec2bf8b88135befcb7ec56efb3a7ea327bd73, seed 601e4694f9726b2228d3571efdb5cfc061c6d442.\n\n432 vendor-carried native path rows / 328,516 logical lines. Zero fork-written. Header/target/selection extraction and grouped review; no line-by-line reading of vendor bodies. Every application result is a complete normal patch call on the selected target-member projection; it is neither a compile nor runtime correctness proof. Both time-to-play quantities remain unmeasured.\n\n## Provenance\n\n'
 headers=['Path','Kind','Mode / link / referent','Inventory lines','Recorded consumers','Source recipe / owner / pin per plan','Selected stack','Origin / header evidence','Target summary','Application / config evidence and limits','Fixed upstream identity / status','Backport status','Carrying reason','Disposition','Next owner / action','Receipts']
 out+=table(headers,[[x['path'],x['kind'],x['mode']+'; '+(json.dumps(x['link'],sort_keys=True) if isinstance(x['link'],dict) else x['link'])+'; blob '+x['oid'],x['lines'],', '.join(x['buildable_by']),x['recipe_pins'],x['selected_stack'],x['origin'],x['target_summary'],x['application'],x['upstream_status'],x['backport_status'],x['carrying_reason'],x['disposition'],x['next_owner'],x['receipts']] for x in rows])
 out+='\n## Coverage\n\n'+table(['Path','Actual coverage','Evidence / limits','Next owner'],[[x['path'],x['coverage'],x['receipts']+'; '+x['application'],x['next_owner']] for x in rows])
 configs=load(R/'stage-b/configurations.json');plans=load(R/'stage-b/plans.json')
 out+='\n## Configuration inputs (12)\n\n'+table(['Path','Source header / pin','Base / fixed upstream','Selected config path / static writers','Missing evidence / owner'],[[x['path'],next(t for n,t in x['header'] if 'Kernel Configuration' in t)+'; '+', '.join(sorted({p['pin'] for p in plans if x['path'] in p['config_paths']})),str(x['base_identical'])+'; '+x['source_to_upstream_numstat']+'; upstream SHA256 '+x['upstream_sha256'],x['selected_path']+'; kernel recipe writers '+', '.join('L'+str(n) for n,t in x['static_writers'])+'; complete text configurations.json',x['missing']+'; '+x['owner']] for x in configs])
 recipes=load(R/'stage-b/recipes.json');out+='\n## Recipe context (31; existing owners)\n\n'+table(['Recipe','Identity / owner','Conditional source pins by plan','Preimage limits'],[[rp,v['sha256']+'; '+', '.join(v['owner']),'; '.join(p['consumer']+'='+p['pin'] for p in plans if p['recipe']==rp),'; '.join(sorted({s for p in plans if p['recipe']==rp for s in p['preimage_limits']})) or 'No extra pre-patch hook/overlay in first census; actual cache/application qualification is per group'] for rp,v in recipes.items()])
 links=load(R/'stage-b/links.json');out+='\n## Symlinks (2 native) and shared shipped consumer\n\n'+table(['Native path','Literal target / referent','Identity / owner'],[[x['path'],x['target']+' -> '+x['resolved'],x['link_tree']+'; '+x['referent_tree']+'; SHA256 '+x['sha256']+'; T43 #690'] for x in links['native']])+ '\nT42-only consumer: '+json.dumps(links['shipped_context'])+'. It does not move either native referent out of T43.\n'
 out+='\n## Coverage boundary\n\nMechanical extraction is exhaustive for native keys, modes, hashes, header/target lines, fixed-base/upstream identity and selected stack entries. The primary read selector/recipe mechanisms and grouped header/target evidence, plus the named prior context after initial observations. Vendor bodies were not read line by line. Current component releases, compilation, generated configuration and runtime behavior were not verified. Source application is bounded to the exact input and target projection in each receipt. No source ownership, removal, shipped-set or contribution decision changes.\n'
 return out
if __name__=='__main__':
 rows=load(sys.argv[1]);assert_input(rows)
 if '--output' in sys.argv:pathlib.Path(sys.argv[sys.argv.index('--output')+1]).write_text(render(rows))
 print('PASS exact 432 native Provenance and Coverage rows; modes, kinds, links and literal header attribution bound')
