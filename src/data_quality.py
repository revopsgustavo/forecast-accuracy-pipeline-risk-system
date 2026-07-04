from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / 'data' / 'processed'
OUTPUT = PROCESSED / 'data_quality_report.csv'
REQUIRED = {
    'opportunities': ['opportunity_id','account_id','ae_id','amount','stage','forecast_category','close_date','probability'],
    'accounts': ['account_id','account_name','industry'],
    'aes': ['ae_id','ae_name','segment','manager'],
    'sales_stages': ['stage','default_probability','stage_order'],
    'forecast_snapshots': ['snapshot_date','month','ae_id','submitted_forecast'],
    'quota_targets': ['month','ae_id','target_amount'],
    'deal_activity': ['activity_date','opportunity_id','activity_type'],
    'stage_history': ['valid_from','opportunity_id','stage'],
    'close_outcomes': ['outcome','opportunity_id','actual_closed_won'],
    'risk_flags': ['risk_type','opportunity_id','severity'],
}
VALID_CATEGORIES = {'pipeline','best_case','commit','closed'}
VALID_STAGES = {'qualification','discovery','solution_fit','proposal','negotiation','legal_procurement','closed_won','closed_lost'}

def rec(check_name, table, status, details, row_count=0):
    return {'check_name': check_name, 'table': table, 'status': status, 'details': details, 'row_count': row_count}

def validate():
    records = []
    for table, columns in REQUIRED.items():
        path = PROCESSED / f'{table}.csv'
        if not path.exists():
            records.append(rec('file_exists', table, 'fail', f'Missing file: {path}', 0))
            continue
        df = pd.read_csv(path)
        records.append(rec('file_exists', table, 'pass', 'File exists', len(df)))
        missing = [column for column in columns if column not in df.columns]
        records.append(rec('required_columns', table, 'fail' if missing else 'pass', f'Missing columns: {missing}', len(df)))
        for column in [c for c in ['opportunity_id','account_id','ae_id'] if c in df.columns]:
            nulls = int(df[column].isna().sum())
            records.append(rec('ids_not_null', table, 'fail' if nulls else 'pass', f'{column} nulls: {nulls}', len(df)))
        for column in [c for c in ['amount','submitted_forecast','weighted_forecast','target_amount','actual_closed_won'] if c in df.columns]:
            negatives = int(pd.to_numeric(df[column], errors='coerce').fillna(0).lt(0).sum())
            records.append(rec('non_negative_money', table, 'fail' if negatives else 'pass', f'{column} negatives: {negatives}', len(df)))
        if table == 'opportunities':
            invalid_categories = sorted(set(df['forecast_category'].dropna()) - VALID_CATEGORIES)
            invalid_stages = sorted(set(df['stage'].dropna()) - VALID_STAGES)
            close_dates = pd.to_datetime(df['close_date'], errors='coerce')
            probabilities = pd.to_numeric(df['probability'], errors='coerce')
            records.append(rec('valid_forecast_categories', table, 'fail' if invalid_categories else 'pass', f'Invalid categories: {invalid_categories}', len(df)))
            records.append(rec('valid_stages', table, 'fail' if invalid_stages else 'pass', f'Invalid stages: {invalid_stages}', len(df)))
            records.append(rec('valid_close_dates', table, 'fail' if close_dates.isna().any() else 'pass', f'Invalid close dates: {int(close_dates.isna().sum())}', len(df)))
            valid_probabilities = probabilities.between(0, 1).all() or probabilities.between(0, 100).all()
            records.append(rec('valid_probabilities', table, 'pass' if valid_probabilities else 'fail', 'Probability scale must be 0-1 or 0-100', len(df)))
    return pd.DataFrame(records)

def main():
    report = validate()
    report.to_csv(OUTPUT, index=False)
    failures = int(report['status'].eq('fail').sum()) if not report.empty else 1
    print(f'Data quality report generated at {OUTPUT}. Failures: {failures}')

if __name__ == '__main__':
    main()
