# BigQuery Schema Design

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/schema-design`

## Purpose
Design optimal table schemas with partitioning, clustering, and data types for performance and cost efficiency.

## When to Use

**Trigger when:**
- Keywords: CREATE TABLE, partition, cluster, schema, design, structure
- User asks: "how to structure table", "setup partitioning", "optimize storage"

**Chat commands:**
```bash
/bigquery/schema-design create events table with partitioning
/bigquery/schema-design add clustering to existing table
/bigquery/schema-design design schema for time-series data
```

## Requirements

<critical>
- Dataset created
- Understanding of query patterns
- Knowledge of data access patterns
</critical>

---

## Partitioning Strategies

### 1. Date/Timestamp Partitioning (Most Common)

```sql
-- Daily partitions (recommended for event data)
CREATE OR REPLACE TABLE `dataset.events`
PARTITION BY DATE(timestamp)
OPTIONS (
  partition_expiration_days = 365,  -- Auto-delete after 1 year
  require_partition_filter = TRUE   -- Force users to filter by date
) AS
SELECT
  timestamp,
  user_id,
  event_name,
  properties
FROM `dataset.raw_events`;
```

**When to use:**
- Event/log data
- Time-series data
- Data queried by date ranges

### 2. Integer Range Partitioning

```sql
-- Partition by user ID ranges
CREATE OR REPLACE TABLE `dataset.users`
PARTITION BY RANGE_BUCKET(user_id, GENERATE_ARRAY(0, 1000000, 10000))
AS
SELECT * FROM `dataset.raw_users`;
```

**When to use:**
- Queries filter by numeric ranges
- Data evenly distributed across ranges

### 3. Ingestion Time Partitioning

```sql
CREATE OR REPLACE TABLE `dataset.events`
PARTITION BY _PARTITIONTIME
AS SELECT * FROM `dataset.raw_events`;
```

---

## Clustering

### Single Column Clustering

```sql
CREATE OR REPLACE TABLE `dataset.events`
PARTITION BY DATE(timestamp)
CLUSTER BY user_id
AS SELECT * FROM `dataset.raw_events`;
```

### Multi-Column Clustering (Order Matters!)

```sql
-- Cluster order: most filtered columns first
CREATE OR REPLACE TABLE `dataset.events`
PARTITION BY DATE(timestamp)
CLUSTER BY tenant_id, user_id, event_name  -- Order by selectivity
AS SELECT * FROM `dataset.raw_events`;
```

**Clustering Rules:**
- Max 4 clustering columns
- Order by most selective first
- Use for high-cardinality columns
- Best for columns in WHERE/GROUP BY

---

## Data Types Best Practices

### Choose Optimal Types

```sql
CREATE OR REPLACE TABLE `dataset.optimized` AS
SELECT
  -- Use STRING for IDs (not INT64)
  CAST(user_id AS STRING) as user_id,
  
  -- Use TIMESTAMP for datetime
  TIMESTAMP(created_at) as created_at,
  
  -- Use NUMERIC for currency (precise decimal)
  CAST(price AS NUMERIC) as price,
  
  -- Use BOOL instead of INT64
  CAST(is_active AS BOOL) as is_active,
  
  -- Use ARRAY for repeating fields
  ARRAY_AGG(tag) as tags,
  
  -- Use JSON for semi-structured data
  TO_JSON_STRING(metadata) as metadata
FROM `dataset.raw_data`;
```

**Type Recommendations:**
- **IDs:** STRING (avoid INT64 for UUIDs)
- **Timestamps:** TIMESTAMP (not STRING)
- **Money:** NUMERIC (exact decimal)
- **True/False:** BOOL (not INT64)
- **Lists:** ARRAY (not delimited strings)
- **Flexible:** JSON

---

## Nested and Repeated Fields

### STRUCT (Nested)

```sql
CREATE OR REPLACE TABLE `dataset.orders` AS
SELECT
  order_id,
  STRUCT(
    customer_name,
    customer_email,
    customer_phone
  ) as customer,
  STRUCT(
    street,
    city,
    country
  ) as shipping_address
FROM `dataset.raw_orders`;

-- Query nested fields
SELECT
  order_id,
  customer.name,
  shipping_address.city
FROM `dataset.orders`;
```

### ARRAY (Repeated)

```sql
CREATE OR REPLACE TABLE `dataset.users_with_events` AS
SELECT
  user_id,
  ARRAY_AGG(STRUCT(
    event_name,
    timestamp,
    properties
  ) ORDER BY timestamp DESC LIMIT 100) as recent_events
