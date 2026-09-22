# SCPE — Spec-Compiled Product Engineering

> Define the product in plain Markdown. Change it only through reviewed changes. Let agents compile each change into working software, and check the result against the examples written in the spec.

The key words **MUST**, **MUST NOT**, **SHOULD** and **MAY** are used as in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

---

## 1. The Idea

AI agents made implementation cheap. What is still expensive — and now the real bottleneck — is knowing, precisely and in writing, **what the product is** and **what should change next**. An agent amplifies whatever understanding it is given, including none.

SCPE is a small standard for writing that understanding down and a simple loop for evolving it. The spec is the source; code is what you get when an agent *compiles* a change to the spec.

It has three parts:

| Part | Folder | Answers |
|---|---|---|
| **The product spec** | `spec/` | What is the product, right now? |
| **Changes** | `changes/` | What should become true next, and why? |
| **Apps** | `apps/` | What software implements it? |

Everything is Markdown with a small YAML header, versioned in Git. No platform, no proprietary tool.

---

## 2. Principles

1. **A defined product over a queue of tickets.** `spec/` describes what the product *is*. Backlogs, boards and task lists are views of changes — never the source of truth.
2. **Explicit changes over silent edits.** The spec changes through exactly one mechanism: a Change, approved by a human. Everything else is a proposal.
3. **Examples over adjectives.** Behaviour is pinned down by concrete *Given / When / Then* scenarios. If you cannot write the example, the decision has not been made yet.
4. **Links over folders.** Every artifact has a stable ID. Relationships are written as IDs, so people, agents and scripts can all follow them.
5. **Small vertical slices over big plans.** Specify the most valuable next outcome, ship it end to end, learn from real use, repeat. Do not map the whole system upfront.
6. **Humans decide, agents build, scripts check.** Anyone can author. An accountable human approves. Agents implement. Deterministic checks verify structure. No agent approves its own work or settles an open product question.
7. **One repository per product.** You clone the product, not a service. Spec, decisions, changes and app manifests live together, so the agent's context *is* the product's context.

---

## 3. The Product Repository

```text
myproduct/
├── AGENTS.md            # how people and agents work here: read order, rules, commands
├── product.md           # why the product exists: problem, users, outcomes, non-goals
├── spec/                # the product definition — current truth, one artifact per file
│   ├── actors/
│   ├── contexts/
│   ├── terms/
│   ├── features/
│   ├── rules/
│   └── quality/
├── decisions/           # technical decisions (architecture, stack, patterns)
├── changes/             # proposed and in-flight changes
│   └── done/            # accepted changes — the product's history
└── apps/                # the software
    └── api-core/
        ├── app.md       # app manifest
        └── src/
```

**Who may edit what:**

| Path | Holds | Edited by |
|---|---|---|
| `product.md`, `spec/**` | The accepted product definition | Only by merging a done Change |
| `decisions/**` | Technical decisions | New decision per PR; supersede, never rewrite |
| `changes/*` | Work in flight | Authors and builders, freely, until done |
| `changes/done/**` | History | Nobody — immutable |
| `apps/**` | Code and tests | Builders, as part of a Change |
| `AGENTS.md` | Working agreement | The team, by PR |

Subfolders inside `spec/` are a convenience. An artifact's kind comes from its `type` field, not its path.

---

## 4. The Product Spec

### 4.1 Common Rules

Every artifact in `spec/` is one Markdown file with this header:

```yaml
---
id: FEAT-PIX-PAYMENT        # stable ID
type: feature               # actor | context | term | feature | rule | quality
title: Pay with Pix
status: active              # draft | active | deprecated | retired
---
```

- **IDs** are `PREFIX-NAME` in uppercase (`A–Z`, `0–9`, `-`). An ID never changes and is never reused, even after the artifact is retired. The file name is the lowercase ID: `feat-pix-payment.md`.
- **Outside `spec/`**, the same header is used by changes (`CHG-`), decisions (`DEC-`) and app manifests (`APP-`).
- **References** between artifacts always use IDs — never paths or titles. A scenario inside a feature is referenced as `FEAT-PIX-PAYMENT#S2`.
- **Required sections** appear as `##` headings, in the order listed below. Extra sections MAY follow.
- **No owner, date or version fields.** Git already records who changed what and when.
- **Product language only.** No class names, tables, endpoints or frameworks, unless they are part of the external contract. Implementation belongs in `decisions/` and `apps/`.
- **Status:** `draft` (not yet accepted), `active` (part of the product), `deprecated` (scheduled for removal), `retired` (kept for traceability only). An `active` artifact MUST NOT reference a `retired` one.

### 4.2 Artifact Types

