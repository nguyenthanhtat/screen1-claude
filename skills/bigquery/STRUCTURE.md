# BigQuery Skills Structure

## Overview

This is a modular skill suite for BigQuery with 1 main router and 8 specialized sub-skills.

## Directory Layout

```
bigquery-skills/
│
├── README.md                    # Main documentation
├── INSTALLATION.md              # Installation guide
├── STRUCTURE.md                 # This file
├── .claude.example              # Example configuration
│
├── SKILL.md                     # 🎯 MAIN ROUTER SKILL
│   └── Routes to appropriate sub-skill based on user request
│
├── query-optimization/          # 🚀 Performance & Cost
│   └── SKILL.md
│       ├── 8 optimization patterns
│       ├── Common pitfalls
│       ├── Vietnamese support
│       └── Integration guides
│
├── data-loading/                # 📥 Import/Export
│   └── SKILL.md
│       ├── CSV, JSON, Parquet loading
│       ├── Streaming inserts
│       ├── Federated queries
│       └── Export patterns
│
├── bqml/                        # 🤖 Machine Learning
│   └── SKILL.md
│       ├── 7 model types
│       ├── Training workflows
│       ├── Predictions
│       └── Time series forecasting
│
├── scheduled-queries/           # ⏰ Automation
│   └── SKILL.md
│       ├── Cron scheduling
│       ├── ETL patterns
│       ├── Error handling
│       └── Notification setup
│
├── cost-monitoring/             # 💰 Budget Control
│   └── SKILL.md
│       ├── Cost analysis queries
│       ├── Budget alerts
│       ├── Optimization tips
│       └── Multi-tenant attribution
│
├── security/                    # 🔒 Access Control
│   └── SKILL.md
│       ├── Row-level security
│       ├── Column masking
│       ├── IAM roles
│       └── Audit logging
│
├── schema-design/               # 📊 Table Structure
│   └── SKILL.md
│       ├── Partitioning strategies
│       ├── Clustering
│       ├── Data types
│       └── Nested/repeated fields
│
└── troubleshooting/             # 🔧 Debug & Fix
    └── SKILL.md
        ├── Common errors (403, 400, 404, 429)
        ├── Performance debugging
        ├── Data quality checks
        └── Emergency fixes

```

## How It Works

### 1. User Request
```
User: /bigquery my query is slow
```

### 2. Main Router (SKILL.md)
Analyzes keywords and routes to appropriate sub-skill:
- "slow" → `/query-optimization`
- "load" → `/data-loading`
- "predict" → `/bqml`
- "cost" → `/cost-monitoring`
- etc.

### 3. Sub-Skill Execution
The routed sub-skill provides:
- Specific instructions
- Code examples
- Best practices
- Step-by-step guides

## Skill Relationships

```
Main SKILL.md
    │
    ├─→ query-optimization ─→ cost-monitoring (verify savings)
    │                     └─→ schema-design (improve structure)
    │
    ├─→ data-loading ─────→ query-optimization (optimize after load)
    │                 └─→ scheduled-queries (automate loading)
    │
    ├─→ bqml ─────────────→ data-loading (prepare training data)
    │                 └─→ scheduled-queries (automate predictions)
    │
    ├─→ scheduled-queries ─→ cost-monitoring (track automation costs)
    │
    ├─→ security ──────────→ troubleshooting (fix permission errors)
    │
    └─→ troubleshooting ───→ [any skill] (debug issues)
```

## File Sizes (Approximate)

| File | Lines | Focus |
|------|-------|-------|
| SKILL.md (main) | 350 | Routing & overview |
| query-optimization/SKILL.md | 600 | Performance tuning |
| data-loading/SKILL.md | 500 | Import/export |
| bqml/SKILL.md | 450 | Machine learning |
| scheduled-queries/SKILL.md | 400 | Automation |
| cost-monitoring/SKILL.md | 450 | Cost analysis |
| security/SKILL.md | 200 | Access control |
| schema-design/SKILL.md | 350 | Table design |
| troubleshooting/SKILL.md | 300 | Debugging |

**Total: ~3600 lines of curated BigQuery knowledge**

## Usage Patterns

### Pattern 1: Direct Access
```bash
/bigquery/query-optimization check my query "SELECT ..."
```
Directly calls specific sub-skill.

### Pattern 2: Auto-Routing
```bash
/bigquery my query takes 2 minutes to run
```
Main router analyzes and routes to `query-optimization`.

### Pattern 3: Workflow
```bash
# Step 1: Design
/bigquery/schema-design create events table

# Step 2: Load
/bigquery/data-loading import CSV

# Step 3: Optimize
/bigquery/query-optimization improve this query

# Step 4: Automate
/bigquery/scheduled-queries run daily at 2am
```

## Customization Points

### Add Your Own Patterns

Each sub-skill can be extended with:

1. **Company-specific patterns:**
   ```sql
   -- Add to query-optimization/SKILL.md
   ### Pattern 9: Our Company's Multi-Region Pattern
   ```

2. **Team conventions:**
   ```sql
   -- Add to schema-design/SKILL.md
   ### Our Naming Convention
   dataset: {environment}_{team}_{purpose}
   table: {date_YYYYMMDD}_{entity}
   ```

3. **Custom commands:**
   ```yaml
   # Add to .claude
   commands:
     our-etl: "Use /bigquery/scheduled-queries with our company ETL pattern"
   ```

## Integration Points

### With Other Tools

- **dbt:** See `scheduled-queries/SKILL.md`
- **Airflow:** See `scheduled-queries/SKILL.md`
- **Next.js:** Examples in main `README.md`
- **Looker Studio:** See `cost-monitoring/SKILL.md`

### With Other Skills

If you have other Claude skills:

```yaml
# .claude
skills:
  - ./skills/bigquery          # This skill suite
  - ./skills/python-data       # Your Python data skill
  - ./skills/api-integration   # Your API skill
```

They can reference each other:
```
Use /bigquery for data loading, then use /python-data for processing
```

## Maintenance

### Updating Individual Skills

To update just one sub-skill:

```bash
# Edit the specific skill
nano skills/bigquery/query-optimization/SKILL.md

# Add new pattern
# Test with specific queries
# Document in skill file
```

### Version Control

Recommended structure for git:

```
.gitignore:
  .claude         # Don't commit (contains local paths)

README:
  - Version number in main SKILL.md
  - Changelog in each sub-skill
  - Document breaking changes
```

## Key Concepts

### 1. Skills are Instructions
Not code - they're detailed instructions for Claude to follow.

### 2. Examples are Critical
Every pattern includes good/bad examples with explanations.

### 3. Context Matters
Skills include Vietnamese-specific examples because you work with Vietnamese data.

### 4. Workflows Over One-Offs
Skills show how to chain operations, not just isolated tasks.

## Performance

Skills are optimized for:
- **Fast loading:** Small markdown files
- **Quick parsing:** Clear structure with headings
- **Easy navigation:** Numbered patterns and sections
- **Minimal redundancy:** Cross-references instead of duplication

## Future Enhancements

Potential additions:
- **Advanced patterns:** Streaming analytics, real-time dashboards
- **Tool integration:** Terraform for infrastructure, dbt templates
- **Industry-specific:** E-commerce, finance, healthcare patterns
- **Regional support:** More Vietnamese business scenarios

---

**This structure balances completeness with maintainability.**

Each skill is self-contained yet aware of others, making the suite both powerful and flexible.
