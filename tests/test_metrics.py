import pandas as pd
from src import metrics
def data(): return pd.read_csv('data/processed/opportunities.csv'),pd.read_csv('data/processed/forecast_snapshots.csv'),pd.read_csv('data/processed/quota_targets.csv'),pd.read_csv('data/processed/close_outcomes.csv')
def test_main_metrics():
 o,f,q,c=data(); assert metrics.total_pipeline(o)>0; assert metrics.open_pipeline(o)>=0; assert metrics.weighted_forecast(o)>=0; assert metrics.pipeline_coverage(o,q)>=0; assert 0<=metrics.forecast_accuracy(metrics.forecast_submitted(f),c.actual_closed_won.sum())<=1
def test_rates():
 o,f,q,c=data(); assert 0<=metrics.best_case_dependency(o)<=1; assert 0<=metrics.slippage_rate(o)<=1; assert 0<=metrics.activity_gap_rate(o)<=1; wr=metrics.win_rate_by_ae(o); assert wr.empty or wr.win_rate.between(0,1).all()
