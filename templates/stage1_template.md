# Stage 1 – Proof of Value

## Purpose of this template

This template defines the reader-facing structure of the Stage 1 Proof of Value DSLC document.

It does not define whether a requirement is required, optional, conditional or blocking.

Those rules come from:

`knowledge/stage1_requirements.yaml`

Governance status must come from:

`knowledge/governance_rules.md`

Evidence must be assessed using:

`knowledge/evidence_rules.md`

Writing and presentation must follow:

`knowledge/output_standard.md`

---

# Document Information

Include:

- Project / Use Case Name
- Stage: Stage 1 – Proof of Value
- Document Status
- Date Generated
- Business / Product Owner, where verified
- Technical Owner, where verified
- Stage Gate / Accountable Owner, where verified
- Checklist / DSLC version where known

Do not present unverified names as confirmed owners.

If ownership is unverified, show the role as PENDING rather than promoting a placeholder into the document header.

---

# 1. Stage 1 Readiness

This section must allow a senior reader to understand the current Stage 1 position without reading the full report.

## Overall Readiness

Provide one concise readiness statement using the governance rules.

Reader-facing outcomes may include:

- READY FOR REVIEW
- PENDING GOVERNANCE
- NOT READY FOR SIGN-OFF
- DRAFT

Do not calculate readiness by counting every occurrence of words such as PENDING, COMPLETE or PARTIAL in the document.

Readiness must be based on the unique applicable Stage 1 requirements defined in `knowledge/stage1_requirements.yaml`.

The agent must never provide approval or sign-off.

## Readiness Summary

The Readiness Summary provides an executive view of the project's current Stage 1 position.

It must allow a reviewer to quickly understand:

- the status of each major Stage 1 area;
- which areas require attention;
- the most important gap or action;
- where to find the detailed assessment.

Use one concise table:

| Stage 1 Area | Status | Key Gap / Action | Go to Section |
|---|---|---|---|
| Business / Use Case | | | Business & Use Case |
| Data Readiness | | | Data Overview |
| Exploratory Analysis | | | Exploratory Analysis |
| Technical Development | | | Feature Engineering / Model Development & Validation |
| Validation | | | Model Development & Validation |
| Governance | | | Governance & Sign-off |
| Final Sign-off | | | Governance & Sign-off |

### Readiness Summary Rules

- Populate the table using evidence from the active project only.
- Assess status using the applicable Stage 1 requirements and governance rules.
- Do not invent, estimate or recalculate a status solely for presentation.
- Use the standard status terminology defined by the governance rules.
- Keep each Key Gap / Action concise, specific and decision-relevant.
- Where no material gap or action exists, state `No material gap identified.`
- Where evidence is incomplete, state the most important evidence or action required.
- Do not include detailed evidence, long filenames, notebook paths, dataset identifiers or URLs in this table.
- Detailed evidence and evidence locations belong in the Evidence Register.
- Use section names rather than fixed page numbers so that navigation remains valid if document pagination changes.
- Do not add or remove Stage 1 areas based solely on the contents of a particular project.
- Where a requirement does not apply to the project, use the appropriate governance status rather than removing the area.
- Colour may be used as a visual aid in the rendered document, but the written status must always remain visible.
- The table must prioritise information requiring reviewer attention and must not repeat detailed content from later sections.

## Priority Blockers

List no more than five items that materially prevent Stage 1 completion.

Prioritise:

1. missing ownership;
2. missing governance registration or approval;
3. missing mandatory review;
4. missing sign-off;
5. material technical or validation gaps.

Do not list minor documentation improvements as executive blockers.

## Project Summary

Maximum four sentences.

Summarise:

- what the use case does;
- what business decision or action it supports;
- current technical and validation position;
- current governance position.

---

# 2. Business & Use Case

## Business Problem

State the verified business problem concisely.

## Decision Supported

Explain what decision, prioritisation or action the solution supports.

## Scope

### In Scope

Summarise the principal boundaries.

### Out of Scope

Include only meaningful exclusions.

## Expected Business Value

Explain the evidenced value without inventing quantitative benefits.

