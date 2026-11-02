"""New T44 syntactic PO reader; never invokes gettext or ES producers."""
import ast,re

class ParseError(ValueError): pass

def parse(data):
    text=data.decode('utf-8-sig',errors='strict')
    entries=[]; cur={}; flags=[]; last=None; start=0; obsolete=0
    def flush():
        nonlocal cur,flags,last,start
        if cur:
            if 'msgid' not in cur or not any(k=='msgstr' or k.startswith('msgstr[') for k in cur):
                raise ParseError('entry lacks msgid/msgstr')
            if 'msgid_plural' in cur:
                ks=sorted(int(k[7:-1]) for k in cur if k.startswith('msgstr['))
                if not ks or ks!=list(range(len(ks))) or 'msgstr' in cur:raise ParseError('invalid plural indices')
            elif 'msgstr' not in cur or any(k.startswith('msgstr[') for k in cur):raise ParseError('unexpected plural msgstr')
            entries.append(dict(fields=cur,flags=sorted(set(flags)),line=start))
        cur={};flags=[];last=None;start=0
    for n,line in enumerate(text.splitlines(),1):
        s=line.strip()
        if not s:flush();continue
        if s.startswith('#~'):obsolete+=1;continue
        if s.startswith('#'):
            if any(k.startswith('msgstr') for k in cur):flush()
            if s.startswith('#,'):flags.extend(x.strip() for x in s[2:].split(','))
            continue
        m=re.fullmatch(r'(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(".*")',s)
        if m:
            k,q=m.groups()
            if k in ('msgid','msgctxt') and any(x.startswith('msgstr') for x in cur):flush()
            if k in cur:raise ParseError(f'duplicate field at {n}')
            if k=='msgid_plural' and 'msgid' not in cur:raise ParseError('plural before msgid')
            if k.startswith('msgstr') and 'msgid' not in cur:raise ParseError('msgstr before msgid')
            last=k;cur[k]='';start=start or n
        elif s.startswith('"'):
            if last is None:raise ParseError(f'orphan continuation at {n}')
            q=s
        else:raise ParseError(f'unrecognized PO syntax at {n}')
        # Accept C-style simple/octal/hex escapes; refuse Python-only escapes.
        i=1
        while i < len(q)-1:
            if q[i]=='"':raise ParseError(f'unescaped interior quote at {n}')
            if q[i]=='\\':
                i+=1
                if i>=len(q)-1 or q[i] not in 'abfnrtv\\"01234567x':raise ParseError(f'unsupported escape at {n}')
                if q[i]=='x' and not re.match(r'[0-9a-fA-F]{2}',q[i+1:]):raise ParseError(f'invalid hex escape at {n}')
            i+=1
        try:v=ast.literal_eval(q)
        except (SyntaxError,ValueError) as e:raise ParseError(f'invalid quoted string at {n}') from e
        if not isinstance(v,str):raise ParseError(f'non-string at {n}')
        cur[last]+=v
    flush()
    keys=[(x['fields'].get('msgctxt'),x['fields']['msgid']) for x in entries]
    if len(set(keys))!=len(keys):raise ParseError('duplicate active context/msgid')
    return entries,obsolete

def counts(data):
    es,obsolete=parse(data);active=[e for e in es if e['fields']['msgid']!='']
    return dict(entries=len(active),headers=len(es)-len(active),plural=sum('msgid_plural' in e['fields'] for e in active),context=sum('msgctxt' in e['fields'] for e in active),format_flagged=sum(any(f.endswith('-format') and not f.startswith('no-') for f in e['flags']) for e in active),fuzzy=sum('fuzzy' in e['flags'] for e in active),untranslated=sum(any(not v for k,v in e['fields'].items() if k.startswith('msgstr')) for e in active),obsolete_lines=obsolete)
