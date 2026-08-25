# Generate Stage 1 DSLC

Generate the complete Stage 1 Proof of Value DSLC package for the active project.

Follow the repository-wide DSLC instructions and all relevant knowledge rules.

The Stage 1 workflow must use one consistent evidence assessment across Markdown, DOCX and PDF outputs.

Presentation differences between output formats must never change:

- project facts;
- evidence conclusions;
- governance statuses;
- missing information;
- blockers;
- assumptions;
- required actions.

---

## Workflow

### Step 1 — Review available project evidence

Review all available active-project evidence before asking the user for information.

Evidence may include:

- project README files;
- Use Case Shaping documentation;
- Solution Design documentation;
- SQL;
- training notebooks;
- validation notebooks;
- scoring notebooks;
- production code;
- model artefacts;
- persisted metrics;
- governance documentation;
- approved business documentation;
- explainability artefacts.

Do not ask the user for information that can reasonably be verified from supplied project evidence.

Do not treat previously generated Stage 1 documents or other generated agent outputs as authoritative project evidence.

---

### Step 2 — Assess Stage 1 requirements

Assess the project against every applicable Stage 1 requirement using:

- `knowledge/stage1_requirements.yaml`;
- `knowledge/evidence_rules.md`;
- `knowledge/governance_rules.md`.

For every applicable requirement determine:

- evidence located;
- evidence source;
- relevant finding;
- whether evidence is sufficient;
- current status;
- missing information;
- required action where applicable.

Use only governance statuses defined in `knowledge/governance_rules.md`.

Do not invent alternative statuses.

Do not begin final document generation before the evidence assessment is complete.

---

### Step 3 — Identify missing or conflicting evidence

Identify any:

- missing evidence;
- unsupported claims;
- conflicting evidence;
- unresolved governance requirements.

Apply evidence-source priority rules defined in `knowledge/evidence_rules.md`.

Do not silently merge contradictory information.

Do not invent information to resolve missing or conflicting evidence.

---

### Step 4 — Ask targeted questions only where necessary

Ask the user only where required information:

- cannot reasonably be verified from available project evidence;
- cannot be resolved using evidence-priority rules;
- genuinely requires user clarification or confirmation.

Group related questions where practical.

Do not ask generic intake questions where evidence already contains the answer.

---

### Step 5 — Build evidence traceability

Build evidence traceability for every major Stage 1 requirement.

For each local project evidence file used:

- confirm the evidence file actually exists in the workspace;
- run `tools/resolve_evidence_link.py` for that file;
- use exactly the evidence location returned by the tool;
- if the tool returns a verified GitHub URL, preserve it as a Markdown hyperlink;
- if the tool returns only a verified relative workspace path, use that path as plain text;
- if no evidence location can be verified, use `Location not available`.

Never manually construct or guess:

- a GitHub repository URL;
- organisation name;
- repository name;
- branch name;
- commit;
- file path;
- SharePoint URL;
- Confluence URL;
- Databricks URL;
- any other evidence location.

Where an explicit external evidence URL already exists in supplied project evidence, preserve that URL rather than replacing it.

---

### Step 6 — Generate the Stage 1 Markdown source

Generate:

`stage1_draft.md`

using:

- `knowledge/output_standard.md`;
- `templates/stage1_template.md`;
- the completed evidence assessment;
- the determined requirement statuses.

`stage1_draft.md` has two purposes:

1. it is the structured Stage 1 source used for validation and document rendering;
2. it is a portable reviewer-facing Markdown document suitable for direct review or copying into collaboration tools such as Confluence.

The Markdown must contain the same authoritative:

- project facts;
- Stage 1 assessment;
- governance statuses;
- evidence conclusions;
- blockers;
- missing information;
- assumptions;
- required actions;

as the rendered DOCX and PDF.

Use:

- standard Markdown headings;
- concise paragraphs;
- standard bullet lists;
- standard numbered lists;
- simple Markdown tables;
- written governance statuses;
- verified Markdown hyperlinks where available.

Do not rely on:

- complex HTML;
- CSS;
- colour-only meaning;
- deeply nested tables;
- merged cells;
- Word page numbers;
- Word bookmarks;
- Word-only callout formatting;
- manual page breaks;
- editor-specific URLs.

---

### Step 7 — Generate portable Markdown navigation

Include a concise `## Contents` section near the beginning of `stage1_draft.md`.

The Markdown Contents section is for document orientation only.

Use plain-text section names.

Do not create hyperlinks in the Markdown Contents section.

For the standard Stage 1 structure, use:

1. Stage 1 Readiness
2. Business & Use Case
3. Data Readiness
4. Exploratory Analysis
5. Feature Engineering
6. Model Development & Validation
7. Governance & Sign-off
8. Risks & Limitations
9. Stage 1 Recommendation
10. Appendix A — Evidence Register
11. Appendix B — Data Sources
12. Appendix C — Model Technical Detail

The Contents section must correspond to headings that actually exist in the generated Stage 1 Markdown.

Never generate Markdown Contents links using:

- `file://` URLs;
- `file+` URLs;
- `vscode-resource` URLs;
- `vscode-cdn.net` URLs;
- absolute local Windows paths;
- absolute local macOS or Linux paths;
- editor preview URLs;
- machine-specific URLs.

Do not include page numbers in the Markdown Contents section.

Do not attempt to construct or infer Markdown heading anchors.

The DOCX renderer may independently create Word-specific Table of Contents navigation as a presentation feature.

Markdown navigation must remain portable and independent of the user's editor or local machine.


---

