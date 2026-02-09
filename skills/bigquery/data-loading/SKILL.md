# BigQuery Data Loading & Export

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/data-loading`

## Purpose
Efficiently import data from various sources (GCS, local files, streaming) and export BigQuery results.

## When to Use

**Trigger automatically when:**
- Keywords: load, import, export, CSV, JSON, Parquet, streaming
- User uploads file and mentions BigQuery
- User asks to "save query results"

**Chat commands:**
```bash
/bigquery/data-loading import CSV from gs://bucket/data.csv
/bigquery/data-loading load this file into table events
/bigquery/data-loading export query results to GCS
/bigquery/data-loading setup streaming for real-time data
```

## Requirements

<critical>
- BigQuery access
- Cloud Storage bucket (for GCS loads)
- Appropriate IAM roles:
  - bigquery.tables.create
  - bigquery.tables.updateData
  - storage.objects.get (for GCS)
</critical>

## Verification
```bash
# Check GCS access
gsutil ls gs://your-bucket/

# Check BigQuery permissions
bq show your_project:dataset
```

---

## Loading Patterns

### Pattern 1: Load CSV from GCS

```bash
# Using bq CLI
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --autodetect \
  dataset.table_name \
  gs://bucket/data.csv
```

```python
# Using Python client
from google.cloud import bigquery

client = bigquery.Client()

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    write_disposition='WRITE_TRUNCATE'  # or WRITE_APPEND
)

uri = "gs://bucket/data.csv"
table_id = "project.dataset.table"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)

load_job.result()  # Wait for completion
print(f"Loaded {load_job.output_rows} rows")
```

**Best Practices:**
- Use `--autodetect` for schema inference (development only)
- Specify explicit schema for production
- Use `WRITE_APPEND` for incremental loads
- Partition target table by date if loading daily

---

### Pattern 2: Load JSON (Newline-Delimited)

```python
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=True,
)

uri = "gs://bucket/events.json"
load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
load_job.result()
```

**JSON Format Required:**
```json
{"user_id": "123", "event": "click", "timestamp": "2024-02-09T10:00:00Z"}
{"user_id": "456", "event": "view", "timestamp": "2024-02-09T10:01:00Z"}
```

**NOT standard JSON array:**
```json
// ❌ This won't work
[
  {"user_id": "123", ...},
  {"user_id": "456", ...}
]
```

---

### Pattern 3: Load Parquet (Recommended for Large Data)

```python
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition='WRITE_TRUNCATE'
)

uri = "gs://bucket/data.parquet"
load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
load_job.result()
```

**Advantages:**
- Compressed (smaller than CSV)
- Schema included (no need for autodetect)
- Faster load times (5-10x vs CSV)
- Columnar format = better query performance

---

### Pattern 4: Streaming Inserts (Real-Time)

```python
# For real-time data (e.g., website events)
rows_to_insert = [
    {"user_id": "123", "event": "purchase", "timestamp": "2024-02-09T10:00:00"},
    {"user_id": "456", "event": "view", "timestamp": "2024-02-09T10:01:00"},
]

errors = client.insert_rows_json(table_id, rows_to_insert)

if errors:
    print(f"Errors: {errors}")
else:
    print("Rows inserted successfully")
```

**Important:**
- Streaming has cost: $0.01 per 200MB
- Use only for real-time requirements
- For batch: use load jobs instead
- Has ~90 second buffer before data is queryable
- Max 10,000 rows per request

---

### Pattern 5: Load from Local File

```python
# Upload local CSV to BigQuery
with open("local_data.csv", "rb") as source_file:
    job = client.load_table_from_file(
        source_file,
        table_id,
        job_config=job_config
    )

