# GROUP_02_C1 — Hip fracture among adult women in the Chilean public health system

## Team

| Member | Role in this submission |
|---|---|
| Maria Poddubnaya | C1 EDA and analysis, report assembly|
| Lukas Garrido | W1 EDA and analysis, report assembly |

Group ID: 02
Submission: C1 — Business Intelligence (IIB423T-1)
Date/version: 01 October 2026, v1.0
Course: IIB423T-1, Universidad del Desarrollo — Instructor: Carlos Elías Pérez Pizarro

## What this project is

An investigation of hip fracture (ICD-10 S72.00, S72.10) among adult women in the
Chilean public high-complexity hospital network (Fonasa GRD data, 2019–2024),
narrowed from the broader "female hospitalizations" scope of W1 in response to
instructor feedback. Full problem statement, methodology and findings are in
`report/GROUP_02_C1_Report.pdf` — that PDF is self-contained and should be read
first; this file only documents how to reproduce the analysis behind it.

## Folder structure and file roles

```
GROUP_02_C1/
├── README.md                          — this file
├── report/
│   └── GROUP_02_C1_Report.pdf         — self-contained report; read this first
├── analysis/
│   └── GROUP_02_C1_Analysis.ipynb             — full analysis notebook, executed top-to-bottom
│                                         with saved outputs (tables, figures)
├── data/
│   ├── grd_procesado.parquet  — [main dataset]
│    
└── presentation/
    └── BI- C1.pdf         — presentation slides (PDF export)
```


## How to run `analysis/c1MariaLukas.ipynb`

1. Open the notebook in Jupyter (or VS Code / JupyterLab with a Python kernel).
2. Ensure the input parquet referenced by the first cell is present at the relative
   path used in the notebook (`data/...`) — update the path if your working copy
   differs, since the notebook uses project-relative paths, not absolute ones.
3. **Restart the kernel and run all cells top to bottom.** The submitted notebook
   was executed this way before export; do not run cells out of order.

### Order of operations inside the notebook
1. Load raw parquet → inspect structure, dtypes, coverage.
2. Clean: duplicate check and removal, missing-value/placeholder inspection.
3. Filter to adult women (`EDAD >= 18`), build `GRUPO_ETARIO` age bins.
4. Filter to hip-fracture cohort (`DIAGNOSTICO1` in S72.00, S72.10).
5. Five Cs checks: join-key verification (`COMUNA_ESTAB`/`COMUNA_REGISTRADA`),
   severity-coding stability by year, establishment-count normalization.
6. EDA: diagnosis/age distribution, LOS, mortality, discharge destination,
   Charlson-tier mortality, year-over-year and sex-comparison analysis.
7. W1 EDA work
8. Misc calculation

## Software and dependencies

- Python: 3.11
- Core libraries: pandas, numpy, matplotlib
- No external API keys or connectors are required to run the notebook as submitted.

## Data

### Source and version
The analysis uses a pre-joined parquet combining:
- Base de Datos GRD Fonasa, 2019–2024
- Base de Establecimientos de Salud (DEIS)
- Dotación de Camas Hospitalarias (DEIS)
- Estimación Población 2002–2035 (INE)
- Estimaciones de Pobreza Comunal 2024 (MINDESOF)
