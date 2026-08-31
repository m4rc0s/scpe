# 🌊 SCPE — Spec-Compiled Product Engineering

> **Documentation becomes the contract. Code is the consequence.**
> A Spec-Native Product Architecture (SNPA) framework, operated by the Autonomous Development Protocol (ADP), for teams building products with AI agents as engineering partners — not fancy autocomplete.

[![Methodology](https://img.shields.io/badge/methodology-SCPE-6C5CE7)](SCPE_METHOD.md)
[![Protocol](https://img.shields.io/badge/protocol-ADP-0984E3)](ADP_SPEC.md)
[![Architecture](https://img.shields.io/badge/architecture-SNPA-00B894)](ARCHITECTURE.md)
[![SSOT](https://img.shields.io/badge/SSOT-Markdown%20%2B%20Natural%20Language-000000)](#-what-is-scpe)
[![Versioning](https://img.shields.io/badge/versioning-git%20tags-success)](#-versions)

**[What is SCPE](#-what-is-scpe) • [Why it exists](#-why-scpe-exists) • [Pillars](#-the-pillars) • [Get Started](#-get-started) • [Wave Pipeline](#-the-wave-pipeline) • [Architecture](#-architecture-snpa) • [Protocol](#-protocol-adp) • [FAQ](#-faq) • [Versions](#-versions)**

---

## 🤔 What is SCPE?

**SCPE (Spec-Compiled Product Engineering)** starts from a simple premise: if an AI agent can already write code with competitive quality, a team's bottleneck is no longer "writing syntax" — it has shifted to **specifying business intent with sufficient precision for an agent to compile it into software**.

In this framework:

* Living documentation, written purely in **Markdown and natural language**, is the **immutable contract** and single source of truth (SSOT) — not an auxiliary artifact that goes stale in the first sprint.
* Code in `apps/` is **generated as a consequence** of the specification, never the starting point of work.
* Autonomous execution engines — any agent capable of reading Markdown and writing code — compile this specification into real products, following an auditable operational protocol, not a loose chat prompt.

This is not *prompt engineering* disguised as a methodology. It is a product engineering method — with defined architecture, state machine, and roles — that treats specifications with the same rigor we treat code today.

---

## 🌍 Why SCPE Exists

The **Spec-Driven Development (SDD)** movement already has open references — [GitHub Spec-Kit](https://github.com/github/spec-kit), OpenSpec/SpecDD, [The SDD Standard](https://github.com/mmanzini/Spec-driven-development). SCPE does not compete with this ecosystem; it occupies a specific position within it.

| Framework | Problem it Solves | Where SCPE Differs |
|---|---|---|
| **GitHub Spec-Kit** | Standardizes the Constitution → Spec → Plan → Tasks → Implementation cycle | SCPE isolates the *workspace* per entire product and formalizes `app_liquid.md` as each app's manifest — the unit is the product, not an isolated code repository |
| **OpenSpec / SpecDD** | File formats and governance folders against context hallucination | SCPE binds the specification to a **state protocol** (`Draft → Ready → WIP → Done → Stale`) executable by an agent without ambiguity |
| **The SDD Standard** | Templates for Product Briefs, Steering Docs, Feature Specs | SCPE adopts conceptual DDD — ubiquitous language, bounded contexts, invariants — as the modeling vocabulary, not merely the file format |

**SCPE's bottom line:** Specification is not *about* the code — it **is** the product. Code is the compilation.

---

## 🧭 The Pillars

- 🔎 **Incremental Feature Discovery** — No mapping the entire system from scratch. The team builds the macro vision of the most critical feature for the business *now*, learns from real delivery, and iterates.
- 🏗️ **Spec-Native Product Architecture (SNPA)** — Absolute workspace isolation per product and universal manifests (`app_liquid.md`) for each application in `apps/`.
- 🤖 **Autonomous Development Protocol (ADP)** — Wave pipeline (Upstream → Readiness Gate → Downstream → Audit), with a formal state machine per epic.
- 🧑‍💻 **Universal Developer** — PMs, designers, staff engineers, and domain experts are all "developers": everyone models intent; no one merely "hands off requirements".
- 🧩 **DDD as a Language, Not a Ritual** — Ubiquitous language, bounded contexts, and invariants guide conceptual modeling before a single line of code exists.

---

## 🚀 Get Started

There is no installer — SCPE is a specification, not a package. Adopting the method means structuring your product workspace like this:

```bash
# 1. Create the isolated workspace for your product (one workspace per product, always)
mkdir -p ~/product_design/myproduct/{apps,features,assets}
cd ~/product_design/myproduct

# 2. Create the baseline context files — the product root
touch index.md product_vision.md roadmap.md glossary.md \
      architecture.md techinal_deal.md team_playbook.md quick_status.md
```

Then:

1. Read the **[master document](SCPE_METHOD.md)** — the complete method manifesto.
2. Fill out `product_vision.md` and `glossary.md` alongside your AI agent — this is the **Upstream**.
3. Open the first feature in `features/<name>/index.md` and model the first epic in `plan.md`.
4. Pass through the **Readiness Gate** — Tech Lead / FDE validates the model and marks the epic `Ready`.
5. Let **Downstream** compile: the agent reads `plan.md`, generates `tasks.md`, and writes code in `apps/`.

No installation. No proprietary CLI. Just Markdown, Git, and the agent your team already uses.

---

## 🌊 The Wave Pipeline

```text
 UPSTREAM               READINESS GATE            DOWNSTREAM                AUDIT
┌──────────────┐        ┌───────────────┐        ┌────────────────┐       ┌─────────────────┐
│ Feature      │        │ Tech Lead/FDE │        │ plan.md   →     │       │ quick_status.md │
│ macro vision │ ─────▶ │ validates     │ ─────▶ │ tasks.md  →     │ ────▶ │ tracked in      │
│ + plan.md    │        │ model & marks │        │ code in         │       │ real-time       │
│ (AI copilot) │        │ Ready         │        │ apps/           │       │                 │
└──────────────┘        └───────────────┘        └────────────────┘       └─────────────────┘
```

*Non-waterfall*: Waves run concurrently and asynchronously across distinct features — never in a single cascade for the entire product.

---

## 🏛️ Architecture: SNPA

```text
myproduct/                     # isolated workspace — one per product
├── index.md                   # master guide and navigation
├── product_vision.md          # vision, business goals, core problem
├── glossary.md                # ubiquitous language (DDD)
├── architecture.md            # C4 Model, integrations
├── quick_status.md            # global control panel
├── apps/                      # generated code — consequence, not starting point
│   └── api-core/
│       ├── app_liquid.md      # universal application manifest
│       └── src/...
└── features/                  # development cycle sliced by domain
    └── checkout/
        ├── index.md
        └── epics/
            └── pix-payment/
                ├── plan.md          # conceptual DDD of the epic
                ├── tasks.md         # atomic task queue
                └── quick_status.md  # epic state
```

Complete specification in **[ARCHITECTURE.md](ARCHITECTURE.md)**.

---

## ⚙️ Protocol: ADP

Each epic is an explicit state machine — no implicit states, no ambiguity for the agent:

```text
Draft → Ready → WIP → Done
  ↑        ↓      ↓      │
  └──── Blocked  Stale ◀─┘   (plan.md changed after delivery)
           │        │
           └───→ (returns to Ready after resolution)
```

- **`Draft`** — in modeling, not yet validated.
- **`Ready`** — approved at the Readiness Gate.
- **`WIP`** — currently being executed by an autonomous engine.
- **`Blocked`** — external dependency or defect interrupted execution.
- **`Done`** — code matches the current plan.
- **`Stale`** — plan changed after delivery; re-enters Readiness Gate before any new execution.

This is what makes "documentation as single source of truth" an **actively maintained** property, not slide aspiration. Full details in **[SCPE_METHOD.md](SCPE_METHOD.md#4-protocol-autonomous-development-protocol-adp)** and **[ADP_SPEC.md](ADP_SPEC.md)**.

---

## ❓ FAQ

**Does SCPE replace Clean Architecture, DDD, SOLID?**
No — it presupposes them. SCPE determines *when* and *by whom* intent is specified; generated code in `apps/` follows whatever technical standards the product's `techinal_deal.md` defines.

**Do I need a specific tool to adopt SCPE?**
No. The method is execution-engine agnostic: any AI agent capable of reading Markdown and writing code works as Downstream.

**What happens if I change `plan.md` after the epic is already delivered?**
This is handled formally: the epic transitions to `Stale` and re-enters the Readiness Gate — it does not become silent, implicit technical debt.

**Does SCPE work with multiple code repositories per product?**
Yes, via `repo_pointer.md`: the `app_manifest.md` stays in the product workspace, pointing to the external physical repository where code actually lives.

**Is this only for teams already using AI heavily?**
It is designed for that scenario, but the core — living documentation as contract, conceptual DDD, state protocol — holds true even before an autonomous agent runs Downstream.

---

## 🗺️ Repository Map

| File | Role |
|---|---|
| [`SCPE_METHOD.md`](SCPE_METHOD.md) | Master document — complete and active method specification |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Spec-Native Product Architecture (SNPA), summary version |
| [`ADP_SPEC.md`](ADP_SPEC.md) | Autonomous Development Protocol (ADP), summary version |
| [`METHODOLOGY.md`](METHODOLOGY.md) | Inviolable principles, condensed version |

---

## 🏷️ Versions

There is **a single method file** (`SCPE_METHOD.md`) — always the current specification. Version history lives in Git, just like code:

```bash
git tag                                    # list published versions
git show v0.2.7:SCPE_METHOD_v0.2.7.md      # inspect a specific past version
git log --oneline v0.1.0..v0.3.0           # view changes between versions
```

| Tag | Significance |
|---|---|
| `v0.1.0` | Initial principles — Spec-First Inversion, conceptual DDD, incremental deliveries |
| `v0.2.7` | Consolidation of SNPA + ADP, Tandem model, `app_liquid.md` as universal manifest |
| `v0.3.0` | Epic state machine, spec drift protocol (`Stale`), multi-repository support |

Since the file was named `SCPE_METHOD_v0.1.0.md` and `SCPE_METHOD_v0.2.7.md` in past versions before being consolidated, use the corresponding path for the tag when inspecting history (e.g., `git show v0.1.0:SCPE_METHOD_v0.1.0.md`).

---

## 🤝 Contributing

This is a living method — just like the documentation it advocates. Disagreements, gaps found in practice, and change proposals follow the method's own principle: write the intent in Markdown, open the discussion, let consensus become a commit — and, when appropriate, a new tag.

---

<p align="center">Made by those who believe specification — not code — is the asset that endures.</p>

