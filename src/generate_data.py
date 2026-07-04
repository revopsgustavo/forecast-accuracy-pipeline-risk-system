from pathlib import Path
import sqlite3, numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'data'/'processed'; DB=ROOT/'data'/'database'/'forecast_pipeline_case.sqlite'
def main():
 P.mkdir(parents=True,exist_ok=True); DB.parent.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(5)
 aes=pd.DataFrame([(f'ae_{i:03d}',n,s,'Manager '+str((i%2)+1),'BR') for i,(n,s) in enumerate([('Ana Ribeiro','Enterprise'),('Bruno Costa','Mid Market'),('Camila Torres','Enterprise'),('Diego Martins','SMB'),('Eduarda Lima','Mid Market'),('Felipe Rocha','Enterprise')],1)],columns=['ae_id','ae_name','segment','manager','region'])
 accounts=pd.DataFrame([(f'acc_{i:03d}',f'Conta SaaS {i:03d}','software','tier_'+str((i%3)+1)) for i in range(1,61)],columns=['account_id','account_name','industry','strategic_tier'])
 sales_stages=pd.DataFrame([('qualification',.1,12,1),('discovery',.2,15,2),('solution_fit',.35,18,3),('proposal',.55,20,4),('negotiation',.7,18,5),('legal_procurement',.85,15,6),('closed_won',1,0,7),('closed_lost',0,0,8)],columns=['stage','default_probability','max_expected_days','stage_order'])
 probs=dict(zip(sales_stages.stage,sales_stages.default_probability)); stages=list(probs); months=pd.period_range('2026-01','2026-06',freq='M')
 rows=[]
 for i in range(1,121):
  st=stages[(i*5)%8]; mo=months[i%6].strftime('%Y-%m'); cat='best_case' if st in ['proposal','negotiation'] else 'commit' if st=='legal_procurement' else 'closed' if st=='closed_won' else 'pipeline'; created=pd.Timestamp(f'{mo}-01')-pd.Timedelta(days=int(rng.integers(10,150))); close=pd.Timestamp(f'{mo}-01')+pd.offsets.MonthEnd(0)
  rows.append({'opportunity_id':f'opp_{i:03d}','account_id':accounts.iloc[i%60].account_id,'ae_id':aes.iloc[i%6].ae_id,'opportunity_name':f'Expansao {i:03d}','created_date':created.date().isoformat(),'close_date':close.date().isoformat(),'close_month':mo,'amount':int(rng.choice([42000,76000,98000,130000,180000,240000])),'stage':st,'forecast_category':cat,'probability':probs[st],'days_in_stage':int(rng.integers(5,40)),'days_since_last_activity':int(rng.integers(1,32)),'next_activity_date':(pd.Timestamp('2026-06-24')+pd.Timedelta(days=5)).date().isoformat(),'close_date_push_count':int(rng.choice([0,0,1,2,3])),'is_open':st not in ['closed_won','closed_lost'],'commit_criteria_met':cat=='commit' and i%4!=0,'new_pipeline_created_month':mo if i%6 else '2026-01'})
 o=pd.DataFrame(rows)
 for oid,ae,st,cat,amt,ds,da,push in [('opp_005','ae_001','legal_procurement','commit',185000,31,22,2),('opp_011','ae_001','negotiation','commit',240000,36,25,3),('opp_023','ae_003','proposal','best_case',260000,49,31,4),('opp_035','ae_004','negotiation','best_case',300000,42,22,3),('opp_053','ae_006','negotiation','best_case',340000,52,29,4),('opp_059','ae_006','legal_procurement','commit',220000,33,26,3)]:
  m=o.opportunity_id.eq(oid); o.loc[m,['ae_id','stage','forecast_category','amount','days_in_stage','days_since_last_activity','close_date_push_count','next_activity_date','is_open','commit_criteria_met']]=[ae,st,cat,amt,ds,da,push,'',True,False]; o.loc[m,'probability']=probs[st]
 quota=pd.DataFrame([{'quota_id':f'q_{mo.strftime("%Y_%m")}_{ae.ae_id}','month':mo.strftime('%Y-%m'),'ae_id':ae.ae_id,'target_amount':float((210000 if ae.segment=='Enterprise' else 150000 if ae.segment=='Mid Market' else 95000)*(1.25 if mo.strftime('%Y-%m')=='2026-04' else 1))} for mo in months for ae in aes.itertuples()])
 fs=[]
 for mo in months:
  mt=mo.strftime('%Y-%m')
  for day,mult in [(7,1.18),(14,1.1),(21,1.04),(28,1.0)]:
   for ae in aes.itertuples():
    s=o[(o.ae_id.eq(ae.ae_id))&(o.close_month.eq(mt))&(o.is_open.astype(bool))]; w=float((s.amount*s.probability).sum()); sub=w*mult*(1.6 if ae.ae_id=='ae_001' else 1.25 if ae.ae_id=='ae_004' else 1.02); fs.append({'snapshot_id':f'fs_{mt}_{ae.ae_id}_{day}','snapshot_date':pd.Timestamp(mo.year,mo.month,day).date().isoformat(),'month':mt,'ae_id':ae.ae_id,'submitted_forecast':round(sub,2),'weighted_forecast':round(w,2),'open_pipeline':float(s.amount.sum())})
 f=pd.DataFrame(fs); act=o[o.stage.isin(['closed_won','closed_lost'])]
 close=pd.DataFrame([{'outcome_id':'out_'+r.opportunity_id,'opportunity_id':r.opportunity_id,'ae_id':r.ae_id,'month':r.close_month,'outcome':'won' if r.stage=='closed_won' else 'lost','actual_closed_won':float(r.amount) if r.stage=='closed_won' else 0.0,'loss_reason':'' if r.stage=='closed_won' else 'no_decision'} for r in act.itertuples()])
 activity=pd.DataFrame([{'activity_id':f'act_{r.opportunity_id}_{n}','opportunity_id':r.opportunity_id,'activity_date':r.close_date,'activity_type':'call','next_step_recorded':bool(r.next_activity_date),'buyer_engaged':r.days_since_last_activity<18} for r in o.itertuples() for n in range(2)])
 hist=pd.DataFrame([{'history_id':f'h_{r.opportunity_id}_{n}','opportunity_id':r.opportunity_id,'stage':st,'valid_from':r.created_date,'valid_to':r.close_date,'converted_to_next_stage':True,'days_in_stage':r.days_in_stage} for r in o.itertuples() for n,st in enumerate(['qualification','discovery',r.stage])])
 risk=[]
 for r in o.itertuples():
  flags=[]
  if r.is_open and r.days_in_stage>20: flags.append('stale_stage')
  if r.is_open and not r.next_activity_date: flags.append('no_next_step')
  if r.close_date_push_count>=2: flags.append('close_date_slippage')
  if r.is_open and r.amount>=180000: flags.append('high_value_exposure')
  if r.forecast_category=='commit' and not r.commit_criteria_met: flags.append('commit_hygiene')
  for fl in flags: risk.append({'risk_flag_id':f'r_{r.opportunity_id}_{fl}','opportunity_id':r.opportunity_id,'risk_type':fl,'risk_description':fl,'severity':'high' if fl in ['high_value_exposure','commit_hygiene'] else 'medium','is_active':True,'created_date':'2026-06-24'})
 tables={'opportunities':o,'accounts':accounts,'aes':aes,'sales_stages':sales_stages,'forecast_snapshots':f,'quota_targets':quota,'deal_activity':activity,'stage_history':hist,'close_outcomes':close,'risk_flags':pd.DataFrame(risk)}
 for n,df in tables.items(): df.to_csv(P/f'{n}.csv',index=False)
 with sqlite3.connect(DB) as con:
  for n,df in tables.items(): df.to_sql(n,con,if_exists='replace',index=False)
 print(f'Synthetic data generated in {P}'); print(f'SQLite database generated at {DB}')
if __name__=='__main__': main()
