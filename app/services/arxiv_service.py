import feedparser
import urllib.parse

def fetch_arxiv(query="machine learning", max_results=5):
    
    # ✅ encode query (THIS FIXES YOUR ERROR)
    encoded_query = urllib.parse.quote(query)

    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    
    feed = feedparser.parse(url)

    papers = []

    for entry in feed.entries:
        paper = {
            "title": entry.title,
            "abstract": entry.summary,
            "link": entry.id
        }
        papers.append(paper)

    return papers