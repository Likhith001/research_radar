from app.db.database import SessionLocal
from app.db.models import Paper

def save_paper(paper_data, summary, score):
    db = SessionLocal()

    # Check duplicate
    existing = db.query(Paper).filter(Paper.link == paper_data["link"]).first()

    if existing:
        db.close()
        return None  # skip duplicate

    new_paper = Paper(
        title=paper_data["title"],
        abstract=paper_data["abstract"],
        summary=summary,
        link=paper_data["link"],
        score=score
    )

    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    db.close()

    return new_paper