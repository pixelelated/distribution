#!/usr/bin/env python3
"""Read-only artifact sweep. Unknown bytes fail; output never includes matches.

The reviewed allowlist is specific to path and context hash for branding,
and path and whole-file hash for public credential-pattern false positives.
It does not approve a directory, package, token prefix, or future changed file.
Run against an owned extracted SYSTEM; do not follow absolute image symlinks.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def contexts(data):
    counts = collections.Counter()
    for match in re.finditer(rb"rocknix|rasteratops", data.lower()):
        left, right = match.span()
        while left > max(0, match.start() - 180) and 32 <= data[left - 1] < 127:
            left -= 1
        while right < min(len(data), match.end() + 180) and 32 <= data[right] < 127:
            right += 1
        counts[digest(data[left:right])] += 1
    return counts


def scan(root, allow, patterns):
    brands = {(x['path'], x['context_sha256']): x for x in allow['branding']}
    secrets = {(x['path'], x['file_sha256']): x for x in allow['public_patterns']}
    count = collections.Counter()
    findings, files, links = [], [], []
    def matching_paths(expression):
        result = subprocess.run(['rg', '--files-with-matches', '--null', '--text',
                                 '--hidden', '--no-ignore', '--regexp', expression,
                                 str(root)], capture_output=True)
        if result.returncode not in (0, 1):
            raise RuntimeError('rg could not completely scan the artifact')
        return {os.fsdecode(p) for p in result.stdout.split(b'\0') if p}
    brand_paths = matching_paths('(?i)rocknix|rasteratops')
    secret_paths = matching_paths(patterns.pattern.decode())
    def onerror(error):
        raise error
    for parent, dirs, names in os.walk(root, followlinks=False, onerror=onerror):
        # Include directory symlinks as entries; never traverse them.
        names += [x for x in dirs if (Path(parent) / x).is_symlink()]
        for name in sorted(names):
            path = Path(parent) / name
            relative = str(path.relative_to(root))
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                target = os.readlink(path)
                links.append({'path': relative, 'target': target})
                count['symlinks'] += 1
                # Names/targets are retained machine paths under NAMING v2.
                if re.search('rocknix|rasteratops', relative + target, re.I):
                    count['legacy_symlink_paths'] += 1
                continue
            if not stat.S_ISREG(mode):
                raise ValueError('Unexpected special file: ' + relative)
            data = path.read_bytes()
            sha = digest(data)
            count['regular_files'] += 1
            count['bytes_read'] += len(data)
            if re.search('rocknix|rasteratops', relative, re.I):
                count['legacy_file_paths'] += 1
            hits = contexts(data) if str(path) in brand_paths else {}
            if hits:
                files.append({'path': relative, 'sha256': sha, 'contexts': dict(hits)})
            for context_sha, occurrences in hits.items():
                entry = brands.get((relative, context_sha))
                disposition = entry['disposition'] if entry else 'UNKNOWN'
                count['brand_occurrences'] += occurrences
                count['brand_contexts'] += 1
                count['brand_' + disposition] += 1
                if disposition != 'KEEP':
                    findings.append({'type': 'branding', 'path': relative,
                                     'context_sha256': context_sha,
                                     'disposition': disposition,
                                     'issue': entry.get('issue') if entry else None})
            matches = list(patterns.finditer(data)) if str(path) in secret_paths else []
            if matches:
                count['credential_pattern_files'] += 1
                count['credential_pattern_matches'] += len(matches)
                entry = secrets.get((relative, sha))
                if entry and len(matches) == entry['matches']:
                    count['reviewed_public_pattern_matches'] += len(matches)
                else:
                    count['unclassified_credential_pattern_matches'] += len(matches)
                    findings.append({'type': 'credential-pattern', 'path': relative,
                                     'file_sha256': sha, 'matches': len(matches)})
            if count['regular_files'] % 10000 == 0:
                print('Progress: read', count['regular_files'], 'regular files', flush=True)
    for key in ['brand_UNKNOWN', 'brand_FIX', 'unclassified_credential_pattern_matches']:
        count.setdefault(key, 0)
    return {'counts': dict(count), 'findings': findings, 'brand_files': files,
            'symlinks': links, 'pass': not findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--allowlist', required=True, type=Path)
    parser.add_argument('--patterns', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    line, = [line for line in args.patterns.read_text().splitlines()
             if line.startswith('SECRET_PATTERNS=')]
    expression = shlex.split(line)[0].split('=', 1)[1].encode()
    allow = json.loads(args.allowlist.read_text())
    report = scan(args.root, allow, re.compile(expression))
    report['root'] = str(args.root.resolve())
    report['allowlist_sha256'] = digest(args.allowlist.read_bytes())
    report['patterns_sha256'] = digest(args.patterns.read_bytes())
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'pass': report['pass'], 'counts': report['counts']}, sort_keys=True))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
