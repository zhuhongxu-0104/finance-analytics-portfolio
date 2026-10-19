"""Baseline credit-default prediction using UCI 350 data OR explicit synthetic demo.
Example: python src/analyze.py --data data/demo_credit_synthetic.csv --mode synthetic
         python src/analyze.py --data 'data/default of credit card clients.xls' --mode uci
The official UCI file is NOT redistributed in this repository; see README.
"""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,roc_curve,confusion_matrix
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--data',default='data/demo_credit_synthetic.csv');p.add_argument('--mode',choices=['synthetic','uci'],default='synthetic');a=p.parse_args()
path=Path(a.data); path=path if path.is_absolute() else ROOT/path
if a.mode=='uci':
 if path.suffix.lower() not in ('.xls','.xlsx'):raise SystemExit('For UCI mode, supply the official .xls or .xlsx file.')
 df=pd.read_excel(path,header=1)
 target='default payment next month'
 if target not in df.columns:raise SystemExit(f'Expected column {target!r}; check official UCI workbook/header.')
 y=df[target].astype(int)
 features=['LIMIT_BAL','AGE','PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6','BILL_AMT1','BILL_AMT2','BILL_AMT3','PAY_AMT1','PAY_AMT2','PAY_AMT3']
 # Demographic protected/proxy variables SEX, EDUCATION and MARRIAGE intentionally excluded for the class project.
else:
 df=pd.read_csv(path)
 y=df['default'].astype(int)
 features=['LIMIT_BAL','AGE','PAY_0','BILL_AMT1','PAY_AMT1']
X=df[features].apply(pd.to_numeric,errors='coerce')
assert y.nunique()==2
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
model=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler()),('lr',LogisticRegression(max_iter=2000))])
model.fit(Xtr,ytr);score=model.predict_proba(Xte)[:,1]
threshold=.20
pred=(score>=threshold).astype(int)
cm=confusion_matrix(yte,pred).tolist()
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
metrics={'data_mode':a.mode,'dataset_size':len(df),'train_n':len(Xtr),'test_n':len(Xte),
 'default_rate':float(y.mean()),'test_default_rate':float(yte.mean()),
 'roc_auc':float(roc_auc_score(yte,score)),
 'avg_precision':float(average_precision_score(yte,score)),
 'brier_score':float(brier_score_loss(yte,score)),
 'threshold':threshold,'confusion_matrix_tn_fp_fn_tp':cm,
 'excluded_demographic_features':['SEX','EDUCATION','MARRIAGE'] if a.mode=='uci' else [],
 'interpretation':'Exploratory educational baseline, NOT loan decisioning or underwriting.'}
(OUT/f'metrics_{a.mode}.json').write_text(json.dumps(metrics,indent=2))
fpr,tpr,_=roc_curve(yte,score)
fig,ax=plt.subplots(figsize=(8.5,5));ax.plot(fpr,tpr,label=f'AUC = {metrics["roc_auc"]:.3f}',color='#087E8B',linewidth=2.5)
ax.plot([0,1],[0,1],'--',color='#A7B1BA');ax.set(xlabel='False positive rate',ylabel='True positive rate',title=f'Credit-default ROC | {a.mode.upper()} data');ax.legend(frameon=False);fig.tight_layout();fig.savefig(OUT/f'roc_{a.mode}.png',dpi=160);plt.close(fig)
# Calibration-by-score-decile overview; test data only (not a validated calibration model).
q=pd.DataFrame({'score':score,'outcome':yte.to_numpy()})
q['bucket']=pd.qcut(q.score,10,labels=False,duplicates='drop')
profile=q.groupby('bucket').agg(avg_pred=('score','mean'),observed=('outcome','mean'),n=('outcome','size')).reset_index()
profile.to_csv(OUT/f'risk_deciles_{a.mode}.csv',index=False)
fig,ax=plt.subplots(figsize=(9,5));ax.plot(profile.bucket+1,profile.avg_pred,marker='o',label='Mean estimated PD',color='#164874');ax.plot(profile.bucket+1,profile.observed,marker='s',label='Observed default rate',color='#DF8F39');ax.set(xlabel='Risk decile (1 = lowest estimated risk)',ylabel='Default rate / predicted PD',title=f'Default rates by score decile | {a.mode.upper()} data');ax.legend(frameon=False);fig.tight_layout();fig.savefig(OUT/f'risk_deciles_{a.mode}.png',dpi=160);plt.close(fig)
print(json.dumps(metrics,indent=2))
