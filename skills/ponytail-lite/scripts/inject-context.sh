#!/bin/sh
# Print the ponytail-lite rules as hook context. Claude Code and Codex share this JSON shape.
# Usage: inject-context.sh SessionStart|SubagentStart
event="${1:-SessionStart}"
skill="$(dirname "$0")/../SKILL.md"

# Drop the frontmatter and leading blank lines, then JSON-escape backslashes, quotes and tabs.
sed '1,/^---$/d' "$skill" |
  sed -e '/./,$!d' -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/	/\\t/g' |
  awk -v event="$event" '
    BEGIN {
      printf "{\"hookSpecificOutput\":{\"hookEventName\":\"%s\",\"additionalContext\":\"", event
      printf "The user installed ponytail-lite as always-on guidance for all coding work in this session.\\n\\n"
    }
    { printf "%s\\n", $0 }
    END { print "\"}}" }
  '
