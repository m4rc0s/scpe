# 🌊 SCPE — Spec-Compiled Product Engineering

> **A documentação vira o contrato. O código é a consequência.**
> Um framework de Spec-Native Product Architecture (SNPA), operado pelo Autonomous Development Protocol (ADP), para times que constroem produtos com agentes de IA como parceiros de engenharia — não como autocomplete chique.

[![Metodologia](https://img.shields.io/badge/metodologia-SCPE-6C5CE7)](SCPE_METHOD.md)
[![Protocolo](https://img.shields.io/badge/protocolo-ADP-0984E3)](ADP_SPEC.md)
[![Arquitetura](https://img.shields.io/badge/arquitetura-SNPA-00B894)](ARCHITECTURE.md)
[![SSOT](https://img.shields.io/badge/SSOT-Markdown%20%2B%20Linguagem%20Natural-000000)](#-o-que-é-scpe)
[![Versionamento](https://img.shields.io/badge/versionamento-git%20tags-success)](#-versões)

**[O que é](#-o-que-é-scpe) • [Por que existe](#-por-que-o-scpe-existe) • [Pilares](#-os-pilares) • [Comece agora](#-comece-agora) • [Pipeline](#-o-pipeline-em-onda) • [Arquitetura](#-arquitetura-snpa) • [Protocolo](#-protocolo-adp) • [FAQ](#-faq) • [Versões](#-versões)**

---

## 🤔 O que é SCPE?

**SCPE (Spec-Compiled Product Engineering)** parte de uma aposta simples: se um agente de IA já escreve código com qualidade competitiva, o gargalo de um time deixou de ser "escrever sintaxe" e passou a ser **especificar intenção de negócio com precisão suficiente para que um agente a compile em software**.

Neste framework:

* A documentação viva, em **Markdown e linguagem natural**, é o **contrato imutável** e a única fonte da verdade (SSOT) — não um artefato acessório que fica desatualizado no primeiro sprint.
* O código em `apps/` é **gerado como consequência** da especificação, nunca o ponto de partida do trabalho.
* Motores de execução autônomos — qualquer agente capaz de ler Markdown e escrever código — compilam essa especificação em produtos reais, seguindo um protocolo operacional auditável, não um prompt solto no chat.

Isso não é *prompt engineering* disfarçado de metodologia. É um método de engenharia de produto — com arquitetura, máquina de estados e papéis definidos — que trata a especificação com o mesmo rigor que hoje tratamos código.

---

## 🌍 Por que o SCPE existe

O movimento de **Spec-Driven Development (SDD)** já tem referências abertas — [GitHub Spec-Kit](https://github.com/github/spec-kit), OpenSpec/SpecDD, [The SDD Standard](https://github.com/mmanzini/Spec-driven-development). O SCPE não compete com esse ecossistema: ele assume uma posição específica dentro dele.

| Framework | Onde ele resolve | Onde o SCPE difere |
|---|---|---|
| **GitHub Spec-Kit** | Padroniza o ciclo Constituição → Spec → Plan → Tasks → Implementação | SCPE isola o *workspace* por produto inteiro e formaliza o `app_liquid.md` como manifesto de cada app — a unidade é o produto, não um repositório de código isolado |
| **OpenSpec / SpecDD** | Formatos de arquivo e pastas de governança contra alucinação de contexto | SCPE amarra a especificação a um **protocolo de estados** (`Draft → Ready → WIP → Done → Stale`) executável por um agente sem margem de interpretação |
| **The SDD Standard** | Templates de Product Briefs, Steering Docs, Feature Specs | SCPE assume DDD conceitual — linguagem ubíqua, bounded contexts, invariantes — como o vocabulário de modelagem, não apenas o formato do arquivo |

**A linha do SCPE:** especificação não é *sobre* o código — ela **é** o produto. O código é a compilação.

---

## 🧭 Os Pilares

- 🔎 **Incremental Feature Discovery** — nada de mapear o sistema inteiro do zero. O time constrói a visão macro da feature mais importante para o negócio *agora*, aprende com a entrega real, e itera.
- 🏗️ **Spec-Native Product Architecture (SNPA)** — isolamento absoluto de workspace por produto e manifestos universais (`app_liquid.md`) para cada aplicação em `apps/`.
- 🤖 **Autonomous Development Protocol (ADP)** — pipeline em onda (Upstream → Readiness Gate → Downstream → Auditoria), com máquina de estados formal por épico.
- 🧑‍💻 **Desenvolvedor Universal** — PMs, designers, staff engineers e especialistas de negócio são todos "desenvolvedores": todos modelam intenção, ninguém apenas "passa requisito" adiante.
- 🧩 **DDD como linguagem, não como ritual** — linguagem ubíqua, bounded contexts e invariantes guiam a modelagem conceitual antes de existir uma linha de código.

---

## 🚀 Comece agora

Não existe instalador — o SCPE é uma especificação, não um pacote. Adotar o método é estruturar o workspace do seu produto assim:

```bash
# 1. Crie o workspace isolado do seu produto (um workspace por produto, sempre)
mkdir -p ~/product_design/meuproduto/{apps,features,assets}
cd ~/product_design/meuproduto

# 2. Crie os arquivos de contexto base — a raiz do produto
touch index.md product_vision.md roadmap.md glossary.md \
      architecture.md techinal_deal.md team_playbook.md quick_status.md
```

Depois:

1. Leia o **[documento mestre](SCPE_METHOD.md)** — o manifesto completo do método.
2. Preencha `product_vision.md` e `glossary.md` em conjunto com seu agente de IA — esse é o **Upstream**.
3. Abra a primeira feature em `features/<nome>/index.md` e modele o primeiro épico em `plan.md`.
4. Passe pelo **Readiness Gate** — Tech Lead / FDE valida o modelo e marca o épico `Ready`.
5. Deixe o **Downstream** compilar: o agente lê `plan.md`, gera `tasks.md`, e escreve código em `apps/`.

Sem instalação. Sem CLI proprietária. Só Markdown, Git, e o agente que o seu time já usa.

---

## 🌊 O Pipeline em Onda

```text
 UPSTREAM               READINESS GATE            DOWNSTREAM                AUDITORIA
┌──────────────┐        ┌───────────────┐        ┌────────────────┐       ┌─────────────────┐
│ Visão macro  │        │ Tech Lead/FDE │        │ plan.md   →     │       │ quick_status.md │
│ da feature + │ ─────▶ │ valida o      │ ─────▶ │ tasks.md  →     │ ────▶ │ rastreado em    │
│ plan.md      │        │ modelo e      │        │ código em       │       │ tempo real      │
│ (IA copiloto)│        │ marca Ready   │        │ apps/           │       │                 │
└──────────────┘        └───────────────┘        └────────────────┘       └─────────────────┘
```

*Non-waterfall*: as ondas correm de forma concorrente e assíncrona entre features distintas — nunca em cascata única para o produto inteiro.

---

## 🏛️ Arquitetura: SNPA

```text
meuproduto/                    # workspace isolado — um por produto
├── index.md                   # guia mestre e navegação
├── product_vision.md          # visão, objetivos de negócio, problema central
├── glossary.md                # linguagem ubíqua (DDD)
├── architecture.md            # C4 Model, integrações
├── quick_status.md            # painel de controle global
├── apps/                      # código gerado — consequência, não ponto de partida
│   └── api-core/
│       ├── app_liquid.md      # manifesto universal da aplicação
│       └── src/...
└── features/                  # ciclo de desenvolvimento por domínio
    └── checkout/
        ├── index.md
        └── epics/
            └── pagamento-pix/
                ├── plan.md          # DDD conceitual do épico
                ├── tasks.md         # fila de tarefas atômicas
                └── quick_status.md  # estado do épico
```

Especificação completa em **[ARCHITECTURE.md](ARCHITECTURE.md)**.

---

## ⚙️ Protocolo: ADP

Cada épico é uma máquina de estados explícita — sem estados implícitos, sem ambiguidade para o agente:

```text
Draft → Ready → WIP → Done
  ↑        ↓      ↓      │
  └──── Blocked  Stale ◀─┘   (plan.md mudou depois da entrega)
           │        │
           └───→ (retorna a Ready após resolução)
```

- **`Draft`** — em modelagem, ainda não validado.
- **`Ready`** — aprovado no Readiness Gate.
- **`WIP`** — em execução por um motor autônomo.
- **`Blocked`** — dependência externa ou defeito interrompeu a execução.
- **`Done`** — código corresponde ao plano vigente.
- **`Stale`** — o plano mudou depois da entrega; reentra no Readiness Gate antes de qualquer nova execução.

Isso é o que torna "documentação como fonte única da verdade" uma propriedade **ativamente mantida**, não uma aspiração de slide. Detalhes completos em **[SCPE_METHOD.md](SCPE_METHOD.md#4-protocolo-autonomous-development-protocol-adp)** e **[ADP_SPEC.md](ADP_SPEC.md)**.

---

## ❓ FAQ

**O SCPE substitui Clean Architecture, DDD, SOLID?**
Não — ele os pressupõe. SCPE decide *quando* e *por quem* a intenção é especificada; o código gerado em `apps/` segue os padrões técnicos que o `techinal_deal.md` do produto definir.

**Preciso de uma ferramenta específica para adotar o SCPE?**
Não. O método é agnóstico de motor de execução: qualquer agente de IA capaz de ler Markdown e escrever código serve como Downstream.

**O que acontece se eu mudar `plan.md` depois que o épico já foi entregue?**
Isso é tratado formalmente: o épico transiciona para `Stale` e reentra no Readiness Gate — não vira dívida técnica implícita e silenciosa.

**O SCPE funciona com múltiplos repositórios de código por produto?**
Sim, via `repo_pointer.md`: o `app_manifest.md` permanece no workspace do produto, apontando para o repositório físico externo onde o código realmente vive.

**Isso só serve para times que já usam IA pesadamente?**
É desenhado para esse cenário, mas o núcleo — documentação viva como contrato, DDD conceitual, protocolo de estados — vale mesmo antes de existir um agente autônomo rodando o Downstream.

---

## 🗺️ Mapa do Repositório

| Arquivo | Papel |
|---|---|
| [`SCPE_METHOD.md`](SCPE_METHOD.md) | Documento mestre — a especificação completa e vigente do método |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Spec-Native Product Architecture (SNPA), versão resumida |
| [`ADP_SPEC.md`](ADP_SPEC.md) | Autonomous Development Protocol, versão resumida |
| [`METHODOLOGY.md`](METHODOLOGY.md) | Princípios invioláveis, versão condensada |

---

## 🏷️ Versões

Existe **um único arquivo** de método (`SCPE_METHOD.md`) — sempre a especificação vigente. O histórico de versões vive no Git, como qualquer código:

```bash
git tag                                    # lista as versões publicadas
git show v0.2.7:SCPE_METHOD_v0.2.7.md      # lê o conteúdo de uma versão específica
git log --oneline v0.1.0..v0.3.0           # vê o que mudou entre duas versões
```

| Tag | O que marca |
|---|---|
| `v0.1.0` | Princípios iniciais — Spec-First Inversion, DDD conceitual, entregas incrementais |
| `v0.2.7` | Consolidação de SNPA + ADP, modelo Tandem, `app_liquid.md` como manifesto universal |
| `v0.3.0` | Máquina de estados do épico, protocolo de spec drift (`Stale`), suporte a multi-repositório |

Como o arquivo já se chamou `SCPE_METHOD_v0.1.0.md` e `SCPE_METHOD_v0.2.7.md` em versões passadas antes de ser unificado, use o caminho correspondente à tag ao inspecionar o histórico (ex.: `git show v0.1.0:SCPE_METHOD_v0.1.0.md`).

---

## 🤝 Contribuindo

Este é um método vivo — assim como a documentação que ele preconiza. Discordâncias, lacunas encontradas na prática e propostas de mudança seguem o mesmo princípio do método: escreva a intenção em Markdown, abra a discussão, deixe o consenso virar commit — e, quando for o caso, uma nova tag.

---

<p align="center">Feito por quem acredita que a especificação — não o código — é o ativo que dura.</p>
