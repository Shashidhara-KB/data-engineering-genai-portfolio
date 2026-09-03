CREATE OR ALTER VIEW reporting.vw_FinancePerformance
AS
SELECT
    fiscal_year,
    fiscal_month,
    entity,
    account,
    currency,
    SUM(CASE WHEN scenario = 'ACT' THEN amount ELSE 0 END) AS actual_amount,
    SUM(CASE WHEN scenario = 'BUD' THEN amount ELSE 0 END) AS budget_amount,
    SUM(CASE WHEN scenario = 'FCST' THEN amount ELSE 0 END) AS forecast_amount,
    SUM(CASE WHEN scenario = 'ACT' THEN amount ELSE 0 END)
      - SUM(CASE WHEN scenario = 'BUD' THEN amount ELSE 0 END) AS actual_vs_budget
FROM gold.finance_pnl_summary
GROUP BY fiscal_year, fiscal_month, entity, account, currency;
GO
