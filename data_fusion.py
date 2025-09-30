import pandas as pd
import numpy as np

def fuse_employment_data(layoffs_df, hiring_df):
    """Fuse layoffs and hiring data for comprehensive analysis"""
    
    # Aggregate layoffs by company and month
    layoffs_monthly = layoffs_df.groupby(['company', 'year', 'month']).agg({
        'layoffs': 'sum',
        'industry': 'first',
        'location': 'first'
    }).reset_index()
    
    # Aggregate hiring by company and month
    hiring_monthly = hiring_df.groupby(['company', 'year', 'month']).agg({
        'hires': 'sum',
        'industry': 'first',
        'location': 'first'
    }).reset_index()
    
    # Merge the datasets
    fused_df = pd.merge(
        layoffs_monthly, 
        hiring_monthly, 
        on=['company', 'year', 'month'], 
        how='outer',
        suffixes=('_layoffs', '_hiring')
    )
    
    # Fill missing values
    fused_df['layoffs'] = fused_df['layoffs'].fillna(0)
    fused_df['hires'] = fused_df['hires'].fillna(0)
    
    # Use industry and location from either dataset
    fused_df['industry'] = fused_df['industry_layoffs'].fillna(fused_df['industry_hiring'])
    fused_df['location'] = fused_df['location_layoffs'].fillna(fused_df['location_hiring'])
    
    # Calculate net employment change
    fused_df['net_change'] = fused_df['hires'] - fused_df['layoffs']
    fused_df['employment_ratio'] = fused_df['hires'] / (fused_df['layoffs'] + 1)  # +1 to avoid division by zero
    
    # Create date column
    fused_df['date'] = pd.to_datetime(fused_df[['year', 'month']].assign(day=1))
    
    # Clean up columns
    fused_df = fused_df.drop(['industry_layoffs', 'industry_hiring', 'location_layoffs', 'location_hiring'], axis=1)
    
    return fused_df

def calculate_industry_trends(layoffs_df, hiring_df):
    """Calculate trends by industry"""
    
    # Industry layoffs trends
    industry_layoffs = layoffs_df.groupby(['industry', 'year']).agg({
        'layoffs': 'sum'
    }).reset_index()
    
    # Industry hiring trends
    industry_hiring = hiring_df.groupby(['industry', 'year']).agg({
        'hires': 'sum'
    }).reset_index()
    
    # Merge industry data
    industry_trends = pd.merge(
        industry_layoffs, 
        industry_hiring, 
        on=['industry', 'year'], 
        how='outer'
    ).fillna(0)
    
    industry_trends['net_change'] = industry_trends['hires'] - industry_trends['layoffs']
    
    return industry_trends

def get_summary_statistics(layoffs_df, hiring_df, fused_df):
    """Calculate key summary statistics"""
    
    total_layoffs = layoffs_df['layoffs'].sum()
    total_hires = hiring_df['hires'].sum()
    net_employment_change = total_hires - total_layoffs
    
    # Most affected companies
    company_layoffs = layoffs_df.groupby('company')['layoffs'].sum().sort_values(ascending=False)
    company_hires = hiring_df.groupby('company')['hires'].sum().sort_values(ascending=False)
    
    # Monthly trends
    monthly_layoffs = layoffs_df.groupby(['year', 'month'])['layoffs'].sum()
    monthly_hires = hiring_df.groupby(['year', 'month'])['hires'].sum()
    
    # Industry impact
    industry_impact = layoffs_df.groupby('industry')['layoffs'].sum().sort_values(ascending=False)
    
    return {
        'total_layoffs': total_layoffs,
        'total_hires': total_hires,
        'net_employment_change': net_employment_change,
        'top_layoff_companies': company_layoffs.head(10),
        'top_hiring_companies': company_hires.head(10),
        'monthly_layoffs': monthly_layoffs,
        'monthly_hires': monthly_hires,
        'industry_impact': industry_impact
    }

def filter_data(df, companies=None, years=None, months=None, industries=None):
    """Filter dataframe based on selected criteria"""
    filtered_df = df.copy()
    
    if companies:
        filtered_df = filtered_df[filtered_df['company'].isin(companies)]
    
    if years:
        filtered_df = filtered_df[filtered_df['year'].isin(years)]
    
    if months:
        filtered_df = filtered_df[filtered_df['month'].isin(months)]
    
    if industries:
        filtered_df = filtered_df[filtered_df['industry'].isin(industries)]
    
    return filtered_df