---
id: FEAT-<NAME>
type: feature
title: <Feature name>
status: draft
actors: [ACT-<NAME>]
context: CTX-<NAME>
rules: []              # RULE- IDs this feature must respect
terms: []              # TERM- IDs used below
---

## Outcome
<!-- What the actor gets and why it matters. One or two sentences. -->

## Flow
<!-- The main path, as numbered steps in product language. -->
1. <step>

## Alternatives and Failures
<!-- Other paths and what the product does when things go wrong. -->
- <condition> → <what happens>

## Scenarios
<!-- One scenario per behaviour. IDs S1, S2… never change. One When per scenario. Then = observable result. -->

### S1 — <short name>
- **Given** <context>
- **When** <one action or event>
- **Then** <observable result>

## Out of Scope
<!-- What this feature deliberately does not cover. -->
