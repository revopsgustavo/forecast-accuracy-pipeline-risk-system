import pandas as pd
OPEN_STAGES={'qualification','discovery','solution_fit','proposal','negotiation','legal_procurement'}
def _num(v): return pd.to_numeric(v,errors='coerce').fillna(0)
def _open(df): return df[df['is_open'].astype(bool)].copy() if len(df) and 'is_open' in df else df.copy()
def total_pipeline(o): return float(_num(o.get('amount',pd.Series(dtype=float))).sum())
def open_pipeline(o): return float(_num(_open(o).get('amount',pd.Series(dtype=float))).sum())
def closed_won_revenue(o): return float(_num(o.loc[o.get('stage','').eq('closed_won'),'amount'] if 'stage' in o else pd.Series(dtype=float)).sum())
def closed_lost_revenue(o): return float(_num(o.loc[o.get('stage','').eq('closed_lost'),'amount'] if 'stage' in o else pd.Series(dtype=float)).sum())
def weighted_forecast(o):
 d=_open(o); p=_num(d.get('probability',pd.Series(dtype=float))); p=p.where(p<=1,p/100); return float((_num(d.get('amount',pd.Series(dtype=float)))*p).sum())
def forecast_submitted(f):
 if f.empty or 'submitted_forecast' not in f: return 0.0
 d=f.copy(); d['snapshot_date']=pd.to_datetime(d.get('snapshot_date'),errors='coerce') if 'snapshot_date' in d else pd.Timestamp('today'); d=d[d.snapshot_date.eq(d.snapshot_date.max())]; return float(_num(d.submitted_forecast).sum())
def forecast_accuracy(s,a):
 den=max(abs(float(s or 0)),abs(float(a or 0)),1.0); return max(0,min(1,1-abs(float(s or 0)-float(a or 0))/den))
def forecast_variance(s,a): return float(s or 0)-float(a or 0)
def _quota(q): return float(_num(q.get('target_amount',pd.Series(dtype=float))).sum()) if q is not None and len(q) else 0.0
def commit_coverage(o,q=None):
 d=_open(o); val=float(_num(d.loc[d.get('forecast_category','').eq('commit'),'amount'] if 'forecast_category' in d else pd.Series(dtype=float)).sum()); qt=_quota(q); return val/qt if qt else 0.0
def best_case_dependency(o):
 d=_open(o); total=float(_num(d.get('amount',pd.Series(dtype=float))).sum()); val=float(_num(d.loc[d.get('forecast_category','').eq('best_case'),'amount'] if 'forecast_category' in d else pd.Series(dtype=float)).sum()); return val/total if total else 0.0
def pipeline_coverage(o,q=None): qt=_quota(q); return open_pipeline(o)/qt if qt else 0.0
def forecast_gap(f,q): return float(f or 0)-float(q or 0)
def quota_attainment(a,q): return float(a or 0)/q if q else 0.0
def slippage_rate(o): return float(_num(o.get('close_date_push_count',pd.Series(dtype=float))).gt(0).mean()) if len(o) else 0.0
def stuck_opportunities(o,days=20):
 d=_open(o); return d[_num(d.get('days_in_stage',pd.Series(dtype=float))).gt(days)].copy() if len(d) else d
def deal_aging(o):
 d=o.copy();
 if len(d) and 'created_date' in d: d['deal_age_days']=(pd.Timestamp('2026-07-04')-pd.to_datetime(d.created_date,errors='coerce')).dt.days.clip(lower=0)
 return d
def stage_conversion_rate(h): return h.groupby('stage',as_index=False)['converted_to_next_stage'].mean().rename(columns={'converted_to_next_stage':'conversion_rate'}) if {'stage','converted_to_next_stage'}.issubset(h.columns) else pd.DataFrame()
def close_date_push_rate(o): return slippage_rate(o)
def win_rate_by_ae(o):
 c=o[o.stage.isin(['closed_won','closed_lost'])] if {'stage','ae_id'}.issubset(o.columns) else pd.DataFrame()
 if c.empty: return pd.DataFrame()
 r=c.groupby('ae_id').agg(closed_deals=('stage','size'),won_deals=('stage',lambda s:s.eq('closed_won').sum())).reset_index(); r['win_rate']=r.won_deals/r.closed_deals; return r
