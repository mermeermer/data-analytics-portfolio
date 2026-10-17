# Netflix Data Analysis | Auspify Technologies Internship

A Python-based data analysis project completed as part of the Data Analysis Using Python Internship at Auspify Technologies.

## Project Overview

This project analyzes a Netflix titles dataset using Python, pandas, Matplotlib, and Plotly. It covers data cleaning, content distribution, country-wise analysis, release-year trends, content ratings, genre analysis, and business insights.

## Tasks Completed

### Task 1 — Data Cleaning and Preparation
- Standardized text and content type labels.
- Converted date fields to the appropriate format.
- Checked for missing values and duplicate rows.
- Exported the cleaned dataset as `netflix_cleaned.csv`.

### Task 2 — Content Type Analysis
- Compared Movies and TV Shows.
- Calculated counts and percentages.
- Created bar and pie charts.
- Exported summary data and a report.

### Task 3 — Country-Wise Analysis
- Analyzed country-title associations.
- Identified the top 10 countries.
- Exported a country summary and chart.

### Task 4 — Release-Year Trend Analysis
- Counted titles by release year.
- Examined year-over-year changes.
- Created a release-year trend chart and report.

### Task 5 — Content Rating and Genre Analysis
- Analyzed content rating categories.
- Identified common genres.
- Compared ratings across Movies and TV Shows.
- Created interactive Plotly visualizations.

### Task 6 — Business Insights Dashboard
- Combined findings from content type, country, genre, rating, and release-year analysis.
- Created an interactive dashboard containing six charts.
- Prepared a report of key findings and limitations.

## Key Findings

| Metric | Finding |
|---|---:|
| Total titles analyzed | 8,790 |
| Movies | 6,126 (69.69%) |
| TV Shows | 2,664 (30.31%) |
| Most common recorded rating | TV-MA |
| Titles with TV-MA rating | 3,205 |
| Most common genre | International Movies |
| United States title associations | 3,240 |
| Highest-count release year | 2018 |
| Titles released in 2018 | 1,146 |

Country and genre counts represent associations. A title associated with multiple countries or genres may be counted in more than one category.

## Technology Stack

- Python
- pandas
- Matplotlib
- Plotly
- CSV and HTML
- Visual Studio Code

## How to Run

Install the required libraries:

```bash
python -m pip install pandas matplotlib plotly
```

Place the source dataset named `Dataset.csv` in the project directory, then run the scripts in order:

```bash
python task1_data_cleaning.py
python task2_content_analysis.py
python task3_country_analysis.py
python task4_trend_analysis.py
python task5_rating_genre_analysis.py
python task6_business_insights.py
```

Task 1 generates `netflix_cleaned.csv`, which is used by the later tasks.

## Interactive Dashboard

After running Task 6, open the following file in a web browser:

`task6_outputs/netflix_business_dashboard.html`

Individual interactive charts and CSV reports are saved in the task output folders.

## Data and Limitations

- The analysis uses a supplied dataset snapshot and is not a live connection to Netflix.
- The cleaned dataset contains 8,790 rows and 10 columns.
- Release years in the dataset range from 1925 to 2021.
- The latest release years may be incomplete.
- This dataset does not establish audience preferences, viewing hours, revenue, profitability, or subscriber engagement.
- Business recommendations require additional evidence before operational decisions are made.

## Acknowledgment

Completed as part of the Data Analysis Using Python Internship at Auspify Technologies.
