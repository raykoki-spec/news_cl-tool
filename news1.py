import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"
MAX_ARTICLES = 2

# Each category maps to search terms that are combined with the country name
CATEGORIES = {
    "technology": "(technology OR tech OR software OR startup OR AI)",
    "business": "(business OR economy OR finance OR trade OR markets)",
    "sports": "(sports OR football OR athletics OR rugby OR cricket)",
}

HINTS = {
    401: "The API key is invalid or not yet active. Check your .env file.",
    429: "Too many requests. Wait before trying again.",
}


def ask_country():
    while True:
        country = input("Enter a country of interest: ").strip()
        if country:
            return country
        print("Country cannot be empty.")


def ask_category():
    names = list(CATEGORIES)
    print("\nChoose a category:")
    for number, name in enumerate(names, start=1):
        print(f"  {number}. {name.capitalize()}")

    while True:
        choice = input("Enter a category name or number: ").strip().lower()
        if choice in CATEGORIES:
            return choice
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return names[int(choice) - 1]
        print("Invalid choice. Please pick technology, business or sports.")


def fetch_articles(country, category):
    query = f'"{country}" AND {CATEGORIES[category]}'
    params = urlencode({
        "q": query,
        "searchIn": "title,description",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": MAX_ARTICLES,
    })
    request = Request(f"{BASE_URL}?{params}", headers={"X-Api-Key": API_KEY})
    with urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("articles", [])


def main():
    if not API_KEY:
        sys.exit("NEWS_API_KEY is not set in the .env file.")

    try:
        country = ask_country()
        category = ask_category()
    except (KeyboardInterrupt, EOFError):
        sys.exit("\nCancelled.")

    print(f"\nFetching {category} news for {country}...\n")

    try:
        articles = fetch_articles(country, category)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            message = json.loads(body).get("message", body)
        except json.JSONDecodeError:
            message = body
        sys.exit(f"{HINTS.get(error.code, 'Request failed.')} (HTTP {error.code}: {message})")
    except (URLError, TimeoutError) as error:
        sys.exit(f"Could not reach NewsAPI: {error}")

    articles = [a for a in articles if a.get("title") and a["title"] != "[Removed]"]
    if not articles:
        sys.exit(f"No {category} news found for {country}.")

    print(f"Top {len(articles)} {category} stories for {country}")
    print("=" * 50 + "\n")
    for number, article in enumerate(articles, start=1):
        source = (article.get("source") or {}).get("name") or "Unknown source"
        published = (article.get("publishedAt") or "")[:10]
        print(f"{number}. {article['title']}")
        print(f"   {source} | {published}")
        print(f"   {article.get('description') or 'No description'}")
        print(f"   {article.get('url') or 'No URL'}\n")


if __name__ == "__main__":
    main()