## Success Measures

Separate where possible:

- business success measures;
- technical or model success measures.

Do not automatically present model metrics as business KPIs.

## End Users & Stakeholders

Use concise prose or a small table where comparison adds value.

## Ownership & Delivery

Use one table:

| Role / Item | Confirmed Information | Status |
|---|---|---|
| Business / Product Owner | | |
| Technical Owner | | |
| Stage Gate / Accountable Owner | | |
| Executive Sponsor where relevant | | |
| Delivery Epic / Milestone | | |

Unverified placeholders must be clearly marked as requiring confirmation.

Do not reproduce governance review or sign-off details here.

Refer to Section 7 for governance status.

---

# 3. Data Readiness

## Data Overview

Summarise the important data domains used by the project.

The main report should describe data at a business or technical domain level.

Example:

"The solution combines Service Checker health data, Hub telemetry, customer attributes, WHIX performance and historical contact data."

Do not list long physical table identifiers in the main narrative.

Full physical dataset and table references belong in Appendix B.

## Data Suitability

Summarise:

- population and coverage;
- target availability;
- important inclusion or exclusion criteria;
- material limitations.

## Data Quality

Summarise only important findings and controls.

Examples:

- missing-data treatment;
- invalid or duplicate data where assessed;
- data coverage;
- material quality limitations.

## Data Governance

Provide a concise statement of the current governance position.

Do not reproduce the full governance-status table.

Refer to Section 7.

## Deployment / Operational Data Considerations

Include only where applicable.

Summarise:

- production data interfaces;
- material migration or repointing needs;
- operational dependencies.

Detailed technical paths belong in appendices.

---

# 4. Exploratory Analysis

## Analysis Performed

Summarise the EDA that can be verified from project evidence.

Do not reproduce a notebook walkthrough.

## Key Findings

Include only findings that materially affected:

- use-case feasibility;
- data suitability;
- feature engineering;
- modelling;
- validation;
- business interpretation.

A concise table may be used:

| Finding | Why It Matters |
|---|---|

## Data / Target Distribution

Include significant distribution findings such as class imbalance where relevant.

## Implications

Explain how the EDA influenced the downstream technical approach.

## Evidence Gap

If a standalone EDA artefact is required but unavailable, identify this once.

Do not repeat the same gap in multiple sections.

---

# 5. Feature Engineering

## Approach

Explain the feature-engineering strategy in business-readable technical language.

## Key Feature Decisions

Summarise the most material decisions.

Examples:

- missing-value treatment;
- derived features;
- temporal windows;
- aggregation strategy;
- feature selection;
- encoding.

Do not include full implementation syntax in the main report unless necessary to explain a material decision.

## Quality & Leakage Considerations

Explain:

- reproducibility;
- target leakage consideration;
- important feature-quality controls.

If formal leakage evidence is unavailable, identify the gap without claiming completion.

## Rationale

Explain why the important engineering choices were appropriate for this use case.

Detailed feature lists belong in Appendix C.

---

# 6. Model Development & Validation

## Model Overview

Summarise:

- problem type;
- final selected model;
- primary output;
- training period;
- major modelling decisions.

Do not include the full hyperparameter list here.

## Model Development

Where multiple meaningful candidates or versions were assessed, summarise them concisely.

Use a small comparison table only where it helps explain model selection.

## Performance Summary

Use:

| Measure | Result | Interpretation | Business Relevance |
|---|---|---|---|

Only include verified results.

Do not invent missing numeric values.

Where exact results cannot be extracted reliably, state that the evidence exists and identify the required follow-up.

## Validation

Explain:

- validation approach;
- validation period or data;
- evidence available;
- what the validation demonstrates;
- material limitations.

Do not confuse training evaluation with independent or out-of-time validation.

## Business Interpretation

Explain how the model output supports the intended business decision.

Avoid claims of realised business benefit unless explicitly evidenced.

## Key Limitations

Include only material limitations.

Do not describe a limitation as accepted unless explicit authorised human risk-acceptance evidence exists.

Full hyperparameters, feature lists and model artefact paths belong in Appendix C.

