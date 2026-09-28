#==================================================================================================================
# IIT PATNA - AI & ML Course - Mini Project 1
# Task 2 : Clean the latest Task 1 JSON file and save it as a CSV.
# Author : Gopalakrishnan RAMAMOORTHY
# Version: 1.0
# Date   : 24-Sep-2026
#==================================================================================================================

#==================================================================================================================
"""Imports and Libraries"""
import json
from pathlib import Path
import pandas as pd
#==================================================================================================================

#==================================================================================================================
"""Global Variables"""
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
CATEGORY_ORDER = ["technology", "worldnews", "sports", "science", "entertainment"]
REQUIRED_COLUMNS = [
    "post_id",
    "title",
    "category",
    "score",
    "num_comments",
    "author",
    "collected_at",
]
#==================================================================================================================

def latest_trends_file():
    """Return the newest dated Task 1 JSON file."""
    files = list(DATA_DIR.glob("trends_*.json"))
    if not files:
        raise FileNotFoundError(f"No trends_YYYYMMDD.json file found in {DATA_DIR}")
    return max(files, key=lambda path: path.stat().st_mtime)


def clean_data(input_path=None):
    """Load, clean, and save the Task 1 stories as a CSV."""
    input_path = Path(input_path) if input_path else latest_trends_file()
    if not input_path.is_absolute():
        input_path = PROJECT_DIR / input_path

    with input_path.open("r", encoding="utf-8") as input_file:
        records = json.load(input_file)
    if not isinstance(records, list):
        raise ValueError(f"Expected a JSON list of stories in {input_path}")

    stories = pd.DataFrame(records)
    missing_columns = set(REQUIRED_COLUMNS) - set(stories.columns)
    if missing_columns:
        raise ValueError(f"Input JSON is missing required fields: {sorted(missing_columns)}")

    print(f"Loaded {len(stories)} stories from {input_path.relative_to(PROJECT_DIR)}")

    # Keep the first copy of each Hacker News post.
    stories = stories.drop_duplicates(subset="post_id", keep="first").copy()
    print(f"After removing duplicates: {len(stories)}")

    stories["title"] = stories["title"].astype("string").str.strip()
    stories["title"] = stories["title"].replace("", pd.NA)
    stories["score"] = pd.to_numeric(stories["score"], errors="coerce")
    stories["num_comments"] = pd.to_numeric(stories["num_comments"], errors="coerce").fillna(0)
    stories = stories.dropna(subset=["post_id", "title", "score"]).copy()
    print(f"After removing nulls: {len(stories)}")

    stories["score"] = stories["score"].astype(int)
    stories["num_comments"] = stories["num_comments"].astype(int)
    stories = stories.loc[stories["score"] >= 5].copy()
    print(f"After removing low scores: {len(stories)}")

    output_path = DATA_DIR / "trends_clean.csv"
    stories.to_csv(output_path, index=False)
    print(f"\nSaved {len(stories)} rows to {output_path.relative_to(PROJECT_DIR)}")
    print("\nStories per category:")
    category_counts = stories["category"].value_counts().reindex(CATEGORY_ORDER, fill_value=0)
    for category, count in category_counts.items():
        print(f"  {category:<14} {count}")
    return stories


if __name__ == "__main__":
    print("========Task 2: Data Processing on Json File started=====")
    clean_data()
    print("========Task 2: Completed================================")