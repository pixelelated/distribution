import ast, pathlib, subprocess, hashlib, json, argparse
p=argparse.ArgumentParser()
p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--output',type=pathlib.Path,required=True)
a=p.parse_args();repo=a.repo.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
path='projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'
manifest={'kind':'host Node synthetic transport control; no VM/device/browser runtime','sources':[]}
for name,ref in [('before','bc2dceb406^'),('accepted','bc9dfe8141d9561dc1d8502313d00a84c4566ee8')]:
    sha=subprocess.check_output(['git','rev-parse',ref],cwd=repo,text=True).strip()
    src=subprocess.check_output(['git','show',sha+':'+path],cwd=repo)
    tree=ast.parse(src)
    assignments={t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
    html=ast.literal_eval(assignments['REMOTE_PAGE']) % {'style':'','name':'Synthetic QA','pin':'1234'}
    (out/(name+'.html')).write_text(html)
    manifest['sources'].append({'case':name,'commit':sha,'path':path,'sha256':hashlib.sha256(src).hexdigest(),'html_sha256':hashlib.sha256(html.encode()).hexdigest()})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
