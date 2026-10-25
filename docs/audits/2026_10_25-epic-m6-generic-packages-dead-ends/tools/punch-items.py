#!/usr/bin/env python3
"""05-punch-list.md from one list (#670): the items, the punch_index and the Phase 7 table.

    python3 -I punch-items.py > ../05-punch-list.md
"""
HOST = "Yes, on the host: the inventory's rows, a generated plan (`tools/viewplan`, through the `curl` shim), `get_pkg_directory`, `git grep`, or a constructed recipe in a scratch tree; no guest, no device, no build, no fetch (brief § 5)"
NOTHING = "nothing inherited: a recipe no image builds has written nothing on a device or in a cloud; the tree is the only place it exists"

I = [
 dict(f="F-01", tracked="#1049", t="`tools/renovation-inventory` does not follow `PKG_DEPENDS_UNPACK`, so five units every plan unpacks read `unreached` (ROCKNIX `spirv-headers`, the three ROCKNIX rust snapshots, generic `binutils-gold`)", sev="Medium", cat="Bug", q="Q3", bug=True,
  area="`tools/renovation-inventory` (`compute_reach`)", what="`compute_reach` marks a recipe reached when a reached recipe names it in `PKG_DEPENDS_UNPACK`, through the closure, as it does for `. ${ROOT}/packages/...` sourcing. The fix is T10's set; the lane edits no tool.",
  where="`tools/renovation-inventory` `compute_reach` and its `SOURCED` regex (at `2174265e9c`)", ev="`02` § Disagreements: the namers' lines, the plans, the resolutions on three devices", vm=HOST,
  aw="what was written: `inventory.json` at `eb4763e3cc` carries `reach: unreached` for the five units, and every later slice's membership read it; the fixed tool regenerates the inventory, and a slice whose set changes is the coordinator's to re-cut",
  acc="a constructed tree with a recipe reached only through a reached recipe's `PKG_DEPENDS_UNPACK` reads `reached` in the tool's output (it reads `unreached` today); the regenerated inventory marks the five units reached"),
 dict(f="F-02", tracked="#1050", t="`tools/pkgcheck` exits 0 when an argument matches no recipe, so a run that checked nothing reads as clean; the brief's sweep form (`tools/pkgcheck packages/...`) did exactly that", sev="Medium", cat="Bug", q="Q2", bug=True,
  area="`tools/pkgcheck` (upstream's)", what="An argument that matches no `package.mk` is an error (non-zero exit, a message naming it), or a full path is accepted as well as a name. A contained fix (D-QA-051 rule 6); the fix is a packet the coordinator routes, not the lane's.",
  where="`tools/pkgcheck:154-160` (the `find ... -path */${arg}/package.mk` loop) and `:169` (`[ ${FAILS} -eq 0 ]`)", ev="`tools/pkgcheck packages/addons/tools/jre.zulu`: rc 0, no output; `tools/pkgcheck tools/jre.zulu`: rc 1 with the FAIL", vm=HOST, aw=NOTHING.replace("a recipe no image builds has written nothing on a device or in a cloud; the tree is the only place it exists", "a lint writes nothing; what it left is earlier runs' clean verdicts, each of which may have checked nothing if a path was passed"),
  acc="`tools/pkgcheck packages/addons/tools/jre.zulu` either checks the recipe (its FAIL printed) or exits non-zero naming the unmatched argument, quoted; `tools/pkgcheck nosuchpackage` exits non-zero"),
 dict(f="F-03", tracked="#1051", t="`packages/graphics/mesa-reusable/package.mk:15` runs `curl` at global scope, so every plan generation, and every build's package scan, makes an HTTPS request to github.com", sev="Medium", cat="Bug", q="Q2", bug=True,
  area="`packages/graphics/mesa-reusable/package.mk` (upstream-carried, unreached)", what="The checksum is pinned in the recipe or read where the package is built, never at parse time; or `scripts/pkgjson` sources recipes with the network unavailable. The lane edits no recipe (D-WORKFLOW-209).",
  where="`packages/graphics/mesa-reusable/package.mk:15`; `scripts/pkgjson:54-55` (every cached recipe sourced)", ev="the `pkgjson` worker with a logging `curl` shim (`stage-a/shim/mesa-reusable-load.txt`); the five plans offline, byte-identical, 5 calls intercepted", vm=HOST + " (the proof is the shim's log: zero calls after the fix)", aw=NOTHING,
  acc="`tools/viewplan image` with a logging `curl` shim first on `PATH` logs no call, quoted (it logs one today)"),
 dict(f="F-04", t="A host plan without `xmlstarlet` drops H700's bootloader chain in silence: `SUBDEVICES` is read through `xmlstarlet ... 2>/dev/null`, so H700-aarch64 plans 605 names on the host against the container's 611", sev="Low", cat="Renovation", q="Q3",
  area="`distributions/ROCKNIX/config/functions` (the build engine's)", what="A missing `xmlstarlet` fails where `SUBDEVICES` is read, or `scripts/checkdeps` requires it. A lead for the coordinator (T5's area).",
  where="`distributions/ROCKNIX/config/functions:224`", ev="`command -v xmlstarlet` empty on the host; the six names; the host plan's `u-boot` wanting only `toolchain`", vm=HOST, aw=NOTHING.replace("a recipe no image builds has written nothing on a device or in a cloud; the tree is the only place it exists", "a host plan writes nothing; builds run in the container, which has `xmlstarlet`"),
  acc="on a host without `xmlstarlet`, `tools/viewplan image` for H700 either fails naming it or plans the six bootloader names, quoted"),
 dict(f="F-06", t="Fork-own row `packages/tools/installer`: a shadowed copy whose override is live; the fork's `459feac81e` (2026-07-01) edited the copy no plan uses", sev="Low", cat="Renovation", q="Q7",
  area="`packages/tools/installer/package.mk` (fork-own)", what="Verdict: **shadowed copy, override live** (resolves to `projects/ROCKNIX/packages/tools/installer` on all three devices; that override is in the GENERIC_X64 plan). Whether the edit (drop grub for GENERIC_X64) belongs on the override, or the copy returns to upstream's bytes, is the coordinator's decision; nothing is changed here.",
  where="`packages/tools/installer/package.mk`; `459feac81e`", ev="`02` § Reachability row; `stage-a/resolve-units.txt`", vm=HOST, aw=NOTHING,
  acc="the coordinator's decision recorded on its issue; if the edit moves, the override carries it and the copy equals `upstream/next`'s bytes (`git diff upstream/next -- packages/tools/installer` empty)"),
 dict(f="F-07", t="Fork-own row `projects/ROCKNIX/packages/graphics/spirv-headers`: reached after all, unpacked by four plan-built overrides; the inventory calls it `unreached`", sev="Low", cat="Renovation", q="Q6",
  area="`projects/ROCKNIX/packages/graphics/spirv-headers/package.mk` (fork-own, D-WORKFLOW-199)", what="Verdict: **reached after all**. The row leaves this slice's set; the coordinator hands it to T8's table; F-01 carries the tool's half. Kept, as D-WORKFLOW-199 decided.",
  where="`projects/ROCKNIX/packages/graphics/{glslang:18,shaderc:12,spirv-tools:18}`, `projects/ROCKNIX/packages/lang/llvm:17`", ev="`02` § Disagreements", vm=HOST, aw=NOTHING,
  acc="the row is in T8's table, or the regenerated inventory marks it reached (F-01's fix)"),
 dict(f="F-05", t="Fork-own row `projects/ROCKNIX/packages/rust/cbindgen`: dead -- named by nothing outside its own directory, not on `upstream/next`; a proposed removal", sev="Low", cat="Renovation", q="Q6",
  area="`projects/ROCKNIX/packages/rust/cbindgen/package.mk` (fork-own)", what="Verdict: **fork-own, dead**. Proposed: remove `projects/ROCKNIX/packages/rust/cbindgen/` (and its generic shadow, `packages/rust/cbindgen`, an upstream-carried copy whose only override is this one, under the class decision). The removal is the coordinator's decision, never made here (D-WORKFLOW-209).",
  where="`projects/ROCKNIX/packages/rust/cbindgen/package.mk`", ev="`stage-b/cbindgen-grep.txt` (7 lines, all inside its own two directories); `git cat-file -e upstream/next:projects/ROCKNIX/packages/rust/cbindgen/package.mk` fails", vm=HOST,
  aw="nothing inherited: no image builds or unpacks `cbindgen` (no plan names it; no `PKG_DEPENDS_UNPACK` names it), so no device holds anything it produced and no cloud carries it; removal touches only the tree",
  acc="the coordinator's decision recorded; if removed, `tools/viewplan image` for the three images (through the shim) is unchanged, and `git grep -n cbindgen -- packages projects` lists only the generic copy or nothing"),
 dict(f="Q1", t="The class decision: the dead, upstream-carried set (603 units, 76,809 lines, 447 of them LibreELEC's media centre) and the five dead files upstream has already deleted (`strace`, `grub`'s three, `qemu`)", sev="Low", cat="Renovation", q="Q1",
  area="`packages/` and `projects/ROCKNIX/packages/` (upstream-carried)", what="The lane's recommendation (`04` § Q1): keep the upstream-carried dead set (a deletion is a modify/delete conflict at every merge that touches it, and the media centre arrives through ROCKNIX's LibreELEC merges); drop only `cbindgen` and the five files upstream already deleted; fix the inventory's gap. The decision is the maintainer's, carried by the coordinator to #346.",
  where="`02` § Reachability (the dispositions); `stage-b/upstream-diff.txt`", ev="`04` § Q1 and § Q6; `git log --oneline c445081a59..upstream/next -- packages` prints 0", vm=HOST,
  aw="nothing inherited: none of these units is built for an image; removing upstream-carried files changes only what the next `upstream/next` merge must reconcile",
  acc="the maintainer's decision recorded on #346 and, if it removes anything, in a register row; the table's dispositions are the input"),
 dict(f="F-08", t="The brief's figures the run moved: 84/5 is 86/3 with the container's plans; *24 named directly* is 25, 30 or 18 by method; *nothing is fetched* is false for any plan generation; the `pkgcheck` sweep form checked nothing", sev="Low", cat="Documentation", q="Q7",
  area="`docs/reviews/briefs/generic-packages-dead-ends.md` (the coordinator's)", what="Recorded; the coordinator corrected the brief and criterion 11 of #670.",
  where="the brief at `74b71ab443` § 2 and § 5", ev="`02` § The split and § The runs; `00`", vm=HOST, aw=NOTHING.replace("a recipe no image builds has written nothing on a device or in a cloud; the tree is the only place it exists", "a brief writes nothing; the correction is the coordinator's commit"),
  acc="the brief at `0a5676ea5d` and #670's criterion 11 carry the corrected figures and the shim"),
]

