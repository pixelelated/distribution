# S5's key test, stage B's rule (02-forward-audit.md, the per-device retroarch.cfg):
# a key is not read when it occurs as a word nowhere in the pin's .c/.h; generated
# families are excluded, and a hotkey input_<bind> counts when <bind> occurs.
# One addition from Phase 4.6/S5: a key whose only occurrence is a menu label
# string (msg_hash_lbl_str.h) is not read either; core_updater_buildbot_url is
# the one such key in the profiles.
import os, re, sys
B, S = sys.argv[1:3]
words = set(); label_only = {"core_updater_buildbot_url"}
for root, ds, fs in os.walk(B):
    if "/.git" in root or "/obj-" in root: continue
    for f in fs:
        if f.endswith((".c", ".h")):
            words |= set(re.findall(r"[A-Za-z0-9_]+", open(os.path.join(root, f), errors="replace").read()))
gen = re.compile(r"^input_.*_(btn|axis|mbtn)$|^input_(libretro_)?device_p\d+$|^network_remote_enable_user_p\d+$|^input_player\d+_")
total = 0
for dev in sorted(os.listdir(S)):
    p = os.path.join(S, dev, "retroarch.cfg")
    if not os.path.isfile(p): continue
    keys = re.findall(r"^([A-Za-z0-9_]+)\s*=", open(p).read(), re.M)
    nr = []
    for k in keys:
        if gen.match(k): continue
        if k in label_only: nr.append(k); continue
        if k in words: continue
        if k.startswith("input_") and k[6:] in words: continue
        nr.append(k)
    total += len(nr)
    print(dev, len(keys), len(nr), nr)
print("total not read:", total)
