from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEMPLATE_PATH = (
    PROJECT_ROOT
    / "templates"
    / "model_card_template.html"
)

DATA_PATH = (
    PROJECT_ROOT
    / "output"
    / "model_card_data.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "Model_Card.html"
)

REVIEW_PATH = (
    PROJECT_ROOT
    / "output"
    / "model_card_review.md"
)


# ============================================================
# CONSTANTS
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}

ARTEFACT_TYPE_LABELS = {
    "shap_plot": "SHAP summary plot",
    "feature_importance_plot": "Feature-importance plot",
    "numeric_feature_importance_table": "Numeric feature-importance table",
    "user_graphic": "User-provided explainability graphic",
}


# ============================================================
# BASIC HELPERS
# ============================================================

def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Model Card data file was not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "Model Card data must be a JSON object."
        )

    return data


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"Model Card template was not found: {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


def safe_text(value: object) -> str:
    if value is None:
        return "PENDING"

    text = str(value).strip()

    if not text:
        return "PENDING"

    return html.escape(text)


def parse_float(value: Any) -> float | None:
    if value in (
        None,
        "",
        "PENDING",
    ):
        return None

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return None


def parse_bool(value: Any) -> bool:
    if isinstance(
        value,
        bool,
    ):
        return value

    if isinstance(
        value,
        str,
    ):
        return value.strip().lower() in {
            "true",
            "1",
            "yes",
            "y",
        }

    if isinstance(
        value,
        (
            int,
            float,
        ),
    ):
        return value != 0

    return False


def is_pending(value: Any) -> bool:
    if value is None:
        return True

    return str(
        value
    ).strip().upper() in {
        "",
        "PENDING",
    }


# ============================================================
# TARGET
# ============================================================

def build_target_display(
    data: dict,
) -> dict[str, str]:

    technical_reference = safe_text(
        data.get("target")
    )

    business_description = data.get(
        "target_business_description"
    )

    approved = parse_bool(
        data.get(
            "target_business_description_approved"
        )
    )

    if (
        approved
        and not is_pending(
            business_description
        )
    ):
        return {
            "target_business_description":
                safe_text(
                    business_description
                ),
            "target_business_class":
                "",
            "target_technical_reference":
                technical_reference,
        }

    return {
        "target_business_description":
            "PENDING",
        "target_business_class":
            "pending",
        "target_technical_reference":
            technical_reference,
    }


# ============================================================
# ROC AUC
# ============================================================

def get_roc_visuals(
    roc_auc: float | None,
) -> dict[str, str]:

    if roc_auc is None:
        return {
            "roc_auc_display":
                "PENDING",
            "roc_auc_circle_style":
                (
                    "background: #9ca3af; "
                    "color: #ffffff;"
                ),
            "roc_auc_interpretation":
                "PENDING",
        }

    display = (
        f"{round(roc_auc * 100)}%"
    )

    if roc_auc < 0.60:
        color = "#c62828"
        interpretation = (
            "Limited discrimination"
        )

    elif roc_auc < 0.70:
        color = "#ef6c00"
        interpretation = (
            "Moderate discrimination"
        )

    elif roc_auc < 0.80:
        color = "#8e24aa"
        interpretation = (
            "Good discrimination"
        )

    elif roc_auc < 0.90:
        color = "#1565c0"
        interpretation = (
            "Strong discrimination"
        )

    else:
        color = "#2e7d32"
        interpretation = (
            "Excellent discrimination"
        )

    return {
        "roc_auc_display":
            display,
        "roc_auc_circle_style":
            (
                "background: "
                "radial-gradient("
                "circle at 30% 28%, "
                "#ffffff33, "
                f"{color}"
                "); "
                "color: #ffffff;"
            ),
        "roc_auc_interpretation":
            interpretation,
    }


# ============================================================
# EXPLAINABILITY
# ============================================================

