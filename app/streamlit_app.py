import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]; sys.path.append(str(ROOT/'src'))
import metrics
from utils import format_currency_br, format_integer_br, format_percent_br, has_columns, select_existing
PROCESSED=ROOT/'data'/'processed'; DOCS=ROOT/'docs'
st.set_page_config(page_title='Forecast Accuracy Pipeline Risk System', layout='wide')
@st.cache_data
def load_table(name):
 p=PROCESSED/f'{name}.csv'; return pd.read_csv(p) if p.exists() else pd.DataFrame()
def read_doc(name):
 p=DOCS/name; return p.read_text(encoding='utf-8') if p.exists() else 'Arquivo ainda nao gerado.'
def note(a,b,c): st.info(f'**O que estamos vendo?** {a}\n\n**Por que importa?** {b}\n\n**Qual decisao isso suporta?** {c}')
def safe_chart(df,cols,fn):
 if df.empty or not has_columns(df,cols): st.warning('Dados insuficientes para exibir este grafico.'); return
 st.plotly_chart(fn(df),use_container_width=True)
def overview():
 st.title('Forecast Accuracy, Pipeline Risk e Governanca Comercial')
 st.write('Sistema analitico sintetico para RevOps avaliar forecast, cobertura de meta, risco de pipeline e decisoes comerciais prioritarias.')
 st.markdown('- Pipeline nominal mostra volume aberto.\n- Weighted forecast ajusta por probabilidade.\n- Commit deve ter evidencia forte.\n- Best Case e upside com risco.\n- IA Consultora e rule-based e gera hipoteses.')
def executive():
 o,f,q,c=load_table('opportunities'),load_table('forecast_snapshots'),load_table('quota_targets'),load_table('close_outcomes'); st.header('Visao Executiva')
 if o.empty: st.warning('Dados insuficientes para exibir este grafico.'); return
 m=metrics.executive_metrics(o,f,q,c); cols=st.columns(4); cols[0].metric('Pipeline aberto',format_currency_br(m.open_pipeline)); cols[1].metric('Weighted forecast',format_currency_br(m.weighted_forecast)); cols[2].metric('Cobertura Commit',format_percent_br(m.commit_coverage)); cols[3].metric('Dependencia Best Case',format_percent_br(m.best_case_dependency)); note('Cobertura e qualidade do forecast.','Executivos precisam separar volume de evidencia.','Qualificar Best Case, auditar Commit e limpar forecast.'); safe_chart(metrics.pipeline_by_forecast_category(o),['forecast_category','amount'],lambda d:px.bar(d,x='forecast_category',y='amount'))
def current():
 o,q=load_table('opportunities'),load_table('quota_targets'); st.header('Forecast Atual'); note('Mix de Commit, Best Case e etapas.','Mostra dependencia de upside.','Revisar criterios de Commit.'); c=st.columns(3); c[0].metric('Commit coverage',format_percent_br(metrics.commit_coverage(o,q))); c[1].metric('Best Case dependency',format_percent_br(metrics.best_case_dependency(o))); c[2].metric('Activity gap',format_percent_br(metrics.activity_gap_rate(o))); safe_chart(metrics.pipeline_by_stage(o),['stage','amount'],lambda d:px.bar(d,x='stage',y='amount'))
def forecast_real():
 st.header('Forecast vs Real'); df=metrics.forecast_vs_actual_by_month(load_table('forecast_snapshots'),load_table('close_outcomes')); note('Forecast submitted vs closed won.','Vies recorrente reduz confianca.','Coaching e calibracao.'); safe_chart(df,['month','submitted_forecast','actual_closed_won'],lambda d:px.line(d,x='month',y=['submitted_forecast','actual_closed_won'],markers=True)); st.dataframe(df,use_container_width=True)
