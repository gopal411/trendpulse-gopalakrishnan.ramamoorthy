#==================================================================================================================
# IIT PATNA - AI & ML Course - Mini Project 1
# Task 3 : Explore the cleaned stories with Pandas and NumPy.
# Author : Gopalakrishnan RAMAMOORTHY
# Version: 1.0
# Date   : 24-Sep-2026
#==================================================================================================================

#==================================================================================================================
"""Imports and Libraries"""
from pathlib import Path
import numpy as np
import pandas as pd
#==================================================================================================================

#==================================================================================================================
"""Global Variables"""
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
INPUT_PATH = DATA_DIR / "trends_clean.csv"
OUTPUT_PATH = DATA_DIR / "trends_analysed.csv"
REQUIRED_COLUMNS = {"post_id", "title", "category", "score", "num_comments"}
#==================================================================================================================


def analyze_data():
    """Print requested summary statistics and save the enriched CSV."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Run task2_data_processing.py first; missing {INPUT_PATH}")

    stories = pd.read_csv(INPUT_PATH)
    missing_columns = REQUIRED_COLUMNS - set(stories.columns)
    if missing_columns:
        raise ValueError(f"Clean CSV is missing required columns: {sorted(missing_columns)}")

    print(f"Loaded data: {stories.shape}")
    print("\nFirst 5 rows:")
    print(stories.head())

    scores = stories["score"].to_numpy(dtype=float)
    comments = stories["num_comments"].to_numpy(dtype=float)
    average_score = float(np.mean(scores)) if scores.size else 0.0
    average_comments = float(np.mean(comments)) if comments.size else 0.0
    print(f"\nAverage score   : {average_score:,.2f}")
    print(f"Average comments: {average_comments:,.2f}")

    print("\n--- NumPy Stats ---")
    if scores.size:
        print(f"Mean score   : {np.mean(scores):,.2f}")
        print(f"Median score : {np.median(scores):,.2f}")
        print(f"Std deviation: {np.std(scores):,.2f}")
        print(f"Max score    : {np.max(scores):,.0f}")
        print(f"Min score    : {np.min(scores):,.0f}")

        category_counts = stories["category"].value_counts()
        if not category_counts.empty:
            most_common_category = category_counts.idxmax()
            print(
                f"\nMost stories in: {most_common_category} "
                f"({category_counts[most_common_category]} stories)"
            )

        most_commented_index = int(np.argmax(comments))
        most_commented = stories.iloc[most_commented_index]
        print(
            f"\nMost commented story: \"{most_commented['title']}\" "
            f"— {int(comments[most_commented_index]):,} comments"
        )
    else:
        print("No stories available for statistics.")

    # Add the requested derived fields using the dataset-wide average score.
    stories["engagement"] = stories["num_comments"] / (stories["score"] + 1)
    stories["is_popular"] = stories["score"] > average_score
    stories.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH.relative_to(PROJECT_DIR)}")
    return stories


if __name__ == "__main__":
    print("========Task 3: Story Analysis started===================")
    analyze_data()
    print("========Task 3: Completed================================")