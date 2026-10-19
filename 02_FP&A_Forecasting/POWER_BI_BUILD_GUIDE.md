# Optional Power BI Desktop Dashboard | Build It Yourself

**Status: INSTRUCTIONS ONLY, not a completed `.pbix`.** The repository currently contains working Excel and Python charts, not an actual Power BI report. Do **not** put 'built in Power BI' on your resume for this case unless you personally build it in Power BI Desktop.

**Data:** All numbers are synthetic. `data/monthly_budget_actual_synthetic.csv` is produced by `src/generate_data.py` with fixed seed 20261019. The ready-made `outputs/monthly_variance_summary.csv` may simplify a first dashboard, but calculating measures from raw product-month data is a stronger exercise.

## Power BI Desktop 15-30 minute build plan
1. In Power BI Desktop: Home > Get Data > Text/CSV > import `data/monthly_budget_actual_synthetic.csv`.
2. Name the table `Retail`; check `month` is text or convert to date, and amounts and units are numeric.
3. Add the following DAX **measures** in Modeling > New Measure, using the exact table name:
```dax
Budget Revenue = SUMX(Retail, Retail[budget_units] * Retail[budget_price_usd])
Actual Revenue = SUMX(Retail, Retail[actual_units] * Retail[actual_price_usd])
Revenue Variance = [Actual Revenue] - [Budget Revenue]
Revenue Variance % = DIVIDE([Revenue Variance], [Budget Revenue])
Budget Profit = SUMX(Retail, Retail[budget_units] * (Retail[budget_price_usd] - Retail[budget_variable_cost_per_unit_usd]) - Retail[budget_fixed_opex_usd])
Actual Profit = SUMX(Retail, Retail[actual_units] * (Retail[actual_price_usd] - Retail[actual_variable_cost_per_unit_usd]) - Retail[actual_fixed_opex_usd])
Profit Variance = [Actual Profit] - [Budget Profit]
```
4. Add cards for budget revenue, actual revenue, revenue variance %, and actual operating profit.
5. Add a clustered column chart using `month` on X and `[Budget Revenue]`, `[Actual Revenue]` on Y; repeat for profit.
6. Add a table by `product` with budget, actual and variance measures. Add month and product slicers.
7. Add visible report subtitle `SYNTHETIC REVENUE AND BUDGET SCENARIO — educational data only`.
8. Test that total actual revenue is **$7,235,861.76**, total budget revenue is **$7,283,614.00**, and actual profit is **$522,943.71** before calling it complete.
9. Save the `.pbix`, optionally commit it to your own GitHub repository; export a screenshot for README (do not use Matplotlib images as proof of Power BI proficiency).

**Note:** You can learn the import and visual-building workflow from [Microsoft's official Financial Sample documentation](https://learn.microsoft.com/en-us/power-bi/create-reports/sample-financial-download), but this project's CSV remains fully custom synthetic data, not the Microsoft sample.
