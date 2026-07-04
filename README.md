# Forecast Accuracy & Pipeline Risk System

Case de portfólio em RevOps Analytics para Forecast Governance, Pipeline Risk e previsibilidade de receita em uma operação SaaS B2B sintética.

## Executive Summary

Os dados sugerem que o forecast tem uma acurácia agregada razoável, mas a cobertura comercial ainda exige governança ativa. A acurácia agregada ficou em **84,9%**, com **Forecast Submitted de R$ 2.412.146,00** contra **Closed Won de R$ 2.048.000,00**, gerando uma diferença de **R$ 364.146,00**. Ao mesmo tempo, o **Weighted Forecast é de R$ 6.432.550,00**, o que indica que a leitura executiva precisa separar pipeline ponderado, forecast submetido e receita efetivamente realizada.

O risco principal não está apenas no volume de pipeline. A evidência disponível aponta para qualidade de cobertura: **Pipeline Coverage de 1,94x**, **Commit Coverage de 45,4%**, **Best Case Dependency de 38,0%**, **46 oportunidades paradas há mais de 20 dias**, **55,9% dos deals abertos sem atividade recente**, **13 oportunidades em Commit sem atividade recente**, **6 oportunidades abertas sem próxima atividade registrada**, **Close Date Push Rate de 60,8%** e **92 deals de alto valor com risk flags ativos**.

A leitura executiva é direta: o pipeline nominal não deve ser tratado como pipeline confiável sem inspeção de Commit, Best Case, aging, atividade recente e concentração de risco. RevOps deve transformar o forecast em processo de governança, não apenas em número reportado.

## Problema de negócio

Lideranças comerciais precisam responder, antes do fechamento do período, se o forecast é confiável, se a meta está coberta por Commit real, se existe dependência excessiva de Best Case, quais oportunidades estão paradas e onde o pipeline pode estar inflado.

## Por que Forecast Governance importa para RevOps e Sales Ops

Forecast Governance reduz surpresa de fechamento, qualifica a cobertura de meta e cria disciplina operacional entre AEs, managers, RevOps, Sales Ops e Finance/FP&A. O objetivo não é apenas mostrar gráficos: é apoiar decisões sobre forecast call, deal review, criação de pipeline, higiene de close date e coaching por AE.

## Objetivo do projeto

Criar um sistema analítico rule-based que mede acurácia de forecast, compara forecast versus realizado, identifica riscos de pipeline, prioriza gaps comerciais e gera recomendações executivas sem usar dados reais, APIs externas ou ML.

## Visão geral da solução

- Dados sintéticos de dois trimestres de operação SaaS B2B.
- Métricas de forecast, quota, pipeline coverage, aging, atividade e risco.
- Consultor de Gaps rule-based com evidência, hipótese provável, evidência ausente, pergunta de validação e ação recomendada.
- IA Consultora rule-based para leitura executiva em português do Brasil.
- Dashboard Streamlit com páginas executivas para RevOps, Sales Ops e liderança comercial.

## Arquitetura do projeto

```text
app/                    Dashboard Streamlit
data/processed/         CSVs sintéticos e artefatos analíticos
data/database/          SQLite do case
docs/                   Documentação executiva e técnica
slides/                 Roteiro de apresentação executiva
src/                    Geração de dados, métricas, consultor e relatórios
tests/                  Testes básicos de métricas, dados e consultor
```

## Dados sintéticos

As entidades incluem `opportunities`, `accounts`, `aes`, `sales_stages`, `forecast_snapshots`, `quota_targets`, `deal_activity`, `stage_history`, `close_outcomes` e `risk_flags`. Os dados foram desenhados para simular cenários reais de governança: AE otimista, baixa cobertura de Commit, dependência de Best Case, deals parados, close dates empurradas e deals grandes com risco ativo.

## Principais módulos

- `src/generate_data.py`: gera CSVs sintéticos e SQLite.
- `src/metrics.py`: calcula métricas de Forecast Governance e Pipeline Risk.
- `src/consultant_gap_finder.py`: detecta gaps rule-based e gera `consultant_gap_log.csv`.
- `src/ai_consultant.py`: gera análise consultiva baseada nos gaps.
- `src/data_quality.py`: valida arquivos, colunas, IDs, domínios e valores monetários.
- `app/streamlit_app.py`: dashboard executivo em Streamlit.

## Principais métricas

