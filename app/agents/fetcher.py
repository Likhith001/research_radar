from app.services.arxiv_service import fetch_arxiv



class FetcherAgent:
    def run(self, topic="machine learning"):
        return fetch_arxiv(query=topic)