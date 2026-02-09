# BigQuery ML (BQML)

**Parent Skill:** `/bigquery`  
**Path:** `/bigquery/bqml`

## Purpose
Create and deploy machine learning models using only SQL - no Python or separate ML platform required.

## When to Use

**Trigger when:**
- Keywords: predict, forecast, model, ML, classification, regression, clustering
- User wants to: predict churn, forecast sales, segment customers, recommend products

**Chat commands:**
```bash
/bigquery/bqml create churn prediction model
/bigquery/bqml forecast next month revenue
/bigquery/bqml segment customers by behavior
/bigquery/bqml recommend products for user
```

## Requirements

<critical>
- BigQuery access
- Training data in BigQuery tables
- Sufficient data (100+ rows minimum, 1000+ recommended)
</critical>

---

## Model Types

### 1. Linear Regression
**Use for:** Predicting continuous values (price, revenue, age)

```sql
CREATE OR REPLACE MODEL `dataset.price_prediction_model`
OPTIONS(
  model_type='LINEAR_REG',
  input_label_cols=['price']
) AS
SELECT
  bedrooms,
  bathrooms,
  sqft,
  location,
  price
FROM `dataset.housing_data`;
```

### 2. Logistic Regression (Binary Classification)
**Use for:** Yes/No predictions (churn, conversion, click)

```sql
CREATE OR REPLACE MODEL `dataset.churn_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['churned']
) AS
SELECT
  user_tenure_days,
  total_purchases,
  last_purchase_days_ago,
  churned  -- 0 or 1
FROM `dataset.user_features`;
```

### 3. Multiclass Classification
**Use for:** Predicting categories (product category, customer segment)

```sql
CREATE OR REPLACE MODEL `dataset.category_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['category']
) AS
SELECT
  title,
  description,
  price,
  category  -- 'electronics', 'clothing', 'home', etc.
FROM `dataset.products`;
```

### 4. K-Means Clustering
**Use for:** Grouping similar items (customer segmentation)

```sql
CREATE OR REPLACE MODEL `dataset.customer_segments`
OPTIONS(
  model_type='KMEANS',
  num_clusters=5
) AS
SELECT
  avg_purchase_value,
  purchase_frequency,
  days_since_last_purchase,
  total_revenue
FROM `dataset.customer_metrics`;
```

### 5. Time Series (ARIMA)
**Use for:** Forecasting over time (sales, traffic, demand)

```sql
CREATE OR REPLACE MODEL `dataset.sales_forecast`
OPTIONS(
  model_type='ARIMA_PLUS',
  time_series_timestamp_col='date',
  time_series_data_col='revenue'
) AS
SELECT
  date,
  revenue
FROM `dataset.daily_sales`;
```

### 6. Deep Neural Network (DNN)
**Use for:** Complex patterns, non-linear relationships

```sql
CREATE OR REPLACE MODEL `dataset.advanced_prediction`
OPTIONS(
  model_type='DNN_CLASSIFIER',
  hidden_units=[128, 64, 32],
  input_label_cols=['converted']
) AS
SELECT
  * EXCEPT(user_id, timestamp)
FROM `dataset.user_events`;
```

### 7. XGBoost (Best for Tabular Data)
**Use for:** High accuracy classification/regression

```sql
CREATE OR REPLACE MODEL `dataset.xgboost_model`
OPTIONS(
  model_type='BOOSTED_TREE_CLASSIFIER',
  input_label_cols=['target'],
  max_iterations=50
) AS
SELECT
  feature1,
  feature2,
  feature3,
  target
FROM `dataset.training_data`;
```

---

## Model Training Workflow

### Step 1: Prepare Training Data

```sql
-- Create training dataset with features
CREATE OR REPLACE TABLE `dataset.training_features` AS
WITH user_activity AS (
  SELECT
    user_id,
    COUNT(*) as event_count,
    COUNT(DISTINCT DATE(timestamp)) as active_days,
    MAX(timestamp) as last_activity
  FROM events
  WHERE DATE(timestamp) BETWEEN '2024-01-01' AND '2024-01-31'
  GROUP BY user_id
),
user_labels AS (
  SELECT
    user_id,
    IF(COUNT(*) = 0, 1, 0) as churned  -- Churned if no activity in Feb
  FROM events
  WHERE DATE(timestamp) BETWEEN '2024-02-01' AND '2024-02-28'
  GROUP BY user_id
)
SELECT
  a.*,
  COALESCE(l.churned, 1) as churned
FROM user_activity a
LEFT JOIN user_labels l USING (user_id);
```

