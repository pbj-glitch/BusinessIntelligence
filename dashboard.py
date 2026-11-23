"""
GROUP_02 — Hip fracture among adult women (C3 storytelling dashboard)
Streamlit app built from saved C1-C2-W3 results only — no raw data file is
loaded or required. Every number below traces to a specific saved output.

Run with: python -m streamlit run dashboard.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# W3 VISUAL SYSTEM — unified palette, typography, and layout rules
# ==============================================================================
OCHRE = "#C2410C"       # Primary accent: active risk / prolonged-stay signal
OCHRE_LIGHT = "#FFEDD5" # Soft tint: false-alarm workload & callout boxes
SLATE = "#475569"       # Primary neutral: baselines & clinical/admin bars
SLATE_SOFT = "#64748B"  # Secondary neutral
SLATE_LIGHT = "#F1F5F9" # Muted cell background
MIST = "#CBD5E1"        # Subtle gridlines & borders
CANVAS = "#F8FAFC"      # Unified off-white background
INK = "#0F172A"         # Deep ink navy for titles & direct labels

plt.rcParams["figure.dpi"] = 140
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.facecolor"] = CANVAS
plt.rcParams["figure.facecolor"] = CANVAS

st.set_page_config(
    page_title="Hip Fracture Triage — Group 02",
    page_icon="🏥",
    layout="wide",
)

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {CANVAS}; }}

    [data-testid="stMain"] h1 {{ color: {INK}; font-size: 2.3rem; line-height: 1.25; }}
    [data-testid="stMain"] h2, [data-testid="stMain"] h3 {{ color: {INK}; font-size: 1.5rem; }}
    [data-testid="stMain"] p, [data-testid="stMain"] li {{ color: {SLATE}; font-size: 1.25rem; line-height: 1.7; }}
    code {{ font-size: 1.05rem; padding: 0.15rem 0.4rem; }}

    .story-hook {{
        background-color: {OCHRE_LIGHT}; border-left: 4px solid {OCHRE};
        padding: 1.1rem 1.4rem; border-radius: 0.4rem; color: {INK};
        font-size: 1.3rem; line-height: 1.6; margin-bottom: 1.2rem;
    }}
    .takeaway-box {{
        background-color: white; border: 1px solid {MIST}; border-left: 4px solid {SLATE};
        padding: 1.1rem 1.4rem; border-radius: 0.4rem; margin-top: 1rem;
        font-size: 1.25rem; line-height: 1.6;
    }}
    .takeaway-box p, .takeaway-box strong {{ color: {INK} !important; }}

    [data-testid="stSidebar"] * {{ color: var(--text-color) !important; }}
    [data-testid="stCaptionContainer"] {{ font-size: 1.0rem !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)
# ==============================================================================
# NAVIGATION — Five-Act Executive Narrative
# ==============================================================================

CHAPTERS = [
    "Act 1 · The Clinical Stakes (C1)",
    "Act 2 · The Pivot & Triage Trade-Off (C2)",
    "Act 3 · Behind the Curtain: Hospital vs. Patient (W3)",
    "Act 4 · The Generalization Trap (C3)",
    "Act 5 · Pilot Decision & Next Steps",
]


# ---- Sidebar: mode switch + cohort context only ----
mode = st.sidebar.radio("Presentation mode", ["Audience briefing (simple)", "Internal review (technical)"])
st.sidebar.markdown("### Decision Briefing")
st.sidebar.caption("For UGCC Bed Managers & Orthopedic / Geriatric Service Directors")
st.sidebar.markdown("---")
st.sidebar.caption(
    "**Cohort Scope:** 4,361 adult female hip-fracture discharges (S72.00, S72.10) "
    "across Chilean high-complexity public hospitals (FONASA, 2019–2024). "
    "All metrics trace directly to verified C1/C2/W3 outputs."
)

if mode.startswith("Internal"):
    # Internal review keeps free jump-to-any-Act navigation for Q&A
    st.sidebar.markdown("---")
    jump = st.sidebar.radio("Jump to Act", CHAPTERS, index=st.session_state.get("act_idx", 0))
    st.session_state.act_idx = CHAPTERS.index(jump)

if "act_idx" not in st.session_state:
    st.session_state.act_idx = 0

PANEL = CHAPTERS[st.session_state.act_idx]

st.progress((st.session_state.act_idx + 1) / len(CHAPTERS))
st.caption(f"Chapter {st.session_state.act_idx + 1} of {len(CHAPTERS)}")

if "act_idx" not in st.session_state:
    st.session_state.act_idx = 0


#st.markdown("---")
col_prev, col_mid, col_next = st.columns([1, 4, 1])
with col_prev:
    if st.button("← Back", disabled=st.session_state.act_idx == 0):
        st.session_state.act_idx -= 1
        st.rerun()
with col_next:
    if st.button("Next →", disabled=st.session_state.act_idx == len(CHAPTERS) - 1):
        st.session_state.act_idx += 1
        st.rerun()


def chapter_footer(prev_summary: str, next_prompt: str):
    """Consistent narrative bridge at the bottom of every chapter."""
    #st.markdown("---")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown(f"**Where we stand:** {prev_summary}")
    with c2:
        st.info(f"**Next question →** {next_prompt}")


# ==============================================================================
# ACT 1 — THE CLINICAL STAKES (C1 EDA)
# ==============================================================================
if PANEL.startswith("Act 1"):
    st.caption("ACT 1 OF 5 · SETTING THE SCENE")
    st.title("Every Year, Thousands of Older Women Are Hospitalized for Hip Fracture — Some Go Home in a Week, Others Stay Months")
    st.markdown(
        """
        <div class="story-hook">
        <strong>The Bed-Management Dilemma:</strong> Across 154,431 female public-hospital discharges (2019–2024),
        hip fracture (S72) stands out as the leading diagnosis among women aged 75+ and carries a direct
        operational lever: <em>if we knew at admission who would stay beyond 15 days, UGCC teams could activate
        home-hospitalization and rehab pathways on Day 1 instead of Day 14.</em>
        </div>
        """,
        unsafe_allow_html=True,
    )

    age_groups = ["18-29", "30-44", "45-59", "60-74", "75-89", "90+"]
    counts = [12, 17, 63, 593, 2579, 1097]
    median_los = [25.5, 22.0, 16.0, 15.0, 14.0, 13.0]
    mortality = [0.0, 5.9, 3.2, 5.9, 7.0, 10.4]

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6.2, 4.3))
        bar_colors = [OCHRE if g in {"75-89", "90+"} else SLATE_SOFT for g in age_groups]
        ax.bar(age_groups, counts, color=bar_colors, width=0.58)
        for i, v in enumerate(counts):
            ax.text(i, v + 45, f"{v:,}", ha="center", fontsize=9.5, fontweight="bold",
                    color=OCHRE if age_groups[i] in {"75-89", "90+"} else INK)
        ax.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
        ax.set_axisbelow(True)
        ax.set_title("84% of Hip Fractures Concentrate in Women 75+", fontsize=11.5, fontweight="bold", color=INK, pad=12)
        ax.set_ylabel("Hip-fracture discharges (2019–2024)", fontsize=9.5, color=SLATE)
        ax.set_ylim(0, 2950)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6.2, 4.3))
        ax2 = ax.twinx()
        ax2.spines["right"].set_visible(True)
        ax2.spines["right"].set_color(OCHRE)
        ax.bar(age_groups, median_los, color=SLATE_LIGHT, edgecolor=SLATE, width=0.5, label="Median LOS (days)")
        ax2.plot(age_groups, mortality, color=OCHRE, marker="o", linewidth=2.4, label="Mortality (%)")
        for i, v in enumerate(median_los):
            ax.text(i, v + 0.5, f"{v:.1f}d", ha="center", fontsize=8.5, color=INK)
        for i, v in enumerate(mortality):
            ax2.text(i, v + 0.55, f"{v:.1f}%", ha="center", fontsize=8.5, color=OCHRE, fontweight="bold")
        ax.set_title("Shorter Stays in the Oldest Patients Mask Rising Mortality", fontsize=11.5, fontweight="bold", color=INK, pad=12)
        ax.set_ylabel("Median length of stay (days)", fontsize=9.5, color=SLATE)
        ax2.set_ylabel("In-hospital mortality (%)", fontsize=9.5, color=OCHRE)
        ax.set_ylim(0, 30)
        ax2.set_ylim(0, 13.5)
        st.pyplot(fig)

    st.markdown(
        f"""
        <div class="takeaway-box">
        <p style="color: {INK}; margin: 0;"><strong>What the EDA reveals:</strong> On the surface, median stay drops from 25.5 days (ages 18–29) to
        13.0 days (ages 90+). That isn't faster recovery — in-hospital mortality climbs to 10.4% in the 90+
        bracket alongside higher transfers to home-hospitalization pathways. Meanwhile, <strong>42.4% of all
        episodes</strong> still exceed 15 days, tying up acute orthopedic beds.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chapter_footer(
        "4,361 hip-fracture admissions are heavily concentrated in women 75+, and 42.4% exceed 15 days.",
        "Can an admission-time model flag those prolonged stays before surgical bottlenecks build up? (Act 2)",
    )


