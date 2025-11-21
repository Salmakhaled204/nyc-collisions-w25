# NYC Motor Vehicle Collisions – Data Pipeline & Interactive Dashboard

Course: Data Engineering and Visualization – Winter 2025  
Team: [Replace with your team name / group number]  

This project analyzes NYC Motor Vehicle Collisions using two related datasets
(crashes + persons). The goal is to build a full pipeline from raw data to a
clean integrated dataset and a fully interactive dashboard for exploration and
reporting.

---

## 1. Repository Structure

Main contents of this repository:

- `notebook.ipynb`  
 Colab notebook containing:
  - Dataset overview (structure, size, columns, issues)
  - Exploratory Data Analysis (EDA)
  - Pre-integration cleaning
  - Integration (joining crashes + persons)
  - Post-integration cleaning
  - Supporting plots for understanding and validating the data

- `app.py`  
  Dash application providing the interactive web dashboard (filters, search,
  Generate Report button, and visualizations).

- `merged_final.csv`  
  Final cleaned and integrated dataset (crashes + persons joined on
  `collision_id`). Used as the data source for `app.py`.

- `requirements.txt`  
  Python dependencies required to run the dashboard.

- `README.md`  
  Project documentation (this file).

## 2. Data Description

The project uses the NYC Open Data Motor Vehicle Collisions datasets:

- **Crashes table** – one row per collision (location, date/time, borough,
  contributing factors, etc.).
- **Persons table** – one row per person involved (role, age, injury severity,
  etc.).

After cleaning and integration, the final dataset:

- Contains all valid crash–person pairs.
- Is joined on `collision_id`.
- Has standardized formats for:
  - Date/time
  - Borough names
  - Vehicle type categories
  - Injury and severity codes
- Contains derived fields such as:
  - `crash_year`
  - `crash_weekday`
  - `age_group` (e.g., `<18`, `18–30`, `31–45`, `46–60`, `60+`)

The full dataset is large (millions of rows), so some visualizations (e.g., the
map) may sample points for display, but **all statistics and aggregations are
computed from the full dataset.**

---

## 3. Notebook Contents (High-Level)

The shared notebook (`Project1-DataVis.ipynb`) is organized roughly as:

1. **Dataset Overview (Member 1)**
   - Loading both datasets
   - Column descriptions and types
   - Missing values overview
   - Initial value counts and simple plots
   - First list of data quality issues

2. **Deep EDA (Member 2)**
   - Crash patterns over time
   - Contributing factors analysis
   - Injuries & fatalities distributions
   - Vehicle type analysis
   - Demographic patterns (persons table)
   - Correlation heatmap, grouped charts, time-series, density plots

3. **Pre-Integration Cleaning (Member 3)**
   - Handling missing values
   - Outlier detection and treatment (IQR, domain rules)
   - Standardizing formats (dates, boroughs, vehicle categories)
   - Removing duplicates
   - Type conversions
   - Documentation of each cleaning decision

4. **Integration & Post-Cleaning (Member 4)**
   - Join strategy using `collision_id` (inner/left join justification)
   - Merging crashes + persons
   - Handling new missing values after merge
   - Resolving conflicting columns and redundant features
   - Validation plots (e.g., crashes vs person counts)
   - Saving final `merged_final.csv`

5. **Dashboard Summary (Member 5)**
   - Short description of the interactive dashboard
   - Explanation of filters, search mode, and visualizations
   - Link to `app.py` and deployment instructions (this README).

---

## 4. Interactive Dashboard (app.py)

The dashboard is implemented in `app.py` using **Dash** and **Plotly** with a
pastel, Pinterest-style visual theme.

### Features

- **Filters**
  - Borough
  - Year
  - Vehicle Type
  - Contributing Factor
  - Age Group

- **Search Mode**
  - Keyword-based search box (e.g. `Brooklyn 2022 pedestrian`)
  - Multi-word queries split into tokens
  - Search applied across:
    - Borough
    - Contributing factor
    - Vehicle type
    - Injury severity
    - Age group
    - Crash year

- **Generate Report Button**
  - Applies both dropdown filters and keyword search
  - Updates all charts and the KPI summary in one click

- **KPI Summary**
  - Number of distinct collisions
  - Number of person records
  - Average age of involved persons

- **Interactive Visualizations**
  1. **Bar chart** – crashes per borough  
  2. **Line chart** – crashes over time (by year)  
  3. **Heatmap** – crashes by hour of day × weekday  
  4. **Map** – crash locations (sampled points for performance)  
  5. **Pie chart** – injury severity distribution  

- **Styling**
  - Soft pastel background
  - Rounded cards with subtle shadows
  - Gradient “Generate Report” button
  - Unified pastel color palette for charts

---