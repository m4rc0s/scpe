---
id: CHG-<NAME>
type: change
title: <What should become true>
status: draft          # draft | ready | building | blocked | done | dropped
add: []                # new artifact IDs; full files go in this change's spec/ folder
modify: []             # existing artifact IDs; full new versions go in this change's spec/ folder
remove: []             # existing artifact IDs to retire
apps: []               # app names affected
---

## Problem
<!-- What is wrong or missing today, and the evidence. -->

## Intended Outcome
<!-- What will be true after this change, and how we will know (metric or observation). -->

## Slices
<!-- Vertical by default: each slice delivers something observable and names the scenarios it makes pass.
     The builder adds tasks when work starts. If a slice cannot be vertical, say why. -->

### Slice 1 — <observable result> (FEAT-<NAME>#S1)
- [ ] <task>

## Open Questions
<!-- Unresolved decisions, with who can answer. Blocking questions must be closed before `ready`. -->

## Out of Scope

## Log
<!-- Dated notes while building: blockers, findings, spec questions. Replaces status files. -->

## Outcome Check
<!-- After release: did the Intended Outcome happen? What did we learn? Which changes follow? -->
