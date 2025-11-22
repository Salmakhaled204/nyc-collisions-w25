# 📘 *NYC Motor Vehicle Collisions – Data Engineering & Interactive Dashboard*

*GIU – Data Engineering & Visualization – Winter 2025*
*Milestone 1 – Full Submission README*

---

## 🧩 *Project Overview*

This project analyzes the *NYC Motor Vehicle Collision* dataset (2012–2025) and integrates the *Persons* dataset using COLLISION_ID.
We perform:

* Dataset loading
* EDA (light + advanced)
* Pre-integration cleaning
* Dataset merging
* Post-integration cleaning
* Interactive dashboard development (Dash/Plotly)
* Deployment on a hosting platform

The final interactive dashboard allows users to explore collisions by borough, year, vehicle type, injury severity, age group, contributing factor, and keyword-based search mode.

---

## 📁 *Datasets Used*

1. *Motor Vehicle Collisions – Crashes*
   Source: NYC Open Data
2. *Motor Vehicle Collisions – Persons*
   Source: NYC Open Data

Merged using:
COLLISION_ID

---

## 📌 *How to Run the Project Locally*

### *1) Clone Repository*

bash
git clone <your-repo-link>
cd <project-folder>


### *2) Install Dependencies*

bash
pip install -r requirements.txt


### *3) Run Dashboard*

bash
python app.py