def normalize_artefact_type(
    raw_type: Any,
) -> str | None:

    if raw_type is None:
        return None

    canonical = (
        str(raw_type)
        .strip()
        .lower()
        .replace(
            "-",
            "_",
        )
        .replace(
            " ",
            "_",
        )
    )

    mapping = {
        "shap":
            "shap_plot",
        "shap_plot":
            "shap_plot",
        "shap_summary":
            "shap_plot",
        "shap_summary_plot":
            "shap_plot",

        "feature_importance_plot":
            "feature_importance_plot",

        "featureimportanceplot":
            "feature_importance_plot",

        "numeric_feature_importance_table":
            "numeric_feature_importance_table",

        "feature_importance_table":
            "numeric_feature_importance_table",

        "user_provided_png_or_jpg_explainability_graphic":
            "user_graphic",

        "user_provided_graphic":
            "user_graphic",

        "user_graphic":
            "user_graphic",
    }

    return mapping.get(
        canonical
    )


def normalize_feature_table(
    raw_table: Any,
) -> list[dict[str, Any]]:

    if not isinstance(
        raw_table,
        list,
    ):
        return []

    normalized = []

    for row in raw_table:

        if not isinstance(
            row,
            dict,
        ):
            continue

        name = (
            row.get("name")
            or row.get("feature")
            or row.get("column")
        )

        raw_importance = (
            row.get("importance")
            if row.get(
                "importance"
            ) is not None
            else row.get("score")
            if row.get(
                "score"
            ) is not None
            else row.get("value")
        )

        importance = parse_float(
            raw_importance
        )

        if (
            name is None
            or importance is None
        ):
            continue

        normalized.append(
            {
                "name":
                    str(name),

                "importance":
                    importance,
            }
        )

    return normalized


def normalize_image_source(
    raw_source: Any,
) -> str | None:

    if raw_source is None:
        return None

    source = str(
        raw_source
    ).strip()

    if not source:
        return None

    if (
        source.startswith(
            "http://"
        )
        or source.startswith(
            "https://"
        )
    ):
        suffix = Path(
            source.split(
                "?",
                1,
            )[0]
        ).suffix.lower()

        if (
            suffix
            in ALLOWED_IMAGE_EXTENSIONS
        ):
            return source

        return None

    candidate = Path(
        source
    )

    if not candidate.is_absolute():
        candidate = (
            PROJECT_ROOT
            / candidate
        ).resolve()

    if (
        not candidate.exists()
        or candidate.suffix.lower()
        not in ALLOWED_IMAGE_EXTENSIONS
    ):
        return None

    return candidate.as_uri()


def normalize_explainability_artefacts(
    data: dict,
) -> list[dict[str, Any]]:

    explainability = data.get(
        "explainability",
        {},
    )

    if not isinstance(
        explainability,
        dict,
    ):
        return []

    raw_artefacts = (
        explainability.get(
            "artefacts",
            [],
        )
    )

    if not isinstance(
        raw_artefacts,
        list,
    ):
        return []

    normalized = []

    for index, raw in enumerate(
        raw_artefacts,
        start=1,
    ):

        if not isinstance(
            raw,
            dict,
        ):
            continue

        artefact_type = (
            normalize_artefact_type(
                raw.get("type")
            )
        )

        if artefact_type is None:
            continue

        item = {
            "id":
                str(
                    raw.get("id")
                    or f"artefact_{index}"
                ),

            "type":
                artefact_type,

            "type_label":
                ARTEFACT_TYPE_LABELS[
                    artefact_type
                ],

            "source":
                str(
                    raw.get("source")
                    or "Project evidence"
                ),

            "caption":
                str(
                    raw.get("caption")
                    or ""
                ),

            "approved":
                (
                    parse_bool(
                        raw.get(
                            "approved_by_user"
                        )
                    )
                    or parse_bool(
                        raw.get(
                            "selected_by_user"
                        )
                    )
                ),
        }

        if (
            artefact_type
            ==
            "numeric_feature_importance_table"
        ):

            if not parse_bool(
                raw.get("verified")
            ):
                continue

            rows = (
                normalize_feature_table(
                    raw.get("table")
                    or raw.get("rows")
                    or raw.get("features")
                )
            )

            if not rows:
                continue

            item["table_rows"] = rows

            normalized.append(
                item
            )

            continue

        image_source = (
            normalize_image_source(
                raw.get("path")
                or raw.get("image")
                or raw.get("src")
            )
        )

        if image_source is None:
            continue

        item["image_src"] = (
            image_source
        )

        normalized.append(
            item
        )

    return normalized


