# Yield Sentinel - Macro Monitor

Um conjunto de ferramentas em Python para monitorizar a saúde da economia global através da análise de curvas de rendimento e spreads de crédito.

## Estrutura do Projeto

### 1. `yield_sentinel.py` (Curva de Rendimento 10Y-5Y)
- **Indicador:** Spread entre as taxas de 10 e 5 anos dos EUA (`^TNX` - `^FVX`).
- **Tese:** Monitoriza a inclinação da curva. Embora o spread 10Y-2Y seja o mais volátil, o 10Y-5Y oferece uma visão mais estável da tendência de longo prazo.

### 2. `euro_sentinel.py` (Risco de Crédito Global)
- **Indicador:** Rácio de preço entre LQD (Corporate Bonds) e TLT (Treasury Bonds).
- **Tese:** Mede o apetite pelo risco. Se o rácio sobe, o mercado está "Risk-On".

### 3. `main_dashboard.py` (Painel Consolidado)
- Combina a visualização do spread 10Y-3M e do rácio de crédito lado a lado para análise de correlação em tempo real.

## Como Executar
```bash
pip install yfinance pandas matplotlib
python main_dashboard.py