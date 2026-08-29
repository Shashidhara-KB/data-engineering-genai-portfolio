CREATE TABLE dbo.DimDate (
    DateKey        int          NOT NULL PRIMARY KEY,
    [Date]         date         NOT NULL UNIQUE,
    FiscalYear     smallint     NOT NULL,
    FiscalMonth    tinyint      NOT NULL,
    MonthName      varchar(10)  NOT NULL,
    FiscalQuarter  char(2)      NOT NULL
);

CREATE TABLE dbo.DimEntity (
    EntityKey      int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    EntityCode     varchar(20)  NOT NULL UNIQUE,
    EntityName     varchar(100) NOT NULL,
    CountryName    varchar(100) NOT NULL,
    Region         varchar(30)  NOT NULL
);

CREATE TABLE dbo.DimAccount (
    AccountKey      int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    AccountCode     varchar(20)  NOT NULL UNIQUE,
    AccountName     varchar(100) NOT NULL,
    PnLGroup        varchar(50)  NOT NULL,
    DisplayOrder    smallint     NOT NULL,
    FavorabilitySign smallint    NOT NULL CHECK (FavorabilitySign IN (-1, 1))
);

CREATE TABLE dbo.DimCostCenter (
    CostCenterKey  int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    CostCenterCode varchar(20)  NOT NULL UNIQUE,
    CostCenterName varchar(100) NOT NULL,
    FunctionName   varchar(50)  NOT NULL
);

CREATE TABLE dbo.DimScenario (
    ScenarioKey    int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    ScenarioCode   varchar(10)  NOT NULL UNIQUE,
    ScenarioName   varchar(50)  NOT NULL,
    ScenarioOrder  tinyint      NOT NULL
);

CREATE TABLE dbo.FactFinance (
    FinanceKey     bigint IDENTITY(1,1) NOT NULL PRIMARY KEY,
    DateKey        int          NOT NULL,
    EntityKey      int          NOT NULL,
    AccountKey     int          NOT NULL,
    CostCenterKey  int          NOT NULL,
    ScenarioKey    int          NOT NULL,
    PostingDate    date         NOT NULL,
    CurrencyCode   char(3)      NOT NULL,
    Amount         decimal(19,2) NOT NULL,
    LoadTimestamp  datetime2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_FactFinance_Date FOREIGN KEY (DateKey) REFERENCES dbo.DimDate(DateKey),
    CONSTRAINT FK_FactFinance_Entity FOREIGN KEY (EntityKey) REFERENCES dbo.DimEntity(EntityKey),
    CONSTRAINT FK_FactFinance_Account FOREIGN KEY (AccountKey) REFERENCES dbo.DimAccount(AccountKey),
    CONSTRAINT FK_FactFinance_CostCenter FOREIGN KEY (CostCenterKey) REFERENCES dbo.DimCostCenter(CostCenterKey),
    CONSTRAINT FK_FactFinance_Scenario FOREIGN KEY (ScenarioKey) REFERENCES dbo.DimScenario(ScenarioKey)
);

CREATE UNIQUE INDEX UX_FactFinance_Grain
ON dbo.FactFinance (
    DateKey,
    EntityKey,
    AccountKey,
    CostCenterKey,
    ScenarioKey,
    CurrencyCode
);

INSERT INTO dbo.DimScenario (ScenarioCode, ScenarioName, ScenarioOrder)
VALUES
    ('ACT', 'Actual', 1),
    ('BUD', 'Budget', 2),
    ('FCST', 'Forecast', 3),
    ('PY', 'Prior Year', 4);

INSERT INTO dbo.DimEntity (EntityCode, EntityName, CountryName, Region)
VALUES
    ('E001', 'North Manufacturing', 'Netherlands', 'EMEA'),
    ('E002', 'Central Manufacturing', 'Germany', 'EMEA'),
    ('E003', 'Asia Manufacturing', 'Singapore', 'Asia');

INSERT INTO dbo.DimAccount
    (AccountCode, AccountName, PnLGroup, DisplayOrder, FavorabilitySign)
VALUES
    ('400000', 'Net Sales', 'Revenue', 10, 1),
    ('500000', 'Raw Materials', 'Variable Cost', 20, -1),
    ('610000', 'Personnel Cost', 'Fixed Cost', 30, -1),
    ('690000', 'Other Operating Cost', 'Fixed Cost', 40, -1);

INSERT INTO dbo.DimCostCenter (CostCenterCode, CostCenterName, FunctionName)
VALUES
    ('CC100', 'Operations', 'Manufacturing'),
    ('CC200', 'Supply Chain', 'Supply Chain'),
    ('CC300', 'Finance', 'Finance');

-- Example synthetic fact rows. Production loads should use a controlled
-- staging-and-MERGE process with reconciliation and audit checks.
INSERT INTO dbo.FactFinance
    (DateKey, EntityKey, AccountKey, CostCenterKey, ScenarioKey, PostingDate, CurrencyCode, Amount)
VALUES
    (20260131, 1, 1, 1, 1, '2026-01-31', 'EUR', 1250000.00),
    (20260131, 1, 1, 1, 2, '2026-01-31', 'EUR', 1200000.00),
    (20260131, 1, 2, 1, 1, '2026-01-31', 'EUR', -460000.00),
    (20260131, 1, 2, 1, 2, '2026-01-31', 'EUR', -440000.00);