# ==============================================================================
# ACT 2 — THE PIVOT & TRIAGE TRADE-OFF (C2 EVALUATION)
# ==============================================================================
elif PANEL.startswith("Act 2"):
    st.caption("ACT 2 OF 5 · THE MODELING PIVOT & OPERATIONAL TRADE-OFF")
    st.title("Predicting Exact Days Failed — Flagging Long Stays (>15d) Catches 89% of Cases")
    st.markdown(
        """
        <div class="story-hook">
        <strong>How the problem was reframed:</strong> Our first instinct in C2 was to predict exact length of stay
        in days. Both a Regression Tree (MAE 11.27 days) and Linear Regression lost to a trivial guess of
        "everyone stays 15 days" (baseline MAE 8.93 days). Exact stay length is too noisy at intake — so we
        pivoted to binary triage: <strong>will this stay exceed 15 days?</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tn, fp, fn, tp = 341, 909, 73, 594
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    total_flags = tp + fp

    col_left, col_right = st.columns([1.35, 1])

    with col_left:
        fig, ax = plt.subplots(figsize=(6.8, 5.0))
        cell_colors = [[SLATE_LIGHT, OCHRE_LIGHT], [SLATE_LIGHT, OCHRE]]
        cell_text_colors = [[INK, OCHRE], [SLATE, "white"]]
        cm = [[tn, fp], [fn, tp]]
        roles = [
            ["True Negative\n(Correctly Unflagged)", "False Positive\n(Early Check-In / False Alarm)"],
            ["False Negative\n(Missed Long Stay)", "True Positive\n(Caught Prolonged Stay)"],
        ]

        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(1.5, -0.5)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(
            ["Predicted <=15d\n(No Flag)", "Predicted >15d\n(Flagged for Early Discharge Plan)"],
            fontsize=9.5, fontweight="bold", color=INK,
        )
        ax.set_yticklabels(
            [f"Actual <=15d\n(n = {tn+fp:,})", f"Actual >15d\n(n = {fn+tp:,})"],
            fontsize=9.5, fontweight="bold", color=INK,
        )

        for i in range(2):
            for j in range(2):
                rect = patches.Rectangle(
                    (j - 0.48, i - 0.48), 0.96, 0.96,
                    facecolor=cell_colors[i][j],
                    edgecolor=OCHRE if j == 1 else MIST,
                    linewidth=2.0 if (i == 1 and j == 1) else 1.0,
                )
                ax.add_patch(rect)
                row_pct = cm[i][j] / sum(cm[i]) * 100
                ax.text(j, i - 0.12, f"{cm[i][j]:,}", ha="center", va="center",
                        fontsize=16, fontweight="bold", color=cell_text_colors[i][j])
                ax.text(j, i + 0.09, f"({row_pct:.1f}% of row)", ha="center", va="center",
                        fontsize=9, color=cell_text_colors[i][j])
                ax.text(j, i + 0.29, roles[i][j], ha="center", va="center",
                        fontsize=8, style="italic", color=cell_text_colors[i][j])

        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(length=0)
        ax.set_title(
            "Test Set Confusion Matrix (2023–2024, n = 1,917 · Threshold = 0.38)",
            fontsize=10.5, fontweight="bold", color=INK, pad=12,
        )
        st.pyplot(fig)

    with col_right:
        st.subheader("The Triage Trade-Off")
        m1, m2 = st.columns(2)
        m1.metric("Prolonged Stays Caught", f"{recall*100:.1f}%", "594 of 667 cases")
        m2.metric("Flagged Precision", f"{precision*100:.1f}%", f"{total_flags:,} total flags")
        st.metric("How well it ranks risk", "Good, not perfect", "Confirmed two different ways")

        st.markdown(
            """
            **Why we chose high recall over raw accuracy:**
            - A naive baseline that *never flags anyone* scores **65% accuracy** — and misses **100%** of prolonged stays.
            - Tuning the probability threshold to **0.38** on the 2022 validation set catches **89.1%** of prolonged stays (`594 / 667`), leaving only **73** unflagged long stays.
            - **Operational cost:** Bed managers must review **909 false alarms** (`72.7%` of normal stays). In hospital operations, an unnecessary Day-1 discharge check-in is cheap; an unplanned 25-day bed block is expensive.
            """
        )

    chapter_footer(
        "Reframing to binary triage catches 89.1% of prolonged stays at threshold 0.38, trading precision (39.5%) for sensitivity.",
        "Before trusting those 1,503 flags, what information is the model actually using to make them? (Act 3)",
    )


# ==============================================================================
# ACT 3 — BEHIND THE CURTAIN: HOSPITAL VS. PATIENT (W3 VISUAL SYSTEM)
# ==============================================================================
elif PANEL.startswith("Act 3"):
    st.caption("ACT 3 OF 5 · OPENING THE BLACK BOX")
    st.title("We Expected Age to Drive Risk — Instead, Which Hospital You Enter Dominates")
    st.markdown(
        """
        <div class="story-hook">
        <strong>The Honest Audit:</strong> Clinical directors naturally assume an admission risk score reflects
        patient frailty and age. When we inspected the model's weights and ran an ablation test removing
        geography, we uncovered a critical operational truth: <strong>the model is primarily learning hospital
        and regional capacity, not individual patient biology.</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_view = st.radio(
        "Inspect admission-time drivers via:",
        [
            "Which direction each factor pushes risk",
            "Which factors the computer leaned on most",   # also drop the leftover "Tree Comparison:" prefix, see below
        ],
        horizontal=True,
    )
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6.4, 4.7))
        if model_view.startswith("Which direction"):
            labels = [
                "Primary Diagnosis (ICD_SUBTYPE_TE)",
                "Same Commune (MISMA_COMUNA)",
                "Patient Commune (COMUNA_REGISTRADA_TE)",
                "Admission Type (6 INGRESO_* grouped)",
                "Patient Age (EDAD)",
                "Hospital Commune (COMUNA_ESTAB_TE)",
            ]
            vals = [0.001, -0.012, -0.018, -0.047, -0.202, 0.655]
            is_geo = [False, True, True, False, False, True]
            colors = [OCHRE if g else SLATE_SOFT for g in is_geo]

            bars = ax.barh(labels, vals, color=colors, height=0.58)
            ax.axvline(0, color=INK, linewidth=0.9)
            for idx_b, bar in enumerate(bars):
                w = bar.get_width()
                off = 0.018 if w >= 0 else -0.018
                ha = "left" if w >= 0 else "right"
                ax.text(w + off, bar.get_y() + bar.get_height() / 2, f"{w:+.3f}",
                        va="center", ha=ha, fontsize=9, fontweight="bold",
                        color=OCHRE if is_geo[idx_b] else INK)
            ax.set_xlim(-0.33, 0.80)
            ax.set_xlabel("Standardized Log-Odds Coefficient (Train Fit 2019–2021)", fontsize=9, color=SLATE)
            ax.set_title("Hospital Commune (+0.655) Dwarfs Every Clinical Variable", fontsize=11, fontweight="bold", color=INK, pad=12)
        else:
            labels = [
                "Primary Diagnosis (ICD_SUBTYPE)",
                "Admission Type (INGRESO_* grouped)",
                "Same Commune (MISMA_COMUNA)",
                "Patient Commune (COMUNA_REGISTRADA)",
                "Patient Age (EDAD)",
                "Hospital Commune (COMUNA_ESTAB)",
            ]
            vals = [0.1, 1.5, 2.3, 24.0, 28.0, 44.0]
            is_geo = [False, False, True, True, False, True]
            colors = [OCHRE if g else SLATE_SOFT for g in is_geo]

            bars = ax.barh(labels, vals, color=colors, height=0.58)
            for idx_b, bar in enumerate(bars):
                w = bar.get_width()
                ax.text(w + 0.9, bar.get_y() + bar.get_height() / 2, f"{w:.1f}",
                        va="center", ha="left", fontsize=9, fontweight="bold",
                        color=OCHRE if is_geo[idx_b] else INK)
            ax.set_xlim(0, 51)
            ax.set_xlabel("CatBoost Split Importance Score (Train Fit 2019–2021)", fontsize=9, color=SLATE)
            ax.set_title("High-Cardinality Communes Dominate Tree Splits", fontsize=11, fontweight="bold", color=INK, pad=12)

        ax.grid(axis="x", linestyle=":", color=MIST, linewidth=0.7)
        ax.set_axisbelow(True)
        st.pyplot(fig)
        st.caption(
            "Burnt Ochre = Geographic / institutional proxy features | Clinical Slate = Patient & admission features."
        )

    with col2:
        fig, ax = plt.subplots(figsize=(6.4, 4.7))
        models = ["Full Admission Model\n(With Commune Geography)", "No-Geography Model\n(Clinical & Admin Only)"]
        aucs = [0.675, 0.525] if model_view.startswith("Selected") else [0.661, 0.535]
        auc_drop = aucs[0] - aucs[1]
        drop_pct = auc_drop / (aucs[0] - 0.5) * 100

        bars = ax.bar(models, aucs, color=[OCHRE, SLATE_SOFT], width=0.40)
        ax.axhline(0.500, color=INK, linestyle="--", linewidth=1.1)
        ax.text(0.50, 0.512, "Random Chance Baseline (0.500)", ha="center", fontsize=6.0, fontweight="bold", color=INK)

        for idx_b, bar in enumerate(bars):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.015, f"{h:.3f}",
                    ha="center", fontsize=11.5, fontweight="bold",
                    color=OCHRE if idx_b == 0 else SLATE)

        ax.annotate(
            f"−{auc_drop:.3f} AUC (−{drop_pct:.0f}% of lift)\nwithout geography",
            xy=(0.82, aucs[1] + 0.01), xytext=(0.68, 0.64),
            ha="center", fontsize=8.8, fontweight="bold", color=OCHRE,
            bbox=dict(boxstyle="round,pad=0.35", facecolor=OCHRE_LIGHT, edgecolor=OCHRE, linewidth=0.9),
            arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2),
        )

        ax.set_ylim(0, 0.78)  # Strict zero-baseline per W3 visual system
        ax.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
        ax.set_axisbelow(True)
        ax.set_ylabel("Validation ROC-AUC (2022, n = 914)", fontsize=9.5, color=SLATE)
        ax.set_title(f"Removing Geography Eliminates {drop_pct:.0f}% of Discriminative Lift", fontsize=11, fontweight="bold", color=INK, pad=12)
        st.pyplot(fig)
        st.caption(
            "Validation-set ablation proves commune identity is not just a split artifact — without it, accuracy collapses near 0.500."
        )

    st.markdown(
        f"""
        <div class="takeaway-box">
        <p style="color: {INK}; margin: 0;">
        <strong style="color: {INK};">What this means in practice:</strong> Two clinically identical 82-year-old
        women receive very different risk scores depending on which hospital they enter. Age also carries a
        negative standardized coefficient, consistent with older patients experiencing higher early mortality
        and faster transfer to home-hospitalization rather than prolonged inpatient stays.
        </p>
        </div>
        """,
    unsafe_allow_html=True,
    )

    chapter_footer(
        "85% of the model's discriminative lift comes from hospital/commune identity rather than patient clinical intake fields.",
        "What happens if we add post-admission clinical severity & comorbidities to make the model 'patient-driven'? (Act 4)",
    )


