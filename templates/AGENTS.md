# AGENTS.md — <Product Name>

This repository follows [SCPE](<link to SCPE_METHOD.md>). Read this file first in every session.

## Read Order
1. `product.md` — why the product exists.
2. The change you are working on: `changes/<chg-id>/change.md` and the files in its `spec/` folder.
3. Every artifact those files reference by ID (`spec/**`).
4. `apps/<app>/app.md` for each app listed in the change.
5. Accepted decisions in `decisions/`.

## Rules
- Never edit `product.md` or `spec/**` directly. Propose edits inside a change's `spec/` folder.
- Never set a change to `ready`, merge a pull request, or resolve an open question. Ask a human.
- If the spec looks wrong while building, stop: write the finding in the change's Log and set `blocked`.
- Name every test after the scenario it covers, e.g. `FEAT-<NAME>#S1 <short description>`.
- Follow accepted decisions. To deviate, propose a new decision instead.

## Commands
<!-- How to install, build, test and run each app. Keep these copy-pasteable. -->
- `<command>` — <what it does>

## Local Additions
<!-- Extra artifact types, naming conventions or review roles this product uses. Delete if none. -->
