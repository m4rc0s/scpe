# SCPE — Spec-Compiled Product Engineering

> **The spec is the source. Code is the compiled output.**
> A lightweight, Markdown-only method for teams that build products with AI agents: define what the product is, change it only through reviewed changes, and let agents build each change.

**[Idea](#the-idea) • [Principles](#principles) • [Repository](#the-product-repository) • [The Loop](#the-loop) • [Get Started](#get-started) • [FAQ](#faq) • [Full Method](SCPE_METHOD.md) • [Templates](templates/)**

---

## The Idea

Agents write code fast. The bottleneck is now knowing, precisely and in writing, **what the product is** and **what should change next**.

SCPE gives that knowledge a standard shape:

| Part | Folder | Answers |
|---|---|---|
| **The product spec** | `spec/` | What is the product, right now? |
| **Changes** | `changes/` | What should become true next, and why? |
| **Apps** | `apps/` | What software implements it? |

Six document types describe the product — **actor, context, term, feature, rule, quality** — each one a small Markdown file with a stable ID. A **change** is the only way to modify them, and it is also the unit of work an agent builds.

---

## Principles

1. **A defined product over a queue of tickets.**
2. **Explicit changes over silent edits.**
3. **Examples over adjectives** — behaviour is pinned by *Given / When / Then* scenarios.
4. **Links over folders** — everything has a stable ID.
5. **Small vertical slices over big plans.**
6. **Humans decide, agents build, scripts check.**
7. **One repository per product.**

---

## The Product Repository

```text
myproduct/
├── AGENTS.md          # how people and agents work here
├── product.md         # problem, users, outcomes, non-goals
├── spec/              # actors, contexts, terms, features, rules, quality — current truth
├── decisions/         # technical decisions
├── changes/           # changes in flight; done/ holds history
└── apps/<app>/app.md  # app manifest (+ code, or a pointer to another repo)
```

A feature carries its own acceptance scenarios:

```markdown
---
id: FEAT-PIX-PAYMENT
type: feature
title: Pay with Pix
status: active
actors: [ACT-CUSTOMER]
rules: [RULE-PIX-CHARGE-EXPIRY]
---
## Outcome
A customer pays for an order instantly with Pix.
...
## Scenarios
### S2 — Expired charge
- **Given** a Pix charge created 31 minutes ago and not paid
- **When** the customer opens the order
- **Then** the charge is shown as expired
```

Tests name the scenario they cover — `FEAT-PIX-PAYMENT#S2` — which is the whole traceability link from spec to code.

---

## The Loop

```text
  PROPOSE  ─▶  APPROVE  ─▶  BUILD  ─▶  VERIFY  ─▶  LEARN
  (draft)      (ready)      (building)  (done)     (outcome check → new changes)
```

- **Propose** — anyone opens a change with the problem, intended outcome and proposed spec files, drafted with an agent.
- **Approve** — an accountable human sets `ready`.
- **Build** — an agent implements the change in vertical slices.
- **Verify** — scenario tests pass; a human merges code and updated spec together.
- **Learn** — after release, the change records whether it worked.

Many changes run at once. Because the spec only changes through this path, spec and code cannot drift apart silently.

---

## Get Started

1. Create one repository for your product and copy [`templates/AGENTS.md`](templates/AGENTS.md) and [`templates/product.md`](templates/product.md).
2. Open `changes/chg-initial/change.md` and, with your agent, write the actors, key terms and **one** feature — the most valuable one right now.
3. Approve, build, merge. Open the next change.

No installer, no CLI, no platform. Markdown, Git, and the agent you already use.

---

## FAQ

**How is this different from Spec Kit or OpenSpec?**
Those tools write a spec per increment and archive it. In SCPE each change writes back into a lasting product definition, so the next change — and the next agent — starts from the current truth.

**How is it different from Product Definition as Code?**
SCPE borrows its core ideas (canonical Markdown definition, stable IDs, explicit changes) with a smaller vocabulary, and it also covers delivery: slices, tasks, status and outcome checks live in the same change file.

**Does SCPE require Clean Architecture, DDD or a specific stack?**
No. It uses DDD's vocabulary — contexts, terms, rules — to describe the product. Code standards are recorded per product in `decisions/`.

**What if the code lives in several repositories?**
The spec stays in the product repository. `apps/<app>/app.md` records the external `repo` and the `revision` last built.

**What if a spec changes after the code is shipped?**
It can't change silently: any edit to `spec/` is a new change, which lists the affected apps and goes through the same loop.

---

## Repository Map

| File | Role |
|---|---|
| [`SCPE_METHOD.md`](SCPE_METHOD.md) | The complete method |
| [`templates/`](templates/) | Ready-to-copy templates for every document type |

## Contributing

Open an issue or pull request describing the problem and the change you propose — the same way SCPE asks you to change a product.