# ==============================================================================
# ACT 4 — THE GENERALIZATION TRAP (C3 EXPERIMENT)
# ==============================================================================
elif PANEL.startswith("Act 4"):
    st.caption("ACT 4 OF 5 · TESTING THE OBVIOUS FIX")
    st.title("Adding Clinical Comorbidities Looked Great in Validation — Then Failed on Test")
    st.markdown(
        """
        <div class="story-hook">
        <strong>Testing the C2 Hypothesis:</strong> Our C2 conclusion asked whether adding clinical severity
        and comorbidity scores (<code>INDICE_CHARLSON</code>, <code>N_COMORBILIDADES</code>) would shift the model
        from "predicts the hospital" to "predicts the patient." In C3, we tested that exact expansion — and
        uncovered a classic temporal distribution-shift trap.
        </div>
        """,
        unsafe_allow_html=True,
    )

    choice = st.radio(
        "Compare feature sets across validation (2022) and test (2023–2024):",
        [
            "At Admission Only (Age, Location, Admission Type — Generalizes)",
            "After Admission (+ Comorbidities & Severity — Overfits Historical Distribution)",
        ],
        horizontal=True,
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        mae_table = pd.DataFrame({
            "Model": ["Median Baseline", "At Admission\n(Location + Age)", "After Admission\n(+ Comorbidities)"],
            "Validation MAE (2022)": [11.75, 11.02, 10.43],
            "Test MAE (2023–2024)": [8.93, 8.58, 9.13],
        })

        fig, ax = plt.subplots(figsize=(6.8, 4.4))
        x = np.arange(3)
        w = 0.35
        bars_val = ax.bar(x - w / 2, mae_table["Validation MAE (2022)"], width=w,
                          color=SLATE_LIGHT, edgecolor=SLATE, label="Validation (2022)")
        bars_test = ax.bar(x + w / 2, mae_table["Test MAE (2023–2024)"], width=w,
                           color=[SLATE_SOFT, OCHRE, "#991B1B"], label="Test (2023–2024)")

        for bars in (bars_val, bars_test):
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.18, f"{h:.2f}d",
                        ha="center", fontsize=9, fontweight="bold", color=INK)

        ax.set_xticks(x)
        ax.set_xticklabels(mae_table["Model"], fontsize=9.2, color=INK)
        ax.set_ylabel("Mean Absolute Error (days)", fontsize=9.5, color=SLATE)
        ax.set_ylim(0, 13.8)
        ax.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
        ax.set_axisbelow(True)
        ax.set_title("The Comorbidity Model Wins on Validation (10.43d) but Loses on Test (9.13d)",
                     fontsize=10.8, fontweight="bold", color=INK, pad=12)
        ax.legend(frameon=False, fontsize=9, loc="upper right")
        st.pyplot(fig)

    with col2:
        drift_df = pd.DataFrame({
            "Period": ["2022\n(Validation)", "2023–2024\n(Test)"],
            "Median Charlson Index": [1.0, 2.0],
            "Median Comorbidities": [9, 10],
        })
        fig2, ax2 = plt.subplots(figsize=(5.6, 4.4))
        ax2b = ax2.twinx()
        ax2b.spines["right"].set_visible(True)
        ax2b.spines["right"].set_color(SLATE_SOFT)

        ax2.plot(drift_df["Period"], drift_df["Median Charlson Index"], marker="o", markersize=8,
                 color=OCHRE, linewidth=2.5, label="Median Charlson Index")
        ax2b.plot(drift_df["Period"], drift_df["Median Comorbidities"], marker="s", markersize=8,
                  color=SLATE_SOFT, linewidth=2.5, linestyle="--", label="Median Comorbidities")

        for i, v in enumerate(drift_df["Median Charlson Index"]):
            ax2.text(i, v + 0.14, f"{v:.1f}", ha="center", fontsize=10, fontweight="bold", color=OCHRE)
        for i, v in enumerate(drift_df["Median Comorbidities"]):
            ax2b.text(i, v + 0.45, f"{v}", ha="center", fontsize=10, fontweight="bold", color=SLATE_SOFT)

        ax2.set_xlim(-0.35, 1.35)
        ax2.set_ylim(0, 2.8)
        ax2b.set_ylim(0, 13)
        ax2.set_ylabel("Median Charlson Index", color=OCHRE, fontsize=9.5)
        ax2b.set_ylabel("Median Comorbidity Count", color=SLATE_SOFT, fontsize=9.5)
        ax2.set_title("Why It Failed: Comorbidity Burden Shifted in 2023–2024",
                      fontsize=10.8, fontweight="bold", color=INK, pad=12)
        st.pyplot(fig2)

    if choice.startswith("At Admission"):
        st.success(
            "**At Admission (Recommended for Pilot):** Using only age, location, and admission type beats the "
            "median baseline on **both** validation (`11.02` vs. `11.75` days) and the untouched 2023–2024 test set "
            "(`8.58` vs. `8.93` days). Crucially, these fields are genuinely recorded at the intake desk."
        )
    else:
        st.warning(
            "**After Admission (Why We Rejected It):** Adding `N_COMORBILIDADES` (which received the largest single "
            "weight, `0.247`) and `INDICE_CHARLSON` improved 2022 validation error to `10.43` days — but degraded "
            "2023–2024 test error to **`9.13` days** (worse than guessing the median `8.93`). Recorded comorbidity "
            "burden doubled in median Charlson score (`1.0 → 2.0`) between 2022 and 2023–2024, causing a static "
            "model trained on 2019–2021 to systematically over-predict stays."
            "Moreover, whether GRD comorbidity fields are available at admission or only finalized at discharge "
            "remains unconfirmed in the documentation available to this team — flagged as an open question since W2, not assumed either way."
        )

    chapter_footer(
        "Simpler admission-only features generalize across years (8.58d vs. 8.93d baseline), whereas discharge-coded comorbidities suffer from temporal drift.",
        "How should UGCC directors deploy this tool responsibly — and what comes next? (Act 5)",
    )


