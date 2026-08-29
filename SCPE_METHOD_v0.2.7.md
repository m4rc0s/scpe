# Spec-Compiled Product Engineering (SCPE v0.2.7)

> **Um framework de Spec-Native Product Architecture (SNPA) impulsionado pelo Autonomous Development Protocol (ADP), guiado por desenvolvimento incremental, entrega iterativa e modelagem colaborativa de intenção de negócio.**

---

## 📋 Sumário Executivo & Manifesto

A Inteligência Artificial chegou e revolucionou, assim como em tantas outras áreas, a engenharia de software e, consequentemente, o desenvolvimento de produtos cujos meios são softwares, automatizando a criação de sintaxe com qualidade comprovada que, em muitos casos, supera a de desenvolvedores experientes.

Nesta metodologia (**SCPE v0.2.7**), a documentação viva — estruturada puramente em **Markdown e linguagem natural** — é estabelecida como o contrato imutável e a única fonte da verdade (SSOT).

O framework fundamenta-se em pilares fundamentais:

* **Incremental Feature Discovery (Visão Macro e Entrega Iterativa):** O foco não é tentar mapear ou descobrir um sistema inteiro do zero, mas sim construir em conjunto a visão macro da feature mais importante para o negócio naquele momento. Abraçamos o desenvolvimento incremental, o aprendizado contínuo através da prática, a entrega iterativa, a mitigação de riscos e a capacidade de falhar cedo para pivotar rapidamente.
* **Spec-Native Product Architecture (SNPA):** Isolamento de workspace por produto e manifestos universais de aplicação (`app_liquid.md`) para gerenciar a camada física em `apps/`.
* **Autonomous Development Protocol (ADP):** O protocolo operacional que garante que motores autônomos e agentes executem o downstream de forma padronizada, assíncrona e em ondas.

### Por que padronizar a documentação em Markdown e Linguagem Natural?

A adoção de arquivos puramente em Markdown e linguagem natural oferece flexibilidade e clareza incomparáveis para equipes e ecossistemas orientados a IA:

* **Legibilidade Universal (Humanos e IAs):** Qualquer pessoa da equipe (técnica ou de negócios) consegue ler, auditar e colaborar sem fricção, enquanto os agentes de IA processam o contexto perfeitamente.
* **Versionamento Impecável:** O Git gerencia diffs limpos e lineares, permitindo rastrear a evolução da intenção de negócio e da arquitetura ao longo do tempo.
* **Independência de Ferramentas:** A especificação pertence ao repositório do produto, mantendo a fonte única da verdade independente de plataformas proprietárias.

---

## 0. O Ecossistema Global de Spec-Driven Development (SDD) e Nossos Diferenciais

O movimento de **Spec-Driven Development (SDD)** e **Spec-First** integra a vanguarda atual da engenharia de software guiada por agentes, encontrando paralelo em iniciativas abertas da comunidade global de tecnologia:

* **GitHub Spec-Kit (`github/spec-kit`):** O projeto de referência que padroniza o ciclo de Constituição → Especificação → Planejamento → Tarefas → Implementação para multiplataformas de agentes.
* **OpenSpec / SpecDD (`specdd.ai`):** O movimento comunitário focado em formatos padronizados de arquivos de especificação e pastas de governança para mitigar alucinações de contexto em IAs.
* **The SDD Standard (`mmanzini/Spec-driven-development`):** Repositórios abertos que formalizam templates de Product Briefs, Steering Docs e Feature Specs.

### Aspectos e Práticas Invioláveis Destacadas por este Método:

* **Isolamento Absoluto por Workspace (Contêiner por Produto):** Protege contra alucinações de contexto ao restringir o escopo operacional do agente estritamente à pasta do produto ativo.
* **A Inversão do Repositório do Produto:** Antigamente, clonávamos o código-fonte de microsserviços isolados. Agora, clonávamos o **Produto** por completo, onde a documentação estruturada capacita os agentes de IA a trabalharem com eficiência, e o código é um *asset* subordinado para validar, executar, testar e fazer o deploy.
* **Hierarquia Estrutural `Produto → Apps`:** O produto centraliza tudo de forma clara: `Produto → Apps → {AppBackend, Client, etc.}`.
* **Excelência Técnica na Implementação (`apps/`):** O código gerado aplica rigorosamente padrões consolidados da indústria (**S.O.L.I.D., Clean Architecture, Arquitetura Hexagonal, Ports and Adapters, Design Patterns e MVC**).
* **Manifesto de Aplicação Nativo (`app_liquid.md`):** Um descritor universal e agnóstico em Markdown que entrega instantaneamente ao agente a responsabilidade, o ecossistema e os limites de cada software contido em `apps/`.

