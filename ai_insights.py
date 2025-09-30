import pandas as pd
import numpy as np
from datetime import datetime
import random

def generate_ai_insights(layoffs_df, hiring_df, fused_df):
    """Generate AI-powered insights from the employment data"""
    
    insights = []
    
    # Trend Analysis
    yearly_layoffs = layoffs_df.groupby('year')['layoffs'].sum()
    yearly_hires = hiring_df.groupby('year')['hires'].sum()
    
    # Peak layoff year
    peak_layoff_year = yearly_layoffs.idxmax()
    peak_layoffs = yearly_layoffs.max()
    insights.append(f"🔍 **Peak Layoffs**: {peak_layoff_year} saw the highest layoffs with {peak_layoffs:,} jobs lost.")
    
    # Peak hiring year
    peak_hiring_year = yearly_hires.idxmax()
    peak_hires = yearly_hires.max()
    insights.append(f"📈 **Peak Hiring**: {peak_hiring_year} had the strongest hiring with {peak_hires:,} new positions.")
    
    # Industry Analysis
    industry_layoffs = layoffs_df.groupby('industry')['layoffs'].sum().sort_values(ascending=False)
    most_affected_industry = industry_layoffs.index[0]
    insights.append(f"🏭 **Most Affected Industry**: {most_affected_industry} experienced the highest layoffs ({industry_layoffs.iloc[0]:,} jobs).")
    
    # Company Analysis
    company_net_change = fused_df.groupby('company')['net_change'].sum().sort_values(ascending=False)
    top_net_hirer = company_net_change.index[0]
    top_net_change = company_net_change.iloc[0]
    insights.append(f"🏢 **Top Net Hirer**: {top_net_hirer} has the highest net employment growth (+{top_net_change:,} positions).")
    
    # Seasonal Patterns
    monthly_layoffs = layoffs_df.groupby('month')['layoffs'].sum()
    peak_layoff_month = monthly_layoffs.idxmax()
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    insights.append(f"📅 **Seasonal Pattern**: {month_names[peak_layoff_month]} typically sees the highest layoff activity.")
    
    # Recovery Indicators
    recent_year = max(yearly_hires.index)
    if recent_year in yearly_hires.index and recent_year in yearly_layoffs.index:
        recent_net = yearly_hires[recent_year] - yearly_layoffs[recent_year]
        if recent_net > 0:
            insights.append(f"🔄 **Recovery Signal**: {recent_year} shows positive net employment growth (+{recent_net:,} jobs).")
        else:
            insights.append(f"⚠️ **Continued Challenges**: {recent_year} still shows net job losses ({recent_net:,} jobs).")
    
    # Market Volatility
    layoff_volatility = yearly_layoffs.std()
    hiring_volatility = yearly_hires.std()
    if layoff_volatility > hiring_volatility:
        insights.append("📊 **Market Volatility**: Layoff patterns show higher volatility than hiring, indicating uncertain market conditions.")
    else:
        insights.append("📊 **Market Stability**: Hiring patterns are more volatile than layoffs, suggesting dynamic growth opportunities.")
    
    return insights

def predict_trends(fused_df):
    """Generate predictive insights based on historical data"""
    
    predictions = []
    
    # Calculate growth rates
    yearly_data = fused_df.groupby('year').agg({
        'layoffs': 'sum',
        'hires': 'sum',
        'net_change': 'sum'
    })
    
    if len(yearly_data) >= 2:
        # Calculate year-over-year changes
        yearly_data['layoff_growth'] = yearly_data['layoffs'].pct_change()
        yearly_data['hiring_growth'] = yearly_data['hires'].pct_change()
        
        latest_year = yearly_data.index[-1]
        latest_layoff_growth = yearly_data['layoff_growth'].iloc[-1]
        latest_hiring_growth = yearly_data['hiring_growth'].iloc[-1]
        
        # Trend predictions
        if latest_layoff_growth < -0.1:
            predictions.append("🔮 **Layoff Trend**: Decreasing layoff activity suggests market stabilization.")
        elif latest_layoff_growth > 0.1:
            predictions.append("🔮 **Layoff Trend**: Increasing layoffs may indicate economic headwinds ahead.")
        
        if latest_hiring_growth > 0.1:
            predictions.append("🔮 **Hiring Trend**: Strong hiring growth indicates expanding job market opportunities.")
        elif latest_hiring_growth < -0.1:
            predictions.append("🔮 **Hiring Trend**: Declining hiring activity suggests cautious market sentiment.")
    
    # Industry momentum
    recent_data = fused_df[fused_df['year'] >= fused_df['year'].max() - 1]
    industry_momentum = recent_data.groupby('industry')['net_change'].sum().sort_values(ascending=False)
    
    if len(industry_momentum) > 0:
        growing_industry = industry_momentum.index[0]
        predictions.append(f"🚀 **Industry Momentum**: {growing_industry} shows strongest recent employment growth.")
    
    return predictions

def generate_recommendations(insights, predictions):
    """Generate actionable recommendations based on insights"""
    
    recommendations = [
        "💡 **For Job Seekers**: Focus on industries showing positive net employment growth and consider companies with strong hiring patterns.",
        "💡 **For Employers**: Monitor seasonal hiring patterns and consider counter-cyclical recruitment strategies during low-activity periods.",
        "💡 **For Investors**: Track employment trends as leading indicators of company performance and market health.",
        "💡 **For Policymakers**: Consider targeted support for industries experiencing significant layoffs while fostering growth in expanding sectors."
    ]
    
    return recommendations