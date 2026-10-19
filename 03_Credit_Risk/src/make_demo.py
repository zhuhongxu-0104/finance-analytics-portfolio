"""Creates clearly synthetic observations for a smoke-test ONLY, not UCI data."""
from pathlib import Path
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20261019)
n=3200
limit=rng.choice([20000,50000,100000,200000,400000],size=n,p=[.16,.25,.30,.20,.09])
age=rng.integers(21,66,size=n)
pay_0=rng.choice([-2,-1,0,1,2,3,4],size=n,p=[.03,.18,.53,.11,.08,.05,.02])
util=rng.beta(2.5,3,size=n)
bill=limit*util;last_payment=bill*rng.uniform(.05,1.12,size=n)
log_odds=-2.9+0.6*np.maximum(pay_0,0)+2.0*util-1.3*(last_payment/(bill+1))
p=1/(1+np.exp(-log_odds))
default=rng.binomial(1,p)
df=pd.DataFrame({'LIMIT_BAL':limit,'AGE':age,'PAY_0':pay_0,'BILL_AMT1':bill.round(0),'PAY_AMT1':last_payment.round(0),'default':default})
(R/'data/demo_credit_synthetic.csv').parent.mkdir(exist_ok=True)
df.to_csv(R/'data/demo_credit_synthetic.csv',index=False)
print('Generated synthetic demo - NOT actual UCI data')
