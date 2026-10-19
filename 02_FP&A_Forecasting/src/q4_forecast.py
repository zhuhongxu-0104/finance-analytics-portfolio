"""Simple Q4 synthetic outlook based on September actual run rate; no true forecasting claim."""
from pathlib import Path
import csv,json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
data=pd.read_csv(ROOT/'data/monthly_budget_actual_synthetic.csv')
sep=data[data.month=='2026-09'].set_index('product')
assumptions={'monthly_unit_growth':.01,'monthly_price_growth':0.,'monthly_variable_unit_cost_increase':.005,'monthly_fixed_opex_increase':.003}
records=[]
for h in range(1,4):
 for product,row in sep.iterrows():
  units=round(row.actual_units*(1+assumptions['monthly_unit_growth'])**h)
  price=row.actual_price_usd*(1+assumptions['monthly_price_growth'])**h
  variable_cost=row.actual_variable_cost_per_unit_usd*(1+assumptions['monthly_variable_unit_cost_increase'])**h
  fixed=row.actual_fixed_opex_usd*(1+assumptions['monthly_fixed_opex_increase'])**h
  rev=units*price;vc=units*variable_cost;profit=rev-vc-fixed
  records.append({'month':f'2026-{9+h:02d}','product':product,'forecast_units':units,'forecast_price_usd':price,'forecast_var_cost_per_unit_usd':variable_cost,'forecast_fixed_opex_usd':fixed,'forecast_revenue_usd':rev,'forecast_profit_usd':profit})
q4=pd.DataFrame(records);q4.to_csv(OUT/'q4_forecast_synthetic.csv',index=False)
ytd_rev=float((data.actual_units*data.actual_price_usd).sum())
ytd_profit=float((data.actual_units*(data.actual_price_usd-data.actual_variable_cost_per_unit_usd)-data.actual_fixed_opex_usd).sum())
metrics={'data_type':'synthetic forecast, not historical results','forecast_assumptions':assumptions,'ytd_actual_revenue_usd':ytd_rev,'ytd_actual_profit_usd':ytd_profit,'q4_forecast_revenue_usd':float(q4.forecast_revenue_usd.sum()),'q4_forecast_profit_usd':float(q4.forecast_profit_usd.sum()),'fy2026_outlook_revenue_usd':ytd_rev+float(q4.forecast_revenue_usd.sum()),'fy2026_outlook_profit_usd':ytd_profit+float(q4.forecast_profit_usd.sum())}
(OUT/'q4_forecast_results.json').write_text(json.dumps(metrics,indent=2))
a=data.assign(actual_revenue=data.actual_units*data.actual_price_usd).groupby('month').actual_revenue.sum().reset_index()
f=q4.groupby('month').forecast_revenue_usd.sum().reset_index()
fig,ax=plt.subplots(figsize=(9.5,4.6))
ax.plot(range(1,10),a.actual_revenue/1000,marker='o',color='#164874',label='Synthetic actual Jan-Sep')
ax.plot(range(9,13),[a.actual_revenue.iloc[-1]/1000]+(f.forecast_revenue_usd/1000).tolist(),marker='D',linestyle='--',color='#C48E30',label='Illustrative Q4 forecast')
ax.axvline(9.5,linewidth=1,color='#A7B1BA',linestyle=':')
ax.set_xticks(range(1,13),[f'{j:02d}' for j in range(1,13)])
ax.set(xlabel='2026 month',ylabel='USD thousands',title='Fictional retailer | Actual-to-forecast revenue')
ax.legend(frameon=False)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout();fig.savefig(OUT/'q4_actual_forecast.png',dpi=165);plt.close(fig)
print(json.dumps(metrics,indent=2))
