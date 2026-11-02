#!/usr/bin/env python3
"""Register, remove or inspect the ponytail-lite SessionStart/SubagentStart hooks.

Claude Code (settings.json) and Codex (hooks.json) share the same hooks shape.
Other hooks and settings are kept as they are; ours are appended at the end
so Codex trust entries (keyed by group index) of existing hooks stay valid.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import sys
from pathlib import Path

MARKER = "ponytail-lite/scripts/inject-context.sh"
MATCHERS = {"SessionStart": "startup|resume|clear|compact", "SubagentStart": None}
DEFAULT_HOOK = Path(__file__).resolve().parents[2] / MARKER


def codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def config_path(agent, scope, project):
    if agent == "claude":
        base = project / ".claude" if scope == "project" else Path.home() / ".claude"
        return base / "settings.json"
    base = project / ".codex" if scope == "project" else codex_home()
    return base / "hooks.json"


def load(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top level is not a JSON object")
    return data


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_name(path.name + ".ponytail-lite.bak"))
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def is_ours(hook):
    return MARKER in str(hook.get("command", ""))


def strip(groups):
    """Drop our hooks; return the remaining groups and the index of the first group we touched."""
    kept, first = [], None
    for group in groups:
        hooks = group.get("hooks", [])
        rest = [hook for hook in hooks if not is_ours(hook)]
        if len(rest) == len(hooks):
            kept.append(group)
            continue
        if first is None:
            first = len(kept)
        if rest:
            kept.append(dict(group, hooks=rest))
    return kept, first


def install(data, script):
    hooks = data.setdefault("hooks", {})
    for event, matcher in MATCHERS.items():
        groups, first = strip(hooks.get(event, []))
        group = {"hooks": [{"type": "command", "command": f"sh {shlex.quote(str(script))} {event}", "timeout": 10}]}
        if matcher:
            group = {"matcher": matcher, **group}
        groups.insert(len(groups) if first is None else first, group)
        hooks[event] = groups


def uninstall(data):
    hooks = data.get("hooks", {})
    for event in MATCHERS:
        if event in hooks:
            hooks[event], _ = strip(hooks[event])
            if not hooks[event]:
                del hooks[event]


def full_ponytail(agent, scope, project):
    """Names of enabled full Ponytail plugins, which would inject a second ruleset."""
    if agent == "claude":
        try:
            plugins = load(config_path("claude", scope, project)).get("enabledPlugins", {})
        except (OSError, ValueError):
            return []
        return [name for name, on in plugins.items() if name.startswith("ponytail@") and on]
    path = codex_home() / "config.toml"
    if not path.exists():
        return []
    found, section = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        header = re.match(r'\s*\[plugins\."(ponytail@[^"]+)"\]', line)
        if header or line.lstrip().startswith("["):
            section = header.group(1) if header else None
        elif section and re.match(r"\s*enabled\s*=\s*true\b", line):
            found.append(section)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["install", "uninstall", "status"])
    parser.add_argument("--agent", choices=["claude", "codex", "all"], default="all")
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--hook-script", type=Path, default=DEFAULT_HOOK)
    args = parser.parse_args()
    agents = ["claude", "codex"] if args.agent == "all" else [args.agent]
    script = args.hook_script.expanduser().resolve()

    if args.command == "install" and not script.is_file():
        sys.exit(f"{script} not found. Install the ponytail-lite skill first:\n"
                 "  npx skills@latest add yakami129/engineering-skills --skill ponytail-lite -g")

    paths = {agent: config_path(agent, args.scope, args.project_dir) for agent in agents}
    try:
        configs = {agent: load(path) for agent, path in paths.items()}
    except (OSError, ValueError) as error:
        sys.exit(f"Cannot read hook config, nothing changed: {error}")

    for agent, path in paths.items():
        data = configs[agent]
        if args.command == "install":
            install(data, script)
            save(path, data)
            print(f"{agent}: registered SessionStart and SubagentStart in {path}")
        elif args.command == "uninstall":
            if not path.exists():
                print(f"{agent}: {path} does not exist, nothing to remove")
                continue
            uninstall(data)
            save(path, data)
            print(f"{agent}: removed ponytail-lite hooks from {path}")
        else:
            for event in MATCHERS:
                hooks = [h for g in data.get("hooks", {}).get(event, []) for h in g.get("hooks", [])]
                state = "installed" if any(is_ours(h) for h in hooks) else "not installed"
                print(f"{agent} {event}: {state} ({path})")
        for name in full_ponytail(agent, args.scope, args.project_dir):
            print(f"{agent}: warning: full Ponytail plugin {name} is enabled; "
                  "disable it or the agent receives two rulesets")
        if args.command == "install" and agent == "codex":
            print("codex: open /hooks in Codex, trust both ponytail-lite hooks, then start a new thread")


if __name__ == "__main__":
    main()