---

## 1. O Novo Paradigma do Domain-Driven Design (DDD) e o Papel Universal do "Desenvolvedor"

Quando Eric Evans escreveu o seu clássico livro sobre Domain-Driven Design, sua premissa fundamental não era sobre como mapear tabelas no banco de dados, mas sim que **o coração do software está na sua capacidade de resolver problemas relacionados ao domínio do usuário**. Ao removermos a barreira da implementação técnica mecânica (agora delegada à IA), aplicamos o DDD na sua forma mais pura: o foco incansável no negócio.

Neste cenário de revolução, **o termo "Desenvolvedor" ganha um significado universal**. Todos os envolvidos na concepção do produto (Product Managers, Designers, Engineering Managers, Staff ou especialistas de negócio) são Desenvolvedores.

Na especificação guiada pelos humanos, o foco absoluto recai sobre os seguintes pilares do DDD conceitual:

* **Linguagem Ubíqua (O "Prompt" Definitivo):** Um glossário rico e unificado (`glossary.md`) que blinda o sistema contra alucinações. Se o negócio define que um "Contrato" difere de uma "Proposta", a IA e a equipe devem usar exatamente esses termos.
* **Bounded Contexts (Foco Autônomo):** Limites claros de onde cada regra de negócio começa e termina. Para a IA, isso garante foco absoluto no micro-universo da feature.
* **Entidades e Regras de Negócio (Invariantes):** Entidades possuem identidade única e ciclo de vida, regidas por "invariantes" — regras que nunca podem ser quebradas.
* **Eventos de Domínio:** Capturam a dinâmica fluida de reações e mudanças de estado crítico no sistema (*"Quando 'Pedido' for pago, notifique 'Expedição'"*).

---

## 2. Arquitetura: Spec-Native Product Architecture (SNPA)

Organizando o portfólio de forma limpa no ambiente de desenvolvimento (ex: `$HOME/product_design/`), o princípio fundamental é o isolamento absoluto: **um workspace dedicado por produto**.

### Anatomia da Raiz do Produto (Workspace Isolado):

```text
meuproduto/
├── index.md                 # Guia mestre da estrutura, sumário e navegação geral
├── product_vision.md        # Visão macro, objetivos de negócio, rentabilidade e problema central
├── roadmap.md               # Direcionamento estratégico e marcos globais do produto
├── glossary.md              # Dicionário da Linguagem Ubíqua (termos de domínio invariáveis)
├── architecture.md          # Padrões C4 Model, escolhas sistêmicas abstratas e integrações
├── techinal_deal.md         # Acordos técnicos, algemas da IA, restrições e stack homologada
├── team_playbook.md         # Regras de engajamento, fluxo de trabalho e cultura da equipe
├── quick_status.md          # Painel de controle global e dinâmico do produto
├── assets/                  # Documentos de referência, wireframes e assets visuais
├── apps/                    # Camada física de ativos: softwares sob padrões rígidos de engenharia
└── features/                # Ciclo de desenvolvimento fatiado por domínios e funcionalidades
```

---

## 3. O Ecossistema de Aplicações (`apps/`) e o Manifesto (`app_liquid.md`)

A pasta `apps/` abriga o software físico gerado como consequência natural da especificação. Cada aplicação possui seu próprio manifesto descritivo universal em Markdown: o **`app_liquid.md`**.

```text
apps/
├── api-core/
│   ├── app_liquid.md        # Manifesto descritivo da aplicação
│   └── src/ ...             # Código fonte gerado via Agente (Clean Arch / Hexagonal)
└── desktop-client/
    ├── app_liquid.md        # Manifesto descritivo da aplicação
    └── src/ ...             # Código fonte gerado via Agente
```

### Estrutura Padrão do `app_liquid.md`:

```markdown
# App Manifest: api-core

- **app_name:** api-core
- **app_type:** backend-rest-api
- **tech_stack:** Kotlin, Spring Boot, PostgreSQL
- **design_patterns:** Clean Architecture, Hexagonal (Ports and Adapters), S.O.L.I.D.
- **app_description:** Serviço central responsável pelo processamento de transações e ledger financeiro.
- **entrypoint:** src/main/kotlin/com/meuproduto/Main.kt
- **dependencies_scope:** Comunicação síncrona via HTTP com o client e mensageria assíncrona para eventos de domínio.
```

