# 02-forward-audit

A fixture for tools/lint-audit-artifacts' index boundary (T10 S7, #945): a
table cell below quotes the lint's own `## Verification` heading, as the
2026-09-28 fix-round audit's line 192 did, before the real heading.

## Findings index (the seats' own severities)

| bucket | seat | id | severity | title | evidence |
| --- | --- | --- | --- | --- | --- |
| I | gpt | G2-I-06 | Medium | the boundary | the lint bounds the index with `forward.find("## Verification")` |
| I | gpt | G2-I-01 | High | a High row after the quoting cell | `tools/x:1` |

## Verification

- **G2-I-06** (gpt): read; Medium, carried as a lead.
