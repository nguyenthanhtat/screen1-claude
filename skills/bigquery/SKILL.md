# BigQuery Skill Suite

## Purpose
Comprehensive BigQuery skills covering optimization, data management, ML, security, and automation for production workloads.

## Version
- **Version:** 2.0.0
- **Last Updated:** 2024-02-09
- **BigQuery API:** v2
- **Compatibility:** Standard SQL only

## How to Use This Skill

### Direct Sub-Skill Access
Use skill paths to access specific functionality:
- `/bigquery/query-optimization` - Optimize slow queries, prevent duplication
- `/bigquery/data-loading` - Import/export data from various sources
- `/bigquery/bqml` - Machine learning model creation and prediction
- `/bigquery/scheduled-queries` - Automate ETL pipelines
- `/bigquery/cost-monitoring` - Track spending and optimize costs
- `/bigquery/security` - Setup RLS, IAM, column-level security
- `/bigquery/schema-design` - Design tables with partitioning/clustering
- `/bigquery/troubleshooting` - Debug errors and performance issues

### Chat Command Examples
```bash
# Query optimization
/bigquery/query-optimization check my query "SELECT * FROM events..."

# Data loading
/bigquery/data-loading import CSV from GCS bucket gs://my-bucket/data.csv

# Cost analysis
/bigquery/cost-monitoring show me expensive queries from last week

# Create ML model
/bigquery/bqml create prediction model for user churn

# Schedule ETL
/bigquery/scheduled-queries setup daily aggregation at 2am
```

## Auto-Routing (Claude Decides)

If you just use `/bigquery`, Claude will analyze your request and automatically route to the appropriate sub-skill.

**Examples:**
- "My query is slow" → routes to `/query-optimization`
- "Load this CSV" → routes to `/data-loading`
- "Predict customer value" → routes to `/bqml`
- "Setup daily reports" → routes to `/scheduled-queries`

## Decision Tree

```
User Request Analysis:
│
├─ Keywords: slow, optimize, duplicate, JOIN, performance
│  → /query-optimization
│
├─ Keywords: load, import, export, CSV, Parquet, streaming
│  → /data-loading
│
├─ Keywords: predict, model, ML, forecast, classification
│  → /bqml
│
├─ Keywords: schedule, automate, daily, ETL, pipeline
│  → /scheduled-queries
│
├─ Keywords: cost, expensive, budget, billing, slots
│  → /cost-monitoring
│
├─ Keywords: access, permission, RLS, security, IAM
│  → /security
│
├─ Keywords: CREATE TABLE, partition, cluster, schema, design
│  → /schema-design
│
└─ Keywords: error, debug, fail, troubleshoot, fix
   → /troubleshooting
```

## Requirements (Global)

<critical>
All sub-skills require:
- BigQuery API enabled in GCP project
- Service account with appropriate permissions
- `bq` CLI installed OR Python/Node.js client library
</critical>

### Quick Setup Verification
```bash
# Check access
bq ls --project_id=your_project

# Check permissions
gcloud projects get-iam-policy your_project \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:your-sa@project.iam.gserviceaccount.com"
```

## Sub-Skills Overview

### 1. Query Optimization
**Focus:** Performance tuning, cost reduction
**Common tasks:**
- Optimize slow queries (>10s execution)
- Prevent JOIN row explosion
- Eliminate DISTINCT overhead
- Reduce bytes processed

**Key metrics:** Execution time, bytes processed, slot usage

---

### 2. Data Loading
**Focus:** Import/export data efficiently
**Common tasks:**
- Load CSV/JSON/Parquet from GCS
- Streaming inserts for real-time data
- Federated queries (external sources)
- Export results to GCS

**Supported formats:** CSV, JSON, Avro, Parquet, ORC

---

### 3. BigQuery ML (BQML)
**Focus:** Machine learning without leaving SQL
**Common tasks:**
- Classification models (churn prediction)
- Regression (price forecasting)
- Clustering (customer segmentation)
- Time series forecasting
- Recommendations

**Model types:** Linear, Logistic, DNN, XGBoost, ARIMA

---

### 4. Scheduled Queries
**Focus:** Automation and orchestration
**Common tasks:**
- Daily/hourly aggregations
- Incremental data processing
- Error handling and retries
- Notification setup (email, Slack)

**Patterns:** Full refresh, incremental, CDC

---

