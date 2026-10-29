# 🌊 SCPE — Spec-Compiled Product Engineering

> **Documentation becomes the contract. Code is the consequence.**
> A product engineering method for teams building products with AI agents as engineering partners — not fancy autocomplete.

[![Method](https://img.shields.io/badge/method-SCPE-6C5CE7)](SCPE_METHOD.md)
[![Source of truth](https://img.shields.io/badge/source%20of%20truth-Markdown%20%2B%20Natural%20Language-000000)](#-what-is-scpe)

**[What is SCPE](#-what-is-scpe) • [Why it exists](#-why-scpe-exists) • [Pillars](#-the-pillars) • [Get Started](#-get-started) • [Wave Pipeline](#-the-wave-pipeline) • [Workspace](#%EF%B8%8F-the-product-workspace) • [Epic States](#%EF%B8%8F-epic-states) • [FAQ](#-faq)**

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

```text
myproduct/                     # one workspace per product
├── index.md                   # master guide and navigation
├── product_vision.md          # vision, business goals, core problem
├── roadmap.md                 # strategic roadmap (synced via scpe roadmap --sync)
├── glossary.md                # ubiquitous language (DDD)
├── architecture.md            # C4 model, integrations
├── technical_deal.md          # agreements, constraints, approved stack
├── apps/                      # generated code — consequence, not starting point
│   └── api-core/
│       ├── app.toml           # application manifest & boundaries (ADR-001)
│       └── src/...
└── features/                  # flat sequential lifecycle
    └── 001-pix-payment/
        ├── plan.md            # intent, business rules (R#), examples (S#), slices
        └── tasks.toml         # state, slices, task graph, temporal log
```

The full workspace and the standard format of each file are in **[SCPE_METHOD.md](SCPE_METHOD.md)** and **[ADR-001](adr.md)**.

---

## ⚙️ Epic States

Each epic has one explicit state — no implicit states, no ambiguity for the agent:

```text
Draft → Ready → WIP → Done
  ↑        ↓      ↓      │
  └──── Blocked  Stale ◀─┘   (plan.md changed after delivery)
           │        │
           └───→ (returns to Ready after resolution)
```

- **`Draft`** — being modeled, not yet validated.
- **`Ready`** — approved at the Readiness Gate.
- **`WIP`** — being built by an agent.
- **`Blocked`** — stopped by an external dependency or a defect.
- **`Done`** — code matches the current plan.
- **`Stale`** — plan changed after delivery; goes back through the Readiness Gate before any new work.

This is what keeps "documentation as single source of truth" an **actively maintained** property. Details in **[SCPE_METHOD.md](SCPE_METHOD.md#44-epic-state-machine)**.

---

## ❓ FAQ

**Does SCPE replace Clean Architecture, DDD, SOLID?**
No — it presupposes them. SCPE decides *when* and *by whom* intent is specified; code in `apps/` follows whatever standards the product's `techinal_deal.md` defines.

**Do I need a specific tool to adopt SCPE?**
No. Any AI agent that can read Markdown and write code works for Downstream.

**What happens if I change `plan.md` after the epic is delivered?**
The epic becomes `Stale` and goes back to the Readiness Gate — it never turns into silent, hidden technical debt.

**Does SCPE work with multiple code repositories per product?**
Yes. The `app.md` stays in the product workspace, and a `repo_pointer.md` next to it points to the repository where the code lives.

**Is this only for teams already using AI heavily?**
It is designed for that, but the core — living documentation as contract, shared domain language, clear epic states — works even before an agent runs Downstream.

---

## 🗺️ Repository Map

| File / Folder | Role |
|---|---|
| [`SCPE_METHOD.md`](SCPE_METHOD.md) | The complete method, including the standard format of every file |
| [`adr.md`](adr.md) | Architecture Decision Records (e.g. ADR-001: TOML execution metadata) |
| [`scripts/scpe.py`](scripts/scpe.py) | Zero-dependency CLI engine (init, feature, pack, roadmap, term, validate) |
| [`templates/`](templates/) | Canonical scaffolds for `app.toml`, `plan.md`, `tasks.toml` |

---

## 🤝 Contributing

This is a living method — just like the documentation it advocates. Gaps found in practice and change proposals follow the method's own principle: write the intent in Markdown, open the discussion, and let consensus become a commit.

---

<p align="center">Made by those who believe specification — not code — is the asset that endures.</p>
