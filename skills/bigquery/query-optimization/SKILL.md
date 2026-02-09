# BigQuery Query Optimization

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/query-optimization`

## Purpose
Optimize BigQuery SQL queries for performance, cost efficiency, and prevent common pitfalls like data duplication, slow JOINs, and expensive aggregations.

## When to Use

**Trigger automatically when:**
- User mentions: slow, optimize, performance, duplicate rows, expensive
- Query execution time > 10 seconds
- Bytes processed > 1GB
- User asks to "check my query"
- Unexpected row counts after JOINs

**Chat commands:**
```bash
/bigquery/query-optimization check my query "SELECT * FROM..."
/bigquery/query-optimization why is this slow "WITH ..."
/bigquery/query-optimization prevent duplicates in JOIN
/bigquery/query-optimization reduce costs for daily analytics
```

## Requirements

<critical>
- BigQuery access configured
- Query history access (for INFORMATION_SCHEMA)
- Understanding of source table partitioning/clustering
</critical>

## Verification
```bash
# Ensure access to query stats
bq ls --project_id=your_project
bq show --format=prettyjson your_project:dataset.table
```

---

## Critical Rules

<critical>
1. ALWAYS use `view` to read this skill BEFORE writing BigQuery queries
2. ALWAYS check for DISTINCT operations - major performance killer
3. ALWAYS validate JOIN conditions to prevent row explosion
4. NEVER use SELECT * in production queries
5. ALWAYS filter on partitioned columns when available
</critical>

---

## Optimization Workflow

### Step 1: Analyze Current Query
```sql
-- Get query execution stats
SELECT
  job_id,
  user_email,
  total_bytes_processed / POW(10,9) as gb_processed,
  total_slot_ms / 1000 as slot_seconds,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_sec,
  SUBSTR(query, 1, 100) as query_preview
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
ORDER BY total_bytes_processed DESC
LIMIT 10;
```

### Step 2: Identify Performance Bottlenecks

**Common Issues:**
- ❌ Late filtering (WHERE after JOINs)
- ❌ Unnecessary DISTINCT
- ❌ Cross JOINs or missing JOIN conditions
- ❌ Multiple window functions over same partition
- ❌ Subqueries in SELECT clause
- ❌ Not using partitioned/clustered columns

### Step 3: Apply Optimization Patterns

---

## Optimization Patterns

### Pattern 1: Filter Early (Partition Pruning)

```sql
-- ❌ BAD: Filter after processing all data
SELECT *
FROM `project.dataset.events`
JOIN `project.dataset.users` USING (user_id)
WHERE DATE(timestamp) = '2024-01-01';

-- ✅ GOOD: Filter on partition before JOIN
WITH filtered_events AS (
  SELECT *
  FROM `project.dataset.events`
  WHERE DATE(timestamp) = '2024-01-01'  -- Partition filter first
)
SELECT *
FROM filtered_events
JOIN `project.dataset.users` USING (user_id);
```

**Impact:** Can reduce bytes processed by 90%+

**When to use:**
- Table is partitioned by date/timestamp
- Query only needs specific date range
- Filtering before JOINs

---

### Pattern 2: Avoid DISTINCT (Use QUALIFY)

```sql
-- ❌ BAD: DISTINCT causes full scan and deduplication overhead
SELECT DISTINCT
  user_id,
  FIRST_VALUE(event_name) OVER (PARTITION BY user_id ORDER BY timestamp DESC) as last_event
FROM events;

-- ✅ GOOD: Use QUALIFY for deduplication
SELECT
  user_id,
  event_name as last_event
FROM events
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) = 1;
```

**Impact:** 50-70% performance improvement on large datasets

**When to use:**
- Need to deduplicate rows
- Getting "latest" or "first" record per group
- Window functions already in query

---

### Pattern 3: JOIN Order & Conditions

```sql
-- ❌ BAD: Large table first, no early filtering
SELECT *
FROM large_events e
LEFT JOIN small_users u ON e.user_id = u.user_id;