def risk():
 st.header('Pipeline Risk'); r,o=load_table('risk_flags'),load_table('opportunities'); note('Flags por tipo e severidade.','Top deals em risco distorcem forecast.','Escalar deal review.')
 if r.empty: st.warning('Dados insuficientes para exibir este grafico.'); return
 c=st.columns(3); c[0].metric('Risk flags',format_integer_br(len(r))); c[1].metric('Deals afetados',format_integer_br(r.opportunity_id.nunique())); c[2].metric('Flags altas',format_integer_br(r.severity.eq('high').sum())); safe_chart(r.groupby('risk_type',as_index=False).size(),['risk_type','size'],lambda d:px.bar(d,x='risk_type',y='size')); st.dataframe(r.merge(o,on='opportunity_id',how='left'),use_container_width=True)
def aging():
 st.header('Deal Aging'); s=metrics.stuck_opportunities(load_table('opportunities'),20); note('Deals parados ha mais de 20 dias.','Aging sugere pipeline inflado.','Limpar ou reciclar deals.'); st.metric('Oportunidades paradas',format_integer_br(len(s))); st.dataframe(s,use_container_width=True)
def ae():
 st.header('Performance por AE'); df=metrics.forecast_accuracy_by_ae(load_table('forecast_snapshots'),load_table('close_outcomes')); note('Acuracia por AE.','Diferencas indicam calibracao.','Coaching por manager.'); safe_chart(df,['ae_id','forecast_accuracy'],lambda d:px.box(d,x='ae_id',y='forecast_accuracy')); st.dataframe(df,use_container_width=True)
def quota_gap():
 st.header('Gap contra Meta'); f,q,c=load_table('forecast_snapshots'),load_table('quota_targets'),load_table('close_outcomes'); note('Forecast, realizado e quota.','Mostra plano de recuperacao.','Acionar criacao de pipeline ou ajuste de expectativa.'); df=f.groupby('month',as_index=False).submitted_forecast.sum().merge(q.groupby('month',as_index=False).target_amount.sum(),on='month'); df=df.merge(c.groupby('month',as_index=False).actual_closed_won.sum(),on='month',how='left').fillna(0); safe_chart(df,['month','submitted_forecast','target_amount'],lambda d:px.bar(d,x='month',y=['submitted_forecast','target_amount','actual_closed_won'],barmode='group')); st.dataframe(df,use_container_width=True)
def gaps():
 st.header('Consultor de Gaps'); g=load_table('consultant_gap_log')
 if g.empty: st.warning('Dados insuficientes para exibir este grafico.'); return
 cols=st.columns(4)
 for col,sev in zip(cols,['critical','high','medium','low']): col.metric(sev.title(),format_integer_br(g.severity.eq(sev).sum()))
 st.subheader('O que exige acao agora')
 for row in g[g.severity.isin(['critical','high'])].head(5).itertuples(): st.markdown(f'**{row.area} | {row.metric}**: {row.recommended_action}')
 st.dataframe(g,use_container_width=True)
def dq():
 st.header('Qualidade dos Dados'); d=load_table('data_quality_report'); note('Checks de arquivos e dominios.','Sem qualidade, forecast vira opiniao.','Bloquear uso executivo quando falhar.'); st.dataframe(d,use_container_width=True)
PAGES={'Visao Executiva':executive,'Forecast Atual':current,'Forecast vs Real':forecast_real,'Pipeline Risk':risk,'Deal Aging':aging,'Performance por AE':ae,'Gap contra Meta':quota_gap,'Consultor de Gaps':gaps,'IA Consultora':lambda:(st.header('IA Consultora'),st.markdown(read_doc('ai_consultant_analysis.md'))),'Analise Executiva':lambda:(st.header('Analise Executiva'),st.markdown(read_doc('executive_analysis.md'))),'Qualidade dos Dados':dq,'Production Flow':lambda:(st.header('Production Flow'),st.markdown(read_doc('production_flow.md')))}
with st.sidebar: selected=st.radio('Menu',list(PAGES.keys()))
overview(); st.divider(); PAGES[selected]()
