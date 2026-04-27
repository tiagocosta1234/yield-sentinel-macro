# Yield Sentinel - Macro Monitor

Este repositório contém um conjunto de ferramentas em Python para monitorizar indicadores macroeconómicos críticos. O projeto foca-se na análise de taxas de juro e risco de crédito, transformando dados financeiros em sinais visuais de alerta.

## Estrutura do Projeto

O monitor está dividido em dois módulos principais:

### 1. `yield_sentinel.py` (O Pulso da Recessão)
Focado no mercado de dívida soberana dos EUA.
- **Indicador:** Spread entre as taxas de 10 anos e 2 anos (^TNX - ^IRX).
- **Objetivo:** Detetar a **Inversão da Curva de Rendimentos**. Historicamente, quando este valor fica abaixo de zero, sinaliza uma recessão económica iminente.

### 2. `euro_sentinel.py` (O Nervo do Risco Global)
Focado no sentimento de risco do mercado (Credit Stress).
- **Indicador:** Rácio entre Corporate Bonds (LQD) e Treasury Bonds (TLT).
- **Objetivo:** Medir o apetite pelo risco.
  - **Rácio a subir:** Confiança na economia (Risk-on).
  - **Rácio a cair:** Fuga para ativos seguros (Risk-off/Stress financeiro).

---

## Como Utilizar

1. **Instalar dependências:**
   ```bash
   pip install yfinance pandas matplotlib