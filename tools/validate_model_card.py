from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_GOVERNANCE_STATUSES = {
    "COMPLETE",
    "PENDING",
    "NOT APPLICABLE",
    "RISK ACCEPTED",
    "DRAFT",
}

ALLOWED_ARTEFACT_TYPES = {
    "shap_plot",
    "feature_importance_plot",
    "numeric_feature_importance_table",
    "user_graphic",
}

REQUIRED_KEYS = {
    "model_name",
    "version",
    "model_type",
    "target",
    "target_business_description",
    "target_business_description_approved",
    "eligibility",
    "owner",
    "roc_auc",
    "statistics_note",
    "model_type_context",
    "model_description",
    "governance_status",
    "explainability",
    "evidence_summary",
    "missing_fields",
    "recommended_actions",
}


def load_json(
    path: Path,
) -> dict:

    if not path.exists():

        raise FileNotFoundError(
            f"Model Card data file "
            f"not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(
            file
        )

    if not isinstance(
        data,
        dict,
    ):

        raise ValueError(
            "Model Card data must "
            "be a JSON object."
        )

    return data


def is_pending(
    value: Any,
) -> bool:

    if value is None:
        return True

    return (
        str(value)
        .strip()
        .upper()
        in {
            "",
            "PENDING",
        }
    )


def validate(
    data: dict,
) -> list[str]:

    errors = []

    missing_keys = (
        REQUIRED_KEYS
        - set(
            data
        )
    )

    for key in sorted(
        missing_keys
    ):

        errors.append(
            f"Missing required key: {key}"
        )

    governance_status = (
        str(
            data.get(
                "governance_status",
                "",
            )
        )
        .strip()
        .upper()
    )

    if (
        governance_status
        not in
        ALLOWED_GOVERNANCE_STATUSES
    ):

        errors.append(
            "governance_status must be "
            "one of: "
            + ", ".join(
                sorted(
                    ALLOWED_GOVERNANCE_STATUSES
                )
            )
        )

    roc_auc = (
        data.get(
            "roc_auc"
        )
    )

    if roc_auc not in (
        None,
        "",
        "PENDING",
    ):

        try:

            value = float(
                roc_auc
            )

            if not (
                0
                <= value
                <= 1
            ):

                errors.append(
                    "roc_auc must be "
                    "between 0 and 1."
                )

        except (
            TypeError,
            ValueError,
        ):

            errors.append(
                "roc_auc must be numeric, "
                "null, or PENDING."
            )

    approved = (
        data.get(
            "target_business_description_approved"
        )
    )

    if not isinstance(
        approved,
        bool,
    ):

        errors.append(
            "target_business_description_approved "
            "must be true or false."
        )

    if (
        approved is True
        and is_pending(
            data.get(
                "target_business_description"
            )
        )
    ):

        errors.append(
            "A missing target_business_description "
            "cannot be approved."
        )

    explainability = (
        data.get(
            "explainability"
        )
    )

    if not isinstance(
        explainability,
        dict,
    ):

        errors.append(
            "explainability must "
            "be a JSON object."
        )

    else:

        artefacts = (
            explainability.get(
                "artefacts",
                [],
            )
        )

        if not isinstance(
            artefacts,
            list,
        ):

            errors.append(
                "explainability.artefacts "
                "must be a list."
            )

            artefacts = []

        valid_ids = set()

        for index, artefact in enumerate(
            artefacts,
            start=1,
        ):

            if not isinstance(
                artefact,
                dict,
            ):

                errors.append(
                    f"Explainability artefact "
                    f"{index} must be an object."
                )

                continue

            artefact_type = (
                str(
                    artefact.get(
                        "type",
                        "",
                    )
                )
                .strip()
            )

            if (
                artefact_type
                not in
                ALLOWED_ARTEFACT_TYPES
            ):

                errors.append(
                    f"Explainability artefact "
                    f"{index} has unsupported type: "
                    f"{artefact_type or '(missing)'}"
                )

            artefact_id = (
                str(
                    artefact.get(
                        "id",
                        "",
                    )
                )
                .strip()
            )

            if not artefact_id:

                errors.append(
                    f"Explainability artefact "
                    f"{index} requires an id."
                )

            else:

                if (
                    artefact_id
                    in valid_ids
                ):

                    errors.append(
                        "Duplicate explainability "
                        f"artefact id: {artefact_id}"
                    )

                valid_ids.add(
                    artefact_id
                )

            if (
                artefact_type
                ==
                "numeric_feature_importance_table"
            ):

                if (
                    artefact.get(
                        "verified"
                    )
                    is not True
                ):

                    errors.append(
                        "Numeric feature-importance "
                        f"artefact {index} must have "
                        "`verified: true`."
                    )

                rows = (
                    artefact.get(
                        "table"
                    )
                    or artefact.get(
                        "rows"
                    )
                    or artefact.get(
                        "features"
                    )
                )

                if (
                    not isinstance(
                        rows,
                        list,
                    )
                    or not rows
                ):

                    errors.append(
                        "Numeric feature-importance "
                        f"artefact {index} must contain "
                        "verified rows."
                    )

        selected_id = (
            explainability.get(
                "selected_artefact_id"
            )
        )

        if (
            selected_id
            is not None
        ):

            if (
                str(
                    selected_id
                )
                not in valid_ids
            ):

                errors.append(
                    "selected_artefact_id "
                    "does not match an available "
                    "explainability artefact."
                )

    for list_field in (
        "evidence_summary",
        "missing_fields",
        "recommended_actions",
    ):

        value = (
            data.get(
                list_field
            )
        )

        if not isinstance(
            value,
            list,
        ):

            errors.append(
                f"{list_field} "
                "must be a list."
            )

    return errors


def main() -> None:

    parser = (
        argparse.ArgumentParser(
            description=(
                "Validate DSLC Model Card "
                "structured data."
            )
        )
    )

    parser.add_argument(
        "file",
        nargs="?",
        help=(
            "Path to "
            "output/model_card_data.json"
        ),
    )

    args = (
        parser.parse_args()
    )

    if not args.file:

        print(
            "Usage:"
        )

        print(
            "python "
            "tools/validate_model_card.py "
            "output/model_card_data.json"
        )

        return

    try:

        data = load_json(
            Path(
                args.file
            )
        )

        errors = validate(
            data
        )

    except Exception as exc:

        print(
            "MODEL CARD "
            "VALIDATION FAILED:"
        )

        print(
            exc
        )

        sys.exit(
            1
        )

    if errors:

        print(
            "MODEL CARD "
            "VALIDATION FAILED "
            f"({len(errors)} error(s))"
        )

        for number, error in enumerate(
            errors,
            start=1,
        ):

            print(
                f"{number}. {error}"
            )

        sys.exit(
            1
        )

    print(
        "MODEL CARD VALIDATION "
        "PASSED — 0 errors."
    )


if __name__ == "__main__":
    main()