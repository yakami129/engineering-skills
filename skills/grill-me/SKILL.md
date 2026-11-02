---
name: grill-me
description: Interview the user over several rounds to work through requirements, technical approach, UI/UX, edge cases, and trade-offs, then write a structured spec to docs/exec-plans/. Use when the user wants requirements clarified, an interview, a SPEC or PRD, or to ask everything before work starts. Invoke with /grill-me.
disable-model-invocation: true
---

# Interview mode

> **Use the structured question tool.** Put every question, choice, and discussion point to the user through your environment's structured question tool (for example `AskUserQuestion` in Claude Code), not as plain text in the conversation. Fall back to plain conversational questions only when no such tool is available.

## When to use

Apply this skill when any of these is true:

- The user says "talk the requirements through with me first", "help me sort out the requirements", or "write a SPEC/PRD".
- The user has only a rough idea for a new feature or refactor and needs the details settled before work starts.
- The user wants you to lead the questioning instead of listing every detail themselves.

## Overall flow

1. Pin down what is being designed (a feature, module, or system) and the output: a spec.
2. Interview over several rounds, grouping questions by dimension instead of asking everything at once.
3. Dig into technical approach, UI/UX, edge cases, concerns, and trade-offs; don't stop at surface requirements.
4. Summarise at key points: play back your current understanding, surface your assumptions, and let the user correct them.
5. Once every key dimension is covered, write a structured spec from the conversation into the project (see [Step 6](#step-6-write-the-spec)).

## Using the question tool (required)

Ask every interview question through the structured question tool where you can.

- **Always use it to:**
  - collect structured preferences (priorities, locations, languages, technology choices); one call can ask several questions
  - have the user choose or trade off (for example, which side they lean to when A and B conflict)
  - confirm key decisions (scope, acceptance criteria, the level of each non-functional requirement)
- **How to use it:**
  - Each round, group 2–5 questions by dimension and present them in one call. Split the round across calls if the tool limits how many questions it takes.
  - Turn deep questions that resist fixed options into "single choice + other (please add)", or break them into several choosable options.
  - After the user answers, summarise in plain language, then start the next round.
- **Only when no such tool is available:** fall back to planned, grouped, multi-round questions in the conversation, keeping the same interview rhythm.

## Interview dimensions (coverage checklist)

A complete interview usually needs to reach all of these dimensions; adjust the order to the context:

1. Goals and scope
2. Users and scenarios
3. Flow and information architecture
4. Data model and interfaces
5. Technical approach and architecture
6. UI/UX requirements
7. States, errors, and edge cases
8. Non-functional requirements (performance, security, scalability, operability)
9. Risks, trade-offs, and non-goals
10. Acceptance criteria and examples

[COVERAGE.md](COVERAGE.md) gives what each dimension should clarify and example questions for it. Don't recite the checklist item by item; jump between and merge dimensions based on what the user has already said. Before you finish, check that every dimension has been touched at least once.

## Step 1: Set up and align expectations

1. **Restate the goal.** In 1–3 sentences, restate your understanding of what the user needs:
   - what is being built (a short description of the feature, module, or system)
   - who the main users or callers are
   - that the output is a spec, used for the design and implementation that follow

2. **Confirm the output location.**
   - Write the spec to `docs/exec-plans/YYYY-MM-DD-<slug>.md`, for example `docs/exec-plans/2026-06-21-terminal-ime-paste.md`. `YYYY-MM-DD` is the date the spec is written; `<slug>` is a name you generate from the subject: two to five lowercase English words joined by hyphens, naming what is being built.
   - Propose the full path to the user. If they name another path in this session, use theirs.
   - If `docs/exec-plans/` doesn't exist, create it when you actually write the file.

3. **Extract what is already known.**
   - If the user opened with a long description, don't start asking yet. First pull out the key points:
     - what is already fairly clear
     - what is obviously missing or contradictory
   - Aim the questions that follow at the gaps, the vague parts, and the conflicts first.

## Step 2: Interview by dimension over several rounds

Work in a loop of "a small group of questions, then a summary", not a dozen questions at once.

**Ask every round through the structured question tool.** Turn 2–5 of the dimension's example questions from [COVERAGE.md](COVERAGE.md) into the tool's options for the user to choose from or add to. After the user answers, summarise in plain language, then move on to the next dimension.

## Step 3: Interview style

- **Don't ask the obvious.**
  - Skip details that common sense or default design conventions settle, such as "should this button have a hover state?"
  - Prefer questions like: "If A and B conflict, which would you give up, and why?"

- **Summarise and confirm instead of mechanically following up.**
  - If the user has already given a lot of information, first sum it up in your own words: "It sounds like A, B, and C are settled, and X and Y are still unclear. Is that right?"
  - Dig further only where the summary exposes something unclear or ambiguous.

- **Control the pace.**
  - Keep each round to 2–5 questions, and summarise after the user answers.
  - If the user is clearly overwhelmed, pause, ask "Which part would you like to settle first?", and reprioritise.

## Step 4: Decide when to stop

Before writing the spec, check for yourself:

- Has each of the 10 dimensions been touched at least once?
- Is there still an obvious large open question (for example, the technical direction is completely undecided)?
- In the last few rounds, has the user mostly been adding detail rather than bringing in large new areas?

When you judge the information is enough to support an implementation, tell the user something like:

> I've now covered the goals, scope, technical approach, UI/UX, edge cases, and trade-offs.
> Next I'll put together a full spec draft from our conversation; you can add to or correct it.

If the user wants to keep digging into a dimension, run one or two more focused rounds on it.

## Step 5: Draft the spec

Use the structure in [SPEC-FORMAT.md](SPEC-FORMAT.md), adding or removing sections to fit the subject.

Before writing the file, post the complete draft as markdown in the conversation and ask the user to read it through as a whole at least once, then revise it once with their additions.

## Step 6: Write the spec

- **Default path:** `docs/exec-plans/YYYY-MM-DD-<slug>.md`, as agreed in Step 1.
  - If `docs/exec-plans/` doesn't exist, create it before writing.
  - If the user asks for another path, respect their choice.
- **How to write it:**
  - Create or overwrite the file with the file editing tools available in the project.
  - Before overwriting an existing file, briefly compare the old and new content, even at a high level, so nothing important is lost by accident.

## Glossary and ADRs

While interviewing, read and apply [domain-modeling](../domain-modeling/SKILL.md): write resolved terms to `GLOSSARY.md` and record decisions that meet its ADR criteria. The spec uses the glossary's terms and links to ADRs instead of restating them. That sibling skill must be installed for this workflow.

## Short example

**User:**
I want to build a new "task reminder" feature. Use interview mode to work out the requirements and details with me, and produce a spec at the end.

**Agent (following this skill), roughly:**

1. Restates in 1–3 sentences its understanding of "task reminder" and confirms the spec will go to `docs/exec-plans/2026-06-21-task-reminder.md`.
2. Asks over several rounds in roughly this order: goals and scope → users and scenarios → flow → data and interfaces → technical approach → UI/UX → edge cases → non-functional requirements → trade-offs → acceptance criteria, summarising every round or two.
3. Notes what the user says about hard parts and trade-offs (for example, whether reliability or flexible configuration matters more).
4. When there is enough information, drafts the full spec from the interview and posts it in the conversation for the user to confirm.
5. Once the user confirms, writes the final version to `docs/exec-plans/2026-06-21-task-reminder.md` and reminds the user how to use it in later development.