# ==============================================================================
# ACT 5 — PILOT DECISION, LIMITS & NEXT STEPS
# ==============================================================================
else:
    st.caption("ACT 5 OF 5 · EXECUTIVE RECOMMENDATION & GUARDRAILS")
    st.title("Which Hospital You're Admitted To Matters More Than Almost Anything Else We Checked")
    st.markdown(
        """
        We tested this two different ways — both agreed: once we remove information about which
        hospital and area a patient comes from, the tool's ability to tell high-risk from low-risk
        patients almost disappears. Removing that information cut its accuracy by roughly 80%,
        consistently across both methods we tried.
        """
    )
    st.markdown(
        """
        <div class="story-hook">
        <strong>Executive Recommendation for UGCC & Service Directors:</strong> Pilot the admission-time binary
        flagging tool (<strong>threshold = 0.38</strong>) specifically in high-volume hospitals with chronic
        surgical/discharge bottlenecks to trigger <strong>early social-work and home-hospitalization screening</strong> —
        while explicitly prohibiting its use for individual clinical rationing.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 1 · What It Is Good For")
        st.markdown(
            """
            - **Early discharge coordination:** Captures **89.1%** of >15-day episodes on Day 1 (`594 / 667`), giving liaison nurses a two-week head start on home-care logistics.
            - **Network capacity allocation:** Identifies which establishments systematically experience prolonged stays so UGCC can target regional post-acute bed expansion.
            """
        )

    with c2:
        st.markdown("#### 2 · Honest Guardrails")
        st.markdown(
            f"""
            - **Institutional proxy bias:** Roughly 80% of the tool's ranking power comes from hospital and
            location identity, confirmed two different ways. Two clinically identical patients can get
            very different risk scores depending only on which hospital they're admitted to.
            - **High false-alarm volume:** Flags <code>1,503</code> of <code>1,917</code> patients
            (<code>78%</code>), requiring a lightweight screening workflow rather than intensive case
            management for every flag.
            - **Untested over time:** We have not yet checked whether the tool's accuracy is stable from
            year to year — before a pilot, we would validate it on the most recent discharges and
            recalibrate if needed.
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown("#### 3 · Concrete Next Steps")
        st.markdown(
            """
            1. **Rolling threshold recalibration:** Re-tune the decision threshold quarterly on the trailing 6 months of discharges to keep false-positive volume aligned with nurse staffing.
            2. **True intake clinical fields:** Capture pre-operative ASA physical status and time-to-surgery targets at admission (rather than discharge-coded GRD comorbidities) to add genuine patient-level risk without temporal drift.
            3. **Expand cohort scope:** Benchmark against male hip-fracture admissions and medium-complexity hospitals before national scaling.
            """
        )

    st.markdown("---")
    st.caption(
        "**Process & AI Usage Disclosure:** Built from verified C1, C2, and W3 notebook outputs by Group 02 "
        "(Lukas Garrido & Maria Poddubnaya). Generative AI (Gemini) assisted with Streamlit layout structuring "
        "and visual system styling; all cohort numbers, model metrics, and analytical conclusions trace directly "
        "to our audited project notebooks."
    )