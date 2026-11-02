#!/usr/bin/env python3
"""T39 correction-stream candidate/commit harness. No build, guest or network."""
import argparse, datetime, json, os, pathlib, subprocess, tarfile, io
ROOT = pathlib.Path(__file__).resolve().parents[3]  # overwritten by git root below
ROOT = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
A = ROOT / "docs/audits/2026_11_01-epic-m6-doctrine-reference"
SCRATCH = pathlib.Path("/workspace/tmp/m6-t39")
ENV = os.environ.copy()
ENV["TMPDIR"] = str(SCRATCH)
def git(*args, data=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, input=data, text=True, env=ENV).strip()
def run(cmd, receipt):
    now = subprocess.check_output(["date", "-u", "+%FT%TZ"], text=True).strip()
    r = subprocess.run(cmd, cwd=ROOT, env=ENV, text=True, capture_output=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text("$ " + " ".join(map(str, cmd)) + "\nstarted_at=" + now + "\n" + r.stdout + r.stderr + "\nrc=" + str(r.returncode) + "\n")
    print(receipt.name, "rc="+str(r.returncode), flush=True)
    if r.returncode: print(r.stdout + r.stderr, flush=True)
    return r.returncode
def harness(ref, dest, withheld=False):
    # Required inode check precedes each export. A fresh exact-membership tar only.
    assert run(["df", "-i", str(SCRATCH)], dest / "inodes.out") == 0
    export = SCRATCH / ("export-" + ref[:12] + "-" + dest.name)
    export.mkdir(exist_ok=True)
    assert not (export / ".git").exists()
    paths = (A / "stage-a/paths.txt").read_text().splitlines()
    assert len(paths) == 254
    raw = subprocess.check_output(["git", "archive", ref, "--", *paths], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        assert all(not pathlib.PurePosixPath(x.name).is_absolute() and ".." not in pathlib.PurePosixPath(x.name).parts for x in tar.getmembers())
        tar.extractall(export, filter="data")
    cmd = ["bash", str(A / "tools/t39-checks.sh"), "--tree", str(export), "--repo", str(ROOT),
           "--commit", ref, "--since", "86ebb6dffc", "--paths", str(A / "stage-a/paths.txt"),
           "--allow", str(A / "tools"), "--out", str(dest / "steps")]
    if withheld: cmd += ["--withhold", "findings"]
    return run(cmd, dest / "harness.out"), str(export)
if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("stream")
    p.add_argument("--manifest", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--refs", default="#686")
    args=p.parse_args()
    dest=A/"stage-e"/args.stream
    dest.mkdir(exist_ok=True)
    files=json.loads(pathlib.Path(args.manifest).read_text())
    assert files and all(isinstance(x,str) for x in files)
    assert not git("diff","--cached","--name-only"), "unrelated staged files"
    parent=git("rev-parse","HEAD")
    subprocess.run(["git","add","--",*files], cwd=ROOT, check=True, env=ENV)
    staged=git("diff","--cached","--name-only").splitlines()
    assert set(staged)<=set(files), "unexpected staged path"
    assert run(["git","diff","--cached","--check"],dest/"staged-check.out")==0
    tree=git("write-tree")
    message=args.title+"\n\nRefs "+args.refs+"\n\nCo-Authored-By: GPT-6-Astra <noreply@openai.com>\n"
    candidate=git("commit-tree",tree,"-p",parent,data=message)
    result={"parent":parent,"candidate":candidate,"tree":tree,"staged_paths":staged}
    (dest/"candidate.json").write_text(json.dumps(result,indent=2)+"\n")
    rc,export=harness(candidate,dest/"candidate")
    result["candidate_export"]=export
    result["candidate_rc"]=rc
    (dest/"candidate.json").write_text(json.dumps(result,indent=2)+"\n")
    if rc: raise SystemExit(rc)
    assert run(["tools/rules-check","--quiet"],dest/"rules-check.out")==0
    if "docs/es-menu-map.md" in files:
        assert run(["tools/es-menu-map-check"],dest/"menu-map-check.out")==0
        assert "0 missing" in (dest/"menu-map-check.out").read_text()
    assert git("write-tree")==tree and git("rev-parse","HEAD")==parent
    assert run(["git","commit","-m",message],dest/"commit.out")==0
    committed=git("rev-parse","HEAD")
    assert git("rev-parse",committed+"^{tree}")==tree
    rc,export=harness(committed,dest/"committed")
    result.update(commit=committed,committed_rc=rc,committed_export=export)
    (dest/"result.json").write_text(json.dumps(result,indent=2)+"\n")
    if rc: raise SystemExit(rc)
    print("STREAM",args.stream,"PASS",committed,flush=True)
