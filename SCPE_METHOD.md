# Spec-Compiled Product Engineering (SCPE)

> **A product engineering method in which living Markdown documentation is the contract and AI agents compile it into software — grounded in incremental feature discovery, business intent modeled by everyone on the team, and traceability between specification and code.**

---

## 📋 Executive Summary & Manifesto

AI agents now write code with a quality that often matches experienced developers. The bottleneck has moved: it is no longer writing syntax, but **specifying business intent precisely enough for an agent to build it**.

In SCPE, living documentation — written in **Markdown and natural language** — is the contract and the single source of truth for business intent. Machine execution state, task graphs, and manifests are maintained in **strongly typed TOML** (ADR-001). Code is their consequence.

The method stands on six pillars:

* **Everyone is a Developer:** Product managers, designers, engineers, and domain experts all model intent. Nobody just "hands off requirements".
* **Incremental Feature Discovery:** Build the macro vision of the most critical feature for the business *now*, deliver it, learn, and iterate. Never map the entire system upfront.
* **Product Workspace & Lean Manifests:** One isolated workspace per product, with a typed manifest (`app.toml`) for each application in `apps/`.
* **Flat Sequential Topology:** Features are atomic, sequentially numbered packages (`features/00X-<slug>/`), eliminating nested epic folders and duplicated roadmaps.
* **JIT Context Compilation:** Downstream agents do not parse dozens of markdown files; the engine compiles exact slice context (`scpe pack`) containing only relevant rules, scenarios, terms, and boundaries (< 1k tokens).
* **Wave Pipeline & DDD Rigor:** Agents execute the specification in an asynchronous flow — Upstream → Readiness Gate → Downstream → Audit — grounded in ubiquitous language, invariants, and test traceability.

### Why Markdown and Natural Language?

* **Anyone can read and write it:** Technical and business people collaborate on the same files; agents read them without conversion.
* **Git handles it:** Clean diffs show how intent and architecture evolve.
* **No tool lock-in:** The specification lives in the product repository, not in a proprietary platform.

---

## 0. Where SCPE Fits

SCPE belongs to the **Spec-Driven Development** movement and borrows from its neighbors:

