#==================================================================================================================
# IIT PATNA - AI & ML Course - Mini Project 1
# Task 1 : Collect and categorize trending stories from the Hacker News API.
# Author : Gopalakrishnan RAMAMOORTHY
# Version: 1.0
# Date   : 24-Sep-2026
#==================================================================================================================

#==================================================================================================================
"""Imports and Libraries"""
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import requests
from urllib.parse import urlsplit
#==================================================================================================================

#==================================================================================================================
"""Global Variables"""
BASE_URL = "https://hacker-news.firebaseio.com/v0"
ALLOWED_HOSTS = {"hacker-news.firebaseio.com"}
HEADERS = {"User-Agent": "TrendPulse/1.0"}
TOP_STORY_LIMIT = 500
STORIES_PER_CATEGORY = 25
MINIMUM_STORY_COUNT = 100

CATEGORY_KEYWORDS = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}
#==================================================================================================================

def get_json(url):
    """Return decoded JSON for a URL, or None when the request fails."""
    try:
        parsed = urlsplit(url)
        if (
            parsed.scheme != "https"
            or parsed.hostname not in ALLOWED_HOSTS
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port not in (None, 443)
            or not parsed.path.startswith("/v0/")
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("URL is not allowed")
        response = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=False)

        if 300 <= response.status_code < 400:
            raise ValueError("Redirects are not allowed")

        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        print(f"Request failed for {url}: {error}")
        return None


def category_for_title(title):
    """Return the first matching category, using the required category order."""
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in title_lower for keyword in keywords):
            return category
    return None


def collect_stories():
    """Fetch and categorize stories, supplementing top stories if needed."""
    print("========Task 1: collecting stories=======================")
    story_ids = get_json(f"{BASE_URL}/topstories.json")
    if not isinstance(story_ids, list):
        print("Could not retrieve a valid list of top story IDs.")
        return []

    stories_by_category = {category: [] for category in CATEGORY_KEYWORDS}
    collected_at = datetime.now(timezone.utc).isoformat()
    processed_ids = set()

    def collect_from_ids(candidate_ids):
        for story_id in candidate_ids[:TOP_STORY_LIMIT]:
            if story_id in processed_ids:
                continue
            processed_ids.add(story_id)

            story = get_json(f"{BASE_URL}/item/{story_id}.json")
            if not isinstance(story, dict) or story.get("type") != "story":
                continue

            title = story.get("title", "").strip()
            category = category_for_title(title)
            if category is None or len(stories_by_category[category]) >= STORIES_PER_CATEGORY:
                continue

            stories_by_category[category].append(
                {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": collected_at,
                }
            )

            story_count = sum(len(stories) for stories in stories_by_category.values())
            if story_count >= MINIMUM_STORY_COUNT or all(
                len(stories) == STORIES_PER_CATEGORY
                for stories in stories_by_category.values()
            ):
                return

    # Fetch the first 500 top stories, then supplement from new stories if needed.
    collect_from_ids(story_ids)
    story_count = sum(len(stories) for stories in stories_by_category.values())
    if story_count < MINIMUM_STORY_COUNT:
        new_story_ids = get_json(f"{BASE_URL}/newstories.json")
        if isinstance(new_story_ids, list):
            collect_from_ids(new_story_ids)

    # Keep the required pause between category-processing intervals.
    for category_index, category in enumerate(CATEGORY_KEYWORDS):
        print(f"{category}: {len(stories_by_category[category])} stories")
        if category_index < len(CATEGORY_KEYWORDS) - 1:
            time.sleep(2)

    return [story for category in CATEGORY_KEYWORDS for story in stories_by_category[category]]


def save_stories(stories):
    print("========Task 1: stories ready============================")
    """Save collected stories to a date-stamped JSON file."""
    output_directory = Path("data")
    output_directory.mkdir(exist_ok=True)
    output_path = output_directory / f"trends_{datetime.now().strftime('%Y%m%d')}.json"
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(stories, output_file, indent=2, ensure_ascii=False)
    return output_path


if __name__ == "__main__":
    print("========Task 1: Data Collection==========================")
    stories = collect_stories()
    output_path = save_stories(stories)
    print(f"Collected {len(stories)} stories. Saved to {output_path}")
    print("========Task 1: Completed================================")
