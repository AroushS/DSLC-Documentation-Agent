# Governance Rules

## Core principle

The agent reports governance status.

The agent does not provide governance approval.

## Allowed statuses

Use only:

- COMPLETE
- PENDING
- NOT APPLICABLE
- RISK ACCEPTED
- DRAFT

## COMPLETE

Use only when sufficient explicit evidence exists.

Example:

Business Sign-off may be COMPLETE only where explicit business approval evidence exists.

Do not infer approval from:
- stakeholder involvement,
- production use,
- completed technical work,
- project documentation.

## PENDING

Use when:
- evidence is missing,
- approval is missing,
- the requirement cannot be verified.

Every PENDING item must explain:
- what is missing,
- what evidence would resolve it.

## NOT APPLICABLE

Use only where the requirement genuinely does not apply.

Always include a reason.

Example:

Model Handover may be NOT APPLICABLE where verified evidence shows the project is limited to Proof of Value and no production deployment is planned.

## RISK ACCEPTED

Use only where explicit human risk-acceptance evidence exists.

The agent must never assign this status independently.

## Business approval logic

Explicit business approval evidence?
- YES → COMPLETE
- NO → PENDING

## Technical approval logic

Explicit technical approval evidence?
- YES → COMPLETE
- NO → PENDING

## Final sign-off

Final Sign-off may be COMPLETE only when:
- all applicable required Stage 1 items are complete,
- technical sign-off exists,
- business sign-off exists,
- explicit final approval evidence exists.

The agent cannot provide final sign-off.