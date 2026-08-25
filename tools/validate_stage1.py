"""
validate_stage1.py — DSLC Stage 1 Quality Gate

Validates a generated Stage 1 Markdown document before rendering into Word/PDF.

Performs 15 comprehensive checks across structure, content, governance presentation,
and document quality without deciding governance status or inventing evidence.

Usage:
    python tools/validate_stage1.py stage1_draft.md

Exit codes:
    0 = PASS (no ERROR findings)
    1 = FAIL (one or more ERROR findings)
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


# ============================================================================
# TYPES
# ============================================================================

class Severity(Enum):
    ERROR   = "ERROR"
    WARNING = "WARNING"
    INFO    = "INFO"


@dataclass
class Finding:
    """A validation finding."""
    check_num: int
    severity: Severity
    location: str | None
    issue: str
    suggestion: str | None = None

    def __str__(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        sugg = f"\n    Suggestion: {self.suggestion}" if self.suggestion else ""
        return f"CHECK {self.check_num}: {self.issue}{loc}{sugg}"


# ============================================================================
# CONFIGURATION
# ============================================================================

# Expected high-level sections per the redesigned Stage 1 template.
# Appendices A/B/C are validated separately by CHECK 8.
MANDATORY_SECTIONS: dict[str, list[set[str]]] = {
    "Stage 1 Readiness": [
        {"stage 1 readiness"},
    ],
    "Business & Use Case": [
        {"business", "use case"},
        {"business & use case"},
    ],
    "Data Readiness": [
        {"data readiness"},
        {"data", "readiness"},
    ],
    "Exploratory Analysis": [
        {"exploratory analysis"},
        {"exploratory"},
    ],
    "Feature Engineering": [
        {"feature engineering"},
        {"feature", "engineering"},
    ],
    "Model Development & Validation": [
        {"model development"},
        {"model", "validation"},
    ],
    "Governance & Sign-off": [
        {"governance", "sign"},
        {"governance & sign-off"},
    ],
    "Risks & Limitations": [
        {"risks & limitations"},
        {"risks", "limitations"},
        {"risk"},
    ],
    "Stage 1 Recommendation": [
        {"stage 1 recommendation"},
        {"recommendation"},
    ],
}

# Old top-level headings that must not substitute for the redesigned structure.
# These are permitted only as subordinate content within new-structure sections.
OLD_TOPLEVEL_SECTIONS: list[str] = [
    "executive summary",
    "project overview",
    "stage 1 completion summary",
    "recommended next actions",
]

# Prohibited implementation-language phrases
PROHIBITED_PHRASES = [
    ("per YAML",        "Remove internal reference 'per YAML'."),
    ("YAML mandates",   "Remove internal reference 'YAML mandates'."),
    ("blocking=true",   "Remove YAML field reference 'blocking=true'."),
    ("required=false",  "Remove YAML field reference 'required=false'."),
    ("assertion type",  "Remove internal term 'assertion type'."),
]

# Patterns indicating agent-generated approval (not allowed)
UNSUPPORTED_APPROVAL_PATTERNS = [
    (r"agent\s+(approves?|has\s+approved|sign[- ]?off)",
     "Agent cannot approve. Remove agent approval claim."),
    (r"(approves?|approved\s+by)\s+(the\s+)?agent",
     "Agent cannot approve. Remove agent approval claim."),
    (r"copilot\s+(approves?|has\s+approved)",
     "Copilot cannot approve. Remove approval claim."),
    (r"AI\s+(approves?|has\s+approved|sign[- ]?off)",
     "AI cannot approve. Remove approval claim."),
    (r"this\s+document\s+is\s+(approved|signed(\s+off)?)",
     "Document is DRAFT. Only a human reviewer can approve."),
]

# Canonical governance requirements used by CHECK 5 requirement-level duplication.
# Each entry: (display_name, list_of_keywords — any one of which identifies the requirement).
CANONICAL_GOV_REQUIREMENTS: list[tuple[str, list[str]]] = [
    ("Business Review",             ["business review"]),
    ("Technical Review",            ["technical review"]),
    ("AI Inventory Registration",   ["ai inventory"]),
    ("Data Governance",             ["data governance"]),
    ("Deployment / Model Handover", ["deployment", "model handover", "handover"]),
    ("Technical Sign-off",          ["technical sign"]),
    ("Business Sign-off",           ["business sign"]),
    ("Final Stage 1 Sign-off",      ["final sign"]),
]

# Governance requirement names (used for heading-level checks)
GOVERNANCE_ITEMS = {
    "business review", "technical review", "ai inventory", "data governance",
    "deployment", "handover", "technical sign", "business sign", "final sign-off",
}


# ============================================================================
# MARKDOWN PARSING
# ============================================================================

def load_lines(path: Path) -> list[str]:
    """Load file lines."""
    return path.read_text(encoding="utf-8").splitlines()


def heading_text(line: str) -> str | None:
    """Extract heading text, returning None if not a heading."""
    m = re.match(r"^(#{1,6})\s+(.*)", line)
    if not m:
        return None
    text = m.group(2).strip()
    text = re.sub(r"\s*\{#[^}]+\}$", "", text)  # remove ID anchors
    return text


def heading_level(line: str) -> int | None:
    """Extract heading level (1-6) or None."""
    m = re.match(r"^(#{1,6})", line)
    return len(m.group(1)) if m else None


def parse_blocks(lines: list[str]) -> list[tuple[int, str, list[str]]]:
    """
    Parse lines into (level, heading_text, body_lines) blocks.
    Lines before the first heading are in a synthetic (0, '', body) block.
    """
    blocks: list[tuple[int, str, list[str]]] = []
    current_level = 0
    current_heading = ""
    current_body: list[str] = []

    for line in lines:
        lvl = heading_level(line)
        if lvl is not None:
            blocks.append((current_level, current_heading, current_body))
            current_level = lvl
            current_heading = heading_text(line) or ""
            current_body = []
        else:
            current_body.append(line)

    blocks.append((current_level, current_heading, current_body))
    return blocks


def substantive_lines(body: list[str]) -> list[str]:
    """Return non-empty, non-heading body lines."""
    return [ln for ln in body if ln.strip() and not heading_text(ln)]


# ============================================================================
# CHECK FUNCTIONS
# ============================================================================

def check_1_required_structure(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """
    CHECK 1 — Required high-level sections must exist per the redesigned template.
    Also flags old section labels used as top-level substitutes.
    """
    findings: list[Finding] = []

    # Verify each required section is present
    for section_name, keyword_sets in MANDATORY_SECTIONS.items():
        found = any(
            all(kw in heading.lower() for kw in ks)
            for _, heading, _ in blocks
            if heading
            for ks in keyword_sets
        )
        if not found:
            findings.append(Finding(
                check_num=1,
                severity=Severity.ERROR,
                location=section_name,
                issue=f"Required section '{section_name}' not found.",
                suggestion=(
                    f"Add a top-level heading for '{section_name}'. "
                    f"Numbering is permitted (e.g., '1. {section_name}')."
                ),
            ))

    # Flag old section labels used at H1/H2 level (redesigned sections must be used)
    for level, heading, _ in blocks:
        if level not in (1, 2) or not heading:
            continue
        heading_lower = heading.lower()
        for old_section in OLD_TOPLEVEL_SECTIONS:
            if old_section in heading_lower:
                findings.append(Finding(
                    check_num=1,
                    severity=Severity.WARNING,
                    location=heading,
                    issue=(
                        f"Heading '{heading}' uses an old Stage 1 structure label. "
                        f"Old sections must not substitute for redesigned top-level sections."
                    ),
                    suggestion=(
                        f"Use '{old_section.title()}' only as subordinate content within "
                        f"a redesigned section, not as a top-level heading."
                    ),
                ))

    return findings


def check_2_prohibited_language(lines: list[str]) -> list[Finding]:
    """CHECK 2 — Flag prohibited implementation-language phrases."""
    findings: list[Finding] = []
    for i, line in enumerate(lines, start=1):
        for phrase, sugg in PROHIBITED_PHRASES:
            if phrase.lower() in line.lower():
                findings.append(Finding(
                    check_num=2,
                    severity=Severity.ERROR,
                    location=f"Line {i}",
                    issue=f"Prohibited phrase '{phrase}' in reader-facing content.",
                    suggestion=sugg,
                ))
    return findings


def check_3_empty_sections(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """
    CHECK 3 — Flag empty sections (hierarchy-aware).

    A section passes when:
    - it has direct body content, OR
    - one of its actual child subsections has content.
    Content from unrelated sections (at equal or higher level) is never counted.
    """
    findings: list[Finding] = []
    for idx, (level, heading, body) in enumerate(blocks):
        if not heading or level == 0:
            continue
        if substantive_lines(body):
            continue  # has direct content — pass

        # Check only actual child subsections:
        # subsequent blocks with level > current level,
        # stopping when a block at level <= current level is reached.
        has_child_content = False
        for j in range(idx + 1, len(blocks)):
            child_level, _, child_body = blocks[j]
            if child_level <= level:
                break  # reached a sibling or ancestor — stop
            if substantive_lines(child_body):
                has_child_content = True
                break

        if not has_child_content:
            is_mandatory = any(
                all(kw in heading.lower() for kw in ks)
                for ks_list in MANDATORY_SECTIONS.values()
                for ks in ks_list
            )
            findings.append(Finding(
                check_num=3,
                severity=Severity.ERROR if is_mandatory else Severity.WARNING,
                location=heading,
                issue=f"Section '{heading}' is empty (no direct content or child subsection content).",
                suggestion="Add content or remove this heading.",
            ))
    return findings


def check_4_pending_explanation(
    blocks: list[tuple[int, str, list[str]]],
    lines: list[str],
) -> list[Finding]:
    """CHECK 4 — Verify PENDING items have gap/reason and next action."""
    findings: list[Finding] = []
    pending_lines = [i for i, ln in enumerate(lines, start=1) if "pending" in ln.lower()]
    for line_num in pending_lines:
        current_line = lines[line_num - 1].lower()
        
        # For table rows (contain |), extract the entire row
        if "|" in current_line:
            row_text = current_line
            cells = [c.strip() for c in current_line.split("|")]
            # Count actual content cells (excluding empty before/after pipes)
            content_cells = [c for c in cells if c]
            
            # In a comprehensive governance table: | Item | Status | Evidence | Action |
            # In a simple bullet list: | Item | Status description |
            is_comprehensive_table = len(content_cells) >= 4
            
            if is_comprehensive_table:
                # For governance tables: col[0]=Requirement, col[1]=Status,
                # col[2]=Evidence/Gap, col[3]=Required Action.
                # Check specific columns, not the whole row.
                gap_text    = content_cells[2] if len(content_cells) > 2 else ""
                action_text = content_cells[3] if len(content_cells) > 3 else ""

                # Evidence/Gap: must be more than a trivial placeholder
                _TRIVIAL_GAP = {"—", "-", "n/a", "tbc", "none", "nil", ""}
                gap_stripped = gap_text.strip()
                has_gap = (
                    len(gap_stripped) > 7
                    and gap_stripped.lower() not in _TRIVIAL_GAP
                    and not re.match(r"^-+$", gap_stripped)
                )

                # Required Action: must contain an actionable verb
                _ACTIONABLE_VERBS = {
                    "confirm", "obtain", "register", "provide", "complete",
                    "establish", "review", "approve", "verif", "document",
                    "schedule", "submit", "request", "arrange", "ensure",
                    "create", "prepare", "clarify", "produce", "must",
                }
                has_action = any(v in action_text.lower() for v in _ACTIONABLE_VERBS)
            else:
                # For simple tables (< 4 cols), check ALL cells after the first
                # for gap keywords. The gap may be in any non-requirement column.
                combined_status = " ".join(content_cells[1:] if len(content_cells) > 1 else content_cells)
                has_gap = any(kw in combined_status for kw in {
                    "gap", "missing", "no ", "none", "marked", "assumed", "cannot",
                    "lacks", "not demonstrated", "not confirmed", "not available",
                    "not found", "no evidence", "none found", "absent",
                })
                # Action is implicit for simple PENDING rows
                has_action = True
        else:
            # For non-table content, look at surrounding context
            start_idx = max(0, line_num - 4)
            end_idx = min(len(lines), line_num + 2)
            row_text = "\n".join(lines[start_idx:end_idx]).lower()
            has_gap = any(kw in row_text for kw in {
                "gap", "missing", "no evidence", "not found", "none found",
                "marked as", "assumed", "cannot", "lacks",
                "not demonstrated", "not confirmed", "no registration", "no ",
            })
            has_action = any(kw in row_text for kw in {
                "next action", "required action", "must", "obtain", "confirm",
                "produce", "register", "provide", "complete", "establish",
            })

        if not has_gap:
            findings.append(Finding(
                check_num=4,
                severity=Severity.ERROR,
                location=f"Line {line_num}",
                issue="PENDING without explaining what is missing or the gap.",
                suggestion="Add the evidence gap or reason why PENDING.",
            ))
        if not has_action:
            findings.append(Finding(
                check_num=4,
                severity=Severity.WARNING,
                location=f"Line {line_num}",
                issue="PENDING without explicit next action.",
                suggestion="Add action needed to resolve (e.g., 'obtain', 'register', 'confirm').",
            ))
    return findings


def check_5_unique_governance_presentation(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """
    CHECK 5 — Detect full governance requirement presentations in multiple major sections.

    The authoritative full presentation (Status + Evidence/Gap + Required Action)
    for each canonical requirement must appear only under 'Governance & Sign-off'.
    A brief reference or summary elsewhere is acceptable.
    A full presentation is detected when a table row contains 3+ meaningful cells
    that reference the requirement.
    """
    findings: list[Finding] = []

    def _major_section_for(target_idx: int) -> str:
        """Return the most recent H1/H2 heading before block at target_idx."""
        for j in range(target_idx - 1, -1, -1):
            lvl, hdg, _ = blocks[j]
            if lvl in (1, 2) and hdg:
                return hdg.lower()
        return ""

    for req_name, keywords in CANONICAL_GOV_REQUIREMENTS:
        full_presentations: list[str] = []  # major section headings where full presentation found

        for idx, (level, heading, body) in enumerate(blocks):
            body_text = "\n".join(body)
            if not body_text.strip():
                continue

            # Check if this block references the requirement at all
            body_lower = body_text.lower()
            heading_lower = (heading or "").lower()
            req_mentioned = any(kw in body_lower or kw in heading_lower for kw in keywords)
            if not req_mentioned:
                continue

            # Detect a full presentation: a table row that contains the requirement
            # keyword AND has 3+ meaningful cells (Status + Evidence + Action)
            table_rows = re.findall(r"\|([^\n]+)\|", body_text)
            for row in table_rows:
                cells = [c.strip() for c in row.split("|")]
                cells = [c for c in cells if c]
                if len(cells) < 3:
                    continue
                row_lower = row.lower()
                if not any(kw in row_lower for kw in keywords):
                    continue
                meaningful = sum(1 for c in cells if len(c) > 8)
                if meaningful >= 3:
                    section = _major_section_for(idx)
                    if section and section not in full_presentations:
                        full_presentations.append(section)

        # Flag if full presentation found in multiple distinct major sections
        gov_sections     = [s for s in full_presentations if "governance" in s or "sign" in s]
        non_gov_sections = [s for s in full_presentations if s not in gov_sections]

        for sect in non_gov_sections:
            if gov_sections:  # authoritative copy exists in Governance & Sign-off
                findings.append(Finding(
                    check_num=5,
                    severity=Severity.ERROR,
                    location=f"'{req_name}' in '{sect}'",
                    issue=(
                        f"Governance requirement '{req_name}' has a full "
                        f"Status/Evidence/Action presentation outside 'Governance & Sign-off'."
                    ),
                    suggestion=(
                        "Keep the authoritative entry in 'Governance & Sign-off' only. "
                        "Use a brief reference or summary row elsewhere."
                    ),
                ))

    return findings


def _count_stage1_requirements() -> int | None:
    """
    Count unique Stage 1 requirements from knowledge/stage1_requirements.yaml
    using regex on raw text (no YAML library required).
    Returns count, or None if the file is unavailable.
    """
    yaml_path = Path(__file__).parent.parent / "knowledge" / "stage1_requirements.yaml"
    if not yaml_path.exists():
        return None
    try:
        content = yaml_path.read_text(encoding="utf-8")
        # Requirement-level id entries are indented at 6 spaces: "      - id:"
        ids = re.findall(r"^      - id:", content, re.MULTILINE)
        return len(ids) if ids else None
    except Exception:
        return None


def check_6_requirement_counting(lines: list[str]) -> list[Finding]:
    """
    CHECK 6 — Validate reported numeric counts against the YAML-derived requirement total.
    Flags counts that exceed the number of unique Stage 1 requirements.
    Also flags bare 'N PENDING' dashboard metrics without a unique-requirement basis.
    """
    findings: list[Finding] = []
    combined    = "\n".join(lines)
    req_total   = _count_stage1_requirements()   # 21 from current YAML

    # Count patterns: "7 PENDING", "12 complete", "20 requirements"
    count_patterns = re.findall(
        r"\b(\d+)\s+(pending|complete|applicable|requirements?)\b",
        combined,
        re.IGNORECASE,
    )
    seen_counts: set[str] = set()
    for count_str, item_type in count_patterns:
        count = int(count_str)
        dedup_key = f"{count_str}:{item_type.lower()}"
        if dedup_key in seen_counts:
            continue
        seen_counts.add(dedup_key)

        if req_total is not None and count > req_total:
            findings.append(Finding(
                check_num=6,
                severity=Severity.ERROR,
                location=f"{count_str} {item_type}",
                issue=(
                    f"Reported count '{count} {item_type}' exceeds the {req_total} "
                    f"unique Stage 1 requirements defined in stage1_requirements.yaml."
                ),
                suggestion=(
                    "Counts must not exceed the number of unique applicable requirements. "
                    "Check for double-counting or incorrect aggregation."
                ),
            ))
        elif req_total is None and count > 100:
            findings.append(Finding(
                check_num=6,
                severity=Severity.WARNING,
                location=f"{count_str} {item_type}",
                issue=f"Reported count '{count} {item_type}' is implausibly large.",
                suggestion="Ensure counts represent unique DSLC requirements.",
            ))

    # Flag bare 'N PENDING' used as a dashboard metric
    dashboard_re = re.compile(r"\b(\d+)\s+PENDING\b", re.IGNORECASE)
    for i, line in enumerate(lines, start=1):
        m = dashboard_re.search(line)
        if m:
            findings.append(Finding(
                check_num=6,
                severity=Severity.WARNING,
                location=f"Line {i}",
                issue=(
                    f"Dashboard metric '{m.group(0)}' used without a unique-requirement basis. "
                    "Prefer qualitative readiness status in executive sections."
                ),
                suggestion=(
                    "Replace numeric counts with qualitative status "
                    "(e.g., 'Some governance items outstanding'). "
                    "Reserve requirement counts for the Governance & Sign-off table."
                ),
            ))

    return findings


_FILE_EXT_PATTERN = re.compile(
    r"\.(ipynb|md|pdf|docx|py|csv|pkl|json|xlsx|txt)\b",
    re.IGNORECASE,
)


def _parse_md_table(body_lines: list[str]) -> list[list[str]]:
    """Parse Markdown table lines from a block body into rows of cells."""
    rows: list[list[str]] = []
    for ln in body_lines:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[-| :]+\|$", s):  # separator row
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        rows.append(cells)
    return rows


def check_7_dashboard_field_integrity(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """
    CHECK 7 — Structurally parse the Readiness Summary table.
    Status cells must contain qualitative readiness assessments,
    not filenames, notebook names, or filesystem paths.
    """
    findings: list[Finding] = []
    seen: set[str] = set()   # deduplicate findings

    for level, heading, body in blocks:
        if not heading:
            continue
        if not (
            "readiness" in heading.lower()
            or "executive summary" in heading.lower()
            or ("summary" in heading.lower() and level <= 3)
        ):
            continue

        table_rows = _parse_md_table(body)
        if not table_rows:
            continue

        # Identify header row
        first = table_rows[0]
        has_header = any(c.lower() in {"area", "status", "summary", "section"} for c in first)
        data_rows  = table_rows[1:] if has_header else table_rows

        # Status column is typically index 1 (second column)
        for row in data_rows:
            if len(row) < 2:
                continue
            status_cell = row[1]

            ext_match = _FILE_EXT_PATTERN.search(status_cell)
            if ext_match:
                key = f"{heading}:{status_cell[:60]}"
                if key not in seen:
                    seen.add(key)
                    findings.append(Finding(
                        check_num=7,
                        severity=Severity.ERROR,
                        location=heading,
                        issue=(
                            f"Status cell contains a file reference: '{status_cell[:80]}'. "
                            f"Status must be a qualitative readiness assessment."
                        ),
                        suggestion=(
                            "Move evidence filenames to Appendix A (Evidence Register). "
                            "Use only: COMPLETE, PENDING, NOT APPLICABLE, RISK ACCEPTED, or DRAFT."
                        ),
                    ))

            allowed_statuses = {
                "COMPLETE",
                "PENDING",
                "NOT APPLICABLE",
                "RISK ACCEPTED",
                "DRAFT",
            }
            normalised_status = status_cell.strip().upper()
            if normalised_status and not ext_match and normalised_status not in allowed_statuses:
                key = f"{heading}:invalid-status:{normalised_status}"
                if key not in seen:
                    seen.add(key)
                    findings.append(Finding(
                        check_num=7,
                        severity=Severity.ERROR,
                        location=heading,
                        issue=(
                            f"Unsupported readiness status: '{status_cell}'. "
                            "Dashboard status must use the governance vocabulary."
                        ),
                        suggestion=(
                            "Use only: COMPLETE, PENDING, NOT APPLICABLE, "
                            "RISK ACCEPTED, or DRAFT."
                        ),
                    ))

    return findings


# Required appendices in canonical order
_REQUIRED_APPENDICES: list[tuple[str, str]] = [
    ("A", "evidence register"),
    ("B", "data sources"),
    ("C", "model technical detail"),
]


def check_8_appendix_order_uniqueness(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """
    CHECK 8 — Require exactly one of each appendix (A, B, C), in correct order,
    with correct content keywords. Detects missing, duplicated, malformed, and
    out-of-order appendices.
    """
    findings: list[Finding] = []

    # Collect all appendix headings with their block index
    appendix_entries: list[tuple[int, str, str]] = []  # (block_idx, letter, heading)
    for idx, (level, heading, body) in enumerate(blocks):
        if not heading:
            continue
        m = re.match(r"appendix\s+([a-z])\b", heading.lower())
        if m:
            letter = m.group(1).upper()
            appendix_entries.append((idx, letter, heading))

    # Flag malformed headings (word duplication)
    for _, letter, heading in appendix_entries:
        key_words = re.findall(
            r"\b(appendix|evidence\s+register|data\s+sources|model\s+technical)\b",
            heading.lower(),
        )
        if len(key_words) != len(set(key_words)):
            findings.append(Finding(
                check_num=8,
                severity=Severity.ERROR,
                location=heading,
                issue=f"Appendix heading contains duplicated text: '{heading}'.",
                suggestion="Remove the repeated words from the heading.",
            ))

    # Check each required appendix: presence, uniqueness, keyword
    for req_letter, req_keyword in _REQUIRED_APPENDICES:
        matches = [(idx, h) for idx, l, h in appendix_entries if l == req_letter]

        if not matches:
            findings.append(Finding(
                check_num=8,
                severity=Severity.ERROR,
                location=f"Appendix {req_letter}",
                issue=f"Required Appendix {req_letter} ({req_keyword.title()}) is missing.",
                suggestion=(
                    f"Add 'Appendix {req_letter} — {req_keyword.title()}' as a section "
                    f"after the main report and any preceding appendices."
                ),
            ))
            continue

        if len(matches) > 1:
            findings.append(Finding(
                check_num=8,
                severity=Severity.ERROR,
                location=f"Appendix {req_letter}",
                issue=(
                    f"Appendix {req_letter} appears {len(matches)} times "
                    f"(must appear exactly once)."
                ),
                suggestion="Consolidate into a single appendix entry.",
            ))

        for _, h in matches:
            if req_keyword not in h.lower():
                findings.append(Finding(
                    check_num=8,
                    severity=Severity.ERROR,
                    location=h,
                    issue=(
                        f"Appendix {req_letter} heading does not identify '{req_keyword}': '{h}'."
                    ),
                    suggestion=(
                        f"Heading should read 'Appendix {req_letter} — {req_keyword.title()}' "
                        f"(or similar)."
                    ),
                ))

    # Enforce ordering: A before B before C
    letter_positions: dict[str, int] = {}
    for idx, letter, _ in appendix_entries:
        if letter not in letter_positions:
            letter_positions[letter] = idx

    for earlier, later in [("A", "B"), ("B", "C"), ("A", "C")]:
        if earlier in letter_positions and later in letter_positions:
            if letter_positions[earlier] > letter_positions[later]:
                findings.append(Finding(
                    check_num=8,
                    severity=Severity.ERROR,
                    location=f"Appendix {later} before Appendix {earlier}",
                    issue=(
                        f"Appendix {later} appears before Appendix {earlier}. "
                        f"Required order: A → B → C."
                    ),
                    suggestion=f"Move Appendix {later} to after Appendix {earlier}.",
                ))

    return findings


def check_9_repeated_actions(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """CHECK 9 — Detect materially identical next-action rows across sections."""
    findings: list[Finding] = []
    action_sections: list[tuple[str, str]] = []

    for level, heading, body in blocks:
        if heading and ("action" in heading.lower() or "recommendation" in heading.lower()):
            body_text = "\n".join(body)
            # Extract table rows
            rows = re.findall(r"\|\s*(.+?)\s*\|", body_text)
            for row in rows:
                norm = re.sub(r"\s+", " ", row.lower().strip())
                if len(norm) > 30:
                    action_sections.append((heading, norm))

    # Check for duplicates
    for i, (sect_a, norm_a) in enumerate(action_sections):
        for sect_b, norm_b in action_sections[i + 1:]:
            if norm_a == norm_b and sect_a != sect_b:
                findings.append(Finding(
                    check_num=9,
                    severity=Severity.WARNING,
                    location=f"{sect_a} vs {sect_b}",
                    issue="Same action appears in multiple sections.",
                    suggestion="Keep in one authoritative location; reference it elsewhere.",
                ))
    return findings


# Risk-acceptance patterns — definitive ERROR (must not auto-pass on soft words)
_RISK_ERROR_PATTERNS: list[str] = [
    r"risk\s+accepted\b",
    r"accepted\s+operationally\b",
]

# Ambiguous 'accepted' in risk context — WARNING
_RISK_AMBIGUOUS_RE = re.compile(r"(?<![a-z])accepted(?![a-z])", re.IGNORECASE)

# Strong authorised-evidence patterns: must name a real human/record/decision.
# 'known', 'documented', 'confirmed', 'date', 'per' are NOT sufficient.
_RISK_STRONG_EVIDENCE_RE = re.compile(
    r"(approved\s+by\s+\w"
    r"|risk\s+owner\s*[:=]\s*\w"
    r"|risk\s+(register|record|log|board)"
    r"|(sign[- ]?off|approval)\s+(by|from)\s+\w"
    r"|approver\s*[:=]\s*\w"
    r"|reviewer\s*[:=]\s*\w)",
    re.IGNORECASE,
)


def check_10_risk_acceptance_language(lines: list[str]) -> list[Finding]:
    """
    CHECK 10 — Flag risk-acceptance wording without explicit authorised evidence.

    'risk accepted' or 'accepted operationally' = ERROR unless the SAME entry
    contains explicit authorised evidence (named approver, risk record, decision).
    Ambiguous 'accepted' in a risk/limitation context = WARNING.

    Words such as 'known', 'documented', 'confirmed', 'date', 'per' are
    NOT treated as authorised evidence.
    """
    findings: list[Finding] = []
    in_risk_section = False

    for i, line in enumerate(lines, start=1):
        # Track current section context
        h = heading_text(line)
        if h is not None:
            in_risk_section = any(
                kw in h.lower() for kw in ("risk", "limitation", "constraint")
            )

        # ERROR: definitive risk-acceptance phrases
        for pattern in _RISK_ERROR_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                has_strong = bool(_RISK_STRONG_EVIDENCE_RE.search(line))
                if has_strong:
                    findings.append(Finding(
                        check_num=10,
                        severity=Severity.INFO,
                        location=f"Line {i}",
                        issue="Risk-acceptance wording with possible authorised evidence marker.",
                        suggestion=(
                            "Ensure the approver name, role, and decision date are clearly "
                            "documented alongside this entry."
                        ),
                    ))
                else:
                    findings.append(Finding(
                        check_num=10,
                        severity=Severity.ERROR,
                        location=f"Line {i}",
                        issue=(
                            f"Risk-acceptance wording without authorised evidence: "
                            f"'{line.strip()[:80]}'."
                        ),
                        suggestion=(
                            "Replace with 'Known limitation', 'Documented constraint', "
                            "'Current operating approach', or 'Mitigation required'. "
                            "Do not imply acceptance without a named approver and decision record."
                        ),
                    ))

        # WARNING: ambiguous 'accepted' in risk/limitation context only
        if in_risk_section and _RISK_AMBIGUOUS_RE.search(line):
            already_flagged = any(
                re.search(p, line, re.IGNORECASE) for p in _RISK_ERROR_PATTERNS
            )
            if not already_flagged:
                findings.append(Finding(
                    check_num=10,
                    severity=Severity.WARNING,
                    location=f"Line {i}",
                    issue=(
                        f"Ambiguous use of 'accepted' in risk context: "
                        f"'{line.strip()[:80]}'."
                    ),
                    suggestion=(
                        "Clarify whether this is an authorised risk decision or a known limitation. "
                        "Prefer 'Known limitation' or 'Current operating approach'."
                    ),
                ))

    return findings


def check_11_main_body_technical_detail(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """CHECK 11 — Warn if main body contains excessive technical identifiers."""
    findings: list[Finding] = []
    for level, heading, body in blocks:
        if heading and "appendix" in heading.lower():
            break
        body_text = "\n".join(body)
        # Count long identifiers
        bq_ids = len(re.findall(r"`[a-z0-9._-]{20,}`", body_text))
        paths = len(re.findall(r"[a-z0-9_/]{20,}\.(pkl|csv|json)", body_text, re.IGNORECASE))
        if bq_ids > 3 or paths > 2:
            findings.append(Finding(
                check_num=11,
                severity=Severity.WARNING,
                location=heading or "Main body",
                issue=f"Extensive technical identifiers in main report.",
                suggestion="Move long dataset IDs, file paths and feature lists to Appendices B or C.",
            ))
    return findings


def check_12_evidence_register_integrity(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """CHECK 12 — Verify Evidence Register exists and is complete."""
    findings: list[Finding] = []
    evidence_blocks = [
        body for level, heading, body in blocks
        if heading and "evidence" in heading.lower() and "register" in heading.lower()
    ]

    if len(evidence_blocks) == 0:
        findings.append(Finding(
            check_num=12,
            severity=Severity.ERROR,
            location="Document",
            issue="No Evidence Register found.",
            suggestion="Add 'Appendix A: Evidence Register' with table mapping requirements to sources.",
        ))
    elif len(evidence_blocks) > 1:
        findings.append(Finding(
            check_num=12,
            severity=Severity.ERROR,
            location="Multiple Evidence Registers",
            issue="Multiple Evidence Registers found (should be exactly one).",
            suggestion="Consolidate into a single Evidence Register.",
        ))

    # Check that major requirements have entries
    for body in evidence_blocks:
        body_text = "\n".join(body).lower()
        if "validation" not in body_text or "governance" not in body_text:
            findings.append(Finding(
                check_num=12,
                severity=Severity.WARNING,
                location="Evidence Register",
                issue="Evidence Register may be incomplete.",
                suggestion="Ensure all major Stage 1 requirements have entries.",
            ))
    return findings


def check_13_unsupported_approval_wording(lines: list[str]) -> list[Finding]:
    """CHECK 13 — Flag agent-generated approval or sign-off claims."""
    findings: list[Finding] = []
    for i, line in enumerate(lines, start=1):
        for pattern, sugg in UNSUPPORTED_APPROVAL_PATTERNS:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                findings.append(Finding(
                    check_num=13,
                    severity=Severity.ERROR,
                    location=f"Line {i}",
                    issue=f"Agent-generated approval claim: '{m.group(0)}'.",
                    suggestion=sugg,
                ))
    return findings


def check_14_document_length(
    blocks: list[tuple[int, str, list[str]]],
) -> list[Finding]:
    """CHECK 14 — Estimate main body size and warn if unusually long."""
    findings: list[Finding] = []
    main_lines = 0
    for level, heading, body in blocks:
        if heading and "appendix" in heading.lower():
            break
        main_lines += len(substantive_lines(body))

    # Heuristic: ~45 lines per rendered page
    est_pages = max(1, main_lines // 45)
    if est_pages > 15:
        findings.append(Finding(
            check_num=14,
            severity=Severity.WARNING,
            location="Main report",
            issue=f"Main report is estimated ~{est_pages} pages (target: 8-12 before appendices).",
            suggestion="Consider moving detailed technical content to appendices.",
        ))
    return findings


def check_15_basic_completeness(
    blocks: list[tuple[int, str, list[str]]],
    lines: list[str],
) -> list[Finding]:
    """CHECK 15 — Basic completeness: readiness statement, governance status, actions."""
    findings: list[Finding] = []
    combined = "\n".join(lines).lower()

    if "overall" not in combined or "readiness" not in combined:
        findings.append(Finding(
            check_num=15,
            severity=Severity.WARNING,
            location="Document",
            issue="No explicit 'overall readiness' statement found.",
            suggestion="Add a clear statement about Stage 1 readiness.",
        ))

    if "next action" not in combined and "recommended" not in combined:
        findings.append(Finding(
            check_num=15,
            severity=Severity.WARNING,
            location="Document",
            issue="No section explicitly titled 'Next Actions' or 'Recommendations'.",
            suggestion="Add a clear section listing outstanding items.",
        ))

    if combined.count("pending") < 1 and combined.count("complete") < 1:
        findings.append(Finding(
            check_num=15,
            severity=Severity.WARNING,
            location="Document",
            issue="No governance statuses (PENDING, COMPLETE, etc.) detected.",
            suggestion="Add explicit status labels to governance items.",
        ))
    return findings


# ============================================================================
# MAIN
# ============================================================================

def run_all_checks(lines: list[str]) -> tuple[list[Finding], list[Finding], list[Finding]]:
    """
    Run all 15 checks and return (errors, warnings, infos).
    """
    blocks = parse_blocks(lines)
    all_findings: list[Finding] = []

    # Run all checks
    all_findings.extend(check_1_required_structure(blocks))
    all_findings.extend(check_2_prohibited_language(lines))
    all_findings.extend(check_3_empty_sections(blocks))
    all_findings.extend(check_4_pending_explanation(blocks, lines))
    all_findings.extend(check_5_unique_governance_presentation(blocks))
    all_findings.extend(check_6_requirement_counting(lines))
    all_findings.extend(check_7_dashboard_field_integrity(blocks))
    all_findings.extend(check_8_appendix_order_uniqueness(blocks))
    all_findings.extend(check_9_repeated_actions(blocks))
    all_findings.extend(check_10_risk_acceptance_language(lines))
    all_findings.extend(check_11_main_body_technical_detail(blocks))
    all_findings.extend(check_12_evidence_register_integrity(blocks))
    all_findings.extend(check_13_unsupported_approval_wording(lines))
    all_findings.extend(check_14_document_length(blocks))
    all_findings.extend(check_15_basic_completeness(blocks, lines))

    # Sort by severity
    errors   = [f for f in all_findings if f.severity == Severity.ERROR]
    warnings = [f for f in all_findings if f.severity == Severity.WARNING]
    infos    = [f for f in all_findings if f.severity == Severity.INFO]

    return errors, warnings, infos


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python tools/validate_stage1.py <stage1_markdown_file>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    lines = load_lines(path)
    errors, warnings, infos = run_all_checks(lines)

    # Report
    print("=" * 70)
    print("DSLC STAGE 1 VALIDATION")
    print("=" * 70)
    print()

    passed = len(errors) == 0
    result = "PASS" if passed else "FAIL"
    print(f"Result: {result}\n")

    if errors:
        print("ERRORS:")
        for finding in errors:
            print(f"  {finding}")
            print()

    if warnings:
        print("WARNINGS:")
        for finding in warnings:
            print(f"  {finding}")
            print()

    if infos:
        print("INFO:")
        for finding in infos:
            print(f"  {finding}")
            print()

    print("=" * 70)
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info")
    print("=" * 70)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()