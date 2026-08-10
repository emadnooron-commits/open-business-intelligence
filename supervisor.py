class Supervisor:

    def review(self, result):

        if not result:
            return "RETRY"

        if result.get("validated") is True:
            return "APPROVED"

        if result.get("risk") == "HIGH":
            return "ESCALATE"

        return "RETRY"


supervisor = Supervisor()


result = {
    "validated": True,
    "risk": "LOW"
}

decision = supervisor.review(result)

print("Supervisor Decision:", decision)
