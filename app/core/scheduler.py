from apscheduler.schedulers.background import BackgroundScheduler
from app.agents.orchestrator import Orchestrator

scheduler = BackgroundScheduler()

def run_job():
    print("Running scheduled job...")
    orch = Orchestrator()
    results = orch.run()
    print("Scheduled results:", results)

def start_scheduler():
    scheduler.add_job(run_job, "interval", minutes=30)
    scheduler.start()