import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample tech layoffs and hiring data"""
    
    # Tech companies list
    companies = [
        'Meta', 'Google', 'Amazon', 'Microsoft', 'Apple', 'Netflix', 'Tesla',
        'Twitter', 'Uber', 'Airbnb', 'Spotify', 'Zoom', 'Salesforce', 'Adobe',
        'Intel', 'NVIDIA', 'PayPal', 'Square', 'Dropbox', 'Slack'
    ]
    
    # Industries
    industries = ['Social Media', 'Search/Cloud', 'E-commerce', 'Software', 'Hardware', 
                 'Streaming', 'Automotive', 'Transportation', 'Travel', 'Music',
                 'Video Conferencing', 'CRM', 'Design', 'Semiconductors', 'Fintech']
    
    # Locations
    locations = ['San Francisco', 'Seattle', 'New York', 'Austin', 'Boston', 
                'Los Angeles', 'Chicago', 'Denver', 'Atlanta', 'Remote']
    
    # Generate layoffs data (2020-2024)
    layoffs_data = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for _ in range(500):  # 500 layoff events
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        company = random.choice(companies)
        industry = random.choice(industries)
        location = random.choice(locations)
        
        # Higher layoffs in 2022-2023 (economic downturn)
        if date.year in [2022, 2023]:
            layoffs = random.randint(50, 2000)
        else:
            layoffs = random.randint(10, 500)
            
        layoffs_data.append({
            'date': date,
            'company': company,
            'layoffs': layoffs,
            'industry': industry,
            'location': location,
            'year': date.year,
            'month': date.month,
            'quarter': f"Q{(date.month-1)//3 + 1}"
        })
    
    # Generate hiring data
    hiring_data = []
    for _ in range(600):  # 600 hiring events
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        company = random.choice(companies)
        industry = random.choice(industries)
        location = random.choice(locations)
        
        # Higher hiring in 2020-2021 (pandemic boom)
        if date.year in [2020, 2021]:
            hires = random.randint(100, 3000)
        elif date.year in [2022, 2023]:
            hires = random.randint(20, 800)
        else:
            hires = random.randint(50, 1500)
            
        hiring_data.append({
            'date': date,
            'company': company,
            'hires': hires,
            'industry': industry,
            'location': location,
            'year': date.year,
            'month': date.month,
            'quarter': f"Q{(date.month-1)//3 + 1}"
        })
    
    layoffs_df = pd.DataFrame(layoffs_data)
    hiring_df = pd.DataFrame(hiring_data)
    
    return layoffs_df, hiring_df

def get_company_list(layoffs_df, hiring_df):
    """Get unique list of companies from both datasets"""
    all_companies = set(layoffs_df['company'].unique()) | set(hiring_df['company'].unique())
    return sorted(list(all_companies))

def get_date_range(layoffs_df, hiring_df):
    """Get the date range from both datasets"""
    min_date = min(layoffs_df['date'].min(), hiring_df['date'].min())
    max_date = max(layoffs_df['date'].max(), hiring_df['date'].max())
    return min_date, max_date