# Phase 7, at stage D (2026-10-25): the three bugs filed by the lane (#1049, #1050, #1051);
# the coordinator's decision issue #1048 (its answer on #670 at 04:29 UTC) for the proposed
# removal, the installer question and the class decision, which the coordinator carries to #346.
P7 = {
  "PL-01": ("Deferred", "bug #1049, filed by the lane; the fix is T10's set (#657), routed by the coordinator"),
  "PL-02": ("Deferred", "bug #1050, filed by the lane; the fix is a packet the coordinator routes; the upstream note to #585 is the coordinator's"),
  "PL-03": ("Deferred", "bug #1051, filed by the lane; the fix is a packet the coordinator routes (the lane edits no recipe, D-WORKFLOW-209)"),
  "PL-04": ("Deferred", "Backlog #1053, the coordinator's (the build engine's `xmlstarlet` lead; its answer on #670 at 04:33 UTC)"),
  "PL-05": ("Deferred", "the coordinator's decision issue #1048: whether the fork's edit belongs on the override"),
  "PL-06": ("Deferred", "bug #1049: its fix marks the row reached; the coordinator hands the row to T8's table"),
  "PL-07": ("Deferred", "the coordinator's decision issue #1048: the proposed removal, never made here"),
  "PL-08": ("Deferred", "the coordinator's decision issue #1048; the class decision goes to #346 from the coordinator at acceptance"),
  "PL-09": ("Resolved", "the coordinator's `0a5676ea5d` (the brief's evidence floor, the `pkgcheck` form, criterion 11)"),
}