def forecast_accuracy_by_ae(f,o):
 if not {'ae_id','month','submitted_forecast'}.issubset(f.columns): return pd.DataFrame()
 a=o.groupby(['ae_id','month'],as_index=False)['actual_closed_won'].sum() if {'ae_id','month','actual_closed_won'}.issubset(o.columns) else pd.DataFrame(columns=['ae_id','month','actual_closed_won'])
 s=f.groupby(['ae_id','month'],as_index=False)['submitted_forecast'].last(); d=s.merge(a,on=['ae_id','month'],how='left').fillna({'actual_closed_won':0}); d['forecast_variance']=d.submitted_forecast-d.actual_closed_won; d['forecast_accuracy']=d.apply(lambda r:forecast_accuracy(r.submitted_forecast,r.actual_closed_won),axis=1); return d
def pipeline_by_forecast_category(o):
 d=_open(o); return d.groupby('forecast_category',as_index=False)['amount'].sum() if {'forecast_category','amount'}.issubset(d.columns) else pd.DataFrame()
def pipeline_by_stage(o):
 d=_open(o); return d.groupby('stage',as_index=False)['amount'].sum() if {'stage','amount'}.issubset(d.columns) else pd.DataFrame()
def risk_flag_count(r): return int(r.get('is_active',pd.Series([True]*len(r))).astype(bool).sum()) if len(r) else 0
def high_value_deals_at_risk(o,r,threshold=120000): return o.merge(r,on='opportunity_id',how='inner').query('amount >= @threshold') if {'opportunity_id','amount'}.issubset(o.columns) and 'opportunity_id' in r else pd.DataFrame()
def activity_gap_rate(o,days=14):
 d=_open(o); return float(_num(d.get('days_since_last_activity',pd.Series(dtype=float))).gt(days).mean()) if len(d) else 0.0
def commit_without_activity(o,days=14):
 d=_open(o); return d[d.forecast_category.eq('commit') & _num(d.days_since_last_activity).gt(days)].copy() if {'forecast_category','days_since_last_activity'}.issubset(d.columns) else pd.DataFrame()
def old_pipeline_share(o,days=90):
 d=deal_aging(_open(o)); total=float(_num(d.get('amount',pd.Series(dtype=float))).sum()); old=float(_num(d.loc[d.get('deal_age_days',pd.Series(dtype=float)).gt(days),'amount'] if 'deal_age_days' in d else pd.Series(dtype=float)).sum()); return old/total if total else 0.0
def large_deal_dependency(o,top_n=3):
 a=_num(_open(o).get('amount',pd.Series(dtype=float))).sort_values(ascending=False); return float(a.head(top_n).sum()/a.sum()) if a.sum() else 0.0
def weighted_forecast_by_month(o):
 d=_open(o).copy();
 if not {'close_month','amount','probability'}.issubset(d.columns): return pd.DataFrame()
 d['weighted_forecast']=_num(d.amount)*_num(d.probability); return d.groupby('close_month',as_index=False)['weighted_forecast'].sum().rename(columns={'close_month':'month'})
def forecast_vs_actual_by_month(f,o):
 if not {'month','submitted_forecast'}.issubset(f.columns): return pd.DataFrame()
 s=f.groupby('month',as_index=False)['submitted_forecast'].sum(); a=o.groupby('month',as_index=False)['actual_closed_won'].sum() if {'month','actual_closed_won'}.issubset(o.columns) else pd.DataFrame({'month':s.month,'actual_closed_won':0}); d=s.merge(a,on='month',how='left').fillna(0); d['forecast_variance']=d.submitted_forecast-d.actual_closed_won; d['forecast_accuracy']=d.apply(lambda r:forecast_accuracy(r.submitted_forecast,r.actual_closed_won),axis=1); return d
class ExecutiveMetrics:
 def __init__(self,**kw): self.__dict__.update(kw)
def executive_metrics(o,f,q,c):
 sub=forecast_submitted(f); act=float(_num(c.get('actual_closed_won',pd.Series(dtype=float))).sum()); return ExecutiveMetrics(total_pipeline=total_pipeline(o),open_pipeline=open_pipeline(o),closed_won_revenue=closed_won_revenue(o),weighted_forecast=weighted_forecast(o),forecast_submitted=sub,forecast_accuracy=forecast_accuracy(sub,act),commit_coverage=commit_coverage(o,q),best_case_dependency=best_case_dependency(o),pipeline_coverage=pipeline_coverage(o,q),activity_gap_rate=activity_gap_rate(o),old_pipeline_share=old_pipeline_share(o),large_deal_dependency=large_deal_dependency(o))
