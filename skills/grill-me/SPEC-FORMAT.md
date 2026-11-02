# Spec format

Default location: `docs/exec-plans/YYYY-MM-DD-<slug>.md` (see the Spec section of [SKILL.md](SKILL.md)). Adapt the structure to the subject: drop sections that don't apply and add ones it needs. Write each section only to the depth implementation needs; use glossary terms as defined and link ADRs rather than repeating their reasoning.

```markdown
# [Feature name] SPEC

## 1. Background and goals
- Context
- Product or business goals

## 2. Scope
### 2.1 In scope
### 2.2 Out of scope

## 3. Users and scenarios
- Typical roles
- Key scenarios (user stories)

## 4. Flow and structure
- High-level flow
- Important states and transitions
- Main pages or modules and how they relate

## 5. Data and interfaces
- Core entities and fields
- External dependencies and integration interfaces

## 6. Technical approach
- Architecture and boundaries
- Key technical decisions and their reasons (link ADRs where they exist)
- Constraints and assumptions

## 7. UI/UX
- Key screens and interactions
- Information hierarchy and feedback
- Accessibility, responsive, or localisation constraints (if applicable)

## 8. States, errors, and edge cases
- Common errors and how they are handled
- Grey states (partial success, pending, manual intervention)
- Expected behaviour under extreme load or input

## 9. Non-functional requirements
- Performance and capacity
- Security and permissions
- Scalability and operability

## 10. Risks, trade-offs, and open questions
- Known risks and mitigations
- Trade-offs made and why
- Open questions (clearly marked)

## 11. Acceptance
- Acceptance checklist
- Representative scenarios
```
