# Evidence Rules

## Core rule

Always review all available project evidence before asking the user for information.

Do not ask questions where the answer can reasonably be verified from supplied evidence.

The agent's role is to locate, assess and trace evidence before generating Stage 1 documentation.

---

## Evidence source priority

Use the most authoritative source for the type of information being assessed.

### Business information

Prefer:

1. Use Case Shaping / approved business documentation
2. Solution Design
3. README
4. Explicit user clarification

Use these sources for information such as:

- business problem
- scope
- expected value
- stakeholders
- Product Owner / business ownership
- success criteria

Do not derive business ownership or approval from technical implementation evidence.

---

### Technical implementation

Prefer:

1. Training / feature engineering / scoring notebooks
2. Production code or pipeline configuration
3. Technical design documentation
4. README
5. Explicit user clarification

Use these sources for information such as:

- datasets
- features
- preprocessing
- model type
- training approach
- scoring approach
- technical dependencies
- production implementation

For determining what was actually implemented, direct implementation evidence should normally be preferred over summary documentation.

---

### Validation

Prefer:

1. Validation notebook
2. Training notebook containing explicit validation evidence
3. Modelling report
4. Explicit user clarification

Use these sources for information such as:

- holdout validation
- out-of-time validation
- cross-validation
- final validation metrics
- reproducibility checks
- scoring verification

Do not treat training performance alone as validation evidence.

---

### Governance

Use only explicit governance evidence.

Examples include:

- approval records
- AI Inventory reference
- Data Governance approval
- sign-off records
- governance questionnaires
- risk acceptance records
- formal review evidence

Never infer governance completion from technical work.

Never infer approval because a model exists, has good performance or is already in production.

---

## Example

To determine model type:

1. Check the training notebook.
2. Check implementation code or the model pipeline.
3. Check the validation notebook where relevant.
4. Check the README.
5. Ask the user only if the model type is still unclear.

Do not ask the user for information already supported by project evidence.

---

## Missing evidence

If required information cannot be verified:

1. identify exactly what information or evidence is missing;
2. record which relevant evidence sources were checked;
3. determine the appropriate status using `knowledge/governance_rules.md`;
4. explain what evidence or clarification would resolve the gap.

Do not automatically assume that missing evidence always means PENDING.

For conditional requirements, the governance rules may determine that the item is NOT APPLICABLE where the condition genuinely does not apply.

---

## Conflicting evidence

If sources disagree:

1. identify the conflict;
2. do not silently merge contradictory information;
3. prefer direct implementation evidence for what was actually built;
4. prefer formal approved documentation for ownership, governance and approvals;
5. ask the user where ambiguity remains.

Record unresolved material conflicts in the generated Stage 1 draft.

---

## Evidence traceability

For every major Stage 1 requirement, the agent should be able to identify:

- the evidence source used;
- what that evidence demonstrates;
- whether the evidence is sufficient;
- what remains missing, if anything;
- where the evidence can be located, where this can be verified.

This evidence assessment should be completed before the final Stage 1 document is written.

The Evidence Register is the authoritative location for recording evidence sources and evidence locations.

Do not repeat detailed evidence links throughout the main report unless a direct link materially improves review.

---

## Evidence location and link rules

Where possible, preserve a traceable location for each major evidence source.

Evidence locations may include:

- a verified GitHub link;
- an explicit SharePoint, Confluence, Databricks or other supplied URL;
- a verified relative workspace path;
- another explicit project evidence location.

Use the following priority order:

1. an explicit evidence URL already supplied in the project evidence;
2. a verified GitHub URL returned by `tools/resolve_evidence_link.py`;
3. a verified relative workspace path returned by `tools/resolve_evidence_link.py`;
4. `Location not available` where no location can be verified.

For local project files, use `tools/resolve_evidence_link.py` to determine the evidence location.

Do not manually construct a GitHub URL.

Do not guess:

- GitHub organisation;
- repository name;
- branch name;
- commit;
- file path;
- SharePoint location;
- Confluence location;
- Databricks location;
- document URL.

A clickable link may only be used where the location is explicitly supplied or returned as verified by the evidence-link resolver.

If the resolver cannot establish a safe GitHub link but confirms the local file path, record the verified relative path instead.

If neither a verified URL nor verified path can be established, use:

`Location not available`

Do not create a hyperlink simply because a filename appears in project documentation.

Do not present an unverified URL as project evidence.

---

## GitHub evidence links

Where project evidence is stored in the active Git repository, the agent may use `tools/resolve_evidence_link.py` to obtain a verified GitHub location.

The resolver should be treated as authoritative for GitHub link creation.

Use exactly the location returned by the resolver.

Do not rewrite, shorten, reconstruct or infer the returned URL.

If the resolver returns only a relative path, use that path rather than attempting to create a GitHub link.

If the evidence file is not available in the verified repository version, do not claim that it can be opened in GitHub.

---

## External evidence links

Where project evidence explicitly contains a valid external URL, preserve that URL.

Examples may include:

- SharePoint documents;
- Confluence pages;
- Databricks notebooks;
- governance systems;
- approved project documentation.

The agent must not invent or predict an external URL based on a document title, folder name or organisation convention.

Where an external document is referenced but no explicit URL is available, record the document name and use:

`Location not available`

---

## Reference material

Reference examples and templates are never project evidence.

They may be used only for:

- structure
- style
- terminology
- expected level of detail

Never copy project-specific facts from reference material.

Reference documents must not be used as the evidence location for active project facts.

---

## General evidence rules

Never:

- invent evidence;
- invent metrics;
- invent owners;
- invent approvals;
- estimate missing project values;
- treat general Data Science knowledge as project evidence;
- invent evidence paths;
- invent evidence URLs;
- construct unverified repository links.

When evidence is uncertain, make the uncertainty visible rather than hiding it.