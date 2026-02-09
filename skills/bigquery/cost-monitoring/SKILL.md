# BigQuery Cost Monitoring

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/cost-monitoring`

## Purpose
Track, analyze, and optimize BigQuery spending across projects, users, and queries.

## When to Use

**Trigger when:**
- Keywords: cost, expensive, budget, billing, spending, slots
- User asks: "how much am I spending", "why is this expensive", "reduce costs"

**Chat commands:**
```bash
/bigquery/cost-monitoring show me expensive queries
/bigquery/cost-monitoring analyze last month costs
/bigquery/cost-monitoring find queries over 10GB
/bigquery/cost-monitoring setup budget alerts
```

## Requirements

<critical>
- Access to INFORMATION_SCHEMA.JOBS_BY_PROJECT
- Billing account access (for cost attribution)
- BigQuery Data Transfer API (for exports)
</critical>

---

## Understanding BigQuery Costs

### Pricing Components

**1. Query Processing (On-Demand)**
- $6.25 per TB processed (first 1TB/month free)
- Billed by bytes scanned, not bytes returned

**2. Storage**
- $0.02/GB/month (active storage, 0-90 days)
- $0.01/GB/month (long-term storage, 90+ days)

**3. Streaming Inserts**
- $0.01 per 200MB

**4. BigQuery ML**
- CREATE MODEL: $250 per TB
- ML.PREDICT: $5 per TB
- ML.EVALUATE: $5 per TB

**5. Data Transfer**
- Export to GCS: $0.011 per GB

---

## Cost Analysis Queries

### 1. Find Most Expensive Queries (Last 7 Days)

```sql
SELECT
  user_email,
  job_id,
  creation_time,
  total_bytes_processed / POW(10, 12) as tb_processed,
  total_bytes_processed / POW(10, 12) * 6.25 as estimated_cost_usd,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_seconds,
  SUBSTR(query, 1, 100) as query_preview
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
  AND total_bytes_processed > 0
ORDER BY estimated_cost_usd DESC
LIMIT 20;
```

### 2. Cost by User (Last Month)

```sql
SELECT
  user_email,
  COUNT(*) as query_count,
  SUM(total_bytes_processed) / POW(10, 12) as total_tb_processed,
  SUM(total_bytes_processed) / POW(10, 12) * 6.25 as estimated_cost_usd,
  AVG(total_bytes_processed) / POW(10, 9) as avg_gb_per_query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
GROUP BY user_email
ORDER BY estimated_cost_usd DESC;
```

### 3. Cost by Project/Dataset

```sql
SELECT
  project_id,
  referenced_tables[SAFE_OFFSET(0)].dataset_id as dataset,
  COUNT(*) as queries,
  SUM(total_bytes_processed) / POW(10, 12) as tb_processed,
  SUM(total_bytes_processed) / POW(10, 12) * 6.25 as cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_type = 'QUERY'
GROUP BY project_id, dataset
ORDER BY cost_usd DESC;
```

### 4. Daily Cost Trend

```sql
SELECT
  DATE(creation_time) as date,
  COUNT(*) as queries,
  SUM(total_bytes_processed) / POW(10, 12) as tb_processed,
  SUM(total_bytes_processed) / POW(10, 12) * 6.25 as cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
GROUP BY date
ORDER BY date DESC;
```

### 5. Multi-Tenant Cost Attribution

```sql
-- Extract tenant_id from query
SELECT
  REGEXP_EXTRACT(query, r"tenant_id = '([^']+)'") as tenant_id,
  COUNT(*) as queries,
  SUM(total_bytes_processed) / POW(10, 12) * 6.25 as cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND query LIKE '%tenant_id%'
GROUP BY tenant_id
ORDER BY cost_usd DESC;
```

---

## Storage Cost Analysis

### 6. Storage by Table

```sql
SELECT
  table_schema as dataset,
  table_name,
  ROUND(size_bytes / POW(10, 9), 2) as size_gb,
  ROUND(size_bytes / POW(10, 9) * 0.02, 2) as monthly_cost_usd,
  creation_time,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), creation_time, DAY) as age_days,
  CASE 
    WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), creation_time, DAY) > 90 
    THEN 'long-term'
    ELSE 'active'
  END as storage_class