def main():
  out = ["# Punch List — M6.P2 T23, the generic packages no image builds", "",
         "**Local depth** (D-WORKFLOW-184): no reviewer seat; the counts are the check. Every `where` is at `8ebaf8daad` (unchanged at the dispatch tip). The lane removes nothing and edits no recipe or tool (D-WORKFLOW-209). Three `bug`s are filed at stage D (PL-01 to PL-03). Generated by `tools/punch-items.py` from one list.", ""]
  idx = ["```yaml", "punch_index:"]
  gate = ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
  for n, x in enumerate(I, 1):
      pl = f"PL-{n:02d}"
      out += [f"## {pl}: {x['t']}", "", f"- **Severity:** {x['sev']}", f"- **Category:** {x['cat']}", f"- **Question:** {x['q']}",
              f"- **Source:** {x['f']}", f"- **Owner area:** {x['area']}", f"- **What:** {x['what']}", f"- **Where:** {x['where']}",
              f"- **Evidence:** {x['ev']}", f"- **Can this be done on the VM?** {x['vm']}", f"- **Already written:** {x['aw']}",
              f"- **Acceptance:** {x['acc']}"]
      if x.get("bug"): out.append(f"- **Bug issue:** {x.get('tracked', 'filed at stage D')}")
      out.append("")
      idx += [f"- id: {pl}", f"  severity: {x['sev']}", f"  category: {x['cat']}", f"  question: {x['q']}",
              f"  source_finding: \"{x['f']}\"", f"  owner_area: \"{x['area'].replace(chr(34), chr(39))}\""]
      if x.get("bug"): idx.append(f"  tracked: \"{x.get('tracked', 'bug issue filed at stage D')}\"")
      p7 = P7.get(pl)
      if p7:
          idx.append(f"  outcome: \"{p7[0].lower()}\"")
          gate.append(f"| {pl} | **{p7[0]}** | {p7[1]} |")
      else:
          idx.append("  outcome: open")
          gate.append(f"| {pl} | Open | stage D: the bugs filed, the decision issue named by the coordinator |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
  main()
