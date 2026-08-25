# DSLC Documentation Agent

Evidence-based documentation agent for generating **Stage 1 DSLC documentation** and **Model Cards** from existing Data Science project evidence.

The agent reviews available project evidence, identifies gaps and generates draft documentation for human review.

It does not invent missing information or provide governance approval.

---

## Requirements

- VS Code
- GitHub Copilot
- Python 3.x
- Git

Make the relevant Data Science project and its evidence available in the VS Code workspace.

Evidence may include:

- project README;
- modelling, training, validation or scoring notebooks;
- EDA;
- Use Case Shaping document;
- Solution Design;
- governance or approved business documentation.

---

## During Generation

The agent may ask for permission to run PowerShell (`pwsh`) or Python commands during generation.

These commands are used for normal workflow tasks such as:

- checking available project files;
- locating and verifying evidence;
- validating generated content;
- generating the final documents.

Seeing command approval requests is a normal part of the workflow. Users are not expected to write the commands themselves.

Users should review commands before approving them, particularly if a command modifies or deletes files.

---

## Workflow 1 — Stage 1 DSLC

Ask GitHub Copilot:

> **Generate the Stage 1 DSLC documentation.**

The agent reviews the available project evidence, assesses the Stage 1 requirements and identifies missing or conflicting evidence.

It generates:

- `stage1_draft.md`;
- editable DOCX;
- PDF review copy, where available;
- Stage 1 Readiness Dashboard;
- Evidence Register with verified evidence locations.

The Markdown output is designed to remain portable for review and use in tools such as Confluence.

---

## Workflow 2 — Model Card

Ask GitHub Copilot:

> **Generate a Model Card for this project.**

The agent uses verified project evidence to populate the Model Card and identifies unsupported fields as `PENDING`.

It generates:

- structured Model Card data;
- HTML Model Card;
- PDF where supported;
- Evidence Summary;
- Missing Fields;
- Recommended Actions.

### Explainability

To populate the explainability section, the project must contain at least one valid explainability artefact:

- SHAP summary plot;
- feature-importance plot;
- verified numeric feature-importance table;
- user-provided PNG or JPG explainability graphic.

If multiple valid artefacts are available and none has been selected, the agent will request a selection.

If no valid explainability evidence is available, the section remains `PENDING`.

**The agent will not create, infer or invent explainability values.**

---

## Evidence & Governance

The agent follows an evidence-first approach.

- Missing or unverifiable information remains visible as `PENDING`.
- Evidence links are used only where they can be safely verified.
- Example documents are used for structure only, never as project evidence.
- Governance approval and sign-off are never inferred.

All generated Stage 1 documentation and Model Cards remain **DRAFTS for human review** unless verified approval evidence demonstrates otherwise.
