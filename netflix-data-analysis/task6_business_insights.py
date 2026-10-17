
# ============================================================
# AUSPIFY INTERNSHIP - TASK 6 (ADVANCED)
# NETFLIX BUSINESS INSIGHTS REPORT
# ============================================================
# This project performs end-to-end exploratory data analysis,
# creates interactive visualizations, and produces a business
# insights report using the cleaned Netflix dataset.
# ============================================================

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

# ------------------------------------------------------------
# STEP 1: SET UP THE PROJECT
# ------------------------------------------------------------

OUTPUT_DIR = Path("task6_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

INPUT_FILE = Path("netflix_cleaned.csv")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "netflix_cleaned.csv was not found. "
        "Place this script in the project folder and run Task 1 first."
    )

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "show_id", "type", "title", "country",
    "release_year", "rating", "duration", "listed_in"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column '{column}' is missing from the dataset."
        )

# Keep the original cleaned data unchanged.
df = df.copy()

# Standardize fields used in the analysis.
for column in ["type", "country", "rating", "listed_in"]:
    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )

df["release_year"] = pd.to_numeric(
    df["release_year"], errors="coerce"
)

df.loc[df["type"].eq(""), "type"] = "Not Given"
df.loc[df["rating"].eq(""), "rating"] = "Not Given"
df.loc[df["country"].eq(""), "country"] = "Not Given"

total_rows = len(df)
unique_titles = df["show_id"].nunique()
duplicate_rows = int(df.duplicated().sum())
missing_cells = int(df.isna().sum().sum())

print("=" * 70)
print("AUSPIFY INTERNSHIP - TASK 6")
print("NETFLIX BUSINESS INSIGHTS REPORT")
print("=" * 70)

# ------------------------------------------------------------
# STEP 2: EXPLORATORY DATA ANALYSIS
# ------------------------------------------------------------

print("\n1. DATASET OVERVIEW")
print("-" * 50)
print(f"Dataset rows: {total_rows:,}")
print(f"Unique titles: {unique_titles:,}")
print(f"Exact duplicate rows: {duplicate_rows:,}")
print(f"Missing cells after preparation: {missing_cells:,}")
print(f"Dataset columns: {len(df.columns)}")

type_counts = (
    df.groupby("type")["show_id"]
    .nunique()
    .sort_values(ascending=False)
)

type_summary = type_counts.reset_index()
type_summary.columns = ["Content Type", "Number of Titles"]
type_summary["Percentage"] = (
    type_summary["Number of Titles"] / unique_titles * 100
).round(2)

print("\nCONTENT TYPE DISTRIBUTION")
print(type_summary.to_string(index=False))

rating_summary = (
    df.groupby("rating")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index()
)
rating_summary.columns = ["Rating", "Number of Titles"]
rating_summary["Percentage"] = (
    rating_summary["Number of Titles"] / unique_titles * 100
).round(2)

print("\nTOP 10 CONTENT RATINGS")
print(rating_summary.head(10).to_string(index=False))

# ------------------------------------------------------------
# STEP 3: RELEASE-YEAR TRENDS
# ------------------------------------------------------------

year_data = df.dropna(subset=["release_year"]).copy()
year_data["release_year"] = year_data["release_year"].astype(int)

year_summary = (
    year_data.groupby("release_year")["show_id"]
    .nunique()
    .reset_index(name="Number of Titles")
    .sort_values("release_year")
)

if year_summary.empty:
    raise ValueError("No valid release-year data is available.")

peak_year_row = year_summary.loc[
    year_summary["Number of Titles"].idxmax()
]

earliest_year = int(year_summary["release_year"].min())
latest_year = int(year_summary["release_year"].max())
peak_year = int(peak_year_row["release_year"])
peak_year_count = int(peak_year_row["Number of Titles"])

# ------------------------------------------------------------
# STEP 4: COUNTRY ANALYSIS
# ------------------------------------------------------------

country_data = df[["show_id", "country"]].copy()

country_data["Country"] = country_data["country"].str.split(",")
country_data = country_data.explode("Country")
country_data["Country"] = country_data["Country"].str.strip()

country_data = country_data[
    country_data["Country"].ne("")
    & country_data["Country"].ne("Not Given")
]

country_data = country_data.drop_duplicates(
    subset=["show_id", "Country"]
)

country_summary = (
    country_data.groupby("Country")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="Number of Titles")
)

top_countries = country_summary.head(10).copy()

