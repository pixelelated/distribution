# Retrospective — M6.P2 T9, build supervision and host maintenance (#656)

Phase 3 of the code-auditor lifecycle: how these tools came to be what they are, read from the 35 fork commits since `c445081a59` and the evidence folders. The renovation face is in `04`.

## 3.1 What the history shows

- **Five waves, each a response to a failure the record names:**
  - **The watcher** (#393 to #395, D-WORKFLOW-141 to 143, early October): two unnoticed build failures in one day (`watch-job:14-16`) and blindspot 73, a monitor that read package completion as build activity.
  - **The swap helper and its installer** (#410, D-INFRA-015, 2026-10-04): the 2026-09-19 OOM that killed a guest and a watcher (`build-preflight:13-16`).
  - **Durable submission** (#444, D-WORKFLOW-148, 2026-10-05).
  - **Retention and admission** (#461, #489, #493, D-INFRA-018 and 022, 2026-10-07 to 10-15).
  - **The release tool's prepare-only rewrite** (#265, #530, #532, #565).
- **Each wave brought its controls,** and the evidence folders under `docs/qa-logs/` record what each guard caught when it was wired (`engineering-practices.md` § Guards must fail closed, *the positive is recorded where the guard is wired*).
- **The later waves did not re-run the earlier waves' controls.** The admission guard (`d7e2d6be41`, 2026-10-13) made `watch-build` refuse an unadmitted run.
  - It updated `test-build-monitor` through `admission-test-fixture.py`.
  - It left the three earlier controls (progress, the 2026-10-04 routing fixture, submission) refusing at the guard's first line.
  - The fork CI runs three controls, none of them these, so their failure has gone unseen for eleven days (F-01).

## 3.2 What worked

- **A guard ships with its refusal tests.** `test-swap-reclaim` (37 tests), `test-build-admission` (68 checks) and `test-retention-report` (19 controls) each construct their guards' failures with doubles, and none touches the real swap, sudoers or Docker.
- **Results belong to their producer.** The exclusive (`'x'`) writes in `watch-build-submit` and `build-admission`, and the runner's `atomic()`, keep each receipt single-writer (#597).
- **The record agrees with the watcher's contract:** 1,885 recorded runs, every one `finished`, and no `runner-error`.

## 3.3 What was hard, as the code shows it

- **Process identity across namespaces.** Each tool answers it differently:
  - `reclaim-swap` refuses unless PID 1 is `systemd` (`:81-82`);
  - `build-admission` binds the PID namespace inode (`:208`, `:246`);
  - `watch-job` reads `/proc/<pid>/stat` and treats an unreadable PID as dead (F-05);
  - `build-preflight` matches command lines by pattern (F-03).
- **One-incident recovery.** `consume-reporting-failure` (`build-admission:285-473`, 189 lines) settles the custody of one #597 collision. It is pinned to the current launcher's hash, so any edit to `watch-build-submit` retires it for future collisions; the guide says so (`build-admission.md:124-125`).

## 3.4 What the slice inherits from earlier lanes

- **T5's *read what the recorded builds would meet before a guard fails closed*:** the record read here (1,885 runs, 663 admitted) is that reading for these guards.
- **T8's *run a fork script once at stage B when it can run*:** the eight controls ran at stage A, and the two-layer cause of F-01 came from running diagnostics, not from reading.

## 3.5 The seams

| Seam | What crosses it | Read | State |
| --- | --- | --- | --- |
| The runner and the Makefile and five scripts | `Makefile:40` wraps native targets without `--entry`. The five scripts `exec ./tools/watch-build --entry` (`build:9`, `build_distro:11`, `image:9`, `install:10`, `build_compat:7`). `docker-%` runs `--docker` on the host and passes `-e RASTERATOPS_BUILD_RUN` into the container (`Makefile:179`, `:208`), whose scripts then reuse the run through `nested()`. | `test-build-monitor`'s 36 checks cover every entry line, the native and Docker routes and the docker-shell exemption | Holds. Inside `make docker-shell` there is no outer run, so a build there needs its own admission and reaches `admit()` on the container's Python 3.10 (F-04). |
| The admission and the retention report | `build-admission:104-159` reads the report beside its own `retention-report` (tool hash), its plan hash, `REPORT_COMPLETE`, no deletion, no inventory errors, the stage budget equal term for term, and an age of 900 s or less | `test-build-admission`'s report and budget cases | Holds, and it is where the report's errors become a refusal. The 900 s window covers the report's scan and the admission's preparation together; no recorded scan time was read against it. |
| The submit launcher and the runner's receipts | The launcher writes `launcher-*.json` and `tool-wrapper.rc`; the runner writes `build.rc` and `runner-result.json`. `consume` requires the three return codes to agree (`build-admission:259-262`). | `test-submit.py` (failing, F-01); `test-build-admission`'s recovery cases | Holds in the code; its control is broken. `launcher-submission.json` records `watch-build`'s hash only, not those of `watch-job` and `build-admission`, which it loads (`watch-build-submit:76`). |
| The preflight and the helper | The preflight calls `sudo -n /usr/local/sbin/pixelelated-reclaim-swap --reclaim` only below 20% free swap (`build-preflight:67-75`), the helper's own threshold (`reclaim-swap:143`), and re-reads memory afterwards (`:77`). The two cannot be combined with `--stop-vms` (`:47-50`). | `test-swap-reclaim`'s `Preflight` class, six tests | Holds. The preflight's "LOW" floor is 16,000 MB available (`:84`), and the helper needs used swap plus 16 GiB (`reclaim-swap:18`, `:125`); they measure different things and neither claims the other's number. |
| The release tool and `docs/releases/versioning.md` | the version pattern (`dev` refused), the build identity `<version>+<stamp>.g<12>`, the image-name prefix, the `v<version>` tag and the `pixelelated <version>` title | `tools/build-identity-test:104-167` (outside the slice) | Holds; the tool matches `versioning.md:10-13`, `:28-30`, `:53-57`, `:74`. |