---

# 7. Governance & Sign-off

This is the single authoritative governance-status section in the document.

Do not reproduce full governance status tables elsewhere.

Use one consolidated table:

| Governance Requirement | Status | Evidence / Gap | Required Action |
|---|---|---|---|
| Business Review | | | |
| Technical Review | | | |
| AI Inventory Registration | | | |
| Data Governance | | | |
| Deployment / Model Handover where applicable | | | |
| Technical Sign-off | | | |
| Business Sign-off | | | |
| Final Stage 1 Sign-off | | | |

Include any additional applicable governance requirement defined by `knowledge/stage1_requirements.yaml`.

Rules:

- Each unique governance requirement appears once.
- Status must follow `knowledge/governance_rules.md`.
- COMPLETE requires sufficient evidence.
- PENDING must explain the evidence gap and required action.
- NOT APPLICABLE requires a clear justification.
- RISK ACCEPTED requires explicit authorised human evidence.
- The agent must never provide approval or sign-off.

Other sections may reference Section 7 but must not reproduce the same status, reason and action information.

---

# 8. Risks & Limitations

Include only material Stage 1 risks and limitations.

Use:

| Risk / Limitation | Impact | Mitigation / Required Action | Status |
|---|---|---|---|

Status wording must be governance-safe.

Prefer:

- Known limitation
- Documented constraint
- Mitigation required
- PENDING
- To confirm

Do not use:

- Accepted
- Accepted operationally
- Risk accepted

unless explicit authorised risk-acceptance evidence exists.

Do not duplicate governance requirements already captured in Section 7 unless the issue also represents a distinct material project risk.

---

# 9. Stage 1 Recommendation

Provide a concise final assessment.

State:

- what is sufficiently evidenced;
- what remains outstanding;
- whether the document is ready for human review;
- whether Stage 1 can currently proceed to sign-off;
- the highest-priority next steps.

Do not provide Stage 1 approval.

Keep this section concise.

---

# Appendix A — Evidence Register

This is the single authoritative Evidence Register for the Stage 1 document.

The Evidence Register provides traceability between major Stage 1 requirements and the project evidence used to assess them.

Use:

| DSLC Requirement | Evidence Source | What the Evidence Demonstrates | Evidence Location |
|---|---|---|---|
| | | | |

Rules:

- include evidence supporting each major applicable Stage 1 requirement;
- identify where required evidence is absent;
- use clear filenames, document names or evidence-source descriptions;
- state concisely what the evidence demonstrates;
- include a verified evidence location where available;
- use clickable Markdown links only where the URL has been explicitly supplied or verified;
- for local repository evidence, use the evidence location returned by `tools/resolve_evidence_link.py`;
- if a verified GitHub URL is returned, use a concise clickable label such as `[Open in GitHub](VERIFIED_URL)`;
- if only a verified relative workspace path is available, show that path as plain text;
- if no evidence location can be verified, use `Location not available`;
- never invent, guess or manually construct evidence URLs;
- never infer a repository, branch, file path or external document location;
- do not reproduce the Evidence Register elsewhere in the document.

The Evidence Register is the primary location for detailed evidence traceability.

The main Stage 1 narrative should remain concise and should not repeatedly reproduce evidence links.

---

# Appendix B — Data Sources

Provide detailed physical dataset references where useful.

Use:

| Data Source / Dataset | Purpose |
|---|---|

This is the appropriate location for:

- BigQuery table identifiers;
- physical dataset paths;
- environment-specific data locations.

In the main report, use concise data-domain descriptions instead.

---

# Appendix C — Model Technical Detail

Include implementation detail useful to technical reviewers but unnecessary for the main Stage 1 narrative.

May include:

## Final Hyperparameters

## Full Feature Lists

## Model Artefacts

## Technical Paths

## Additional Modelling Detail

Do not repeat technical information already sufficiently explained in the main report.

---

# Final Document Rule

The main report must prioritise decisions, readiness and material evidence.

A business or governance reader should understand the project's Stage 1 position from the first two pages.

Detailed implementation evidence should remain available through the appendices without dominating the main report.