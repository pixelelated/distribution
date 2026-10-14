#!/usr/bin/env python3
"""UNRUN. Exact read-only ES source identity; no product imports or execution."""
import os
from pathlib import Path
import stat
from common import HERE, SEQUENCES, read, require, sha


def predecessors(owner,stage):
    require(stage=='es-syntax' and SEQUENCES=={'es':['es-syntax']},'one syntax stage only')


def inspect_source(work,family,binding):
    require(family=='es','wrong source family')
    root=Path(binding['es_source']['path'])
    expected=read(HERE/'plan/es-source-files.json')
    require(sha(HERE/'plan/es-source-files.json')==binding['es_source']['manifest_sha256'],'ES manifest changed')
    count=0
    for name,row in expected.items():
        path=root/name;info=path.lstat()
        if row['kind']=='gitlink':
            require(path.is_dir() and not path.is_symlink(),'ES submodule path changed')
            continue
        if row['mode']=='120000':
            require(stat.S_ISLNK(info.st_mode) and os.readlink(path)==row['target'],'ES source symlink changed')
        else:
            require(stat.S_ISREG(info.st_mode) and path.resolve()==path,'ES source is aliased/nonregular')
            mode='100755' if info.st_mode&stat.S_IXUSR else '100644'
            require(mode==row['mode'] and info.st_size==row['bytes'] and sha(path)==row['sha256'],'ES source bytes/mode changed: '+name)
        count+=1
    return {'commit':binding['es_source']['commit'],'tree':binding['es_source']['tree'],
            'manifest_sha256':binding['es_source']['manifest_sha256'],'files':count,
            'all_original_source_files_unchanged':True}
