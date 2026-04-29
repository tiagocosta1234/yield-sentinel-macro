# Macro Trading Lab

Este repositório é um laboratório pessoal dedicado à exploração de modelos macroeconómicos, análise quantitativa e desenvolvimento de algoritmos de trading utilizando Python.

## Estrutura do Repositório

O laboratório está organizado nos seguintes módulos principais:

### 1. SMA Backtest (Nasdaq Futures)
Simulador quantitativo focado em contratos de futuros do Nasdaq-100.
*   **Ficheiro**: `sma_backtest.py`
*   **Estratégia**: Cruzamento de Médias Móveis (10/30) aplicado a **5 contratos Micro (MNQ=F)**.
*   **Gestão de Risco**: Implementação de um **Daily Loss Limit de 4%** e cálculo de exposição nocional/alavancagem.
*   **Métricas**: Comparação direta de performance contra a estratégia de *Buy & Hold*.

### 2. Main Dashboard (Macro Indicators)
Interface de monitorização de sentimento de mercado e stress financeiro.
*   **Ficheiro**: `main_dashboard.py`
*   **Yield Curve Monitor**: Spread 10Y-3M dos EUA (^TNX - ^IRX).
*   **Credit Stress Tracker**: Rácio LQD/TLT para avaliar apetite pelo risco global.

### 3. Euro Sentinel
Módulo dedicado à análise do par de moedas EUR/USD e indicadores da Zona Euro.
*   **Ficheiro**: `euro_sentinel.py`
*   **Objetivo**: Monitorizar a força relativa do Euro e diferenciais de taxas de juro.

## Tecnologias Utilizadas

*   **Python 3.x**: Linguagem principal.
*   **Pandas & NumPy**: Processamento de dados e lógica vetorial de sinais.
*   **YFinance**: Extração de dados históricos e em tempo real.
*   **Matplotlib**: Visualização de performance e dashboards técnicos.

## Como Executar

1. Clonar o repositório:
   ```bash
   git clone [https://github.com/tiagocosta1234/macro-trading-lab.git](https://github.com/tiagocosta1234/macro-trading-lab.git)