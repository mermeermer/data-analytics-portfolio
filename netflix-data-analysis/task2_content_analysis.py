
# ============================================================
# AUSPIFY INTERNSHIP - TASK 2
# NETFLIX CONTENT TYPE ANALYSIS DASHBOARD
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# STEP 1: Create the output folder
output_dir = Path("task2_outputs")
output_dir.mkdir(exist_ok=True)

# STEP 2: Load the cleaned dataset
df = pd.read_csv("netflix_cleaned.csv")

print("=" * 60)
print("NETFLIX CONTENT TYPE ANALYSIS")
print("=" * 60)

# STEP 3: Validate the dataset
if "type" not in df.columns:
    raise ValueError("The dataset does not contain a 'type' column.")

if df["type"].isna().any():
    raise ValueError("The Type column contains missing values.")

# STEP 4: Count Movies and TV Shows
content_counts = df["type"].value_counts()

expected_types = ["Movie", "TV Show"]
content_counts = content_counts.reindex(
    expected_types, fill_value=0
)

total_titles = int(content_counts.sum())

if total_titles == 0:
    raise ValueError("No content records were found.")

# STEP 5: Calculate percentages
content_percentages = (
    content_counts / total_titles * 100
).round(2)

summary = pd.DataFrame({
    "Content Type": content_counts.index,
    "Number of Titles": content_counts.values,
    "Percentage": content_percentages.values
})

print("\n1. CONTENT DISTRIBUTION")
print(summary.to_string(index=False))
print(f"\nTotal titles analyzed: {total_titles:,}")

# STEP 6: Create the bar chart
plt.figure(figsize=(9, 6))

bars = plt.bar(
    content_counts.index,
    content_counts.values
)

plt.title("Netflix Content Distribution by Type")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.grid(axis="y", linestyle="--", alpha=0.4)

# Display actual counts above each bar
for bar in bars:
    height = int(bar.get_height())
    plt.annotate(
        f"{height:,}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    output_dir / "content_type_bar_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# STEP 7: Create the pie chart
plt.figure(figsize=(8, 8))

plt.pie(
    content_counts.values,
    labels=content_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Percentage Share of Netflix Content Types")
plt.tight_layout()

plt.savefig(
    output_dir / "content_type_pie_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# STEP 8: Calculate key findings
movie_count = int(content_counts["Movie"])
tv_count = int(content_counts["TV Show"])

movie_pct = movie_count / total_titles * 100
tv_pct = tv_count / total_titles * 100
difference = abs(movie_pct - tv_pct)

findings = [
    "NETFLIX CONTENT TYPE ANALYSIS - SUMMARY",
    "=" * 45,
    f"Total titles analyzed: {total_titles:,}",
    f"Movies: {movie_count:,} ({movie_pct:.2f}%)",
    f"TV Shows: {tv_count:,} ({tv_pct:.2f}%)",
    f"Difference: {difference:.2f} percentage points",
    "",
    "KEY FINDINGS",
    f"1. Movies represent {movie_pct:.2f}% of the dataset.",
    f"2. TV Shows represent {tv_pct:.2f}% of the dataset.",
    f"3. Movies exceed TV Shows by {difference:.2f} percentage points.",
    "",
    "INTERPRETATION",
    "The dataset contains a larger share of movies than TV shows.",
    "This describes the dataset's composition; it does not, by itself,",
    "establish audience preferences or viewing performance.",
    "",
    "OUTPUT FILES",
    "content_type_bar_chart.png",
    "content_type_pie_chart.png",
    "content_type_summary.csv",
    "content_type_report.txt"
]

report_text = "\n".join(findings)

# STEP 9: Export the summary and report
summary.to_csv(
    output_dir / "content_type_summary.csv",
    index=False
)

with open(
    output_dir / "content_type_report.txt",
    "w",
    encoding="utf-8"
) as report_file:
    report_file.write(report_text)

# STEP 10: Display final results
print("\n2. KEY FINDINGS")
print(f"Movies: {movie_pct:.2f}%")
print(f"TV Shows: {tv_pct:.2f}%")
print(f"Difference: {difference:.2f} percentage points")

print("\n3. EXPORTED FILES")

for file_path in sorted(output_dir.iterdir()):
    print(file_path)

print("\nSUCCESS: Task 2 analysis completed.")
