# Spec-Compiled Product Engineering (SCPE v0.3.0 — Proposta)

> Um framework de Spec-Native Product Architecture (SNPA), operado pelo Autonomous Development Protocol (ADP), fundamentado em descoberta incremental de domínio, modelagem colaborativa da intenção de negócio e **rastreabilidade formal entre especificação e implementação**.

Esta versão herda a base de v0.2.7 (revisada) sem alterações nas Seções 0–3 e 5. As mudanças estão concentradas no protocolo (Seção 4), motivadas por três lacunas que a revisão de prosa não podia resolver: nenhuma delas é um problema de redação — são ausências de mecanismo. Seção 4 ganha ainda um direcionamento de planejamento (4.2.1), que não fecha uma lacuna do protocolo — é uma recomendação opcional sobre como fatiar épicos, motivada por um princípio já assumido em 4.1 (Incremental Feature Discovery) que a versão anterior não tornava explícito no nível do épico.

---

## Motivação: Três Lacunas Não Resolvidas em v0.2.7

**Lacuna 1 — Deriva de especificação (spec drift).** O protocolo descreve como `plan.md` se torna `tasks.md` se torna código em `apps/`, mas não descreve o que acontece quando `plan.md` muda *depois* que o código já foi gerado. Aprendizado contínuo — um pilar explícito do método desde v0.2.7 — implica que o Upstream revisita épicos já entregues. Sem um mecanismo que marque o código como desatualizado em relação ao plano, "aprendizado contínuo" e "SSOT" (fonte única da verdade) são incompatíveis na prática: o plano muda, o código não sabe.

**Lacuna 2 — Nenhum estado formal de execução.** `quick_status.md` é referenciado com exemplos de estado (`Ready`, `WIP`, `Blocked`, `Done`) mas o método nunca declara o conjunto completo de estados válidos nem suas transições permitidas. Um agente autônomo não pode implementar uma máquina de estados que não está especificada — o próprio framework viola, aqui, seu princípio de que uma invariante sem mecanismo de garantia é uma especificação incompleta (Seção 1).

**Lacuna 3 — Escala além de um único repositório físico.** SNPA assume `apps/<app>/src/` como código residente dentro do workspace do produto. Produtos reais frequentemente exigem que cada `app` viva em seu próprio repositório (times distintos, pipelines de CI/CD distintos, controle de acesso distinto). O método não define como o isolamento por workspace (Seção 2) coexiste com múltiplos repositórios de código — hoje, a única leitura possível é "SNPA não escala para esse caso", o que não é declarado em lugar nenhum.

---

## 4. Protocolo: Autonomous Development Protocol (ADP v0.3.0)

A Subseção 4.1 permanece como em v0.2.7. A Subseção 4.2 (Ciclo de Features, Épicos e `index.md`) também permanece como em v0.2.7, com uma adição em 4.2.1. As demais mudanças começam em 4.3.

### 4.2.1. Direcionamento de Planejamento: Fatiamento Vertical (Recomendação Opcional)

Ao decompor uma feature em épicos, e um épico em tarefas atômicas (`tasks.md`), a forma como o trabalho é fatiado determina quando o usuário passa a receber valor real — e, por consequência, quando o time começa de fato a aprender com o uso real (Seção 4.1).

* **Fatiamento Horizontal:** organiza o trabalho por camada técnica — primeiro todo o modelo de dados, depois toda a API, depois toda a interface. O produto só entrega valor observável quando todas as camadas convergem, adiando a validação de hipóteses e o aprendizado contínuo.
* **Fatiamento Vertical (recomendação padrão do método):** cada épico — e, sempre que possível, cada tarefa em `tasks.md` — atravessa todas as camadas necessárias (dado, domínio, API, interface) para entregar, ainda que de forma mínima, um incremento de valor tangível para o usuário desde o primeiro épico, o momento zero. Cada fatia vertical já é, por si só, uma oportunidade real de validar hipótese, aprender e pivotar — reforçando diretamente o pilar de Incremental Feature Discovery.

**Caráter opcional:** este é um direcionamento recomendado, não uma invariante do método. O time (Tech Lead / FDE, no Readiness Gate) pode optar por outra estratégia de fatiamento quando o contexto técnico ou de negócio justificar — por exemplo, uma migração de infraestrutura ou uma reescrita de camada de dados que não possui, por natureza, valor perceptível fatiável verticalmente. Quando o time optar por não seguir o fatiamento vertical, essa decisão e sua justificativa devem ser registradas em `plan.md` ou `epic_roadmap.md`, preservando a documentação como fonte da verdade também sobre as escolhas de planejamento.

### 4.3. Máquina de Estados do Épico

`quick_status.md`, no nível de épico, declara exatamente um destes estados — nenhum outro valor é válido:

```text
Draft → Ready → WIP → Done
  ↑        ↓      ↓
  └──── Blocked  Stale
           │        │
           └───→ (retorna a Ready após resolução)
```

