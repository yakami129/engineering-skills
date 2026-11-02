---
name: grilling
description: Grill the user relentlessly about a plan, decision, idea, or feature requirements until there is a shared understanding. Use when the user wants to stress-test their thinking, clarify requirements before building ("ask me first", "梳理需求", "先问清楚再开工"), or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

## Before the first round

Restate what you are grilling in 1–3 sentences: what is being built or decided, who it is for, and what the session should produce. If the user opened with a long description, first sort it into what is already clear, what is missing, and what contradicts itself. Seed the tree from the missing and contradictory parts; don't re-ask what the user has already told you.

## Rounds

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

If your environment has a structured question tool (for example `AskUserQuestion` in Claude Code), you may use it for questions with discrete options: put your recommended answer first and mark it as recommended, and leave room for a free-form answer. Split the round across several calls if the tool limits how many questions it takes. Open-ended questions stay in the text format above.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Open the next round with a short summary of what was just settled ("So far: A, B, C. Still open: X and Y."), then recompute the frontier and ask. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Keep rounds digestible. If the frontier grows beyond about five questions, or the user signals overload, ask which branch they want to settle first and take the rest in later rounds.

## What to ask

Spend questions on decisions and trade-offs, not on details that convention or a sensible default already settles. "If A and B conflict, which do you give up?" is worth asking; "should the button have a hover state?" is not. Push for concrete examples wherever the answer is fuzzy, especially failure modes and edge cases.

When the subject is a feature, module, or system, use [COVERAGE.md](COVERAGE.md) to find branches the tree is missing. Don't walk it as a script; merge and skip dimensions the conversation has already covered.

## Facts and decisions

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. For a feature or system, that also means every relevant dimension in [COVERAGE.md](COVERAGE.md) has been touched, and recent rounds are adding detail rather than new large branches. Summarise the shared understanding, list anything deliberately left open, and do not act on it until the user confirms you have reached a shared understanding.
