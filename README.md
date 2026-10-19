# Undergraduate Finance & Analytics Portfolio | Winter 2027 Co-op

A collection of four **educational finance and analytics case studies** featuring Excel models, Python analyses, written reports and transparent data sourcing. The projects explore valuation, budgeting and forecasting, credit risk, and finance-process controls. They are **not professional employment or client engagements**. Reported financials, synthetic datasets and forward-looking assumptions are labeled separately.

| Project | Core skill | Best-suited roles | Data origin |
|---|---|---|---|
| [01 Walmart fundamentals & DCF](01_Walmart_Valuation/) | Reported financials, cash-flow drivers, assumptions, sensitivity | Investment / Capital Markets / Corporate Finance | **Real SEC FY2024-26 reported data**, illustrative forecast |
| [02 Retail FP&A forecast](02_FP&A_Forecasting/) | Excel budgeting, price-volume profit bridge, scenarios, visual reporting | FP&A / Financial Analyst / Business Analyst | **Synthetic** company and transactions |
| [03 Credit-risk baseline](03_Credit_Risk/) | Statistical classification, train/test, evaluation | Lending / Risk / Data Analytics | **Synthetic demonstration only**; official UCI run is optional and pending |
| [04 Invoice-to-GL reconciliation](04_Finance_Reconciliation_Automation/) | Reconciliation, exception reports, quality controls, documented process | Finance Transformation / Reporting / Accounting | **Synthetic** invoices and journal entries; 8 automated tests |


## Quick execution
Install Python 3.10+ and dependencies:
```bash
python -m pip install -r requirements.txt
python 01_Walmart_Valuation/src/analysis.py
python '02_FP&A_Forecasting/src/analyze.py'
python '02_FP&A_Forecasting/src/q4_forecast.py'
python 03_Credit_Risk/src/analyze.py --mode synthetic
python 04_Finance_Reconciliation_Automation/src/reconcile.py
python -m unittest discover -s 04_Finance_Reconciliation_Automation/tests -v
python -m unittest discover -s tests -v
```
Run the commands from the repository root. For credit risk, `--mode uci` requires an official historical dataset download (not included). Scripts use paths relative to their own source files.

## Integrity, tools and evidence
- Reported Walmart historical numbers trace to Walmart FY2026 [SEC Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm). Only **reported historical financials** are real; projections and DCF values are **illustrative assumptions**.
- FP&A and reconciliation analyses depict **fictional businesses/transactions**. No claims about a real firm, confidential records, professional time savings, or validated predictions.
- The Credit Risk dataset from [UCI](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) is publicly described, but **not bundled or yet evaluated** here. Current demonstration plots and AUC use **synthetic data**.
- FP&A charts are made with Python/Matplotlib. **No Power BI .pbix file is supplied**, so do not claim this project is a Power BI dashboard. [Power BI next steps](02_FP&A_Forecasting/POWER_BI_BUILD_GUIDE.md) explain how to build one yourself.
- Python code, input CSVs, assumptions, calculations, reports, exception evidence and test commands are included. The model is not investment advice or lending policy.

See [SOURCE_AUDIT.md](SOURCE_AUDIT.md) and [data provenance](PROJECT_DATA_PROVENANCE.md) for sources, assumptions, validation checks and limitations.