-- ✅ GOOD: Small table first (if possible), pre-filtered
WITH active_users AS (
  SELECT user_id, email
  FROM small_users
  WHERE status = 'active'  -- Filter small table first
),
recent_events AS (
  SELECT *
  FROM large_events
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
)
SELECT *
FROM active_users u
LEFT JOIN recent_events e ON u.user_id = e.user_id;
```

**Key Check:** Use EXPLAIN to verify JOIN order

**When to use:**
- Joining multiple tables
- One table significantly smaller
- Can filter before joining

---

### Pattern 4: Prevent Row Explosion

```sql
-- ❌ BAD: Can cause row explosion if multiple matches
SELECT
  e.*,
  s.session_id
FROM events e
LEFT JOIN sessions s ON e.user_id = s.user_id;  -- One user can have many sessions!

-- ✅ GOOD: Ensure 1:1 relationship or aggregate
SELECT
  e.*,
  s.session_id
FROM events e
LEFT JOIN (
  SELECT user_id, session_id
  FROM sessions
  QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY session_start DESC) = 1
) s ON e.user_id = s.user_id;

-- OR use aggregation if you need all sessions
SELECT
  e.event_id,
  e.user_id,
  ARRAY_AGG(s.session_id) as session_ids
FROM events e
LEFT JOIN sessions s ON e.user_id = s.user_id
GROUP BY e.event_id, e.user_id;
```

**Verification:**
```sql
-- Check for duplication
WITH original AS (SELECT COUNT(*) as cnt FROM events),
     after_join AS (SELECT COUNT(*) as cnt FROM [your_query])
SELECT 
  o.cnt as original_rows,
  a.cnt as after_join_rows,
  a.cnt - o.cnt as row_explosion
FROM original o, after_join a;
```

**When to use:**
- JOINing on non-unique keys
- One-to-many relationships
- Unexpected row count increases

---

### Pattern 5: Aggregate Efficiently

```sql
-- ❌ BAD: Multiple scans of same data
SELECT
  (SELECT COUNT(*) FROM events WHERE event_name = 'purchase') as purchases,
  (SELECT COUNT(*) FROM events WHERE event_name = 'view') as views,
  (SELECT COUNT(*) FROM events WHERE event_name = 'click') as clicks;

-- ✅ GOOD: Single scan with conditional aggregation
SELECT
  COUNTIF(event_name = 'purchase') as purchases,
  COUNTIF(event_name = 'view') as views,
  COUNTIF(event_name = 'click') as clicks
FROM events;
```

**Impact:** Reduces scans from N to 1

**When to use:**
- Multiple aggregations on same table
- Conditional counts
- Different WHERE conditions for different metrics

---

### Pattern 6: Window Function Optimization

```sql
-- ❌ BAD: Multiple window functions with same partition
SELECT
  user_id,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as rn,
  FIRST_VALUE(event_name) OVER (PARTITION BY user_id ORDER BY timestamp) as first_event,
  LAST_VALUE(event_name) OVER (PARTITION BY user_id ORDER BY timestamp) as last_event
FROM events;

-- ✅ GOOD: Combine window functions with same partition
SELECT
  user_id,
  ROW_NUMBER() OVER w as rn,
  FIRST_VALUE(event_name) OVER w as first_event,
  LAST_VALUE(event_name) OVER w as last_event
FROM events
WINDOW w AS (PARTITION BY user_id ORDER BY timestamp);
```

**Impact:** Reduces computation overhead

**When to use:**
- Multiple window functions
- Same PARTITION BY and ORDER BY
- Complex analytics queries

---

### Pattern 7: Date/Time Handling

```sql
-- ❌ BAD: Function on partition column prevents pruning
SELECT *
FROM events
WHERE DATE(timestamp) = '2024-01-01';