- **`Draft`** — em modelagem no Upstream; `plan.md` ainda não submetido ao Readiness Gate.
- **`Ready`** — aprovado no Readiness Gate; elegível para execução Downstream.
- **`WIP`** — em execução por um motor autônomo.
- **`Blocked`** — execução interrompida por dependência externa ou defeito descoberto; retorna a `Ready` quando o bloqueio é removido, não avança sozinho.
- **`Done`** — código em `apps/` corresponde ao `plan.md` vigente no momento da entrega.
- **`Stale`** — estado novo em v0.3.0 (ver 4.4). Um épico `Done` cujo `plan.md` foi alterado após a entrega transiciona automaticamente para `Stale`. Só um novo ciclo de Readiness Gate devolve o épico a `Ready`.

Transições são escritas exclusivamente por quem executa a ação que as causa (Tandem move `Draft → Ready` via Gate; motor autônomo move `Ready → WIP → Done`; qualquer mudança em `plan.md` move `Done → Stale` automaticamente). Isso resolve a Lacuna 2: o protocolo agora é implementável por um agente sem interpretação.

### 4.4. Protocolo de Deriva de Especificação (Spec Drift)

**Regra:** nenhum commit em `plan.md` de um épico em estado `Done` é silencioso.

Ao detectar uma alteração em `plan.md` cujo épico está `Done`, o estado transiciona para `Stale` e o épico reentra na fila do Readiness Gate — não na fila do Upstream, porque o modelo já foi revalidado uma vez; o que precisa de revalidação agora é a *diferença* entre o modelo antigo e o novo, não o modelo inteiro.

O Tech Lead, no Readiness Gate, avalia a diferença e decide entre duas ações, registradas em `epic_roadmap.md`:

- **Re-execução** — a mudança afeta comportamento já implementado; o épico volta a `Ready` e um novo ciclo Downstream regenera as partes afetadas de `apps/`.
- **Aceitação de deriva documentada** — a mudança é cosmética ou não afeta o comportamento implementado; o Tech Lead marca o épico `Done` novamente, registrando explicitamente por que a divergência entre `plan.md` e `apps/` é aceitável.

Isso resolve a Lacuna 1: "documentação como fonte única da verdade" deixa de ser uma afirmação aspiracional e passa a ser uma propriedade que o protocolo ativamente mantém ou declara violada — nunca deixa a violação implícita.

### 4.5. Aplicações Multi-Repositório

Quando um `app` em `apps/` reside em um repositório físico separado do workspace do produto, `app_manifest.md` permanece dentro de `apps/<app>/` — a especificação nunca sai do workspace isolado — mas o código-fonte é substituído por um ponteiro:

```text
apps/
└── api-core/
    ├── app_manifest.md      # Permanece no workspace do produto
    └── repo_pointer.md      # Novo em v0.3.0: URL do repositório, branch de integração, commit de referência
```

`repo_pointer.md` contém apenas metadados de localização — nunca código. O motor autônomo, ao executar Downstream para um épico associado a esse app, escreve no repositório externo referenciado, mas o estado (`quick_status.md`) e a especificação (`plan.md`, `app_manifest.md`) continuam vivendo, sem exceção, dentro do workspace isolado do produto (Seção 2). Isso resolve a Lacuna 3 sem enfraquecer o princípio de isolamento: o que se distribui é a *compilação*, nunca a *especificação*.

---

## Trade-offs Assumidos em v0.3.0

- **Complexidade de estado.** Seis estados formais substituem quatro estados informais. O custo é mais superfície de protocolo para o Tech Lead auditar; o ganho é que um agente pode implementar a máquina de estados sem ambiguidade — trade-off aceito porque a alternativa (estados implícitos) já se provou insuficiente na Lacuna 2.
- **`Stale` cria trabalho de revisão obrigatório.** Toda edição de `plan.md` pós-entrega agora força uma passagem pelo Readiness Gate, mesmo quando a mudança é trivial. Isso é deliberado: o custo de uma revisão desnecessária é menor que o custo de uma deriva não detectada entre especificação e código em produção.
- **`repo_pointer.md` introduz uma segunda fonte de verdade para localização de código.** O ponteiro pode ficar desatualizado se o repositório for migrado sem atualizar o manifesto. v0.3.0 aceita esse risco porque a alternativa — embutir código de múltiplos repositórios dentro do workspace do produto — quebra o isolamento que é o princípio fundacional da Seção 2. Um mecanismo de verificação automática do ponteiro fica fora do escopo desta versão.

---

## O Que Não Mudou (Escopo Explicitamente Fora de v0.3.0)

- Seções 0, 1, 2, 3 e 5 permanecem como na revisão de v0.2.7.
- O modelo Tandem e EventStorming no Upstream não são alterados.
- Nenhuma mudança na estrutura de diretórios de `features/` ou `epics/` — 4.2.1 é uma recomendação sobre como decompor o conteúdo de um épico, não sobre onde ele é armazenado.

Isso é intencional: v0.3.0 resolve lacunas mecânicas do protocolo de execução e torna explícito, em 4.2.1, um direcionamento de planejamento que já era implícito no pilar de Incremental Feature Discovery — não revisita decisões de modelagem de domínio já validadas em versões anteriores.
