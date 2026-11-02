# Load ponytail-lite every session

Installed as a skill, `ponytail-lite` only loads when the agent decides a task needs it. To keep the rules in context for every session without editing `AGENTS.md` or `CLAUDE.md`, register [scripts/inject-context.sh](scripts/inject-context.sh) as a lifecycle hook. The script prints the `SKILL.md` body (frontmatter stripped) as `hookSpecificOutput.additionalContext`, the shape both Claude Code and Codex read. It needs only `sh`, `sed` and `awk`.

The quickest way is the [`setup-ponytail-lite`](../setup-ponytail-lite/SKILL.md) skill (`/setup-ponytail-lite`): it checks prerequisites, merges the entries below without touching other hooks, and can remove them again. The rest of this page is the manual route.

Two events:

- `SessionStart` loads the rules into the main session. Match `startup|resume|clear|compact` so they come back after `/clear` and compaction.
- `SubagentStart` loads them into each subagent, which never sees the parent's session context.

The commands below assume a global install by the skills CLI (`~/.agents/skills/ponytail-lite`). For a project install or a manual copy, point them at that skill directory instead.

## Claude Code

Merge into `~/.claude/settings.json` (all projects) or `.claude/settings.json` (one project). Append to existing `SessionStart` and `SubagentStart` arrays; don't replace them.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          { "type": "command", "command": "sh ~/.agents/skills/ponytail-lite/scripts/inject-context.sh SessionStart", "timeout": 10 }
        ]
      }
    ],
    "SubagentStart": [
      {
        "hooks": [
          { "type": "command", "command": "sh ~/.agents/skills/ponytail-lite/scripts/inject-context.sh SubagentStart", "timeout": 10 }
        ]
      }
    ]
  }
}
```

## Codex

Merge the same `hooks` object into `~/.codex/hooks.json` (or `<repo>/.codex/hooks.json` in a trusted project). Codex skips new or changed hooks until they are trusted: run `codex`, open `/hooks`, review and trust both, then start a new thread.

If the full Ponytail plugin is also enabled (`codex plugin list`, or `/plugin` in Claude Code), disable it first so the agent doesn't receive two rulesets.

## Verify

```bash
sh ~/.agents/skills/ponytail-lite/scripts/inject-context.sh SessionStart
```

The output is one JSON object. Then start a new session and ask the agent what always-on guidance it was given; it should quote the ponytail-lite ladder.

## Remove

Run `/setup-ponytail-lite` and ask to remove, or delete the two hook entries by hand. Uninstalling the skill without removing them leaves hooks that fail on a missing file.
