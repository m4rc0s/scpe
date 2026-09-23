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
- 🏗️ **Product Workspace** — One isolated workspace per product, with an `app.md` manifest for each application in `apps/`.
- 🌊 **Wave Pipeline** — Upstream → Readiness Gate → Downstream → Audit, with a formal state for each epic.
- 🧩 **DDD as a Language, Not a Ritual** — Ubiquitous language, bounded contexts, invariants, and *Given/When/Then* examples shape the model before any code exists.

---

## 🚀 Get Started

There is no installer — SCPE is a method, not a package. Adopting it means structuring your product workspace like this:

```bash
# 1. Create the workspace for your product (one workspace per product, always)
mkdir -p ~/product_design/myproduct/{apps,features,assets}
cd ~/product_design/myproduct

# 2. Create the product root files
touch index.md product_vision.md roadmap.md glossary.md \
      architecture.md techinal_deal.md team_playbook.md quick_status.md
```

Then:

1. Read the **[method](SCPE_METHOD.md)**.
2. Fill in `product_vision.md` and `glossary.md` with your AI agent — this is **Upstream**.
3. Open the first feature in `features/<name>/index.md` and model the first epic in `plan.md`: rules, examples, and slices.
4. Pass the **Readiness Gate** — the Tech Lead validates the model and marks the epic `Ready`.
5. Let **Downstream** compile: the agent reads `plan.md`, writes `tasks.md`, and builds code and tests in `apps/`.

No installation. No proprietary CLI. Just Markdown, Git, and the agent your team already uses.

---

## 🌊 The Wave Pipeline

```text
 UPSTREAM               READINESS GATE            DOWNSTREAM                AUDIT
┌──────────────┐        ┌───────────────┐        ┌────────────────┐       ┌─────────────────┐
│ Feature      │        │ Tech Lead     │        │ plan.md   →    │       │ quick_status.md │
│ macro vision │ ─────▶ │ validates     │ ─────▶ │ tasks.md  →    │ ────▶ │ tracked in      │
│ + plan.md    │        │ model & marks │        │ code in        │       │ real time       │
│ (AI copilot) │        │ Ready         │        │ apps/          │       │                 │
└──────────────┘        └───────────────┘        └────────────────┘       └─────────────────┘
```

*Non-waterfall*: Waves run concurrently across different features — never as a single cascade for the whole product.

---

## 🏛️ The Product Workspace

```text
myproduct/                     # one workspace per product
├── index.md                   # master guide and navigation
├── product_vision.md          # vision, business goals, core problem
├── glossary.md                # ubiquitous language (DDD)
├── architecture.md            # C4 model, integrations
├── quick_status.md            # product-wide status panel
├── apps/                      # generated code — consequence, not starting point
│   └── api-core/
│       ├── app.md             # application manifest
│       └── src/...
└── features/                  # development cycle sliced by domain
    └── checkout/
        ├── index.md
        └── epics/
            └── pix-payment/
                ├── plan.md          # rules, examples, and slices
                ├── tasks.md         # atomic task queue
                └── quick_status.md  # epic state
```

The full workspace and the standard format of each file are in **[SCPE_METHOD.md](SCPE_METHOD.md)**.

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

| File | Role |
|---|---|
| [`SCPE_METHOD.md`](SCPE_METHOD.md) | The complete method, including the standard format of every file |

---

## 🤝 Contributing

This is a living method — just like the documentation it advocates. Gaps found in practice and change proposals follow the method's own principle: write the intent in Markdown, open the discussion, and let consensus become a commit.

---

<p align="center">Made by those who believe specification — not code — is the asset that endures.</p>
