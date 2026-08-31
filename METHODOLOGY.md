# Spec-Compiled Product Engineering (SCPE)

## Visão Geral
O **Spec-Compiled Product Engineering (SCPE)** é o framework que unifica o **Spec-Native Product Architecture (SNPA)** e o **Autonomous Development Protocol (ADP)** sob os princípios imutáveis de Domain-Driven Design (DDD) e **Incremental Feature Discovery**.

## Princípios Invioláveis (Cumulative Legacy)
1. **Spec-First Inversion & Markdown SSOT:** A documentação em Markdown é a única fonte da verdade e o contrato imutável.
2. **Incremental Feature Discovery:** Foco na visão macro da feature mais importante para o momento do negócio, rejeitando mapeamento exaustivo do zero e abraçando aprendizado contínuo, iteração e falhas precoces.
3. **SNPA & Repositório Invertido:** Isolamento absoluto de workspace por produto (`$HOME/product_design/<produto>/`) e manifestos universais de aplicação (`app_liquid.md`) em `apps/`.
4. **ADP (Autonomous Development Protocol):** Pipeline em ondas (*non-waterfall*) com Upstream, Readiness Gate, Downstream de tarefas atômicas (`tasks.md`), máquina de estados formal por épico e auditoria via `quick_status.md`.
5. **Desenvolvedor Universal:** Todos na equipe (PMs, Designers, Staff, Engenheiros) participam ativamente da modelagem conceitual e intenção de negócio.

A versão vigente do método é sempre a apontada pela tag Git mais recente (`git tag`) — não há número de versão no nome de arquivo.