### Step 2: Split Train/Test

```sql
-- 80/20 split
CREATE OR REPLACE TABLE `dataset.train_data` AS
SELECT * FROM `dataset.training_features`
WHERE MOD(ABS(FARM_FINGERPRINT(CAST(user_id AS STRING))), 10) < 8;

CREATE OR REPLACE TABLE `dataset.test_data` AS
SELECT * FROM `dataset.training_features`
WHERE MOD(ABS(FARM_FINGERPRINT(CAST(user_id AS STRING))), 10) >= 8;
```

### Step 3: Train Model

```sql
CREATE OR REPLACE MODEL `dataset.churn_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['churned'],
  max_iterations=20
) AS
SELECT * EXCEPT(user_id)
FROM `dataset.train_data`;
```

### Step 4: Evaluate Model

```sql
-- Get model metrics
SELECT
  *
FROM
  ML.EVALUATE(MODEL `dataset.churn_model`,
    (SELECT * FROM `dataset.test_data`));

-- Output: precision, recall, accuracy, f1_score, roc_auc
```

**Good Metrics:**
- **Accuracy:** >0.80 (80%+)
- **Precision:** >0.70
- **Recall:** >0.70
- **ROC AUC:** >0.85

### Step 5: Make Predictions

```sql
-- Predict churn for new users
SELECT
  user_id,
  predicted_churned,
  predicted_churned_probs[OFFSET(1)].prob as churn_probability
FROM
  ML.PREDICT(MODEL `dataset.churn_model`,
    (
      SELECT
        user_id,
        event_count,
        active_days,
        last_activity
      FROM `dataset.current_users`
    )
  )
WHERE predicted_churned = 1
ORDER BY churn_probability DESC
LIMIT 100;
```

---

## Advanced Patterns

### Feature Engineering

```sql
-- Create features from raw events
CREATE OR REPLACE TABLE `dataset.ml_features` AS
SELECT
  user_id,
  -- Time-based features
  DATE_DIFF(CURRENT_DATE(), DATE(MIN(timestamp)), DAY) as user_age_days,
  DATE_DIFF(CURRENT_DATE(), DATE(MAX(timestamp)), DAY) as days_since_last_event,
  
  -- Behavioral features
  COUNT(*) as total_events,
  COUNT(DISTINCT DATE(timestamp)) as active_days,
  COUNT(DISTINCT session_id) as total_sessions,
  
  -- Event type features
  COUNTIF(event_name = 'purchase') as purchase_count,
  COUNTIF(event_name = 'view') as view_count,
  COUNTIF(event_name = 'click') as click_count,
  
  -- Ratio features
  SAFE_DIVIDE(
    COUNTIF(event_name = 'purchase'),
    COUNT(*)
  ) as purchase_rate,
  
  -- Revenue features
  SUM(IF(event_name = 'purchase', 
    CAST(JSON_EXTRACT_SCALAR(properties, '$.amount') AS FLOAT64), 
    0)) as total_revenue
  
FROM events
GROUP BY user_id;
```

### Hyperparameter Tuning

```sql
CREATE OR REPLACE MODEL `dataset.tuned_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['churned'],
  l1_reg=0.1,              -- L1 regularization
  l2_reg=0.1,              -- L2 regularization
  max_iterations=50,
  learn_rate=0.01,
  early_stop=TRUE,
  min_rel_progress=0.001
) AS
SELECT * FROM `dataset.train_data`;
```

### Model Versioning

```sql
-- Create new version
CREATE OR REPLACE MODEL `dataset.churn_model_v2`
OPTIONS(
  model_type='BOOSTED_TREE_CLASSIFIER',
  max_iterations=50
) AS
SELECT * FROM `dataset.train_data`;

-- Compare versions
SELECT
  'v1' as version,
  precision,
  recall,
  accuracy,
  roc_auc
FROM ML.EVALUATE(MODEL `dataset.churn_model`, 
  (SELECT * FROM `dataset.test_data`))

UNION ALL

SELECT
  'v2' as version,
  precision,
  recall,
  accuracy,
  roc_auc
FROM ML.EVALUATE(MODEL `dataset.churn_model_v2`,
  (SELECT * FROM `dataset.test_data`));
```

---

## Time Series Forecasting

### ARIMA Model

