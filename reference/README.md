# DSLC Reference Material

## Purpose

The documents in this folder contain official or supporting DSLC reference material.

They provide traceability to the original guidance used to design the Stage 1 Documentation Agent and should be treated as the authoritative source for understanding the intent of the Data Science Lifecycle (DSLC).

These documents support the agent but are **not** the primary source used when generating Stage 1 documentation.

---

# How the agent should use these files

Reference material may be used to:

- verify official DSLC terminology;
- understand the purpose of Stage 1 requirements;
- understand official governance expectations;
- understand roles and responsibilities;
- understand checklist and sign-off expectations;
- clarify the intent of official DSLC documentation;
- resolve ambiguity where the distilled knowledge files are unclear.

These documents exist to support the agent's reasoning, **not** to provide project-specific information.

---

# When to consult reference material

The agent should consult the documents in this folder only when:

- verifying an official DSLC definition;
- confirming governance expectations;
- clarifying roles and responsibilities;
- resolving ambiguity that cannot be answered using the distilled knowledge files;
- validating that generated documentation remains aligned with the official DSLC guidance.

The agent should **not** read every reference document during every Stage 1 generation.

Use these documents only when additional clarification is required.

---

# Priority

When generating Stage 1 documentation, always use the distilled knowledge sources first.

Priority order:

1. `knowledge/stage1_requirements.yaml`
2. `knowledge/evidence_rules.md`
3. `knowledge/governance_rules.md`
4. `knowledge/output_standard.md`
5. `templates/stage1_template.md`

These files contain the standardised rules that should normally be followed during Stage 1 generation.

The documents contained within `reference/official/` provide supporting context and traceability to the official DSLC documentation.

They should not normally be reinterpreted from scratch during every generation.

---

# Handling conflicts

If a reference document appears to conflict with one of the distilled knowledge files:

- do not silently override either source;
- identify the conflict;
- continue using the distilled knowledge files as the primary generation rules;
- flag the conflict for human review so the knowledge files can be updated if necessary.

The reference material exists to support governance and continuous improvement of the agent, not to introduce inconsistent behaviour.

---

# Important

Reference documents are **NOT** evidence about the active project.

Never copy project-specific information from reference material, including:

- project names;
- Product Owners;
- Technical Owners;
- stakeholders;
- dates;
- datasets;
- features;
- model names;
- model metrics;
- approvals;
- governance statuses;
- risks;
- evidence links;
- completion dates;
- model results.

Reference documents must never be used to populate missing project-specific information.

---

# Missing project information

If project evidence is missing or cannot be verified:

- follow the evidence rules;
- follow the governance rules;
- identify the missing information;
- explain what evidence is required;
- determine the appropriate status using the governance rules.

Do **not** replace missing project information with information taken from reference documents.

---

# Relationship to project evidence

The Stage 1 Documentation Agent works with three different types of information.

## 1. Distilled Knowledge

Stored in:

- `knowledge/`
- `templates/`

Defines:

- Stage 1 requirements;
- evidence rules;
- governance rules;
- writing standards;
- report structure.

---

## 2. Reference Material

Stored in:

- `reference/official/`

Provides:

- official DSLC guidance;
- governance context;
- terminology;
- traceability to source documentation.

---

## 3. Project Evidence

Supplied by the active project.

Examples include:

- README files;
- Use Case Shaping documentation;
- Solution Design documentation;
- training notebooks;
- validation notebooks;
- scoring notebooks;
- feature engineering notebooks;
- production code;
- governance documentation;
- approval records.

Only project evidence should be used to generate project-specific Stage 1 content.

Reference material should never replace project evidence.

---

# Repository design principle

This repository separates:

- **what Stage 1 requires;**
- **where evidence should come from;**
- **how governance should be assessed;**
- **how the final document should be written;**
- **where official DSLC guidance can be traced.**

This separation improves consistency, maintainability and enables the Stage 1 Documentation Agent to be used across multiple projects and by multiple Data Science teams.