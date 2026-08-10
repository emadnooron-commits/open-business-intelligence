from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent.parent


def load_skill(skill_name):
    skill_path = ROOT / "skills" / skill_name

    manifest = skill_path / "manifest.yaml"
    instructions = skill_path / "skills" / skill_name / "SKILL.md"
    schema = skill_path / "schema.json"

    return {
        "manifest": manifest,
        "instructions": instructions,
        "schema": schema,
    }


def route(request):
    text = request.lower()

    if "حلل المشروع" in text or "قابل للتنفيذ" in text:
        return [
            "idea-analysis",
            "market-research",
            "competitor-analysis",
            "feasibility-study",
            "financial-analysis",
            "risk-analysis",
            "recommendation-engine",
            "report-builder",
        ]

    if "منافسين" in text:
        return ["competitor-analysis"]

    if "سوق" in text:
        return ["market-research"]

    if "جدوى" in text:
        return ["feasibility-study"]

    return ["idea-analysis"]


def inspect_skill(skill_name):
    files = load_skill(skill_name)

    return {
        "skill": skill_name,
        "manifest_exists": files["manifest"].exists(),
        "instructions_exists": files["instructions"].exists(),
        "schema_exists": files["schema"].exists(),
    }


if __name__ == "__main__":
    request = "حلل مشروع نور"

    skills = route(request)

    print("=== NOOR ORCHESTRATOR V1 ===")
    print("Request:", request)
    print("Skills:")

    for skill in skills:
        print("-", skill)
        print(inspect_skill(skill))
