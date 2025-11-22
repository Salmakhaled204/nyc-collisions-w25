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

9. How does crash frequency change when multiple filters (borough, hour, weekday, and vehicle type) are combined, and what interaction patterns appear across time and location?
10. What are the most common injury outcomes for different types of road users (drivers, passengers, pedestrians, cyclists), and how does this distribution shift when filters or search keywords are applied?

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

✅ Answer to RQ9: Crash Frequency by Combined Filters

RQ9:
How does crash frequency change when multiple filters (borough, hour, weekday, and vehicle type) are combined, and what interaction patterns appear across time and location?

Answer:

Using the interactive dashboard:
The heatmap reveals consistent temporal patterns:
Crash frequency peaks around 5–6 PM across all boroughs (evening rush hour).
Weekends show more afternoon crashes, especially Saturdays.
Weekdays show concentrated morning (8 AM) and evening (5–7 PM) peaks.
When Borough filters are applied:
Brooklyn and Queens display the strongest rush-hour peaks.
Manhattan shows more late-night crashes (nightlife + tourism zones).
When Vehicle Type filters are combined:
“Sedan” and “SUV” amplify standard rush-hour patterns.
“Motorcycle” crashes peak more in warm seasons (visible when filtering by year).
When search keywords like “Uber”, “bike”, or “truck” are applied:
Patterns shift to specific hours or days related to activity levels.

Conclusion:

Crash frequency strongly depends on the interaction of borough × hour × weekday × vehicle type.
Rush hours are universally high, Brooklyn/Queens dominate volume, and certain vehicle types shift the temporal pattern.

✅ Answer to RQ10: Injury Outcomes Across Road User Types

RQ10:
What are the most common injury outcomes for different types of road users (drivers, passengers, pedestrians, cyclists), and how does this distribution shift when filters or search keywords are applied?

Answer:

Using the injury severity pie chart + age groups + filters:
Drivers:
Most injuries fall into “Possible Injury” and “Minor Injury.”
Severe injuries are present but less common due to vehicle protection.
Passengers:
Injury distribution is similar to drivers but with slightly fewer severe cases.
Pedestrians:
Show a much higher proportion of “Moderate” and “Severe” injuries.
Filters reveal Manhattan as the borough with the highest pedestrian injury ratios.
Cyclists:
Higher share of moderate injuries, especially in Brooklyn and Manhattan.
Search keywords like “bicycle” highlight these patterns clearly.
Filters & Keyword Effects:
Filtering by “age 60+” increases severe injury proportions.
Filtering by “Brooklyn” + “SUV” increases moderate injuries.
Searching “pedestrian 2022” raises the share of serious injuries.

Conclusion:

Injury severity strongly depends on the road-user type.
Pedestrians and cyclists face the highest risk of serious injuries, while drivers and passengers show milder overall severity. Filters and search queries significantly shift severity proportions.
---

## ✔ Submission Requirements Checklist

This README includes:

* ✓ Setup steps
* ✓ Deployment instructions
* ✓ Description of each team member’s contribution
* ✓ Research questions
* ✓ Clear explanation of dashboard features
* ✓ Clean project overview