from pathlib import Path
import json
import jsonschema


ROOT = Path(__file__).resolve().parent.parent


def load_skill(skill_name):
    skill_path = ROOT / "skills" / skill_name

    manifest = ROOT / "orchestrator" / "skills" / skill_name / "manifest.yaml"
    instructions = skill_path / "skills" / skill_name / "SKILL.md"
    schema = skill_path / "schema.json"

    return {
        "manifest": manifest,
        "instructions": instructions,
        "schema": schema,
    }


def route(request):
    text = request.lower().strip()

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

    if "منافسين" in text:
        return ["competitor-analysis"]

    if "سوق" in text or "السوق" in text:
        return ["market-research"]

    if "جدوى" in text:
        return ["feasibility-study"]

    return ["idea-analysis"]


def load_schema(skill_name):
    files = load_skill(skill_name)

    with open(files["schema"], "r", encoding="utf-8") as file:
        return json.load(file)


def load_instructions(skill_name):
    files = load_skill(skill_name)

    with open(files["instructions"], "r", encoding="utf-8") as file:
        return file.read()


def validate_input(skill_name, data):
    schema = load_schema(skill_name)

    input_schema = schema

    jsonschema.validate(
        instance=data,
        schema=input_schema
    )


def create_dry_run_output(input_data):
    idea = input_data["idea"]

    return {
        "idea_summary": idea,
        "problem_statement": (
            "This is a first-pass dry-run analysis. "
            "The actual problem statement must be validated "
            "through the idea-analysis skill."
        ),
        "value_proposition": (
            "For the target customer, the proposed business "
            "aims to transform the identified idea into "
            "valuable products or services."
        ),
        "target_segments": [
            input_data.get(
                "target_customer",
                "Not specified"
            )
        ],
        "assumptions": [
            {
                "assumption": (
                    "The business idea has sufficient "
                    "market and operational potential."
                ),
                "confidence": "low",
                "needs_validation_by": "market-research"
            }
        ],
        "open_questions": [
            "What is the validated market demand?",
            "What are the main competitors?",
            "What are the expected production costs?",
            "What regulations apply?"
        ],
        "risks_preview": [
            "Market demand may differ from initial assumptions.",
            "Raw material availability may vary.",
            "Regulatory requirements may affect implementation."
        ],
        "recommended_next_skills": [
            "market-research",
            "competitor-analysis",
            "feasibility-study"
        ]
    }


def validate_output(skill_name, data):
    schema = load_schema(skill_name)

    output_schema = schema.get("output")

    if output_schema is None:
        raise ValueError(
            "The skill schema does not contain an 'output' schema."
        )

    jsonschema.validate(
        instance=data,
        schema=output_schema
    )


def save_artifact(skill_name, data):
    artifact_dir = (
        ROOT
        / "artifacts"
        / skill_name
    )

    artifact_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = artifact_dir / "data.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    return output_file


def run_skill(skill_name, input_data):
    print()
    print(f"=== RUNNING SKILL: {skill_name} ===")

    files = load_skill(skill_name)

    print("Manifest:", files["manifest"])
    print("Instructions:", files["instructions"])
    print("Schema:", files["schema"])

    if not files["manifest"].is_file():
        raise FileNotFoundError(
            f"Manifest not found: {files['manifest']}"
        )

    if not files["instructions"].is_file():
        raise FileNotFoundError(
            f"SKILL.md not found: {files['instructions']}"
        )

    if not files["schema"].is_file():
        raise FileNotFoundError(
            f"Schema not found: {files['schema']}"
        )

    print("✓ Skill files found")

    print("✓ Validating input...")
    validate_input(skill_name, input_data)

    print("✓ Input is valid")

    instructions = load_instructions(skill_name)

    print(
        f"✓ SKILL.md loaded ({len(instructions)} characters)"
    )

    print("✓ Creating dry-run output...")

    output = create_dry_run_output(input_data)

    print("✓ Validating output...")
    validate_output(skill_name, output)

    print("✓ Output is valid")

    artifact = save_artifact(
        skill_name,
        output
    )

    print("✓ Artifact saved:")
    print(artifact)

    return output


def main():
    request = "حلل مشروع نور"

    input_data = {
        "idea": (
            "شركة نور تريد بناء مجموعة صناعية مصرية "
            "تعتمد على تحويل المخلفات الزراعية إلى "
            "منتجات ذات قيمة اقتصادية، تبدأ بالفحم النباتي "
            "وفحم الشواء المضغوط، ثم تتوسع إلى الفحم النشط "
            "وخل الخشب والطاقة الحيوية والمنتجات الخشبية "
            "ومنتجات أخرى من المخلفات الزراعية."
        ),
        "location": "Egypt",
        "target_customer": (
            "مطاعم ومحلات الشواء والموزعون "
            "والأسواق المحلية وأسواق التصدير"
        ),
        "known_constraints": (
            "البداية من مصر؛ الاعتماد على المخلفات "
            "الزراعية؛ منتجات قابلة للتوسع والتصدير؛ "
            "البدء بالفحم ثم التوسع تدريجيًا"
        )
    }

    print("=== NOOR ORCHESTRATOR V1 ===")
    print("Project root:", ROOT)
    print("Request:", request)

    skills = route(request)

    print()
    print("Skills selected:")

    for skill in skills:
        print("-", skill)

    # V1 test: execute only the first skill.
    first_skill = skills[0]

    run_skill(
        first_skill,
        input_data
    )


if __name__ == "__main__":
    main()
