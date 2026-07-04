from pathlib import Path
import pandas as pd
import metrics
ROOT=Path(__file__).resolve().parents[1]
PROCESSED=ROOT/'data'/'processed'
OUTPUT=PROCESSED/'consultant_gap_log.csv'
def load_table(name):
 p=PROCESSED/f'{name}.csv'; return pd.read_csv(p) if p.exists() else pd.DataFrame()
def gap(gap_id,area,metric,actual_value,expected_value,severity,evidence,probable_cause,action,owner,follow_up):
 return {'gap_id':gap_id,'area':area,'metric':metric,'actual_value':actual_value,'expected_value':expected_value,'severity':severity,'evidence':evidence,'probable_cause':probable_cause,'missing_evidence':'Faltam notas dos AEs, motivo de push, qualidade do next step, feedback do comprador, concorrencia, criterio real de Commit, inspecao da forecast call, procurement e existencia de champion.','validation_questions':'Quais evidencias sustentam a classificacao atual e o que precisa ser validado com AE, manager, comprador e Finance/FP&A?','recommended_action':action,'owner':owner,'urgency':'immediate' if severity=='critical' else 'this_week' if severity=='high' else 'this_month','expected_impact':'Melhorar previsibilidade, reduzir pipeline inflado e orientar decisao comercial com base em evidencia.','follow_up_metric':follow_up,'status':'open'}
def find_gaps(opportunities,forecast_snapshots,quota_targets,close_outcomes,risk_flags):
 gaps=[]; weighted=metrics.weighted_forecast(opportunities); submitted=metrics.forecast_submitted(forecast_snapshots); quota=float(pd.to_numeric(quota_targets.get('target_amount',pd.Series(dtype=float)),errors='coerce').fillna(0).sum())
 if submitted>weighted*1.25: gaps.append(gap('gap_forecast_inflated','forecast_governance','forecast_submitted_vs_weighted',round(submitted/max(weighted,1),2),'<= 1.25','critical',f'Os dados sugerem forecast submitted {submitted:,.0f} acima do weighted forecast {weighted:,.0f}.','Hipotese provavel: criterios de forecast podem estar aceitando upside como compromisso comercial.','Revisar forecast call por deal e exigir evidencia minima para Commit.','Head de Sales e RevOps','forecast_accuracy'))
 best=metrics.best_case_dependency(opportunities)
 if best>0.35: gaps.append(gap('gap_best_case_dependency','pipeline_quality','best_case_dependency',round(best,3),'<= 0.35','high',f'Ha indicios de dependencia de Best Case: {best:.1%} do pipeline aberto.','Hipotese provavel: cobertura de meta depende de deals ainda sem criterio forte de fechamento.','Criar revisao semanal dos maiores Best Case e plano de conversao para Commit.','Sales Managers','best_case_dependency'))
 commit=metrics.commit_coverage(opportunities,quota_targets)
 if commit<0.60: gaps.append(gap('gap_low_commit_coverage','forecast_governance','commit_coverage',round(commit,3),'>= 0.60','critical',f'A cobertura de Commit esta em {commit:.1%} da quota analisada.','Hipotese provavel: a meta nao esta coberta por deals com evidencia operacional suficiente.','Separar gap por mes e exigir plano de acao por manager.','Head de RevOps','commit_coverage'))
 pc=metrics.pipeline_coverage(opportunities,quota_targets)
 if pc<2.5: gaps.append(gap('gap_pipeline_coverage','pipeline_generation','pipeline_coverage',round(pc,2),'>= 2.50','high',f'O pipeline aberto representa {pc:.2f}x a quota.','Hipotese provavel: cobertura nominal nao absorve perdas esperadas e slippage.','Recalibrar meta de pipeline coverage por segmento e reforcar criacao de pipeline novo.','RevOps e Demand Generation','pipeline_coverage'))
 stuck=metrics.stuck_opportunities(opportunities,20)
 if len(stuck)>=8: gaps.append(gap('gap_stuck_opportunities','deal_execution','stuck_opportunities',len(stuck),'< 8','high',f'Foram encontradas {len(stuck)} oportunidades abertas paradas ha mais de 20 dias.','Hipotese provavel: parte do pipeline pode estar inflada por deals sem progressao real.','Executar limpeza de pipeline e bloquear estagio avancado sem next step.','Sales Ops Manager','stuck_opportunities'))
 act=metrics.activity_gap_rate(opportunities,14); cna=metrics.commit_without_activity(opportunities,14)
 if act>0.20 or len(cna)>0: gaps.append(gap('gap_activity_hygiene','deal_execution','activity_gap_rate',round(act,3),'<= 0.20','high',f'A evidencia aponta para {act:.1%} dos deals abertos sem atividade recente e {len(cna)} Commit sem atividade recente.','Hipotese provavel: parte dos deals forecastaveis nao possui cadencia comercial ativa.','Exigir next step datado para Commit e estagios avancados.','Sales Managers','activity_gap_rate'))
 push=metrics.close_date_push_rate(opportunities)
 if push>0.30: gaps.append(gap('gap_close_date_slippage','forecast_hygiene','close_date_push_rate',round(push,3),'<= 0.30','medium',f'Ha indicios de higiene fraca de close date: {push:.1%} das oportunidades tiveram push.','Hipotese provavel: close dates podem estar sendo usadas como expectativa interna.','Criar reason code obrigatorio para push e revisao quinzenal por manager.','Sales Ops','close_date_push_rate'))
 dep=metrics.large_deal_dependency(opportunities); high=metrics.high_value_deals_at_risk(opportunities,risk_flags)
 if dep>0.25 or len(high)>=3: gaps.append(gap('gap_large_deal_dependency','revenue_risk','large_deal_dependency',round(dep,3),'<= 0.25','critical',f'Poucos deals grandes concentram {dep:.1%} do pipeline aberto; {len(high)} deals de alto valor tem risco ativo.','Hipotese provavel: forecast pode estar exposto a poucos eventos de fechamento.','Criar deal review executivo para top deals em risco.','CRO','large_deal_dependency'))
 return pd.DataFrame(gaps)
def main():
 out=find_gaps(load_table('opportunities'),load_table('forecast_snapshots'),load_table('quota_targets'),load_table('close_outcomes'),load_table('risk_flags')); out.to_csv(OUTPUT,index=False); print(f'Consultant gap log generated at {OUTPUT} with {len(out)} gaps')
if __name__=='__main__': main()
