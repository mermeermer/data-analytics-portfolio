
# ============================================================
# AUSPIFY INTERNSHIP - TASK 5
# NETFLIX CONTENT RATING AND GENRE ANALYSIS
# ============================================================

import pandas as pd
import plotly.express as px
from pathlib import Path

# STEP 1: Create the output folder
output_dir = Path("task5_outputs")
output_dir.mkdir(exist_ok=True)

# STEP 2: Load the cleaned dataset
input_file = Path("netflix_cleaned.csv")

if not input_file.exists():
    raise FileNotFoundError(
        "netflix_cleaned.csv was not found. Please run Task 1 first."
    )

df = pd.read_csv(input_file)

print("=" * 65)
print("NETFLIX CONTENT RATING AND GENRE ANALYSIS")
print("=" * 65)

# STEP 3: Validate the required columns
required_columns = ["show_id", "type", "rating", "listed_in", "title"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column '{column}' was not found."
        )

if df["show_id"].isna().any():
    raise ValueError("Missing show IDs were found.")

# STEP 4: Prepare the analysis columns
df["type"] = df["type"].fillna("Not Given").astype(str).str.strip()
df["rating"] = df["rating"].fillna("Not Given").astype(str).str.strip()
df["listed_in"] = df["listed_in"].fillna("").astype(str).str.strip()

# Treat empty rating values as unavailable
df.loc[df["rating"].eq(""), "rating"] = "Not Given"

total_titles = df["show_id"].nunique()

print("\n1. DATASET OVERVIEW")
print(f"Total titles: {total_titles:,}")
print(f"Movies: {(df['type'] == 'Movie').sum():,}")
print(f"TV Shows: {(df['type'] == 'TV Show').sum():,}")

# STEP 5: Analyze content ratings
rating_counts = (
    df.groupby("rating")["show_id"]
    .nunique()
    .sort_values(ascending=False)
)

rating_summary = rating_counts.reset_index()
rating_summary.columns = ["Rating", "Number of Titles"]

rating_summary["Percentage"] = (
    rating_summary["Number of Titles"] / total_titles * 100
).round(2)

print("\n2. CONTENT RATING DISTRIBUTION")
print(rating_summary.to_string(index=False))

# Interactive chart 1: rating distribution
rating_chart = px.bar(
    rating_summary.sort_values(
        "Number of Titles", ascending=False
    ),
    x="Rating",
    y="Number of Titles",
    color="Rating",
    title="Netflix Titles by Content Rating",
    hover_data={"Percentage": ":.2f"},
    labels={
        "Rating": "Content Rating",
        "Number of Titles": "Number of Titles"
    }
)

rating_chart.update_layout(
    showlegend=False,
    xaxis_title="Content Rating",
    yaxis_title="Number of Titles"
)

rating_chart.write_html(
    output_dir / "rating_distribution.html"
)

# STEP 6: Analyze genres
# Each title can have multiple genres, so split and count
# each title once for every genre listed.
genre_df = df[["show_id", "listed_in"]].copy()

genre_df["Genre"] = genre_df["listed_in"].str.split(",")

genre_df = genre_df.explode("Genre")
genre_df["Genre"] = genre_df["Genre"].str.strip()

genre_df = genre_df[
    genre_df["Genre"].ne("")
].drop_duplicates(
    subset=["show_id", "Genre"]
)

genre_counts = (
    genre_df.groupby("Genre")["show_id"]
    .nunique()
    .sort_values(ascending=False)
)

genre_summary = genre_counts.reset_index()
genre_summary.columns = ["Genre", "Number of Titles"]

print("\n3. TOP 15 GENRES")
print(genre_summary.head(15).to_string(index=False))

top_genres = genre_summary.head(15).copy()

# Interactive chart 2: top genres
genre_chart = px.bar(
    top_genres.sort_values(
        "Number of Titles", ascending=True
    ),
    x="Number of Titles",
    y="Genre",
    orientation="h",
    title="Top 15 Netflix Genres",
    labels={
        "Number of Titles": "Number of Titles",
        "Genre": "Genre"
    },
    hover_data={"Number of Titles": True}
)

genre_chart.update_layout(
    yaxis_title="Genre",
    xaxis_title="Number of Titles"
)

genre_chart.write_html(
    output_dir / "top_genres.html"
)

# STEP 7: Compare ratings across Movies and TV Shows
rating_type_counts = pd.crosstab(
    df["rating"],
    df["type"]
)

rating_type_counts.index.name = "Rating"
rating_type_counts = rating_type_counts.reset_index()

print("\n4. RATINGS BY CONTENT TYPE")
print(rating_type_counts.to_string(index=False))

