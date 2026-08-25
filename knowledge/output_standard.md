# Document Design Standard

## Design principle

The final Stage 1 package must be designed for rapid review by business, technical and governance stakeholders.

The reader should be able to understand the project's Stage 1 readiness within the first two pages of the rendered document and quickly understand the same position from the Markdown version.

The Stage 1 workflow must maintain one consistent evidence assessment across Markdown, DOCX and PDF outputs.

Presentation differences between output formats must never change:

- project facts;
- evidence conclusions;
- governance statuses;
- missing information;
- blockers;
- assumptions;
- required actions.

The Markdown source must remain portable and collaboration-friendly.

The DOCX/PDF renderer may enhance presentation but must not alter evidence meaning.

---

## Information hierarchy

Prioritise information in this order:

1. overall Stage 1 readiness;
2. major blockers;
3. business purpose and value;
4. technical and validation evidence;
5. governance position;
6. detailed evidence and technical appendices.

Do not give every piece of information equal visual importance.

The main narrative should explain what the evidence means for Stage 1 readiness rather than reproduce large quantities of raw technical information.

---

## Executive readiness dashboard

The beginning of the Stage 1 package should provide a concise executive Readiness Dashboard.

A reviewer should be able to quickly determine:

- the overall Stage 1 position;
- which major areas are complete;
- which areas require attention;
- the key action or gap for any incomplete area;
- the relevant detailed section.

The dashboard must remain concise and should not reproduce detailed evidence.

Where supported by the DOCX/PDF renderer, visual status indicators may use:

- green for sufficiently evidenced / complete areas;
- amber for pending or clarification-required areas;
- red for outcomes that currently prevent Stage 1 progression;
- neutral styling for not-applicable areas.

Colour is a visual aid only.

The written governance status must always remain visible and authoritative.

Visual presentation must never change, override or independently calculate governance status.

---

## Main body vs appendix

Keep the main body concise.

Move detailed technical information to appendices where possible.

Examples that should normally be moved to an appendix include:

- long dataset or table identifiers;
- full hyperparameter lists;
- full feature lists;
- detailed file paths;
- extensive notebook references;
- detailed evidence locations.

The main report should explain findings, implications, gaps and actions.

Appendices should provide supporting detail and traceability.

---

## Tables

Use tables only when they improve comparison, readability or status visibility.

Avoid creating separate tables for every governance check.

Prefer one consolidated governance table where appropriate.

Avoid tables where long technical identifiers cause poor wrapping or unreadable layout.

For Markdown portability, avoid:

- merged cells;
- nested tables;
- very large technical tables;
- presentation that depends on fixed column widths;
- Word-specific table formatting.

### Markdown table integrity

All Markdown tables must use valid standard Markdown table syntax.

Every column must be separated using a pipe character (`|`).

Example:

| Stage 1 Area | Status | Key Gap / Action | Go to Section |
| --- | --- | --- | --- |
| Business / Use Case | PENDING | Confirm accountable owner and business purpose. | Business & Use Case |
| Data Readiness | COMPLETE | No current blocking action. | Data Readiness |

Never collapse multiple column headings into one cell.

Incorrect:

`| Stage 1 AreaStatusKey Gap / ActionGo to Section |`

Correct:

`| Stage 1 Area | Status | Key Gap / Action | Go to Section |`

Apply this rule to all Markdown tables, including:

- Document Information;
- Readiness Summary;
- ownership and delivery;
- model-performance measures;
- governance tables;
- risks and limitations;
- Evidence Register;
- data-source tables;
- technical appendices.

Before finalising `stage1_draft.md`, verify that:

- each table row contains the expected number of columns;
- each header contains separate cells;
- the separator row contains the same number of columns as the header;
- headings and values have not accidentally been concatenated;
- table content remains readable when copied as standard Markdown.

If a table cannot be represented cleanly using standard Markdown, prefer a short heading and bullet list rather than generating malformed table syntax.

Markdown table formatting is presentation only.

Table formatting must never change:

- evidence;
- project facts;
- governance statuses;
- blockers;
- missing information;
- conclusions;
- required actions.

---

## Navigation and usability

The Stage 1 package must support rapid navigation and document orientation without depending on a particular editor or local machine.

The rendered DOCX should provide:

- an executive Readiness Dashboard near the beginning;
- a Word Table of Contents;
- navigation from the Readiness Dashboard to relevant detailed sections where supported;
- an Evidence Register for detailed evidence traceability.

The Readiness Dashboard should show:

- Stage 1 area;
- current status;
- the most important gap or action;
- the relevant detailed section.

Navigation is a presentation feature only.

