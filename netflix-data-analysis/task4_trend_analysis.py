
# ============================================================
# AUSPIFY INTERNSHIP - TASK 4
# NETFLIX RELEASE-YEAR TREND ANALYSIS
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# STEP 1: Create the output folder
output_dir = Path("task4_outputs")
output_dir.mkdir(exist_ok=True)

# STEP 2: Load the cleaned dataset
input_file = Path("netflix_cleaned.csv")

if not input_file.exists():
    raise FileNotFoundError(
        "netflix_cleaned.csv was not found. Please run Task 1 first."
    )

df = pd.read_csv(input_file)

print("=" * 60)
print("NETFLIX RELEASE-YEAR TREND ANALYSIS")
print("=" * 60)

# STEP 3: Validate required columns
required_columns = ["show_id", "release_year"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column '{column}' was not found."
        )

if df["show_id"].isna().any():
    raise ValueError("Missing show IDs were found.")

total_titles = df["show_id"].nunique()

print("\n1. DATASET OVERVIEW")
print(f"Total dataset rows: {len(df):,}")
print(f"Unique titles: {total_titles:,}")

# STEP 4: Convert release year to numeric
df["release_year"] = pd.to_numeric(
    df["release_year"],
    errors="coerce"
)

valid_df = df.dropna(subset=["release_year"]).copy()

# Release years must be whole numbers
valid_df = valid_df[
    valid_df["release_year"] % 1 == 0
].copy()

valid_df["release_year"] = (
    valid_df["release_year"].astype(int)
)

titles_without_year = (
    df.loc[df["release_year"].isna(), "show_id"].nunique()
)

if valid_df.empty:
    raise ValueError("No valid release-year records were found.")

print(f"Titles with valid release years: {len(valid_df):,}")
print(f"Titles without valid release years: {titles_without_year:,}")

# STEP 5: Count unique titles by release year
yearly_counts = (
    valid_df.groupby("release_year")["show_id"]
    .nunique()
    .sort_index()
)

# Include years with zero titles between the first and last year
all_years = range(
    int(yearly_counts.index.min()),
    int(yearly_counts.index.max()) + 1
)

yearly_summary = (
    yearly_counts
    .reindex(all_years, fill_value=0)
    .rename_axis("Release Year")
    .reset_index(name="Number of Titles")
)

yearly_summary["Number of Titles"] = (
    yearly_summary["Number of Titles"].astype(int)
)

# STEP 6: Calculate year-over-year changes
yearly_summary["Change in Titles"] = (
    yearly_summary["Number of Titles"].diff()
)

previous_year_count = (
    yearly_summary["Number of Titles"].shift(1)
)

# Calculate percentage change only when the previous year
# has a count greater than zero. Otherwise, leave it undefined.
yearly_summary["Year-over-Year Change (%)"] = (
    (
        yearly_summary["Number of Titles"]
        - previous_year_count
    )
    .div(previous_year_count.where(previous_year_count > 0))
    .mul(100)
    .round(2)
)

# The first year has no previous year for comparison.
yearly_summary.loc[
    0, ["Change in Titles", "Year-over-Year Change (%)"]
] = float("nan")

# STEP 7: Identify key trend statistics
peak_row = yearly_summary.loc[
    yearly_summary["Number of Titles"].idxmax()
]

earliest_year = int(yearly_summary["Release Year"].min())
latest_year = int(yearly_summary["Release Year"].max())
peak_year = int(peak_row["Release Year"])
peak_count = int(peak_row["Number of Titles"])

print("\n2. KEY FINDINGS")
print(f"Earliest release year: {earliest_year}")
print(f"Latest release year: {latest_year}")
print(f"Peak year: {peak_year}")
print(f"Titles released in peak year: {peak_count:,}")

# STEP 8: Create the trend chart
plt.figure(figsize=(14, 7))

plt.plot(
    yearly_summary["Release Year"],
    yearly_summary["Number of Titles"],
    marker="o",
    markersize=3,
    linewidth=1.8
)

plt.title("Netflix Titles by Release Year", fontsize=15)
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

chart_file = output_dir / "release_year_trend.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# STEP 9: Export the yearly summary
summary_file = output_dir / "release_year_summary.csv"

yearly_summary.to_csv(
    summary_file,
    index=False
)

# STEP 10: Create the written report
report_lines = [
    "NETFLIX RELEASE-YEAR TREND ANALYSIS",
    "=" * 50,
    "",
    "DATASET OVERVIEW",
    f"Total unique titles: {total_titles:,}",
    f"Titles with valid release years: {len(valid_df):,}",
    f"Titles without valid release years: {titles_without_year:,}",
    f"Earliest release year: {earliest_year}",
    f"Latest release year: {latest_year}",
    "",
    "KEY FINDINGS",
    (
        f"The highest yearly title count occurred in {peak_year}, "
        f"with {peak_count:,} titles."
    ),
    (
        "The CSV includes yearly counts, changes in counts, "
        "and percentage changes compared with the previous year."
    ),
    "",
    "INTERPRETATION AND LIMITATIONS",
    (
        "Release year indicates when a title was originally released, "
        "not necessarily when it was added to Netflix."
    ),
    (
        "The dataset is a snapshot of Netflix titles and does not "
        "represent every title released worldwide in each year."
    ),
    (
        "The newest years may be incomplete in this dataset, "
        "so their lower counts should be interpreted cautiously."
    ),
    (
        "Percentage change is left blank when the previous year "
        "has zero titles because the calculation is undefined."
    ),
    "",
    "OUTPUT FILES",
    "release_year_trend.png",
    "release_year_summary.csv",
    "release_year_report.txt"
]

report_file = output_dir / "release_year_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("\n".join(report_lines))

# STEP 11: Display a concise preview
print("\n3. RECENT YEARLY COUNTS")
print(yearly_summary.tail(10).to_string(index=False))

print("\n4. EXPORTED FILES")

for file_path in sorted(output_dir.iterdir()):
    print(file_path)

print("\nSUCCESS: Task 4 analysis completed.")