| Type | Prefix | Answers | Links (frontmatter) | Required sections |
|---|---|---|---|---|
| **actor** | `ACT-` | Who interacts with the product? | `kind`: human, system, scheduled | Goals · Responsibilities · Boundaries |
| **context** | `CTX-` | Where does a set of words hold one meaning? | — | Responsibility · Boundaries · Integrations |
| **term** | `TERM-` | What does this word mean here? | `context`, `synonyms` | Definition · Not to Be Confused With · Example |
| **feature** | `FEAT-` | What outcome does an actor get, and how does it behave? | `actors`, `context`, `rules`, `terms` | Outcome · Flow · Alternatives and Failures · Scenarios · Out of Scope |
| **rule** | `RULE-` | What must always (or never) be true? | `applies-to`, `terms` | Rule · Why · Examples · Exceptions |
| **quality** | `QUAL-` | How well must it work, measurably? | `applies-to`, `attribute` | Requirement · Measurement |

This is the whole vocabulary. It is enough for most products; if your domain needs more (for example domain events or regulatory obligations), add a type with the same common rules and document it in `AGENTS.md`.

**Why these six:** actors, contexts and terms are the *ubiquitous language* of Domain-Driven Design; rules are its *invariants*; features carry behaviour and the examples that verify it; quality holds measurable non-functional requirements. Ready-to-copy templates are in [`templates/`](templates/).

### 4.3 Features and Scenarios

The feature is the centre of the spec. Its scenarios are the acceptance criteria that agents implement and tests check.

```markdown
---
id: FEAT-PIX-PAYMENT
type: feature
title: Pay with Pix
status: active
actors: [ACT-CUSTOMER]
context: CTX-PAYMENTS
rules: [RULE-PIX-CHARGE-EXPIRY]
terms: [TERM-ORDER, TERM-PIX-CHARGE]
---

## Outcome
A customer pays for an order instantly with Pix, without typing card details.

## Flow
1. The customer chooses Pix at checkout.
2. The product creates a Pix charge for the order total and shows its QR code.
3. The customer pays from their bank app.
4. The product confirms the payment and marks the order as paid.

## Alternatives and Failures
- The charge expires before payment → the order stays unpaid and the customer can create a new charge.
- The bank confirms a different amount → the payment is held for manual review.

## Scenarios

### S1 — Paid order
- **Given** an order of R$ 120,00 awaiting payment
- **When** the customer pays the Pix charge for R$ 120,00
- **Then** the order is marked as paid
- **And** the customer sees the payment confirmation

### S2 — Expired charge
- **Given** a Pix charge created 31 minutes ago and not paid
- **When** the customer opens the order
- **Then** the charge is shown as expired
- **And** the customer can create a new charge

## Out of Scope
Refunds via Pix — a future change.
```

Scenario rules:

- Each scenario has a local ID (`S1`, `S2`, …) that never changes. Retired scenarios keep their number; new ones get the next one.
- One `When` per scenario. Alternatives become separate scenarios, not an `or`.
- `Then` states what a user or another system can **observe** — not internal state.
- Every scenario of an `active` feature MUST be covered by at least one test that names its ID.

---

## 5. Changes

A **Change** is the only way the product definition evolves, and the unit of work that agents build. It replaces the feature/epic/plan/tasks/status split with **one folder and one file**.

```text
changes/chg-pix-payment/
├── change.md                         # intent, scope, slices, log
└── spec/                             # complete future version of every added/modified artifact
    ├── features/feat-pix-payment.md
    ├── rules/rule-pix-charge-expiry.md
    └── terms/term-pix-charge.md
```

### 5.1 `change.md`

```markdown
---
id: CHG-PIX-PAYMENT
type: change
title: Accept Pix at checkout
status: building          # draft | ready | building | blocked | done | dropped
add: [FEAT-PIX-PAYMENT, RULE-PIX-CHARGE-EXPIRY, TERM-PIX-CHARGE]
modify: [FEAT-CHECKOUT]
remove: []
apps: [api-core, web-checkout]
---

## Problem
38% of abandoned checkouts happen on the card form. Customers ask for Pix.

## Intended Outcome
Customers can pay with Pix. We expect checkout abandonment to fall below 25%.

## Slices

### Slice 1 — Pay an order with Pix (FEAT-PIX-PAYMENT#S1)
- [x] Create Pix charge for an order
- [x] Show QR code at checkout
- [ ] Confirm payment from bank webhook and mark order paid

### Slice 2 — Expired charges (FEAT-PIX-PAYMENT#S2, RULE-PIX-CHARGE-EXPIRY)
- [ ] Expire unpaid charges after 30 minutes
- [ ] Let the customer create a new charge

## Open Questions
- Should we hold amounts that differ by less than R$ 0,01? (Finance)

## Out of Scope
Pix refunds.

## Log
- 2026-09-20 — Slice 1 in review. Bank sandbox rejects amounts with 3 decimals; confirmed with provider, no spec impact.

## Outcome Check
_Filled after release: did abandonment fall? What did we learn? Which new changes does it suggest?_
```

