# BigQuery Security & Governance

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/security`

## Purpose
Setup access control, row-level security, column-level security, and audit logging for compliance and data governance.

## When to Use

**Trigger when:**
- Keywords: security, permission, RLS, access, IAM, privacy, GDPR
- User asks: "restrict access", "multi-tenant isolation", "hide sensitive data"

**Chat commands:**
```bash
/bigquery/security setup RLS for multi-tenant
/bigquery/security mask email column
/bigquery/security grant read access to user
/bigquery/security audit query access
```

## Requirements

<critical>
- BigQuery Admin or Data Owner role
- Dataset/table ownership
- IAM policy editor permissions
</critical>

---

## Row-Level Security (RLS)

### Multi-Tenant Isolation

```sql
-- Step 1: Create policy table
CREATE OR REPLACE TABLE `dataset.row_access_policies` AS
SELECT 'tenant_a' as tenant_id, 'user_a@example.com' as user_email
UNION ALL
SELECT 'tenant_b' as tenant_id, 'user_b@example.com' as user_email;

-- Step 2: Create row access policy
CREATE OR REPLACE ROW ACCESS POLICY tenant_filter
ON `dataset.events`
GRANT TO ('user_a@example.com', 'user_b@example.com')
FILTER USING (
  tenant_id IN (
    SELECT tenant_id FROM `dataset.row_access_policies`
    WHERE user_email = SESSION_USER()
  )
);
```

---

## Column-Level Security (Data Masking)

```sql
-- Apply policy tag to sensitive columns
ALTER TABLE `dataset.users`
ALTER COLUMN email
SET OPTIONS (policy_tags = ['projects/PROJECT/locations/LOCATION/taxonomies/TAXONOMY/policyTags/TAG']);

-- Users with maskedReader role see: "***@***.com"
```

---

## IAM Access Control

```bash
# Grant dataset access
bq update --dataset --access_control "role=READER,userByEmail=user@example.com" PROJECT:DATASET

# Grant BigQuery User role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:EMAIL" --role="roles/bigquery.user"
```

---

## Audit Logging

```sql
-- Track table access by user
SELECT
  DATE(creation_time) as date,
  user_email,
  referenced_tables[SAFE_OFFSET(0)].table_id as table,
  COUNT(*) as query_count
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date, user_email, table;
```

## Version
- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
