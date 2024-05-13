import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Load the data
@st.cache
def load_data():
    return pd.read_csv("startup_data.csv"), pd.read_csv("competitors_data.csv")

df, df_competitors = load_data()

# Page Title
st.title('Startup Investment Analysis Dashboard')

# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.selectbox("Select a Page", ["Overview", "Financial Health", "Competitive Landscape", "Company Data"])

if page == "Overview":
    st.header("Investment Portfolio Overview")
    # Quick stats
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Companies", len(df))
    col2.metric("Average EBITDA", f"${df['EBITDA'].mean():,.0f}")
    col3.metric("Average Runway (Months)", f"{df['runway'].mean():.1f}")
    
    # Interactive sector distribution
    st.subheader("Sector Distribution")
    fig, ax = plt.subplots()
    sector_data = df['industry'].value_counts().rename_axis('industry').reset_index(name='counts')
    sns.barplot(data=sector_data, x='industry', y='counts', ax=ax)
    ax.set_title('Number of Companies by Industry')
    st.pyplot(fig)

elif page == "Financial Health":
    st.header("Financial Health Metrics")
    company_name = st.selectbox("Select a Company", df['company_name'].unique())
    selected_company = df[df['company_name'] == company_name].iloc[0]
    
    st.subheader("Key Financial Ratios")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Quick Ratio", f"{selected_company['quick_ratio']:.2f}")
    col2.metric("Debt to Equity", f"{selected_company['debt_to_equity']:.2f}")
    col3.metric("Gross Margin", f"{selected_company['gross_margin']}%")
    col4.metric("Net Profit Margin", f"{selected_company['net_profit_margin']}%")

elif page == "Competitive Landscape":
    st.header("Competitive Landscape Analysis")
    company_name = st.selectbox("Select a Company", df['company_name'].unique())
    company_id = df[df['company_name'] == company_name]['company_id'].values[0]
    company_data = df[df['company_id'] == company_id]
    competitors_data = df_competitors[df_competitors['company_id'] == company_id]

    
    # Plot radar chart for competitive analysis
    labels=np.array(['Quality', 'Price', 'Innovation', 'Customer Service'])
    num_vars = len(labels)
    
    # Create a radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one axe per variable and add labels
    plt.xticks(angles[:-1], labels)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([5,7,9], ["5","7","9"], color="grey", size=7)
    plt.ylim(0,10)
    
    # Company data
    values = company_data[['quality', 'price', 'innovation', 'customer_service']].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=company_name)

    # Competitors average data
    avg_values = competitors_data.mean()[['competitor_quality', 'competitor_price', 'competitor_innovation', 'competitor_customer_service']].values.flatten().tolist()
    avg_values += avg_values[:1]
    ax.plot(angles, avg_values, linewidth=1, linestyle='solid', label='Average Competitor', color='red')
    ax.fill(angles, avg_values, 'red', alpha=0.1)

    # Add legend, titles, and labels
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], labels)
    ax.set_rlabel_position(0)
    plt.yticks([5,7,9], ["5","7","9"], color="grey", size=7)
    plt.ylim(0,10)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    st.pyplot(fig)

elif page == "Company Data":
    st.header("Explore Company Data")
    company_name = st.selectbox("Select a Company", df['company_name'].unique())
    company_data = df[df['company_name'] == company_name].iloc[0]

    st.subheader(f"Fact Sheet: {company_name}")
    metrics = pd.DataFrame({
        'Metric': ['EBITDA', 'Monthly Revenue', 'Capital Raised', 'Burn Rate', 'Runway'],
        'Value': [
            f"${company_data['EBITDA']:,.0f}",
            f"${company_data['revenue_monthly']:,.0f}/month",
            f"${company_data['capital_raised']:,.0f}",
            f"${company_data['burn_rate']:,.0f}/month",
            f"{company_data['runway']:,.1f} months"
        ]
    })
    # Presenting data in a cleaner format
    st.table(company_data.transpose())

    st.write("### Detailed Performance Metrics")
    performance_fig, ax = plt.subplots()
    sns.barplot(ax=ax, data=metrics, x='Metric', y='Value')
    ax.set_title('Performance Metrics Overview')
    ax.set_ylabel('Value')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    st.pyplot(performance_fig)

# Footer
st.sidebar.text("Developed by Your Company")
st.sidebar.text("2024 © All Rights Reserved")
