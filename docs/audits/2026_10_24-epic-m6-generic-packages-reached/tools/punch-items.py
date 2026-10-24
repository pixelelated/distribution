#!/usr/bin/env python3
"""05-punch-list.md from one list (#654): the items, the punch_index and the Phase 7 table.
    python3 -I punch-items.py > 05-punch-list.md
"""
VMNO = "No: a fetch property of a recipe, proved on the host (brief § 5; nothing here runs on an image)"
VMT = "No: the tree, the record and the release sources (brief § 5)"
AWF = "nothing on devices or in clouds: a recipe's source is a build input; the shared cache's file and stamp, and ROCKNIX's mirror, are the retained copies (D-INFRA-022)"
AWN = "nothing: a recipe's text or a record; no device or cloud holds anything of it"
BUMP = "the fork's: a Backlog issue in #839's shape, filed by the coordinator at acceptance for the first build after the M7 candidate; no pin moves in M6 (brief § 2, D-WORKFLOW-187)"
I = [
 dict(f="F-01", t="`libfmt` 9.1.0 is fetched with an empty `PKG_SHA256`, and T5's `get_archive` refuses it on GENERIC_X64 and H700", sev="High", cat="Interaction Defect", q="Q3", area="a ROCKNIX override of a generic recipe: `projects/ROCKNIX/packages/devel/libfmt`",
  what="The override is an orphan: ROCKNIX deleted it after the base (`6103571f67`, its PR #3470, 2026-10-11), so the next base merge removes it and `libfmt` becomes 12.2.0 with its checksum on every plan. Whichever lands first decides: if T5's branch (whose `get_archive:7-9` makes the empty value fatal) reaches `next` before the base merge, give the 9.1.0 branch its checksum, `5dea48d1fcddc3ec571ce2058e13910a0d4a6bab4cc09a809d8b1dd1c88ae6f2`, on which the live fetch, the shared cache's stamp and ROCKNIX's mirror agree (trust on first use, as D-WORKFLOW-193's stream did). The register needs a row refining D-WORKFLOW-194's count from five archive versions to six (the coordinator's).",
  where="`projects/ROCKNIX/packages/devel/libfmt/package.mk:11` (the row `packages/devel/libfmt/package.mk`)", ev="P6, P9, P10; `02` § The fetch sweep; `03` § 3.5",
  vm=VMNO, aw="nothing on devices or in clouds: the archive's bytes are a build input. Every GENERIC_X64 and H700 build since ROCKNIX wrote the empty value (`ea767206a2`, 2025-07-19) fetched 9.1.0 unverified; the cache's file `libfmt-9.1.0.tar.gz` and its stamp hold `5dea48d1...`, equal to today's fetch, so nothing already built is suspect on this evidence",
  acc="`PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 bash -c '. config/options libfmt; echo $PKG_SHA256'` prints `5dea48d1...` (and the same for H700 aarch64 and arm); `git grep -E 'PKG_SHA256=(\"\"|$)' -- '*package.mk'` prints nothing; with T5's `get_archive`, a fetch of `libfmt` for GENERIC_X64 into an empty source directory exits 0 with that sha256.",
  bug=True, upstream=True),
 dict(f="F-02", t="`wsdd2`'s `PKG_URL` is gone: the `Netgear/wsdd2` repository is deleted", sev="Low", cat="Code Quality", q="Q3", area="a generic recipe: `packages/network/wsdd2`",
  what="The source survives only in ROCKNIX's mirror and the shared cache (both `b0b6b315...`, equal to the recipe). LibreELEC master moved the recipe to `pesa1234/wsdd2` at v1.9.2, which has no 1.8.7 tag, so no `PKG_URL` line keeps 1.8.7 at a live origin: the fix is the base merge's bump; until then the mirror is the fetch's only working source and the cache's copy is a retained input.",
  where="`packages/network/wsdd2/package.mk:9`", ev="P8, P9, P13; `02` § The fetch sweep",
  vm=VMNO, aw=AWF, acc="a fetch of `wsdd2` for GENERIC_X64 into an empty source directory exits 0 with `b0b6b315...` (from the mirror today); the bug names the base merge that replaces the URL.",
  bug=True, upstream=True),
 dict(f="F-03", t="`newt`'s `PKG_URL` is gone: `releases.pagure.org/newt/` serves no archive", sev="Low", cat="Code Quality", q="Q3", area="a generic recipe (GENERIC_X64 only): `packages/tools/newt`",
  what="LibreELEC master carries the same URL, so the defect is upstream's; ROCKNIX's mirror serves the recipe's sha256 (`ef0ca9ee...`), and the shared cache holds the file. Record it; propose the URL to #585 when a live origin for 0.52.25 is found.",
  where="`packages/tools/newt/package.mk:9`", ev="P8, P9", vm=VMNO, aw=AWF,
  acc="a fetch of `newt` for GENERIC_X64 into an empty source directory exits 0 with `ef0ca9ee...`; the bug names the origin's state on each read.", bug=True, upstream=True),
 dict(f="F-04", t="`libmpeg2`'s `PKG_URL` ends in a 404 at `libmpeg2.sourceforge.io`", sev="Low", cat="Code Quality", q="Q3", area="a generic recipe: `packages/multimedia/libmpeg2`",
  what="LibreELEC master carries the same URL; the mirror serves `dee22e89...`, equal to the recipe; the cache holds the file. Record it; propose a live URL to #585 if one carries 0.5.1.",
  where="`packages/multimedia/libmpeg2/package.mk:10`", ev="P8, P9", vm=VMNO, aw=AWF,
  acc="a fetch of `libmpeg2` for GENERIC_X64 into an empty source directory exits 0 with `dee22e89...`.", bug=True, upstream=True),
 dict(f="F-05", t="`configtools`'s `PKG_URL` is refused (400) by savannah's new cgit host", sev="Low", cat="Code Quality", q="Q3", area="a generic recipe: `packages/devel/configtools`",
  what="Three reads over six minutes: 400, 502, 400. LibreELEC master carries the same URL; the mirror serves `6e4ebaa2...`, equal to the recipe; the cache holds the file. Re-read before a fix; if it holds, propose savannah's current snapshot URL to #585.",
  where="`packages/devel/configtools/package.mk:10`", ev="P8, P9", vm=VMNO, aw=AWF,
  acc="a fetch of `configtools` for GENERIC_X64 into an empty source directory exits 0 with `6e4ebaa2...`; the bug records each read of the origin with its time.", bug=True, upstream=True),
 dict(f="F-06", t="`brotli` 1.2.0 is behind its project's 1.2.1", sev="Low", cat="Renovation", q="Q4", area="a fork-introduced recipe: `packages/compress/brotli`",
  what=BUMP, where="`packages/compress/brotli/package.mk:5`", ev="P5 (`q4c.txt`)", vm=VMT, aw=AWN,
  acc="the Backlog issue exists, in #839's shape, citing this item; `tools/fork-package-freshness brotli` prints BEHIND until it lands.", defer="a Backlog issue (#839's shape)"),
 dict(f="F-07", t="`ruby` 3.3.12 is behind 3.3.13 in its declared series", sev="Low", cat="Renovation", q="Q4", area="a fork-introduced recipe: `packages/devel/ruby`",
  what=BUMP, where="`packages/devel/ruby/package.mk:6`", ev="P5", vm=VMT, aw=AWN,
  acc="the Backlog issue exists, in #839's shape, citing this item.", defer="a Backlog issue (#839's shape)"),
 dict(f="F-08", t="`glib-networking` 2.90.0 is behind 2.90.1", sev="Low", cat="Renovation", q="Q4", area="a fork-introduced recipe: `packages/network/glib-networking`",
  what=BUMP, where="`packages/network/glib-networking/package.mk:5`", ev="P5", vm=VMT, aw=AWN,
  acc="the Backlog issue exists, in #839's shape, citing this item.", defer="a Backlog issue (#839's shape)"),
 dict(f="F-09", t="`webkitgtk` 2.54.1 is behind 2.54.2", sev="Low", cat="Renovation", q="Q4", area="a fork-introduced recipe: `packages/web/webkitgtk` (the sign-in window, #576)",
  what=BUMP + "; the bump is the costly one (`device-builds.md` § Before a build: webkitgtk's memory)", where="`packages/web/webkitgtk/package.mk:5`", ev="P5", vm=VMT, aw=AWN,
  acc="the Backlog issue exists, in #839's shape, citing this item.", defer="a Backlog issue (#839's shape)"),
 dict(f="F-10", t="the sixteen fork-own recipes sit under `packages/`, where upstream refuses a PR (#645)", sev="Low", cat="Renovation", q="Q7", area="the upstream series: #645's move table",
  what="Post `04` § Q7's sixteen rows on #645 (the coordinator, D-WORKFLOW-189): thirteen moves under `projects/ROCKNIX/packages/<group>/<name>` (with `woff2`'s and `webkitgtk`'s patches), three #585 proposals with an override as the fallback. The slice moves nothing.",
  where="`04-analysis.md` § Q7", ev="P2, P3; `02` § The #644 findings (17)", vm=VMT, aw="nothing: no file moves in this slice; a move later changes no installed path (the recipe's install lines are unchanged), so nothing on a device differs",
  acc="#645 carries the sixteen rows with a link to `04` § Q7; `git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- packages` is empty.", defer="#645"),
 dict(f="F-11", t="`btrfs-progs` is in GENERIC_X64's plan and absent from the M7 GENERIC_X64 root and its image", sev="Low", cat="Renovation", q="Q6", area="the record: the M7 GENERIC_X64 build root and the inventory",
  what="A note for the inventory's owner and the M7 lane (brief § 4 Q6: the coordinator files it under #657's epic): `viewplan` at the hash and the image recipe name `btrfs-progs`; the root `m7-signin-build-20261022-07` (`069fc27044`) has no build directory, no stamp and no `mkfs.btrfs`; the H700 and SM8550 roots have all three. Not explained by reading.",
  where="`projects/ROCKNIX/packages/virtual/image/package.mk:14`; the root's `.stamps`", ev="P11", vm="Yes, later: the next GENERIC_X64 image's `image/system/usr/sbin` read on the host, or `ls /usr/sbin/mkfs.btrfs` on its guest; not run here (no guest in this slice)",
  aw="the GENERIC_X64 image of 2026-10-23 (`069fc27044`) carries no btrfs tools; nothing written by them exists to inherit",
  acc="the note is filed under #657's epic, citing this item, with the three reads quoted.", defer="#657"),
 dict(f="F-12", t="the inventory's `shadowed_by` cannot see an override that sources the generic recipe; three change the effective pin", sev="Low", cat="Renovation", q="Q7", area="P1's tool: `tools/renovation-inventory`",
  what="47 ROCKNIX overrides source one of the 243; `opus`, `gcc` and `libfmt` set their own version, four their own URL or checksum; six of the 47 are absent on `upstream/next` (`libfreeaptx`, `opus`, `libfmt`, `harfbuzz-icu`, `gst-plugins-bad`, `gnutls`: #644 finding 16's orphans, T8's). Add an effective-pin note (or a `sourced_by` column) so a currency read does not take the generic recipe's pin as the image's. A lead for #657.",
  where="`docs/reviews/inventory.json` (its columns); `sourcing-overrides.txt`", ev="P12", vm=VMT, aw=AWN,
  acc="#657 carries the lead with this item's text.", defer="#657"),
 dict(f="F-13", t="`libsoup` and `ruby` cut the release series from the version with `${PKG_VERSION:0:3}`", sev="Low", cat="Renovation", q="Q7", area="fork-introduced recipes: `packages/web/libsoup`, `packages/devel/ruby`",
  what="`${PKG_VERSION:0:3}` of `3.10.0` is `3.1`, so the first two-digit minor fetches from the wrong directory and the fetch fails. `glib-networking:6`'s `${PKG_VERSION%.*}` is the shape that holds. A `PKG_URL` line is a fix the table can carry (brief § 2); its test is a fetch of the current version into an empty directory, unchanged sha256.",
  where="`packages/web/libsoup/package.mk:9`; `packages/devel/ruby/package.mk:10`", ev="the read; `04` § Q7", vm=VMT, aw=AWN,
  acc="both `PKG_URL` lines derive the series without a fixed width, and each expands, through `config/options`, to the URL it gives today."),
 dict(f="F-14", t="22 recipes fetch over http; `glu`'s https URL redirects to http", sev="Low", cat="Renovation", q="Q1", area="generic recipes (`04` § Q1 lists them)",
  what="Integrity rests on `PKG_SHA256`, which every one carries and which matched for each fetched; transport is the modernization. Two are the fork's to change (`dmidecode`'s own recipe; `syslinux`'s edited copy keeps upstream's URL); the other twenty are #585 candidates (D-WORKFLOW-164; submission held, D-WORKFLOW-165).",
  where="`packages/sysutils/dmidecode/package.mk:11` and the 21 others in `probe/expand.txt`", ev="P8, P9", vm=VMT, aw=AWN,
  acc="`dmidecode`'s `PKG_URL` is https and expands to an archive with the same sha256; the twenty upstream rows are in #585's proposal.", upstream=True),
 dict(f="F-15", t="five GitHub `PKG_URL`s name a renamed (3), archived (1) or personally forked (1) repository", sev="Low", cat="Renovation", q="Q1", area="generic recipes: `lm_sensors`, `libfreeaptx`, `nss-mdns`, `oniguruma`, `populatefs`",
  what="Today's bytes are right (all five fetched and matched); a renamed repository's archive is #841's class, an archived one stops receiving fixes, and `populatefs`'s `kfix` fork is portaudio's shape (#849). LibreELEC master carries all five as they are: #585 candidates, following the base merge.",
  where="the five recipes' `PKG_URL` lines (`populatefs:10`)", ev="P13", vm=VMT, aw=AWN,
  acc="#585's proposal names the five with their current owners.", upstream=True),
]

