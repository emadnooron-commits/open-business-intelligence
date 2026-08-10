from agents.agent import research_agent


class Scheduler:

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def next_task(self):
        if not self.tasks:
            return None

        self.tasks.sort(
            key=lambda task: task["priority"],
            reverse=True
        )

        return self.tasks.pop(0)

    def assign_agent(self, task):

        if research_agent.can_do(task["skill"]):
            return research_agent

        return None


scheduler = Scheduler()

scheduler.add_task({
    "id": "NOOR-001",
    "title": "Research charcoal competitors",
    "skill": "competitor_analysis",
    "priority": 10
})

task = scheduler.next_task()

agent = scheduler.assign_agent(task)

print("Task:", task["title"])

if agent:
    print("Assigned Agent:", agent.name)
else:
    print("No suitable Agent found")
