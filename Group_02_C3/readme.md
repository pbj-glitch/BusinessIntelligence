# Predicting Prolonged Hospital Stay (>15 Days) at Admission for Adult Female Hip-Fracture Patients

**Course / Deliverable:** C3 Final Submission — Group 02  
**Domain:** Clinical Operations & Hospital Discharge Planning (Chilean Public Healthcare / FONASA GRD Dataset, 2019–2024)

---

## 1. Research Question & Clinical Motivation

> **Can admission-time demographic, geographic, and clinical-pathway variables predict whether an adult female hip-fracture patient will experience a prolonged hospital stay ($>15\text{ days}$) early enough to support proactive discharge planning and home-hospitalization coordination?**

Hip fractures in adult women represent a high-burden acute care pathway in Chile's public hospital network. Across the 4,361 verified adult female hip-fracture episodes recorded between 2019 and 2024, **42.4% ($n = 1,847$)** required a prolonged hospital stay exceeding 15 days. Identifying high-risk episodes at the moment of admission—without relying on post-discharge diagnostic or severity codes—enables clinical teams to initiate early social work, rehabilitation, and home-hospitalization pathways (`Hospitalización Domiciliaria`), which expanded from 7.0% of discharges in 2019 to 23.3% in 2024.

---

## 2. Team Members (Group 02)

* **[Maria Poddubnaya]**
* **[Lukas Garrido]**
---

## 3. Repository Structure & Recommended Reading Order

To review this project efficiently, please follow the numbered reading order below:

```text
GROUP_02_C3_Submission/
├── README.md                                  # [1] Project overview, reading guide & setup notes (this file)
├── presentations/
│   ├── dashboard.py

├── notebooks/
│   └── GROUP_02_W3.ipynb       # [4] Full analysis & modeling notebook (all outputs saved)
```

### File Roles
1. **`README.md`**: Entry point summarizing the research question, team roles, repository map, software stack, and zero-execution review instructions.
2. **`presentations/Presentation_1_External_Audience.pdf`**: Plain-language presentation designed for hospital administrators and orthopedic/geriatric care coordinators, translating model thresholds into bed-capacity and home-hospitalization workflows.
3. **`presentations/Presentation_2_Internal_Review.pdf`**: Technical deep dive covering the strict temporal split (`2019–2021` train, `2022` validation, `2023–2024` test), leakage prevention, validation-only model selection, and methodological limitations.
4. **`notebooks/GROUP_02_C2_classification.ipynb`**: Complete Python analytical workflow—from cohort scoping and admission-safe feature engineering to validation model comparison (Logistic Regression vs. CatBoost) and single-shot test evaluation—saved with all cell outputs and figures intact.
5. **`visual_system/generate_charts.py` & `dashboard.html`**: Reproducible visualization code and interactive view built exclusively from saved summary tables and model evaluation metrics (zero patient-level records).
6. **`visual_system/screenshots/`**: High-resolution `.png` captures of every figure and every interactive dashboard state for immediate visual inspection.

---

## 4. Data Privacy & Zero-Setup Guarantee

* **No Raw Data Included:** In compliance with data governance and repository guidelines, no raw patient-level files (`grd_procesado.parquet` or `.csv` extracts) are included in this repository.
* **No Re-Execution Required:** Every code cell, summary table, metric printout, and `matplotlib` figure inside `notebooks/GROUP_02_C2_classification.ipynb` is pre-executed and saved in place. All visual system charts and interactive dashboard states are pre-rendered as static images in `visual_system/screenshots/`. Reviewers do not need to download external datasets or run any scripts to inspect the full submission.

---

## 5. Software & Library Environment

If you wish to inspect or run the standalone visualization code using the embedded summary metrics, the project was developed and tested with:

* **Python:** `3.11+`
* **Core Data & Modeling Libraries:**
  * `pandas` (`>=2.0`)
  * `numpy` (`>=1.24`)
  * `scikit-learn` (`>=1.3`)
  * `catboost` (`>=1.2`)
  * `pyarrow` (`>=14.0`, used during local Parquet ingestion only)
* **Visualization:**
  * `matplotlib` (`>=3.7`)
* **Running the dashboard**
'''bash
python -m streamlit run dashboard.py

'''

---

## 6. Key Methodological Guardrails & Summary Findings

* **Cohort & Temporal Split:** 4,361 adult female hip-fracture admissions (`2019–2024`), partitioned strictly by discharge year into **Train-Fit (`2019–2021`, $n = 1,530$)**, **Validation (`2022`, $n = 914$)**, and **Holdout Test (`2023–2024`, $n = 1,917$)**, with documented patient-ID (`CIP_ENCRIPTADO`) overlap audits across periods.
* **Strict Admission-Time Feature Discipline:** Post-discharge variables (`TIPO_ALTA`, `IR_29301_COD_GRD`, `IR_29301_PESO`, procedures, secondary diagnoses) and variables whose admission-time availability could not be guaranteed (`IR_29301_SEVERIDAD`, `INDICE_CHARLSON`, `N_COMORBILIDADES`) were excluded to prevent target leakage.
* **Validation-Only Model Selection:** On the 2022 validation set, L2-regularized Logistic Regression (`ROC AUC = 0.675`) outperformed CatBoost (`ROC AUC = 0.661`) and was selected prior to inspecting the 2023–2024 test set.
* **Known Limitations Documented:** Includes structural circularity of `COMUNA_ESTAB` (derived from hospital facility identifiers rather than an independent geographic attribute) and prior descriptive visibility into 2023–2024 aggregate trends during C1 exploration.