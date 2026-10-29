---
id: 1
type: initiative
title: "SCPE 0.4.0 (Experimental): The Compiled & Lean Spec Engine"
parent: none
covers: []
sources: ["SCPE_METHOD.md", "README.md", "adr.md"]
after: []
risk: medium
---

# Initiative: SCPE 0.4.0 (Experimental) — The Compiled & Lean Spec Engine

## Description
Evolve the SCPE (Spec-Compiled Product Engineering) framework by introducing a compiled JIT context engine, flat sequential feature topology (`features/00X-slug/`), TOML-based execution metadata (ADR-001), a single consolidated product roadmap, and Git-native branch/PR lifecycle workflows. This eliminates the "Markdown Bloat" where agents were forced to read 8+ files per task, reducing token overhead by ~80% and delivering clean, human-readable specifications at every altitude.

## Outcome
Developers and AI agents build software with zero cognitive and token bloat: each task receives a pre-compiled, self-contained context payload (`scpe pack`) under 1,000 tokens; features are flat and sequentially numbered; the entire product roadmap is centralized and auto-synchronized; and every feature can be developed in an isolated Git branch with automated PR description generation.

## Requirements
- **R1 (Topology & Numbering):** Flatten the directory structure by removing the intermediate `epics/` folder. Every feature folder directly in `features/` is an atomic capability named with a 3-digit sequential prefix: `features/00X-<short-slug>/`.
- **R2 (Consolidated Roadmap):** Eliminate `feat_roadmap.md` and `epic_roadmap.md`. Maintain a single canonical `roadmap.md` at the product workspace root, auto-synchronized by `scpe.py roadmap --sync`.
- **R3 (TOML Execution Metadata - ADR-001):** Replace loose `tasks.md` and `quick_status.md` with a structured `tasks.toml` per feature (`[state]`, `[[slice]]`, `[[task]]`, `[[log]]`). Replace `app.md` with a strongly typed `app.toml` (`[app]`, `[commands]`, `[boundaries]`).
- **R4 (JIT Context Compiler `scpe pack`):** Implement `scpe pack <feature> <slice_id>` in `scpe.py` to extract only the Invariants `R#` and Scenarios `S#` from `plan.md`, definitions from `glossary.md`, and commands/boundaries from `app.toml` relevant to that slice, emitting a clean payload under 1,000 tokens.
- **R5 (JIT Glossary Lookup `scpe term`):** Implement `scpe term <word>` in `scpe.py` for instant CLI lookup of ubiquitous language entries in `glossary.md`.
- **R6 (Git-Native Branch Lifecycle):** Add `--branch` flag to `scpe feature "<Title>"` to automatically calculate the next sequential number, create the feature folder, and checkout a git branch `feat/00X-<slug>`.

## Constraints
- **Standard Library Only:** All CLI logic in `scpe.py` must use Python 3.11+ standard library (`tomllib`, `re`, `pathlib`, `subprocess`, `argparse`). Zero external pip dependencies.
- **Backwards Compatibility / Progressive Adoption:** The engine must continue to recognize existing workspaces while encouraging the new lean layout.
- **Preserve DDD Rigor:** Living Markdown remains sovereign for human intent (`product_vision.md`, `glossary.md`, `architecture.md`, `plan.md`). TOML is reserved for machine metadata and execution state.

## Done When
1. `templates/` in the SCPE skill contains canonical `app.toml` and `tasks.toml` scaffolds.
2. `scpe.py` implements `pack`, `term`, `roadmap --sync`, sequential numbering, and the `--branch` flag.
3. `scpe pack` successfully generates a compiled context payload under 1,000 tokens on a real or sample feature.
4. `SCPE_METHOD.md` and `README.md` are updated to reflect SCPE 0.4.0 architecture and ADR-001.
5. `SKILL.md` and agent guidelines (`senior-backend-developer.md`, `senior-frontend-developer.md`) instruct agents to use `scpe pack` instead of multi-file markdown reading.
6. A Pull Request is opened on GitHub against `main`.

## Boundaries
- Touch points: `scpe.py` engine, template scaffolds, method documentation, and agent personas.
- Must not change: The core Wave Pipeline (Upstream -> Gate -> Downstream -> Audit), DDD principles, or `<epic>#S#` test traceability requirements.

## References
- `adr.md` — ADR-001: Adoption of TOML for Execution Metadata, Task Graphs, and Manifests.
- `SCPE_METHOD.md` — Canonical SCPE method specification.
