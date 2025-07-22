import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Bank Customer Churn Dashboard", layout="wide")

# Title
st.title("🏦 Bank Customer Churn Dashboard")

# Sidebar for Country Selection
st.sidebar.title("Select Country")
country = st.sidebar.selectbox("Choose a country", ["France", "Germany", "Spain"])

# Load the appropriate dataset
@st.cache_data
def load_country_data(selected_country):
    """Loads and caches data for a single country."""
    file_map = {
        "France": "france_df.csv",
        "Germany": "germany_df.csv",
        "Spain": "spain_df.csv"
    }
    df = pd.read_csv(file_map[selected_country])
    # Drop columns that are consistently present
    cols_to_drop = ['Unnamed: 0', 'RowNumber']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    return df

# In your main script, call the function with the selected country
country = st.sidebar.selectbox("Choose a country", ["France", "Germany", "Spain"])
df = load_country_data(country)


# Optional: Rename churn column if needed
if 'Exited' not in df.columns:
    st.error("The expected column `Exited` is not found in the dataset.")
    st.stop()

# Show basic stats
st.markdown(f"### Dataset Overview - {country}")
st.dataframe(df.head())

# Show metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", len(df))
with col2:
    st.metric("Churned Customers", df['Exited'].sum())
with col3:
    churn_rate = df['Exited'].mean() * 100
    st.metric("Churn Rate (%)", f"{churn_rate:.2f}")

# Plot 1: Churn Distribution
fig1 = px.histogram(df, x='Exited', color='Exited',
                    title="Churn Distribution",
                    labels={'Exited': 'Churned (1) vs Not Churned (0)'},
                    barmode='group',
                    nbins=1)
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Churn by Gender
if 'Gender' in df.columns:
    fig2 = px.histogram(df, x='Gender', color='Exited', barmode='group',
                        title="Churn by Gender")
    st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Churn by Age
if 'Age' in df.columns:
    fig3 = px.box(df, x='Exited', y='Age', color='Exited',
                  title="Age Distribution by Churn Status")
    st.plotly_chart(fig3, use_container_width=True)

# Plot 4: Churn by Credit Score (Optional)
if 'CreditScore' in df.columns:
    fig4 = px.histogram(df, x='CreditScore', color='Exited',
                        title="Credit Score Distribution by Churn")
    st.plotly_chart(fig4, use_container_width=True)
# Section: Age Group vs Estimated Salary (Box Plot)
if 'AgeGroup' in df.columns and 'EstimatedSalary' in df.columns:
    st.markdown("### Estimated Salary by Age Group (Box Plot)")
    fig5 = px.box(df, x='AgeGroup', y='EstimatedSalary', color='AgeGroup',
                  title="Estimated Salary Distribution Across Age Groups")
    st.plotly_chart(fig5, use_container_width=True)

# Section: Age Group vs Estimated Salary by Card Type (Bar Plot)
if 'AgeGroup' in df.columns and 'Card Type' in df.columns:
    st.markdown("### Avg Estimated Salary by Age Group & Card Type")
    grouped_df = df.groupby(['AgeGroup', 'Card Type'])['EstimatedSalary'].mean().reset_index()
    fig6 = px.bar(grouped_df, x='AgeGroup', y='EstimatedSalary',
                  color='Card Type', barmode='group',
                  title="Average Estimated Salary by Age Group and Card Type")
    st.plotly_chart(fig6, use_container_width=True)

# Bonus: Pie Chart of Churn
st.markdown("### Churn Breakdown")
churn_counts = df['Exited'].value_counts().rename({0: 'Retained', 1: 'Churned'})
fig7 = px.pie(values=churn_counts.values, names=churn_counts.index,
              title='Churn vs Retention')
st.plotly_chart(fig7, use_container_width=True)

# Bonus: Churn by Tenure (if column exists)
if 'Tenure' in df.columns:
    st.markdown("### Churn by Tenure")
    fig8 = px.histogram(df, x='Tenure', color='Exited',
                        title="Churn Distribution by Customer Tenure",barmode='group')
    st.plotly_chart(fig8, use_container_width=True)
