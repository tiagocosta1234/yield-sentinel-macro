# Macro Trading Lab

Este repositório é um laboratório pessoal dedicado à exploração de modelos macroeconómicos, análise quantitativa e desenvolvimento de algoritmos de trading utilizando Python.

## Estrutura do Repositório

O laboratório está organizado nos seguintes módulos principais:

## 1. Backtesting de Médias Móveis (Nasdaq Futures)
Simuladores quantitativos focados em contratos de futuros do Nasdaq-100 (**MNQ=F**).

*   **SMA Strategy (`sma_backtest.py`)**: Implementação clássica de cruzamento de Médias Móveis Simples (10/30). Serve como o ponto de partida e *benchmark* do laboratório.
*   **EMA Strategy (`ema_backtest.py`)**: Evolução técnica utilizando Médias Móveis Exponenciais (10/30). Esta versão reage mais rapidamente aos pivôs de preço, reduzindo o *lag* inerente às médias simples.
*   **Volatility Adjusted Strategy (`volat_adjusted_backtest.py`)**: O modelo mais avançado do laboratório. Utiliza uma arquitetura vectorizada para processar dados de 2020-2026 e implementa **Volatility Equalization**. O tamanho da posição é ajustado dinamicamente via ATR, garantindo que o risco em dólares é constante independentemente da volatilidade do mercado.
*   **Diferenciação na Gestão de Risco**: 
    *   Nas estratégias iniciais (**SMA/EMA**), a gestão é estática, operando com **5 contratos Micro fixos** e um limite de perda diária de 4%.
    *   No **Volatility Adjusted Strategy**, a gestão é **dinâmica e baseada em risco nominal**: o sistema calcula o número de contratos com base na volatilidade atual (ATR), arriscando um valor fixo (ex: $4,000) por unidade de desvio. Isto permite que a estratégia reduza a exposição em mercados "selvagens" e a aumente em mercados de tendência clara, otimizando o rácio de Sharpe.

### 2. Sentinelas de Mercado
Ferramentas de monitorização em tempo real para diferentes classes de ativos.

*   **Main Dashboard (`main_dashboard.py`)**: Visualizador de indicadores macro como o **Yield Curve Spread (10Y-3M)** e o rácio de stress de crédito **LQD/TLT**.
*   **Yield Sentinel (`yield_sentinel.py`)**: Focado especificamente na análise detalhada das curvas de juros e o seu impacto no custo de capital.
*   **Euro Sentinel (`euro_sentinel.py`)**: Monitorização do par **EUR/USD**, analisando a força relativa da moeda europeia face ao dólar.

## Tecnologias Utilizadas

*   **Python 3.x**
*   **Pandas & NumPy**: Processamento de dados e lógica de sinais.
*   **YFinance**: Extração de dados do Yahoo Finance.
*   **Matplotlib**: Motor gráfico para visualização técnica.

## Como Executar

1. Clonar o repositório:
   ```bash
   git clone [https://github.com/tiagocosta1234/macro-trading-lab.git](https://github.com/tiagocosta1234/macro-trading-lab.git)