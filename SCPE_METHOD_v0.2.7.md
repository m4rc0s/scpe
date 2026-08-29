# Spec-Compiled Product Engineering (SCPE v0.2.7)

> **Um framework de Spec-Native Product Architecture (SNPA) impulsionado pelo Autonomous Development Protocol (ADP), guiado por desenvolvimento incremental, entrega iterativa e modelagem colaborativa de intenção de negócio.**

---

## 📋 Sumário Executivo & Manifesto

A Inteligência Artificial chegou e revolucionou, assim como em tantas outras áreas, a engenharia de software e, consequentemente, o desenvolvimento de produtos cujos meios são softwares, automatizando a criação de sintaxe com qualidade comprovada que, em muitos casos, supera a de desenvolvedores experientes. 

Nesta metodologia (**SCPE v0.2.7**), a documentação viva — estruturada puramente em **Markdown e linguagem natural** — é o próprio coração do produto. A intenção de negócio, o domínio e os padrões de excelência em engenharia tornam-se o patrimônio imutável que guia os agentes autônomos rumo a entregas extraordinárias.

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

Em uma verdadeira sinergia multidisciplinar, a equipe atua de forma orquestrada:
* **Linguagem Ubíqua (O "Prompt" Definitivo):** Um glossário rico e unificado (`glossary.md`) que blinda o sistema contra alucinações. Se o negócio define que um "Contrato" difere de uma "Proposta", a IA e a equipe devem usar exatamente esses termos.
* **Bounded Contexts (Foco Autônomo):** Limites claros de onde cada regra de negócio começa e termina, garantindo foco no micro-universo da feature.
* **Entidades e Regras de Negócio (Invariantes):** Entidades possuem identidade única e ciclo de vida, regidas por "invariantes" — regras universais que nunca podem ser quebradas.
* **Eventos de Domínio:** Capturam a dinâmica fluida de reações e mudanças de estado crítico no sistema (*"Quando 'Pedido' for pago, notifique 'Expedição'"*).

---

## 2. Arquitetura: Spec-Native Product Architecture (SNPA)

Organizando o portfólio de forma limpa no ambiente de desenvolvimento (ex: `$HOME/product_design/`), o princípio fundamental é o isolamento absoluto: **um workspace dedicado por produto**.

### Anatomia da Raiz do Produto (Workspace Isolado):
```text
meuproduto/
├── index.md                 # Guia mestre da estrutura, sumário e navegação geral do repositório
├── product_vision.md        # Visão macro, objetivos de negócio, rentabilidade e problema central
├── roadmap.md               # Direcionamento estratégico e marcos globais do produto
├── glossary.md              # Dicionário da Linguagem Ubíqua (termos de domínio invariáveis para a IA)
├── architecture.md          # Padrões C4 Model, escolhas sistêmicas abstratas e integrações
├── techinal_deal.md         # Acordos técnicos, diretrizes para a IA, restrições e stack homologada
├── team_playbook.md         # Regras de engajamento, fluxo de trabalho e cultura da equipe
├── quick_status.md          # Painel de controle global e dinâmico do produto
├── assets/                  # Documentos de referência, wireframes e assets visuais
├── apps/                    # A camada física de ativos: softwares sob padrões rígidos de engenharia
└── features/                # O ciclo de desenvolvimento fatiado por domínios e funcionalidades
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

## 4. O Ciclo de Features, Épicos e a Padronização do `index.md`

A gestão ágil ganha agilidade nativa na árvore de diretórios, onde cada pasta de feature atua como um agregador de valor de negócio. O uso padronizado do arquivo `index.md` serve como ponto de entrada universal e semântico para parsers, ferramentas de busca e agentes de IA.

```text
features/
└── [nome_da_feature]/
    ├── index.md             # Visão geral da funcionalidade e escopo de negócio
    ├── feat_roadmap.md      # Marcos e passos para entregar a feature completa
    ├── quick_status.md      # Status atual (Ready, WIP, Blocked, Done)
    └── epics/               # Divisão da feature em pacotes atômicos de entrega de valor
        └── [nome_do_epico]/
            ├── index.md         # Escopo detalhado do Épico, Bounded Contexts e Critérios de Aceite
            ├── plan.md          # Enabler de Domínio: DDD conceitual estruturado para a entrega incremental
            ├── tasks.md         # Fila de Tarefas Atômicas e operacionais para o Agente executar
            ├── quick_status.md  # Rastro local de auditoria e status de andamento deste épico
            └── epic_roadmap.md  # Planejamento tático de execução das entregas deste épico
```

---

## 5. Protocolo: Autonomous Development Protocol (ADP) & O Fluxo de Trabalho com Agentes

O **ADP** é o protocolo operacional que rege o fluxo de trabalho do SCPE. Ele rejeita fluxos em cascata e burocracias de mapeamento prévio exaustivo, operando como um pipeline contínuo, assíncrono e concorrente:

### 5.1. Incremental Feature Discovery (Visão Macro e Entrega Iterativa)
O processo rejeita o mapeamento de um sistema inteiro do zero (*Big Design Up Front*). A equipe foca em construir a **visão macro da feature mais importante para o negócio naquele momento**:
* **O Tandem de Modelagem:** O Especialista de Domínio (detentor do negócio) e a liderança técnica sênior / Arquiteto (condutor da modelagem de domínio) atuam em par.
* **Dinâmicas Práticas (ex: EventStorming):** Conduzem exercícios focados exclusivamente no escopo da feature prioritária com o time e interessados, usando IA como co-piloto para rascunhar o `plan.md`.
* **Aprendizado Contínuo e Falha Precoce:** Foco em entregas incrementais rápidas, validando hipóteses e corrigindo rotas com agilidade.

### 5.2. As 6 Etapas do Fluxo de Trabalho (Spec-First com Governança Técnica)
1. **Contexto Base:** Refinamento colaborativo dos arquivos da raiz (`product_vision.md`, `architecture.md`, `techinal_deal.md`, `glossary.md`), estabelecendo a linguagem ubíqua, diretrizes de código e padrões de engenharia (Clean Arch, S.O.L.I.D., Hexagonal).
2. **Definição de Feature (Upstream):** Abertura do escopo da feature prioritária via `index.md`, alinhando perfeitamente as regras de negócio e o valor entregue ao usuário, guiada pela expertise multidisciplinar da equipe.
3. **Modelagem no Épico (`plan.md`):** O Arquiteto e o Especialista de Domínio estruturam o DDD conceitual (EventStorming focado). O agente de IA propõe e refina os enablers de domínio sem introduzir código concreto.
4. **Readiness Gate & Planejamento Operacional (`tasks.md`):** O Tech Lead / FDE valida a consistência técnica, aprova o plano, marca como `Ready` e traduz o plano conceitual em uma fila clara de tarefas atômicas para a construção do código.
5. **Geração Ágil e Inspeção Humana (`apps/` - Downstream):** Motores autônomos puxam as tarefas de `tasks.md` e geram o código na pasta `apps/` seguindo o respectivo `app_liquid.md`. A equipe atua como revisor estratégico, garantindo a excelência técnica e padrões de projeto.
6. **Auditoria Contínua:** Acompanhamento transparente do progresso, aprendizado prático e bloqueios em tempo real através dos arquivos `quick_status.md`.
