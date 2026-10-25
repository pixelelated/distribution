#!/usr/bin/env python3
"""T40 (#687): the provenance table of the patches and kernel configurations no plan applies.

Reads only what stage A saved under .qa-scratch/t40/ (the inventory's rows at 2174265e9c,
T23's reachability rows read from its branch with git show, the symlinked patches entries,
the rows deleted at upstream/next) and the bytes at 8ebaf8daad through `git show`. It classes
every row by scripts/unpack's rules, first match in order, reads each patch's header, finds
the shadowed patches whose diff the live override already carries, and asserts the counts, so
a missing row fails here instead of printing an empty cell. It changes nothing in the tree.

    python3 -I t40-tables.py <worktree> stats | provenance | coverage | shadowed | json
"""
import collections, hashlib, json, os, re, subprocess, sys
from pathlib import Path

W = Path(sys.argv[1]); S = W / '.qa-scratch/t40'; MODE = sys.argv[2]; HASH = '8ebaf8daad'

def git(*a):
    return subprocess.run(['git', '-C', str(W), *a], capture_output=True, text=True, errors='replace').stdout

inv = json.load(open(S / 'inventory-rows.json')); rows = inv['rows']
byp = {r['path']: r for r in rows}
recipes = {r['path'][:-len('/package.mk')] for r in rows if r['path'].endswith('/package.mk')}
T = sorted((r for r in rows if r['area'] == 'patches-and-configs' and r['reach'] == 'unreached'), key=lambda r: r['path'])
assert len(T) == 778 and sum(r['lines'] or 0 for r in T) == 317908
assert sum(r['path'].endswith('.patch') for r in T) == 760 and sum(r['path'].endswith('.conf') for r in T) == 18

t23 = {}
for l in open(S / 't23-reach-rows.md'):
    m = re.match(r'^\| `([^`]+)`.*\*\*([^*]+)\*\* \|\s*$', l.rstrip('\n'))
    assert m, l[:80]
    t23[m.group(1)] = m.group(2)
assert len(t23) == 731
deleted = {l.split()[1] for l in open(S / 'deleted-upstream.txt')}
symlinked = {}   # an override's patches directory that is a git symlink -> the directory it points at
for l in open(S / 'symlink-targets.txt'):
    src, dst = l.rstrip('\n').split(' -> ')
    if src.endswith('/patches'):
        symlinked[src] = os.path.normpath(os.path.join(os.path.dirname(src), dst))

def unit_of(p):
    d = os.path.dirname(p)
    while d and d not in recipes: d = os.path.dirname(d)
    return d or None

def header(p):
    if not p.endswith('.patch'): return {}
    text = git('show', f'{HASH}:{p}')
    h = {}
    for line in text.splitlines()[:60]:
        if line.startswith('From: ') and 'from' not in h: h['from'] = line[6:].strip()
        elif line.startswith('Subject: ') and 'subject' not in h: h['subject'] = line[9:].strip()
        elif line.startswith('diff --git a/') and 'target' not in h: h['target'] = line.split()[2][2:]
    if 'target' not in h:
        m = re.search(r'^(?:diff --git a/|--- a/)(\S+)', text, re.M)
        if m: h['target'] = m.group(1)
    s = h.get('subject', '')
    m = re.match(r'^\[PATCH(?: v\d+)?(?: (\d+/\d+))?\]\s*', s)
    if m: h['series'] = m.group(1) or ''; s = s[m.end():]
    tags = re.findall(r'^(?:(FROMGIT|FROMLIST|WIP|LOCAL|HACK|UPSTREAM|BACKPORT)\b[:,]?\s*)', s)
    h['tag'] = tags[0] if tags else ''
    h['subject_clean'] = s
    return h

def _body(text):
    i = text.find('diff --git')
    if i < 0: i = text.find('--- ')
    return text[i:].splitlines()
