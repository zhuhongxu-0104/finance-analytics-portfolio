"""Reproduce FP&A reporting outputs from clearly synthetic data."""
from pathlib import Path
import pandas as pd, numpy as np, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/'data/monthly_budget_actual_synthetic.csv')
for prefix in ['budget','actual']:
 df[f'{prefix}_revenue']=df[f'{prefix}_units']*df[f'{prefix}_price_usd']
 df[f'{prefix}_variable_cost']=df[f'{prefix}_units']*df[f'{prefix}_variable_cost_per_unit_usd']
 df[f'{prefix}_profit']=df[f'{prefix}_revenue']-df[f'{prefix}_variable_cost']-df[f'{prefix}_fixed_opex_usd']
agg=df.groupby('month',sort=True)[['budget_revenue','actual_revenue','budget_profit','actual_profit']].sum().reset_index()
agg['revenue_variance']=agg.actual_revenue-agg.budget_revenue
agg['profit_variance']=agg.actual_profit-agg.budget_profit
agg.to_csv(OUT/'monthly_variance_summary.csv',index=False)
rev_v=float(agg.revenue_variance.sum());profit_v=float(agg.profit_variance.sum())
# Core driver decomposition with cross-term assigned to price impact.
units_effect=float(((df.actual_units-df.budget_units)*df.budget_price_usd).sum())
price_effect=float((df.actual_units*(df.actual_price_usd-df.budget_price_usd)).sum())
assert abs(units_effect+price_effect-rev_v)<1e-6
stats={'period':'Jan-Sep 2026', 'data_type':'100% synthetic, educational scenario',
 'budget_revenue_usd':float(df.budget_revenue.sum()),'actual_revenue_usd':float(df.actual_revenue.sum()),
 'budget_operating_profit_usd':float(df.budget_profit.sum()),'actual_operating_profit_usd':float(df.actual_profit.sum()),
 'revenue_variance_usd':rev_v,'revenue_variance_pct':rev_v/float(df.budget_revenue.sum()),
 'operating_profit_variance_usd':profit_v,'operating_profit_variance_pct':profit_v/abs(float(df.budget_profit.sum())),
 'volume_effect_usd':units_effect,'price_effect_usd':price_effect}
(OUT/'results.json').write_text(json.dumps(stats,indent=2))
plt.rcParams.update({'font.size':9.5,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,1,figsize=(10.5,7.3),sharex=True,gridspec_kw={'hspace':.36})
x=np.arange(len(agg));width=.38
for ax,a,b,title in [(axs[0],'budget_revenue','actual_revenue','Monthly revenue | Budget vs Actual'),(axs[1],'budget_profit','actual_profit','Monthly operating profit | Budget vs Actual')]:
 ax.bar(x-width/2,agg[a]/1000,width,label='Budget',color='#164874')
 ax.bar(x+width/2,agg[b]/1000,width,label='Actual',color='#087E8B')
 ax.set_ylabel('USD thousands');ax.set_title(title,loc='left',fontweight='bold');ax.legend(loc='upper right',frameon=False)
axs[1].set_xticks(x,agg.month.tolist());fig.suptitle('Synthetic retail operating model - Jan to Sep 2026',fontweight='bold',fontsize=13);fig.subplots_adjust(top=.89,bottom=.11,hspace=.36);fig.savefig(OUT/'budget_actual_dashboard.png',dpi=150);plt.close(fig)
print(json.dumps(stats,indent=2))
