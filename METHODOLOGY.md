# Spec-Compiled Product Engineering (SCPE)

## Overview
**Spec-Compiled Product Engineering (SCPE)** is the framework that unifies **Spec-Native Product Architecture (SNPA)** and the **Autonomous Development Protocol (ADP)** under the immutable principles of Domain-Driven Design (DDD) and **Incremental Feature Discovery**.

## Inviolable Principles (Cumulative Legacy)
1. **Spec-First Inversion & Markdown SSOT:** Documentation in Markdown is the single source of truth (SSOT) and the immutable contract.
2. **Incremental Feature Discovery:** Focus on the macro vision of the most critical feature for current business needs, rejecting exhaustive upfront mapping and embracing continuous learning, rapid iteration, and failing early.
3. **SNPA & Inverted Repository:** Absolute workspace isolation per product (`$HOME/product_design/<product>/`) and universal application manifests (`app_liquid.md`) in `apps/`.
4. **ADP (Autonomous Development Protocol):** Wave-based pipeline (*non-waterfall*) with Upstream, Readiness Gate, Downstream atomic task execution (`tasks.md`), formal epic state machine, and real-time auditing via `quick_status.md`.
5. **Universal Developer:** Everyone on the team (PMs, Designers, Staff, Engineers) actively participates in conceptual modeling and capturing business intent.

The current active version of the method is always pointed to by the latest Git tag (`git tag`) — there is no version number in the file name.
