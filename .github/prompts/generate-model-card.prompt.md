# Generate DSLC Model Card

Generate the Model Card for the active Data Science project.

Follow the repository-wide DSLC instructions and the Model Card requirements.

## Mandatory sources

Before generating the Model Card, review:

1. `knowledge/model_card_requirements.yaml`
2. `knowledge/evidence_rules.md`
3. `knowledge/governance_rules.md`
4. `templates/model_card_template.html`

Reference examples may be consulted for layout only.

Never use example Model Cards as project evidence.

---

## Workflow

### Step 1 — Review available project evidence

Review all relevant active-project evidence before asking the user questions.

Evidence may include:

- project README;
- Use Case Shaping;
- Solution Design;
- training notebooks;
- validation notebooks;
- scoring notebooks;
- production code;
- governance documentation;
- approved business documentation;
- explainability artefacts.

Do not ask the user for information that can reasonably be verified from project evidence.

---

### Step 2 — Determine Model Card fields

Assess the evidence for:

- model name;
- model version;
- model type;
- technical target variable;
- approved business-language target description;
- eligibility;
- model owner;
- ROC AUC;
- model description;
- explainability evidence;
- governance status.

Use `PENDING` where required information cannot be verified.

Never invent missing information.

---

### Step 3 — Assess explainability evidence

Accepted explainability evidence:

- SHAP summary plot;
- feature-importance plot;
- verified numeric feature-importance table;
- user-provided PNG/JPG explainability graphic.

Selection rules:

1. Use an artefact explicitly approved or selected by the user first.
2. If exactly one valid artefact exists, use it.
3. If multiple valid artefacts exist and none is approved, use `SELECTION REQUIRED`.
4. If no valid artefact exists, use `PENDING`.
5. Do not automatically prefer SHAP over other valid evidence.
6. Never invent explainability values.

---

### Step 4 — Create structured Model Card data

Create:

`output/model_card_data.json`

Only include values supported by evidence.

The JSON should contain the fields required by the Model Card renderer.

Missing values must be represented explicitly rather than guessed.

---

### Step 5 — Validate

Run:

`python tools/validate_model_card.py output/model_card_data.json`

If validation fails:

- correct evidence-mapping or structural issues;
- do not invent information simply to make validation pass.

---

### Step 6 — Render

Run:

`python tools/render_model_card.py`

The renderer must use:

`templates/model_card_template.html`

and:

`output/model_card_data.json`

The renderer must not independently change project facts or governance conclusions.

---

## Output

Generate:

- completed HTML Model Card;
- PDF where supported;
- Evidence Summary;
- Missing Fields;
- Recommended Actions.

The Model Card remains a draft for human review.

Do not represent the Model Card as approved or signed off.