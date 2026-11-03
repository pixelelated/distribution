"""Only heading coordinates/digests; no body or heading-title export."""
import hashlib,json,pathlib,re,subprocess
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];rows=[]
for item in json.loads((A/'stage-b/ranges.json').read_text()):
 if item['kind']!='bounded-day-entry':continue
 b=subprocess.check_output(['git','show',item['source']+':'+item['path']],cwd=R);heads=[];fence=None
 for n,line in enumerate(b.decode().splitlines(),1):
  if fence:
   if re.fullmatch(r' {0,3}'+re.escape(fence[0])+'{'+str(fence[1])+r',}\s*',line):fence=None
   continue
  m=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$',line)
  if m and (m[1][0]!='`' or '`' not in m[2]):fence=(m[1][0],len(m[1]));continue
  m=re.match(r'^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$',line)
  if m:
   title=re.sub(r'[ \t]+#+[ \t]*$','',m[2]).strip();heads.append({'line':n,'level':len(m[1]),'title_sha256':hashlib.sha256(title.encode()).hexdigest()})
 rows.append({'path':item['path'],'source':item['source'],'oid':item['oid'],'source_sha256':hashlib.sha256(b).hexdigest(),'headings':heads,'unclosed_fence':fence is not None,'reading_credit':'metadata only; no earlier entry body credit'})
p=A/'stage-b/heading-metadata.json'
if p.exists():raise SystemExit('refuse overwrite')
p.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n');print('PASS all ATX heading metadata outside fences: '+str(len(rows))+' bounded day targets; no title/body export')
