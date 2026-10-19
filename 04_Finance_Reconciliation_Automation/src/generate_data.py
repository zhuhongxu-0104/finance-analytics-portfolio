"""Fully synthetic, repeatable accounts-payable-to-general-ledger records."""
from pathlib import Path
from datetime import date,timedelta
import random,csv
R=Path(__file__).resolve().parents[1]; (R/'data').mkdir(exist_ok=True)
rng=random.Random(20261019)
vendors=['Aspen Supplies','Birch Office','Cedar Services','Delta Hardware']
departments=['Operations','IT','Marketing','Administration']
invoices=[];gl=[]
for i in range(1,73):
 inv=f'INV-{i:04d}'
 amount=round(rng.uniform(125,6500),2)
 dept=departments[(i-1)%4]
 vendor=vendors[(i-1)%4]
 d=(date(2026,9,1)+timedelta(days=(i*7)%30)).isoformat()
 invoices.append(dict(invoice_id=inv,invoice_date=d,vendor=vendor,department=dept,invoice_amount_usd=f'{amount:.2f}'))
 if i in [11,44]:continue  # legitimate invoice has no GL posting
 gl_amount=amount+({20:125.00,33:-60.00}.get(i,0))
 gl_dept='Operations' if i==55 else dept
 gl.append(dict(entry_id=f'GL-{i:04d}',invoice_id=inv,posting_date=d,department=gl_dept,posted_amount_usd=f'{gl_amount:.2f}'))
 if i==66:  # accidental duplicate posting
  gl.append(dict(entry_id='GL-DUP-66',invoice_id=inv,posting_date=d,department=gl_dept,posted_amount_usd=f'{amount:.2f}'))
# Entries without a matching invoice (not actual vendor transactions)
for j,amount in [(1,900.00),(2,1750.00)]:
 gl.append(dict(entry_id=f'GL-UNMATCH-{j}',invoice_id=f'EXT-{j:04d}',posting_date='2026-09-30',department='IT',posted_amount_usd=f'{amount:.2f}'))
with (R/'data/invoice_register_synthetic.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(invoices[0]));w.writeheader();w.writerows(invoices)
with (R/'data/general_ledger_synthetic.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(gl[0]));w.writeheader();w.writerows(gl)
print(f'{len(invoices)} synthetic invoices and {len(gl)} synthetic GL entries')