**Slices** are vertical by default: each one cuts across data, logic, interface and API to deliver something a user can observe, and names the scenarios it makes pass. Tasks are plain checklists under each slice; the builder (agent or human) writes them when work starts. If a slice cannot be vertical — an infrastructure migration, for example — say so and why in the slice.

**Size:** if a change cannot be done in about a week, split it. Small changes ship, get used, and teach you something sooner.

### 5.2 Lifecycle

```text
 draft ──approve──▶ ready ──start──▶ building ──merge──▶ done
   │                  ▲                  │
   ▼                  └──── blocked ◀────┘
 dropped
```

| Status | Meaning | Set by |
|---|---|---|
| `draft` | Being written and discussed | Author |
| `ready` | Approved: this is what we want, and it can be built | Accountable human (the approver) |
| `building` | An agent or person is implementing it | Builder |
| `blocked` | Stopped by an external dependency, a defect, or a spec question found while building | Builder |
| `done` | Merged: code, tests and updated spec are on the main branch | Human reviewer, by merging |
| `dropped` | Abandoned; kept for the record | Author or approver |

### 5.3 Rules

1. A change lists every artifact it adds, modifies or removes, and carries the **complete future version** of each one under its own `spec/` folder.
2. To become `ready`, a change MUST have: every added or modified feature with scenarios, no open question that blocks building, and the affected `apps` listed.
3. If building shows the spec is wrong, the builder MUST NOT quietly adapt. It records the finding in the Log, sets `blocked`, and the approver re-approves the corrected proposal.
4. A change is `done` when one pull request merges: the code, tests naming each covered scenario, the proposed files moved into `spec/`, and the change folder moved to `changes/done/`.
5. A `done` change is history and MUST NOT be edited. Corrections are new changes.
6. Two changes that are not done MUST NOT modify or remove the same artifact. The second one waits, or is rebased after the first is done.

Because `spec/` can only change through this path, spec and code cannot silently drift apart. Any divergence is a visible, open change.

---

## 6. The Loop

```text
  PROPOSE  ─▶  APPROVE  ─▶  BUILD  ─▶  VERIFY  ─▶  LEARN
  (draft)      (ready)      (building)  (done)     (outcome check → new changes)
     ▲                                                  │
     └──────────────────────────────────────────────────┘
```

1. **Propose.** Someone — product manager, designer, engineer, domain expert — opens a change with the problem and intended outcome. An agent helps draft features, rules and scenarios; the author refines them.
2. **Approve.** An accountable human checks that the change says what the product should do and fits the technical decisions, then sets `ready`. This is a check per change, not a phase for the whole product.
3. **Build.** An agent reads the change, the artifacts it cites, the app manifests and the decisions; writes the tasks; implements slice by slice.
4. **Verify.** Tests named after scenarios pass; a human reviews and merges; the spec is updated in the same merge.
5. **Learn.** After release, the Outcome Check records whether the change worked. Lessons become new changes.

Many changes move through the loop at the same time. There is no product-wide gate.

**Four questions, four kinds of evidence.** A green build does not mean a change is right.

| Question | Answered by | Evidence |
|---|---|---|
| Is it well formed? | Checks (Section 9) | CI result |
| Is it what we want? | Approver | `ready` status and review |
| Is it built as specified? | Builder and reviewer | Passing tests that name scenario IDs |
| Did it work? | The team | Outcome Check in the done change |

---

## 7. Apps

Each app in `apps/` has an `app.md` manifest so an agent knows immediately what it is, what it owns, and how to run it.

```markdown
---
id: APP-API-CORE
type: app
title: api-core
kind: backend-api
stack: [Kotlin, Spring Boot, PostgreSQL]
contexts: [CTX-PAYMENTS, CTX-ORDERS]
repo: https://github.com/acme/api-core   # only if the code lives in another repository
revision: 3f2a91c                         # commit the product last built against
---

## Responsibility
Order lifecycle and payment processing.

## Boundaries
Does not render UI. Does not store card data.

## Interfaces
REST API for web and mobile clients; publishes `OrderPaid` events.

## Run and Test
`./gradlew test` — tests are named after scenario IDs.
```

When the code lives in another repository, `apps/<app>/` holds only `app.md`; the spec and changes still live in the product repository. `revision` MUST be a commit, not a branch.

Code standards (Clean Architecture, hexagonal, SOLID, and so on) are **product choices, not method rules**. Record them in `decisions/`.

