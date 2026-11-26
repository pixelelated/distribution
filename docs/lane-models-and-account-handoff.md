# Lane models and account handoff

D-WORKFLOW-198 applies to the OS and codebase-renovation workspaces; D-WORKFLOW-200 (Max, 2026-11-24) sets which harness and model each role runs. Choose the role when a lane is created or reopened; it selects the harness and tier. Keep the same worktree, task owner, permissions and native thread on an account switch. Each workspace manager continues to own its workers.

| Role (`--role`) | Harness and model | Reasoning and permissions |
| --- | --- | --- |
| One-on-one steward (`steward`) | Claude Code, latest Fable: `claude-fable-5-2` | `xhigh`, existing native permissions |
| OS work coordinator (`coordinator`) | Claude Code, latest Opus: `claude-opus-5-5` | `xhigh`, existing native permissions |
| Worker (`worker`) | Codex, latest GPT Sol: `gpt-6.2-sol` | `xhigh`, fast mode (`service_tier="priority"`, D-WORKFLOW-238), workspace-write, on-request, automatic approval review |

Max, 2026-11-24: *"the one-on-ones should be running the latest Fable, and the work coordinator runs the latest Opus, and the worker lanes run GPT Soul on the latest"*. `tools/herdr-lane` refuses a Codex coordinator or steward. A Claude worker departs from the policy and needs an explicit `--tier`. When a newer Fable, Opus or GPT Sol ships, update the launcher's model table and this one together.

**Fast mode (D-WORKFLOW-238).** Max, 2026-11-25: *"Also, for any lane in pixelelated or in the pixelelated code audit, let's make sure we're running it in fast mode if it's using the Codex harness (because there's a promotion running now through the end of the year, where fast mode is included for free in ChatGPT Codex)."* `tools/herdr-lane` passes `-c service_tier="priority"` to every Codex lane it launches or resumes. That is gpt-6.2-sol's fast tier in codex-cli 0.172.0's catalog (shown as "Fast", "2x speed, increased usage"). Never set it in the shared `~/.codex/config.toml`, which other projects' lanes read, and never with the in-session Fast toggle, which saves its choice there. An open lane is switched by closing its Codex client and resuming the same thread through `tools/herdr-lane`. A tier the model does not advertise is dropped without an error, so the proof is the rollout's `thread_settings_applied` record saying `priority` after the first turn. Revisit when the promotion ends (end of 2026).

Retain any narrower approved profile, specific writable roots, or managed restrictions. The launcher encodes the two workspaces' standard Codex profile. When the original lane requires different limits, inspect its effective profile and retain them before starting it. Claude Code uses its own permission system. Its native default inherits settings; pass an explicit permission mode only when it matches the lane's established policy. Check active permission rules, including project and managed rules. Keep separately authorized device and publication actions within their existing scope.

## Start or resume one lane

Use `tools/herdr-lane` from canonical `next`, including when the worktree assigned to the lane is on an older branch. Both commands print argv by default. On a user-authorized launch, run the same command with `--apply` from the intended Herdr session. `fresh` creates an unfocused tab and starts the native client in its returned pane. `resume` reuses the original pane at its shell prompt. It checks the UUID and saved worktree in the selected harness's transcript store before starting the client. Native thread IDs are harness-specific. A deliberate harness change needs a fresh thread and the outgoing conversation's project handoff.

```sh
tools/herdr-lane fresh --workspace w4 --name os-worker --cwd "$worktree" --role worker
tools/herdr-lane resume --workspace w4 --pane "$original_pane" --session "$thread" --name os-coordinator --cwd "$worktree" --role coordinator
tools/herdr-lane fresh --workspace wN --name renovation-worker --cwd "$worktree" --role worker
tools/herdr-lane fresh --workspace w4 --name one-on-one --cwd "$worktree" --role steward
```

The role supplies the harness and tier; pass `--harness` or `--tier` only to record a deliberate, named departure from D-WORKFLOW-200. Retain the returned workspace, pane, native UUID, role, cwd and start result in operational records. On timeout or identity mismatch, inspect the original pane and process before repeating any action.

## User-initiated account handoff

1. Capture the original native UUID, absolute cwd, harness, role/tier, effective model, effort, sandbox and permission/review settings. Inspect outstanding CLI jobs, worker returns and native approvals. Preserve the thread and pending work before closing a client. Only the designated rollout owner changes live panes.
2. Run `tools/herdr-lane stores` in the actual launch environments. Check the OS user, home, resolved `CODEX_HOME` or `CLAUDE_CONFIG_DIR`, and credential backend/profile. Codex normally uses `~/.codex`, Claude Code normally uses `~/.claude` and its native credential store. An override, keyring context, managed provider or environment credential can change the effective identity. Inspect configured mode and override **names** only. Avoid opening or copying credentials, filtering secrets after collection, or putting account details in a report.
3. Authenticate **once per distinct harness and shared credential store**. For Codex use `codex login status` and `codex login`. For Claude Code use `claude auth status` and `claude auth login`. If the native switch requires signing out, use that harness's logout only for the requested account change. The two workspaces on this host share a UID and the default Codex store. Both also resolve the same default Claude directory. Signing into one harness does not authenticate the other. An already confirmed fresh login needs no repeat.
4. Resume the pinned native thread after the owner verifies the old application exited and its jobs have been reconciled. Inspect the ready pane's cwd and UUID. In Codex check the displayed model/effort and `/status`; verify effective sandbox, approval policy and reviewer in the runtime context or native session settings. In Claude Code check `/model`, `/status`, the displayed effort and `/permissions`. Verify the provider's returned model metadata on the next authorized call. An argv preview or a successful login establishes neither effective settings nor completed work. Resolve discrepancies before dispatch.
5. Inspect the actual job results, resource ownership and last accepted milestone. Continue the next authorized step. Preserve failed and completed attempts across account changes.

## Reviewer identity

Use the existing Facilitator for review and council calls. Keep the tier and reasoning budget selected by the review route. Direct Anthropic identifiers are in the table above. OpenRouter uses `anthropic/claude-fable-5.2` and `anthropic/claude-opus-5.5`; check the provider's returned model using the route's verification logic. Interactive lane defaults do not change another lab's council seat. Run the offline Facilitator routing and verification tests and `tools/herdr-lane-test` after changes.
