"""Tiny JSON Markdown path/anchor validator; no file-system traversal or execution."""
import json,re,sys
x=json.load(open(sys.argv[1]));path=x['path'];anchor=x['anchor'];files=x['files']
if path not in files:print('REFUSE missing target');sys.exit(1)
heads=[];fence=None
for line in files[path].splitlines():
 if fence:
  if re.fullmatch(r' {0,3}'+re.escape(fence[0])+'{'+str(fence[1])+r',}\s*',line):fence=None
  continue
 m=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$',line)
 if m and (m[1][0]!='`' or '`' not in m[2]):fence=(m[1][0],len(m[1]));continue
 m=re.match(r'^ {0,3}#{1,6}\s+([A-Za-z0-9 ]+)\s*$',line)
 if m:heads.append(re.sub(' +','-',m[1].strip().lower()))
 elif re.match(r'^ {0,3}#|^ {0,3}<|^ {0,3}(?:=+|-+)\s*$',line):print('UNKNOWN unsupported heading/HTML/setext syntax');sys.exit(2)
if fence:print('UNKNOWN unclosed fence');sys.exit(2)
if len(heads)!=len(set(heads)):print('UNKNOWN duplicate anchor suffix convention');sys.exit(2)
if anchor and anchor not in heads:print('REFUSE missing anchor');sys.exit(1)
print('PASS literal fixture path and supported ASCII ATX anchor')
