## Maintainer question

> Do we need another 4 TB drive for build space? I wasn't expecting it to get used up this fast or to have this much space full. If I need to get a second drive so we can set up a RAID array and get us 8 TB for build space, I can do that.

## Current state

The approved #491 cleanup and #492 H700 then SM8550 builds continue. Before recommending a purchase, distinguish active build requirements from accumulated build/image/VM history. The October5 inventory is historical and must not be presented as current after subsequent builds and removals. The maintainer has clarified RAID0; assess that option without revisiting RAID-level intent. This task authorizes read-only assessment, not disk formatting, RAID conversion, purchase or additional deletion.

Can this be done on the VM? No: actual host filesystem allocation, build-directory usage and storage layout are host facts. The report is read-only and requires no handheld action.

## Acceptance criteria

- [x] A dated read-only report reconciles current filesystem availability and allocated usage by major build/artifact/cache/QA area, with unreadable paths disclosed.
- [ ] A capacity recommendation separates current/fallback/source/evidence retention from superseded working copies and budgets H700 then SM8550 without assuming unapproved cleanup.
- [ ] The recommendation compares the existing drive, separate added capacity, and two-drive RAID0 usable capacity and failure behavior using primary documentation; it names whether more hardware is currently justified and what remains uncertain.


## Clarification

> Yeah, I meant RAID 0.

Compare the capacity/performance case for RAID0 with bounded retention and a separate build volume; do not re-ask which RAID level was intended. No storage conversion is requested yet.


## Post-build cleanup request — 2026-10-07T04:26:30.133810+00:00

> Once this build is done, we should really look at how we can clear out as much space as possible. If we have a 4 TB drive, we shouldn't be running into these compilation issues given that much space. Hopefully, we can sort it out, or we'll consider getting a RAID set up to give us combined 8 TB of build space if needed.

After this build completes, broaden the retention review beyond #494’s four VM trees to the large retained-image and temporary-QA stores. Keep current and useful fallback builds, the ROCKNIX adoption baseline, exact source/licence inputs and required independent failure/QA evidence. Prepare exact removable sets and measured net recovery; any new deletion or RAID operation still gets a concrete separate decision. Required qualification precedes retirement under D-INFRA-018.

- [ ] After successful build/required qualification, a refreshed report classifies the large build, image and temporary-QA stores into protected dependencies and exact proposed retirements, with measured preservation cost, net recovery and next-build headroom.
- [ ] The post-build recommendation records a repeatable retention cadence and capacity triggers, then determines whether bounded retention suffices or another4TB drive is warranted; no hardware purchase is assumed.

Current evidence: published next63ef759a, docs/qa-logs/2026-10-07-device-builds. The actual first H700 failure was GCC12/SPIRV host compatibility (#495), now repaired; capacity separately constrains subsequent build stages. The four-tree preservation completed04:24:03, costing59,297,792allocated bytes and estimating432.57GiB net recovery, pending remaining dependency review and explicit removal approval.

Dependency review narrowed #494: replacement12 stays because two retained QA overlays still link to its source. Three remaining trees offer324.38 GiB potential net recovery, pending root process readback and exact deletion approval. This would establish the next H700 firmware budget; SM8550 still gets its own later capacity check. The sizing02 image-store census includes104 x64-prefixed directories (417,036,288,000 bytes) and117 H700-prefixed directories (440,225,484,800 bytes); these names are review groups, not proof of disposable contents. Refresh and classify after successful build/qualification.

The later arm04 failure was a generated-path identity mismatch (#497), not disk exhaustion: DISTRO remains ROCKNIX while build roots use DISTRONAME=pixelelated. The scoped source repair passes42 controls and the fresh arm05 build is running. Actual storage pressure remains a separate capacity gate.
