# 🌊 SCPE — Spec-Compiled Product Engineering

> **Documentation becomes the contract. Code is the consequence.**
> A product engineering method for teams building products with AI agents as engineering partners — not fancy autocomplete.

[![Method](https://img.shields.io/badge/method-SCPE-6C5CE7)](SCPE_METHOD.md)
[![Source of truth](https://img.shields.io/badge/source%20of%20truth-Markdown%20%2B%20Natural%20Language-000000)](#-what-is-scpe)

**[What is SCPE](#-what-is-scpe) • [Why it exists](#-why-scpe-exists) • [Pillars](#-the-pillars) • [Get Started](#-get-started) • [Wave Pipeline](#-the-wave-pipeline) • [Workspace](#%EF%B8%8F-the-product-workspace) • [Agents](#-specialized-agent-roster) • [Feature States](#%EF%B8%8F-feature-states) • [FAQ](#-faq)**

---

## 🤔 What is SCPE?

**SCPE (Spec-Compiled Product Engineering)** starts from a simple premise: if an AI agent can already write code with competitive quality, a team's bottleneck is no longer writing syntax — it is **specifying business intent precisely enough for an agent to compile it into software**.

In this method:

* Living documentation, written in **Markdown and natural language**, is the contract and the single source of truth — not a side artifact that goes stale in the first sprint.
* Code in `apps/` is **generated as a consequence** of the specification, never the starting point of work.
* Any agent that can read Markdown and write code compiles the specification into a real product, following a clear workflow — not a loose chat prompt.
* **Everyone is a Developer**: PMs, designers, engineers, and domain experts all write the specification together.

---

## 🌍 Why SCPE Exists

The **Spec-Driven Development** movement already has open references. SCPE builds on them and occupies a specific position:

| Reference | What It Solves | Where SCPE Differs |
|---|---|---|
| [GitHub Spec-Kit](https://github.com/github/spec-kit), OpenSpec | Spec → Plan → Tasks → Implementation for one change | The unit is the whole **product**: one workspace holds the vision, glossary, features, and every app |
| [Product Definition as Code](https://github.com/product-definition-as-code/spec) | A versioned, validated product definition in Markdown | Lighter: plain Markdown in a fixed workspace, written by everyone, no schemas required |
| [specdriven.com](https://specdriven.com/) | Intent → Spec → Implementation → Evidence, with rules and *Given/When/Then* examples | Adds a workspace layout and an epic state machine an agent can follow |
| [AI-Native Agile Manifesto](https://arxiv.org/html/2605.07717v2) | Shared living context, humans in control, verification first | Applied to one product team and its repository |

**SCPE's bottom line:** The specification is not *about* the code — it **is** the product. Code is the compilation.

---

## 🧭 The Pillars

- 🧑‍💻 **Everyone is a Developer** — PMs, designers, staff engineers, and domain experts all model intent; nobody just hands off requirements. Humans decide; agents execute.
- 🔎 **Incremental Feature Discovery** — No mapping the entire system upfront. Build the macro vision of the most critical feature *now*, learn from real delivery, and iterate.
- 🏗️ **Product Workspace & Lean Manifests** — One isolated workspace per product, with strongly typed `app.toml` manifests for each application in `apps/`.
- ⚡ **JIT Context Compilation (`scpe pack`)** — Downstream agents do not parse dozens of markdown files; the engine compiles exact slice context (<1k tokens) containing only relevant rules, scenarios, terms, and boundaries.
- 📐 **Flat Sequential Topology & Git Lifecycles** — Features live in flat folders (`features/00X-<slug>/`) with automatic sequential prefixes and isolated Git feature branches (`feat/00X-<slug>`).
- 🌊 **Wave Pipeline & Traceability** — Upstream → Readiness Gate → Downstream → Audit, with machine states in `tasks.toml` and test evidence linking back to `<feature>#S#`.
- 🧩 **DDD as a Language, Not a Ritual** — Ubiquitous language, bounded contexts, invariants, and *Given/When/Then* examples shape the model before any code exists.

---

## 🚀 Get Started

SCPE provides a zero-dependency CLI engine (`scpe.py`) using Python 3.11+ standard library:

```bash
# 1. Initialize a new product workspace
python3 scripts/scpe.py init "My Product" ~/product_design/myproduct
cd ~/product_design/myproduct

# 2. Create your first feature in its own Git branch
python3 scripts/scpe.py feature "Pix Payment" --branch

# 3. Model your plan in features/001-pix-payment/plan.md (Upstream)
# 4. Compile tasks into tasks.toml and pass the Readiness Gate

# 5. Compile JIT slice context for downstream AI agents (Downstream)
python3 scripts/scpe.py pack 001-pix-payment 1

# 6. Auto-sync the product roadmap
python3 scripts/scpe.py roadmap --sync
```

No external dependencies. Just Python standard library, Markdown, TOML, Git, and your AI agent.

---

## 🌊 The Wave Pipeline

```text
 UPSTREAM               READINESS GATE            DOWNSTREAM (JIT)            AUDIT & SYNC
┌──────────────┐        ┌───────────────┐        ┌──────────────────┐       ┌─────────────────┐
│ Feature      │        │ Tech Lead     │        │ scpe pack <f> <s>│       │ scpe roadmap    │
│ plan.md      │ ─────▶ │ verifies &    │ ─────▶ │ compiled context │ ────▶ │ --sync          │
│ (AI copilot) │        │ compiles      │        │ → code & tests   │       │ tasks.toml log  │
│              │        │ tasks.toml    │        │ in apps/ (<1k tok│       │                 │
└──────────────┘        └───────────────┘        └──────────────────┘       └─────────────────┘
```

*Non-waterfall*: Waves run concurrently across different features — never as a single cascade for the whole product.

---

## 🏛️ The Product Workspace

SCPE eliminates unnecessary markdown bloat, adopting a **lean, flat, and direct workspace structure** inspired by BMad:

```text
myproduct/                     # one workspace per product
├── agents.toml                # agent roster, stages, write ownership & boundaries (BMad-inspired)
├── roadmap.md                 # single consolidated product roadmap (synced via scpe roadmap --sync)
├── glossary.md                # ubiquitous language (queried JIT via scpe term <word>)
├── architecture.md            # C4 model, system boundaries, approved stack & engineering guardrails
├── product_vision.md          # (optional) macro business vision, problem statement & drivers
│
├── apps/                      # generated applications (consequence of spec, not starting point)
│   └── api-core/
│       ├── app.toml           # typed application manifest, commands & negative boundaries
│       └── src/...            # generated domain, infra, and tests
│
└── features/                  # flat sequential capability lifecycle (each folder is an epic)
    ├── 001-user-auth/
    │   ├── plan.md            # domain intent, rules (R#), examples (S#), vertical slices
    │   └── tasks.toml         # machine state, task graph, and temporal audit log
    └── 002-pix-payment/
        ├── plan.md
        └── tasks.toml
```

- **Clean & Direct Root**: No redundant indices (`index.md`) or duplicate agreement files (`technical_deal.md`, `team_playbook.md`). Architectural agreements and tech stack live in `architecture.md` and `app.toml`; agent governance lives in `agents.toml`.
- **Single Source of Truth Roadmap**: `roadmap.md` is centralized at the root and auto-synchronized across all feature lifecycles via `scpe roadmap --sync`.
- **Flat Features (Zero Jira-bloat)**: No hollow `epics/` folders, `quick_status.md`, or per-feature roadmaps. Each sequential feature folder (`features/00X-<slug>/`) contains only **`plan.md`** (human/agent intent) and **`tasks.toml`** (machine execution).

The full workspace and the standard format of each file are in **[SCPE_METHOD.md](SCPE_METHOD.md)** and **[ADR-001](adr.md)**.

---

## 🤖 Specialized Agent Roster

SCPE workspaces structure collaboration across 7 native specialized agents defined in `agents.toml`:

| Agent | Specialty | Stage (Wave) | Owns (Writes) | Boundaries (Consults) |
|---|---|---|---|---|
| **`product-manager`** 🎯 | Product Engineering | **1. Upstream** | `product_vision.md`, `roadmap.md`, `glossary.md`, `features/*/plan.md` | `architecture.md`, `apps/*/app.toml` |
| **`ux-researcher`** 📊 | User Behavior & Analytics | **1. Upstream** | `research/`, `analytics_plan.md` | `product_vision.md`, `features/*/plan.md` |
| **`senior-fullstack-product-designer`** 🎨 | Product Design & UI | **1. Upstream** & **3. Downstream** | `design_system.md`, `assets/`, `apps/*/src/components/ui/` | `product_vision.md`, `features/*/plan.md` |
| **`software-architect`** 🏛️ | Architecture & Tech Lead | **2. Readiness Gate** | `architecture.md`, `apps/*/app.toml`, `adr.md` | `features/*/plan.md` |
| **`senior-backend-developer`** ⚙️ | Backend & Persistence | **3. Downstream (JIT)** | `apps/*/src/domain/`, `apps/*/src/infrastructure/`, `apps/*/tests/`, `features/*/tasks.toml` | `apps/*/app.toml` boundaries, `features/*/plan.md` |
| **`senior-frontend-developer`** 💻 | Frontend & UI State | **3. Downstream (JIT)** | `apps/*/src/pages/`, `apps/*/src/components/`, `apps/*/tests/ui/`, `features/*/tasks.toml` | `design_system.md`, `apps/*/app.toml`, `features/*/plan.md` |
| **`ux-specialist`** 🔍 | Runtime UI Audit | **4. Audit** | `audits/ux_audit.md` | `design_system.md`, running UI |

---

## ⚙️ Feature States

Declared inside each feature's `tasks.toml` under `[state]`:

```text
Draft → Ready → WIP → Done
  ↑        ↓      ↓      │
  └──── Blocked  Stale ◀─┘   (plan.md changed after delivery)
           │        │
           └───→ (returns to Ready after resolution)
```

- **`Draft`** — being modeled in Upstream; not yet validated at the Readiness Gate.
- **`Ready`** — validated by the Tech Lead / Software Architect; ready for agent compilation.
- **`WIP`** — being actively implemented by downstream developer agents.
- **`Blocked`** — stopped by an external dependency or defect.
- **`Done`** — code matches the current `plan.md` and passes `<feature>#S#` tests.
- **`Stale`** — `plan.md` was edited post-delivery; requires review before re-execution.

---

## ❓ FAQ

**Does SCPE replace Clean Architecture, DDD, SOLID?**  
No — it presupposes them. SCPE decides *when* and *by whom* intent is specified; code in `apps/` follows whatever standards the product's `architecture.md` and `app.toml` define.

**Do I need a specific tool to adopt SCPE?**  
No, but the built-in `scripts/scpe.py` CLI (zero external dependencies, Python 3.11+ standard library) provides commands for init, feature scaffolding, JIT context packing (`scpe pack`), and automated roadmap synchronization (`scpe roadmap --sync`).

**What happens if I change `plan.md` after a feature is delivered?**  
The feature becomes `Stale` and returns to the Readiness Gate — it never turns into silent, hidden technical debt.

**Does SCPE work with multiple code repositories per product?**  
Yes. The `app.toml` stays in the product workspace, and a `repo_pointer.md` next to it points to the external repository where the code lives.

---

## 🗺️ Repository Map

| File / Folder | Role |
|---|---|
| [`SCPE_METHOD.md`](SCPE_METHOD.md) | The complete method specification, file standards, and protocols |
| [`adr.md`](adr.md) | Architecture Decision Records (e.g. ADR-001: TOML execution metadata) |
| [`scripts/scpe.py`](scripts/scpe.py) | Zero-dependency CLI engine (init, feature, pack, roadmap, term, validate) |
| [`templates/`](templates/) | Canonical scaffolds for `app.toml`, `plan.md`, `tasks.toml`, `agents.toml` |

---

## 🤝 Contributing

This is a living method — just like the documentation it advocates. Gaps found in practice and change proposals follow the method's own principle: write the intent in Markdown, open the discussion, and let consensus become a commit.

---

<p align="center">Made by those who believe specification — not code — is the asset that endures.</p>
