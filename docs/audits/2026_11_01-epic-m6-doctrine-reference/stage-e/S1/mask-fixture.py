#!/usr/bin/env python3
"""Exercise the literal documented mask; fixture values are built only at runtime."""
import pathlib, re, shlex, subprocess
ROOT=pathlib.Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())
path="docs/device-testing-policy.md"
before=subprocess.check_output(["git","show","96ef183aae:"+path],text=True)
after=(ROOT/path).read_text()
canonical=subprocess.check_output(["git","show","7f25f9f78b3da3a6b2c893397b58a3ce5a04be75:.claude/rules/engineering-practices.md"],text=True)
command=next(l.strip() for l in canonical.splitlines() if l.strip().startswith("sed -E ") and "; s/(--" in l)
m=re.search(r"<!-- device-output-log-mask:begin -->\n\x60{3}bash\n([^\n]+)\n\x60{3}\n<!-- device-output-log-mask:end -->",after)
assert m and m[1]==command, "documented mask must be the canonical literal"
args=shlex.split(command); assert args[:2]==["sed","-E"] and len(args)==3
keys=["token","key","pass","password","psk","user","TOKEN","PaSsWoRd"]
cases=[]
for i,k in enumerate(keys):
    for form in ["assignment","flag-space","flag-equals"]:
        v="T"+str(39)+"_"+str(i)+"_"+form.replace("-","")+"_"+chr(90)*5
        s=(k+" = "+v if form=="assignment" else "--"+k+(" " if form=="flag-space" else "=")+v)
        cases.append((form,s,v))
benign="PASS benign status: complete\nordinary evidence line\n"
text="\n".join(s for _,s,_ in cases)+"\n"+benign
def apply(expr):
    return subprocess.run(["sed","-E",expr],input=text,text=True,capture_output=True,check=True).stdout
old=apply(args[2].split("; ")[0])
new=apply(args[2])
old_leaks=sum(v in old for _,_,v in cases); new_leaks=sum(v in new for _,_,v in cases)
assert old_leaks==len(keys), "omitting flag substitution must expose all space-flag controls"
assert new_leaks==0 and benign in new
assert "device-output-log-mask:begin" not in before
print("BEFORE FAIL: long-form documented mask absent; assignment-only control exposes",old_leaks,"of",len(cases),"planted values")
print("AFTER PASS: literal canonical mask; planted values remaining",new_leaks,"of",len(cases),"; benign lines preserved")
print("CONTROL PASS: removing the flag substitution fails the space-flag proof")
