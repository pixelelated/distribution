from pathlib import Path
import json,sys,traceback
p=Path(__file__).with_name('fixture-original.py')
ns={'__name__':'fixture_diagnostic','__file__':str(p)}
exec(compile(p.read_bytes(),str(p),'exec'),ns)
try: raise SystemExit(ns['main']())
except Exception as e:
 frames=[];t=e.__traceback__
 while t:
  f=t.tb_frame;row={'function':f.f_code.co_name,'line':t.tb_lineno}
  for k in ('name','expected','category'):
   if k in f.f_locals and isinstance(f.f_locals[k],(str,int,type(None))):row[k]=f.f_locals[k]
  if f.f_code.co_name=='invoke':
   c=f.f_locals.get('p');row['actual_rc']=None if c is None else c.returncode
   if c:
    try:
     report=json.loads(c.stdout);row['failures']=[x for x in report.get('checks',[]) if x['status'] in ('blocked','error')];row['gate_status']=report.get('status')
    except Exception:row['unparsed']=True
  if f.f_code.co_name=='run':
   c=f.f_locals.get('p');row['actual_rc']=None if c is None else c.returncode;row['program']=Path(f.f_locals['argv'][0]).name
  frames.append(row);t=t.tb_next
 print(json.dumps({'status':'error','exception':type(e).__name__,'frames':frames}))
 raise SystemExit(2)
