"""Small transparent cross-project tests; works with Python standard library."""
from pathlib import Path
import csv,json,unittest
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
def rows(path):
 with (R/path).open(newline='') as f:return list(csv.DictReader(f))
def d(x):return Decimal(str(x))
class PortfolioAuditTests(unittest.TestCase):
 def test_walmart_reported_identity(self):
  data=rows('01_Walmart_Valuation/data/walmart_fy2024_fy2026.csv')
  self.assertEqual(len(data),3)
  for x in data:
   self.assertEqual(d(x['net_sales_usd_m'])+d(x['membership_other_usd_m']),d(x['total_revenue_usd_m']))
   self.assertEqual(d(x['total_revenue_usd_m'])-d(x['cost_of_sales_usd_m'])-d(x['sga_usd_m']),d(x['operating_income_usd_m']))
   self.assertGreater(d(x['operating_cash_flow_usd_m'])-d(x['capex_usd_m']),0)
 def test_walmart_dcf_base_formula(self):
  j=json.loads((R/'01_Walmart_Valuation/outputs/results.json').read_text())
  a=j['assumptions'];forecast=j['forecast'];fcff=[z['fcff'] for z in forecast]
  disc=sum(x/(1+a['wacc'])**i for i,x in enumerate(fcff,1))
  terminal=(fcff[-1]*(1+a['terminal_growth'])/(a['wacc']-a['terminal_growth']))/((1+a['wacc'])**len(fcff))
  self.assertAlmostEqual(j['illustrative_enterprise_value_usd_m'],disc+terminal,places=5)
 def test_fpa_source_and_variance_bridge(self):
  data=rows('02_FP&A_Forecasting/data/monthly_budget_actual_synthetic.csv')
  self.assertEqual(len(data),27)
  b=sum((d(x['budget_units'])*d(x['budget_price_usd']) for x in data),Decimal('0'))
  a=sum((d(x['actual_units'])*d(x['actual_price_usd']) for x in data),Decimal('0'))
  volume=sum(((d(x['actual_units'])-d(x['budget_units']))*d(x['budget_price_usd']) for x in data),Decimal('0'))
  price=sum((d(x['actual_units'])*(d(x['actual_price_usd'])-d(x['budget_price_usd'])) for x in data),Decimal('0'))
  self.assertEqual(a-b,volume+price)
  self.assertEqual(b,Decimal('7283614'))
  self.assertEqual(a,Decimal('7235861.76'))
 def test_fpa_q4_forecast_consistency(self):
  j=json.loads((R/'02_FP&A_Forecasting/outputs/q4_forecast_results.json').read_text())
  self.assertAlmostEqual(j['fy2026_outlook_revenue_usd'],j['ytd_actual_revenue_usd']+j['q4_forecast_revenue_usd'],places=5)
  self.assertAlmostEqual(j['fy2026_outlook_profit_usd'],j['ytd_actual_profit_usd']+j['q4_forecast_profit_usd'],places=5)
 def test_credit_not_improperly_labeled_uci(self):
  j=json.loads((R/'03_Credit_Risk/outputs/metrics_synthetic.json').read_text())
  self.assertEqual(j['data_mode'],'synthetic')
  self.assertEqual(j['dataset_size'],3200)
  self.assertGreaterEqual(j['roc_auc'],0)
  self.assertLessEqual(j['roc_auc'],1)
 def test_reconciliation_amount_controls(self):
  j=json.loads((R/'04_Finance_Reconciliation_Automation/outputs/control_summary.json').read_text())
  self.assertEqual(j['exception_keys'],8)
  self.assertEqual(j['matched_keys'],66)
  self.assertEqual(d(j['invoice_register_total_usd'])-d(j['gl_total_usd']),d(j['aggregate_invoice_minus_gl_usd']))
if __name__=='__main__':unittest.main()