-- ✅ GOOD: Range filter on partition column directly
SELECT *
FROM events
WHERE timestamp >= '2024-01-01 00:00:00'
  AND timestamp < '2024-01-02 00:00:00';
```

**Impact:** Enables partition pruning

**When to use:**
- Filtering on partitioned timestamp columns
- Date range queries
- Always for production queries

---

### Pattern 8: Multi-Tenant Optimization

```sql
-- Specific use case: multi-tenant analytics

-- ❌ BAD: Not using tenant_id early
SELECT
  e.user_id,
  COUNT(*) as event_count
FROM events e
WHERE e.event_name = 'purchase'
GROUP BY e.user_id;

-- ✅ GOOD: Filter by tenant_id first (if clustered)
WITH tenant_events AS (
  SELECT *
  FROM events
  WHERE tenant_id = 'tenant_123'  -- If clustered by tenant_id
    AND DATE(timestamp) = '2024-01-01'  -- Partition filter
)
SELECT
  user_id,
  COUNT(*) as event_count
FROM tenant_events
WHERE event_name = 'purchase'
GROUP BY user_id;
```

**When to use:**
- Multi-tenant applications
- Table clustered by tenant_id
- User-specific analytics

---

## Common Pitfalls & Solutions

### Pitfall 1: Accidental Cartesian Product
```sql
-- ❌ This can explode rows
SELECT *
FROM events e, sessions s  -- Missing WHERE/ON
WHERE e.event_name = 'click';

-- ✅ Always specify JOIN condition
SELECT *
FROM events e
INNER JOIN sessions s ON e.session_id = s.session_id
WHERE e.event_name = 'click';
```

### Pitfall 2: NULL Handling in JOINs
```sql
-- ❌ BAD: NULLs don't match in standard JOIN
SELECT *
FROM events e
LEFT JOIN users u ON e.user_id = u.user_id;  -- If user_id is NULL, no match

-- ✅ GOOD: Handle NULLs explicitly or filter
SELECT *
FROM events e
LEFT JOIN users u ON COALESCE(e.user_id, 'unknown') = COALESCE(u.user_id, 'unknown');

-- OR filter out NULLs early if they're invalid
SELECT *
FROM events e
LEFT JOIN users u ON e.user_id = u.user_id
WHERE e.user_id IS NOT NULL;
```

### Pitfall 3: ARRAY_AGG Without LIMIT
```sql
-- ❌ BAD: Can create massive arrays
SELECT
  user_id,
  ARRAY_AGG(event_name) as all_events
FROM events
GROUP BY user_id;

-- ✅ GOOD: Limit array size
SELECT
  user_id,
  ARRAY_AGG(event_name ORDER BY timestamp DESC LIMIT 100) as recent_events
FROM events
GROUP BY user_id;
```

### Pitfall 4: Inefficient Subqueries
```sql
-- ❌ BAD: Correlated subquery runs for each row
SELECT
  user_id,
  (SELECT COUNT(*) FROM events e WHERE e.user_id = u.user_id) as event_count
FROM users u;

-- ✅ GOOD: Use JOIN or window function
SELECT
  u.user_id,
  COUNT(e.event_id) as event_count
FROM users u
LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.user_id;
```

---

## Performance Verification Checklist

After optimization, verify:

```sql
-- 1. Check bytes processed (should be significantly lower)
-- Run in BigQuery Console - see "Bytes processed" estimate

-- 2. Use EXPLAIN to check execution plan
-- In BigQuery Console, click "Execution details" after running

-- 3. Compare slot usage
SELECT
  job_id,
  total_slot_ms / 1000 as slot_seconds,
  total_bytes_processed / POW(10, 9) as gb_processed
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE query LIKE '%your_table%'
  AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY creation_time DESC
LIMIT 5;
```

**Target Metrics:**
- ✅ Bytes processed reduced by 50%+ for filtered queries
- ✅ Execution time < 10 seconds for < 10GB scans
- ✅ No unexpected row count increases
- ✅ Slot time proportional to data size

---

## Vietnamese Market Specific Notes

```sql
-- Handle Vietnamese characters in search
SELECT *
FROM products
WHERE LOWER(name) LIKE '%ô tô%'  -- Works with Vietnamese
  OR LOWER(name) LIKE '%xe hơi%';

