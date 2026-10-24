# File: README.md

# News API

A students grade tracker for school examinations.
It reads the students' raw data logged by the teacher, cleans it, computes the results then outputs the report.

## What It Does

- Reads students score from a structured CSV data
- Handles missing and invalid input without crashing
- Applies logic to compute results  and assign each student's average score and grade
- Formats a clear report
- Exports the summary to JSON

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```python
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

     print(f"Top {len(articles)} {category} stories for {country}")
    print("=" * 50 + "\n")
    for number, article in enumerate(articles, start=1):
        source = (article.get("source") or {}).get("name") or "Unknown source"
        published = (article.get("publishedAt") or "")[:10]
        print(f"{number}. {article['title']}")
        print(f"   {source} | {published}")
        print(f"   {article.get('description') or 'No description'}")
        print(f"   {article.get('url') or 'No URL'}\n")

```

## Sample Output

```
Top 2 business stories for Kenya
==================================================

2. jumuia-mcp 0.1.10
   Pypi.org | 2026-10-21
   MCP server for Kenya community finance — SACCO finder, chama formation, cooperative benefits, loan guides, and member rights. 5 tools.
   https://pypi.org/project/jumuia-mcp/0.1.10/

```

## Stack

Python

Built-in Modules: `JSON`
