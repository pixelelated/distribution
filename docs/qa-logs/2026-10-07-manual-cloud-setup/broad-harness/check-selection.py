#!/usr/bin/env python3
"""Exercise the harness's exact source-availability gate in local fixtures."""
from pathlib import Path
import json, subprocess, tempfile
root=Path(__file__).resolve().parents[4]
text=(root/'tools/last-good-scripts-test').read_text()
gate=text[text.index('MIGRATION_AVAILABLE=0\n'):text.index('# busybox for the applets',text.index('MIGRATION_AVAILABLE=0\n'))]
results=[]
with tempfile.TemporaryDirectory(prefix='lgst-selection-') as directory:
    fixture=Path(directory)
    for name, engine, installed, want in [('retired',False,False,0),('missing-installed',False,True,2),('historical-present',True,True,0)]:
        tree=fixture/name
        source=tree/'projects/ROCKNIX/packages/network/rclone/sources'
        source.mkdir(parents=True)
        (source.parent/'package.mk').write_text('cp cloud_migrate_layout ${INSTALL}/usr/bin\n' if installed else 'cp cloud_setup ${INSTALL}/usr/bin\n')
        if engine:(source/'cloud_migrate_layout').write_text('# historical synthetic engine\n')
        cs=tree/'staged';(cs/'src').mkdir(parents=True)
        script='set -eu\nROOT=$1;CS=$2;OLD=0;NOT_APPLICABLE=0;RCLONE_REL=projects/ROCKNIX/packages/network/rclone/sources\nsrc_of() { cp "${ROOT}/$1" "$2"; }\n'+gate+'\nprintf "availability=%s na=%s\\n" "$MIGRATION_AVAILABLE" "$NOT_APPLICABLE"\n'
        r=subprocess.run(['bash','-c',script,'check',str(tree),str(cs)],capture_output=True,text=True)
        passed=r.returncode==want
        if name=='retired':passed=passed and 'NOT APPLICABLE' in r.stdout and 'availability=0 na=1' in r.stdout
        if name=='historical-present':passed=passed and 'availability=1 na=0' in r.stdout and (cs/'src/cloud_migrate_layout').is_file()
        if name=='missing-installed':passed=passed and 'recipe installs missing' in r.stderr
        results.append(dict(case=name,status='PASS' if passed else 'FAIL',returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
output=Path(__file__).with_name('selection-results.json')
output.write_text(json.dumps({'scope':'synthetic source fixtures; no device/cloud actions','cases':results},indent=2)+'\n')
print(json.dumps({'cases':len(results),'passed':sum(x['status']=='PASS' for x in results)}))
raise SystemExit(any(x['status']!='PASS' for x in results))
