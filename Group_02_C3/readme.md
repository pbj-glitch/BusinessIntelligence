# Business Intelligence Project (C3): Predicting Surgical Waiting List Outcomes in Chile

**Course:** Business Intelligence (IIB423T-1) — Universidad del Desarrollo  
**Assessment:** C3 — Explain and Defend Your BI Study  
**Group:** Group 02  
**Team Members:** Maria Poddubnaya and Lukas Garrido 

---

## 1. Research Question & Project Scope

**Core Business & Policy Question:**  
> *Can routinely collected administrative admission records predict whether a non-GES elective surgery patient in Chile's public healthcare system (FONASA) will exit the waiting list within 180 days (binary classification) and estimate expected waiting duration (regression), without relying on geographic proxies?*

* **Unit of Analysis (1 Row):** One non-GES elective surgical referral episode (`ID_CASO` / patient-episode record).
* **Dataset Provenance & Period:** Official Chilean Ministry of Health (MINSAL) Non-GES Waiting List open administrative records (2022–2024 cohort; $N = 148,320$ total clean analytical records split chronologically/stratified into Train, Validation, and Hold-out Test sets).
* **Data Policy Compliance:** In strict compliance with C3 submission rules, **no raw, curated, or extracted data files (`.csv`, `.parquet`, `.xlsx`) are included in this repository**. All provenance links, summary statistics, and distributions are preserved inside the executed notebooks.

---

## 2. Methodological Evolution & Traceability (C2 $\rightarrow$ C3)

A central focus of this final C3 repository is documenting how instructor feedback from **C2** reshaped our analytical pipeline and final modeling conclusions:

1. **C2 Baseline Pipeline (`notebooks/GROUP_02_C2_classification.ipynb`):**
   * Included geographic target-encoded features (`COMUNA_REGISTRADA_TE`, `COMUNA_ESTAB_TE`, `MISMA_COMUNA`) while excluding clinical comorbidity counts (`N_COMORBILIDADES`, `INDICE_CHARLSON`) out of initial caution regarding post-admission recording.
   * Under that setup, regularized **Logistic Regression** achieved the strongest generalization (`Val AUC = 0.675`, `Test AUC = 0.669`).
2. **Instructor Feedback & C3 Revision (`notebooks/GROUP_02_C3_final.ipynb` & `presentations/dashboard_5.py`):**
   * Following C2 feedback, we identified that geographic encodings (`COMUNA_*`) act as structural capacity proxies that mask clinical urgency and risk institutional bias when used for triage prioritization.
   * In C3, we **removed all geographic variables** (`0` geographic features) and incorporated validated admission-level clinical burden indicators (`N_COMORBILIDADES`, `INDICE_CHARLSON`).
   * **Updated C3 Findings:** Without geographic shortcuts, non-linear gradient boosting (**CatBoost Classifier**) outperformed linear baselines (`Val AUC = 0.650`, `Test AUC = 0.672`, compared to Majority Baseline `AUC = 0.500`). Additionally, we paired classification with a **Wait-Time Regression** diagnostic (`MAE = 112.4 days`, `RMSE = 148.9 days`) to quantify scheduling uncertainty for hospital managers.

---

## 3. Repository Structure & Reading Order

The reviewer does **not** need to install libraries, download external datasets, or re-run code. All notebooks are saved with complete pre-executed outputs, and static views of the interactive dashboard are archived in `visual_system/screenshots/`.

### Recommended Reading Order
1. **`README.md` (This file):** Project overview, C2-to-C3 methodological traceability, and pipeline navigation.
2. **`notebook/GROUP_02_C3_final.ipynb`:** Revised C3 pipeline (geography removed, comorbidity features validated, CatBoost classification + wait-time regression, and error/fairness limits).
4. **`presentation/dashboard_5.py` & `visual_system/screenshots/`:** Interactive Streamlit decision-support prototype and static pre-rendered screenshots for offline inspection.


### Directory Tree
```text
├── README.md
├── notebook/
│   ├── GROUP_02_C3.py
├── presentation/
│   ├── dashboard.py                     # Interactive Streamlit dashboard (no-geography model) with Audience-facing deck and Instructor review deck
└── visual_system/
    ├── style_config.py                    # Shared color palette, typography, and chart rules
    └── screenshots/                       # Static captures of interactive dashboard views
        ├── 01_executive_overview.png
        ├── 02_model_comparison.png
        └── 03_triage_simulator.png
```

---

## 4. Visual System & Design Rules

To guarantee visual consistency across notebooks, the Streamlit dashboard, and both slide decks (Rubric Criteria C & E), all charts adhere to a unified semantic color and encoding system:

* **Primary / Model Highlight (Deep Navy):** `#1E3A8A` — Used for the selected C3 CatBoost model and primary KPIs.
* **Alert / High-Risk Threshold (Warm Amber):** `#D97706` — Used for $>180$-day prolonged wait risk and critical clinical bottlenecks.
* **Reference / Baseline (Neutral Slate):** `#94A3B8` — Used for dummy/majority baselines, C2 reference comparisons, and secondary gridlines.
* **Accessibility & Clarity:** All visual comparisons pair color with direct data labels, clear units (`days`, `ROC-AUC`, `% of cohort`), and distinct marker/line styles so distinctions remain legible without relying on color alone.

---

## 5. Software Environment & Reproducibility

All analytical notebooks and visual artifacts were produced using:
* **Python:** `3.10+`
* **Core Libraries:** `pandas (2.x)`, `numpy`, `scikit-learn (1.3+)`, `catboost (1.2+)`, `matplotlib`, `seaborn`, `plotly`, `streamlit`

*(Optional)* To launch the interactive dashboard locally:
```bash
pip install streamlit pandas numpy plotly
streamlit run presentations/dashboard_5.py
```

---

## 6. AI Usage Disclosure (Course Policy)

In accordance with the IIB423T-1 course policy:
* Generative AI tools (LLM assistants) were used strictly for **code refactoring, Streamlit UI layout structuring, and editorial proofreading** of markdown/slide text.
* All research questions, data cleaning logic, feature selection decisions (including the C2 $\rightarrow$ C3 removal of geographic variables), model validation, and analytical interpretations were designed, executed, and verified directly by the team members.