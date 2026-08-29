# Spec-Compiled Product Engineering (SCPE v0.2.6)

> **Um framework de Spec-Native Product Architecture (SNPA) impulsionado pelo Autonomous Development Protocol (ADP), guiado por modelagem colaborativa de domínio e facilitação técnica sênior.**

---

## 📋 Sumário Executivo

A evolução tecnológica revolucionou a engenharia de software ao automatizar a criação de sintaxe com qualidade que iguala ou supera a de desenvolvedores experientes. No **Spec-Compiled Product Engineering (SCPE v0.2.6)**, a documentação viva — estruturada puramente em **Markdown e linguagem natural** — é estabelecida como o contrato imutável e a única fonte da verdade (SSOT). 

O framework fundamenta-se em pilares fundamentais:
1. **Senior-Led Domain Discovery (Tandem Model):** O Especialista de Domínio conhece profundamente o negócio, mas a tradução desse conhecimento em uma solução orientada ao domínio é conduzida em tandem por lideranças técnicas sênior (Arquiteto, Staff ou Principal Engineer) atuando como condutores. Através de workshops de facilitação e dinâmicas como **EventStorming** com o time e interessados, eles estruturam o domínio, Bounded Contexts e invariantes, auxiliados por agentes de IA como co-pilotos.
2. **Spec-Native Product Architecture (SNPA):** Isolamento de workspace e manifestos de aplicação (`app_manifest.md`) para gerenciar a camada física em `apps/`.
3. **Autonomous Development Protocol (ADP):** O protocolo operacional que garante que motores autônomos e agentes executem o downstream de forma padronizada, assíncrona e em ondas.

---

## 1. Arquitetura: Spec-Native Product Architecture (SNPA v0.2.6)

A **SNPA** define a topologia estrutural, física e estática do ecossistema de um produto, unindo a governança de negócio e as especificações de domínio à camada de software compilado.

### 1.1. Isolamento Absoluto por Workspace
* **Caminho padrão:** `$HOME/product_design/<nome_do_produto>/`
* **Garantia:** Contêiner de workspace isolado por produto para proteger contra vazamentos de contexto em motores de execução.

### 1.2. Inversão do Repositório do Produto (Estrutura Macro)
```text
meuproduto/
├── index.md                 # Guia mestre da estrutura e sumário do produto
├── product_vision.md        # Visão macro, objetivos de negócio e problema central
├── roadmap.md               # Marcos estratégicos globais
├── glossary.md              # Dicionário de Linguagem Ubíqua (âncora semântica do domínio)
├── architecture.md          # Padrões C4 Model e integrações sistêmicas globais
├── techinal_deal.md         # Acordos técnicos e stack homologada
├── team_playbook.md         # Regras de engajamento e cultura do time
├── quick_status.md          # Painel de controle global e dinâmico
├── assets/                  # Wireframes e assets visuais de referência
├── apps/                    # Camada física de software compilado (implementação)
└── features/                # O ecossistema de especificação fatiado por domínios
```

### 1.3. O Ecossistema de Aplicações (`apps/`) e o Manifesto (`app_manifest.md`)
A pasta `apps/` abriga os softwares físicos gerados como consequência da especificação. Cada software possui seu próprio **Manifesto de Aplicação (`app_manifest.md`)**:
```text
apps/
├── api-core/
│   ├── app_manifest.md      # Manifesto descritivo da aplicação
│   └── src/ ...             # Código gerado (Clean Architecture / Hexagonal / S.O.L.I.D.)
└── web-client/
    ├── app_manifest.md      # Manifesto descritivo da aplicação
    └── src/ ...             # Código gerado
```

#### Exemplo de `app_manifest.md`:
```markdown
# App Manifest: api-core

- **app_name:** api-core
- **app_type:** backend-rest-api
- **tech_stack:** Kotlin, Spring Boot, PostgreSQL
- **design_patterns:** Clean Architecture, Hexagonal (Ports and Adapters), S.O.L.I.D.
- **app_description:** Serviço central responsável pelo processamento de transações.
- **entrypoint:** src/main/kotlin/com/meuproduto/Main.kt
```
O manifesto permite que motores autônomos e desenvolvedores compreendam instantaneamente a responsabilidade e os padrões de engenharia de cada aplicação sem varreduras custosas no código-fonte.

---

## 2. Protocolo: Autonomous Development Protocol (ADP v0.2.6)

O **Autonomous Development Protocol (ADP)** é o protocolo operacional que rege o fluxo de trabalho. Ele define a mecânica padronizada e em ondas (non-waterfall) que garante que os agentes e motores autônomos operem de forma determinística, segura e previsível no produto.

### 2.1. Senior-Led Domain Discovery (O Papel do Conductor em Tandem)
A modelagem conceitual de domínio é conduzida por uma liderança técnica sênior (Arquiteto, Staff ou Principal Engineer) atuando como *conductor* em parceria (*tandem*) com o Especialista de Domínio:
* **Visão Holística e Facilitação:** Condução de workshops e dinâmicas como **EventStorming** com o time e stakeholders para mapear eventos, comandos, agregados e Bounded Contexts.
* **Agentes como Co-Pilotos:** Uso da IA para estruturar rascunhos de domínio (`plan.md`) durante as sessões.

### 2.2. A Estrutura Tática de Features e Épicos
Cada pasta de feature e épico segue o padrão estrito de especificação:
```text
features/
└── [nome_da_feature]/
    ├── index.md             # Visão geral da funcionalidade e Bounded Context
    ├── feat_roadmap.md      # Marcos temporais da feature
    ├── quick_status.md      # Status local atual (Ready, WIP, Blocked, Done)
    └── epics/
        └── [nome_do_epico]/
            ├── index.md         # Escopo detalhado do Épico
            ├── plan.md          # Enabler de Domínio: DDD conceitual estruturado via EventStorming
            ├── tasks.md         # Fila de Tarefas Atômicas para os Motores Autônomos executarem
            └── epic_roadmap.md  # Planejamento tático de execução
```

### 2.3. O Pipeline em Onda (Non-Waterfall Workflow)
O ADP rejeita fluxos em cascata. O trabalho flui de forma concorrente, contínua e assíncrona através de três fases interligadas:

1. **Upstream (Senior-Led Tandem Discovery & EventStorming):**
   - O Conductor e o Especialista de Domínio conduzem sessões práticas, utilizando agentes como co-pilotos para consolidar o domínio conceitual (`plan.md`).
2. **Readiness Gate (A Validação Técnica):**
   - O Tech Lead / FDE valida a consistência do modelo conceitual, assegura o alinhamento com os acordos de arquitetura e define o status como `Ready`.
3. **Downstream (Execução Padronizada / Code as Consequence):**
   - Assim que o épico atinge o estado `Ready`, motores autônomos seguem o ADP para puxar as tarefas atômicas de `tasks.md` e implementam o software em `apps/` de forma padronizada e estritamente aderente ao domínio modelado.

---

## 3. O Papel do Ecossistema
* **Conductor (Arquiteto / Staff / Principal) + Especialista de Domínio:** Tandem condutor do discovery, facilitação (EventStorming) e modelagem conceitual.
* **Product Engineers & Stakeholders:** Participam ativamente da intenção e refinamento.
* **Motores Autônomos:** Executam a implementação downstream de forma padronizada sob o rigor do ADP.
