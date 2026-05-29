# Autonomy Policy

This policy classifies every action into one of four tiers. The default for
anything not explicitly listed as *auto-allowed* is **requires Ben approval**.
Nothing in the current LS0 phase grants autonomous execution.

> **Current phase (LS0):** No automation exists. AI may read this repository and
> draft records. AI may not act on the world. This policy describes the target
> discipline so that, when capabilities are added later, they slot into an
> already-agreed structure.

---

## Tier 1 — Actions AI MAY perform automatically (auto-allowed)

Only low-risk, fully-reversible, internal-to-this-repository actions:

- Reading any file in this repository.
- Drafting and appending well-formed records to the learning ledgers
  (`learning/decisions.ndjson`, `contradictions.ndjson`, `failures.ndjson`)
  **as proposals clearly marked `status: draft`**.
- Summarising existing repository state for Ben.
- Validating that records conform to the schemas in `schemas/`.

Even auto-allowed actions never touch product repos, external systems, or
private data.

## Tier 2 — Actions AI MAY DRAFT ONLY (draft, never send/apply)

AI may prepare these, but they have no effect until Ben approves:

- Approval packets (`handoffs/approval-packets/`).
- Next-step prompts for tools (`handoffs/next-prompts/`).
- Proposed changes to product mirrors (`products/*/`), provider evidence
  (`provider-intelligence/`), or pilot records (`pilots/apius/`).
- Proposed promotions of a provider candidate (proposal only — see promotion
  gates; promotion still requires approval).
- Proposed edits to `state/authorised-work.yaml` or `blocked-work.yaml`.

Drafts are inert artefacts. Producing a draft is never the same as acting.

## Tier 3 — Actions REQUIRING Ben's explicit approval

These are paused in `state/approval-queue.yaml` until Ben decides:

- Authorising any new category of work beyond LS0 scaffolding.
- Changing product boundaries or the data/consent policy.
- Promoting a provider candidate or changing its status.
- Any action that would touch a product repository.
- Any action that would contact, or prepare to contact, a provider or
  external party.
- Connecting any external system, API, model, or automation.
- Ingesting any founder-private or provider material.

## Tier 4 — PROHIBITED actions (not allowed at all in current phase)

- Autonomous execution or deployment of any kind.
- Contacting providers, founders, or any external party.
- Modifying production / product code or active product branches.
- Promoting founders or providers, or implying provider approval / fit beyond
  accepted evidence.
- Integrating ScaleSignals and Vantage, or mixing their data.
- Orchestrating models or APIs; storing or using credentials.
- Collecting telemetry or usage data.
- Developing app features through this governance repository.
- Creating scripts, installing dependencies, or wiring automations here.

## Escalation and logging

- Anything ambiguous is treated as **Tier 3** and queued, never assumed.
- Each approved action becomes a decision record in
  `learning/decisions.ndjson`.
- Any breach (or near-breach) of this policy is logged in
  `learning/failures.ndjson` as a governance failure.
