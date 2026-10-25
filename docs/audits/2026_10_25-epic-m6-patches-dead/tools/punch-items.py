#!/usr/bin/env python3
"""05-punch-list.md from one list (#687): the items, the punch_index and the Phase 7 table.

    python3 -I punch-items.py > ../05-punch-list.md
"""
HOST = "Yes, on the host: the patch's bytes at `8ebaf8daad`, `scripts/unpack` read, `get_pkg_directory` under `config/options` (no request), `git ls-tree`, or a constructed tree; no guest, no device, no build, no plan, no network (brief § 5)"
NOTHING = "nothing inherited: a patch no image applies has written nothing on a device or in a cloud; the tree is the only place it exists"

I = [
 dict(f="F-01", t="Five `patches/x86_64` files under live ROCKNIX recipes are never selected (`scripts/unpack:127-128` sets `PATCH_ARCH=x86`): vitaquake2-lr's four, whose recipe passes `platform=` only on aarch64, and EmulationStation's `cpugov.patch`, whose `getAvailableGpuGovernors` calls `get_available_cpu_governors`", sev="Medium", cat="Bug", q="Q3", bug=True,
  area="`projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr` (four patch directories and `package.mk`), `projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch`", what="Rename each `patches/x86_64` to `patches/x86`; give vitaquake2-lr's `pre_make_target` an x86_64 branch passing `platform=${DEVICE}` (the x86 patch's `@DEVICE@`); correct `cpugov.patch`'s GPU call to `get_available_gpu_governors` in both arms. A packet after the maintainer's word; the lane edits no patch or recipe (D-WORKFLOW-209).",
  where="`scripts/unpack:127-128`, `:150-159`, `:196`; `vitaquake2-lr/package.mk:19-25`; `cpugov.patch:17-24`", ev="`02` § The x86_64 five", vm=HOST + " (the trace; that the renamed ES patch applies and runs is the next image's open item, D-QA-051; vitaquake2-lr's needs an AMD64 build nobody makes)",
  aw="nothing on a device: the five patches have never applied, so no image carries their effect; `40fce2a089` (2026-08-20) and `9f1fab30f6` (2025-07-13) put them in the tree only",
  acc="after the packet, a GENERIC_X64 build's EmulationStation `unpack` log names `patches/x86/cpugov.patch` applied (an open item for that image); on the host, `git ls-tree -r --name-only HEAD -- projects/ROCKNIX/packages | grep -c /patches/x86_64/` prints 0"),
 dict(f="F-02", tracked="#1056", t="`tools/renovation-inventory` does not resolve a symlinked `patches` directory, so gcc's three and cmake's one generic patches read `unreached` while every image applies them", sev="Medium", cat="Bug", q="Q3", bug=True,
  area="`tools/renovation-inventory` (`selected_patch_dirs`, the patch-row reach)", what="Resolve a symlinked `patches` entry to its target before the directory set is built (`os.path.realpath` against the checkout, or the blob's target). The fix is T10's set, beside #1049; the lane edits no tool.",
  where="`tools/renovation-inventory:382-401` (`:397` `os.path.normpath`), `:461-462`", ev="`02` § The symlinked four; `git ls-tree` mode `120000` on `projects/ROCKNIX/packages/{lang/gcc,devel/cmake}/patches`", vm=HOST + " (a constructed tree whose override's `patches` is a symlink to a generic directory)",
  aw="what was written: `inventory.json` at `eb4763e3cc` marks the four `reach: unreached`, and T40's membership read it; the fixed tool regenerates the inventory",
  acc="a constructed tree with an override whose `patches` symlinks to a generic directory reads the generic patches reached in the tool's output (unreached today); the regenerated inventory marks gcc's three and cmake's one reached"),
 dict(f="F-03", t="68 shadowed LibreELEC patches the live ROCKNIX overrides build without (31 overrides: bluez 8, ffmpeg 7, glibc 7, busybox 6, systemd 4, ...); 18 of them the override carries in another form, 50 with no counterpart", sev="Low", cat="Renovation", q="Q4",
  area="the ROCKNIX overrides in `02` § The shadowed 74", what="Each is a lead for T42's row on that override (T41's for a kernel package): whether the override should carry the change. Not answered here; none is a removal.",
  where="`02` § The shadowed 74 (each row's subject and tier)", ev="the generator's three tests", vm=HOST, aw=NOTHING,
  acc="each override's row in T41's or T42's table names these patches and answers whether the change is carried"),
 dict(f="F-04", t="14 patches are hand-made diffs with no `From:` or `Subject:` (12 ROCKNIX's, 2 LibreELEC's), so they cannot say what they are for", sev="Low", cat="Renovation", q="Q2",
  area="the 14 in `stage-a/headerless.txt`", what="Recorded: all 14 are dead rows (classes c, d, e2), so nothing is applied without a header; the five class (c) files take a header with F-01's packet.",
  where="`stage-a/headerless.txt`", ev="the header count (`02` § The runs)", vm=HOST, aw=NOTHING,
  acc="a design: recorded with its sentence in the Phase 7 table"),
 dict(f="F-05", t="The class decision: the 277 generic kernel patches and the 234 other projects' rows, beside T23's 603 units; class (d)'s 234 follow T23's decision; the six already deleted upstream go with the next base merge", sev="Low", cat="Renovation", q="Q1",
  area="`packages/linux/patches/`, `projects/<other>/`, and T23's units", what="The lane's recommendation (`04` § Q1): keep the 277 and the 234 as T23 recommended for its set, with this table as the map; let the next base merge drop the six. The decision is the maintainer's, on #346 beside T23's, from the coordinator.",
  where="`04` § Q1 and § Q6", ev="the dispositions (sum 778); 102 commits since June, 99 LibreELEC's; 0 fork-authored", vm=HOST,
  aw="nothing inherited: none of these is applied to an image; a removal changes only what the next merge reconciles",
  acc="the maintainer's decision recorded on #346 (and #1048 for any removal)"),
 dict(f="F-06", t="The brief's figure the run moved: *68 LibreELEC changes the override builds without* is 50 with no counterpart and 18 the override carries in another form (12 re-offset, 6 with the context moved)", sev="Low", cat="Documentation", q="Q7",
  area="`docs/reviews/briefs/patches-dead.md` (the coordinator's)", what="Recorded; whether the brief changes is the coordinator's.", where="the brief at `92f2f35c16` § 2", ev="`02` § The shadowed 74", vm=HOST, aw=NOTHING.replace("a patch no image applies has written nothing on a device or in a cloud; the tree is the only place it exists", "a brief writes nothing"),
  acc="a design: recorded with its sentence in the Phase 7 table"),
]

P7 = {}

def main():
  out = ["# Punch List — M6.P2 T40, the patches and kernel configurations no plan applies", "",
         "**Local depth** (D-WORKFLOW-184): no reviewer seat; the counts are the check. Every `where` is at `8ebaf8daad` (unchanged at the dispatch tip). The lane removes nothing and edits no `.patch`, `.conf`, recipe or tool (D-WORKFLOW-209). Generated by `tools/punch-items.py` from one list.", ""]
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
          gate.append(f"| {pl} | Open | stage D: the bugs filed; the coordinator's answers on #687 name the targets |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
  main()