# Plot: Churn by Credit Score Category
if 'CreditScoreCategory' in df.columns:
    st.markdown("### Churn by Credit Score Category")

    fig9 = px.histogram(
        df,
        x='CreditScoreCategory',
        color='Exited',
        barmode='group',
        title='Churn Distribution Across Credit Score Categories',
        labels={'Exited': 'Churn Status', 'Credit Score Category': 'Credit Score Category'},
        category_orders={'Credit Score Category': sorted(df['CreditScoreCategory'].unique())}
    )
    fig9.update_layout(xaxis_title="Credit Score Category", yaxis_title="Number of Customers")
    st.plotly_chart(fig9, use_container_width=True)

# Insights Section
st.markdown("##  Key Findings & Insights")

# Compute metrics for insights
churned = df[df['Exited'] == 1]
retained = df[df['Exited'] == 0]

avg_salary_churned = churned['EstimatedSalary'].mean()
avg_salary_retained = retained['EstimatedSalary'].mean()

top_card_churned = churned['Card Type'].value_counts().idxmax() if 'Card Type' in churned else 'N/A'
common_agegroup_churned = churned['AgeGroup'].value_counts().idxmax() if 'AgeGroup' in churned else 'N/A'

# Streamlit dark/light theme-aware styles using inline CSS and Streamlit's theme
country_heading_colors = {
    "France": "#0055A4",     # French Blue
    "Germany": "#D00000",    # German Red
    "Spain": "#FFC400"       # Spanish Yellow
}
heading_color = country_heading_colors.get(country, "#FFD700") 
insight_template = f"""
<style>
.insight-box {{
    background-color: rgba(240, 240, 240, 0.05);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}}
.insight-box h3 {{
    color: {heading_color};
    margin-top: 0;
}}
.insight-box ul {{
    padding-left: 1.2rem;
    color: inherit;
}}
.insight-box li {{
    margin-bottom: 0.6rem;
}}
.insight-box p {{
    font-style: italic;
    color: gray;
}}
</style>

<div class="insight-box">
  <h3> {country} — Churn Analysis Summary</h3>
  <ul>
    <li> <strong>Churn Rate:</strong> <span style="color:#e74c3c;"><strong>{churn_rate:.2f}%</strong></span></li>
    <li> <strong>Avg Salary (Churned):</strong> €{avg_salary_churned:,.0f}</li>
    <li> <strong>Most Common Card Type among Churned:</strong> {top_card_churned}</li>
    <li> <strong>Most Affected Age Group:</strong> {common_agegroup_churned}</li>
    <li> <strong>Avg Salary (Retained):</strong> €{avg_salary_retained:,.0f}</li>
  </ul>
  <p> Tip: Target churn-prone age groups and card holders with personalized offers.</p>
</div>
"""

# Display it
st.markdown(insight_template, unsafe_allow_html=True)
st.markdown("---")

# 🔗 LinkedIn Buttons
st.markdown("## Connect with Me")
linkedin_url = "http://www.linkedin.com/in/neha-sharma-09835724b"  # <-- change this to your actual LinkedIn
github_url = "https://github.com/NehaSharma-26"  # optional

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
        <a href="{linkedin_url}" target="_blank">
            <button style='background-color:#0e76a8; color:white; padding:10px 24px; border:none; border-radius:8px; font-size:16px; cursor:pointer;'>💼 LinkedIn Profile</button>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <a href="{github_url}" target="_blank">
            <button style='background-color:#333; color:white; padding:10px 24px; border:none; border-radius:8px; font-size:16px; cursor:pointer;'>💻 GitHub Projects</button>
        </a>
    """, unsafe_allow_html=True)

# ❓ FAQ Section
st.markdown("## Frequently Asked Questions")

with st.expander("What does 'churn' mean in this dashboard?"):
    st.write("Churn refers to customers who have exited the bank — meaning they’ve closed their accounts or stopped using services.")

with st.expander("How is churn rate calculated?"):
    st.write("Churn Rate = (Number of Churned Customers / Total Customers) × 100")

with st.expander("What is the meaning of 'Card Type'?"):
    st.write("This usually refers to the type of bank card issued to the customer (e.g., Gold, Silver, Platinum), which may correlate with spending habits or services.")

with st.expander("How was this dashboard built?"):
    st.write("This dashboard was created using Python, Streamlit, and Plotly for interactive data visualization. It’s meant to simulate a PowerBI-like dashboard in code.")