### Step 8 — Generate the Stage 1 Readiness Dashboard

Include a concise Stage 1 Readiness Dashboard near the beginning of `stage1_draft.md`.

The dashboard should show:

- Stage 1 area;
- current written status;
- key gap or required action;
- relevant detailed section.

Use only statuses defined in `knowledge/governance_rules.md`.

Do not introduce alternative governance statuses for presentation purposes.

The Markdown dashboard must remain understandable without colour.

The DOCX/PDF renderer may add visual styling.

Visual styling must never change, calculate or override governance status.

---

### Step 9 — Populate Appendix A — Evidence Register

Populate Appendix A — Evidence Register with:

- DSLC Requirement;
- Evidence Source;
- What the Evidence Demonstrates;
- Evidence Location.

Appendix A is the authoritative evidence-traceability location.

Do not repeatedly reproduce detailed evidence locations throughout the main report.

Where useful, the main report may identify an evidence source by name.

Detailed file paths and links should normally remain in Appendix A.

For evidence locations:

- use a verified clickable link where safely available;
- otherwise use a verified relative workspace path;
- otherwise use `Location not available`.

Never guess an evidence location.

---

### Step 10 — Validate the Stage 1 Markdown

Validate `stage1_draft.md` before rendering.

Run the existing Stage 1 validation workflow.

Validation must confirm that:

- every applicable Stage 1 requirement is represented;
- project-specific claims are supported by evidence;
- no project facts have been invented;
- no approval or sign-off has been invented;
- conditional requirements have been evaluated;
- missing evidence is clearly identified;
- unsupported items are not marked COMPLETE;
- only governance statuses defined in `knowledge/governance_rules.md` are used;
- Readiness Dashboard statuses match the detailed assessment;
- evidence locations have not been guessed;
- relative paths are used where verified clickable links are unavailable;
- `Location not available` is used where neither link nor path can be verified;
- Markdown navigation contains no VS Code-local resource URLs;
- Markdown navigation contains no machine-specific local URLs;
- Markdown contains no Word page-number navigation;
- Markdown, DOCX and PDF represent the same evidence assessment.

If validation fails:

- correct structural or evidence-mapping issues;
- do not invent information to make validation pass;
- rerun validation before rendering.

---

### Step 11 — Render the Stage 1 document

Render the validated Stage 1 Markdown using the existing standard Stage 1 renderer.

The renderer may add presentation features including:

- colours;
- borders;
- fonts;
- spacing;
- callout boxes;
- page breaks;
- page numbers;
- headers and footers;
- Table of Contents fields;
- internal document navigation;
- bookmarks.

The renderer is a presentation layer.

The renderer must not independently:

- create evidence;
- change project facts;
- change evidence conclusions;
- change governance statuses;
- remove unresolved gaps;
- convert `PENDING` into completion;
- introduce unsupported conclusions.

The DOCX Table of Contents should be based on document heading styles.

Do not invent or hard-code final Word page numbers.

Where Word Table of Contents page numbers require Microsoft Word field refresh, retain the valid Table of Contents structure and allow Word to refresh the final pagination.

Failure to refresh Word page numbers automatically is a presentation limitation only.

It must not:

- fail Stage 1 generation;
- change evidence assessment;
- change governance status;
- cause page numbers to be guessed.

---

### Step 12 — Produce the standard Stage 1 deliverables

Produce:

1. `stage1_draft.md`
2. `Stage1_<ProjectName>.docx`
3. `Stage1_<ProjectName>.pdf`

`stage1_draft.md` is the portable reviewer-facing Markdown version and structured content source.

`Stage1_<ProjectName>.docx` is the editable master document.

`Stage1_<ProjectName>.pdf` is the controlled review/distribution copy.

All available outputs must represent the same evidence assessment and governance position.

If PDF generation is technically unavailable:

- still produce Markdown and DOCX.

If DOCX/PDF rendering is technically unavailable:

- still produce validated Markdown.

Presentation failures must never cause:

- evidence fabrication;
- governance-status changes;
- suppression of identified gaps;
- guessed evidence locations;
- guessed navigation targets;
- guessed page numbers.

---

## Output quality

The final Stage 1 package must:

- be concise and business-readable;
- prioritise Stage 1 readiness and outstanding actions;
- make major blockers visible early;
- avoid unnecessary repetition;
- avoid exposing YAML or unnecessary internal agent terminology;
- clearly distinguish technical readiness from governance readiness;
- clearly identify pending items;
- explain important missing evidence;
- provide clear next actions;
- show important evidence without dumping raw notebook content;
- provide traceability through Appendix A — Evidence Register;
- include verified clickable evidence links where available;
- fall back safely to verified workspace paths where clickable links are unavailable;
- use `Location not available` where no evidence location can be verified;
- never contain guessed, fabricated or inferred evidence URLs;
- keep technical detail proportionate to Stage 1 review;
- produce portable Markdown suitable for review outside VS Code;
- prevent VS Code-local resource URLs from entering the Markdown;
- preserve the same facts, statuses, gaps and actions across Markdown, DOCX and PDF.

---

## Final rule

Markdown, DOCX and PDF are different presentations of the same evidence assessment.

No output format may independently change:

- evidence;
- project facts;
- governance status;
- Stage 1 readiness;
- blockers;
- missing information;
- required actions.

If a presentation feature cannot be produced safely, use the defined fallback and continue generation.

The Stage 1 package remains a draft for human review unless explicit approved evidence demonstrates otherwise.

Never represent the Stage 1 package as approved or signed off without verified approval evidence.