def _h(lines): return hashlib.sha256('\n'.join(lines).encode()).hexdigest()
# Three tests for "the override already carries this patch", strictest first:
#   strict  -- the diff body byte-equal, index lines aside (a duplicate);
#   offsets -- equal once hunk headers and file headers are set aside (the same change, re-offset);
#   changed -- the added and removed lines equal (the same change, its context moved).
def hashes(text):
    b = _body(text)
    return (_h([l for l in b if not l.startswith('index ')]),
            _h([l for l in b if not l.startswith(('index ', 'diff --git', '--- ', '+++ ', '@@'))]),
            _h([l for l in b if l[:1] in '+-' and not l.startswith(('+++ ', '--- '))]))

override_bodies = {}
def override_hashes(o):
    if o not in override_bodies:
        files = [f for f in git('ls-tree', '-r', '--name-only', HASH, '--', o + '/patches/').split() if f.endswith('.patch')]
        hs = {f: hashes(git('show', f'{HASH}:{f}')) for f in files}
        override_bodies[o] = [{v[k]: f for f, v in hs.items()} for k in range(3)]
    return override_bodies[o]

out = []
for r in T:
    p = r['path']; u = unit_of(p); sb = r.get('shadowed_by'); h = header(p)
    rec = dict(match=None, path=p, lines=r['lines'] or 0, kind='conf' if p.endswith('.conf') else 'patch', unit=u, shadowed_by=sb,
               origin=h.get('from') or ('hand-made' if p.endswith('.patch') else '--'),
               subject=h.get('subject_clean') or ('hand-made' if p.endswith('.patch') else 'kernel configuration'),
               tag=h.get('tag', ''), series=h.get('series', ''), target=h.get('target', ''), t23=None, dup_of=None)
    if p.startswith('packages/linux/patches/'):
        cls = 'a'; disp = 'dead: a generic kernel patch the ROCKNIX override never applies'
    elif p.startswith('projects/') and not p.startswith('projects/ROCKNIX/'):
        cls = 'b'; disp = "dead: another project's, which no Makefile target builds"
    elif p.startswith('projects/ROCKNIX/') and '/patches/x86_64/' in p:
        cls = 'c'; disp = 'never selected: a patches/x86_64 directory under PATCH_ARCH=x86'
    elif u in t23:
        cls = 'd'; rec['t23'] = t23[u]; disp = f'inside a T23 dead unit ({t23[u]})'
    else:
        link = next((s for s, d in symlinked.items() if u and d == u + '/patches'), None)
        if sb and link:
            cls = 'e1'; disp = 'reached after all'; rec['symlink'] = link
        elif sb:
            cls = 'e1'; disp = "dead: a sourced generic recipe's patches, which the live override's globbing never reaches"
        elif u and (u.startswith('packages/emulation/libretro-') or u.startswith('projects/ROCKNIX/packages/emulators/')):
            cls = 'e2'; disp = "dead: an unbuilt recipe's"
        else:
            cls = 'e2'; disp = "dead: an unbuilt recipe's"
    if p in deleted:
        disp = 'already deleted at upstream/next'
    rec['class'] = cls; rec['disposition'] = disp
    if sb and sb != 'projects/ROCKNIX/packages/linux' and p.endswith('.patch'):
        mine = hashes(git('show', f'{HASH}:{p}')); ov = override_hashes(sb)
        if mine[0] in ov[0]: rec['dup_of'] = ov[0][mine[0]]
        elif mine[1] in ov[1]: rec['match'] = ('the same change, re-offset', ov[1][mine[1]])
        elif mine[2] in ov[2]: rec['match'] = ('the same changed lines, its context moved', ov[2][mine[2]])
    if p in deleted: rec['upstream'] = 'deleted at upstream/next since the base'
    elif sb and sb != 'projects/ROCKNIX/packages/linux' and rec['match']:
        rec['upstream'] = f"the override carries {rec['match'][0]}"
    elif sb and sb != 'projects/ROCKNIX/packages/linux' and not rec['dup_of'] and rec['disposition'] != 'reached after all':
        rec['upstream'] = 'a LibreELEC change the override builds without'
    else: rec['upstream'] = 'carried'
    out.append(rec)