-- Timezone handling for Vietnam
SELECT
  DATETIME(timestamp, 'Asia/Ho_Chi_Minh') as vietnam_time,
  event_name
FROM events
WHERE timestamp >= TIMESTAMP('2024-01-01 00:00:00', 'Asia/Ho_Chi_Minh');
```

---

## Cost Optimization Tips

```sql
-- 1. Use table sampling for development
SELECT *
FROM events TABLESAMPLE SYSTEM (1 PERCENT)  -- Only scan 1%
WHERE DATE(timestamp) = '2024-01-01';

-- 2. Materialized views for repeated queries
CREATE MATERIALIZED VIEW daily_stats AS
SELECT
  DATE(timestamp) as date,
  user_id,
  COUNT(*) as event_count
FROM events
GROUP BY 1, 2;

-- Then query the MV instead of raw table
SELECT * FROM daily_stats WHERE date = '2024-01-01';

-- 3. Clustering for frequently filtered columns
-- (Run once as DDL)
CREATE OR REPLACE TABLE events_clustered
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, event_name
AS SELECT * FROM events;
```

---

## Debugging Slow Queries

```sql
-- Find slow queries in your project
SELECT
  job_id,
  user_email,
  ROUND(total_slot_ms / 1000, 2) as slot_seconds,
  ROUND(total_bytes_processed / POW(10, 9), 2) as gb_processed,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_seconds,
  SUBSTR(query, 1, 100) as query_preview
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
  AND total_slot_ms > 60000  -- More than 60 slot-seconds
ORDER BY total_slot_ms DESC
LIMIT 20;
```

---

## Testing Strategy

```python
# Use this pattern in Claude Code
def test_query_optimization(original_query, optimized_query):
    """
    Compare two queries for performance
    """
    from google.cloud import bigquery
    
    client = bigquery.Client()
    
    # Dry run to get bytes processed
    original_job = client.query(original_query, 
                                job_config=bigquery.QueryJobConfig(dry_run=True))
    optimized_job = client.query(optimized_query,
                                 job_config=bigquery.QueryJobConfig(dry_run=True))
    
    print(f"Original: {original_job.total_bytes_processed:,} bytes")
    print(f"Optimized: {optimized_job.total_bytes_processed:,} bytes")
    reduction = (1 - optimized_job.total_bytes_processed/original_job.total_bytes_processed)*100
    print(f"Reduction: {reduction:.1f}%")
    
    return reduction > 30  # Success if >30% reduction
```

---

## Quick Reference Card

| Issue | Solution | Pattern |
|-------|----------|---------|
| Slow query | Filter on partition column first | WHERE DATE(ts) = ... |
| Duplicates | Use QUALIFY + ROW_NUMBER | QUALIFY ROW_NUMBER() OVER (...) = 1 |
| Row explosion | Verify JOIN cardinality | Check COUNT before/after |
| Expensive DISTINCT | Use window functions | QUALIFY instead of DISTINCT |
| Multiple scans | Conditional aggregation | COUNTIF instead of subqueries |
| Cartesian product | Always use explicit JOINs | INNER/LEFT JOIN ON ... |
| NULL issues | Handle explicitly | COALESCE or WHERE IS NOT NULL |

---

## Integration with Other Skills

**Next steps after optimization:**
- Use `/bigquery/cost-monitoring` to verify cost savings
- Use `/bigquery/scheduled-queries` to automate if recurring
- Use `/bigquery/schema-design` if table structure needs improvement
- Use `/bigquery/troubleshooting` if errors persist

---

## Version & Changelog

- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
- **Tested on:** BigQuery Standard SQL

### Changelog
- 2024-02-09: Initial version with 8 core patterns
