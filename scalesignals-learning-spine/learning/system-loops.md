# System Loops

The Learning Spine preserves two learning loops and watches two feedback
dynamics. Together they ask both *"are we doing the work well?"* and *"are we
doing the right work?"* — and guard the trust that makes the work worth doing.

---

## 1. Execution-improvement loop

> *Improves **how** tasks are carried out.*

```
sensors / data  →  policy  →  tools  →  quality gates  →  learning mechanism
        ↑                                                        |
        └────────────────────────────────────────────────────────┘
```

- **Sensors / data** — observations about how a task went (in LS0, recorded by
  humans; no telemetry is collected).
- **Policy** — the rules that govern the task (charter, autonomy policy,
  evidence rules).
- **Tools** — the means of carrying out the task (e.g. Claude Code, Codex,
  Figma — none connected in LS0).
- **Quality gates** — the checks a result must pass (founder-value tests,
  institutional-quality tests, promotion gates).
- **Learning mechanism** — distilling what worked into `learning/lessons.yaml`
  and feeding it back into policy.

This loop makes execution steadily better **within** the bounds set by the
governing loop. It cannot, by itself, change what the bounds *are*.

## 2. Governing-learning loop

> *Asks whether the system is doing the **right** work and measuring the
> **right** result.*

```
purpose  →  assumptions  →  system outcomes  →  contradictions  →  revised
   ↑                                                              policy /
   └──────────────────────── roadmap / product belief ───────────┘
```

- **Purpose** — the north star (founder-side and institutional-side).
- **Assumptions** — what we currently take to be true
  (`learning/assumptions.yaml`).
- **System outcomes** — what actually happened (pilot outcomes, decisions).
- **Contradictions** — where outcomes conflict with purpose or assumptions
  (`learning/contradictions.ndjson`).
- **Revised policy / roadmap / product belief** — the considered response,
  recorded as decisions.

This loop can change the bounds the execution loop operates within. It is the
mechanism by which the company avoids getting very efficient at the wrong
thing.

## 3. Positive founder-value feedback loop

> *The dynamic the company wants to strengthen.*

```
honest, evidence-grounded, useful output
   → founder trust
   → deeper / continued engagement and real context
   → better-grounded next output
   → more founder value  ↺
```

When ScaleSignals delivers credible, transparent, genuinely useful next actions
(no overclaiming, no premature contact), the founder trusts it, stays engaged,
and the system earns better grounding for the next round. This is the loop the
first-value definition is designed to start.

## 4. Trust-destruction risks (the loop running in reverse)

The same loop runs destructively if any of these occur. These are the failure
modes the charter is built to prevent:

- **Weak evidence / overclaiming** — asserting fit or confidence beyond the
  evidence breaks credibility on contact with reality.
- **Slow or low-value routes** — sending founders down visible-but-poor routes
  (e.g. assuming a public portal means a worthwhile route — assumption A-002)
  wastes their scarcest resource: time during a raise.
- **Private-data misuse** — letting founder-private material leak into
  investor-side (Vantage) intelligence destroys trust irreversibly and breaches
  the consent wall.

Each of these is logged, when observed, in `learning/failures.ndjson`
(and as a `contradiction` when it conflicts with stated purpose). Preventing
them is more important than any single efficiency gain from the
execution-improvement loop.

## How the loops connect

The execution loop optimises **within** the guardrails; the governing loop
revises **the guardrails themselves**; the founder-value loop is the outcome
both are ultimately serving; and the trust-destruction risks define the lines
that, if crossed, make all the other loops worthless. Ben's approval sits
between proposal and action throughout — see `charter/autonomy-policy.md`.
