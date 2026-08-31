# Autonomous Development Protocol (ADP)

## 1. Overview
The **Autonomous Development Protocol (ADP)** is the operational protocol governing the workflow of the **SCPE** framework.

## 2. Protocol Pillars
1. **Incremental Feature Discovery:** Iterative construction focused on the highest-priority business feature right now, without prior exhaustive waterfall mapping.
2. **Feature Hierarchy (`index.md` & SMART Epics):** Universal use of `index.md` as the entry point for features and epics.
3. **Wave Pipeline (Non-Waterfall):**
   - **Upstream:** Definition of the priority feature and structuring of `plan.md` with AI as a co-pilot.
   - **Readiness Gate:** Technical validation and marking as `Ready` by the FDE/Tech Lead.
   - **Downstream:** Iterative execution of atomic tasks in `tasks.md` generating code in `apps/` alongside `app_liquid.md`.
   - **Audit:** Real-time tracking via `quick_status.md`.
4. **Epic State Machine:** `quick_status.md` declares one of six formal states — `Draft → Ready → WIP → Done`, with `Blocked` and `Stale` as controlled deviations — each transition written strictly by the actor executing it. See complete specification in [`SCPE_METHOD.md`](SCPE_METHOD.md#44-epic-state-machine).
