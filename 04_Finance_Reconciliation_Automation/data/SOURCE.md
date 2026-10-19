# Data lineage and integrity

- **All transactions are invented** by `src/generate_data.py`; there is no real corporate or client data.
- Every 2026 date, vendor name, departmental assignment, and invoice amount is fictional.
- Seed `20261019` makes the generation reproducible.
- Anomalies inserted deliberately: missing GL postings INV-0011 and INV-0044; amount changes INV-0020 and INV-0033; department mismatch INV-0055; duplicate GL INV-0066; GL-only EXT-0001 and EXT-0002.
- Summaries and plots were computed from the generated CSVs by code and checked with unit tests.