| Reference | What SCPE Takes | Where SCPE Differs |
|---|---|---|
| [GitHub Spec-Kit](https://github.com/github/spec-kit), OpenSpec | Spec → Plan → Tasks → Implementation | The unit is the whole **product**, not an isolated code repository or a single change |
| [Product Definition as Code](https://github.com/product-definition-as-code/spec) | The product definition lives as Markdown in Git; references by name; tools check structure, humans decide truth | Lighter: plain Markdown files in a fixed workspace, no schemas required |
| [specdriven.com](https://specdriven.com/) | Intent → Specification → Implementation → Evidence; business rules plus *Given/When/Then* examples | Adds a workspace layout and an epic state machine an agent can follow |
| [AI-Native Agile Manifesto](https://arxiv.org/html/2605.07717v2) | Shared living context over meetings; humans in control, agents executing; verification first | Applied to one product team, not a whole organization |

### Core Practices

* **One Workspace per Product:** The agent's scope is restricted to the active product folder, which protects it from unrelated context.
* **Clone the Product, Not the Service:** You clone the entire product. Documentation guides the agents; code is the subordinate asset that is validated, run, tested, and deployed.
* **Product → Apps:** The product owns everything: `Product → Apps → {Backend, Client, …}`.
* **Agreed Engineering Standards:** Generated code follows the standards agreed in `architecture.md` and `app.toml` — for example SOLID, Clean Architecture, Hexagonal (Ports and Adapters), and established design patterns.
* **Application Manifest (`app.toml`):** A strongly typed TOML descriptor (ADR-001) that specifies the responsibility, execution commands (`run`, `test`, `lint`), dependencies, and negative boundaries of each application in `apps/`.
* **JIT Context Compilation (`scpe pack`):** Downstream agents receive focused, compiled context per vertical slice without loading the entire documentation corpus.

---

## 1. Everyone is a Developer — DDD Without the Ritual

Eric Evans' central idea in Domain-Driven Design was not about mapping tables, but that **the heart of software is solving problems in the user's domain**. With implementation delegated to agents, a team can focus on exactly that.

That is why, in SCPE, **"Developer" has a universal meaning**. Everyone who shapes the product — Product Managers, Designers, Engineering Managers, Staff Engineers, domain experts — is a Developer. Each contributes their own expertise, and together they guide agents in writing feature plans (`plan.md`), anchored to the team's technical agreements and system boundaries.

**Humans decide, agents execute.** Developers define intent, review, and approve. Agents draft documents, break plans into tasks, and write code. No agent approves its own work or settles an open business question on its own.

When modeling, Developers focus on five things:

* **Ubiquitous Language:** A shared glossary (`glossary.md`). If the business says a "Contract" differs from a "Proposal", the team and the agent use exactly those terms.
* **Bounded Contexts:** Clear boundaries for where each business rule starts and ends, so the agent stays focused on one part of the domain.
* **Entities and Business Rules (Invariants):** Entities have identity and a lifecycle governed by invariants — rules that must never be broken.
* **Domain Events:** Reactions and important state changes (*"When an Order is paid, notify Shipping"*).
* **Examples:** Every rule and behavior is illustrated with a concrete *Given / When / Then* scenario. If you cannot write the example, the decision has not been made yet.

---

## 2. Architecture: The Product Workspace

Keep your portfolio organized in one place (e.g., `$HOME/product_design/`), with one rule: **one dedicated workspace per product**.

### Product Root:

```text
myproduct/
├── agents.toml              # Agent roster, stages, write ownership, and boundaries (BMad-inspired)
├── roadmap.md               # Strategic direction and product milestones (synced via scpe roadmap --sync)
├── glossary.md              # Ubiquitous language (domain terms, queried via scpe term <word>)
├── architecture.md          # C4 model, tech agreements, constraints, and systemic boundaries
├── product_vision.md        # (Optional) Macro vision, business goals, and core problem
├── assets/                  # (Optional) Reference documents, wireframes, and visual assets
├── apps/                    # Generated applications (consequence of spec, each with app.toml)
│   └── api-core/
│       ├── app.toml         # Application manifest and boundaries
│       └── src/ ...
└── features/                # Flat sequential capability folders (each folder is an epic)
    ├── 001-user-auth/
    │   ├── plan.md          # Living specification: intent, rules (R#), examples (S#), slices
    │   └── tasks.toml       # Machine execution: state, slices, task graph, and log
    └── 002-pix-payment/
        ├── plan.md
        └── tasks.toml
```

---

## 3. Applications (`apps/`) and the Manifest (`app.toml`)

The `apps/` folder holds the software generated from the specification. Each application has a strongly typed TOML manifest: **`app.toml`** (ADR-001).

```text
apps/
├── api-core/
│   ├── app.toml             # Application manifest and boundaries
│   └── src/ ...             # Source code generated by the agent
└── desktop-client/
    ├── app.toml             # Application manifest and boundaries
    └── src/ ...             # Source code generated by the agent
```

### Standard `app.toml`:

A strongly typed manifest that works for any kind of application — backend, web, mobile, worker, library, data pipeline.

```toml
[app]
name = "api-core"
type = "backend-api"
description = "Core service for transaction processing and the financial ledger."
stack = "Kotlin, Spring Boot, PostgreSQL"
standards = "Clean Architecture, SOLID, Hexagonal"
entrypoint = "src/main/kotlin/com/myproduct/Main.kt"
depends_on = ["database", "payment-gateway"]

[commands]
run = "./gradlew bootRun"
test = "./gradlew test"
lint = "./gradlew check"

[boundaries]
forbidden = [
  "Does not render UI / HTML",
  "Does not store card data in plaintext"
]
```

*(Note: The CLI engine remains backwards-compatible with legacy `app.md` files if present).*

---

## 4. Protocol: The Wave Pipeline

### 4.1. Incremental Feature Discovery

SCPE rejects mapping an entire system upfront. The team builds the **macro vision of the most critical feature for the business right now**:

* **Learn as you build:** Validate hypotheses quickly, iterate on real deliveries, fail early, adjust course.
* **AI as co-pilot:** Developers use agents to draft and structure the intent of the priority feature into living Markdown (`plan.md`).

### 4.2. Flat Feature Topology & Sequential Numbering

Work is organized flatly directly under `features/`. Each folder represents a deliverable capability and is prefixed with a 3-digit sequential number (`001`, `002`, `003`...):

```text
features/
├── 001-user-auth/
│   ├── plan.md              # Living specification: rules, examples, slices
│   └── tasks.toml           # Slices, tasks, execution state, and temporal log
└── 002-pix-payment/
    ├── plan.md
    └── tasks.toml
```

This flat topology replaces the legacy nested `features/<feature>/epics/<epic>/` structure, eliminating intermediate folders, redundant `quick_status.md` files, and local roadmaps.

#### 4.2.1. Git Branch-per-Feature Lifecycle
Every feature can be developed in its own isolated Git branch:
```bash
python3 scripts/scpe.py feature "Pix Payment" --branch
```
This automatically detects the next prefix (e.g. `002`), scaffolds `features/002-pix-payment/`, and checks out the branch `feat/002-pix-payment`.

#### 4.2.2. Vertical Slicing (Recommended)

How a feature is sliced decides when users see value — and when the team starts learning.

* **Horizontal slicing** builds one layer at a time (all data, then all API, then all UI). Nothing is usable until every layer is done.
* **Vertical slicing** (the default) makes each feature slice cut across every layer needed to deliver a small but real increment to the user. Each slice is a chance to validate, learn, and pivot.

This is a recommendation, not a rule. When a feature cannot be sliced vertically — an infrastructure migration, for instance — the Tech Lead may accept another approach at the Readiness Gate. The choice and its reason are written in `plan.md`.

### 4.3. The Wave Pipeline & JIT Context Compilation

Work flows through four waves with JIT compilation replacing raw document loading:

| Wave | Who | What Happens | Artifacts |
|---|---|---|---|
| **1. Upstream** | Developers (any role) with an agent | Align on current priority, scope the feature, and model the plan: terms, rules `R#`, examples `S#`, vertical slices | `product_vision.md`, `glossary.md`, `features/00X-*/plan.md` |
| **2. Readiness Gate** | Tech Lead / Tooling | Verify consistency, ensure all `R#` have `S#` scenarios, compile initial `tasks.toml`, set state to `Ready` | `tasks.toml` |
| **3. Downstream (JIT)** | Agent (`scpe pack`) | Compiles slice payload (<1k tokens) containing only relevant rules, scenarios, terms, and commands. Writes code and tests in `apps/` | `tasks.toml`, `apps/` |
| **4. Audit & Sync** | Everyone / CLI | Track progress, log gotchas in `tasks.toml`, sync product root `roadmap.md` via `scpe roadmap --sync` | `roadmap.md`, `tasks.toml` |

#### The JIT Compilation Flow:
Instead of loading multiple markdowns into developer agent contexts, the agent runs:
```bash
python3 scripts/scpe.py pack 002-pix-payment 1
```
The engine inspects Slice 1, extracts solely the matching `R#` and `S#` blocks from `plan.md`, definitions from `glossary.md`, and test/build commands and boundaries from `app.toml`. The result is an ultra-lean context payload (~700 tokens) with zero token waste.

### 4.4. Feature State Machine

The feature's `tasks.toml` declares exactly one of these states under `[state]`:

```text
Draft → Ready → WIP → Done
  ↑        ↓      ↓
  └──── Blocked  Stale
           │        │
           └───→ (returns to Ready after resolution)
```

| State | Meaning | Set by |
|---|---|---|
| `Draft` | Being modeled in Upstream; not yet submitted to the Readiness Gate | Developers |
| `Ready` | Approved at the Readiness Gate; ready to be built | Tech Lead |
| `WIP` | Being built by a Downstream agent | Agent |
| `Blocked` | Stopped by an external dependency; returns to `Ready` once resolved | Agent or Developer |
| `Done` | Code in `apps/` matches current `plan.md` and passes tests | Agent, confirmed by review |
| `Stale` | `plan.md` was changed after `Done`; requires review before re-execution | Automatic, on any edit to `plan.md` |

### 4.5. Spec Drift

**Rule:** No change to the `plan.md` of a `Done` feature is silent.

When `plan.md` changes on a `Done` feature, the feature becomes `Stale` and returns to the Readiness Gate. Only the difference needs review:
- **Re-execute:** The change affects implemented behavior. The feature returns to `Ready`, and Downstream updates the affected code.
- **Accept the drift:** The change is cosmetic or non-breaking. The feature returns to `Done` with a log entry in `tasks.toml`.

### 4.6. Multi-Repository Applications

When an application's code lives in a separate repository, its manifest stays in `apps/<app>/` — the specification never leaves the product workspace — and the code is replaced by a pointer:

```text
apps/
└── api-core/
    ├── app.toml             # Stays inside the product workspace
    └── repo_pointer.md      # Repository URL, integration branch, reference commit
```

`repo_pointer.md` holds only location data, never code. The agent writes code to the external repository, but status (`tasks.toml`) and specification (`plan.md`, `app.toml`) always stay in the product workspace. What is distributed is the *code*, never the *specification*.

---

## 5. Standard File Formats

In SCPE, living Markdown represents human intent and domain rules, while TOML represents machine execution and manifests.

Naming inside a feature: rules are numbered `R1, R2…` and examples `S1, S2…`. Tasks and tests cite them as `<feature_name>#S2`. This is the traceability link from specification to code.

### Feature `plan.md`

```markdown
# Plan: Pix Payment

## Intent
Customers pay instantly with Pix instead of typing card details.

## Domain Model
- **Terms:** Order, Pix Charge (see glossary.md)
- **Entities:** Order (total, status), Pix Charge (amount, expires_at)
- **Domain events:** OrderPaid → notify Shipping

## Business Rules
- **R1:** A Pix charge expires 30 minutes after it is created.
- **R2:** An order is paid only when the confirmed amount equals the order total.

## Examples
- **S1 — Paid order:** Given an order of R$ 120 awaiting payment, When the customer pays R$ 120 with Pix, Then the order is marked paid.
- **S2 — Expired charge:** Given a Pix charge created 31 minutes ago and unpaid, When the customer opens the order, Then the charge shows as expired and a new one can be created.

## Slices
1. Pay an order with Pix — S1, R2
2. Expired charges — S2, R1

## Open Questions
- Should differences under R$ 0,01 be accepted? (Finance)
```

### Feature `tasks.toml` (Execution Graph & State)

```toml
[state]
current = "WIP"
updated_at = "2026-10-29"
updated_by = "senior-backend-developer"

[[slice]]
id = 1
name = "Pay an order with Pix"
description = "Immediate payment generation and webhook confirmation."
covers = ["S1", "R2"]
apps = ["api-core", "web-checkout"]
after = []
hitl = false
verify = "api-core#S1 and web-checkout#S1 integration tests pass"

[[task]]
id = "T1"
slice_id = 1
title = "Create a Pix charge for an order"
covers = ["S1"]
parallel = false
target_files = [
  "apps/api-core/src/pix.controller.ts",
  "apps/api-core/tests/pix-payment#S1.spec.ts"
]

[[task]]
id = "T2"
slice_id = 1
title = "Confirm payment from the bank webhook"
covers = ["S1", "R2"]
parallel = false
target_files = [
  "apps/api-core/src/pix-webhook.handler.ts"
]

[[log]]
date = "2026-10-29"
author = "senior-backend-developer"
entry = "T1 done. Bank sandbox rejects amounts with 3 decimals; no plan impact."
```

### `glossary.md` Entry

```markdown
## Contract
- **bounded_context:** Sales
- **definition:** A signed agreement that obliges both parties.
- **not_to_be_confused_with:** Proposal — an unsigned offer that can still change.
```

### Product `roadmap.md` (Auto-Synchronized)

```markdown
# Product Roadmap

| Feature | State | Slices Total | Done | WIP | Open Blockers |
|---|---|---|---|---|---|
| [001-user-auth](features/001-user-auth/) | Done | 2 | 2 | 0 | None |
| [002-pix-payment](features/002-pix-payment/) | WIP | 2 | 1 | 1 | None |
```

---

## Trade-offs

- **More states to audit.** Six formal states instead of four informal ones mean more protocol for the Tech Lead to watch — but an agent can follow them without ambiguity.
- **`Stale` forces reviews.** Every edit to `plan.md` after delivery goes back through the Readiness Gate, even when it is trivial. This is deliberate: an unnecessary review costs far less than undetected drift between specification and code.
- **`repo_pointer.md` can go out of date.** If a repository moves and the pointer is not updated, it points to the wrong place. This is accepted, because putting code from several repositories inside the product workspace would break its isolation. Automatic pointer checks are out of scope for now.