Navigation must never:

- change a Stage 1 status;
- change a governance conclusion;
- create evidence;
- imply that a requirement is complete;
- replace evidence assessment.

If a navigation feature cannot be created safely, retain the readable section name rather than failing document generation.

---

## Markdown navigation

Markdown navigation must remain portable outside VS Code and independent of the user's local machine.

The Markdown `## Contents` section must use plain-text section names.

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

The Contents section must correspond to headings that actually exist in the generated Markdown.

Never generate Markdown Contents links using:

- `file://` URLs;
- `file+` URLs;
- `vscode-resource` URLs;
- `vscode-cdn.net` URLs;
- absolute local Windows paths;
- absolute local macOS or Linux paths;
- temporary editor preview URLs;
- machine-specific URLs.

Do not include page numbers in the Markdown Contents section.

Do not attempt to construct or infer Markdown heading anchors for the Contents section.

The DOCX renderer may independently create Word-specific Table of Contents navigation as a presentation feature.

Markdown navigation must remain portable and independent of the user's editor.

---

## Word Table of Contents

The DOCX Table of Contents is a presentation feature.

The renderer should create a standard Word Table of Contents based on document heading styles where supported.

The renderer must not manually invent, calculate or hard-code final page numbers.

Final Word pagination may depend on Microsoft Word refreshing document fields after the DOCX is opened.

Automatic Microsoft Word automation is not a mandatory requirement of the Stage 1 workflow.

The standard Stage 1 workflow must not require the user to install additional Windows-specific packages solely to refresh the Table of Contents.

If Word has not refreshed the Table of Contents automatically:

- retain the valid Word Table of Contents structure;
- allow Microsoft Word to refresh it through its normal field-update functionality;
- do not treat this as Stage 1 validation failure;
- do not change governance status;
- do not guess page numbers.

Failure to refresh Word page numbers automatically is a presentation limitation only.

It must never prevent successful Stage 1 generation.

---

## Status consistency

Use only the statuses defined in `knowledge/governance_rules.md`:

- COMPLETE
- PENDING
- NOT APPLICABLE
- RISK ACCEPTED
- DRAFT

Do not introduce alternative governance statuses such as:

- PARTIAL;
- EVIDENCE PRESENT;
- PASS;
- FAIL;
- APPROVED.

Visual colours may make status easier to understand, but colour must not create or change status.

The written governance status is always authoritative.

A status must remain understandable when colour, icons or other visual styling are removed.

---

## Evidence presentation

Appendix A — Evidence Register is the authoritative location for detailed evidence traceability.

Do not repeatedly reproduce evidence locations throughout the main report.

Where useful, the main report may identify an evidence source by name, but detailed paths and links should normally remain in the Evidence Register.

For evidence locations:

- use a clickable verified link where one is safely available;
- otherwise use a verified relative path;
- otherwise use `Location not available`.

Failure to create a hyperlink must never prevent Stage 1 document generation.

Never display a guessed or constructed evidence URL.

Raw local filesystem paths should not normally appear in the main narrative.

Where a technical path is required for traceability, place it in the Evidence Register or relevant appendix.

---

## Graceful degradation

Optional presentation features must not cause the complete Stage 1 workflow to fail.

If:

- a GitHub link cannot be verified, use the verified relative path;
- no evidence location can be verified, use `Location not available`;
- Markdown navigation cannot safely support a hyperlink, use the readable section name as plain text;
- an internal DOCX navigation link cannot be created, retain the readable section name;
- Microsoft Word has not refreshed the Table of Contents, retain the valid TOC structure for normal Word field refresh;
- PDF generation is technically unavailable, still produce Markdown and editable DOCX.

Missing presentation functionality must not alter evidence assessment or governance status.

Missing required project evidence must continue to be handled according to:

- `knowledge/evidence_rules.md`;
- `knowledge/governance_rules.md`.

No optional presentation feature should introduce a mandatory platform-specific dependency for ordinary Stage 1 generation.

---

## Callouts

Use callout boxes sparingly in rendered documents for:

- critical governance gaps;
- important assumptions;
- required actions;
- major limitations.

Do not place every note inside a callout box.

The Markdown source must not depend on Word-specific callout formatting to communicate important information.

Where a callout is represented in Markdown, its meaning must remain clear using headings, bold text or concise explanatory text.

---

## Technical charts

Where meaningful charts already exist in verified project evidence, consider including a small number of decision-relevant figures such as:

- ROC curve;
- gain/lift;
- SHAP summary;
- validation comparison.

Do not include charts solely for decoration.

Do not create, infer or reconstruct technical results merely to improve document appearance.

