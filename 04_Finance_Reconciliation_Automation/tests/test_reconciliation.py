import sys,unittest
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from reconcile import reconcile,load
class ReconciliationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows,cls.s=reconcile(load(R/'data/invoice_register_synthetic.csv'),load(R/'data/general_ledger_synthetic.csv'))
 def get(self,k):return next(x for x in self.rows if x['invoice_id']==k)
 def test_data_counts(self):
  self.assertEqual(self.s['invoice_register_rows'],72)
  self.assertEqual(self.s['gl_postings'],73)  # 72 - 2 missing + 1 duplicate + 2 GL-only
 def test_missing_invoices(self):
  self.assertIn('Invoice without GL',self.get('INV-0011')['issues'])
  self.assertIn('Invoice without GL',self.get('INV-0044')['issues'])
 def test_unmatched_ledger(self):
  self.assertIn('GL without invoice',self.get('EXT-0001')['issues'])
 def test_duplicate(self):self.assertIn('Duplicate GL',self.get('INV-0066')['issues'])
 def test_amount(self):self.assertIn('Amount mismatch',self.get('INV-0020')['issues'])
 def test_department(self):self.assertIn('Department mismatch',self.get('INV-0055')['issues'])
 def test_summary_reconciles(self):
  a=Decimal(self.s['invoice_register_total_usd'])
  b=Decimal(self.s['gl_total_usd'])
  self.assertEqual(a-b,Decimal(self.s['aggregate_invoice_minus_gl_usd']))
  self.assertEqual(self.s['matched_keys']+self.s['exception_keys'],self.s['unique_reconciliation_keys'])
 def test_exception_count(self):self.assertEqual(self.s['exception_keys'],8)
if __name__=='__main__':unittest.main()