def select_explainability_artefact(
    data: dict,
    artefacts: list[dict[str, Any]],
) -> tuple[
    str,
    dict[str, Any] | None,
]:

    if not artefacts:
        return (
            "PENDING",
            None,
        )

    explainability = data.get(
        "explainability",
        {},
    )

    selected_id = None

    if isinstance(
        explainability,
        dict,
    ):
        selected_id = (
            explainability.get(
                "selected_artefact_id"
            )
        )

    if selected_id:

        matches = [
            artefact
            for artefact
            in artefacts
            if artefact["id"]
            == str(
                selected_id
            )
        ]

        if len(
            matches
        ) == 1:
            return (
                "SELECTED",
                matches[0],
            )

    approved = [
        artefact
        for artefact
        in artefacts
        if artefact.get(
            "approved"
        )
    ]

    if len(
        approved
    ) == 1:
        return (
            "SELECTED",
            approved[0],
        )

    if len(
        approved
    ) > 1:
        return (
            "SELECTION REQUIRED",
            None,
        )

    if len(
        artefacts
    ) == 1:
        return (
            "SELECTED",
            artefacts[0],
        )

    return (
        "SELECTION REQUIRED",
        None,
    )


def create_feature_rows(
    features: list[dict[str, Any]],
) -> str:

    if not features:
        return (
            '<p class="pending">'
            'PENDING — No verified '
            'feature-importance values '
            'available.'
            '</p>'
        )

    maximum = max(
        float(
            feature[
                "importance"
            ]
        )
        for feature
        in features
    )

    if maximum <= 0:
        maximum = 1

    rows = []

    for feature in features:

        name = safe_text(
            feature.get(
                "name"
            )
        )

        importance = float(
            feature[
                "importance"
            ]
        )

        width = max(
            2.0,
            round(
                (
                    importance
                    / maximum
                )
                * 100,
                1,
            ),
        )

        rows.append(
            f"""
            <div class="feature-row">

                <div class="feature-name">
                    {name}
                </div>

                <div class="bar-track">

                    <div
                        class="bar"
                        style="width: {width}%;">

                    </div>

                </div>

                <div class="feature-score">
                    {importance:g}
                </div>

            </div>
            """
        )

    return "\n".join(
        rows
    )


def build_available_options_html(
    artefacts: list[dict[str, Any]],
) -> str:

    if not artefacts:
        return ""

    rows = []

    for artefact in artefacts:

        rows.append(
            "<li>"
            f"ID: "
            f"{safe_text(artefact['id'])}"
            " | "
            f"Type: "
            f"{safe_text(artefact['type_label'])}"
            " | "
            f"Source: "
            f"{safe_text(artefact['source'])}"
            "</li>"
        )

    return (
        '<ul class="options-list">'
        + "".join(
            rows
        )
        + "</ul>"
    )