If a chart is unavailable in a Markdown-compatible form, retain a clear textual description or evidence reference rather than introducing unsupported information.

---

## Length

Aim for a concise main report.

The main Stage 1 narrative should normally be approximately 8–12 pages when rendered, excluding appendices, depending on project complexity.

Avoid unnecessary repetition to reach or fill a page count.

Markdown should prioritise readability and information hierarchy rather than attempting to reproduce Word page lengths or page breaks.

---

## Markdown portability

`stage1_draft.md` is both:

1. the structured Stage 1 source used for validation and document rendering; and
2. a portable reviewer-facing version suitable for direct review and copying into collaboration tools such as Confluence.

The Markdown must therefore be treated as a supported Stage 1 output, not temporary processing text.

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

The Markdown must never contain a separate or independently generated governance interpretation.

### Markdown structure

Use standard Markdown wherever possible.

Use:

- `#` for the document title;
- `##` for major sections;
- `###` for subsections;
- concise paragraphs;
- standard bullet lists;
- standard numbered lists;
- valid simple Markdown tables where useful;
- bold text sparingly;
- readable section names.

Maintain a clear hierarchy so the Markdown remains easy to scan when copied into collaboration platforms.

### Markdown readiness dashboard

The Markdown should include a concise Stage 1 Readiness Dashboard near the beginning.

The dashboard should communicate:

- Stage 1 area;
- written status;
- key gap or required action;
- relevant detailed section.

Use a valid simple Markdown table where appropriate.

The dashboard must not depend on colour.

Do not introduce a different governance status solely to improve presentation.

### Markdown actions and gaps

Missing evidence and required actions must remain easy to identify without DOCX styling.

For incomplete areas, clearly state:

- authoritative status;
- missing evidence or information;
- why the gap matters where supported;
- required next action.

Do not rely on red, amber or green formatting to communicate required action.

### Markdown compatibility

For maximum portability, avoid relying on:

- complex HTML;
- CSS;
- colour-only status meaning;
- deeply nested tables;
- merged table cells;
- very large technical tables;
- Word-specific page numbers;
- Word bookmarks;
- Word-only callout formatting;
- manual page breaks;
- VS Code resource URLs;
- machine-specific local links;
- decorative layout elements that have no meaning outside the renderer.

These presentation features may be added by `tools/render_stage1.py` when creating the DOCX/PDF.

Their absence from Markdown must not remove important information.

### Markdown and rendered document consistency

The Markdown is the content source.

The renderer is responsible for enhanced document presentation.

The renderer may add:

- colours;
- borders;
- fonts;
- spacing;
- callout boxes;
- page breaks;
- page numbers;
- headers and footers;
- Word Table of Contents fields;
- internal document navigation;
- bookmarks;
- other non-semantic presentation improvements.

The renderer must not independently:

- create evidence;
- change evidence conclusions;
- change governance statuses;
- change project facts;
- remove unresolved gaps;
- convert `PENDING` into a completed status;
- introduce unsupported technical conclusions.

---

## Deliverables

A complete Stage 1 generation should produce:

1. `stage1_draft.md`
2. `Stage1_<ProjectName>.docx`
3. `Stage1_<ProjectName>.pdf`

`stage1_draft.md` is the portable reviewer-facing Markdown version and structured content source.

`Stage1_<ProjectName>.docx` is the editable master document.

`Stage1_<ProjectName>.pdf` is the controlled review/distribution copy.

All available outputs must represent the same evidence assessment and governance position.

The user should not need to explicitly request these formats.

If PDF generation is technically unavailable, still produce Markdown and DOCX.

If DOCX/PDF rendering is technically unavailable, still produce validated Markdown rather than failing the complete Stage 1 assessment.

Presentation failures must never cause the agent to:

- invent evidence;
- change governance status;
- suppress identified gaps;
- guess navigation targets;
- guess page numbers.

---

## Deployment and user experience

The standard Stage 1 workflow should remain straightforward for another data scientist to use after cloning or forking the repository.

Ordinary Stage 1 generation should not require the user to understand or manually operate internal rendering components.

The expected interaction should remain:

1. make the DSLC agent available to the active project;
2. request Stage 1 generation;
3. allow the agent to review project evidence;
4. answer targeted questions only where genuinely necessary;
5. receive the generated Stage 1 outputs.

Optional presentation enhancements must not introduce unnecessary setup requirements.

In particular, automatic Microsoft Word automation must not be a mandatory dependency of ordinary Stage 1 generation.

A user must not be required to install an additional Windows-specific Python package solely to make the Stage 1 evidence assessment or core document generation work.

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