import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import custom modules
from data_generator import generate_sample_data, get_company_list, get_date_range
from data_fusion import fuse_employment_data, calculate_industry_trends, get_summary_statistics, filter_data
from ai_insights import generate_ai_insights, predict_trends, generate_recommendations
from visualizations import (
    create_timeline_chart, create_company_comparison_chart, create_industry_heatmap,
    create_net_change_chart, create_top_companies_chart, create_quarterly_trends
)

# Page configuration
st.set_page_config(
    page_title="AI Powered Data Fusion and Visualization Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the sample data"""
    return generate_sample_data()

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Powered Data Fusion and Visualization Dashboards</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Tech Industry Employment Analytics & Insights</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading employment data..."):
        layoffs_df, hiring_df = load_data()
        fused_df = fuse_employment_data(layoffs_df, hiring_df)
        stats = get_summary_statistics(layoffs_df, hiring_df, fused_df)
    
    # Sidebar filters
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    
    # Company filter
    all_companies = get_company_list(layoffs_df, hiring_df)
    selected_companies = st.sidebar.multiselect(
        "Select Companies",
        options=all_companies,
        default=all_companies[:5],
        help="Choose companies to analyze"
    )
    
    # Year filter
    years = sorted(layoffs_df['year'].unique())
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=years,
        default=years,
        help="Choose years to analyze"
    )
    
    # Month filter
    months = list(range(1, 13))
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    selected_months = st.sidebar.multiselect(
        "Select Months",
        options=months,
        default=months,
        format_func=lambda x: month_names[x],
        help="Choose months to analyze"
    )
    
    # Industry filter
    industries = sorted(layoffs_df['industry'].unique())
    selected_industries = st.sidebar.multiselect(
        "Select Industries",
        options=industries,
        default=industries,
        help="Choose industries to analyze"
    )
    
    # Filter data based on selections
    filtered_layoffs = filter_data(layoffs_df, selected_companies, selected_years, selected_months, selected_industries)
    filtered_hiring = filter_data(hiring_df, selected_companies, selected_years, selected_months, selected_industries)
    filtered_fused = filter_data(fused_df, selected_companies, selected_years, selected_months, selected_industries)
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Trends", "🏢 Companies", "🏭 Industries", "🤖 AI Insights"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">📊 Executive Summary</h2>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_layoffs = filtered_layoffs['layoffs'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Layoffs</h3>
                <h2>{total_layoffs:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_hires = filtered_hiring['hires'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Hiring</h3>
                <h2>{total_hires:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            net_change = total_hires - total_layoffs
            color = "green" if net_change >= 0 else "red"
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {color} 0%, {'#2d5a27' if net_change >= 0 else '#5a2d2d'} 100%);">
                <h3>Net Change</h3>
                <h2>{net_change:+,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            active_companies = len(set(filtered_layoffs['company'].unique()) | set(filtered_hiring['company'].unique()))
            st.markdown(f"""
            <div class="metric-card">
                <h3>Active Companies</h3>
                <h2>{active_companies}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Timeline visualization
        if not filtered_layoffs.empty and not filtered_hiring.empty:
            st.plotly_chart(create_timeline_chart(filtered_layoffs, filtered_hiring), use_container_width=True)
        
        # Net change chart
        if not filtered_fused.empty:
            st.plotly_chart(create_net_change_chart(filtered_fused), use_container_width=True)
    
    with tab2:
        st.markdown('<h2 class="sub-header">📈 Trend Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not filtered_layoffs.empty and not filtered_hiring.empty:
                st.plotly_chart(create_quarterly_trends(filtered_layoffs, filtered_hiring), use_container_width=True)
        
        with col2:
            # Monthly breakdown
            monthly_data = filtered_fused.groupby('month').agg({
                'layoffs': 'sum',
                'hires': 'sum',
                'net_change': 'sum'
            }).reset_index()
            
            if not monthly_data.empty:
                monthly_data['month_name'] = monthly_data['month'].map(month_names)
                
                fig = px.line(monthly_data, x='month_name', y=['layoffs', 'hires'], 
                             title='Monthly Employment Activity',
                             labels={'value': 'Number of Employees', 'month_name': 'Month'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Industry heatmap
        if not filtered_layoffs.empty and not filtered_hiring.empty:
            st.plotly_chart(create_industry_heatmap(filtered_layoffs, filtered_hiring), use_container_width=True)
    
    with tab3:
        st.markdown('<h2 class="sub-header">🏢 Company Analysis</h2>', unsafe_allow_html=True)
        
        # Company comparison
        if not filtered_fused.empty:
            st.plotly_chart(create_company_comparison_chart(filtered_fused, selected_companies), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not filtered_layoffs.empty:
                st.plotly_chart(create_top_companies_chart(filtered_layoffs, filtered_hiring, 'layoffs'), use_container_width=True)
        
        with col2:
            if not filtered_hiring.empty:
                st.plotly_chart(create_top_companies_chart(filtered_layoffs, filtered_hiring, 'hires'), use_container_width=True)
        
        # Company details table
        if not filtered_fused.empty:
            st.markdown("### Company Performance Summary")
            company_summary = filtered_fused.groupby('company').agg({
                'layoffs': 'sum',
                'hires': 'sum',
                'net_change': 'sum',
                'industry': 'first'
            }).reset_index()
            
            company_summary = company_summary.sort_values('net_change', ascending=False)
            st.dataframe(company_summary, use_container_width=True)
    
    with tab4:
        st.markdown('<h2 class="sub-header">🏭 Industry Insights</h2>', unsafe_allow_html=True)
        
        if not filtered_layoffs.empty and not filtered_hiring.empty:
            industry_trends = calculate_industry_trends(filtered_layoffs, filtered_hiring)
            
            # Industry performance chart
            fig = px.bar(industry_trends.groupby('industry').agg({
                'layoffs': 'sum',
                'hires': 'sum',
                'net_change': 'sum'
            }).reset_index(), 
            x='industry', y=['layoffs', 'hires'], 
            title='Industry Employment Activity',
            barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            # Industry trends over time
            fig2 = px.line(industry_trends, x='year', y='net_change', color='industry',
                          title='Industry Net Employment Change Over Time')
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab5:
        st.markdown('<h2 class="sub-header">🤖 AI-Powered Insights</h2>', unsafe_allow_html=True)
        
        # Generate insights
        insights = generate_ai_insights(filtered_layoffs, filtered_hiring, filtered_fused)
        predictions = predict_trends(filtered_fused)
        recommendations = generate_recommendations(insights, predictions)
        
        # Display insights
        st.markdown("### 🔍 Key Insights")
        for insight in insights:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔮 Predictive Analysis")
        for prediction in predictions:
            st.markdown(f'<div class="insight-box">{prediction}</div>', unsafe_allow_html=True)
        
        st.markdown("### 💡 Strategic Recommendations")
        for recommendation in recommendations:
            st.markdown(f'<div class="insight-box">{recommendation}</div>', unsafe_allow_html=True)
        
        # AI Analysis Summary
        st.markdown("### 📋 Analysis Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Market Health Indicators:**")
            if not filtered_fused.empty:
                recent_net = filtered_fused[filtered_fused['year'] == filtered_fused['year'].max()]['net_change'].sum()
                health_status = "🟢 Healthy" if recent_net > 0 else "🔴 Challenging" if recent_net < -1000 else "🟡 Stable"
                st.write(f"Current Market Status: {health_status}")
                st.write(f"Recent Net Change: {recent_net:+,} positions")
        
        with col2:
            st.markdown("**Volatility Assessment:**")
            if not filtered_layoffs.empty:
                layoff_volatility = filtered_layoffs.groupby('year')['layoffs'].sum().std()
                hiring_volatility = filtered_hiring.groupby('year')['hires'].sum().std()
                volatility_ratio = layoff_volatility / hiring_volatility if hiring_volatility > 0 else 0
                volatility_level = "High" if volatility_ratio > 1.2 else "Moderate" if volatility_ratio > 0.8 else "Low"
                st.write(f"Market Volatility: {volatility_level}")
                st.write(f"Volatility Ratio: {volatility_ratio:.2f}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 AI Powered Data Fusion and Visualization Dashboards</p>
        <p>Empowering data-driven decisions in the tech industry</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()