import pandas as pd
def test_gap_log():
 g=pd.read_csv('data/processed/consultant_gap_log.csv'); assert len(g)>=1
 for c in ['severity','recommended_action','missing_evidence','validation_questions']: assert c in g.columns
def test_no_root_cause_claim():
 text=' '.join(pd.read_csv('data/processed/consultant_gap_log.csv').astype(str).agg(' '.join,axis=1)).lower(); assert not any(x in text for x in ['a causa e','foi comprovado','garantidamente','com certeza'])
