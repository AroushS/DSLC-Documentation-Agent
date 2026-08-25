# DSLC Stage 1 Documentation Agent

## Purpose

Generates a draft **DSLC Stage 1 document** from existing project evidence.

The agent reviews available evidence, assesses Stage 1 requirements, identifies gaps and produces a structured document for human review.

## What You Need

Provide the project evidence available for the project, such as:

- Project README
- Project / modelling notebooks
- EDA
- Use Case Shaping documentation

Where available, the agent can also use supporting evidence such as validation, solution design and governance documentation.

You do not need to manually provide GitHub links for evidence stored in a Git repository.

## Requirements

- VS Code
- GitHub Copilot
- Python 3.x
- Git, where repository evidence links are required

## How to Use

1. Open the repository in VS Code.

2. Make the relevant project evidence available in the workspace.

3. Open GitHub Copilot Chat.

4. Ask:

   **`Generate the Stage 1 DSLC documentation.`**

5. Respond to any targeted questions where required information cannot be verified from the available evidence.

6. Review the generated Stage 1 document before approval or sign-off.

## Output

Generated outputs include:

- editable DOCX;
- PDF review copy, where available.

The document includes:

- Stage 1 Readiness Dashboard;
- Table of Contents and document navigation;
- detailed Stage 1 assessment;
- Evidence Register;
- verified evidence links or locations where available.

## Important

The agent does not invent missing project evidence or provide governance approval.

Missing or unverifiable information is made visible for human review.

Evidence links are created only where they can be safely verified. If a link cannot be verified, the agent uses a verified file location where possible rather than guessing a URL.

All generated Stage 1 documentation remains a **DRAFT for human review**.
