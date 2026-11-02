from pathlib import Path
import subprocess, json, collections, hashlib, csv, sys
ROOT=Path(__file__).parent
REV='2c6885a54f'
T40='88a648da0d'
def show(path, rev=REV):
    return subprocess.check_output(['git','show',rev+':'+path])
folder='docs/audits/2026_10_25-epic-m6-patches-dead/'
text=show(folder+'02-forward-audit.md',T40).decode()
section=text.split('## The shadowed 74\n',1)[1].split('\n## ',1)[0]
leads=[]
for line_no,line in enumerate(text.splitlines(),1):
    if line in section.splitlines() and '; no counterpart in the override' in line:
        row=[c.strip(' `') for c in line.split('|')[1:-1]]
        leads.append(dict(zip(['override','patch','subject','t40_disposition'],row),t40_line=line_no))
inv=json.loads(show('docs/reviews/inventory.json'))
rows={r[1]:dict(zip(inv['columns'],r)) for r in inv['rows'] if r[0]=='distribution'}
owner_map={'generic-packages':('T8 #655','f50a031158'),'os-scripts-and-launch':('T22 #669','cbab6483dc'),'devices':('T27 #674','0ac98afe43')}
qpath='docs/audits/2026_10_24-epic-m6-image-packages/q4-table.md'
qrows={}
for n,line in enumerate(show(qpath,'f50a031158').decode().splitlines(),1):
    if line.startswith('| `projects/'):
        cols=[c.strip(' `') for c in line.split('|')[1:-1]]
        qrows[cols[0]]=(n,cols)
for lead in leads:
    recipe=lead['override']+'/package.mk'
    owner,accepted=owner_map[rows[recipe]['area']]
    lead.update(recipe_owner=owner,accepted_recipe_tip=accepted,
        shadowed_patch_unchanged=show(lead['patch'],T40)==show(lead['patch']),
        recipe_unchanged_from_acceptance=show(recipe,accepted)==show(recipe))
    if recipe in qrows:
        n,cols=qrows[recipe]
        lead.update(prior_evidence=f'{accepted}:{qpath}:{n}',prior_pin=cols[2],prior_disposition=cols[7])
    elif owner=='T22 #669':
        name=lead['override'].split('/')[-1]
        lead.update(prior_evidence='cbab6483dc:docs/audits/2026_10_25-epic-m6-os-system-services/05-punch-list.md:PL-15',prior_pin={'busybox':'1.36.1','systemd':'255.8','util-linux':'2.39.2'}[name],prior_disposition='Recorded: settled by the next base merge; this does not resolve the inherited patch question.')
    else:
        lead.update(prior_evidence='0ac98afe43:docs/audits/2026_10_25-epic-m6-device-h700/02-forward-audit.md:71-73',prior_pin='wrapper 1.0; DDR3/DDR4 v2026.01',prior_disposition='T27 PL-01 recorded: version pins equal then-local upstream; author releases CANNOT (no network).')
with (ROOT/'leads.tsv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(leads[0]),delimiter='\t');w.writeheader();w.writerows(leads)
groups=collections.defaultdict(list)
for lead in leads:groups[lead['override']].append(lead)
summary={'lead_rows':len(leads),'overrides':len(groups),'owner_leads':dict(collections.Counter(r['recipe_owner'] for r in leads)),'owner_overrides':dict(collections.Counter(rs[0]['recipe_owner'] for rs in groups.values())),'changed_shadowed_patches':sum(not r['shadowed_patch_unchanged'] for r in leads),'changed_override_recipes':sum(not rs[0]['recipe_unchanged_from_acceptance'] for rs in groups.values()),'t40_forward_sha256':hashlib.sha256(show(folder+'02-forward-audit.md',T40)).hexdigest()}
(ROOT/'counts.json').write_text(json.dumps(summary,indent=2)+'\n')
table=['| Override (relative to projects/ROCKNIX/) | Leads | Recipe owner | Accepted pin / prior disposition evidence |','| --- | ---: | --- | --- |']
for override,rs in groups.items():
    r=rs[0]
    if r['recipe_owner']=='T8 #655': evidence=f"{r['prior_pin']}; T8 q4 row {qrows[override+'/package.mk'][0]}, follows base merge"
    elif r['recipe_owner']=='T22 #669':evidence=f"{r['prior_pin']}; T22 PL-15 recorded, next base merge"
    else:evidence=r['prior_pin']+'; T27 PL-01 recorded'
    table.append(f"| `{override.removeprefix('projects/ROCKNIX/')}` | {len(rs)} | {r['recipe_owner']} | {evidence} |")
(ROOT/'ownership-table.md').write_text('\n'.join(table)+'\n')
print(json.dumps(summary,indent=2))
