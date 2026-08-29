# Dynamic Regional Row-Level Security

## Security Table

Create `SecurityUserRegion` with one row per authorized user and region:

| UserPrincipalName | Region |
|---|---|
| analyst.emea@example.com | EMEA |
| analyst.asia@example.com | Asia |

Relate `SecurityUserRegion[Region]` to `DimEntity[Region]` with a controlled security-filter path.

## Role Expression

Apply this expression to `SecurityUserRegion`:

```dax
LOWER ( SecurityUserRegion[UserPrincipalName] ) = LOWER ( USERPRINCIPALNAME () )
```

## Validation

- Test every role using **View as** in Power BI Desktop.
- Validate multi-region users and users with no mapping.
- Keep the security table governed and auditable.
- Do not use RLS as a substitute for workspace and app permissions.

