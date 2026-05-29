# ScaleSignals Learning Spine

**Status:** LS0 — initial read-only scaffolding only.
**Mode:** Governance and memory. No execution. No automation. No data ingestion.

> This repository is an **operating-system / governance layer**. It is not a
> product, not an application, and not a feature of any product. It records
> decisions, assumptions, current state, and the rules under which future
> work may proceed. It does **not** run that work.

---

## Why this repository exists

ScaleSignals and Vantage are products that will evolve over many decisions,
across multiple tools (Claude Code, Codex, Figma, provider research) and over a
long period. Today that coordination lives almost entirely in Ben's head.

The Learning Spine exists to **externalise and preserve** that coordination so
that, over time, the company can:

- preserve the *why* behind each decision, not just the *what*;
- monitor whether implementation matches the decision that authorised it;
- audit whether decisions produced the returns they promised;
- detect drift between stated purpose and actual system behaviour;
- assemble conservative, evidence-backed approval packets for Ben;
- gradually reduce Ben's manual coordination burden **without** removing his
  authority.

It does this through two learning loops (see `learning/system-loops.md`):

1. **Execution-improvement loop** — sensors/data → policy → tools → quality
   gates → learning mechanism. *Improves how tasks are carried out.*
2. **Governing-learning loop** — purpose → assumptions → system outcomes →
   contradictions → revised policy, roadmap or product belief. *Asks whether
   the system is doing the right work and measuring the right result.*

## What this repository owns

- The **charter**: north star, product boundaries, autonomy policy, data and
  consent policy.
- The **declared state** of work: what is authorised, what is blocked, what is
  queued for approval.
- A **conservative mirror** of each product's current priority and build state
  (ScaleSignals and Vantage), kept separate.
- **Provider-intelligence governance**: evidence rules and promotion gates.
  (Governance only — not provider outreach, not a CRM, not approvals.)
- The **Apius pilot record**: purpose, accepted evidence, candidate providers,
  missing evidence, and outcomes.
- The **learning ledgers**: decisions, assumptions, contradictions, failures,
  lessons.
- **Schemas** that describe the conservative shape of future tool returns
  (Claude Code, Codex, Figma) and governance records — as templates only.
- **Inbox / handoff / eval** folders as placeholders for a future,
  separately-approved workflow.

## What this repository never owns

- **Execution.** It never runs builds, deployments, jobs, or agents.
- **Product code.** ScaleSignals and Vantage source code live in their own
  repositories and are never modified from here.
- **Private founder material or fundraising submissions.** No company-private
  data is ingested here.
- **Provider relationships.** No provider is contacted, ranked as "approved",
  or promoted from this repository.
- **Model / API orchestration.** No keys, no API calls, no model routing.
- **Telemetry.** No automatic collection of usage or behaviour.
- **Authority.** It records the rules; Ben remains the approver.

## How the four domains remain separate

This repository keeps four concerns in **separate, non-merging** spaces:

| Domain | Lives in | Boundary |
| --- | --- | --- |
| **ScaleSignals** (founder-facing) | `products/scalesignals/` | Founder-private context. Never flows to Vantage. |
| **Vantage** (institutional-facing) | `products/vantage/` | Investor-facing. Never receives founder-private material. |
| **Provider Intelligence** | `provider-intelligence/` | Evidence + gates only. Never implies approval or outreach. |
| **Apius pilot** | `pilots/apius/` | A single controlled pilot. Its evidence is pilot-scoped, not a product dataset. |

The strict prohibition on mixing ScaleSignals (founder-private) and Vantage
(institutional) data is defined in `charter/product-boundaries.md` and
`charter/data-and-consent-policy.md`. Crossing that boundary requires a
**separately approved** consent, privacy and governance architecture that does
not yet exist.

## How future automation must remain approval-gated

Nothing in this repository executes. When automation is eventually proposed it
must follow `charter/autonomy-policy.md`, which classifies every action as one
of: *auto-allowed*, *draft-only*, *requires-Ben-approval*, or *prohibited*.

Until that policy is expanded and explicitly approved:

- AI may **read** this repository and **draft** records.
- AI may **not** act on the world, contact anyone, deploy anything, or change
  any product.
- Every state-changing or outward-facing action routes through
  `state/approval-queue.yaml` and a human approval step.

## Repository map

```
scalesignals-learning-spine/
  charter/                 # north star, boundaries, autonomy + data policy
  state/                   # current state, authorised / blocked / queued work
  products/
    scalesignals/          # founder-facing product mirror (conservative)
    vantage/               # institutional-facing product mirror (conservative)
  provider-intelligence/   # evidence rules + promotion gates (governance only)
  pilots/apius/            # the controlled Apius pilot record
  learning/                # decisions, assumptions, contradictions, failures, lessons, loops
  inbox/                   # placeholders for future tool returns (not ingested)
  handoffs/                # placeholders for next-prompts / approval-packets / archive
  evals/                   # placeholders for future evaluation suites
  schemas/                 # conservative templates for future returns + records
```

## Reading order for a new contributor

1. `charter/north-star.md`
2. `charter/product-boundaries.md`
3. `charter/autonomy-policy.md`
4. `charter/data-and-consent-policy.md`
5. `state/current-state.yaml`
6. `learning/system-loops.md`
7. `learning/assumptions.yaml`

---

*All content here is markdown, YAML or NDJSON. There are no scripts,
no dependencies, no API connections and no automations in this repository.*
