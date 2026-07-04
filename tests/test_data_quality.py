from pathlib import Path
import pandas as pd
def test_files_and_columns():
 p=Path('data/processed'); req={'opportunities.csv':['opportunity_id','account_id','ae_id','amount','stage','forecast_category','close_date'],'forecast_snapshots.csv':['snapshot_date','submitted_forecast'],'quota_targets.csv':['target_amount']}
 for name,cols in req.items():
  df=pd.read_csv(p/name); assert all(c in df.columns for c in cols)
def test_ids_not_null():
 o=pd.read_csv('data/processed/opportunities.csv'); assert o.opportunity_id.notna().all(); assert o.account_id.notna().all(); assert o.ae_id.notna().all()
