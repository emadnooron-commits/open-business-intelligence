class Agent:

    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def can_do(self, skill):
        return skill in self.skills


research_agent = Agent(
    "Research Agent",
    [
        "market_research",
        "competitor_analysis"
    ]
)
