"""Deterministic SYNTHETIC monthly FP&A data, Jan-Sep 2026 (as at Oct 2026)."""
from pathlib import Path
import csv, math, numpy as np
ROOT=Path(__file__).resolve().parents[1]
ROOT.joinpath('data').mkdir(exist_ok=True)
rng=np.random.default_rng(20261019)
products={'Core':(7300,54,31),'Premium':(2400,114,66),'Accessories':(4400,26,11)}
with (ROOT/'data/monthly_budget_actual_synthetic.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['month','product','budget_units','actual_units','budget_price_usd','actual_price_usd','budget_variable_cost_per_unit_usd','actual_variable_cost_per_unit_usd','budget_fixed_opex_usd','actual_fixed_opex_usd'])
 for m in range(1,10):
  for idx,(name,(base_u,p,v)) in enumerate(products.items()):
   season=1+0.04*math.sin(2*math.pi*m/12+idx*.4)
   budget_units=int(round(base_u*season*(1+0.008*(m-1))))
   actual_units=int(round(budget_units*(1+rng.normal(-.006,.050))))
   actual_price=round(p*(1+rng.normal(.004,.018)),2)
   actual_v=round(v*(1+rng.normal(.024,.025)),2)
   budget_fixed=round([115000,97000,66000][idx]*(1+.002*(m-1)),2)
   actual_fixed=round(budget_fixed*(1+rng.normal(.019,.024)),2)
   w.writerow([f'2026-{m:02d}',name,budget_units,actual_units,p,actual_price,v,actual_v,budget_fixed,actual_fixed])
print('synthetic data generated')
