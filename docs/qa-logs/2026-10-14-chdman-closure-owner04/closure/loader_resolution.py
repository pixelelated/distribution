#!/usr/bin/env python3
"""Only the two observed image interpreter paths map to the pinned SDK loader."""
from pathlib import Path
from common import require, safe_member, sha


def resolve_interpreter(interpreter,sysroot,tc,binding):
    require(interpreter in binding['interpreter_map'],'unsupported interpreter path; no basename/host fallback')
    relative=safe_member(binding['interpreter_map'][interpreter])
    canonical=sysroot/relative;expected=binding['canonical']
    require(canonical==tc/safe_member(expected['relative_to_toolchain']) and canonical.resolve()==canonical
            and canonical.is_relative_to(tc) and canonical.is_file(),'canonical retained loader absent/escaped/linked')
    require(canonical.stat().st_size==expected['bytes'] and canonical.stat().st_mode&0o7777==expected['mode']
            and sha(canonical)==expected['sha256'],'canonical retained loader bytes/mode differ')
    requested=sysroot/interpreter.lstrip('/')
    resolved=requested.resolve(strict=False)
    require(resolved.is_relative_to(tc),'requested interpreter escapes retained toolchain')
    if requested.exists() or requested.is_symlink():
        require(requested.resolve(strict=True)==canonical,'conflicting interpreter at requested SDK path')
    return canonical,{'requested':interpreter,'requested_sdk_path':str(requested),'selected':str(canonical),
                      'sha256':expected['sha256'],'resolution':'literal' if requested==canonical else 'exact-image-alias'}
