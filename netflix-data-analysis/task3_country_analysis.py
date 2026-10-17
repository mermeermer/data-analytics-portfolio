
# ============================================================
# AUSPIFY INTERNSHIP - TASK 3
# NETFLIX COUNTRY-WISE CONTENT ANALYSIS
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# STEP 1: Create the output folder
output_dir = Path("task3_outputs")
output_dir.mkdir(exist_ok=True)

# STEP 2: Load the cleaned dataset from Task 1
input_file = Path("netflix_cleaned.csv")

if not input_file.exists():
    raise FileNotFoundError(
        "netflix_cleaned.csv was not found. "
        "Run Task 1 first and check that the file is in "
        "your project folder."
    )

df = pd.read_csv(input_file)

print("=" * 65)
print("NETFLIX COUNTRY-WISE CONTENT ANALYSIS")
print("=" * 65)

# STEP 3: Validate the required columns
required_columns = ["show_id", "title", "country"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"The dataset is missing the required column: {column}"
        )

if df["show_id"].isna().any():
    raise ValueError(
        "The dataset contains missing show IDs. "
        "Please investigate before continuing."
    )

total_titles = df["show_id"].nunique()

print("\n1. DATASET OVERVIEW")
print(f"Total dataset rows: {len(df):,}")
print(f"Unique titles: {total_titles:,}")

# STEP 4: Identify titles without country information
# Treat blank values and 'Not Given' as unavailable information.
country_text = df["country"].fillna("").astype(str).str.strip()

missing_country_mask = (
    country_text.eq("")
    | country_text.str.casefold().eq("not given")
)

titles_without_country = df.loc[
    missing_country_mask, "show_id"
].nunique()

print(
    "Titles without country information:",
    f"{titles_without_country:,}"
)

# STEP 5: Keep only titles with country information
country_df = df.loc[
    ~missing_country_mask,
    ["show_id", "title", "country"]
].copy()

# STEP 6: Split titles associated with multiple countries
# Example: "India, United States" becomes two country records.
country_df["country"] = country_df["country"].str.split(",")

country_df = country_df.explode("country")

# Remove extra spaces around each country name.
country_df["country"] = country_df["country"].str.strip()

# Remove any empty or unavailable country entries.
country_df = country_df[
    country_df["country"].ne("")
    & country_df["country"].str.casefold().ne("not given")
].copy()

# Count a title only once per country.
country_df = country_df.drop_duplicates(
    subset=["show_id", "country"]
)

if country_df.empty:
    raise ValueError(
        "No valid country records were found in the dataset."
    )

# STEP 7: Calculate country-wise title counts
country_counts = (
    country_df.groupby("country")["show_id"]
    .nunique()
    .sort_values(ascending=False)
)

country_summary = country_counts.reset_index()
country_summary.columns = ["Country", "Number of Titles"]

# Calculate the percentage of titles with known country
# information associated with each country.
# Because some titles have multiple countries, percentages
# can add up to more than 100%.
country_summary["Percentage of Known-Country Titles"] = (
    country_summary["Number of Titles"]
    / country_df["show_id"].nunique()
    * 100
).round(2)

print("\n2. COUNTRY ANALYSIS")
print(f"Countries identified: {len(country_summary):,}")
print(
    "Titles with at least one known country:",
    f"{country_df['show_id'].nunique():,}"
)

# STEP 8: Display the top 10 countries
top_10 = country_summary.head(10).copy()

print("\n3. TOP 10 COUNTRIES BY TITLE COUNT")
print(top_10.to_string(index=False))

# STEP 9: Create a bar chart for the top 10 countries
chart_data = top_10.sort_values(
    by="Number of Titles",
    ascending=True
)

plt.figure(figsize=(12, 7))

bars = plt.barh(
    chart_data["Country"],
    chart_data["Number of Titles"]
)

plt.title(
    "Top 10 Countries by Number of Netflix Titles",
    fontsize=15
)
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.grid(axis="x", linestyle="--", alpha=0.4)

# Add exact counts beside each bar.
for bar in bars:
    width = int(bar.get_width())

    plt.annotate(
        f"{width:,}",
        xy=(width, bar.get_y() + bar.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        fontsize=9
    )

plt.tight_layout()

chart_file = output_dir / "top_10_countries_chart.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# STEP 10: Export the complete country summary
summary_file = output_dir / "country_wise_summary.csv"

country_summary.to_csv(
    summary_file,
    index=False
)

# STEP 11: Generate a written report
top_country = country_summary.iloc[0]

report_lines = [
    "NETFLIX COUNTRY-WISE CONTENT ANALYSIS",
    "=" * 50,
    "",
    "DATASET OVERVIEW",
    f"Total dataset rows: {len(df):,}",
    f"Unique titles: {total_titles:,}",
    f"Countries identified: {len(country_summary):,}",
    (
        "Titles without country information: "
        f"{titles_without_country:,}"
    ),
    (
        "Titles with at least one known country: "
        f"{country_df['show_id'].nunique():,}"
    ),
    "",
    "TOP 10 COUNTRIES",
    "-" * 30
]

for rank, row in enumerate(top_10.itertuples(index=False), start=1):
    report_lines.append(
        f"{rank}. {row.Country}: {row._1:,} titles"
    )

report_lines.extend([
    "",
    "KEY FINDINGS",
    (
        f"The country with the highest title count is "
        f"{top_country['Country']}, with "
        f"{int(top_country['Number of Titles']):,} titles."
    ),
    (
        f"The dataset contains {titles_without_country:,} titles "
        "without usable country information."
    ),
    "",
    "METHODOLOGY AND LIMITATIONS",
    (
        "Titles listing multiple countries are counted once "
        "for each listed country."
    ),
    (
        "Each title-country combination is counted only once."
    ),
    (
        "Country counts therefore represent title-country "
        "associations and may add up to more than the total "
        "number of unique titles."
    ),
    (
        "Country percentages use the number of unique titles "
        "with at least one known country as the denominator. "
        "They may add up to more than 100% because titles "
        "can be associated with multiple countries."
    ),
    (
        "These results describe the dataset and do not, by "
        "themselves, establish audience preferences or "
        "viewing performance."
    ),
    "",
    "OUTPUT FILES",
    "top_10_countries_chart.png",
    "country_wise_summary.csv",
    "country_wise_report.txt"
])

report_file = output_dir / "country_wise_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("\n".join(report_lines))

# STEP 12: Display exported files
print("\n4. OUTPUT FILES")

for file_path in sorted(output_dir.iterdir()):
    print(file_path)

print("\nSUCCESS: Task 3 analysis completed.")