FROM `dataset.events`
GROUP BY user_id;

-- Query arrays
SELECT
  user_id,
  event.event_name,
  event.timestamp
FROM `dataset.users_with_events`,
UNNEST(recent_events) as event
WHERE event.event_name = 'purchase';
```

---

## Schema Evolution

### Add Column

```sql
-- Add nullable column (no rewrite needed)
ALTER TABLE `dataset.events`
ADD COLUMN new_field STRING;

-- Add required column (requires default)
ALTER TABLE `dataset.events`
ADD COLUMN new_required STRING NOT NULL DEFAULT 'default_value';
```

### Modify Column Type

```sql
-- Cannot change type directly
-- Must create new table
CREATE OR REPLACE TABLE `dataset.events_v2` AS
SELECT
  *,
  CAST(string_column AS INT64) as string_column_int
FROM `dataset.events`;
```

---

## Table Design Patterns

### Pattern 1: Event Store (Append-Only)

```sql
CREATE OR REPLACE TABLE `dataset.events`
PARTITION BY DATE(timestamp)
CLUSTER BY tenant_id, user_id
OPTIONS (
  partition_expiration_days = 730  -- 2 years
)
AS SELECT
  timestamp,
  tenant_id,
  user_id,
  event_name,
  TO_JSON_STRING(properties) as properties
FROM `dataset.raw_events`;
```

### Pattern 2: Slowly Changing Dimension (SCD Type 2)

```sql
CREATE OR REPLACE TABLE `dataset.users_history` AS
SELECT
  user_id,
  name,
  email,
  valid_from,
  LEAD(valid_from, 1, TIMESTAMP('9999-12-31')) OVER (
    PARTITION BY user_id ORDER BY valid_from
  ) as valid_to,
  is_current
FROM `dataset.user_changes`;
```

### Pattern 3: Aggregation Table

```sql
-- Pre-aggregated for fast queries
CREATE OR REPLACE TABLE `dataset.daily_stats`
PARTITION BY date
CLUSTER BY tenant_id
AS SELECT
  DATE(timestamp) as date,
  tenant_id,
  COUNT(DISTINCT user_id) as unique_users,
  COUNT(*) as total_events
FROM `dataset.events`
GROUP BY date, tenant_id;
```

---

## Vietnamese Automotive Schema Example

```sql
-- Car listings table
CREATE OR REPLACE TABLE `dataset.car_listings`
PARTITION BY DATE(created_at)
CLUSTER BY dealership_id, category, city
OPTIONS (
  description = 'Danh sách ô tô và xe máy tại Việt Nam',
  partition_expiration_days = 365
) AS
SELECT
  listing_id,
  dealership_id,
  
  -- Category: 'ô tô', 'xe máy', 'xe tải'
  category,
  
  -- Location (Vietnam cities)
  city,  -- 'Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng'
  district,
  
  -- Car details
  STRUCT(
    make,      -- Toyota, Honda, Mazda
    model,     -- Vios, City, CX-5
    year,
    price,
    mileage_km,
    fuel_type, -- 'xăng', 'dầu', 'hybrid', 'điện'
    transmission  -- 'số sàn', 'số tự động'
  ) as vehicle_info,
  
  -- Contact
  STRUCT(
    dealer_name,
    phone,
    email
  ) as contact,
  
  -- Timestamps
  created_at,
  updated_at
  
FROM `dataset.raw_listings`;
```

---

## Performance Optimization

### Denormalization

```sql
-- Join frequently accessed data
CREATE OR REPLACE TABLE `dataset.events_denormalized`
PARTITION BY DATE(timestamp)
CLUSTER BY tenant_id
AS
SELECT
  e.*,
  u.email,
  u.city,
  u.registration_date
FROM `dataset.events` e
LEFT JOIN `dataset.users` u USING (user_id);
```

### Table Expiration

```sql
ALTER TABLE `dataset.temp_table`
SET OPTIONS (
  expiration_timestamp = TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
);
```

---

## Quick Reference

| Pattern | Partition By | Cluster By | Use Case |
|---------|--------------|------------|----------|
| Events | DATE(timestamp) | tenant_id, user_id | Event tracking |
| Users | - | user_id | User lookup |
| Transactions | DATE(created_at) | merchant_id, amount | Financial data |
| Logs | _PARTITIONTIME | severity, service | System logs |
| Analytics | DATE | category, region | Aggregated data |

## Version
- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
