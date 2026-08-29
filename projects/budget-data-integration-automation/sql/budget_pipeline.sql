CREATE TABLE dbo.BudgetStaging (
    LoadRunId      uniqueidentifier NOT NULL,
    BusinessKey    varchar(100)     NOT NULL,
    EntityCode     varchar(20)      NOT NULL,
    AccountCode    varchar(20)      NOT NULL,
    CostCenterCode varchar(20)      NOT NULL,
    CurrencyCode   char(3)          NOT NULL,
    Jan decimal(19,2) NULL, Feb decimal(19,2) NULL, Mar decimal(19,2) NULL,
    Apr decimal(19,2) NULL, May decimal(19,2) NULL, Jun decimal(19,2) NULL,
    Jul decimal(19,2) NULL, Aug decimal(19,2) NULL, Sep decimal(19,2) NULL,
    Oct decimal(19,2) NULL, Nov decimal(19,2) NULL, [Dec] decimal(19,2) NULL,
    LoadedAt datetime2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.BudgetFinal (
    BusinessKey    varchar(100) NOT NULL PRIMARY KEY,
    EntityCode     varchar(20)  NOT NULL,
    AccountCode    varchar(20)  NOT NULL,
    CostCenterCode varchar(20)  NOT NULL,
    CurrencyCode   char(3)      NOT NULL,
    Jan decimal(19,2) NULL, Feb decimal(19,2) NULL, Mar decimal(19,2) NULL,
    Apr decimal(19,2) NULL, May decimal(19,2) NULL, Jun decimal(19,2) NULL,
    Jul decimal(19,2) NULL, Aug decimal(19,2) NULL, Sep decimal(19,2) NULL,
    Oct decimal(19,2) NULL, Nov decimal(19,2) NULL, [Dec] decimal(19,2) NULL,
    RefreshedAt datetime2(0) NOT NULL
);
GO

CREATE OR ALTER PROCEDURE dbo.usp_RefreshBudgetFinal @LoadRunId uniqueidentifier
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    IF EXISTS (
        SELECT BusinessKey FROM dbo.BudgetStaging
        WHERE LoadRunId = @LoadRunId GROUP BY BusinessKey HAVING COUNT(*) > 1
    ) THROW 50001, 'Duplicate business keys detected in staging.', 1;

    BEGIN TRANSACTION;
        DELETE FROM dbo.BudgetFinal;
        INSERT INTO dbo.BudgetFinal (
            BusinessKey, EntityCode, AccountCode, CostCenterCode, CurrencyCode,
            Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, [Dec], RefreshedAt
        )
        SELECT BusinessKey, EntityCode, AccountCode, CostCenterCode, CurrencyCode,
               Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, [Dec], SYSUTCDATETIME()
        FROM dbo.BudgetStaging WHERE LoadRunId = @LoadRunId;
    COMMIT TRANSACTION;
END;
GO

CREATE OR ALTER VIEW dbo.vw_BudgetReporting
AS
SELECT
    B.BusinessKey, B.EntityCode, B.AccountCode, B.CostCenterCode, B.CurrencyCode,
    P.Period, P.Amount, B.RefreshedAt
FROM dbo.BudgetFinal AS B
CROSS APPLY (VALUES
    (1, B.Jan), (2, B.Feb), (3, B.Mar), (4, B.Apr), (5, B.May), (6, B.Jun),
    (7, B.Jul), (8, B.Aug), (9, B.Sep), (10, B.Oct), (11, B.Nov), (12, B.[Dec])
) AS P(Period, Amount);
GO
