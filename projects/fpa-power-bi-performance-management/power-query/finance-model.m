let
    // ParameterServer and ParameterDatabase are Power BI parameters.
    // Authentication is configured in the Power BI service or gateway.
    Source = Sql.Database(
        ParameterServer,
        ParameterDatabase,
        [
            Query = "
                SELECT
                    FinanceKey,
                    DateKey,
                    EntityKey,
                    AccountKey,
                    CostCenterKey,
                    ScenarioKey,
                    PostingDate,
                    CurrencyCode,
                    Amount,
                    LoadTimestamp
                FROM dbo.FactFinance
                WHERE PostingDate >= DATEADD(year, -3, CAST(GETDATE() AS date));"
        ]
    ),
    TypedColumns = Table.TransformColumnTypes(
        Source,
        {
            {"FinanceKey", Int64.Type},
            {"DateKey", Int64.Type},
            {"EntityKey", Int64.Type},
            {"AccountKey", Int64.Type},
            {"CostCenterKey", Int64.Type},
            {"ScenarioKey", Int64.Type},
            {"PostingDate", type date},
            {"CurrencyCode", type text},
            {"Amount", Currency.Type},
            {"LoadTimestamp", type datetime}
        }
    ),
    ValidRows = Table.SelectRows(
        TypedColumns,
        each [EntityKey] <> null and [AccountKey] <> null and [ScenarioKey] <> null
    )
in
    ValidRows

