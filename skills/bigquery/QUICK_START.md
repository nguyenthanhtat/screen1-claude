# 🚀 BigQuery Skills - Quick Start

## 📦 What You Have

You now have a complete BigQuery skill suite with:

✅ **1 Main Router Skill** - Automatically routes to the right sub-skill
✅ **8 Specialized Sub-Skills:**
  1. Query Optimization - Speed up queries, reduce costs
  2. Data Loading - Import/export CSV, JSON, Parquet
  3. BQML - Machine learning with SQL
  4. Scheduled Queries - Automate ETL pipelines
  5. Cost Monitoring - Track and reduce spending
  6. Security - RLS, IAM, audit logging
  7. Schema Design - Partitioning, clustering
  8. Troubleshooting - Debug errors

✅ **~3600 lines** of curated BigQuery knowledge
✅ **Vietnamese market support** (UTF-8, timezone, examples)
✅ **Next.js integration** examples

---

## 🎯 Installation (Choose One)

### Option A: Extract & Use Directly

```bash
# Extract archive
tar -xzf bigquery-skills.tar.gz

# Copy to Claude skills directory
cp -r bigquery-skills /mnt/skills/user/bigquery

# OR copy to your project
cp -r bigquery-skills ./skills/bigquery
```

### Option B: Use Folder Directly

The `bigquery-skills/` folder is ready to use as-is!

```bash
# Just move it where you want
mv bigquery-skills /path/to/your/project/skills/bigquery
```

---

## ✅ Verify Installation

Test that skills work:

```bash
# Method 1: Direct command (if installed in /mnt/skills/user/)
/bigquery

# Method 2: Via Claude Code
claude ask "/bigquery help"

# Method 3: In Claude AI chat
Type: /bigquery
```

You should see the main skill menu with all 8 sub-skills listed.

---

## 🎮 Try It Out

### Example 1: Optimize a Query

```bash
/bigquery/query-optimization check my query "
SELECT *
FROM events
JOIN users USING (user_id)
WHERE event_name = 'purchase'
"
```

Claude will:
- Identify performance issues
- Suggest adding partition filter
- Recommend removing SELECT *
- Show optimized version

### Example 2: Load CSV Data

```bash
/bigquery/data-loading import CSV from gs://my-bucket/data.csv into dataset.table
```

Claude will:
- Generate Python/CLI code
- Include schema detection
- Add error handling
- Suggest next steps

### Example 3: Create ML Model

```bash
/bigquery/bqml create churn prediction model using users table
```

Claude will:
- Design feature engineering
- Create train/test split
- Generate CREATE MODEL SQL
- Include evaluation queries

---

## 📖 Documentation

All documentation is in the `bigquery-skills/` folder:

- **README.md** - Main documentation (read this first!)
- **INSTALLATION.md** - Detailed installation guide
- **STRUCTURE.md** - How the skills are organized
- **.claude.example** - Example configuration file

Each sub-skill folder has its own SKILL.md with:
- When to use
- Requirements
- Patterns and examples
- Quick reference

---

## 💡 Common Usage Patterns

### Auto-Routing (Let Claude Decide)

```
User: /bigquery my query is slow
Claude: [Routes to query-optimization]

User: /bigquery load this CSV
Claude: [Routes to data-loading]

User: /bigquery predict customer churn
Claude: [Routes to bqml]
```

### Direct Sub-Skill Access

```bash
# Go directly to specific skill
/bigquery/query-optimization
/bigquery/data-loading
/bigquery/bqml
/bigquery/scheduled-queries
/bigquery/cost-monitoring
/bigquery/security
/bigquery/schema-design
/bigquery/troubleshooting
```

### Workflow Chain

```bash
# Complete workflow
1. /bigquery/schema-design create partitioned table
2. /bigquery/data-loading import data
3. /bigquery/query-optimization optimize queries
4. /bigquery/scheduled-queries automate daily
5. /bigquery/cost-monitoring track spending
```

---

## 🌏 Vietnamese Use Cases

All skills include Vietnamese-specific examples:

```sql
-- UTF-8 Vietnamese text
WHERE name LIKE '%ô tô%'

-- Vietnam timezone
DATETIME(timestamp, 'Asia/Ho_Chi_Minh')

-- Vietnamese automotive categories
category IN ('ô tô', 'xe máy', 'xe tải')
```

---

## 🔧 Configuration

### Create .claude File (Optional)

```bash
cd your-project/
cat > .claude << 'EOF'
skills:
  - ./skills/bigquery

# Optional shortcuts
commands:
  optimize: "Use /bigquery/query-optimization"
  load: "Use /bigquery/data-loading"
EOF
```

---

## 📊 What Each Skill Does

| Skill | Use When | Example |
|-------|----------|---------|
| query-optimization | Query slow, high cost, duplicates | "Optimize this JOIN query" |
| data-loading | Import/export data | "Load CSV from GCS" |
| bqml | Need predictions, forecasts | "Predict churn" |
| scheduled-queries | Automate recurring tasks | "Run daily at 2am" |
| cost-monitoring | Track spending | "Show expensive queries" |
| security | Control access, RLS | "Setup multi-tenant RLS" |
| schema-design | Create tables | "Design partitioned table" |
| troubleshooting | Debug errors | "Fix permission error" |

---

## 🚦 Next Steps

1. ✅ **Install** skills (see above)
2. 📖 **Read** README.md for full documentation
3. 🎯 **Try** a simple command: `/bigquery/query-optimization`
4. 🔨 **Customize** with your own patterns
5. 🔄 **Iterate** based on your use cases

---

## 🆘 Need Help?

**Skills not loading?**
- Check INSTALLATION.md
- Verify path in .claude file
- Ensure SKILL.md files exist

**Want to customize?**
- Each SKILL.md is editable
- Add your own patterns
- Update examples for your data

**Found an issue?**
- Use `/bigquery/troubleshooting`
- Check error messages
- Review skill documentation

---

## 📦 What's in the Package

```
bigquery-skills/
├── README.md              ← Start here!
├── INSTALLATION.md        ← Setup guide
├── STRUCTURE.md          ← Architecture
├── .claude.example       ← Config template
├── SKILL.md              ← Main router
└── [8 sub-skill folders]
```

**Total files:** 12 markdown files
**Total size:** ~33KB (compressed)
**Knowledge:** ~3600 lines of BigQuery expertise

---

## 🎉 You're Ready!

Start using BigQuery skills now:

```bash
/bigquery help
```

Or jump right in:

```bash
/bigquery/query-optimization check my query "SELECT * FROM events"
```

**Happy querying! 🚀**

---

*Created: 2024-02-09*  
*Version: 2.0.0*
