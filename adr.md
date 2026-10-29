# Architecture Decision Records (ADR) — SCPE

Este documento registra as decisões arquiteturais fundamentais do método SCPE (Spec-Compiled Product Engineering).

---

## ADR-001: Adoção de TOML para Metadados Estruturados, Fila de Tarefas e Manifestos

- **Status:** Aceito
- **Data:** 2026-10-29
- **Decisores:** Marcos Araújo
- **Contexto:** Comparativo de eficiência operacional entre o BMad Method (v2–v7) e o SCPE.

### Contexto & Problema

O SCPE nasceu sob o princípio de *"Living Markdown é o contrato; o código em `apps/` é a consequência"*. Embora o Markdown e a linguagem natural sejam insubstituíveis para modelagem de domínio por humanos (DDD, visão de produto, glossário ubíquo, regras de negócio `R#` e cenários `S#` Given/When/Then), o uso de Markdown puro para dados operacionais de máquina (`tasks.md`, `app.md`, `quick_status.md`) apresentou fragilidades quando manipulado diretamente por agentes de IA:

1. **Fragilidade de Sintaxe em IA:** LLMs frequentemente cometem erros de parse ao tentar editar tabelas de markdown, checklists com múltiplos metadados inline ou campos `- **chave:** valor` com caracteres especiais.
2. **Ausência de Grafo de Dependências Estrito nas Tarefas:** O formato `- [ ] T1 — descrição (S1, R2)` em `tasks.md` não suporta nativamente ordenação DAG (Directed Acyclic Graph), bloqueios entre tarefas (`after = [...]`), checkpoints humanos (`hitl = true`), estimativas de risco e execução isolada por fatia.
3. **Sobrecarga de Contexto no Downstream:** Sem tarefas estruturadas, o agente de desenvolvimento downstream precisa carregar o repositório inteiro de especificações para entender o contexto de uma única tarefa, degradando a atenção do LLM e desperdiçando tokens.
4. **Armadilhas do YAML:** O YAML foi descartado por ser estritamente sensível a espaços/indentação e ambíguo em tipagem (`no` virando booleano, strings com `:` quebrando parse).

### Decisão

Adotamos a divisão de responsabilidades:
- **Markdown (`.md`):** Exclusivo para **intenção humana, modelagem e documentação viva** (`product_vision.md`, `glossary.md`, `architecture.md`, `technical_deal.md`, `plan.md`).
- **TOML (`.toml`):** Adotado para **metadados estruturados, grafos de execução de agentes, configurações e manifestos de máquina**.

#### O que passa a usar TOML:

1. **Fila de Execução e Fatias (`tasks.toml`):**
   Substitui/complementa o `tasks.md` em cada épico (`features/<feature>/epics/<epic>/tasks.toml`):
   ```toml
   # tasks.toml — Grafo de fatias e tarefas compiladas do plan.md
   [[slice]]
   id = 1
   name = "Cobrança Pix Imediata"
   covers = ["S1", "R2"]
   after = []
   hitl = false
   risk = "low"
   apps = ["api-core", "web-checkout"]
   verify = "api-core#S1 gera QR Code e web-checkout exibe tela de pagamento"

   [[task]]
   id = "T1"
   slice_id = 1
   title = "Endpoint de criação de cobrança Pix"
   covers = ["S1"]
   after = []
   target_files = [
     "apps/api-core/src/controllers/pix.controller.ts",
     "apps/api-core/tests/pix-payment#S1.spec.ts"
   ]
   ```

2. **Manifesto de Aplicação (`app.toml`):**
   Substitui o `app.md` em `apps/<app>/app.toml` (ou na raiz em tiny SCPE):
   ```toml
   [app]
   name = "api-core"
   type = "backend-api"
   description = "Serviço central de processamento de transações financeiras"
   stack = "TypeScript, Fastify, Prisma, PostgreSQL"
   standards = "Clean Architecture, SOLID, Hexagonal"
   entrypoint = "src/main.ts"
   depends_on = ["database", "payment-gateway"]

   [commands]
   run = "npm run dev"
   test = "npm test"
   lint = "npm run lint"

   [boundaries]
   forbidden = [
     "Não renderiza UI/HTML",
     "Não armazena dados de cartão em plain text"
   ]
   ```

3. **Status e Transições de Estado (`status.toml`):**
   Substitui/estrutura o `quick_status.md`:
   ```toml
   [state]
   current = "WIP"
   updated_by = "senior-backend-developer"
   updated_at = "2026-10-29T15:15:00Z"

   [[log]]
   date = "2026-10-29"
   author = "senior-backend-developer"
   entry = "T1 concluído. Sandbox do banco homologado para S1."

   [blockers]
   active = false
   items = []
   ```

4. **Configurações Globais do SCPE Workspace (`scpe.toml`):**
   Configurações de workspace, plugins habilitados, thresholds do gate e preferências do time.

### Consequências

#### Positivas:
- **Zero Ambiguidades e Sem Erros de Indentação:** Ao contrário do YAML, o TOML possui sintaxe plana de seções/tabelas e tipos rigorosos (`true`/`false`, aspas explícitas).
- **Processamento Nativo em Python:** `scpe.py` utiliza o módulo nativo `tomllib` (Python 3.11+), mantendo o princípio de **zero dependências externas**.
- **Isolamento de Contexto no Downstream:** Com `tasks.toml`, um novo comando `scpe compile-slice` pode alimentar o agente apenas com o bloco da fatia atual e os arquivos alvos, eliminando o *context bloat*.
- **Compatibilidade com Comentários:** Diferente do JSON, o TOML aceita comentários completos (`#`), permitindo que templates sirvam como guia interativo para pessoas e agentes.

#### Negativas / Mitigações:
- *Dois formatos no workspace:* Humanos e agentes manipulam `.md` e `.toml`.  
  *Mitigação:* A fronteira é clara: se é sobre o **domínio do negócio ou arquitetura**, é `.md`. Se é **instrução de execução para ferramentas e agentes**, é `.toml`.
