# Análise Executiva

## Veredito executivo

Os dados sugerem que o forecast atual é parcialmente confiável no agregado, mas ainda não está maduro como processo de governança. A acurácia agregada ficou em 84,9%, com Forecast Submitted de R$ 2.412.146,00 contra Closed Won de R$ 2.048.000,00. A diferença de R$ 364.146,00 não é o único sinal relevante: a evidência disponível aponta para baixa cobertura de Commit, dependência de Best Case, pipeline parado, atividade comercial insuficiente e close dates empurradas.

## Diagnóstico do período

O forecast parece razoável quando visto pela acurácia agregada, mas a governança por trás do número exige revisão. Há indícios de que a operação combina três riscos: qualidade de cobertura, disciplina de execução dos deals e higiene de forecast.

A meta não parece suficientemente coberta por Commit. A operação depende de Best Case em nível relevante, possui 46 oportunidades paradas há mais de 20 dias e apresenta 55,9% dos deals abertos sem atividade recente. Além disso, 13 oportunidades em Commit estão sem atividade recente e 6 oportunidades abertas não têm próxima atividade registrada.

## Resumo de métricas

| Métrica | Valor observado | Leitura executiva |
|---|---:|---|
| Forecast Accuracy | 84,9% | Boa leitura agregada, mas precisa ser analisada por qualidade de cobertura. |
| Forecast Submitted | R$ 2.412.146,00 | Número declarado pela operação no snapshot mais recente. |
| Closed Won | R$ 2.048.000,00 | Realizado usado para comparação com forecast. |
| Diferença Submitted vs Closed Won | R$ 364.146,00 | Indício de variação que deve ser acompanhado por AE e mês. |
| Weighted Forecast | R$ 6.432.550,00 | Pipeline ponderado acima do submitted; requer leitura por mês e categoria. |
| Pipeline Coverage | 1,94x | Abaixo da referência de 2,50x. |
| Commit Coverage | 45,4% | Abaixo da referência de 60,0%. |
| Best Case Dependency | 38,0% | Acima do limite desejado de 35,0%. |
| Stuck Opportunities | 46 | Volume relevante de deals parados. |
| Activity Gap Rate | 55,9% | Sinal forte de baixa cadência em oportunidades abertas. |
| Commit sem atividade recente | 13 | Risco direto de qualidade do Commit. |
| Close Date Push Rate | 60,8% | Indício de baixa higiene de close date. |
| Deals de alto valor com risco ativo | 92 | Requer deal review executivo e priorização. |

## Principais achados

1. O forecast parece razoável no agregado, mas não deve ser tratado como plenamente confiável sem auditoria de Commit e Best Case.
2. A meta não está suficientemente coberta por Commit: a cobertura observada é 45,4% versus referência de 60,0%.
3. Há dependência relevante de Best Case: 38,0% do pipeline aberto.
4. Existe risco de pipeline inflado: 46 oportunidades estão paradas há mais de 20 dias.
5. A disciplina de próxima ação precisa de revisão: 55,9% dos deals abertos estão sem atividade recente e 13 Commit estão sem atividade recente.
6. A higiene de close date é um risco de previsibilidade: 60,8% das oportunidades tiveram push.
7. AEs com maior variação média de forecast exigem revisão: ae_006, ae_004, ae_002 e ae_001 aparecem com maior variação média entre submitted forecast e closed won.
8. Há concentração operacional em deals de alto valor com risco ativo: 92 oportunidades de alto valor possuem risk flags.

## Riscos operacionais

- Decidir por pipeline nominal e ignorar qualidade de cobertura.
- Tratar Best Case como compromisso de receita.
- Manter oportunidades paradas como se ainda representassem pipeline confiável.
- Permitir Commit sem atividade recente ou sem próxima ação validada.
- Aceitar close date push sem reason code e sem revisão de manager.
- Subestimar risco de concentração em deals grandes com flags ativos.

## Impacto potencial em receita e previsibilidade

A evidência disponível sugere risco de surpresa negativa no fechamento caso a liderança use apenas pipeline nominal como proxy de cobertura. Baixa cobertura de Commit, dependência de Best Case e gaps de atividade podem reduzir conversão esperada, aumentar slippage e enfraquecer a confiança de Finance/FP&A no forecast comercial.

## Recomendações priorizadas

| Prioridade | Responsável | Ação | Métrica impactada | Métrica de acompanhamento | Prazo sugerido | Impacto esperado |
|---|---|---|---|---|---|---|
| 1 | Head de RevOps | Recalibrar critérios de Commit e exigir evidência mínima por deal. | Commit Coverage | Commit Coverage e Forecast Accuracy | Próxima forecast call | Aumentar confiabilidade do forecast. |
| 2 | Head de Sales | Revisar maiores Best Case e definir plano de conversão para Commit. | Best Case Dependency | Best Case Dependency | 5 dias úteis | Reduzir dependência de upside incerto. |
| 3 | Sales Ops Manager | Limpar ou requalificar oportunidades paradas há mais de 20 dias. | Stuck Opportunities | Stuck Opportunities e Old Pipeline Share | 10 dias úteis | Reduzir pipeline inflado. |
| 4 | Sales Managers | Exigir próxima ação datada para Commit e estágios avançados. | Activity Gap Rate | Commit Without Activity | Próxima semana | Melhorar execução dos deals. |
| 5 | Sales Ops | Implementar reason code para close date push. | Close Date Push Rate | Close Date Push Rate | 30 dias | Melhorar higiene de forecast. |
| 6 | CRO | Conduzir deal review executivo para deals de alto valor com risco ativo. | High Value Deals at Risk | Risk Flag Count | 5 dias úteis | Reduzir risco material de receita. |
| 7 | Sales Managers | Fazer coaching com AEs de maior variação de forecast. | Forecast Accuracy by AE | Forecast Variance by AE | Quinzenal | Reduzir viés de forecast por AE. |

## Limitações

Os dados são sintéticos e a análise é rule-based. O projeto não usa ML, APIs externas ou dados reais. As conclusões devem ser lidas como hipóteses operacionais para validação em forecast call, deal review, inspeção de CRM e alinhamento com Finance/FP&A.

## Conclusão executiva

A decisão recomendada é tratar forecast como processo de governança de receita. A liderança deve auditar Commit, qualificar Best Case, limpar pipeline parado, exigir próxima ação e revisar top deals em risco.
