from pathlib import Path


BANNED_TERMS = {
    "文化路夜市": "文化路商圈",
    "嘉義市中心夜市區": "文化路周邊",
    "嘉義著名夜市觀光區": "文化路商圈",
}

# These files intentionally document banned terms, avoid_terms, replacement rules,
# or review instructions. They are not public-facing dashboard content.
ALLOWLIST_FILES = {
    Path("docs/local_terminology_style_guide.md"),
    Path("docs/local_terms_validation_rules.md"),
    Path("docs/local_place_dictionary.md"),
    Path("docs/local_place_dictionary_expansion_plan.md"),
    Path("docs/place_name_review_sheet.md"),
    Path("docs/codex_local_terms_instruction.md"),
    Path("docs/pr_review_guide.md"),
    Path("docs/ci_quality_gate_plan.md"),
    Path("dashboard/data/local_place_dictionary.json"),
}

SCAN_PATTERNS = [
    "dashboard/**/*.html",
    "dashboard/data/*.json",
    "docs/*.md",
    "data/sample/*.csv",
    "data/processed/*.csv",
    "reports/**/*.md",
    "reports/**/*.json",
    "reports/**/*.html",
]


def iter_target_files(repo_root: Path):
    seen = set()
    for pattern in SCAN_PATTERNS:
        for path in repo_root.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(repo_root)
            if relative in ALLOWLIST_FILES:
                continue
            if relative in seen:
                continue
            seen.add(relative)
            yield relative, path


def test_public_facing_files_do_not_use_banned_local_terms():
    repo_root = Path(__file__).resolve().parents[1]
    violations = []

    for relative, path in iter_target_files(repo_root):
        text = path.read_text(encoding="utf-8")
        for banned_term, suggested_replacement in BANNED_TERMS.items():
            if banned_term in text:
                violations.append(
                    f"- {relative} contains banned term: {banned_term}\n"
                    f"  Suggested replacement: {suggested_replacement}"
                )

    assert not violations, "Local terminology validation failed:\n" + "\n".join(violations)
