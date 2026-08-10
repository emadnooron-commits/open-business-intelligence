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


scheduler = Scheduler()

scheduler.add_task({
    "id": "NOOR-001",
    "title": "Market Research",
    "priority": 10
})

scheduler.add_task({
    "id": "NOOR-002",
    "title": "Competitor Analysis",
    "priority": 8
})
