from pathlib import Path


# Project root:
# /workspaces/open-business-intelligence
ROOT = Path(__file__).resolve().parent.parent


def load_skill(skill_name):
    # Main skill directory
    skill_path = ROOT / "skills" / skill_name

    # The orchestrator manifest is stored separately
    manifest = ROOT / "orchestrator" / "skills" / skill_name / "manifest.yaml"

    # Skill instructions and schema
    instructions = skill_path / "skills" / skill_name / "SKILL.md"
    schema = skill_path / "schema.json"

    return {
        "manifest": manifest,
        "instructions": instructions,
        "schema": schema,
    }


def route(request):
    text = request.lower().strip()

    # Full analysis
    if "حلل المشروع" in text or "هل الفكرة قابلة للتنفيذ" in text:
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

    # Competitor analysis only
    if "منافسين" in text:
        return ["competitor-analysis"]

    # Market research only
    if "سوق" in text or "السوق" in text:
        return ["market-research"]

    # Feasibility only
    if "جدوى" in text:
        return ["feasibility-study"]

    # Default
    return ["idea-analysis"]


def inspect_skill(skill_name):
    files = load_skill(skill_name)

    return {
        "skill": skill_name,
        "manifest": str(files["manifest"]),
        "manifest_exists": files["manifest"].is_file(),
        "instructions": str(files["instructions"]),
        "instructions_exists": files["instructions"].is_file(),
        "schema": str(files["schema"]),
        "schema_exists": files["schema"].is_file(),
    }


def main():
    request = "حلل مشروع نور"

    skills = route(request)

    print("=== NOOR ORCHESTRATOR V1 ===")
    print("Project root:", ROOT)
    print("Request:", request)
    print()
    print("Skills:")

    for skill in skills:
        print()
        print("-", skill)

        result = inspect_skill(skill)

        print("  Manifest:")
        print("   ", result["manifest"])
        print("   exists:", result["manifest_exists"])

        print("  Instructions:")
        print("   ", result["instructions"])
        print("   exists:", result["instructions_exists"])

        print("  Schema:")
        print("   ", result["schema"])
        print("   exists:", result["schema_exists"])


if __name__ == "__main__":
    main()
