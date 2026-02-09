# BigQuery Scheduled Queries

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/scheduled-queries`

## Purpose
Automate recurring queries, ETL pipelines, and data transformations with scheduled execution.

## When to Use

**Trigger when:**
- Keywords: schedule, automate, daily, hourly, ETL, pipeline, cron
- User wants to: run query daily, automate reports, incremental loads

**Chat commands:**
```bash
/bigquery/scheduled-queries create daily aggregation at 2am
/bigquery/scheduled-queries setup hourly event summary
/bigquery/scheduled-queries automate weekly report
```

## Requirements

<critical>
- BigQuery Data Transfer Service enabled
- Service account with bigquery.transfers.update permission
- Target dataset/table permissions
</critical>

---

## Basic Scheduled Query

### Using BigQuery Console

1. Write your query
2. Click "Schedule" button
3. Configure:
   - Name: `daily_user_stats`
   - Schedule: `every day 02:00`
   - Destination table: `dataset.daily_stats`
   - Write preference: `WRITE_TRUNCATE` or `WRITE_APPEND`

### Using bq CLI

```bash
bq mk \
  --transfer_config \
  --data_source=scheduled_query \
  --target_dataset=my_dataset \
  --display_name='Daily User Stats' \
  --schedule='every day 02:00' \
  --params='{
    "query":"SELECT DATE(timestamp) as date, COUNT(*) as events FROM `project.dataset.events` WHERE DATE(timestamp) = CURRENT_DATE() - 1 GROUP BY date",
    "destination_table_name_template":"daily_stats",
    "write_disposition":"WRITE_APPEND"
  }'
```

---

## Common Patterns

### Pattern 1: Daily Aggregation

```sql
-- Scheduled: every day 02:00 UTC
-- Destination: dataset.daily_summary
-- Write: WRITE_APPEND

SELECT
  CURRENT_DATE() - 1 as date,
  COUNT(DISTINCT user_id) as active_users,
  COUNT(*) as total_events,
  COUNTIF(event_name = 'purchase') as purchases,
  SUM(IF(event_name = 'purchase', 
    CAST(JSON_EXTRACT_SCALAR(properties, '$.amount') AS FLOAT64), 
    0)) as revenue
FROM `project.dataset.events`
WHERE DATE(timestamp) = CURRENT_DATE() - 1
GROUP BY date;
```

### Pattern 2: Incremental Load (Partition Overwrite)

```sql
-- Scheduled: every hour
-- Destination: dataset.hourly_stats$YYYYMMDDHH
-- Write: WRITE_TRUNCATE

DECLARE target_hour TIMESTAMP;
SET target_hour = TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), HOUR) - INTERVAL 1 HOUR;

SELECT
  user_id,
  COUNT(*) as events,
  MAX(timestamp) as last_event
FROM `project.dataset.events`
WHERE timestamp >= target_hour
  AND timestamp < target_hour + INTERVAL 1 HOUR
GROUP BY user_id;
```

### Pattern 3: Materialized View Refresh

```sql
-- Scheduled: every 30 minutes
-- Destination: dataset.recent_activity
-- Write: WRITE_TRUNCATE

SELECT
  user_id,
  COUNT(*) as recent_events,
  MAX(timestamp) as last_activity
FROM `project.dataset.events`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY user_id;
```

### Pattern 4: Multi-Tenant Daily Reports

```sql
-- Scheduled: every day 03:00
-- Destination: dataset.tenant_daily_stats
-- Write: WRITE_APPEND

SELECT
  tenant_id,
  CURRENT_DATE() - 1 as date,
  COUNT(DISTINCT user_id) as unique_users,
  COUNT(*) as events,
  COUNTIF(event_name = 'conversion') as conversions
