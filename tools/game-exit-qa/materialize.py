"""An admitted top overlay over the exact stopped, held upgrade chain."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import sha, write


def fingerprint(path):
    st = path.lstat()
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]


def main(owner):
    c=json.loads((owner/'config.json').read_text())
    top=owner/'vm/disk.qcow2'
    base=Path(c['backing']['path'])
    raw=Path(c['raw_backing']['path'])
    assert fingerprint(base)==c['backing']['identity'] and fingerprint(raw)==c['raw_backing']['identity']
    exe=c['host_inputs']['qemu_img']
    subprocess.run([exe,'create','-f','qcow2','-F','qcow2','-b',str(base),'-o','cluster_size=65536',
                    str(top),str(16*1024**3)],check=True,timeout=10)
    chain=json.loads(subprocess.check_output([exe,'info','--output=json','--backing-chain',str(top)],timeout=10))
    assert [x['filename'] for x in chain]==[str(top),str(base),str(raw)]
    assert [x['format'] for x in chain]==['qcow2','qcow2','raw']
    assert chain[0]['virtual-size']==chain[1]['virtual-size']==16*1024**3
    assert chain[2]['virtual-size']==c['raw_backing']['identity'][4]
    v=owner/'vm/vars.fd'
    template=Path(c['host_inputs']['ovmf_vars_template'])
    with v.open('xb') as f,template.open('rb') as s:
        shutil.copyfileobj(s,f)
    assert sha(v)==c['inputs'][str(template)]
    write(owner/'records/materialization.json',{'chain':chain,'overlay_allocated':top.stat().st_blocks*512,
                                              'private_vars_sha256':sha(v)},True)


if __name__=='__main__':
    main(Path(sys.argv[1]))