---

## 4. Protocolo: Autonomous Development Protocol (ADP)

### 4.1. Incremental Feature Discovery (Visão Macro e Entrega Iterativa)

O processo de especificação rejeita a tentativa exaustiva e burocrática de mapear um sistema inteiro do início ao fim. Em vez disso, a equipe foca em construir a **visão macro da feature mais importante para o negócio naquele momento**:

* **Aprendizado Contínuo e Iteração:** Adota-se o desenvolvimento incremental ("aprender enquanto faz"), validando hipóteses rapidamente, iterando sobre as entregas reais e garantindo espaço para falhar cedo, corrigir rotas e evoluir o produto de forma orgânica.
* **IA como Co-Piloto Colaborativo:** Os papéis estratégicos do time utilizam os agentes para rascunhar e estruturar rapidamente a intenção pura da feature prioritária em artefatos textuais padronizados (`plan.md`).

### 4.2. O Ciclo de Features, Épicos e a Padronização do `index.md`

A gestão ágil acontece nativamente na árvore de diretórios. Padronizamos o uso de **`index.md`** como ponto de entrada universal para parsers e IDEs orientadas a IA.

```text
features/
└── [nome_da_feature]/
    ├── index.md             # Visão geral da funcionalidade, escopo de negócio e valor
    ├── feat_roadmap.md      # Marcos temporais da feature
    ├── quick_status.md      # Status local atual (Ready, WIP, Blocked, Done)
    └── epics/               # Divisão da feature em pacotes atômicos
        └── [nome_do_epico]/
            ├── index.md         # Escopo detalhado do Épico e Bounded Contexts
            ├── plan.md          # Enabler de Domínio: DDD conceitual estruturado para entrega incremental
            ├── tasks.md         # Fila de Tarefas Atômicas para o Agente executar
            ├── quick_status.md  # Rastro local de auditoria e status de andamento
            └── epic_roadmap.md  # Planejamento tático de execução
```

### 4.3. O Pipeline em Onda (Non-Waterfall Workflow)

O ADP rejeita fluxos em cascata. O trabalho flui de forma concorrente, contínua e assíncrona através de fases interligadas:

1. **Upstream (Incremental Feature Discovery & Alinhamento Estratégico):** A equipe alinha a prioridade de negócio atual, desenhando a visão macro da feature mais importante e utilizando agentes como co-pilotos para estruturar o `plan.md`.
2. **Readiness Gate (A Validação Técnica):** O Tech Lead / FDE valida a consistência do modelo conceitual, assegura o alinhamento arquitetural e define o status como `Ready`.
3. **Downstream (Execução Padronizada / Code as Consequence):** Com o plano aprovado, o agente traduz o `plan.md` em tarefas atômicas no `tasks.md`. Motores autônomos executam a fila iterativamente, alocando o código gerado em `apps/` junto ao respectivo `app_liquid.md`.
4. **Auditoria Contínua:** Progresso, aprendizado prático e bloqueios são rastreados em tempo real nos arquivos `quick_status.md`.

---

## 5. O Fluxo de Trabalho com Agentes (Spec-First com Governança Técnica)

* **Contexto Base:** Refinamento colaborativo dos arquivos da raiz (`product_vision.md`, `architecture.md`, `techinal_deal.md`), estabelecendo as diretrizes de código e padrões de engenharia (Clean Arch, S.O.L.I.D., Hexagonal).
* **Definição de Feature:** Abertura do escopo da feature via `index.md`, alinhando perfeitamente as regras de negócio e o valor entregue ao usuário.
* **Modelagem no Épico (`plan.md`):** O agente propõe o rascunho aplicando DDD conceitual com base no contexto. O engenheiro revisa e aprimora a intenção pura de forma leve e interativa.
* **Planejamento Operacional (`tasks.md`):** O agente traduz o plano conceitual em uma fila clara de tarefas atômicas para a construção do código.
* **Geração Ágil e Inspeção Humana (`apps/`):** O agente gera a estrutura de código em minutos. O desenvolvedor atua como um arquiteto revisor, garantindo a excelência técnica, os padrões de projeto e a escalabilidade.
* **Auditoria Contínua:** Acompanhamento transparente do progresso e fluidez das entregas através dos arquivos `quick_status.md`.
