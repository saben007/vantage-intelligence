# Data and Consent Policy

This policy governs what data may exist in this repository, how it is
classified, and the consent required before any sensitive data is used or
moved. The current phase ingests **no** private data of any kind.

---

## 1. Data classes

- **Public** — published, citable, freely shareable (e.g. a provider's public
  website, a company's public registration).
- **Pilot-scoped** — evidence accepted within a specific controlled pilot
  (e.g. `pilots/apius/`). Usable only inside that pilot's purpose.
- **Founder-private** — confidential company context, fundraising submissions,
  permissioned company material given to ScaleSignals in confidence.
- **Provider-private** — any non-public material about a provider.
- **Investor-facing (Vantage)** — intelligence intended for institutional
  users.

## 2. What may exist in this repository now

Only **public** and **conservative, derived** governance descriptions, plus the
explicitly supplied pilot facts recorded as **pilot-scoped** evidence.

This repository must **not** contain:

- founder-private material or fundraising submissions;
- provider-private material;
- credentials, tokens, or API keys;
- telemetry, analytics, or behavioural data;
- raw exports from any product system.

If sensitive data is needed for a future capability, that capability is queued
in `state/approval-queue.yaml`; the data is not added in the meantime.

## 3. The founder ↔ investor consent wall

Founder-private data must never become investor-facing (Vantage) intelligence
without **all** of the following, approved separately and in writing:

1. **Explicit, informed founder consent** for that specific use.
2. An approved **privacy architecture** (storage, access, retention, deletion).
3. An approved **governance architecture** (who may approve crossings, how
   they are logged and audited).

Until those exist, the wall is absolute. See `product-boundaries.md §2`.

## 4. Consent principles (for when consent is in scope later)

- **Purpose-bound:** consent covers a stated purpose only; reuse needs new
  consent.
- **Informed:** the founder understands what is shared, with whom, and why.
- **Revocable:** consent can be withdrawn, with a defined deletion path.
- **Logged:** each consent and revocation is a decision record.
- **Least-data:** only the minimum necessary data is ever used.

## 5. Provider data discipline

- Provider records use **public, citable** evidence by default.
- Evidence rules (`provider-intelligence/evidence-rules.yaml`) define what
  counts as acceptable evidence and how uncertainty is stated.
- No provider record may imply contact, endorsement, or approval.

## 6. Retention and deletion

- Governance records (decisions, assumptions, contradictions, failures,
  lessons) are retained as the long-term memory of the system.
- Any sensitive data introduced later must have a defined retention limit and
  deletion path **before** it is introduced.

## 7. Enforcement

- Introducing disallowed data is a governance failure
  (`learning/failures.ndjson`).
- Any proposed data movement across the consent wall halts at
  `state/approval-queue.yaml`.
