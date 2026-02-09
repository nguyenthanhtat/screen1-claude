# BigQuery Skill Suite

Complete set of BigQuery skills for Claude Code and Claude AI.

## 📦 What's Included

### Main Router Skill
- **SKILL.md** - Main entry point that routes to sub-skills

### 8 Sub-Skills

1. **query-optimization/** - Optimize slow queries, prevent duplicates, reduce costs
2. **data-loading/** - Import/export data (CSV, JSON, Parquet, streaming)
3. **bqml/** - Machine learning with BigQuery ML
4. **scheduled-queries/** - Automate ETL pipelines and recurring queries
5. **cost-monitoring/** - Track spending, find expensive queries
6. **security/** - Row-level security, IAM, audit logging
7. **schema-design/** - Design tables with partitioning and clustering
8. **troubleshooting/** - Debug errors and performance issues

## 🚀 Installation

### Option 1: Claude User Skills (Recommended)

```bash
# Copy to user skills directory
cp -r bigquery-skills /mnt/skills/user/bigquery
```

### Option 2: Local Project

```bash
# Copy to your project
cp -r bigquery-skills ./skills/bigquery

# Configure in .claude file
echo "skills:" >> .claude
echo "  - ./skills/bigquery" >> .claude
```

## 📖 Usage

### Direct Sub-Skill Access

```bash
# Optimize a query
/bigquery/query-optimization check my query "SELECT * FROM events..."

# Load CSV data
/bigquery/data-loading import CSV from gs://bucket/data.csv

# Create ML model
/bigquery/bqml create churn prediction model

# Setup daily ETL
/bigquery/scheduled-queries setup daily aggregation at 2am

# Analyze costs
/bigquery/cost-monitoring show me expensive queries

# Setup multi-tenant RLS
/bigquery/security setup RLS by tenant_id

# Design schema
/bigquery/schema-design create events table with partitioning

# Debug error
/bigquery/troubleshooting fix error "Resources exceeded"
```

### Auto-Routing

Let Claude decide which sub-skill to use:

```bash
# Claude will route to appropriate skill
/bigquery my query is slow
/bigquery load this CSV into BigQuery
/bigquery predict customer churn
/bigquery why am I spending so much
```

## 🎯 Use Cases

### For Vietnamese Automotive Analytics

```bash
# Design car listings schema
/bigquery/schema-design create car listings table with Vietnamese categories

# Load daily listings
/bigquery/data-loading load daily car data from CSV

# Optimize lead queries
/bigquery/query-optimization optimize daily analytics for tenant_id

# Predict purchase intent
/bigquery/bqml predict car purchase likelihood

# Schedule daily reports
/bigquery/scheduled-queries create daily report for dealerships

# Monitor costs per tenant
/bigquery/cost-monitoring track costs by tenant_id

# Multi-tenant isolation
/bigquery/security setup RLS for dealership access
```

### For Next.js Integration

```javascript
// pages/api/analytics.js
import { BigQuery } from '@google-cloud/bigquery';

// Use query-optimization patterns
const bigquery = new BigQuery();
const query = `
  WITH filtered_events AS (
    SELECT * FROM events
    WHERE tenant_id = @tenantId
      AND DATE(timestamp) = CURRENT_DATE() - 1
  )
  SELECT event_name, COUNT(*) as count
  FROM filtered_events
  GROUP BY event_name
`;
```

## 📊 Feature Coverage

| Feature | Skill | Coverage |
|---------|-------|----------|
| Query Performance | query-optimization | ✅ Complete |
| Data Import/Export | data-loading | ✅ Complete |
| Machine Learning | bqml | ✅ Complete |
| ETL Automation | scheduled-queries | ✅ Complete |
| Cost Analysis | cost-monitoring | ✅ Complete |
| Access Control | security | ✅ Complete |
| Schema Design | schema-design | ✅ Complete |
| Error Resolution | troubleshooting | ✅ Complete |

## 🌏 Vietnamese Market Support

All skills include specific support for:
- UTF-8 Vietnamese characters (Tiếng Việt)
- Vietnam timezone (Asia/Ho_Chi_Minh)
- Vietnamese business terminology (ô tô, xe máy, etc.)
- Multi-tenant Vietnamese automotive use cases

## 🔧 Requirements

### Global Requirements (All Skills)
- BigQuery API enabled
- Service account with permissions
- `bq` CLI OR Python/Node.js client library

### Specific Requirements
- **BQML:** Training data in BigQuery (100+ rows)
- **Scheduled Queries:** Data Transfer Service enabled
- **Security:** BigQuery Admin role
- **Cost Monitoring:** Billing account access

## 📚 Quick Reference

### Query Optimization
```sql
-- Filter on partition first
WHERE DATE(timestamp) = '2024-02-09'

-- Use QUALIFY instead of DISTINCT
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts DESC) = 1
```

### Data Loading
```python
# Load CSV from GCS
client.load_table_from_uri(
    'gs://bucket/file.csv',
    'dataset.table',
    job_config=job_config
)
```

### Machine Learning
```sql
-- Create model
CREATE MODEL dataset.churn_model
OPTIONS(model_type='LOGISTIC_REG', input_label_cols=['churned'])
AS SELECT * FROM training_data;
```

### Scheduled Queries
```bash
# Schedule daily at 2am
--schedule='every day 02:00'
```

### Cost Monitoring
```sql
-- Find expensive queries
SELECT job_id, total_bytes_processed / POW(10,12) * 6.25 as cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
ORDER BY cost_usd DESC;
```

### Security (RLS)
```sql
-- Multi-tenant isolation
CREATE ROW ACCESS POLICY tenant_filter
ON dataset.events
FILTER USING (tenant_id = SESSION_USER_TENANT);
```

### Schema Design
```sql
-- Partitioned and clustered
CREATE TABLE dataset.events
PARTITION BY DATE(timestamp)
CLUSTER BY tenant_id, user_id;
```

### Troubleshooting
```bash
# Dry run to check cost
bq query --dry_run "SELECT ..."
```

## 🔄 Integration Workflow

```
1. Design schema      → /schema-design
2. Load data          → /data-loading
3. Optimize queries   → /query-optimization
4. Create ML models   → /bqml
5. Schedule ETL       → /scheduled-queries
6. Monitor costs      → /cost-monitoring
7. Setup security     → /security
8. Debug issues       → /troubleshooting
```

## 📈 Version History

- **2.0.0** (2024-02-09) - Initial modular skill suite
  - 8 comprehensive sub-skills
  - Vietnamese market support
  - Next.js integration examples
  - Multi-tenant patterns

## 🤝 Support

For issues or feature requests:
1. Check `/bigquery/troubleshooting` first
2. Review relevant sub-skill documentation
3. Update skills based on production learnings

## 📄 License

Free to use and modify for personal and commercial projects.

## 🎓 Learning Path

**Beginner:**
1. Start with `/schema-design` - Learn table structure
2. Use `/data-loading` - Import your first dataset
3. Try `/query-optimization` - Speed up queries

**Intermediate:**
4. Explore `/bqml` - Create prediction models
5. Setup `/scheduled-queries` - Automate workflows
6. Monitor with `/cost-monitoring` - Control spending

**Advanced:**
7. Implement `/security` - Multi-tenant isolation
8. Master `/troubleshooting` - Debug complex issues

## 🌟 Best Practices

1. **Always read the skill** before executing tasks
2. **Test with LIMIT 10** before running on full data
3. **Use partition filters** to reduce costs
4. **Monitor costs** regularly with cost-monitoring skill
5. **Start simple** then add complexity
6. **Document your patterns** in skill files
7. **Share learnings** with your team

---

**Happy querying! 🚀**
