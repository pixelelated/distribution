#!/usr/bin/env bash
# T38 (#685) stage E, PL-24's check: the source estate's terms over the four imported skills that carry them, each
# line in one class -- provenance (a front-matter origin note), the fork's own sentence ("there is no docs/planning/
# here"), the term cornerstone alone (this repository's audits use it; defined in code-auditor § Project
# conformance), or the estate's (anything else). Run in an export's .claude/skills.
P='for scaffold|scaffold does not|cornerstone|logs/audits|example-api|services/|\.kno|caddy|OpenBao|tenant zero|docs/planning|docs/architecture|docs/design'
LC_ALL=C grep -r -i -E "$P" begin-delivery code-auditor futro mini-retro | awk '
  { l = tolower($0); sub(/^[^:]*:/, "", l)
    if (l ~ /^  origin:/) o++
    else if (index(l, "there is no `docs/planning/` here")) w++
    else { t = l; gsub(/cornerstone/, "", t)
           if (t ~ /for scaffold|scaffold does not|logs\/audits|example-api|services\/|\.kno|caddy|openbao|tenant zero|docs\/planning|docs\/architecture|docs\/design/) x++; else c++ } }
  END { printf "provenance %d ; the fork'"'"'s own %d ; the term cornerstone %d ; the estate'"'"'s %d\n", o, w, c, x }'
