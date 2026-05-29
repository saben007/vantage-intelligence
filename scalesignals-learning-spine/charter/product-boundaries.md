# Product Boundaries

This document defines hard boundaries between products and domains. These are
not guidelines — they are constraints. Crossing any of them requires a
separate, explicit, written approval from Ben **and** an approved governance
architecture (see `data-and-consent-policy.md`).

---

## 1. ScaleSignals and Vantage are separate products

| | ScaleSignals | Vantage |
| --- | --- | --- |
| Audience | Founders raising capital | GPs, LPs, DFIs, family offices, allocators |
| Data sensitivity | Founder-private, confidential | Investor-facing, permissioned |
| Direction of trust | Founder → product | Product → institution |
| Repository | Its own product repo | Its own product repo |
| Mirror here | `products/scalesignals/` | `products/vantage/` |

They may share engineering practices and a quality philosophy. They must **not**
share private data or be merged into one product without separate approval.

## 2. The prohibition on casual data mixing (explicit)

The following are **prohibited** unless a separate consent, privacy and
governance architecture has been explicitly approved:

- Using **founder-private** ScaleSignals information (company context,
  fundraising submissions, permissioned company material, pilot evidence) as
  **Vantage / investor-side** intelligence.
- Aggregating founder-private material across companies into investor-facing
  datasets, benchmarks, signals, or "market intelligence".
- Inferring or deriving investor-side conclusions from founder-private inputs
  and presenting them on the Vantage side.
- Reusing Apius pilot evidence (`pilots/apius/`) as a general product dataset
  or as Vantage intelligence.
- Any "temporary" or "convenience" copy of founder-private data into a
  Vantage-side location.

There is no informal, undocumented, or "just this once" exception. If a use
case appears to need crossing this boundary, it is logged in
`state/approval-queue.yaml` and stops until Ben decides.

## 3. Provider Intelligence is governance, not relationship

`provider-intelligence/` holds **evidence rules and promotion gates** only.
It must never:

- imply that a provider is approved, endorsed, or recommended;
- represent provider contact, outreach, or introductions;
- function as a CRM or pipeline;
- promote a provider beyond what its accepted evidence supports.

Provider naming in the pilot is **candidate analysis under evidence rules**, not
endorsement.

## 4. The Apius pilot is scoped

`pilots/apius/` is a single controlled pilot. Its purpose, accepted evidence,
candidates, gaps and outcomes are **pilot-scoped**. Pilot evidence is not a
product dataset and does not flow to Vantage.

## 5. This repository never modifies products

The Learning Spine never edits, deploys, or configures ScaleSignals or Vantage
product code. The product mirrors here (`products/*/`) are **conservative,
read-oriented descriptions**, not the source of truth for the running products.

## 6. Boundary changes are first-class decisions

Any change to these boundaries must be recorded as a decision in
`learning/decisions.ndjson`, with reasoning, and must pass through Ben's
approval. Silent boundary erosion is itself a failure to be logged in
`learning/failures.ndjson`.
