# AI Powered Dashboards — Tech Layoffs vs Hiring Trends (2022 to Present)
**THIS IS MOT A FINISHED PROJECT THIS MAY CHANGE IN FUTURE**
This project builds interactive dashboards to visualize and analyze trends in **tech industry layoffs vs. hiring** over the past few years. By fusing multiple data sources, we draw insights into market health, recovery, and sector-specific dynamics.

---

## 📊 Project Goal & Motivation

- Track how hiring and layoffs in the tech sector have evolved from 2022 onward  
- Enable stakeholders (job seekers, analysts, companies) to see patterns, downturns, and recoveries  
- Use AI / data analysis to highlight anomalies, ratios, growth rates, and predictive signals  

---

## 🛠 Tech Stack

- **Language**: Python  
- **Dashboard / Web Framework**: (e.g. Streamlit / Dash / Flask) — *(replace with your actual framework)*  
- **Libraries**: pandas, NumPy, matplotlib / plotly / seaborn, scikit-learn (if used for modeling or insight extraction)  
- **Project Modules** (example names—replace with yours):  
  - `app.py` — runs the dashboard  
  - `data_fusion.py` — merges and processes datasets  
  - `insights.py` — computes derived metrics, anomalies, ratios  
  - `requirements.txt` — dependency list  

---

## 🧭 Methodology & Workflow

1. **Data Collection & Fusion**  
   - Gather datasets (e.g. tech job postings, layoff announcements, market reports)  
   - Clean, standardize, and merge into unified datasets  

2. **Exploratory Data Analysis (EDA)**  
   - Compute aggregate statistics: total hires, total layoffs, year-over-year shifts  
   - Plot timelines, correlations, heatmaps  

3. **Insight / AI Layer**  
   - Compute ratios like layoffs : hiring, growth rates  
   - Detect spikes or anomalies in layoffs/hiring  
   - Optionally, simple forecasting or trend projection  

4. **Dashboard Construction**  
   - Build interactive visuals: line charts, bar charts, filters by year / domain / geography  
   - Arrange into views: overview, comparison, trends  

5. **Interpretation & Insights**  
   - Narrative around what the trends mean: which years were hardest, which sectors recovered faster, etc.  
   - Suggest possible future movements or caution signals  

---

## 📈 Sample Findings 
<img width="1905" height="855" alt="image" src="https://github.com/user-attachments/assets/e4a53d52-6a73-422b-aae0-aa389bd41767" />

<img width="1883" height="860" alt="image" src="https://github.com/user-attachments/assets/dd22889f-efff-4088-991d-65cda005183f" />
<img width="1896" height="862" alt="image" src="https://github.com/user-attachments/assets/bd5b441a-4481-4bec-9580-44e3a4d0ba88" />


**NOTE:the companys taken for the following data is AMAZON,AIRBNB,DROPBOX,APPLE,ADOBE.**


---

## 🚀 How to Run

```bash
git clone https://github.com/udayram05/AI_powered_Dashboards.git
cd AI_powered_Dashboards
pip install -r requirements.txt
python app.py
