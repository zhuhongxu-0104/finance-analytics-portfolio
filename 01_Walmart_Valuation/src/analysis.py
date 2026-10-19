"""Reproduce Walmart FY2024-26 figures and a learning-only FCFF DCF.
Usage: python src/analysis.py (from project root)
Dependencies: pandas, numpy, matplotlib.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/'data/walmart_fy2024_fy2026.csv')
assert (df.total_revenue_usd_m-df.cost_of_sales_usd_m-df.sga_usd_m-df.operating_income_usd_m).abs().max()==0
df['revenue_growth']=df.total_revenue_usd_m.pct_change()
df['operating_margin']=df.operating_income_usd_m/df.total_revenue_usd_m
df['company_fcf_usd_m']=df.operating_cash_flow_usd_m-df.capex_usd_m
# These are student-case assumptions; NOT company guidance, analyst consensus, nor forecasted fact.
assumptions={'revenue_growth':[.046,.043,.040,.038,.035],
 'operating_margin':[.042,.0425,.043,.0435,.044],
 'da_pct_sales':.020,'capex_pct_sales':.035,'incremental_nwc_pct_of_revenue_increase':.0025,
 'cash_tax_rate':.25,'wacc':.075,'terminal_growth':.025}
r=float(df.iloc[-1].total_revenue_usd_m); fcff=[]; rows=[]
for year,(growth,margin) in enumerate(zip(assumptions['revenue_growth'],assumptions['operating_margin']),start=2027):
 new_rev=r*(1+growth);ebit=new_rev*margin;nopat=ebit*(1-assumptions['cash_tax_rate'])
 da=new_rev*assumptions['da_pct_sales'];capex=new_rev*assumptions['capex_pct_sales'];delta_nwc=(new_rev-r)*assumptions['incremental_nwc_pct_of_revenue_increase']
 f=nopat+da-capex-delta_nwc
 rows.append(dict(fy=year,revenue=new_rev,ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=delta_nwc,fcff=f))
 fcff.append(f);r=new_rev
pv_explicit=sum(x/(1+assumptions['wacc'])**(i+1) for i,x in enumerate(fcff))
tv=fcff[-1]*(1+assumptions['terminal_growth'])/(assumptions['wacc']-assumptions['terminal_growth'])
pv_tv=tv/(1+assumptions['wacc'])**len(fcff)
ev=pv_explicit+pv_tv
calc={'source_years':[2024,2025,2026], 'latest_reported_revenue_usd_m':int(df.iloc[-1].total_revenue_usd_m),
 'latest_reported_operating_margin':float(df.iloc[-1].operating_margin),
 'fiscal_2026_revenue_growth':float(df.iloc[-1].revenue_growth),
 'latest_reported_company_fcf_usd_m':int(df.iloc[-1].company_fcf_usd_m),
 'illustrative_enterprise_value_usd_m':float(ev),'enterprise_value_forecast_component_usd_m':float(pv_explicit),
 'enterprise_value_terminal_component_usd_m':float(pv_tv),'terminal_share':float(pv_tv/ev),
 'assumptions':assumptions,'forecast':rows}
(OUT/'results.json').write_text(json.dumps(calc,indent=2))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(9.5,4.6))
y=df.fiscal_year.astype(str);ax.bar(y,df.total_revenue_usd_m/1000,color='#164874',width=.55)
for x,z in zip(y,df.total_revenue_usd_m/1000):ax.text(x,z+5,f'${z:,.1f}B',ha='center',fontsize=11)
ax.set_ylim(0,850);ax.set_ylabel('Total revenue (USD billions)');ax.set_title('Walmart | Fiscal 2024-2026 reported revenue',loc='left',fontweight='bold');fig.tight_layout();fig.savefig(OUT/'revenue_historical.png',dpi=165);plt.close(fig)
fig,ax=plt.subplots(figsize=(9.5,4.6))
years=[str(r['fy']) for r in rows];growth=[r['fcff']/1000 for r in rows]
ax.bar(years,growth,color='#087E8B');ax.set_ylabel('FCFF (USD billions)');ax.set_title('Illustrative FCFF forecast - NOT company guidance',loc='left',fontweight='bold');fig.tight_layout();fig.savefig(OUT/'forecast_fcff.png',dpi=165);plt.close(fig)
print(json.dumps({k:calc[k] for k in ['fiscal_2026_revenue_growth','latest_reported_operating_margin','latest_reported_company_fcf_usd_m','illustrative_enterprise_value_usd_m','terminal_share']},indent=2))
