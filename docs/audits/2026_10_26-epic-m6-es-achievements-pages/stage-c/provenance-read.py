"""T20 (#667): read each seat's provenance directly (an audit invoke has no
council-run manifest, so `tools/council/run summary` and `verify-seals` have
nothing to read; T17 met the same).

    python3 -I -B docs/audits/2026_10_26-epic-m6-es-achievements-pages/stage-c/provenance-read.py

For each of the four outputs: the verification result and what it observed,
the served provider, the effort check, attempts and finish, the
facilitator_version, and the output's sha256 against the provenance's own
record of it. A missing file, a FAIL, or a hash that differs is printed as
such and makes the exit 1; nothing here reads a key.
"""
import hashlib, json, os, sys

D = "docs/audits/2026_10_26-epic-m6-es-achievements-pages/second-opinions"
OUTS = ["astra-probe.md", "astra-audit.md", "argon-probe.md", "argon-audit.md"]
bad = 0


def find(d, names):
    """The first value under any of these keys, anywhere in the document."""
    if isinstance(d, dict):
        for k, v in d.items():
            if k in names and not isinstance(v, (dict, list)):
                return v
        for v in d.values():
            r = find(v, names)
            if r is not None:
                return r
    elif isinstance(d, list):
        for v in d:
            r = find(v, names)
            if r is not None:
                return r
    return None


for out in OUTS:
    p, pv = os.path.join(D, out), os.path.join(D, out + ".provenance.json")
    if not (os.path.exists(p) and os.path.exists(pv)):
        print(f"{out}: MISSING ({'output' if not os.path.exists(p) else 'provenance'})")
        bad += 1
        continue
    d = json.load(open(pv))
    fin = d.get("final", {})
    ver, eff, prov = fin.get("verification", {}), fin.get("effort_verification", {}), fin.get("provider_verification", {})
    got = hashlib.sha256(open(p, "rb").read()).hexdigest()
    recorded = d.get("output_file_sha256")
    match = "match" if recorded == got else f"DIFFERS (recorded {recorded})"
    attempts = d.get("attempts", [])
    # The last attempt is the one whose output was kept; earlier ones are listed.
    finish = find(attempts[-1:], {"finish_reason", "finish"})
    earlier = [find([x], {"finish_reason", "finish"}) for x in attempts[:-1]]
    print(f"{out}: verification={ver.get('result')} observed={ver.get('observed')} source={ver.get('model_identity_source')}; "
          f"provider={prov.get('result')} observed={prov.get('observed')}; effort={eff.get('result')} "
          f"(declared {eff.get('declared')}, reasoning {eff.get('observed_reasoning_tokens')}); attempts={len(attempts)} finish={finish}" + (f" (earlier: {earlier})" if earlier else "") + "; "
          f"facilitator_version={d.get('facilitator_version')}; output sha256 {got[:16]} {match}")
    if ver.get("result") != "PASS" or prov.get("result") not in ("PASS", None) or recorded != got:
        bad += 1
sys.exit(1 if bad else 0)
