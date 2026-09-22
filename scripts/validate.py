"""Validate the public package with Python's standard library only."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "audit-delivery",
    "certify-delivery",
    "verified-backup-before-edit",
    "non-destructive-autonomy",
    "reproduce-before-fixing",
    "claim-evidence-table",
    "test-tenant-isolation",
    "brief-a-subagent",
    "stop-repeating-rounds",
)
AGENTS = ("adversarial-reviewer",)
REQUIRED = (
    "README.md",
    "PUBLISHING.md",
    "LICENSE",
    "docs/agents.md",
    "examples/calculator/README.md",
    "examples/calculator/requirements.md",
    "examples/calculator/calculator.py",
    "examples/calculator/test_calculator.py",
    "examples/calculator/team-claim.md",
    "examples/calculator/expected-analysis.md",
    "examples/safe-change/README.md",
    "examples/safe-change/app.py",
    "examples/safe-change/test_app.py",
    "examples/safe-change/archive-note.txt",
    "examples/safe-change/expected-behavior.md",
    "examples/misleading-error/README.md",
    "examples/misleading-error/report.py",
    "examples/misleading-error/test_report.py",
    "examples/misleading-error/orders.json",
    "examples/misleading-error/expected-analysis.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    ".github/workflows/validate.yml",
    "skills/verified-backup-before-edit/scripts/backup_file.py",
    "tests/test_backup_file.py",
)
TEXT_SUFFIXES = {".md", ".py", ".txt", ".json", ".yml", ""}
PERSONAL_PATH = re.compile(
    r"(?i)(?:[a-z]:[/\\]users[/\\][^/\\\s]+|/home/[^/\s]+|/Users/[^/\s]+)"
)


def validate() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing file: {relative}")

    entries = [(name, ROOT / "skills" / name / "SKILL.md") for name in SKILLS]
    entries += [(name, ROOT / "agents" / f"{name}.md") for name in AGENTS]
    for name, path in entries:
        if not path.is_file():
            errors.append(f"Missing skill or agent: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
        if not frontmatter:
            errors.append(f"Invalid frontmatter: {path.relative_to(ROOT)}")
            continue
        metadata = frontmatter.group(1)
        if not re.search(rf"(?m)^name:[ \t]*{re.escape(name)}[ \t]*$", metadata):
            errors.append(f"Wrong skill name: {name}")
        if not re.search(r"(?m)^description:[ \t]*\S.*$", metadata):
            errors.append(f"Missing description: {name}")

    for folder, allowed in (("skills", set(SKILLS)), ("agents", set(AGENTS))):
        found = {
            path.parent.name if folder == "skills" else path.stem
            for path in (ROOT / folder).glob("*/SKILL.md" if folder == "skills" else "*.md")
        }
        for name in sorted(found - allowed):
            errors.append(f"Unlisted {folder[:-1]}: {name}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in TEXT_SUFFIXES:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue  # The path-detection expression matches its own source text.
        content = path.read_text(encoding="utf-8")
        if PERSONAL_PATH.search(content):
            errors.append(f"Personal path in {path.relative_to(ROOT)}")

    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        raise SystemExit(1)
    print("Package structure and public-text checks passed.")
