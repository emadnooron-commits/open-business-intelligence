from scheduler import Scheduler
from supervisor import supervisor
from agents.agent import research_agent


scheduler = Scheduler()

task = {
    "id": "NOOR-001",
    "title": "Research charcoal competitors",
    "skill": "competitor_analysis",
    "priority": 10
}

scheduler.add_task(task)

next_task = scheduler.next_task()

agent = scheduler.assign_agent(next_task)

print("=== NOOR AI OS ===")
print("Task:", next_task["title"])

if agent:
    print("Agent:", agent.name)

    result = {
        "validated": True,
        "risk": "LOW",
        "message": "Research completed successfully"
    }

    decision = supervisor.review(result)

    print("Supervisor:", decision)

else:
    print("No suitable Agent found")
