# Finance transaction data contract

| Column | Type after Silver processing | Rule |
|---|---|---|
| record_id | string | Required; latest `updated_at` wins |
| posting_date | date | Required and parseable |
| entity | string | Required; trimmed and upper-cased |
| account | string | Required; trimmed and upper-cased |
| cost_center | string | Trimmed and upper-cased |
| scenario | string | ACT, BUD or FCST |
| currency | string | Three-letter uppercase code |
| amount | decimal(19,2) | Required and numeric |
| updated_at | timestamp | Used for record deduplication |

Rejected records are retained in the quarantine dataset with one `quality_error`
value. This makes failed loads traceable instead of silently discarding data.
