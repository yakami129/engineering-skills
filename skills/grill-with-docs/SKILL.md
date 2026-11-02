---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's, glossary, and a SPEC.md for features) as we go.
disable-model-invocation: true
---

Use the following two installed skills together:

1. Read and apply [grilling](../grilling/SKILL.md) to conduct the interview.
2. Read and apply [domain-modeling](../domain-modeling/SKILL.md) to capture resolved terminology and qualifying decisions as the discussion progresses.

Both sibling skills must be installed for this workflow.

## SPEC.md

When the session is designing a feature, module, or system, it also produces a spec. Confirm at the start whether the user wants one and where it goes (default `docs/SPEC.md`). Skip it for decisions that don't describe something to build.

Each document keeps its own job:

- `GLOSSARY.md` holds terms only, written as they are resolved.
- ADRs hold the few decisions that meet domain-modeling's three criteria.
- `SPEC.md` holds everything else that implementation needs: scope, flows, data, technical approach, UI/UX, edge cases, non-functional requirements, trade-offs, and acceptance criteria. It uses the glossary's terms and links to ADRs instead of restating them.

Write the spec once grilling is done and the user has confirmed the shared understanding:

1. Draft it in the conversation using [SPEC-FORMAT.md](SPEC-FORMAT.md), dropping sections that don't apply. Mark anything still undecided as an open question rather than filling it with an assumption.
2. Ask the user to read the whole draft, then revise it with their corrections.
3. Write the confirmed version to the agreed path, creating the directory if needed. If the file already exists, summarise what the new version changes or removes before overwriting it.
