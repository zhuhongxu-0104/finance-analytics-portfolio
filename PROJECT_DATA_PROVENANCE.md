# Project source / provenance register (verified October 19, 2026)

| Project | Primary evidence | Status | What is actually real? |
|---|---|---|---|
| 01 Walmart historical | SEC Walmart FY2026 10-K [official HTML](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) (Income Statement p.52, Cash Flow p.56) | Source entries compared with official rows | Revenue, operating income, net income, D&A, operating cash flow and capex, FY2024-26, USD millions |
| 01 Walmart forecasts | Student-case inputs in Excel and Python | Assumptions, not externally verified facts | All FY2027-31 forecasts, tax, WACC, terminal value, DCF enterprise value are **illustrative** |
| 02 FP&A budget / actual / Q4 | NumPy synthetic generator `src/generate_data.py`, seed 20261019 | Reproducible synthetic | **No real company's budget or financial results** |
| 03 credit-risk demo | NumPy synthetic generator `src/make_demo.py`, seed 20261019 | Demo evaluated; results are synthetic | **No genuine bank records or actual UCI observations processed in bundled results** |
| 03 future real UCI dataset | [UCI dataset #350](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients), Yeh (2009), DOI [10.24432/C55S3H](https://doi.org/10.24432/C55S3H), CC BY 4.0 | Official metadata verified, original raw observations **not downloaded or executed here** | 30,000 historical Taiwanese customer records / 23 predictors; do not infer Canadian population performance |
| 04 invoice / GL control | Python standard-library synthetic generator, seed 20261019, scripted injected anomalies | Reproduced, 8 passing tests | 72 fictional invoices, 73 fictional journal entries, not employer records |

## Historical Walmart 10-K cross-check

| USD millions | FY2024 | FY2025 | FY2026 |
|---|---:|---:|---:|
| Total revenue | 648,125 | 680,985 | 713,163 |
| Operating income | 27,012 | 29,348 | 29,825 |
| Consolidated net income | 16,270 | 20,157 | 22,270 |
| Operating cash flow | 35,726 | 36,443 | 41,565 |
| Capital expenditure (cash paid, listed as positive) | 20,606 | 23,783 | 26,642 |
| Depreciation & amortization | 11,853 | 12,973 | 14,203 |

Financial statements report capex as a negative cash-flow outlay; model stores capex positive and subtracts it. Walmart company-defined FCF (`CFO - capex`) is not unlevered FCFF used in the forecast model.

Absolute certainty is impossible for software and assumptions; [SOURCE_AUDIT.md](SOURCE_AUDIT.md) documents exact checks and residual limitations.
