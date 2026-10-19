"""Invoice-to-GL reconciliation and exception report. Run from any directory."""
from pathlib import Path
from decimal import Decimal,InvalidOperation
from collections import defaultdict,Counter
import csv,json
R=Path(__file__).resolve().parents[1]
def money(x):
 try: return Decimal(str(x)).quantize(Decimal('0.01'))
 except InvalidOperation as e: raise ValueError(f'Invalid monetary value {x!r}') from e

def load(path):
 with path.open(newline='') as f: return list(csv.DictReader(f))

def reconcile(invoice_rows,gl_rows):
 invoices=defaultdict(list); ledger=defaultdict(list)
 for row in invoice_rows:
  invoices[row['invoice_id'].strip()].append(row)
 for row in gl_rows:
  ledger[row['invoice_id'].strip()].append(row)
 results=[]
 for key in sorted(set(invoices)|set(ledger)):
  a,b=invoices[key],ledger[key]
  ain=sum((money(r['invoice_amount_usd']) for r in a),Decimal('0'))
  gln=sum((money(r['posted_amount_usd']) for r in b),Decimal('0'))
  issues=[]
  if len(a)>1:issues.append('Duplicate invoice')
  if len(b)>1:issues.append('Duplicate GL')
  if not a:issues.append('GL without invoice')
  if not b:issues.append('Invoice without GL')
  if a and b:
   if ain!=gln:issues.append('Amount mismatch')
   if {r['department'] for r in a}!={r['department'] for r in b}:issues.append('Department mismatch')
  results.append(dict(invoice_id=key,invoice_count=len(a),gl_entry_count=len(b),
      invoice_total_usd=f'{ain:.2f}',gl_total_usd=f'{gln:.2f}',difference_invoice_minus_gl_usd=f'{ain-gln:.2f}',
      invoice_department=';'.join(sorted({r['department'] for r in a})),
      gl_department=';'.join(sorted({r['department'] for r in b})),
      status='EXCEPTION' if issues else 'MATCHED',issues='; '.join(issues)))
 summary={'data_type':'100% synthetic accounts payable and general ledger control test',
   'period':'Sep 2026','invoice_register_rows':len(invoice_rows),'gl_postings':len(gl_rows),
   'unique_invoice_ids_in_register':len(invoices),'unique_reconciliation_keys':len(results),
   'matched_keys':sum(x['status']=='MATCHED' for x in results),
   'exception_keys':sum(x['status']=='EXCEPTION' for x in results),
   'exception_rate_of_keys':sum(x['status']=='EXCEPTION' for x in results)/len(results),
   'invoice_register_total_usd':f"{sum((money(r['invoice_amount_usd']) for r in invoice_rows),Decimal('0')):.2f}",
   'gl_total_usd':f"{sum((money(r['posted_amount_usd']) for r in gl_rows),Decimal('0')):.2f}",
   'aggregate_invoice_minus_gl_usd':f"{sum((money(r['invoice_amount_usd']) for r in invoice_rows),Decimal('0'))-sum((money(r['posted_amount_usd']) for r in gl_rows),Decimal('0')):.2f}",
   'issue_counts':dict(sorted(Counter(issue for x in results for issue in x['issues'].split('; ') if issue).items()))}
 return results,summary

def main():
 rows,summary=reconcile(load(R/'data/invoice_register_synthetic.csv'),load(R/'data/general_ledger_synthetic.csv'))
 (R/'outputs').mkdir(exist_ok=True)
 with (R/'outputs/reconciliation_all_keys.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 with (R/'outputs/exceptions_only.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([r for r in rows if r['status']=='EXCEPTION'])
 (R/'outputs/control_summary.json').write_text(json.dumps(summary,indent=2))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
