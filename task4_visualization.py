#==================================================================================================================
# IIT PATNA - AI & ML Course - Mini Project 1
# Task 4 : Create the three requested charts and a combined TrendPulse dashboard.
# Author : Gopalakrishnan RAMAMOORTHY
# Version: 1.0
# Date   : 24-Sep-2026
#==================================================================================================================

#==================================================================================================================
"""Imports and Libraries"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
#==================================================================================================================

#==================================================================================================================
"""Global Variables"""
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
INPUT_PATH = DATA_DIR / "trends_analysed.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
CATEGORY_ORDER = ["technology", "worldnews", "sports", "science", "entertainment"]
REQUIRED_COLUMNS = {"title", "category", "score", "num_comments", "is_popular"}
#==================================================================================================================

def short_title(title):
    """Keep chart labels readable without changing the source data."""
    title = str(title)
    return title if len(title) <= 50 else f"{title[:47]}..."


def draw_top_stories(axis, stories):
    top_stories = stories.nlargest(10, "score").sort_values("score")
    axis.barh(top_stories["title"].map(short_title), top_stories["score"], color="#287D78")
    axis.set_title("Top 10 Stories by Score")
    axis.set_xlabel("Score")
    axis.set_ylabel("Story title")


def draw_categories(axis, stories):
    counts = stories["category"].value_counts().reindex(CATEGORY_ORDER, fill_value=0)
    colors = plt.get_cmap("tab10").colors[: len(counts)]
    axis.bar(counts.index, counts.values, color=colors)
    axis.set_title("Stories per Category")
    axis.set_xlabel("Category")
    axis.set_ylabel("Number of stories")
    axis.tick_params(axis="x", labelrotation=25)


def draw_scatter(axis, stories):
    popular = stories["is_popular"].astype(str).str.lower().eq("true")
    axis.scatter(
        stories.loc[~popular, "score"],
        stories.loc[~popular, "num_comments"],
        color="#D17A22",
        label="Not popular",
        alpha=0.75,
    )
    axis.scatter(
        stories.loc[popular, "score"],
        stories.loc[popular, "num_comments"],
        color="#287D78",
        label="Popular",
        alpha=0.75,
    )
    axis.set_title("Score vs Comments")
    axis.set_xlabel("Score")
    axis.set_ylabel("Number of comments")
    axis.legend()


def create_charts():
    """Load Task 3 output and write three charts plus their dashboard."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Run task3_analysis.py first; missing {INPUT_PATH}")

    stories = pd.read_csv(INPUT_PATH)
    missing_columns = REQUIRED_COLUMNS - set(stories.columns)
    if missing_columns:
        raise ValueError(f"Analysed CSV is missing required columns: {sorted(missing_columns)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(11, 7))
    draw_top_stories(axis, stories)
    figure.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart1_top_stories.png", dpi=150, bbox_inches="tight")
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(9, 6))
    draw_categories(axis, stories)
    figure.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart2_categories.png", dpi=150, bbox_inches="tight")
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(9, 6))
    draw_scatter(axis, stories)
    figure.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart3_scatter.png", dpi=150, bbox_inches="tight")
    plt.close(figure)

    # Reuse the same chart functions so dashboard charts match the standalone files.
    figure, axes = plt.subplots(2, 2, figsize=(16, 11))
    draw_top_stories(axes[0, 0], stories)
    draw_categories(axes[0, 1], stories)
    draw_scatter(axes[1, 0], stories)
    axes[1, 1].axis("off")
    figure.suptitle("TrendPulse Dashboard", fontsize=16)
    figure.tight_layout(rect=(0, 0, 1, 0.96))
    plt.savefig(OUTPUT_DIR / "dashboard.png", dpi=150, bbox_inches="tight")
    plt.close(figure)

    print(f"Saved 3 charts and the dashboard to {OUTPUT_DIR.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    print("========Task 4: Trending Visualization started===================")
    create_charts()
    print("========Task 4: Completed================================")