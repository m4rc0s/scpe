# Spec-Native Product Architecture (SNPA v0.2.7)

## 1. Visão Geral
A **Spec-Native Product Architecture (SNPA)** define a topologia estrutural, física e estática do ecossistema de um produto dentro do framework **SCPE (v0.2.7)**.

## 2. Isolamento por Workspace & Repositório Invertido
* **Workspace Isolado:** `$HOME/product_design/<nome_do_produto>/` (um contêiner dedicado por produto para eliminar alucinações de contexto).
* **Inversão do Repositório:** O produto centraliza a governança viva (`index.md`, `product_vision.md`, `glossary.md`, `features/`) e delega a implementação física estritamente à pasta `apps/`.

## 3. O Ecossistema de Aplicações e o `app_liquid.md`
Cada software dentro de `apps/` possui seu próprio manifesto descritivo universal: o **`app_liquid.md`**.
```text
apps/
├── api-core/
│   ├── app_liquid.md        # Manifesto descritivo da aplicação
│   └── src/ ...             # Código fonte gerado como consequência
```
