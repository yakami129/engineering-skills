# Coverage checklist

The ten interview dimensions from [SKILL.md](SKILL.md). Each one says what it should clarify, followed by example questions. Pick 2–4 per dimension and adapt them to what the user has already said; they are prompts for finding gaps, not a script. Skip dimensions that don't apply, but check before finishing that every relevant one has been touched.

## 1. Goals and scope

Clarify why this is being done, and what is and isn't in scope.

- If this fully succeeds, what is the most visible change for the user or team?
- What is explicitly out of scope (e.g. no mobile, no multi-tenancy for now)?
- Which 2–3 pain points of the current approach matter most?
- If half the features had to be cut, which part would you keep, and why?

## 2. Users and scenarios

Focus on who uses it, and in what situations.

- What are the typical roles (end users, admins, operators, other services)?
- Walk through one or two end-to-end stories, from arriving to finishing the task.
- Which usages should deliberately _not_ be supported, and why?

## 3. Flow and information architecture

Focus on steps, state transitions, and how pages or modules relate.

- What is the high-level flow from trigger to completion (3–7 steps)?
- Which steps must be sequential, and which can run in parallel or asynchronously?
- Which step looks like one step but hides several?

## 4. Data model and interfaces

Clarify the key entities, their fields, and the interfaces to external systems.

- What are the 2–3 core entities, and what does each one's lifecycle look like?
- Which existing systems or third-party services does this integrate with? Who controls those interfaces?
- Which fields matter for analytics, auditing, or debugging even if nothing uses them yet?

## 5. Technical approach and architecture

Don't aim for a complete design; lock down the key decision points and constraints.

- Which layer should this live in (frontend, backend, separate service, script)?
- What technical direction is already preferred, and what is ruled out?
- Which parts look tricky enough to think through now?
- If this is later refactored or split out, where is the natural boundary?

## 6. UI/UX requirements

Not pixel-level design: interaction principles, information hierarchy, and what the experience should feel like.

- What matters most in the experience (fewest steps, information at a glance, configurability)?
- Which interaction patterns should be avoided (too many dialogs, repeated confirmations)?
- Are there hard or soft requirements for accessibility, responsive layout, or localisation?

## 7. States, errors, and edge cases

This is a high-value area; push for as many concrete examples as you can.

- What are the common failure modes? What will users or the system get wrong?
- When something fails, what is shown to the user, and what is logged or monitored?
- Are there grey states: partial success, waiting on an external callback, needing manual intervention?
- Which extreme cases are worrying (huge imports, very unstable networks)?

## 8. Non-functional requirements

Performance, security, scalability, maintainability, and similar qualities.

- What are the expected data volumes and request rates? Any peaks or batch jobs?
- How strict are the security and permission requirements? What level counts as safe enough?
- If more teams, tenants, or environments need support later, how should it scale out?

## 9. Risks, trade-offs, and non-goals

Help the user make the trade-offs explicit.

- Which trade-offs have already been made implicitly (e.g. simplicity for faster delivery)?
- If this goes wrong later, which one or two questions would you least like to be asked?
- What will this not do now, but might do later?

## 10. Acceptance criteria and examples

Finally, make clear when it counts as done.

- What must be true before you would call it ready to ship?
- Which representative scenarios, once passing, would give you confidence?
- Is automated acceptance testing needed, and roughly what should it cover?