C = collections.Counter(x['class'] for x in out)
SH = [x for x in out if x['shadowed_by'] and x['shadowed_by'] != 'projects/ROCKNIX/packages/linux']

if MODE == 'stats':
    print('rows', len(out), 'lines', sum(x['lines'] for x in out))
    for c in ('a', 'b', 'c', 'd', 'e1', 'e2'):
        xs = [x for x in out if x['class'] == c]
        print(f'class {c}: {len(xs)} rows, {sum(x["lines"] for x in xs)} lines')
    print('class (e) total', C['e1'] + C['e2'])
    print('(a) by subdir', dict(collections.Counter(x['path'].split('/')[3] for x in out if x['class'] == 'a')))
    print('(b) by project', dict(collections.Counter(x['path'].split('/')[1] for x in out if x['class'] == 'b')), 'confs', sum(1 for x in out if x['class'] == 'b' and x['kind'] == 'conf'))
    print('(d) units', len({x['unit'] for x in out if x['class'] == 'd'}), 'by T23 disposition (rows)', dict(collections.Counter(x['t23'] for x in out if x['class'] == 'd')))
    for x in out:
        if x['class'] in ('e1', 'e2'): print('  ', x['class'], x['path'], x['lines'], '|', x['disposition'], '|', x.get('symlink', ''))
    print('dispositions', dict(collections.Counter(x['disposition'] for x in out)))
    print('shadowed non-kernel', len(SH), '; content duplicates', [(x['path'], x['dup_of']) for x in SH if x['dup_of']],
          '; reached after all through a symlink', sum(1 for x in SH if x['disposition'] == 'reached after all'),
          '; the rest', sum(1 for x in SH if not x['dup_of'] and x['disposition'] != 'reached after all'),
          '; of the rest: re-offset', sum(1 for x in SH if (x.get('match') or ('',))[0] == 'the same change, re-offset'),
          'context moved', sum(1 for x in SH if (x.get('match') or ('',))[0] == 'the same changed lines, its context moved'),
          'no counterpart', sum(1 for x in SH if not x['dup_of'] and not x.get('match') and x['disposition'] != 'reached after all'))
    print('headers: with From:+Subject:', sum(1 for x in out if x['kind'] == 'patch' and x['origin'] != 'hand-made'), 'hand-made', sum(1 for x in out if x['origin'] == 'hand-made'))
elif MODE == 'json':
    print(json.dumps(out, indent=1))
elif MODE == 'provenance':
    for x in out:
        sub = x['subject'].replace('|', '\\|')
        if len(sub) > 90: sub = sub[:87] + '...'
        org = x['origin'].replace('|', '\\|')
        print(f"| `{x['path']}` | {x['lines']} | {x['kind']} | {x['class']} | {('`' + x['unit'] + '`') if x['unit'] else '--'} | "
              f"{x['t23'] or '--'} | {('`' + x['shadowed_by'] + '`') if x['shadowed_by'] else '--'} | {org} | {sub} | "
              f"{x['tag'] or '--'} | {x['series'] or '--'} | {('`' + x['target'] + '`') if x['target'] else '--'} | {x['upstream']} | **{x['disposition']}** |")
elif MODE == 'coverage':
    for x in out:
        print(f"| `{x['path']}` | {x['lines']} | {x['kind']} | {x['class']} | {x['disposition']} |")
elif MODE == 'shadowed':
    for x in sorted(SH, key=lambda x: (x['shadowed_by'], x['path'])):
        what = (f"duplicate of `{x['dup_of']}`" if x['dup_of'] else
                f"reached after all (`{x['symlink']}` is a symlink)" if x['disposition'] == 'reached after all' else
                f"a lead for T41/T42; the override carries {x['match'][0]} (`{x['match'][1]}`)" if x.get('match') else
                'a lead for T41/T42; no counterpart in the override')
        sub = x['subject'].replace('|', '\\|')[:90]
        print(f"| `{x['shadowed_by']}` | `{x['path']}` | {sub} | {what} |")
