# Pipeline ETL — Ações da B3 

Pipeline de dados completo para coleta, transformação e armazenamento de dados históricos de ações da bolsa brasileira (B3).

##  Objetivo

Construir um pipeline ETL do zero com dados reais, aplicando boas práticas de engenharia de dados em um contexto financeiro brasileiro.

##  Stack

- **Python** — orquestração do pipeline
- **Pandas** — transformação e análise dos dados
- **yfinance** — coleta automática de dados da B3
- **SQLite** — armazenamento estruturado

##  O que o pipeline faz

**Extract** — coleta dados históricos de 2024 das ações BBDC4, ITUB4 e PETR4 via API

**Transform** — calcula retorno diário (%), média móvel de 20 dias e identifica os melhores e piores dias de cada ativo

**Load** — carrega os dados transformados em banco SQL com 3 tabelas: `precos`, `retornos` e `media_movel`

##  Insights encontrados nos dados de 2024

| Ação | Melhor dia | Pior dia |
|------|-----------|---------|
| BBDC4 | +7.59% (05/08) | -15.90% (07/02) |
| ITUB4 | +4.29% (06/02) | -3.60% (28/11) |
| PETR4 | +7.26% (26/08) | -9.14% (08/03) |

##  Arquivos

- `etl.py` — pipeline completo
- `precos.csv` — preços de fechamento diários
- `retorno_diario.csv` — retorno percentual diário
- `media_movel_20.csv` — média móvel de 20 dias

##  Como executar

```bash
pip install yfinance pandas
python etl.py
```

##  Autora

**Samara Hellen** — Engenharia de Computação | PUC Minas

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Samara_Hellen-blue)](https://linkedin.com/in/samarahellen)