# Prepare data for the interactive stacked bar chart
rating_type_long = (
    df.groupby(["rating", "type"])["show_id"]
    .nunique()
    .reset_index(name="Number of Titles")
)

rating_type_chart = px.bar(
    rating_type_long,
    x="rating",
    y="Number of Titles",
    color="type",
    barmode="stack",
    title="Content Ratings by Type: Movies vs TV Shows",
    labels={
        "rating": "Content Rating",
        "Number of Titles": "Number of Titles",
        "type": "Content Type"
    }
)

rating_type_chart.write_html(
    output_dir / "ratings_by_content_type.html"
)

# STEP 8: Calculate rating percentages within each content type
type_totals = df.groupby("type")["show_id"].nunique()

rating_type_percentages = (
    df.groupby(["type", "rating"])["show_id"]
    .nunique()
    .rename("Number of Titles")
    .reset_index()
)

rating_type_percentages["Type Total"] = (
    rating_type_percentages["type"].map(type_totals)
)

rating_type_percentages["Percentage within Type"] = (
    rating_type_percentages["Number of Titles"]
    / rating_type_percentages["Type Total"]
    * 100
).round(2)

rating_type_percentages.to_csv(
    output_dir / "rating_percentages_by_type.csv",
    index=False
)

# STEP 9: Export detailed summaries
rating_summary.to_csv(
    output_dir / "rating_summary.csv",
    index=False
)

genre_summary.to_csv(
    output_dir / "genre_summary.csv",
    index=False
)

rating_type_counts.to_csv(
    output_dir / "ratings_by_content_type.csv",
    index=False
)

# STEP 10: Prepare key findings
most_common_rating = rating_summary.iloc[0]
most_common_genre = genre_summary.iloc[0]

most_common_movie_rating = (
    df.loc[df["type"] == "Movie", "rating"]
    .value_counts()
)

most_common_tv_rating = (
    df.loc[df["type"] == "TV Show", "rating"]
    .value_counts()
)

movie_rating_text = (
    f"{most_common_movie_rating.index[0]} "
    f"({most_common_movie_rating.iloc[0]:,} titles)"
    if not most_common_movie_rating.empty
    else "Not available"
)

tv_rating_text = (
    f"{most_common_tv_rating.index[0]} "
    f"({most_common_tv_rating.iloc[0]:,} titles)"
    if not most_common_tv_rating.empty
    else "Not available"
)

report_lines = [
    "NETFLIX CONTENT RATING AND GENRE ANALYSIS",
    "=" * 50,
    "",
    "DATASET OVERVIEW",
    f"Total unique titles: {total_titles:,}",
    f"Unique ratings/categories: {df['rating'].nunique():,}",
    f"Genres identified: {genre_summary['Genre'].nunique():,}",
    "",
    "KEY FINDINGS",
    (
        f"Most common rating overall: {most_common_rating['Rating']} "
        f"({int(most_common_rating['Number of Titles']):,} titles)."
    ),
    (
        f"Most common genre: {most_common_genre['Genre']} "
        f"({int(most_common_genre['Number of Titles']):,} titles)."
    ),
    f"Most common Movie rating category: {movie_rating_text}.",
    f"Most common TV Show rating category: {tv_rating_text}.",
    "",
    "METHODOLOGY AND LIMITATIONS",
    (
        "Genre counts include one association per title and genre. "
        "A title can belong to multiple genres."
    ),
    (
        "Rating counts describe the dataset's recorded rating labels. "
        "They do not directly measure audience age or viewing behavior."
    ),
    (
        "The rating-by-type chart compares the number of titles. "
        "Use the percentage summary for comparisons that account "
        "for different totals of Movies and TV Shows."
    ),
    (
        "These results describe the available dataset and do not "
        "establish audience preferences or viewing performance."
    ),
    "",
    "INTERACTIVE CHARTS",
    "rating_distribution.html",
    "top_genres.html",
    "ratings_by_content_type.html",
    "",
    "CSV OUTPUTS",
    "rating_summary.csv",
    "genre_summary.csv",
    "ratings_by_content_type.csv",
    "rating_percentages_by_type.csv"
]

report_file = output_dir / "rating_genre_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("\n".join(report_lines))

# STEP 11: Display the key findings and output files
print("\n5. KEY FINDINGS")
print(
    f"Most common rating: {most_common_rating['Rating']}"
)
print(
    f"Most common genre: {most_common_genre['Genre']}"
)
print(f"Most common Movie rating: {movie_rating_text}")
print(f"Most common TV Show rating: {tv_rating_text}")

print("\n6. EXPORTED FILES")

for file_path in sorted(output_dir.iterdir()):
    print(file_path)

print("\nSUCCESS: Task 5 analysis completed.")