P7 = {}   # (outcome, evidence, proved) by F; filled at Phase 7

def main():
  out = ["# Punch List — M6.P2 T7, the generic packages the image builds", "",
         "**Local depth** (plan § 6c, D-WORKFLOW-184): no reviewer; Phase 4.5 in `04`. Fifteen items, one High: five `bug`s (PL-01 to PL-05), four Backlog bumps (PL-06 to PL-09), the #645 rows (PL-10), and six `Renovation` rows. Every `where` is at `8ebaf8daad`. Generated by `tools/punch-items.py` from one list, so the items, the `punch_index` and the Phase 7 table agree.", "", "---", ""]
  idx = ["```yaml", "punch_index:"]
  gate = ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
  for n, x in enumerate(I, 1):
      pl = f"PL-{n:02d}"
      out += [f"## {pl}: {x['t']}", "", f"- **Severity:** {x['sev']}", f"- **Category:** {x['cat']}", f"- **Question:** {x['q']}", f"- **Source Finding:** {x['f']}", f"- **Owner area:** {x['area']}", f"- **What:** {x['what']}", f"- **Where:** {x['where']}", f"- **Evidence:** {x['ev']}", f"- **Can this be done on the VM?** {x['vm']}", f"- **Already written:** {x['aw']}", f"- **Acceptance:** {x['acc']}"]
      if x.get("bug"): out.append("- **Bug issue:** filed at stage D")
      if x.get("upstream"): out.append("- **Upstream:** a #585 candidate (D-WORKFLOW-164; submission deferred, D-WORKFLOW-165); the coordinator posts it")
      if x.get("defer"): out.append(f"- **Disposition note:** deferred to {x['defer']} at Phase 7")
      out.append("")
      idx += [f"- id: {pl}", f"  severity: {x['sev']}", f"  category: {x['cat']}", f"  question: {x['q']}", f"  source_finding: \"{x['f']}\"", f"  owner_area: \"{x['area'].replace(chr(34), chr(39))}\""]
      if x.get("bug"): idx.append(f"  tracked: \"{x.get('tracked', 'bug issue filed at stage D')}\"")
      p7 = P7.get(x["f"])
      if p7:
          idx.append(f"  outcome: \"{p7[0].lower()}\"")
          if p7[2]: idx.append(f"  proved: \"{p7[2]}\"")
          gate.append(f"| {pl} | **{p7[0]}** | {p7[1]}{'; ' + p7[2] if p7[2] else ''} |")
      else:
          idx.append("  outcome: open")
          gate.append(f"| {pl} | Open | stage D files the issue; a stage-E stream brief or the named issue resolves |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
    main()