```sql
-- Forecast next 30 days
CREATE OR REPLACE MODEL `dataset.revenue_forecast`
OPTIONS(
  model_type='ARIMA_PLUS',
  time_series_timestamp_col='date',
  time_series_data_col='revenue',
  holiday_region='VN'  -- Vietnam holidays
) AS
SELECT
  date,
  SUM(amount) as revenue
FROM `dataset.transactions`
GROUP BY date;

-- Get forecast
SELECT
  forecast_timestamp as date,
  forecast_value as predicted_revenue,
  prediction_interval_lower_bound as lower_bound,
  prediction_interval_upper_bound as upper_bound
FROM
  ML.FORECAST(MODEL `dataset.revenue_forecast`,
    STRUCT(30 AS horizon, 0.95 AS confidence_level));
```

---

## Recommendation Systems

```sql
-- Matrix Factorization for recommendations
CREATE OR REPLACE MODEL `dataset.product_recommendations`
OPTIONS(
  model_type='MATRIX_FACTORIZATION',
  user_col='user_id',
  item_col='product_id',
  rating_col='implicit_rating'
) AS
SELECT
  user_id,
  product_id,
  COUNT(*) as implicit_rating  -- View count as implicit rating
FROM events
WHERE event_name = 'product_view'
GROUP BY user_id, product_id;

-- Get recommendations for user
SELECT
  product_id,
  predicted_implicit_rating
FROM
  ML.RECOMMEND(MODEL `dataset.product_recommendations`,
    (SELECT 'user_123' as user_id));
```

---

## Model Management

### Export Model

```sql
-- Export model for deployment
EXPORT MODEL `dataset.churn_model`
OPTIONS(
  uri='gs://my-bucket/models/churn_model_*'
);
```

### Import Model

```sql
CREATE OR REPLACE MODEL `dataset.imported_model`
OPTIONS(
  model_type='TENSORFLOW',
  model_path='gs://my-bucket/models/churn_model_*'
);
```

### Delete Model

```sql
DROP MODEL IF EXISTS `dataset.old_model`;
```

---

## Cost Optimization

**BQML Pricing:**
- **CREATE MODEL:** $250 per TB processed
- **ML.PREDICT:** $5 per TB processed  
- **ML.EVALUATE:** $5 per TB processed

**Tips:**
- Use sampling for large datasets
- Partition training data by date
- Reuse models instead of retraining daily

```sql
-- Train on sample for development
CREATE OR REPLACE MODEL `dataset.sample_model`
OPTIONS(model_type='LOGISTIC_REG', input_label_cols=['target'])
AS
SELECT * FROM `dataset.training_data`
TABLESAMPLE SYSTEM (10 PERCENT);  -- Use only 10%
```

---

## Vietnamese Use Case: Car Sales Prediction

```sql
-- Predict likelihood of car purchase
CREATE OR REPLACE MODEL `dataset.car_purchase_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['purchased']
) AS
SELECT
  -- Demographics
  CASE 
    WHEN age < 25 THEN '18-24'
    WHEN age < 35 THEN '25-34'
    WHEN age < 45 THEN '35-44'
    ELSE '45+' 
  END as age_group,
  
  -- Location (Vietnam cities)
  CASE
    WHEN city IN ('Hồ Chí Minh', 'Hà Nội') THEN 'tier1'
    WHEN city IN ('Đà Nẵng', 'Cần Thơ', 'Hải Phòng') THEN 'tier2'
    ELSE 'tier3'
  END as city_tier,
  
  -- Behavior
  page_views,
  search_count,
  days_since_first_visit,
  
  -- Engagement
  COUNTIF(event_name = 'phone_click') as phone_clicks,
  COUNTIF(event_name = 'form_submit') as form_submits,
  
  -- Target
  purchased
FROM `dataset.car_leads`;
```

---

## Integration with Other Skills

**Workflow:**
1. Load training data → `/bigquery/data-loading`
2. Feature engineering → `/bigquery/query-optimization`
3. Train model → `/bigquery/bqml`
4. Schedule predictions → `/bigquery/scheduled-queries`
5. Monitor costs → `/bigquery/cost-monitoring`

---

## Quick Reference

| Task | Model Type | Use Case |
|------|------------|----------|
| Predict price | LINEAR_REG | Car pricing, revenue forecast |
| Predict churn | LOGISTIC_REG | Customer retention |
| Segment users | KMEANS | Customer clustering |
| Forecast sales | ARIMA_PLUS | Time series prediction |
| Recommend | MATRIX_FACTORIZATION | Product recommendations |
| High accuracy | BOOSTED_TREE | Complex classification |

## Version

- **Version:** 1.0.0
- **Last Updated:** 2024-02-09
