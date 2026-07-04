# Metrics Dictionary

Todas as taxas estão em escala 0-1 no código e são exibidas em percentual no dashboard/documentação. `pipeline_coverage` é multiplicador. Valores monetários são exibidos em reais no padrão brasileiro.

| Métrica | Definição | Fórmula | Interpretação | Decisão suportada | Limitação |
|---|---|---|---|---|---|
| total_pipeline | Valor total das oportunidades. | soma de `amount` | Mede volume bruto da base. | Avaliar tamanho total da carteira comercial. | Inclui oportunidades fechadas e não mede qualidade. |
| open_pipeline | Valor das oportunidades abertas. | soma de `amount` em oportunidades abertas | Mostra pipeline nominal disponível. | Avaliar cobertura inicial contra quota. | Pode incluir pipeline antigo ou sem atividade. |
| closed_won_revenue | Receita ganha. | soma de `amount` em `closed_won` | Mede realizado comercial. | Comparar forecast versus resultado. | Depende do período de análise. |
| closed_lost_revenue | Receita perdida. | soma de `amount` em `closed_lost` | Mede perdas fechadas. | Revisar conversão e perdas por etapa. | Não explica motivo da perda. |
| weighted_forecast | Forecast ponderado por probabilidade. | `amount * probability` em oportunidades abertas | Estima cobertura ajustada por etapa. | Comparar pipeline ponderado com quota e submitted forecast. | Probabilidades podem estar mal calibradas. |
| forecast_submitted | Forecast declarado no snapshot mais recente. | soma de `submitted_forecast` no último snapshot | Representa visão declarada pela operação. | Revisar disciplina de forecast e confiança executiva. | Pode refletir viés de AE ou manager. |
| forecast_accuracy | Acurácia entre submitted e realizado. | `1 - abs(submitted - actual) / max(submitted, actual)` | Quanto mais perto de 1, mais confiável. | Calibrar forecast call e coaching por AE. | Acurácia agregada pode esconder problemas por AE. |
| forecast_variance | Diferença entre forecast e realizado. | `submitted - actual` | Positivo sugere forecast acima do realizado. | Identificar viés de otimismo ou conservadorismo. | Não confirma causa raiz. |
| commit_coverage | Cobertura da quota por Commit. | pipeline Commit / quota | Mede quanto da meta está sustentada por deals mais previsíveis. | Avaliar se a meta está coberta por oportunidades com maior evidência. | Depende da qualidade do critério de Commit. |
| best_case_dependency | Participação de Best Case no pipeline aberto. | pipeline Best Case / pipeline aberto | Mede dependência de upside incerto. | Identificar dependência excessiva de oportunidades menos previsíveis. | Best Case pode ser saudável em alguns contextos. |
| pipeline_coverage | Cobertura nominal de pipeline contra quota. | pipeline aberto / quota | Multiplicador de cobertura. | Avaliar suficiência de pipeline contra meta. | Multiplo ideal varia por segmento e win rate. |
| forecast_gap | Diferença entre forecast e quota. | forecast - quota | Mede déficit ou excedente esperado. | Decidir plano de recuperação ou ajuste de expectativa. | Requer alinhamento de período e reconhecimento. |
| quota_attainment | Atingimento de quota. | actual / quota | Mede performance contra meta. | Avaliar entrega comercial e risco de fechamento. | Parcial durante o período. |
| slippage_rate | Proporção de oportunidades com close date empurrada. | deals com `close_date_push_count > 0` / total | Mede risco de higiene de close date. | Revisar disciplina de close date e qualidade do forecast. | Precisa reason code para explicar motivo. |
| stuck_opportunities | Oportunidades paradas. | oportunidades abertas com `days_in_stage > 20` | Sinal de pipeline sem progressão. | Priorizar inspeção de deals parados. | Threshold deve ser calibrado por ciclo de venda. |
| deal_aging | Idade da oportunidade. | data de referência - `created_date` | Mede maturidade do pipeline. | Requalificar ou reciclar pipeline antigo. | Aging alto pode ser normal em Enterprise. |
| stage_conversion_rate | Conversão entre etapas. | média de `converted_to_next_stage` por stage | Mede eficiência do funil. | Revisar gargalos por etapa. | Dados sintéticos simplificam transições. |
| close_date_push_rate | Taxa de push de close date. | oportunidades com push / total | Mede higiene de forecast e slippage. | Revisar close date hygiene e qualidade do forecast. | Não explica o motivo do push. |
| win_rate_by_ae | Win rate por AE. | deals ganhos / deals fechados por AE | Mede conversão por vendedor. | Direcionar coaching e leitura de performance. | Sensível a mix de território e ticket. |
| forecast_accuracy_by_ae | Acurácia por AE e mês. | forecast accuracy agrupada por AE | Mede consistência individual de forecast. | Revisar disciplina de forecast e calibrar confiança por AE. | Amostra pequena pode distorcer leitura. |
| pipeline_by_forecast_category | Pipeline por categoria de forecast. | soma de `amount` por categoria | Mostra mix de Commit, Best Case e Pipeline. | Avaliar dependência de categorias menos previsíveis. | Categoria pode estar desatualizada. |
| pipeline_by_stage | Pipeline por etapa. | soma de `amount` por stage | Mostra distribuição do funil. | Revisar concentração por etapa e maturidade. | Stage pode não refletir etapa real do comprador. |
| risk_flag_count | Quantidade de risk flags ativos. | contagem de flags ativas | Mede volume de sinais de risco. | Priorizar deal review e inspeção operacional. | Flags podem se sobrepor. |
| high_value_deals_at_risk | Deals de alto valor com risk flag. | oportunidades acima do threshold com flag ativa | Mede exposição material. | Reduzir risco de concentração em poucos deals grandes. | Threshold deve ser calibrado por segmento. |
| activity_gap_rate | Deals abertos sem atividade recente. | deals com `days_since_last_activity > 14` / deals abertos | Mede cadência comercial. | Exigir próxima ação e revisar execução. | Atividade registrada não garante qualidade da interação. |
| commit_without_activity | Commit sem atividade recente. | Commit com `days_since_last_activity > 14` | Mede risco de Commit sem evidência operacional. | Auditar Commit antes da forecast call. | Pode haver atividade fora do CRM. |
| old_pipeline_share | Participação de pipeline antigo. | pipeline com aging alto / pipeline aberto | Mede risco de pipeline inflado por oportunidades antigas. | Requalificar ou reciclar pipeline antigo. | Ciclo Enterprise pode exigir thresholds maiores. |
| large_deal_dependency | Dependência dos maiores deals. | top N deals / pipeline aberto | Mede concentração de risco. | Reduzir risco de concentração em poucos deals grandes. | Enterprise pode naturalmente concentrar ticket. |
| weighted_forecast_by_month | Weighted forecast por mês. | `amount * probability` agrupado por mês | Mostra cobertura ponderada temporal. | Avaliar risco mensal de quota. | Depende de close date confiável. |
| forecast_vs_actual_by_month | Forecast versus realizado por mês. | submitted e closed won agrupados por mês | Mede variação temporal do forecast. | Ajustar forecast call e expectativa com Finance/FP&A. | Timing de reconhecimento pode distorcer comparação. |
