# Spec-Native Product Architecture (SNPA)

## 1. Overview
The **Spec-Native Product Architecture (SNPA)** defines the structural, physical, and static topology of a product's ecosystem within the **SCPE** framework.

## 2. Workspace Isolation & Inverted Repository
* **Isolated Workspace:** `$HOME/product_design/<product_name>/` (a dedicated container per product to eliminate context hallucinations).
* **Repository Inversion:** The product centralizes living governance (`index.md`, `product_vision.md`, `glossary.md`, `features/`) and strictly delegates physical implementation to the `apps/` folder.

## 3. Application Ecosystem and `app_liquid.md`
Each piece of software inside `apps/` has its own universal descriptive manifest: **`app_liquid.md`**.
```text
apps/
├── api-core/
│   ├── app_liquid.md        # Universal application manifest
│   └── src/ ...             # Source code generated as a consequence
```
