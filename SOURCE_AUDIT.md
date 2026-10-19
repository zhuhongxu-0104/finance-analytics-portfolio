# Source, Model, and Repository Pre-Publication Audit

**Date:** October 19, 2026  
**Scope:** published files, model logic, financial source extraction, labeled synthetic data, reproducibility, common spreadsheet/PDF integrity checks.  
**Important:** An audit is not a warranty of zero errors or a certificate of accounting, finance, or lending-system reliability.

## Confirmed factual sources
- Walmart [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), fiscal year ended 31 Jan 2026, filed 13 Mar 2026: FY2024-FY2026 income statement figures (net sales, membership and other income, total revenue, cost of sales, SG&A, operating income, consolidated net income), cash flow items (D&A, CFO and cash capex) checked against official tables. See [provenance](PROJECT_DATA_PROVENANCE.md).
- UCI [Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients), dataset #350, DOI 10.24432/C55S3H, 30,000 records, 23 features, CC BY 4.0: official descriptive metadata verified, **not the raw observations or model's real-data execution**.
- Synthetic FP&A and invoice-reconciliation data are generated deterministically from code. They are **not 'factual' financial histories**, although their computed figures can be reproduced precisely.

## Corrections made after first edition
1. **Walmart sensitivity-table highlight:** prior file visually emphasized B8 (7.5% WACC/1.5% growth). Correct base assumptions (7.5%/2.5%) are in **D8**; the workbook now highlights D8.
2. **FP&A presentation:** earlier informal description could imply a Power BI artifact existed. It did not. Model is Excel and Matplotlib, and a build guide explicitly explains how to produce a real .pbix independently.
3. **FP&A PDF typography/negative variance labels:** corrected title rendering and negative-number placement.
4. **Role coverage:** added a new Finance Transformation / accounting-control project with testable invoice-to-ledger reconciliation to address actual job postings requiring validation and process improvements.

## Code and formula review
- Walmart historical accounting identities match reported values; base DCF total from five discounted FCFF estimates and terminal value; sensitivity base cell matches model EV.
- Retail FP&A revenue difference equals unit-volume plus unit-price contribution; operating profit difference reconciles to revenue less variable-cost and fixed-cost changes; Q4 forecast uses declared assumptions only.
- Credit-risk pipeline fits imputation and scaling on training data; current metrics and plots tagged synthetic; no inference to real-world bank performance.
- Reconciliation records validate cent-level monetary totals and matching; 8 unit tests cover duplicate, missing, extra, amount, department, counts and controls.
- The project does **not** claim 100% fault-free operation, actual employer work, validated Power BI files, proprietary data, calibrated live forecasts or superior chances of hiring.

## Known limits and conditions before resume publication
- Underlying Walmart future forecast assumptions (WACC, long-run growth, working-capital convention) are illustrative and **not independently supported by a live market comparables study**. No stock price target is produced.
- Real UCI data must be downloaded, checked and run before making empirical credit-risk claims. Only synthetic validation has been performed.
- Actual `.pbix` dashboard must be built and tested in Power BI Desktop; instructions are included but cannot substitute for it.
- Claims about project work should be limited to analyses the applicant has independently reproduced, checked and can explain. No quantified impact on co-op hiring odds can be established.
- Audit currently checks included data and generated artifacts; cannot validate future edits, different software environments or hidden bugs. See code/tests and reports for more detail.
