# Finance transformation case: example current-state vs proposed-state

**Educational, fictional process. This is not a record of an employer's actual control system.**

## Current-state illustrative process
```mermaid
flowchart LR
  A[Export invoices and GL] --> B[Manual VLOOKUP checking]
  B --> C[Email issues to finance team]
  C --> D[Manual sign-off]
```

## Proposed automated control
```mermaid
flowchart TD
  A[Read invoice CSV and GL CSV] --> B[Check IDs and currency values]
  B --> C[Group by invoice ID]
  C --> D{Match amounts, count and department?}
  D -->|Yes| E[Mark matched]
  D -->|No| F[Add to exception queue]
  E --> G[Reconcile control totals]
  F --> G
  G --> H[Reviewer checks and documents resolution]
```

## Example testing/acceptance criteria
- An invoice missing from GL must be flagged and present in the exception queue.
- An extra GL posting must not silently pass a matched invoice.
- Dollar differences must be exact to cents and traceable to source rows.
- Total register and GL monetary amounts must reconcile to the difference reported.
- A human analyst reviews potential false positives before any accounting adjustment.
