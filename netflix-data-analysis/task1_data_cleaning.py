
import pandas as pd

# ==================================================
# AUSPIFY INTERNSHIP - TASK 1
# NETFLIX DATA CLEANING AND PREPARATION
# ==================================================

# STEP 1: Load the original dataset
df = pd.read_csv("Dataset.csv")

print("=" * 55)
print("NETFLIX DATA CLEANING AND PREPARATION")
print("=" * 55)

print("\n1. ORIGINAL DATASET")
print("Rows and columns:", df.shape)
print("Missing values:", df.isnull().sum().sum())
print("Exact duplicate rows:", df.duplicated().sum())

# STEP 2: Create a copy so the original data stays unchanged
cleaned_df = df.copy()

# STEP 3: Standardize text formatting
# Remove unnecessary spaces at the beginning and end.
text_columns = cleaned_df.select_dtypes(include="str").columns

for column in text_columns:
    cleaned_df[column] = cleaned_df[column].str.strip()

print("\n2. TEXT FORMATTING")
print("Leading/trailing spaces have been removed where present.")

# STEP 4: Standardize the Type column
# Preserve the correct capitalization of TV Show.
cleaned_df["type"] = cleaned_df["type"].replace({
    "movie": "Movie",
    "Movie": "Movie",
    "tv show": "TV Show",
    "TV Show": "TV Show",
    "Tv Show": "TV Show"
})

print("\n3. STANDARDIZED CONTENT TYPES")
print(cleaned_df["type"].value_counts())

# Confirm that the expected categories are present.
expected_types = {"Movie", "TV Show"}
actual_types = set(cleaned_df["type"].unique())

if actual_types != expected_types:
    raise ValueError(
        f"Unexpected content types found: {actual_types}"
    )

# STEP 5: Standardize Country formatting
# Trim spaces around individual country names.
# Preserve comma-separated country names and their order.
cleaned_df["country"] = cleaned_df["country"].apply(
    lambda value: ", ".join(
        part.strip() for part in value.split(",")
    )
)

print("\n4. COUNTRY STANDARDIZATION")
print("Country formatting checked.")
print(
    "'Not Given' records:",
    cleaned_df["country"].eq("Not Given").sum()
)

# STEP 6: Standardize Rating formatting
cleaned_df["rating"] = cleaned_df["rating"].str.upper()

print("\n5. RATING STANDARDIZATION")
print("Rating categories:")
print(sorted(cleaned_df["rating"].unique()))

# STEP 7: Convert date_added to a proper date
cleaned_df["date_added"] = pd.to_datetime(
    cleaned_df["date_added"],
    format="%m/%d/%Y",
    errors="coerce"
)

unconverted_dates = cleaned_df["date_added"].isna().sum()

print("\n6. DATE CONVERSION")
print("Dates that could not be converted:", unconverted_dates)

if unconverted_dates > 0:
    raise ValueError(
        "Some dates could not be converted. "
        "Investigate them before exporting."
    )

# STEP 8: Remove exact duplicate rows if present
rows_before = len(cleaned_df)

cleaned_df = cleaned_df.drop_duplicates()

duplicates_removed = rows_before - len(cleaned_df)

print("\n7. DUPLICATE REMOVAL")
print("Duplicate rows removed:", duplicates_removed)

# STEP 9: Validate the cleaned dataset
print("\n8. FINAL VALIDATION")
print("Final shape:", cleaned_df.shape)

print("\nMissing values per column:")
print(cleaned_df.isnull().sum())

print("\nExact duplicate rows remaining:")
print(cleaned_df.duplicated().sum())

print("\nFinal content types:")
print(cleaned_df["type"].value_counts())

# STEP 10: Export the cleaned dataset
output_file = "netflix_cleaned.csv"

cleaned_df.to_csv(output_file, index=False)

print("\n9. EXPORT")
print(f"Successfully exported: {output_file}")
print("Task 1 cleaning script completed.")