FROM `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE project_id = 'your_project'
ORDER BY size_bytes DESC
LIMIT 50;
```

### 7. Find Tables to Archive/Delete

```sql
-- Tables not queried in 90 days
WITH table_access AS (
  SELECT
    referenced_tables[SAFE_OFFSET(0)].table_id as table_name,
    MAX(creation_time) as last_query
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  GROUP BY table_name
)
SELECT
  t.table_name,
  t.size_gb,
  t.monthly_cost_usd,
  a.last_query,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), a.last_query, DAY) as days_since_last_query
FROM (
  SELECT
    table_name,
    ROUND(size_bytes / POW(10, 9), 2) as size_gb,
    ROUND(size_bytes / POW(10, 9) * 0.02, 2) as monthly_cost_usd
  FROM `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE
) t
LEFT JOIN table_access a USING (table_name)
WHERE a.last_query IS NULL 
   OR TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), a.last_query, DAY) > 90
ORDER BY t.monthly_cost_usd DESC;
```

---

## Budget Alerts

### Setup Budget Alert (Console)

1. Go to **Billing** → **Budgets & alerts**
2. Create budget:
   - Name: `BigQuery Monthly Budget`
   - Projects: Select your project
   - Services: Select **BigQuery**
   - Amount: $500/month
   - Alerts: 50%, 90%, 100%
3. Add email notifications

### Setup Budget Alert (CLI)

```bash
gcloud billing budgets create \
  --billing-account=012345-567890-ABCDEF \
  --display-name="BigQuery Monthly Budget" \
  --budget-amount=500 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100 \
  --all-updates-rule-monitoring-notification-channels=CHANNEL_ID
```

---

## Cost Optimization Strategies

### 1. Partition and Cluster Tables

```sql
-- Before: Full table scan every query
SELECT * FROM events WHERE DATE(timestamp) = '2024-02-09';
-- Cost: Scans entire table

-- After: Partitioned table
CREATE OR REPLACE TABLE events_partitioned
PARTITION BY DATE(timestamp)
CLUSTER BY user_id
AS SELECT * FROM events;

SELECT * FROM events_partitioned 
WHERE DATE(timestamp) = '2024-02-09';
-- Cost: Scans only 1 day partition (90%+ savings)
```

### 2. Use Materialized Views

```sql
-- Expensive query run multiple times per day
SELECT
  user_id,
  COUNT(*) as events,
  MAX(timestamp) as last_event
FROM events
GROUP BY user_id;

-- Create materialized view (auto-refreshed)
CREATE MATERIALIZED VIEW mv_user_summary AS
SELECT
  user_id,
  COUNT(*) as events,
  MAX(timestamp) as last_event
FROM events
GROUP BY user_id;

-- Query MV instead (much cheaper)
SELECT * FROM mv_user_summary WHERE events > 10;
```

### 3. Set Table Expiration

```sql
-- Auto-delete old data
ALTER TABLE dataset.temp_table
SET OPTIONS (
  expiration_timestamp = TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
);
```

### 4. Use Query Result Caching

```bash
# Results cached for 24 hours (free)
# Rerun same query = $0 cost

# Disable cache for testing
bq query --use_cache=false "SELECT ..."
```

### 5. Limit with LIMIT (Development)

```sql
-- Development: Use LIMIT
SELECT * FROM large_table LIMIT 1000;

-- Production: Use WHERE filters
SELECT * FROM large_table 
WHERE DATE(timestamp) = CURRENT_DATE();
```

---

## Monitoring Dashboard (Looker Studio)

### Setup Cost Dashboard

```sql
-- Create daily cost summary table
CREATE OR REPLACE TABLE `dataset.daily_costs` AS
SELECT
  DATE(creation_time) as date,
  user_email,
  COUNT(*) as queries,
  SUM(total_bytes_processed) / POW(10, 12) as tb_processed,
  SUM(total_bytes_processed) / POW(10, 12) * 6.25 as cost_usd,
  AVG(TIMESTAMP_DIFF(end_time, start_time, SECOND)) as avg_duration_sec
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
GROUP BY date, user_email;