### 5. Cost Monitoring
**Focus:** Budget control and attribution
**Common tasks:**
- Track spending by project/user
- Identify expensive queries
- Setup budget alerts
- Optimize reservation usage

**Tools:** INFORMATION_SCHEMA, Cloud Monitoring, Looker Studio

---

### 6. Security & Governance
**Focus:** Access control and compliance
**Common tasks:**
- Row-level security (RLS) for multi-tenant
- Column-level security (data masking)
- IAM role assignment
- Audit logging

**Use cases:** Multi-tenant isolation, GDPR compliance

---

### 7. Schema Design
**Focus:** Optimal table structure
**Common tasks:**
- Choose partitioning strategy (date, range, integer)
- Setup clustering for frequently filtered columns
- Denormalization vs normalization
- Nested/repeated fields design

**Best practices:** Partition pruning, clustering order

---

### 8. Troubleshooting
**Focus:** Debug and resolve issues
**Common tasks:**
- Decode error messages
- Fix permission errors
- Resolve quota exceeded
- Debug UDF failures

**Common errors:** 400 (syntax), 403 (permission), 500 (internal)

---

## Workflow Integration

### For Vietnamese Automotive Analytics

```bash
# Step 1: Design schema
/bigquery/schema-design create events table for car listings with partitioning

# Step 2: Load data
/bigquery/data-loading import Vietnamese car data from CSV

# Step 3: Optimize queries
/bigquery/query-optimization optimize daily lead analytics query

# Step 4: Setup automation
/bigquery/scheduled-queries schedule daily aggregation for car views

# Step 5: Monitor costs
/bigquery/cost-monitoring track query costs by tenant_id

# Step 6: Predict leads
/bigquery/bqml create lead conversion prediction model
```

### For Next.js Integration

```javascript
// Example: Use with API routes
// pages/api/analytics.js

import { BigQuery } from '@google-cloud/bigquery';

export default async function handler(req, res) {
  // Use /bigquery/query-optimization patterns here
  const query = `
    WITH tenant_data AS (
      SELECT * FROM events
      WHERE tenant_id = @tenantId
        AND DATE(timestamp) >= CURRENT_DATE() - 7
    )
    SELECT 
      event_name,
      COUNT(*) as count
    FROM tenant_data
    GROUP BY event_name
  `;
  
  const bigquery = new BigQuery();
  const [rows] = await bigquery.query({
    query,
    params: { tenantId: req.query.tenant }
  });
  
  res.json(rows);
}
```

## Quick Reference

| Task | Sub-Skill | Command Example |
|------|-----------|-----------------|
| Slow query | query-optimization | `/bigquery/query-optimization check query "SELECT..."` |
| Import CSV | data-loading | `/bigquery/data-loading load gs://bucket/file.csv` |
| Daily ETL | scheduled-queries | `/bigquery/scheduled-queries setup at 2am UTC` |
| Churn model | bqml | `/bigquery/bqml predict churn from users table` |
| High costs | cost-monitoring | `/bigquery/cost-monitoring analyze last month` |
| Multi-tenant | security | `/bigquery/security setup RLS by tenant_id` |
| New table | schema-design | `/bigquery/schema-design partition by date cluster by user_id` |
| Error | troubleshooting | `/bigquery/troubleshooting fix error "Resources exceeded"` |

## Installation

Copy this entire folder to your Claude skills directory:

```bash
# Option 1: User skills (recommended)
cp -r bigquery-skills /mnt/skills/user/bigquery

# Option 2: Local project
cp -r bigquery-skills ./claude-skills/bigquery
```

Then configure in your `.claude` file:
```yaml
skills:
  - /mnt/skills/user/bigquery
```

## Related Documentation

- Official: https://cloud.google.com/bigquery/docs
- Best practices: https://cloud.google.com/bigquery/docs/best-practices
- Pricing: https://cloud.google.com/bigquery/pricing
- API Reference: https://cloud.google.com/bigquery/docs/reference/rest

## Changelog

### 2.0.0 (2024-02-09)
- Initial modular skill suite
- 8 sub-skills covering all major BigQuery features
- Vietnamese market support
- Next.js integration examples

## Support

For issues or suggestions:
1. Use `/bigquery/troubleshooting` for technical problems
2. Update skill files based on production learnings
3. Add new patterns to relevant sub-skills

## License

Free to use and modify for personal/commercial projects.
