from app.agents.fetcher import FetcherAgent
from app.agents.summarizer import SummarizerAgent
from app.agents.scorer import ScorerAgent
from app.agents.notifier import NotifierAgent
from app.services.email_service import send_email
from app.services.db_service import save_paper


class Orchestrator:

    def __init__(self):
        self.fetcher = FetcherAgent()
        self.summarizer = SummarizerAgent()
        self.scorer = ScorerAgent()
        self.notifier = NotifierAgent()

    def run(self, topic="machine learning"):
        papers = self.fetcher.run(topic)
        results = []

        for paper in papers[:2]:  # ✅ limit to 2 papers
            summary = self.summarizer.summarize(paper["abstract"])
            score = self.scorer.score(summary)
            saved = save_paper(paper, summary, score)

            if saved:
                results.append(f"{paper['title']} (Score: {score:.2f})")

        
        # ✅ send email
        if results:
            content = "\n".join(results)
            send_email(content)

        self.notifier.notify(f"{len(results)} new papers stored")

        return results