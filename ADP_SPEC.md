# Autonomous Development Protocol (ADP)

## 1. Visão Geral
O **Autonomous Development Protocol (ADP)** é o protocolo operacional que rege o fluxo de trabalho do framework **SCPE**.

## 2. Pilares do Protocolo
1. **Incremental Feature Discovery:** Construção iterativa focada na feature mais prioritária do negócio atual, sem cascata exaustiva prévia.
2. **Hierarquia de Features (`index.md` & Épicos SMART):** O uso universal de `index.md` para pontos de entrada em features e épicos.
3. **Pipeline em Onda (Non-Waterfall):**
   - **Upstream:** Definição da feature prioritária e estruturação do `plan.md` com IA como co-piloto.
   - **Readiness Gate:** Validação técnica e marcação como `Ready` pelo FDE/Tech Lead.
   - **Downstream:** Execução iterativa de tarefas atômicas em `tasks.md` gerando código em `apps/` com `app_liquid.md`.
   - **Auditoria:** Rastreio em tempo real via `quick_status.md`.
4. **Máquina de Estados do Épico:** `quick_status.md` declara um de seis estados formais — `Draft → Ready → WIP → Done`, com `Blocked` e `Stale` como desvios controlados — cada transição escrita apenas por quem a executa. Ver especificação completa em [`SCPE_METHOD.md`](SCPE_METHOD.md#44-máquina-de-estados-do-épico).