- Forecast Accuracy: 84,9%.
- Forecast Submitted: R$ 2.412.146,00.
- Closed Won: R$ 2.048.000,00.
- Diferença Submitted vs Closed Won: R$ 364.146,00.
- Weighted Forecast: R$ 6.432.550,00.
- Pipeline Coverage: 1,94x.
- Commit Coverage: 45,4%.
- Best Case Dependency: 38,0%.
- Stuck Opportunities: 46.
- Activity Gap Rate: 55,9%.
- Commit sem atividade recente: 13.
- Oportunidades abertas sem próxima atividade: 6.
- Close Date Push Rate: 60,8%.
- Deals de alto valor com risco ativo: 92.

## Principais gaps encontrados

- Baixa cobertura de Commit: 45,4% versus referência de 60,0%.
- Dependência de Best Case: 38,0% do pipeline aberto.
- Pipeline Coverage insuficiente: 1,94x versus referência de 2,50x.
- 46 oportunidades paradas há mais de 20 dias.
- 55,9% dos deals abertos sem atividade recente.
- 13 oportunidades em Commit sem atividade recente.
- Close Date Push Rate de 60,8%.
- 92 deals de alto valor com risk flags ativos.

## Decisões recomendadas

- Revisar critérios de Commit antes da próxima forecast call.
- Qualificar os maiores Best Case e definir plano de conversão para Commit.
- Executar limpeza de pipeline parado e requalificar oportunidades antigas.
- Exigir próxima atividade datada para Commit e estágios avançados.
- Criar reason code obrigatório para close date push.
- Realizar deal review executivo para deals de alto valor com risco ativo.
- Fazer coaching por AE com base em variação entre submitted forecast e closed won.

## Consultor de Gaps

O Consultor de Gaps é rule-based e prioriza qualidade de decisão. Cada gap contém `gap_id`, área, métrica, valor atual, valor esperado, severidade, evidência observada, hipótese provável, evidência ausente, perguntas de validação, ação recomendada, responsável, urgência, impacto esperado, métrica de acompanhamento e status.

## IA Consultora rule-based

A IA Consultora lê `consultant_gap_log.csv` e gera uma análise executiva com veredito, leitura da operação, gaps, hipóteses, evidências ausentes, perguntas de validação, recomendações priorizadas e riscos de decisão. Ela não confirma causa raiz; ela organiza hipóteses para validação humana.

## Limitações

- Dados 100% sintéticos.
- Sem APIs externas.
- Sem ML nesta versão.
- Métricas e recomendações são rule-based.
- A análise gera hipóteses, não prova causa raiz.
- Em produção, seria necessário integrar CRM, Sales Engagement, Billing e Finance/FP&A.

## Como rodar localmente

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/consultant_gap_finder.py
python src/ai_consultant.py
python src/data_quality.py
python src/reports.py
python -m compileall src app
python -m pytest
streamlit run app/streamlit_app.py
```

## Stack utilizada

Python, pandas, numpy, SQLite, Streamlit, Plotly e pytest.

## Repository Description

Forecast Accuracy and Pipeline Risk System for RevOps and Sales Ops, using synthetic B2B SaaS data to analyze forecast reliability, pipeline coverage, deal risk, commit quality and revenue governance.

Suggested topics: `revops`, `sales-ops`, `revenue-operations`, `forecasting`, `pipeline-management`, `forecast-accuracy`, `pipeline-risk`, `sales-analytics`, `streamlit`, `python`, `data-analytics`, `saas`, `b2b`, `portfolio-project`.

## Próximos passos

- Integrar fontes reais de CRM, Sales Engagement, Billing e Finance/FP&A.
- Adicionar reason codes reais para close date push.
- Criar coortes de pipeline novo versus reciclado.
- Adicionar workflow humano para deal review e forecast call.
- Versionar critérios de Commit e auditar mudanças por período.

## Dashboard Preview
O dashboard Streamlit fica em `app/streamlit_app.py`. Screenshots devem ser adicionados em `docs/screenshots/` antes da divulgação pública.

## Data Disclaimer
Todos os dados são sintéticos. O projeto não usa APIs externas nem dados reais. As análises são rule-based e devem ser tratadas como hipóteses para validação, não como causa raiz confirmada.

## Consulting Use Case
Este case pode ser usado como base para diagnóstico RevOps em SaaS B2B, apoiando liderança com evidências, hipóteses, perguntas de validação, responsáveis e métricas de acompanhamento.

## Contact
LinkedIn: https://www.linkedin.com/in/gustavo-worliczek-lazzarotto/  
E-mail: gustavo.lazzaro77o@gmail.com

