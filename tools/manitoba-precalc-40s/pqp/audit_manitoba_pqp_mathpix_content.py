#!/usr/bin/env python3
"""Audit generated Manitoba Mathpix PQP content."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from manitoba_mathpix_common import MB_DIR


ROOT = MB_DIR / "derived" / "pqp-mathpix"
PQP_DIR = ROOT / "pqp"
REPORT_JSON = ROOT / "content-audit-report.json"
REPORT_MD = ROOT / "content-audit-report.md"


VISIBLE_ARTIFACT_PATTERNS: dict[str, re.Pattern[str]] = {
    "remote_mathpix_image_reference": re.compile(r"https://cdn\.mathpix\.com"),
    "visible_latex_figure_artifact": re.compile(
        r"\\begin\{figure\}|\\end\{figure\}|labelformat=empty|\{figure\}", re.I
    ),
    "visible_latex_includegraphics": re.compile(r"\\includegraphics", re.I),
    "raw_alignment_ampersand": re.compile(r"(?<!\\)&"),
    "upright_space_nobreak_artifact": re.compile(r"upright\(space\.nobreak", re.I),
    "dollar_artifact": re.compile(r"\$dollar\b", re.I),
    "double_comma_math_artifact": re.compile(r",,,"),
    "escaped_slash_artifact": re.compile(r"\\/"),
    "plus_minus_text_artifact": re.compile(r"plus\.minus", re.I),
}

IMAGE_REF_RE = re.compile(r'#image\("assets/([^"]+)"')
LINE_START_CHOICE_RE = re.compile(r"(^|\n)\s*(?:a|b|c|d|с)[\).]\s+", re.I)
MATH_WORD_RE = re.compile(r"[A-Za-z]{2,}")
MATH_STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"')
KNOWN_TYPST_MATH_WORDS = {
    "abs",
    "alpha",
    "and",
    "bb",
    "beta",
    "bullet",
    "ceil",
    "cos",
    "cot",
    "csc",
    "degree",
    "delta",
    "divides",
    "dot",
    "exp",
    "floor",
    "for",
    "frac",
    "gamma",
    "if",
    "in",
    "lim",
    "ln",
    "log",
    "lr",
    "max",
    "min",
    "mod",
    "not",
    "oo",
    "or",
    "pi",
    "pm",
    "quad",
    "root",
    "sec",
    "sect",
    "sin",
    "sqrt",
    "tan",
    "text",
    "therefore",
    "theta",
    "times",
    "underline",
    "union",
    "upright",
    "where",
}


def normalize_text(text: str) -> str:
    text = re.sub(r"#image\([^)]*\)", " ", text)
    text = re.sub(r"[^A-Za-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def looks_like_appendix_outcome_table(text: str) -> bool:
    norm = normalize_text(text)
    has_table_headers = "question learning outcome mark" in norm
    has_units = len(re.findall(r"\bunit\s+[a-z]\b", norm)) >= 2
    has_curriculum_headers = any(
        phrase in norm
        for phrase in (
            "trigonometric equations and identities",
            "exponents and logarithms",
            "radicals and rationals",
            "learning outcomes",
        )
    )
    return has_table_headers and (has_units or has_curriculum_headers)


def snippet(text: str, limit: int = 220) -> str:
    return re.sub(r"\s+", " ", text).strip()[:limit]


def content_fields(question: dict[str, Any], *, include_extensions: bool = False) -> list[tuple[str, str]]:
    content = question.get("content") if isinstance(question.get("content"), dict) else {}
    fields: list[tuple[str, str]] = []
    for field_name in ("stem", "solution"):
        block = content.get(field_name)
        if isinstance(block, dict):
            fields.append((field_name, str(block.get("text") or "")))
            if include_extensions:
                extensions = block.get("extensions")
                if isinstance(extensions, dict):
                    fields.append((f"{field_name}.latexSource", str(extensions.get("latexSource") or "")))
    choices = content.get("choices") if isinstance(content.get("choices"), list) else []
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        choice_id = str(choice.get("id") or "?")
        body = choice.get("body")
        if isinstance(body, dict):
            fields.append((f"choice.{choice_id}", str(body.get("text") or "")))
            if include_extensions:
                extensions = body.get("extensions")
                if isinstance(extensions, dict):
                    fields.append((f"choice.{choice_id}.latexSource", str(extensions.get("latexSource") or "")))
    return fields


def math_spans(text: str) -> list[str]:
    spans: list[str] = []
    index = 0
    while index < len(text):
        if text[index] != "$" or (index > 0 and text[index - 1] == "\\"):
            index += 1
            continue
        end = index + 1
        while end < len(text):
            if text[end] == "$" and text[end - 1] != "\\":
                break
            end += 1
        if end >= len(text):
            index += 1
            continue
        spans.append(text[index + 1 : end])
        index = end + 1
    return spans


def bare_multiletter_math_words(text: str) -> list[str]:
    words: list[str] = []
    for span in math_spans(text):
        scrubbed = MATH_STRING_RE.sub('""', span)
        for word in MATH_WORD_RE.findall(scrubbed):
            if word not in KNOWN_TYPST_MATH_WORDS and word not in words:
                words.append(word)
    return words


def asset_filenames(package: dict[str, Any]) -> set[str]:
    filenames: set[str] = set()
    for asset in package.get("assets", []):
        if not isinstance(asset, dict):
            continue
        filename = asset.get("filename")
        if isinstance(filename, str):
            filenames.add(filename)
        storage = asset.get("storage")
        if isinstance(storage, dict):
            path = storage.get("path")
            if isinstance(path, str) and path.startswith("assets/"):
                filenames.add(path.removeprefix("assets/"))
    return filenames


def question_records(
    package_id: str,
    package_dir: Path,
    package_assets: set[str],
    question: dict[str, Any],
) -> list[dict[str, Any]]:
    qid = str(question.get("id", ""))
    kind = str(question.get("kind", ""))
    content = question.get("content") if isinstance(question.get("content"), dict) else {}
    stem = content.get("stem", {}).get("text", "") if isinstance(content.get("stem"), dict) else ""
    solution = content.get("solution", {}).get("text", "") if isinstance(content.get("solution"), dict) else ""
    solution_ext = content.get("solution", {}).get("extensions", {}) if isinstance(content.get("solution"), dict) else {}
    solution_source = solution_ext.get("source") if isinstance(solution_ext, dict) else None
    choices = content.get("choices") if isinstance(content.get("choices"), list) else []

    records: list[dict[str, Any]] = []
    def add(issue: str, field: str, detail: str) -> None:
        records.append(
            {
                "issue": issue,
                "package": package_id,
                "questionId": qid,
                "field": field,
                "detail": detail,
            }
        )

    if looks_like_appendix_outcome_table(solution):
        add("appendix_outcome_table_used_as_solution", "solution", snippet(solution))
    if looks_like_appendix_outcome_table(stem):
        add("appendix_outcome_table_used_in_stem", "stem", snippet(stem))
    if solution_source == "unmatched":
        add("solution_unmatched", "solution", "")
    if not solution.strip():
        add("solution_empty", "solution", "")
    if re.search(r"\bQuestion\s+\d+\b", stem):
        add("question_marker_visible_in_stem", "stem", snippet(stem))
    if kind == "mcq" and len(choices) != 4:
        add("mcq_choices_not_structured", "content", f"{len(choices)} choices")
    if kind == "mcq" and question.get("answer", {}).get("value") not in {"A", "B", "C", "D"}:
        add("mcq_missing_or_bad_answer", "answer", str(question.get("answer")))
    if kind == "mcq" and LINE_START_CHOICE_RE.search(stem):
        add("mcq_choice_label_embedded_in_stem", "stem", snippet(stem))

    classification = question.get("classification") if isinstance(question.get("classification"), dict) else {}
    if classification.get("classId") != "pre-calculus-40s":
        add("curriculum_class_missing_or_wrong", "classification", str(classification.get("classId")))
    curriculum = classification.get("extensions", {}).get("curriculum") if isinstance(classification.get("extensions"), dict) else {}
    if not isinstance(curriculum, dict) or not curriculum.get("primaryOutcomeCode"):
        add("curriculum_outcome_missing", "classification", "")

    stem_norm = normalize_text(stem)
    solution_norm = normalize_text(solution)
    if len(stem_norm) > 80 and stem_norm in solution_norm:
        add("solution_repeats_full_question_body", "solution", snippet(solution))

    for field, text in content_fields(question):
        for issue, pattern in VISIBLE_ARTIFACT_PATTERNS.items():
            if pattern.search(text):
                add(issue, field, snippet(text))
        for match in IMAGE_REF_RE.finditer(text):
            filename = match.group(1)
            if filename not in package_assets:
                add("image_reference_not_declared", field, filename)
            if not (package_dir / "assets" / filename).exists():
                add("image_reference_missing_local_file", field, filename)
        bare_words = bare_multiletter_math_words(text)
        if bare_words:
            add("bare_multiletter_math_identifier", field, ", ".join(bare_words[:12]))

    return records


def main() -> None:
    package_paths = sorted(PQP_DIR.glob("*/**/*.pqp.json"))
    records: list[dict[str, Any]] = []
    package_count = 0
    question_count = 0
    diagnostics_count: Counter[str] = Counter()
    info_count: Counter[str] = Counter()
    stem_groups: dict[tuple[str, str], list[str]] = defaultdict(list)

    for path in package_paths:
        package = json.loads(path.read_text(encoding="utf-8"))
        package_id = path.parent.name
        package_assets = asset_filenames(package)
        package_count += 1
        questions = package.get("questions", [])
        question_count += len(questions)
        for diagnostic in package.get("diagnostics", []):
            if isinstance(diagnostic, dict):
                diagnostics_count[str(diagnostic.get("code", "unknown"))] += 1
        for question in questions:
            content = question.get("content") if isinstance(question.get("content"), dict) else {}
            solution = content.get("solution") if isinstance(content.get("solution"), dict) else {}
            solution_ext = solution.get("extensions") if isinstance(solution.get("extensions"), dict) else {}
            if isinstance(solution_ext, dict) and solution_ext.get("source") == "source-pdf-text":
                info_count["solution_source_pdf_fallback"] += 1
            records.extend(question_records(package_id, path.parent, package_assets, question))
            stem = content.get("stem", {}).get("text", "") if isinstance(content.get("stem"), dict) else ""
            stem_norm = normalize_text(stem)
            if stem_norm:
                stem_groups[(package_id, stem_norm)].append(str(question.get("id")))

    for (package_id, _), ids in stem_groups.items():
        if len(ids) <= 1:
            continue
        for qid in ids:
            records.append(
                {
                    "issue": "duplicate_stem_group",
                    "package": package_id,
                    "questionId": qid,
                    "field": "stem",
                    "detail": ", ".join(ids),
                }
            )

    summary = Counter(record["issue"] for record in records)
    by_issue_package: dict[str, dict[str, int]] = defaultdict(dict)
    for record in records:
        issue = record["issue"]
        package = record["package"]
        by_issue_package[issue][package] = by_issue_package[issue].get(package, 0) + 1

    report = {
        "root": PQP_DIR.relative_to(MB_DIR.parent).as_posix(),
        "packages": package_count,
        "questions": question_count,
        "summary": dict(sorted(summary.items())),
        "infoSummary": dict(sorted(info_count.items())),
        "diagnosticsSummary": dict(sorted(diagnostics_count.items())),
        "byIssuePackage": {key: dict(sorted(value.items())) for key, value in sorted(by_issue_package.items())},
        "records": records,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Manitoba PQP Content Audit",
        "",
        f"Packages scanned: {package_count}",
        f"Questions scanned: {question_count}",
        "",
        "## Summary",
    ]
    if summary:
        for issue, count in sorted(summary.items()):
            lines.append(f"- {issue}: {count}")
    else:
        lines.append("- No issues found.")
    lines.extend(["", "## Info Summary"])
    if info_count:
        for issue, count in sorted(info_count.items()):
            lines.append(f"- {issue}: {count}")
    else:
        lines.append("- No informational counts.")
    lines.extend(["", "## Diagnostics Summary"])
    if diagnostics_count:
        for code, count in sorted(diagnostics_count.items()):
            lines.append(f"- {code}: {count}")
    else:
        lines.append("- No diagnostics found.")
    lines.extend(["", "## Issue Details"])
    for issue, count in sorted(summary.items()):
        lines.extend(["", f"### {issue} ({count})"])
        package_counts = by_issue_package[issue]
        package_summary = ", ".join(f"{package}={value}" for package, value in sorted(package_counts.items()))
        lines.append(f"Packages: {package_summary}")
        for record in [record for record in records if record["issue"] == issue][:50]:
            detail = f": {record['detail']}" if record.get("detail") else ""
            lines.append(f"- {record['package']} {record['questionId']} [{record['field']}]{detail}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(REPORT_JSON), "summary": report["summary"]}, indent=2))


if __name__ == "__main__":
    main()