def build_explainability_display(
    data: dict,
) -> dict[str, str]:

    artefacts = (
        normalize_explainability_artefacts(
            data
        )
    )

    status, selected = (
        select_explainability_artefact(
            data,
            artefacts,
        )
    )

    options = (
        build_available_options_html(
            artefacts
        )
    )

    if status == "PENDING":

        return {
            "status":
                (
                    '<span '
                    'class="status-pending">'
                    'PENDING'
                    '</span>'
                ),

            "type":
                (
                    '<span '
                    'class="pending">'
                    'PENDING'
                    '</span>'
                ),

            "source":
                (
                    '<span '
                    'class="pending">'
                    'PENDING'
                    '</span>'
                ),

            "visual":
                "",

            "caption":
                "",

            "options":
                "",

            "details":
                """
                <div class="explainability-empty-state">

                    <h3>
                        Explainability evidence
                        has not yet been supplied
                    </h3>

                    <p>
                        Provide one valid artefact
                        to populate this section:
                    </p>

                    <ul>
                        <li>
                            SHAP summary plot
                        </li>

                        <li>
                            Feature-importance plot
                        </li>

                        <li>
                            Verified numeric
                            feature-importance table
                        </li>

                        <li>
                            User-provided PNG or JPG
                            explainability graphic
                        </li>
                    </ul>

                    <p class="empty-state-note">
                        The agent will not create
                        or infer explainability values.
                    </p>

                </div>
                """,
        }

    if (
        status
        ==
        "SELECTION REQUIRED"
    ):

        return {
            "status":
                (
                    '<span '
                    'class="status-selection-required">'
                    'SELECTION REQUIRED'
                    '</span>'
                ),

            "type":
                (
                    '<span '
                    'class="pending">'
                    'PENDING'
                    '</span>'
                ),

            "source":
                (
                    '<span '
                    'class="pending">'
                    'PENDING'
                    '</span>'
                ),

            "visual":
                "",

            "caption":
                (
                    "Multiple valid explainability "
                    "artefacts are available. "
                    "User selection is required."
                ),

            "options":
                options,

            "details":
                "",
        }

    assert (
        selected
        is not None
    )

    if (
        selected["type"]
        ==
        "numeric_feature_importance_table"
    ):

        visual = ""

        details = (
            create_feature_rows(
                selected.get(
                    "table_rows",
                    [],
                )
            )
        )

    else:

        visual = (
            '<img '
            'class="explainability-image" '
            f'src="{html.escape(selected["image_src"])}" '
            f'alt="{html.escape(selected["type_label"])}">'
        )

        details = ""

    return {
        "status":
            (
                '<span '
                'class="status-selected">'
                'SELECTED'
                '</span>'
            ),

        "type":
            safe_text(
                selected[
                    "type_label"
                ]
            ),

        "source":
            safe_text(
                selected[
                    "source"
                ]
            ),

        "visual":
            visual,

        "caption":
            safe_text(
                selected.get(
                    "caption"
                )
                or (
                    "Selected explainability "
                    "evidence: "
                    f"{selected['type_label']}."
                )
            ),

        "options":
            options,

        "details":
            details,
    }


# ============================================================
# REVIEW POSITION
# ============================================================

def determine_review_position(
    data: dict,
) -> str:

    required_fields = (
        "model_name",
        "model_type",
        "model_description",
        "owner",
        "target",
        "target_business_description",
        "eligibility",
    )

    if any(
        is_pending(
            data.get(
                field
            )
        )
        for field
        in required_fields
    ):
        return (
            "NOT READY FOR APPROVAL"
        )

    if not parse_bool(
        data.get(
            "target_business_description_approved"
        )
    ):
        return (
            "NOT READY FOR APPROVAL"
        )

    governance_status = (
        str(
            data.get(
                "governance_status",
                "DRAFT",
            )
        )
        .strip()
        .upper()
    )

    if (
        governance_status
        !=
        "COMPLETE"
    ):
        return (
            "NOT READY FOR APPROVAL"
        )

    explainability = (
        build_explainability_display(
            data
        )
    )

    status_text = (
        explainability[
            "status"
        ]
    )

    if (
        "PENDING"
        in status_text
        or
        "SELECTION REQUIRED"
        in status_text
    ):
        return (
            "NOT READY FOR APPROVAL"
        )

    return (
        "READY FOR REVIEW"
    )


# ============================================================
# MODEL CARD
# ============================================================