titles_without_country = int(
    df["country"].eq("Not Given").sum()
)

# Country totals are title-country associations. A title linked
# to multiple countries is counted once for each associated country.

# ------------------------------------------------------------
# STEP 5: GENRE ANALYSIS
# ------------------------------------------------------------

genre_data = df[["show_id", "listed_in"]].copy()
genre_data["Genre"] = genre_data["listed_in"].str.split(",")
genre_data = genre_data.explode("Genre")
genre_data["Genre"] = genre_data["Genre"].str.strip()

genre_data = genre_data[
    genre_data["Genre"].ne("")
].drop_duplicates(
    subset=["show_id", "Genre"]
)

genre_summary = (
    genre_data.groupby("Genre")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="Number of Titles")
)

top_genres = genre_summary.head(10).copy()

# ------------------------------------------------------------
# STEP 6: CONTENT RATING BY TYPE
# ------------------------------------------------------------

rating_type_summary = (
    df.groupby(["rating", "type"])["show_id"]
    .nunique()
    .reset_index(name="Number of Titles")
)

rating_type_summary.columns = [
    "Rating", "Content Type", "Number of Titles"
]

type_totals = df.groupby("type")["show_id"].nunique().to_dict()

rating_type_summary["Type Total"] = (
    rating_type_summary["Content Type"].map(type_totals)
)

rating_type_summary["Percentage within Type"] = (
    rating_type_summary["Number of Titles"]
    / rating_type_summary["Type Total"]
    * 100
).round(2)

# ------------------------------------------------------------
# STEP 7: CREATE INTERACTIVE CHARTS
# ------------------------------------------------------------

# Chart 1: Movie and TV Show distribution
fig_type = px.bar(
    type_summary,
    x="Content Type",
    y="Number of Titles",
    color="Content Type",
    text="Number of Titles",
    title="Netflix Content Distribution",
    hover_data={"Percentage": ":.2f"}
)

fig_type.update_layout(
    showlegend=False,
    template="plotly_white"
)

fig_type.write_html(
    OUTPUT_DIR / "content_distribution.html"
)

# Chart 2: Top 10 countries
fig_country = px.bar(
    top_countries.sort_values(
        "Number of Titles", ascending=True
    ),
    x="Number of Titles",
    y="Country",
    orientation="h",
    text="Number of Titles",
    title="Top 10 Countries by Netflix Title Associations",
    template="plotly_white"
)

fig_country.write_html(
    OUTPUT_DIR / "top_countries.html"
)

# Chart 3: Top 10 genres
fig_genre = px.bar(
    top_genres.sort_values(
        "Number of Titles", ascending=True
    ),
    x="Number of Titles",
    y="Genre",
    orientation="h",
    text="Number of Titles",
    title="Top 10 Netflix Genres",
    template="plotly_white"
)

fig_genre.write_html(
    OUTPUT_DIR / "top_genres.html"
)

# Chart 4: Release-year trend
fig_year = px.line(
    year_summary,
    x="release_year",
    y="Number of Titles",
    markers=True,
    title="Netflix Titles by Release Year",
    labels={
        "release_year": "Release Year",
        "Number of Titles": "Number of Titles"
    },
    template="plotly_white"
)

fig_year.write_html(
    OUTPUT_DIR / "release_year_trend.html"
)

# Chart 5: Rating by content type
fig_rating = px.bar(
    rating_type_summary,
    x="Rating",
    y="Number of Titles",
    color="Content Type",
    barmode="stack",
    title="Content Ratings: Movies vs TV Shows",
    template="plotly_white"
)

fig_rating.write_html(
    OUTPUT_DIR / "ratings_by_type.html"
)

# ------------------------------------------------------------
# STEP 8: BUILD A COMBINED INTERACTIVE DASHBOARD
# ------------------------------------------------------------

