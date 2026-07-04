from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PROCESSED = ROOT / 'data' / 'processed'

def main():
    DOCS.mkdir(exist_ok=True)
    gaps = pd.read_csv(PROCESSED / 'consultant_gap_log.csv') if (PROCESSED / 'consultant_gap_log.csv').exists() else pd.DataFrame()
    critical = int(gaps['severity'].eq('critical').sum()) if 'severity' in gaps else 0
    high = int(gaps['severity'].eq('high').sum()) if 'severity' in gaps else 0
    text = f'''# AI Consultant Analysis

## Veredito executivo

A IA Consultora rule-based indica que o forecast deve ser tratado como um sistema de risco e governança, não como um número isolado. A acurácia agregada de 84,9% é positiva, mas a qualidade da cobertura exige atenção: Pipeline Coverage de 1,94x, Commit Coverage de 45,4%, Best Case Dependency de 38,0%, 46 oportunidades paradas há mais de 20 dias, 55,9% dos deals abertos sem atividade recente e Close Date Push Rate de 60,8%.

Foram identificados {critical} gaps críticos e {high} gaps altos. A análise não confirma causa raiz; ela organiza hipóteses para validação humana.

## Leitura da operação

A evidência disponível aponta para um problema mais ligado à qualidade da cobertura e à governança do pipeline do que apenas ao volume total. O pipeline aberto é material, mas parte dele depende de Best Case, oportunidades paradas, deals sem atividade recente e close dates empurradas.

## Principais gaps identificados

- Baixa cobertura de Commit: 45,4% versus referência de 60,0%.
- Dependência de Best Case: 38,0% do pipeline aberto.
- Pipeline Coverage insuficiente: 1,94x versus referência de 2,50x.
- 46 oportunidades abertas paradas há mais de 20 dias.
- 55,9% dos deals abertos sem atividade recente.
- 13 oportunidades em Commit sem atividade recente.
- 6 oportunidades abertas sem próxima atividade registrada.
- Close Date Push Rate de 60,8%.
- 92 deals de alto valor com risk flags ativos.

## Hipóteses prováveis

- Os dados sugerem que parte da cobertura pode depender de oportunidades com previsibilidade menor do que a categoria de forecast indica.
- Há indícios de pipeline inflado por deals parados ou sem atividade recente.
- Hipótese provável: parte do Commit precisa de evidência operacional mais clara.
- A evidência disponível aponta para risco de slippage, especialmente onde close dates foram empurradas repetidamente.

## Evidências observadas

- Forecast Submitted de R$ 2.412.146,00 versus Closed Won de R$ 2.048.000,00.
- Diferença entre Forecast Submitted e Closed Won de R$ 364.146,00.
- Weighted Forecast de R$ 6.432.550,00.
- Commit Coverage de 45,4%.
- Best Case Dependency de 38,0%.
- Pipeline Coverage de 1,94x.
- Stuck Opportunities: 46.
- Activity Gap Rate: 55,9%.
- Commit sem atividade recente: 13.
- Close Date Push Rate: 60,8%.
- Deals de alto valor com risco ativo: 92.

## Evidências ausentes

- Motivo de push de close date.
- Qualidade real das próximas ações.
- Histórico completo de interações comerciais.
- Feedback do comprador.
- Concorrência envolvida.
- Critério real usado para classificar Commit.
- Inspeção da forecast call.
- Notas dos AEs e managers.
- Status de procurement e legal.
- Existência de champion.
- Etapa real do processo de compra.

## Perguntas de validação

- Head de Sales: quais deals sustentam o compromisso do período sem depender de Best Case?
- Head de RevOps: o critério de Commit é auditável e aplicado da mesma forma por todos os managers?
- Sales Ops: quais oportunidades tiveram push de close date e qual reason code explica cada movimento?
- Sales Managers: quais deals parados ainda têm próxima etapa validada pelo comprador?
- AEs: qual é a próxima ação datada para cada oportunidade em Commit?
- Finance/FP&A: a leitura de forecast operacional está alinhada ao reconhecimento esperado de receita?

## Recomendações priorizadas

### Fazer agora

1. Head de RevOps: revisar critérios de Commit antes da próxima forecast call. Métrica: Commit Coverage e Forecast Accuracy.
2. Head de Sales: inspecionar maiores Best Case e exigir plano de conversão para Commit. Métrica: Best Case Dependency.
3. CRO: conduzir deal review executivo para deals de alto valor com risco ativo. Métrica: High Value Deals at Risk.
4. Sales Managers: exigir próxima ação datada para Commit e estágios avançados. Métrica: Activity Gap Rate e Commit Without Activity.

### Fazer depois

1. Sales Ops: implementar reason code obrigatório para close date push. Métrica: Close Date Push Rate. Prazo sugerido: 30 dias.
2. RevOps Analytics: criar visão de pipeline novo versus pipeline reciclado. Métrica: Old Pipeline Share. Prazo sugerido: 45 dias.
3. Sales Managers: criar rotina quinzenal de coaching para AEs com maior variação de forecast. Métrica: Forecast Accuracy by AE.

### Monitorar

- Evolução semanal de Commit Coverage.
- Redução de Best Case Dependency.
- Oportunidades paradas por mais de 20 dias.
- Deals em Commit sem atividade recente.
- Close Date Push Rate por AE e manager.
- Conversão dos top deals com risk flags.

## Riscos de decisão

Decidir apenas por pipeline nominal pode mascarar baixa qualidade de cobertura, deals sem próxima ação, close dates pouco confiáveis e concentração de risco em oportunidades grandes.

## Conclusão executiva

A IA Consultora é rule-based e não afirma causa raiz. A liderança deve auditar Commit, qualificar Best Case, limpar pipeline parado e priorizar deals de alto valor com risco ativo para melhorar previsibilidade de receita.
'''
    (DOCS / 'ai_consultant_analysis.md').write_text(text, encoding='utf-8')
    print(f'AI consultant analysis generated at {DOCS / "ai_consultant_analysis.md"}')

if __name__ == '__main__':
    main()
