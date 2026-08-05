# Bank Customer Churn Analysis

Predicting which bank customers are likely to leave (churn), and identifying the key drivers behind churn — so the business can target retention efforts where they matter most.

## 📌 Business Problem

Customer churn is expensive: acquiring a new customer costs far more than retaining an existing one. This project analyzes 10,000 bank customer records to answer:

- Which customers are most likely to churn?
- What factors are driving churn (geography, age, balance, product usage, engagement)?
- Can we build a model to flag at-risk customers in advance?

## 📊 Dataset

- **Source:** Customer-Churn-Records.csv (10,000 rows)
- **Key columns:** CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited (target), Complain, Satisfaction Score, Card Type, Point Earned

## 🔍 Key Findings

- **Geography matters:** Germany has a significantly higher churn rate than France or Spain — driven mainly by balance differences, not demographics (confirmed via chi-square test).
- **Age:** Older customers churn at a higher rate than younger ones (Mann-Whitney U test, statistically significant).
- **Balance:** Customers who churn tend to hold higher balances (Mann-Whitney U test, statistically significant).
- **Number of products:** Customers with only 1 product churn far more than those with 2+ (chi-square test, statistically significant).
- **Active membership:** Inactive members churn at a noticeably higher rate (chi-square test, statistically significant).
- **Complaints:** Almost every customer who complained also churned — flagged as data leakage and excluded from modeling since it isn't a genuine predictive signal.
- **Satisfaction Score:** No meaningful relationship with churn (chi-square test, not significant) — a useful negative finding.

## 🤖 Predictive Modeling

Two models were built and compared to predict churn:

| Model | Recall (Churn class) | ROC-AUC |
|---|---|---|
| Logistic Regression | 0.21 | 0.78 |
| **Random Forest** | **0.72** | **0.87** |

Random Forest was selected as the final model — it catches far more actual churners (recall), which matters more than raw accuracy in a churn use case, since missing a churner is costlier than a false alarm.

**Top features driving churn (by importance):** Age, Number of Products, Balance, Geography, Active Membership.

## 📈 Dashboard

An interactive Power BI dashboard (2 pages) accompanies this analysis:

- **Page 1 — Overview:** KPI cards + breakdowns by Geography, Number of Products, Active Membership, Balance Group, Age Group, and Satisfaction Score.
- **Page 2 — Risk Segments & Predictive Model:** Combined risk segmentation, geography comparison, complaint/leakage view, card type breakdown, and model performance comparison.

📄 See `Bank_Churn_Analysis_Dashboard.pdf` for a static preview, or open `Bank_Churn_Analysis_Dashboard.pbix` in Power BI Desktop for the interactive version.

## 🛠️ Tools Used

- **Python (Google Colab):** Data cleaning, EDA, statistical testing, machine learning (Random Forest, Logistic Regression)
- **SQL:** Business-question queries validated against Python results
- **Power BI:** Interactive dashboard and visualization

## 💡 Business Recommendations

- Prioritize retention outreach for single-product, inactive, high-balance customers in Germany.
- Investigate why Germany's higher balances correlate with higher churn — possible service/expectation mismatch.
- Use the Random Forest model to flag at-risk customers for proactive retention campaigns.
- Treat "Complain" as a lagging indicator, not a predictive one — act on the leading indicators (product count, activity, balance) instead.

## 📁 Repository Structure

```
├── data/                                     # Raw and cleaned datasets
├── BankCustomerChurnAnalysis.ipynb           # Full analysis notebook (EDA, stats tests, modeling)
├── Bank_Churn_Analysis_Dashboard.pbix        # Power BI dashboard file
├── Bank_Churn_Analysis_Dashboard.pdf         # Dashboard PDF preview
└── README.md
```
