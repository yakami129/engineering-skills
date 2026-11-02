---
name: setup-ponytail-lite
description: Register ponytail-lite as always-on context through SessionStart and SubagentStart hooks in Claude Code and Codex, without editing AGENTS.md or CLAUDE.md. Also checks, reinstalls or removes the hooks. Invoke with /setup-ponytail-lite.
disable-model-invocation: true
---

Wire the `ponytail-lite` rules into the user's agents with lifecycle hooks, so every session and every subagent starts with them. All config edits go through [scripts/setup.py](scripts/setup.py) (Python 3.9+, standard library only); don't hand-edit hook JSON.

`SETUP` below means `python3 <this skill's directory>/scripts/setup.py`.

## 1. Check the prerequisite

The hooks run `ponytail-lite/scripts/inject-context.sh` from the `ponytail-lite` skill installed next to this one. If that skill is missing, `SETUP install` stops without writing anything. Offer to install it in the same scope as this skill:

```bash
npx skills@latest add yakami129/engineering-skills --skill ponytail-lite -g
```

## 2. Show the current state

Run `SETUP status` and show the output. It lists each agent's config file, whether each event is registered, and warns when the full Ponytail plugin is enabled.

## 3. Agree on the target

Ask only what the status didn't answer:

- **Agents**: `--agent claude`, `--agent codex`, or `--agent all` (default). Configure only the agents the user actually uses.
- **Scope**: `--scope user` (default; `~/.claude/settings.json` and `$CODEX_HOME/hooks.json`, every project) or `--scope project` (`.claude/settings.json` and `.codex/hooks.json` in the current repo, shared with collaborators who commit them).

These are the user's own config files and often hold other hooks. Say which files will change and get a yes before writing.

## 4. Resolve a full Ponytail conflict

If status warned about an enabled `ponytail@…` plugin, both rulesets would be injected. Ask the user whether to disable it:

- Codex: in `$CODEX_HOME/config.toml`, set `enabled = false` under `[plugins."ponytail@ponytail"]`.
- Claude Code: run `/plugin` and disable it, or set its `enabledPlugins` value to `false` in `settings.json`.

If they keep it, continue; the warning is advice, not a blocker.

## 5. Install

Run `SETUP install` with the agreed flags. The script:

- appends one `SessionStart` group (matcher `startup|resume|clear|compact`) and one `SubagentStart` group per agent, after existing hooks, so Codex trust for those hooks stays valid
- replaces its own earlier entries instead of duplicating them, so rerunning is safe
- leaves every other hook and setting untouched, and writes `<file>.ponytail-lite.bak` before changing an existing file
- refuses to write if a config file isn't valid JSON

For Codex, tell the user to open `/hooks`, review and trust both ponytail-lite hooks, and start a new thread. Codex skips untrusted hooks silently.

## 6. Verify

1. Run `SETUP status`; both events should be `installed` for each chosen agent.
2. Run one registered command, e.g. `sh <ponytail-lite dir>/scripts/inject-context.sh SessionStart`, and check it prints one JSON object.
3. Ask the user to start a new session and ask the agent to quote rung 3 of the ponytail-lite ladder. It should answer "Does the standard library do it? Use it."

## Remove

Run `SETUP uninstall` with the same `--agent` and `--scope`. It deletes only ponytail-lite hooks. Do this before uninstalling the `ponytail-lite` skill; otherwise every session starts with a hook that fails on a missing file.
