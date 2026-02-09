# BigQuery Troubleshooting

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/troubleshooting`

## Purpose
Debug errors, resolve common issues, and fix BigQuery problems.

## When to Use

**Trigger when:**
- Keywords: error, fail, debug, troubleshoot, fix, problem
- User encounters: permissions errors, quota errors, syntax errors

**Chat commands:**
```bash
/bigquery/troubleshooting fix error "Resources exceeded"
/bigquery/troubleshooting debug permission denied
/bigquery/troubleshooting resolve syntax error in query
```

---

## Common Errors & Solutions

### 1. Permission Denied (403)

**Error:**
```
Access Denied: BigQuery BigQuery: Permission denied while getting Drive credentials
```

**Solutions:**
```bash
# Grant necessary role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:EMAIL" \
  --role="roles/bigquery.dataViewer"

# Check current permissions
bq show --dataset PROJECT:DATASET
```

### 2. Resources Exceeded (400)

**Error:**
```
Resources exceeded during query execution
```

**Solutions:**
```sql
-- Use partition filter
SELECT * FROM events
WHERE DATE(timestamp) = '2024-02-09'  -- Add partition filter
LIMIT 1000;

-- Break into smaller queries
-- Use LIMIT for development
-- Add more WHERE filters
```

### 3. Syntax Errors (400)

**Error:**
```
Syntax error: Expected end of input but got keyword SELECT
```

**Common causes:**
- Missing comma in SELECT
- Wrong JOIN syntax
- Unclosed parenthesis
- Reserved keyword as column name

**Solutions:**
```sql
-- ❌ Wrong
SELECT
  user_id
  event_name  -- Missing comma
FROM events;

-- ✅ Correct
SELECT
  user_id,
  event_name
FROM events;

-- Escape reserved keywords
SELECT `user`, `group` FROM table;
```

### 4. Table Not Found (404)

**Error:**
```
Not found: Table PROJECT:dataset.table
```

**Solutions:**
```bash
# Check table exists
bq ls PROJECT:dataset

# Check project/dataset name
bq show PROJECT:dataset.table

# Use fully qualified name
SELECT * FROM `project.dataset.table`;
```

### 5. Quota Exceeded (429)

**Error:**
```
Quota exceeded: Your project exceeded quota for concurrent queries
```

**Solutions:**
- Wait and retry
- Reduce concurrent queries
- Request quota increase
- Use reservations for guaranteed slots

### 6. Schema Mismatch

**Error:**
```
Cannot convert value to type INT64
```

**Solutions:**
```sql
-- Use SAFE_CAST instead of CAST
SELECT
  SAFE_CAST(price AS FLOAT64) as price,
  SAFE_CAST(quantity AS INT64) as quantity
FROM table;

-- Check for NULL values
SELECT * FROM table WHERE price IS NULL;
```

### 7. JOIN Producing Too Many Rows

**Error:**
```
Query exceeded resource limits
```

**Debug:**
```sql
-- Check cardinality before JOIN
SELECT COUNT(*) FROM table1;  -- 1000 rows
SELECT COUNT(*) FROM table2;  -- 1000 rows

-- After JOIN
SELECT COUNT(*)
FROM table1
JOIN table2 USING (user_id);  -- 100,000 rows?! Row explosion!

-- Fix: Add QUALIFY to deduplicate
SELECT *
FROM table1
JOIN (
  SELECT *
  FROM table2
  QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) = 1
) USING (user_id);
```

---

## Debugging Queries

### Use EXPLAIN

```sql
-- See execution plan
EXPLAIN
SELECT *
FROM events
WHERE DATE(timestamp) = '2024-02-09';

-- Look for:
-- - Partition pruning (should say "partition filter applied")
-- - Full table scans
-- - Large shuffle operations
```

### Dry Run (Estimate Cost)

```bash
# Check bytes processed without running
bq query --dry_run "SELECT * FROM events WHERE DATE(timestamp) = '2024-02-09'"
```

### Query Validator

```python
from google.cloud import bigquery

client = bigquery.Client()

# Validate query
query = "SELECT * FROM dataset.table WHERE date = '2024-02-09'"