**Decisions** (`decisions/DEC-0001-*.md`) are short architecture decision records with `id`, `type: decision`, `title`, `status` (`proposed | accepted | superseded`), optional `supersedes`, and the sections Context · Decision · Consequences.

---

## 8. Working with Agents

- **`AGENTS.md`** at the root is the entry point for every agent session: what to read first, the rules below, and the commands to build and test.
- **Minimum context for a task** is the change file, the artifacts its IDs point to, the relevant `app.md` files and the accepted decisions. IDs make that context easy to collect — and keep it small.
- **Tests name scenario IDs**, for example `test("FEAT-PIX-PAYMENT#S2 expired charge can be recreated")`. This is the traceability link from spec to code.
- **Agents may draft anything and approve nothing.** They do not set `ready`, merge, or close open questions.
- **Specialist review passes are optional.** A change can be reviewed by agents playing focused roles — security, testing, UX, operations — before a human approves or merges it.

---

## 9. Checks

These checks are deterministic: the same files always give the same answer. A script or CI job can run them; SCPE does not require a specific tool.

1. Every artifact has a valid `id`, `type`, `title` and `status`, and its ID prefix matches its type.
2. IDs are unique across the repository.
3. Every referenced ID exists, and no `active` artifact references a `retired` one.
4. Every artifact has its required sections, in order.
5. Every `add` or `modify` in a change has a matching file under the change's `spec/` folder, and every file there is listed.
6. No two changes that are not done modify or remove the same artifact.
7. Every scenario of an `active` feature is named by at least one test.
8. Files under `spec/` change only in commits that also move a change to `changes/done/`.

Checks prove that the spec is **well formed**, not that it is **right**. Only people and real usage answer that.

---

## 10. Getting Started

1. Create one repository for the product. Add `AGENTS.md` and `product.md` from [`templates/`](templates/).
2. Open the first change, `CHG-INITIAL`. Ask an agent to help you write the actors, the key terms and **one** feature — the most valuable one for the business right now.
3. For an existing product, use `CHG-INITIAL` to recover the spec from code, tests and team knowledge. Recover only what the next changes need, not the whole system.
4. Approve it, build it, merge it. Then open the next change.

---

## 11. How SCPE Relates to Other Work

| Approach | What SCPE takes | Where SCPE differs |
|---|---|---|
| [Product Definition as Code](https://github.com/product-definition-as-code/spec) | A canonical product definition in Markdown; stable IDs; typed links; explicit Product Changes; checks that prove structure, not truth | A smaller vocabulary (six types); the change is also the unit of delivery, with slices and tasks; no citation digests — tests reference scenario IDs directly |
| SDD toolkits ([Spec Kit](https://github.com/github/spec-kit), OpenSpec) | Spec → plan → tasks → implementation per increment | The increment writes back into a lasting product definition instead of being archived as a one-off spec |
| [specdriven.com](https://specdriven.com/) | Intent → spec → implementation → evidence; rules plus Given/When/Then examples per slice | Adds a fixed file layout and lifecycle, so agents can work without asking where things live |
| [AI-Native Large-Scale Agile Manifesto](https://arxiv.org/html/2605.07717v2) | Shared living context over meetings; human in control, not in the loop; verification first; specialist agent roles | Applies these ideas at the level of one product repository, not a whole organisation |

---

## Appendix: Coming from Earlier SCPE Drafts

| Before | Now |
|---|---|
| SNPA, ADP, SSOT, FDE, Tandem, Universal Developer | Plain words: product repository, the loop, the spec, approver, author |
| `index.md`, `team_playbook.md`, `techinal_deal.md` | `AGENTS.md` + `decisions/` |
| `product_vision.md`, `roadmap.md` | `product.md` (roadmap is an optional *Now / Next / Later* section listing change IDs) |
| `glossary.md` | One `term` per file in `spec/terms/`, grouped by `context` |
| `architecture.md` | `decisions/` + `app.md` manifests |
| `features/<f>/index.md`, `feat_roadmap.md`, `epics/<e>/index.md`, `plan.md`, `tasks.md`, `epic_roadmap.md` | `spec/features/feat-*.md` (what the product does) + `changes/chg-*/change.md` (what changes next) |
| `quick_status.md` at three levels | `status` in each change's frontmatter; the overview is `grep -H '^status:' changes/*/change.md` |
| Upstream → Readiness Gate → Downstream → Audit | Propose → Approve → Build → Verify → Learn |
| `Stale` state | Not needed: the spec changes only through changes, so drift cannot be silent |
| `app_liquid.md` / `app_manifest.md` + `repo_pointer.md` | One `app.md` with optional `repo` and `revision` |
| Mandatory Clean Architecture / hexagonal / SOLID | A product decision in `decisions/` |