FROM `project.dataset.events`
WHERE DATE(timestamp) = CURRENT_DATE() - 1
GROUP BY tenant_id, date;
```

---

## Advanced Patterns

### Pattern 5: Incremental Processing with Watermark

```sql
-- Track last processed timestamp
CREATE TABLE IF NOT EXISTS `dataset.watermark` (
  job_name STRING,
  last_processed TIMESTAMP
);

-- Scheduled query
DECLARE last_run TIMESTAMP;

-- Get last watermark
SET last_run = (
  SELECT last_processed 
  FROM `dataset.watermark` 
  WHERE job_name = 'event_processing'
);

-- Process new data
INSERT INTO `dataset.processed_events`
SELECT *
FROM `dataset.raw_events`
WHERE timestamp > COALESCE(last_run, TIMESTAMP('2024-01-01'))
  AND timestamp <= CURRENT_TIMESTAMP();

-- Update watermark
MERGE `dataset.watermark` T
USING (SELECT 'event_processing' as job_name, CURRENT_TIMESTAMP() as last_processed) S
ON T.job_name = S.job_name
WHEN MATCHED THEN UPDATE SET last_processed = S.last_processed
WHEN NOT MATCHED THEN INSERT (job_name, last_processed) VALUES (S.job_name, S.last_processed);
```

### Pattern 6: Conditional Execution

```sql
-- Only run if new data exists
DECLARE row_count INT64;

SET row_count = (
  SELECT COUNT(*)
  FROM `dataset.staging_table`
  WHERE DATE(created_at) = CURRENT_DATE()
);

IF row_count > 0 THEN
  -- Process data
  INSERT INTO `dataset.final_table`
  SELECT * FROM `dataset.staging_table`
  WHERE DATE(created_at) = CURRENT_DATE();
  
  -- Clean up staging
  DELETE FROM `dataset.staging_table`
  WHERE DATE(created_at) = CURRENT_DATE();
END IF;
```

---

## Error Handling

### Pattern: Email Notifications

```bash
# Configure email on failure
bq mk \
  --transfer_config \
  --notification_pubsub_topic=projects/PROJECT/topics/bq-errors \
  --schedule='every day 02:00' \
  ...
```

### Pattern: Retry Logic

```sql
-- Built-in retries (automatic)
-- BigQuery retries up to 3 times on transient errors

-- Manual validation
CREATE OR REPLACE TABLE `dataset.job_status` AS
SELECT
  CURRENT_TIMESTAMP() as run_time,
  (SELECT COUNT(*) FROM `dataset.daily_stats` 
   WHERE date = CURRENT_DATE() - 1) as rows_inserted,
  CASE 
    WHEN rows_inserted > 0 THEN 'SUCCESS'
    ELSE 'FAILED'
  END as status;
```

---

## Scheduling Options

### Cron-style Schedule

```bash
# Every day at 2am UTC
--schedule='every day 02:00'

# Every Monday at 9am
--schedule='every monday 09:00'

# Every 4 hours
--schedule='every 4 hours'

# Every 30 minutes
--schedule='every 30 minutes'

# First day of month
--schedule='1 of month 00:00'

# Complex: Every weekday at 8am and 6pm
--schedule='every weekday 08:00'
--schedule='every weekday 18:00'
```

### Using Scripting for Complex Schedules

```sql
-- Run different logic based on day of week
DECLARE day_of_week INT64;
SET day_of_week = EXTRACT(DAYOFWEEK FROM CURRENT_DATE());

IF day_of_week = 1 THEN  -- Sunday
  -- Weekly aggregation
  INSERT INTO `dataset.weekly_stats`
  SELECT ...;
ELSE
  -- Daily aggregation
  INSERT INTO `dataset.daily_stats`
  SELECT ...;
END IF;
```

---

## Monitoring Scheduled Queries

### Check Transfer Run History

```sql
SELECT
  run_time,
  state,
  error_status.message as error_message