job_config = bigquery.QueryJobConfig(dry_run=True)

try:
    query_job = client.query(query, job_config=job_config)
    print(f"✅ Query valid. Will process {query_job.total_bytes_processed:,} bytes")
except Exception as e:
    print(f"❌ Query error: {e}")
```

---

## Performance Issues

### Slow Query Diagnosis

```sql
-- Find slow queries
SELECT
  job_id,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_sec,
  total_bytes_processed / POW(10,9) as gb_processed,
  total_slot_ms / 1000 as slot_seconds,
  SUBSTR(query, 1, 100) as query_preview
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND state = 'DONE'
ORDER BY duration_sec DESC
LIMIT 10;
```

**Common fixes:**
- Add partition filter
- Remove DISTINCT
- Optimize JOINs
- Use clustering
- See `/bigquery/query-optimization`

---

## Data Quality Issues

### Find NULL Values

```sql
SELECT
  COUNTIF(column1 IS NULL) as column1_nulls,
  COUNTIF(column2 IS NULL) as column2_nulls,
  COUNT(*) as total_rows
FROM dataset.table;
```

### Find Duplicates

```sql
SELECT
  user_id,
  COUNT(*) as count
FROM dataset.users
GROUP BY user_id
HAVING count > 1;
```

### Data Type Mismatches

```sql
-- Find non-numeric values in "numeric" STRING column
SELECT price
FROM products
WHERE SAFE_CAST(price AS FLOAT64) IS NULL
  AND price IS NOT NULL;
```

---

## Loading Errors

### CSV Load Failures

**Error:**
```
Error while reading table: CSV table encountered too many errors
```

**Debug:**
```bash
# Allow some bad records
bq load --max_bad_records=100 \
  --source_format=CSV \
  dataset.table \
  gs://bucket/file.csv
```

### JSON Parse Errors

```bash
# Use --autodetect with caution
bq load --source_format=NEWLINE_DELIMITED_JSON \
  --max_bad_records=10 \
  dataset.table \
  gs://bucket/data.json
```

---

## Vietnamese-Specific Issues

### UTF-8 Encoding

```python
# Ensure UTF-8 for Vietnamese characters
job_config = bigquery.LoadJobConfig(
    encoding='UTF-8',
    source_format=bigquery.SourceFormat.CSV
)
```

### Timezone Issues

```sql
-- Convert to Vietnam time
SELECT
  DATETIME(timestamp, 'Asia/Ho_Chi_Minh') as vietnam_time
FROM events;
```

---

## Emergency Fixes

### Kill Running Query

```bash
bq cancel JOB_ID
```

### Restore Deleted Table (Time Travel)

```sql
-- Restore table from 2 hours ago
CREATE OR REPLACE TABLE `dataset.table_restored` AS
SELECT * FROM `dataset.table`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR);
```

### Recover from Accidental DELETE

```sql
-- Deleted data in last hour? Restore it
INSERT INTO `dataset.table`
SELECT * FROM `dataset.table`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
WHERE id NOT IN (SELECT id FROM `dataset.table`);
```

---

## Quick Diagnostics Checklist

- [ ] Check error message carefully
- [ ] Verify permissions (IAM roles)
- [ ] Validate SQL syntax
- [ ] Check table/dataset exists
- [ ] Confirm partition filter present
- [ ] Review JOIN conditions
- [ ] Test with LIMIT 10 first
- [ ] Use dry run to estimate cost
- [ ] Check quota limits
- [ ] Review recent schema changes

---

## Getting Help

**Error persists?**
1. Copy full error message
2. Check BigQuery Status Dashboard
3. Review audit logs
4. Contact GCP Support with job_id

**For optimization:**
- Use `/bigquery/query-optimization`
- Check execution plan with EXPLAIN
- Monitor with `/bigquery/cost-monitoring`

---

## Common Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 400 | Syntax/invalid query | Check SQL syntax |
| 403 | Permission denied | Grant IAM roles |
| 404 | Not found | Verify table exists |
| 429 | Quota exceeded | Wait or request increase |
| 500 | Internal error | Retry, contact support |

## Version
- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