dashboard = make_subplots(
    rows=3,
    cols=2,
    subplot_titles=(
        "Content Type Distribution",
        "Top 10 Countries",
        "Top 10 Genres",
        "Release-Year Trend",
        "Ratings by Content Type",
        "Top Content Ratings"
    ),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "scatter"}],
        [{"type": "bar"}, {"type": "bar"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.13
)

# Content type chart
for _, row in type_summary.iterrows():
    dashboard.add_trace(
        go.Bar(
            x=[row["Content Type"]],
            y=[row["Number of Titles"]],
            name=row["Content Type"],
            showlegend=False,
            hovertemplate=(
                "%{x}<br>Titles: %{y:,}<extra></extra>"
            )
        ),
        row=1, col=1
    )

# Country chart
dashboard.add_trace(
    go.Bar(
        x=top_countries["Number of Titles"],
        y=top_countries["Country"],
        orientation="h",
        name="Countries",
        showlegend=False,
        hovertemplate=(
            "%{y}<br>Titles: %{x:,}<extra></extra>"
        )
    ),
    row=1, col=2
)

# Genre chart
dashboard.add_trace(
    go.Bar(
        x=top_genres["Number of Titles"],
        y=top_genres["Genre"],
        orientation="h",
        name="Genres",
        showlegend=False,
        hovertemplate=(
            "%{y}<br>Titles: %{x:,}<extra></extra>"
        )
    ),
    row=2, col=1
)

# Release-year chart
dashboard.add_trace(
    go.Scatter(
        x=year_summary["release_year"],
        y=year_summary["Number of Titles"],
        mode="lines+markers",
        name="Release year",
        showlegend=False,
        hovertemplate=(
            "Year: %{x}<br>Titles: %{y:,}<extra></extra>"
        )
    ),
    row=2, col=2
)

# Ratings by content type
for content_type in rating_type_summary["Content Type"].unique():
    type_subset = rating_type_summary[
        rating_type_summary["Content Type"] == content_type
    ]

    dashboard.add_trace(
        go.Bar(
            x=type_subset["Rating"],
            y=type_subset["Number of Titles"],
            name=content_type,
            legendgroup=content_type,
            showlegend=True,
            hovertemplate=(
                "Rating: %{x}<br>Titles: %{y:,}<extra></extra>"
            )
        ),
        row=3, col=1
    )

# Top ratings chart
top_ratings = rating_summary.head(10).sort_values(
    "Number of Titles", ascending=True
)

dashboard.add_trace(
    go.Bar(
        x=top_ratings["Number of Titles"],
        y=top_ratings["Rating"],
        orientation="h",
        name="Ratings",
        showlegend=False,
        hovertemplate=(
            "%{y}<br>Titles: %{x:,}<extra></extra>"
        )
    ),
    row=3, col=2
)

dashboard.update_layout(
    title={
        "text": "NETFLIX BUSINESS INTELLIGENCE DASHBOARD",
        "x": 0.5
    },
    template="plotly_white",
    height=1450,
    barmode="stack",
    legend_title_text="Content Type"
)

dashboard.update_xaxes(title_text="Content Type", row=1, col=1)
dashboard.update_yaxes(title_text="Titles", row=1, col=1)
dashboard.update_xaxes(title_text="Titles", row=1, col=2)
dashboard.update_xaxes(title_text="Titles", row=2, col=1)
dashboard.update_xaxes(title_text="Release Year", row=2, col=2)
dashboard.update_xaxes(title_text="Rating", row=3, col=1)
dashboard.update_xaxes(title_text="Titles", row=3, col=2)

dashboard.write_html(
    OUTPUT_DIR / "netflix_business_dashboard.html"
)

# ------------------------------------------------------------
# STEP 9: GENERATE BUSINESS INSIGHTS
# ------------------------------------------------------------

most_common_type = type_summary.iloc[0]
most_common_rating = rating_summary.iloc[0]
most_common_genre = genre_summary.iloc[0]
most_common_country = country_summary.iloc[0]

movie_count = int(
    df.loc[df["type"] == "Movie", "show_id"].nunique()
)
tv_count = int(
    df.loc[df["type"] == "TV Show", "show_id"].nunique()
)

movie_percentage = (
    movie_count / unique_titles * 100
    if unique_titles else 0
)
tv_percentage = (
    tv_count / unique_titles * 100
    if unique_titles else 0
)

insights = [
    "NETFLIX BUSINESS INSIGHTS REPORT",
    "=" * 65,
    "",
    "1. EXECUTIVE SUMMARY",
    (
        f"The dataset contains {unique_titles:,} unique titles. "
        f"Movies represent {movie_percentage:.2f}% and TV Shows "
        f"represent {tv_percentage:.2f}% of the titles."
    ),
    (
        f"The most frequent recorded rating is "
        f"{most_common_rating['Rating']} "
        f"({int(most_common_rating['Number of Titles']):,} titles)."
    ),
    (
        f"The most frequent genre is {most_common_genre['Genre']} "
        f"({int(most_common_genre['Number of Titles']):,} titles)."
    ),
    "",
    "2. KEY FINDINGS",
    (
        f"Content type: {most_common_type['Content Type']} is the "
        f"largest content type in the dataset."
    ),
    (
        f"Country: {most_common_country['Country']} ranks first by "
        f"title-country associations "
        f"({int(most_common_country['Number of Titles']):,})."
    ),
    (
        f"Genre: {most_common_genre['Genre']} ranks first by "
        f"genre-title associations."
    ),
    (
        f"Release years: the earliest recorded year is {earliest_year}, "
        f"and the latest recorded year is {latest_year}."
    ),
    (
        f"The year with the largest number of titles in this dataset "
        f"is {peak_year}, with {peak_year_count:,} titles."
    ),
    (
        f"Titles without country information: {titles_without_country:,}."
    ),
    "",
    "3. BUSINESS RECOMMENDATIONS",
    (
        "Catalog planning: review the current balance between Movies "
        "and TV Shows alongside business goals and customer demand."
    ),
    (
        "Content localization: investigate country-level catalog "
        "coverage and regional viewing data before prioritizing "
        "new local productions or licensing."
    ),
    (
        "Genre strategy: compare leading genres with viewing hours, "
        "completion rates, subscriber retention, and production costs "
        "before making investment decisions."
    ),
    (
        "Audience suitability: use content ratings to improve catalog "
        "filtering and age-appropriate discovery, while following "
        "the applicable rating definitions."
    ),
    (
        "Data quality: maintain consistent country, rating, and genre "
        "values and monitor records without country information."
    ),
    "",
    "4. IMPORTANT LIMITATIONS",
    (
        "This dataset describes titles and their metadata, not actual "
        "views, revenue, profit, subscriber preferences, or engagement."
    ),
    (
        "Country counts are title-country associations. A title "
        "associated with multiple countries contributes to each one."
    ),
    (
        "Genre counts are title-genre associations. A title may "
        "belong to multiple genres."
    ),
    (
        "The latest release year in this dataset is not necessarily "
        "the current year. Do not interpret the dataset as a complete "
        "or live Netflix catalog."
    ),
    (
        "Business recommendations are hypotheses to investigate. "
        "They should be validated using viewing, revenue, cost, and "
        "subscriber data before operational decisions are made."
    ),
    "",
    "5. OUTPUT FILES",
    "netflix_business_dashboard.html",
    "content_distribution.html",
    "top_countries.html",
    "top_genres.html",
    "release_year_trend.html",
    "ratings_by_type.html",
    "content_type_summary.csv",
    "rating_summary.csv",
    "country_summary.csv",
    "genre_summary.csv",
    "release_year_summary.csv",
    "rating_type_summary.csv",
    "business_insights_report.txt"
]

report_path = OUTPUT_DIR / "business_insights_report.txt"

with open(report_path, "w", encoding="utf-8") as report:
    report.write("\n".join(insights))

# ------------------------------------------------------------
# STEP 10: EXPORT ANALYTICAL TABLES
# ------------------------------------------------------------

type_summary.to_csv(
    OUTPUT_DIR / "content_type_summary.csv",
    index=False
)

rating_summary.to_csv(
    OUTPUT_DIR / "rating_summary.csv",
    index=False
)

country_summary.to_csv(
    OUTPUT_DIR / "country_summary.csv",
    index=False
)

genre_summary.to_csv(
    OUTPUT_DIR / "genre_summary.csv",
    index=False
)

year_summary.to_csv(
    OUTPUT_DIR / "release_year_summary.csv",
    index=False
)

rating_type_summary.to_csv(
    OUTPUT_DIR / "rating_type_summary.csv",
    index=False
)

# ------------------------------------------------------------
# STEP 11: DISPLAY RESULTS
# ------------------------------------------------------------

print("\n2. TOP BUSINESS INSIGHTS")
print("-" * 50)
print(
    f"Most common content type: {most_common_type['Content Type']}"
)
print(
    f"Most common rating: {most_common_rating['Rating']}"
)
print(
    f"Most common genre: {most_common_genre['Genre']}"
)
print(
    f"Top country: {most_common_country['Country']}"
)
print(f"Peak release year: {peak_year} ({peak_year_count:,} titles)")

print("\n3. EXPORTED FILES")
print("-" * 50)

for output_file in sorted(OUTPUT_DIR.iterdir()):
    print(output_file)

print("\nSUCCESS: Task 6 business insights report completed.")
print(f"Open the dashboard: {OUTPUT_DIR / 'netflix_business_dashboard.html'}")