FROM `region-us`.INFORMATION_SCHEMA.TRANSFER_RUN
WHERE transfer_config_id = 'your-config-id'
ORDER BY run_time DESC
LIMIT 10;
```

### Query Job History

```sql
SELECT
  job_id,
  creation_time,
  state,
  total_bytes_processed,
  error_result.message as error
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_type = 'QUERY'
  AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
  AND statement_type = 'INSERT'
ORDER BY creation_time DESC;
```

---

## Vietnamese Use Case: Daily Car Listings Report

```sql
-- Scheduled: every day 01:00 Vietnam time (18:00 UTC previous day)
-- Destination: dataset.daily_car_stats
-- Write: WRITE_APPEND

WITH daily_listings AS (
  SELECT
    DATE(created_at, 'Asia/Ho_Chi_Minh') as date,
    category,  -- 'ô tô', 'xe máy', etc.
    city,
    COUNT(*) as new_listings,
    AVG(price) as avg_price
  FROM `dataset.car_listings`
  WHERE DATE(created_at, 'Asia/Ho_Chi_Minh') = CURRENT_DATE('Asia/Ho_Chi_Minh') - 1
  GROUP BY date, category, city
),
daily_leads AS (
  SELECT
    DATE(timestamp, 'Asia/Ho_Chi_Minh') as date,
    COUNT(*) as total_leads,
    COUNTIF(event_name = 'phone_click') as phone_clicks,
    COUNTIF(event_name = 'form_submit') as form_submits
  FROM `dataset.events`
  WHERE DATE(timestamp, 'Asia/Ho_Chi_Minh') = CURRENT_DATE('Asia/Ho_Chi_Minh') - 1
  GROUP BY date
)
SELECT
  l.*,
  d.total_leads,
  d.phone_clicks,
  d.form_submits
FROM daily_listings l
LEFT JOIN daily_leads d USING (date);
```

---

## Integration with Cloud Composer (Advanced)

```python
# Airflow DAG for complex workflows
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'bigquery_etl',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2am daily
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    
    # Step 1: Load data
    load_task = BigQueryInsertJobOperator(
        task_id='load_events',
        configuration={
            'query': {
                'query': 'SELECT ... FROM ...',
                'destinationTable': {
                    'projectId': 'project',
                    'datasetId': 'dataset',
                    'tableId': 'events'
                },
                'writeDisposition': 'WRITE_APPEND'
            }
        }
    )
    
    # Step 2: Aggregate
    aggregate_task = BigQueryInsertJobOperator(
        task_id='aggregate_daily',
        configuration={...}
    )
    
    # Step 3: Export
    export_task = BigQueryInsertJobOperator(
        task_id='export_results',
        configuration={...}
    )
    
    load_task >> aggregate_task >> export_task
```

---

## Best Practices

1. **Use parameterized queries** for date ranges
2. **Always include date filter** to limit data scanned
3. **Write to partitioned tables** for efficient storage
4. **Monitor job failures** with alerting
5. **Test with dry run** before scheduling
6. **Use WRITE_APPEND** for incremental data
7. **Set table expiration** for temp tables

---

## Cost Optimization

```sql
-- Use clustering for frequently filtered columns
CREATE OR REPLACE TABLE `dataset.daily_stats`
PARTITION BY date
CLUSTER BY tenant_id, category
AS SELECT ...;

-- Scheduled query automatically benefits from clustering
SELECT *
FROM `dataset.daily_stats`
WHERE date = CURRENT_DATE() - 1
  AND tenant_id = 'abc123';  -- Cluster pruning applied
```

---

## Quick Reference

| Frequency | Schedule String | Use Case |
|-----------|----------------|----------|
| Every hour | `every hour` | Real-time dashboards |
| Every 4 hours | `every 4 hours` | Periodic updates |
| Daily 2am | `every day 02:00` | Daily ETL |
| Weekdays 9am | `every weekday 09:00` | Business reports |
| Weekly Mon 8am | `every monday 08:00` | Weekly summaries |
| Monthly 1st | `1 of month 00:00` | Monthly reports |

## Version

- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