def build_model_card(
    template: str,
    data: dict,
) -> str:

    target = (
        build_target_display(
            data
        )
    )

    roc = (
        get_roc_visuals(
            parse_float(
                data.get(
                    "roc_auc"
                )
            )
        )
    )

    explainability = (
        build_explainability_display(
            data
        )
    )

    review_position = (
        determine_review_position(
            data
        )
    )

    owner = safe_text(
        data.get(
            "owner"
        )
    )

    owner_class = (
        "pending"
        if owner.upper()
        == "PENDING"
        else ""
    )

    replacements = {

        "{{MODEL_NAME}}":
            safe_text(
                data.get(
                    "model_name"
                )
            ),

        "{{VERSION}}":
            safe_text(
                data.get(
                    "version"
                )
            ),

        "{{MODEL_TYPE}}":
            safe_text(
                data.get(
                    "model_type"
                )
            ),

        "{{MODEL_TYPE_CONTEXT}}":
            safe_text(
                data.get(
                    "model_type_context"
                )
            ),

        "{{MODEL_DESCRIPTION}}":
            safe_text(
                data.get(
                    "model_description"
                )
            ),

        "{{TARGET_BUSINESS_DESCRIPTION}}":
            target[
                "target_business_description"
            ],

        "{{TARGET_BUSINESS_CLASS}}":
            target[
                "target_business_class"
            ],

        "{{TARGET_TECHNICAL_REFERENCE}}":
            target[
                "target_technical_reference"
            ],

        "{{ELIGIBILITY}}":
            safe_text(
                data.get(
                    "eligibility"
                )
            ),

        "{{OWNER}}":
            owner,

        "{{OWNER_CLASS}}":
            owner_class,

        "{{ROC_AUC_DISPLAY}}":
            roc[
                "roc_auc_display"
            ],

        "{{ROC_AUC_CIRCLE_STYLE}}":
            roc[
                "roc_auc_circle_style"
            ],

        "{{ROC_AUC_INTERPRETATION}}":
            safe_text(
                roc[
                    "roc_auc_interpretation"
                ]
            ),

        "{{STATISTICS_NOTE}}":
            safe_text(
                data.get(
                    "statistics_note"
                )
            ),

        "{{GOVERNANCE_STATUS}}":
            safe_text(
                str(
                    data.get(
                        "governance_status",
                        "DRAFT",
                    )
                ).upper()
            ),

        "{{REVIEW_POSITION}}":
            safe_text(
                review_position
            ),

        "{{EXPLAINABILITY_STATUS}}":
            explainability[
                "status"
            ],

        "{{EXPLAINABILITY_TYPE}}":
            explainability[
                "type"
            ],

        "{{EXPLAINABILITY_SOURCE}}":
            explainability[
                "source"
            ],

        "{{EXPLAINABILITY_VISUAL}}":
            explainability[
                "visual"
            ],

        "{{EXPLAINABILITY_CAPTION}}":
            explainability[
                "caption"
            ],

        "{{EXPLAINABILITY_AVAILABLE_OPTIONS}}":
            explainability[
                "options"
            ],

        "{{EXPLAINABILITY_DETAILS}}":
            explainability[
                "details"
            ],
    }

    result = template

    for (
        placeholder,
        value,
    ) in replacements.items():

        result = result.replace(
            placeholder,
            value,
        )

    if (
        "{{"
        in result
        or
        "}}"
        in result
    ):
        raise ValueError(
            "Unresolved Model Card "
            "template placeholders remain."
        )

    return result


# ============================================================
# REVIEW MARKDOWN
# ============================================================

def render_review_markdown(
    data: dict,
) -> str:

    def section(
        title: str,
        values: Any,
    ) -> str:

        if (
            not isinstance(
                values,
                list,
            )
            or not values
        ):
            return (
                f"## {title}\n\n"
                "None recorded.\n"
            )

        lines = [
            f"## {title}",
            "",
        ]

        for value in values:

            if isinstance(
                value,
                dict,
            ):
                text = (
                    value.get(
                        "summary"
                    )
                    or value.get(
                        "item"
                    )
                    or json.dumps(
                        value
                    )
                )

            else:
                text = str(
                    value
                )

            lines.append(
                f"- {text}"
            )

        lines.append(
            ""
        )

        return "\n".join(
            lines
        )

    return (
        "# Model Card Review\n\n"

        "Draft for human review. "
        "The generated Model Card "
        "does not constitute governance "
        "approval or sign-off.\n\n"

        + section(
            "Evidence Summary",
            data.get(
                "evidence_summary"
            ),
        )

        + "\n"

        + section(
            "Missing Fields",
            data.get(
                "missing_fields"
            ),
        )

        + "\n"

        + section(
            "Recommended Actions",
            data.get(
                "recommended_actions"
            ),
        )
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    data = load_json(
        DATA_PATH
    )

    template = load_template(
        TEMPLATE_PATH
    )

    completed_html = (
        build_model_card(
            template,
            data,
        )
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        completed_html,
        encoding="utf-8",
    )

    REVIEW_PATH.write_text(
        render_review_markdown(
            data
        ),
        encoding="utf-8",
    )

    print(
        "Model Card HTML generated:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        "Model Card review generated:"
    )

    print(
        REVIEW_PATH
    )


if __name__ == "__main__":
    main()