This starts the dashboard at:
*[http://127.0.0.1:8050](http://127.0.0.1:8050)*

---

## 🚀 *Deployment Instructions*

The dashboard is already deployed on *Hugging Face Spaces*.

To deploy from scratch:

1. Create a Hugging Face account
2. Create a new *Space → SDK: Python → Runtime: CPU Basic*
3. Upload:

   * app.py
   * requirements.txt
   * merged_final.parquet
4. Push via Git or drag-and-drop
5. Hugging Face autodeploys the dashboard
6. Make sure the Space is *Public* under Settings

### ✔ Final Deployment (Live Dashboard)

👉 **[https://huggingface.co/spaces/salmazakiii/nyc-collisions-dashboard0](https://huggingface.co/spaces/salmazakiii/nyc-collisions-dashboard0)**

---

## 🎯 *Research Questions*

As required (8 for a 4-member team, 10 for a 5-member team), we prepared *10 research questions*. These guided all EDA, cleaning, and dashboard design.

### *Member 1*

🔷 Research Question 1 — Borough Crash Distribution

Which NYC borough has the highest frequency of motor vehicle crashes, and how has this pattern changed over the years (2012–2025)?

Why this fits:
You already explored borough counts and crash counts by year, so this question comes directly from your EDA foundation.

🔷 Research Question 2 — Injury Severity by Person Type

How is injury severity (Injured, Killed, Unspecified) distributed across different person types (Occupants, Pedestrians, Bicyclists), and which group shows the highest risk?

Why this fits:
You analyzed PERSON_TYPE and PERSON_INJURY in your uniques, counts, and plots. This is a perfect extension.

### *Member 2*

3. How do crash patterns vary across different time periods (hourly, daily, monthly), and which time windows show the highest risk?
4. Which contributing factors are most strongly associated with severe outcomes (injuries and fatalities), and how do these vary across boroughs?

### Member 3

5. How do missing values, inconsistent formats, and invalid entries in the raw NYC crashes and persons datasets affect data quality, and what cleaning strategies are most effective in producing a reliable standardized dataset?
6. How does demographic cleaning—including age imputation, sex standardization, and injury-category normalization—improve the accuracy and reliability of downstream analysis and visualizations?

### Member 4

7. How does integrating the cleaned crashes dataset with the cleaned persons dataset (using collision_id) improve the ability to analyze person-level involvement such as injury severity, age patterns, and time-of-day crash risk?  
8. What insights emerge from the unified merged dataset regarding the relationship between demographic factors (age, sex, person type) and crash characteristics (borough, contributing factor, crash hour)?

### *Member 5*

9. How do crash patterns across hours and weekdays change when focusing on specific boroughs and vehicle types, and what time–day combinations show the highest crash density under each scenario?
10. How does the distribution of injury severity differ between pedestrians, cyclists, and vehicle occupants when applying different keywords and borough filters?

---

# 👥 *Team Members & Contributions*

### ⭐ *Member 1 — Data Loading, Initial Exploration & Early Observations*

*1. Data Acquisition*
Loaded Crashes and Persons datasets directly via NYC API → pandas.read_csv().

*2. Missing Values Analysis*
Computed missing percentages; identified issues in pedestrian fields, boroughs, age, sex.

*3. Variable Summaries*
Analyzed PERSON_AGE, PERSON_SEX, PERSON_TYPE, borough distribution, factors, vehicle codes.

*4. Basic Visual Checks*
Created early plots:

* Age histograms
* Borough counts
* Injuries distribution
* Yearly crash count

*5. Early Issues Identified*
Documented:

* Missing boroughs
* Invalid ages (0, >120)
* Unknown sex codes
* High missingness in several fields

*6. Research Questions*
Defined three foundational RQs that shaped deeper analysis.

*7. Handover to Member 2*
Delivered raw datasets, missing value report, initial plots, variables summary.

---

### ⭐ *Member 2 — Deep EDA + Statistical Exploration*

* Performed detailed EDA on time trends, injury distributions, vehicle patterns
* Built advanced charts (correlation heatmap, KDE plots, grouped bars)
* Investigated relationships between injury severity and demographic variables
* Explored contributing factors over time
* Summarized insights for Member 1 research questions
* Provided cleaned intermediate EDA-ready tables

---

### ⭐ *Member 3 — Pre-Integration Cleaning & Standardization*

* Cleaned both datasets individually
* Handled missing values using drop/impute strategies
* Standardized:

  * Datetime formats
  * Borough names
  * Vehicle categories
  * Injury labels
* Removed duplicates
* Applied outlier detection using:

  * IQR
  * Domain logic
* Documented each cleaning step extensively in Markdown

---

### ⭐ *Member 4 — Integration + Post-Merge Cleaning*

* Performed join (LEFT JOIN) on COLLISION_ID
* Fixed duplicated keys and mismatched data types
* Cleaned new missing values created after merging
* Removed redundant columns from both tables
* Created validation plots:

  * Crash counts vs person counts
  * Null value comparison pre- vs post-merge
* Delivered final integrated dataset (CSV & Parquet)

---

### ⭐ *Member 5 — Dashboard Development, Interactivity & Deployment (Your Part)*

* Developed full *Plotly Dash dashboard* with Bootstrap layout
* Implemented filters:

  * Borough
  * Year
  * Vehicle Type
  * Contributing Factor
  * Age Group
* Added *keyword search mode*: automatically searches across dataset columns
* Built central *Generate Report* button
* Created 6+ interactive charts:

  * Borough bar chart
  * Yearly line chart
  * Hour vs weekday heatmap
  * Crash location map (Mapbox)
  * Injury severity pie chart
  * KPI summary card
* Loaded final dataset using a *local Parquet file* for guaranteed reliability
* Deployed complete dashboard to Hugging Face Spaces
* Wrote final README
* Answered Member 5’s research questions directly through dashboard logic

---

## 🧠 *Answers to Member 5 Research Questions*

✅ Answer to RQ9: 
RQ9:

How do crash patterns across hours and weekdays change when focusing on specific boroughs and vehicle types, and what time–day combinations show the highest crash density under each scenario?

Answer:
Filtering the dataset by borough and vehicle type revealed consistent temporal patterns. In all tested scenarios (“Brooklyn SUV”, “Manhattan Taxi”, and “Queens Motorcycle”), crashes peaked between 12 PM and 7 PM, especially on Monday, Thursday, and Friday. The heatmaps showed strong afternoon and early-evening clusters regardless of borough or vehicle type. The map visualizations also confirmed location-specific clustering: Brooklyn displayed widespread activity, Manhattan showed dense linear patterns along major avenues, and Queens had a broad distribution of motorcycle-related crashes. KPI results further showed that filtered crash counts vary by borough, with Brooklyn returning the highest counts. These findings demonstrate that crash density is influenced by both time-of-day and borough-specific traffic patterns.


✅ Answer to RQ10: 

RQ10:
How does the distribution of injury severity differ between pedestrians, cyclists, and vehicle occupants when applying different keywords and borough filters?


Answer:
Filtering the dataset by road-user type revealed clear differences in injury severity. Pedestrians showed a notable proportion of confirmed injuries (41%) and a small fatality share. Cyclist-related crashes, although fewer in number, displayed the highest injury percentage (67%), highlighting their vulnerability. Drivers experienced the lowest confirmed injury rate, with most records marked as “unknown,” suggesting milder outcomes or incomplete reporting. Elderly pedestrians (60+) had the most severe outcomes: nearly 70% injured and the highest fatality percentage (3.6%). These results indicate that injury severity is strongly influenced by both road-user type and age, with vulnerable groups—especially cyclists and older pedestrians—experiencing the worst outcomes.

## ✔ Submission Requirements Checklist

This README includes:

* ✓ Setup steps
* ✓ Deployment instructions
* ✓ Description of each team member’s contribution
* ✓ Research questions
* ✓ Clear explanation of dashboard features
* ✓ Clean project overview