job.result()
print(f"Loaded {job.output_rows} rows")
```

**Use cases:**
- Small files (<100MB)
- One-time imports
- Development/testing

**For large files:** Upload to GCS first, then load

---

### Pattern 6: Federated Query (External Data)

```sql
-- Query CSV directly from GCS without loading
CREATE EXTERNAL TABLE dataset.external_table
OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket/*.csv'],
  skip_leading_rows = 1
);

-- Now query it
SELECT * FROM dataset.external_table
WHERE date = '2024-02-09';
```

**Use cases:**
- One-time analysis
- Data changes frequently
- Don't want to pay storage costs

**Limitations:**
- Slower than native tables
- No clustering/partitioning
- Limited query optimization
- Cannot use DML (UPDATE/DELETE)

---

## Export Patterns

### Export 1: Query Results to GCS

```bash
# Export to CSV
bq extract \
  --destination_format=CSV \
  --compression=GZIP \
  dataset.table \
  gs://bucket/export-*.csv
```

```python
# Python client
destination_uri = "gs://bucket/export-*.csv"
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table(table_id)

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    location="US",
)
extract_job.result()
print("Export completed")
```

**Format options:**
- CSV (human-readable)
- JSON (structured)
- Avro (compressed, with schema)
- Parquet (best for re-import)

---

### Export 2: Large Results (Sharded)

```bash
# For > 1GB results, use wildcards for automatic sharding
bq extract \
  --destination_format=CSV \
  dataset.large_table \
  gs://bucket/shard-*.csv

# Creates: shard-000000000000.csv, shard-000000000001.csv, ...
```

**BigQuery automatically shards files > 1GB**

---

### Export 3: Export Query Results Directly

```python
# Export query result without creating intermediate table
query = """
SELECT 
  user_id,
  COUNT(*) as event_count
FROM events
WHERE DATE(timestamp) = CURRENT_DATE() - 1
GROUP BY user_id
"""

# Configure export
job_config = bigquery.QueryJobConfig(
    destination="project.dataset.temp_export"
)

# Run query
query_job = client.query(query, job_config=job_config)
query_job.result()

# Export the result table
destination_uri = "gs://bucket/export.csv"
extract_job = client.extract_table(
    "project.dataset.temp_export",
    destination_uri
)
extract_job.result()

# Clean up temp table
client.delete_table("project.dataset.temp_export")
```

---

## Schema Management

### Explicit Schema (Production Recommended)

```python
from google.cloud import bigquery

schema = [
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("event_name", "STRING"),
    bigquery.SchemaField("properties", "JSON"),
    bigquery.SchemaField("metadata", "RECORD", fields=[
        bigquery.SchemaField("source", "STRING"),
        bigquery.SchemaField("version", "INTEGER")
    ])
]

job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition='WRITE_APPEND'
)
```

### Schema Auto-Detection (Development Only)

```python
job_config = bigquery.LoadJobConfig(
    autodetect=True,
    write_disposition='WRITE_TRUNCATE'
)
```

**Warning:** Auto-detect can infer wrong types
- ZIP codes as INTEGER (should be STRING)
- Phone numbers as INTEGER
- Dates as STRING

---

## Incremental Loading Strategy

### Pattern: Daily Incremental Loads

```python
from datetime import datetime, timedelta

# Get yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Load with partition decorator
partition_date = yesterday.replace('-', '')  # Format: 20240209
table_id = f"project.dataset.events${partition_date}"

# Load data for yesterday only
uri = f"gs://bucket/data-{yesterday}.csv"
load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
load_job.result()

print(f"Loaded data for partition {yesterday}")
```

### Pattern: Merge/Upsert Strategy

```sql
-- Use MERGE for deduplication and updates
MERGE dataset.target T
USING dataset.staging S
ON T.user_id = S.user_id AND T.date = S.date
WHEN MATCHED THEN
  UPDATE SET 
    event_count = S.event_count,
    last_updated = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (user_id, date, event_count, last_updated)
  VALUES (S.user_id, S.date, S.event_count, CURRENT_TIMESTAMP());
```

---

## Error Handling

```python
try:
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # Wait and check for errors
    
    print(f"✅ Loaded {load_job.output_rows} rows")
    
except Exception as e:
    print(f"❌ Load failed: {e}")
    
    # Check detailed errors
    if hasattr(load_job, 'errors') and load_job.errors:
        for error in load_job.errors:
            print(f"Error: {error.get('message')}")
            print(f"Location: {error.get('location')}")
            print(f"Reason: {error.get('reason')}")
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| Schema mismatch | Column types don't match | Use explicit schema |
| Permission denied | Missing IAM roles | Add bigquery.tables.updateData |
| File not found | Wrong GCS path | Check URI with `gsutil ls` |
| Invalid format | Malformed CSV/JSON | Validate file format |
| Quota exceeded | Too many concurrent loads | Wait or request quota increase |

---

## Performance Tips

### Optimize Load Speed

```python
# 1. Use Parquet instead of CSV (5-10x faster)
source_format=bigquery.SourceFormat.PARQUET

# 2. Load multiple files in parallel
uris = [
    "gs://bucket/file1.csv",
    "gs://bucket/file2.csv",
    "gs://bucket/file3.csv"
]
load_job = client.load_table_from_uri(uris, table_id, job_config=job_config)

# 3. Use compression
job_config.compression = 'GZIP'

# 4. Allow some bad records (for dirty data)
job_config.max_bad_records = 100

# 5. Batch loads vs streaming
# Batch: Free, use for scheduled ETL
# Streaming: $0.01/200MB, use only for real-time
```

### Cost Optimization

**Costs:**
- **Batch loads:** FREE (only pay for storage)
- **Streaming:** $0.01 per 200MB
- **Export:** $0.011 per GB (to GCS)
- **Storage:** $0.02/GB/month (active), $0.01/GB/month (long-term)

**Recommendations:**
- Use batch loads whenever possible
- Compress files before loading
- Use Parquet for large datasets
- Partition tables for faster queries

---

## Vietnamese Data Handling

```python
# Ensure UTF-8 encoding for Vietnamese characters
job_config.encoding = 'UTF-8'

# Example CSV with Vietnamese
# user_id,name,location,product
# 1,Nguyễn Văn A,Hồ Chí Minh,Xe ô tô Toyota
# 2,Trần Thị B,Hà Nội,Xe máy Honda
```

**Test Vietnamese characters:**
```python
# After loading
query = """
SELECT name, location
FROM dataset.table
WHERE location LIKE '%Hồ Chí Minh%'
"""
results = client.query(query).result()
for row in results:
    print(f"{row.name} - {row.location}")
```

---

## Integration Examples

### Next.js API Route (Load Data)

```javascript
// pages/api/upload-data.js
import { BigQuery } from '@google-cloud/bigquery';
import { Storage } from '@google-cloud/storage';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const bigquery = new BigQuery();
  const storage = new Storage();
  
  try {
    // 1. Upload file to GCS
    const bucket = storage.bucket('my-bucket');
    const fileName = `uploads/${Date.now()}.csv`;
    const file = bucket.file(fileName);
    
    await file.save(req.body);
    
    // 2. Load to BigQuery
    const [job] = await bigquery
      .dataset('my_dataset')
      .table('events')
      .load(file, {
        sourceFormat: 'CSV',
        skipLeadingRows: 1,
        autodetect: true
      });
    
    // 3. Wait for completion
    const [metadata] = await job.getMetadata();
    
    res.json({ 
      success: true, 
      rowsLoaded: metadata.statistics.load.outputRows 
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

---

## Integration with Other Skills

**Workflow:**
1. Load data → `/bigquery/data-loading`
2. Design schema → `/bigquery/schema-design`
3. Optimize queries → `/bigquery/query-optimization`
4. Schedule incremental loads → `/bigquery/scheduled-queries`
5. Monitor costs → `/bigquery/cost-monitoring`

---

## Quick Reference

| Task | Format | Command |
|------|--------|---------|
| Load CSV | CSV | `bq load --source_format=CSV` |
| Real-time | Streaming | `client.insert_rows_json()` |
| One-time query | Federated | `CREATE EXTERNAL TABLE` |
| Export results | Parquet | `bq extract --destination_format=PARQUET` |
| Daily batch | Parquet | Cloud Scheduler + load job |
| Large files | Parquet/Avro | Load from GCS |

## Version

- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