-- Schedule to run daily (see /scheduled-queries)
```

**Connect to Looker Studio:**
1. Create new report
2. Add BigQuery connector
3. Select `dataset.daily_costs` table
4. Create charts:
   - Line chart: cost_usd by date
   - Bar chart: cost_usd by user_email
   - Scorecard: Total cost this month

---

## Slot Usage (For Reservations)

### Monitor Slot Utilization

```sql
SELECT
  job_id,
  user_email,
  total_slot_ms / 1000 as slot_seconds,
  total_bytes_processed / POW(10, 9) as gb_processed,
  total_slot_ms / (TIMESTAMP_DIFF(end_time, start_time, MILLISECOND) + 1) as avg_slots
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
ORDER BY total_slot_ms DESC
LIMIT 20;
```

---

## Vietnamese Use Case: Multi-Tenant Cost Tracking

```sql
-- Track costs per tenant for billing
CREATE OR REPLACE TABLE `dataset.tenant_costs` AS
WITH tenant_queries AS (
  SELECT
    DATE(creation_time) as date,
    REGEXP_EXTRACT(query, r"tenant_id = '([^']+)'") as tenant_id,
    total_bytes_processed
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    AND query LIKE '%tenant_id%'
)
SELECT
  tenant_id,
  date,
  COUNT(*) as queries,
  SUM(total_bytes_processed) / POW(10, 12) as tb_processed,
  SUM(total_bytes_processed) / POW(10, 12) * 6.25 as cost_usd
FROM tenant_queries
WHERE tenant_id IS NOT NULL
GROUP BY tenant_id, date
ORDER BY tenant_id, date;

-- Monthly billing report
SELECT
  tenant_id,
  SUM(cost_usd) as monthly_cost,
  SUM(queries) as total_queries
FROM `dataset.tenant_costs`
WHERE date >= DATE_TRUNC(CURRENT_DATE(), MONTH)
GROUP BY tenant_id
ORDER BY monthly_cost DESC;
```

---

## Cost Alerts with Cloud Functions

```python
# Cloud Function triggered on budget threshold
def budget_alert(data, context):
    import smtplib
    from google.cloud import bigquery
    
    client = bigquery.Client()
    
    # Get current month costs
    query = """
    SELECT SUM(total_bytes_processed) / POW(10,12) * 6.25 as cost
    FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
    WHERE DATE(creation_time) >= DATE_TRUNC(CURRENT_DATE(), MONTH)
    """
    
    result = client.query(query).result()
    cost = list(result)[0].cost
    
    if cost > 400:  # $400 threshold
        # Send alert email
        send_email(f"BigQuery costs: ${cost:.2f} this month")
```

---

## Quick Cost Reduction Checklist

- [ ] Partition tables by date
- [ ] Cluster frequently filtered columns
- [ ] Use materialized views for repeated queries
- [ ] Avoid SELECT * in production
- [ ] Set table expiration for temp tables
- [ ] Use query result caching
- [ ] Monitor and optimize top 10 expensive queries
- [ ] Delete unused tables/datasets
- [ ] Use table sampling for development

---

## Integration with Other Skills

**Workflow:**
1. Identify expensive queries → `/bigquery/cost-monitoring`
2. Optimize queries → `/bigquery/query-optimization`
3. Improve schema → `/bigquery/schema-design`
4. Automate monitoring → `/bigquery/scheduled-queries`

---

## Quick Reference

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Query cost | TB processed × $6.25 | <$1 per query |
| Storage cost | GB × $0.02/month | Archive after 90 days |
| Daily budget | Monthly budget / 30 | Track daily |
| Cost per user | User costs / total costs | Find top spenders |

## Version

- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
