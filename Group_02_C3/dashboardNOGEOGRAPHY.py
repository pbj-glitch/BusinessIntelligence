"""
GROUP_02 — Hip fracture among adult women (C3 storytelling dashboard)
Streamlit app built from saved C1-C2-W3 results only — no raw data file is
loaded or required. Every number below traces to a specific saved output.

Run with: python -m streamlit run dashboardNOGEOGRAPHY_2.py
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

    .persona-card {{
        background-color: white; border: 1px solid {MIST}; border-top: 5px solid {OCHRE};
        padding: 1.4rem 1.6rem; border-radius: 0.5rem; margin-bottom: 1.2rem;
    }}
    .factor-card {{
        background-color: white; border: 1px solid {MIST}; border-left: 4px solid {OCHRE};
        padding: 1.1rem 1.3rem; border-radius: 0.4rem; height: 100%;
    }}

    [data-testid="stSidebar"] * {{ color: var(--text-color) !important; }}
    [data-testid="stCaptionContainer"] {{ font-size: 1.0rem !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# NAVIGATION — Dual-Register Five-Act Narrative (Audience vs. Internal Review)
# ==============================================================================
CHAPTERS_BY_MODE = {
    "audience": [
        "Act 1 · Why Early Discharge Planning Matters",
        "Act 2 · The Value of Patient-Only Screening",
        "Act 3 · Meet Ana: Correcting Our First Audit",
        "Act 4 · Can We Predict the Exact Day? (A Harder Test)",
        "Act 5 · Bringing Early Triage to the Ward",
    ],
    "internal": [
        "Act 1 · Cohort EDA & Censoring Bias (C1)",
        "Act 2 · Regression-to-Classification Pivot (C2)",
        "Act 3 · Feature Attribution & Geography Ablation (W3)",
        "Act 4 · Post-Admission Comorbidities & Temporal Drift (C3)",
        "Act 5 · Deployment Governance & Audit Summary",
    ],
}

if "act_idx" not in st.session_state:
    st.session_state.act_idx = 0

# ---- Sidebar: mode switch + cohort context ----
mode = st.sidebar.radio(
    "Presentation mode",
    ["audience", "internal"],
    format_func=lambda x: {
        "audience": "Audience briefing (clinical & operational)",
        "internal": "Internal review (technical & C3 audit)",
    }[x],
)

CHAPTERS = CHAPTERS_BY_MODE[mode]

st.sidebar.markdown("### Decision Briefing" if mode == "audience" else "### C3 Technical Audit")
st.sidebar.caption(
    "For UGCC Bed Managers & Orthopedic / Geriatric Service Directors"
    if mode == "audience"
    else "For Data Science Evaluation & Methodological Traceability (C1–C3)"
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "**Cohort Scope:** 4,361 adult female hip-fracture discharges (S72.00, S72.10) "
    "across Chilean high-complexity public hospitals (FONASA, 2019–2024). "
    "All metrics trace directly to verified C1/C2/W3 outputs. \n"
    "Team members: Lukas Garrido, Maria Poddubnaya. \n"
    "Business Intelligence; Professor Carlos Pérez. \n"
    "25th of November 2026. \n"
)

if mode == "internal":
    st.sidebar.markdown("---")
    jump = st.sidebar.radio("Jump to Act", CHAPTERS, index=st.session_state.act_idx)
    st.session_state.act_idx = CHAPTERS.index(jump)

st.progress((st.session_state.act_idx + 1) / len(CHAPTERS))
st.caption(f"Chapter {st.session_state.act_idx + 1} of {len(CHAPTERS)}")

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
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown(f"**Where we stand:** {prev_summary}")
    with c2:
        st.info(f"**Next question →** {next_prompt}")


# ==============================================================================
# ACT 1 — THE CLINICAL STAKES (C1 EDA)
# ==============================================================================
if st.session_state.act_idx == 0:
    if mode == "audience":
        st.caption("ACT 1 OF 5 · WHY THIS PREDICTION MATTERS")
        st.title("Nearly Half of Older Women With Hip Fractures Stay Over Two Weeks — Locking Up Critical Orthopedic Beds")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Why Predicting Prolonged Stays Matters:</strong> Across 2019–2024 hospital discharges shown below,
            hip fracture is concentrated overwhelmingly in women aged 75+. Today, discharge teams often discover a
            complex stay only after two weeks have already passed. <strong>Identifying high-risk patients right after
            initial clinical workup (Days 1–2) unlocks nearly a two-week head start</strong> to coordinate home
            hospitalization, family support, and rehabilitation—freeing acute surgical beds for incoming emergencies.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("ACT 1 OF 5 · C1 COHORT EDA & COMPETING-RISK CENSORING")
        st.title("84% of Closed Hip Fractures Occur at Age 75+, While Rising Mortality Masks Prolonged-Stay Risk (42.4% >15d)")
        st.markdown(
            """
            <div class="story-hook">
            <strong>The Bed-Management Dilemma:</strong> Across 154,431 female public-hospital discharges (2019–2024),
            the 4,361 hip-fracture episodes (S72) plotted below concentrate heavily in women aged 75+ and carry a
            direct operational lever: <em>if we identify post-intake who will stay beyond 15 days, UGCC teams can
            activate home-hospitalization and rehab pathways in the first 24–48 hours instead of Day 14.</em>
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
        ax.set_title("84% of Hip Fractures Concentrate in Women 75+ (3,676 of 4,361)", fontsize=11.0, fontweight="bold", color=INK, pad=12)
        ax.set_ylabel("Hip-fracture discharges (2019–2024)", fontsize=9.5, color=SLATE)
        ax.set_ylim(0, 2950)
        st.pyplot(fig)

    with col2:
        fig, (ax_top, ax_bot) = plt.subplots(
            2, 1, sharex=True, figsize=(6.2, 4.5), gridspec_kw={"hspace": 0.28}
        )

        # Top panel: Median LOS (days)
        ax_top.bar(age_groups, median_los, color=SLATE_LIGHT, edgecolor=SLATE, width=0.52)
        for i, v in enumerate(median_los):
            ax_top.text(i, v + 0.8, f"{v:.1f}d", ha="center", fontsize=8.5, fontweight="bold", color=INK)
        ax_top.set_ylabel("Median LOS (days)", fontsize=9, color=SLATE)
        ax_top.set_ylim(0, 31)
        ax_top.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
        ax_top.set_axisbelow(True)
        ax_top.set_title(
            "Shorter Stays in the Oldest Patients Mask Rising Mortality",
            fontsize=11.2, fontweight="bold", color=INK, pad=10,
        )

        # Bottom panel: In-hospital mortality (%)
        ax_bot.plot(age_groups, mortality, color=OCHRE, marker="o", linewidth=2.4)
        ax_bot.fill_between(age_groups, mortality, color=OCHRE_LIGHT, alpha=0.55)
        for i, v in enumerate(mortality):
            ax_bot.text(i, v + 0.75, f"{v:.1f}%", ha="center", fontsize=8.5, fontweight="bold", color=OCHRE)
        ax_bot.set_ylabel("Mortality (%)", fontsize=9, color=OCHRE)
        ax_bot.set_ylim(0, 13.8)
        ax_bot.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
        ax_bot.set_axisbelow(True)
        ax_bot.tick_params(axis="x", labelsize=9.5)

        st.pyplot(fig)

    if mode == "audience":
        st.markdown(
            f"""
            <div class="takeaway-box">
            <p style="color: {INK}; margin: 0;"><strong>Why this matters to hospital teams:</strong> As shown above,
            <strong>3,676 of 4,361 admissions (84%)</strong> are women aged 75+, and across all episodes
            <strong>42.4% (nearly 1,850 patients) stayed longer than 15 days</strong>. In the oldest brackets,
            median stays appear shorter (14.0d and 13.0d) only because in-hospital mortality rises to 7.0%–10.4%
            alongside transfers to home-hospitalization programs. Spotting long-stay cases right after initial
            clinical workup allows nurses and social workers to organize post-acute care immediately.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        chapter_footer(
            "84% of hip fractures occur in women 75+, and 42.4% of all stays exceed 15 days, creating major acute-bed pressure.",
            "How effectively can a post-intake screening tool catch these prolonged stays early? (Act 2)",
        )
    else:
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
            "Can a binary triage screen flag those prolonged stays early before surgical bottlenecks build up? (Act 2)",
        )


# ==============================================================================
# ACT 2 — THE PIVOT & TRIAGE TRADE-OFF (C2 EVALUATION)
# ==============================================================================
elif st.session_state.act_idx == 1:
    tn, fp, fn, tp = 387, 863, 84, 583
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    total_flags = tp + fp
    flag_rate = total_flags / (tn + fp + fn + tp)

    if mode == "audience":
        st.caption("ACT 2 OF 5 · THE VALUE OF PATIENT-ONLY SCREENING")
        st.title("Flagging High-Risk Stays Using Only Ana's Own Information Catches 87% of Prolonged Cases")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Focusing on What Bed Managers Actually Need:</strong> Care teams don't need an exact discharge
            date — they need an early warning once a patient is admitted and evaluated for a stay likely to exceed
            <strong>two weeks</strong>. Using only Ana's own clinical information — no hospital shortcuts — a
            patient-only screen catches <strong>87.4% (nearly 9 in 10)</strong> of these prolonged cases.
            </div>
            """,
            unsafe_allow_html=True,
        )

        k1, k2, k3 = st.columns(3)
        k1.metric("Prolonged Stays Caught", f"{recall*100:.1f}%", "583 of 667 long-stay patients identified")
        k2.metric("Planning Head Start", "~13–14 Days", "Triggered after initial workup instead of week 2")
        k3.metric("Missed Long Stays", f"{(1-recall)*100:.1f}%", "84 of 667 cases went unflagged")

        st.markdown("### The Trade-Off: Casting a Wide Net to Protect Bed Flow")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">Why High Sensitivity Matters</h4>
                <p style="font-size:1.1rem; color:{SLATE}; margin-bottom:0;">
                An unplanned 25-day stay blocks an acute bed. Catching <strong>583 of 667 prolonged stays
                (87.4%)</strong> using only Ana's own information lets liaison nurses start home-care planning
                immediately.
                </p>
                </div>
                """, unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">What the Extra Flags Mean</h4>
                <p style="font-size:1.1rem; color:{SLATE}; margin-bottom:0;">
                To catch nearly 9 in 10 long stays, the screen flags <strong>{flag_rate*100:.1f}% of admissions
                (about 3 in 4)</strong>, and <strong>{precision*100:.1f}% of flagged patients (2 in 5)</strong>
                actually stay over 15 days. An early check-in is cheap; missing a real bed block is not.
                </p>
                </div>
                """, unsafe_allow_html=True,
            )

        chapter_footer(
            "A patient-only screen (no hospital information used) catches 87.4% of prolonged stays (583 of 667).",
            "Is this signal actually coming from the patient, or was it secretly about the hospital? (Act 3)",
        )

    else:
        st.caption("ACT 2 OF 5 · C2 PROBLEM REFRAMING, RE-EVALUATED WITHOUT GEOGRAPHY")
        st.title("Binary Classification at τ = 0.40 Achieves 87.4% Recall, AUC 0.672 — Using Only Patient-Level Features")
        st.markdown(
            """
            <div class="story-hook">
            <strong>How the problem was reframed:</strong> A continuous LOS regression tree (MAE 11.27 days) lost to
            a trivial median guess (MAE 8.93 days), so we pivoted to binary triage. Per instructor guidance, all
            geographic/institutional features were removed before re-fitting and re-evaluating this classifier.
            </div>
            """,
            unsafe_allow_html=True,
        )

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
            ax.set_xlim(-0.5, 1.5); ax.set_ylim(1.5, -0.5)
            ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
            ax.set_xticklabels(["Predicted <=15d\n(No Flag)", "Predicted >15d\n(Flagged)"], fontsize=9.5, fontweight="bold", color=INK)
            ax.set_yticklabels([f"Actual <=15d\n(n={tn+fp:,})", f"Actual >15d\n(n={fn+tp:,})"], fontsize=9.5, fontweight="bold", color=INK)
            for i in range(2):
                for j in range(2):
                    rect = patches.Rectangle((j-0.48, i-0.48), 0.96, 0.96, facecolor=cell_colors[i][j],
                                              edgecolor=OCHRE if j == 1 else MIST, linewidth=2.0 if (i==1 and j==1) else 1.0)
                    ax.add_patch(rect)
                    row_pct = cm[i][j] / sum(cm[i]) * 100
                    ax.text(j, i-0.12, f"{cm[i][j]:,}", ha="center", va="center", fontsize=16, fontweight="bold", color=cell_text_colors[i][j])
                    ax.text(j, i+0.09, f"({row_pct:.1f}% of row)", ha="center", va="center", fontsize=9, color=cell_text_colors[i][j])
                    ax.text(j, i+0.29, roles[i][j], ha="center", va="center", fontsize=8, style="italic", color=cell_text_colors[i][j])
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.tick_params(length=0)
            ax.set_title("Test Set Confusion Matrix, No Geography (2023–2024, n=1,917 · τ=0.40)", fontsize=10.3, fontweight="bold", color=INK, pad=12)
            st.pyplot(fig)

        with col_right:
            st.subheader("Patient-Only Triage Trade-Off")
            m1, m2 = st.columns(2)
            m1.metric("Prolonged Stays Caught", f"{recall*100:.1f}%", "583 of 667 cases")
            m2.metric("Flagged Precision", f"{precision*100:.1f}%", f"{total_flags:,} total flags")
            st.metric("Test ROC-AUC", "0.672", "Nearly identical to original with-geography model (0.669)")
            st.markdown(
                f"""
                - Majority-class baseline: **65.2% accuracy** (`1,250/1,917`), **0% recall** — catches zero prolonged stays.
                - Threshold **0.40** (F1-maximized on 2022 validation) catches **87.4%** of prolonged stays (`583/667`), missing **12.6%** (`84/667`).
                - Removing geography *reduced* false alarms to **69.0%** of normal stays (`863/1,250`, vs. `909` originally) at a small recall cost (`87.4%` vs. `89.1%`).
                """
            )

        chapter_footer(
            "Rebuilt without any geographic feature, the classifier performs almost identically to the original (AUC 0.672 vs. 0.669).",
            "If performance barely changed, was geography ever really the main driver? (Act 3)",
        )


# ==============================================================================
# ACT 3 — PATIENT PERSONA (AUDIENCE) VS. FEATURE AUDIT (INTERNAL)
# ==============================================================================
elif st.session_state.act_idx == 2:
    if mode == "audience":
        st.caption("ACT 3 OF 5 · MEET ANA: CORRECTING OUR FIRST AUDIT")
        st.title("Our First Check Said Ana's Score Was Mostly About Her Hospital — A Closer Look Said Otherwise")
        st.markdown(
            f"""
            <div class="persona-card">
            <h3 style="color:{INK}; margin-top:0;">Patient Profile: Ana, 82 Years Old</h3>
            <p style="font-size:1.2rem; color:{INK}; margin-bottom:0;">
            Ana is admitted with a closed femoral neck fracture. Our first check of the screening tool
            suggested it was mostly reading <em>which hospital</em> she walked into, not anything about
            Ana herself — a worrying sign. So we looked closer.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="takeaway-box">
            <p style="color: {INK}; margin: 0;">
            <strong>What we found on closer inspection:</strong> Our first geography-removal test was itself
            incomplete — it dropped true hospital identity but still carried a hospital-derived flag, and
            hadn't yet added a genuine clinical detail (Ana's fracture subtype). Once corrected, the
            patient-only screen performs almost identically to the original (test AUC 0.672 vs. 0.669,
            Act 2). The real finding: Ana's score was never mostly about her hospital — our test was
            briefly wrong, not her risk score.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">1 · Number of Comorbidities</h4>
                <p style="font-size:1.05rem; color:{SLATE}; margin-bottom:0;">
                Ana's chronic conditions (median 9–10 in this cohort), documented after her initial evaluation.
                </p>
                </div>
                """, unsafe_allow_html=True,
            )
        with f2:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">2 · Patient Age (82)</h4>
                <p style="font-size:1.05rem; color:{SLATE}; margin-bottom:0;">
                Women 75+ make up 84% of hip-fracture admissions in this cohort.
                </p>
                </div>
                """, unsafe_allow_html=True,
            )
        with f3:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">3 · Fracture Type & Pathway</h4>
                <p style="font-size:1.05rem; color:{SLATE}; margin-bottom:0;">
                Emergency vs. scheduled admission, and femoral neck vs. pertrochanteric fracture.
                </p>
                </div>
                """, unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="takeaway-box">
            <p style="color: {INK}; margin: 0;"><strong>What we tested next:</strong> Using only these three
            patient-level factors — nothing about hospital or location — the yes/no screen holds up well (Act 2).
            Next, we tested whether those same factors can predict Ana's <em>exact</em> number of days in hospital.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        chapter_footer(
            "Our first audit looked alarming, but a corrected rebuild shows Ana's patient-only score holds up (AUC 0.672, nearly matching the original).",
            "The screen works for a yes/no flag — but can it predict Ana's exact number of days? That's a harder test. (Act 4)",
        )

    else:
        st.caption("ACT 3 OF 5 · W3 ATTRIBUTION AUDIT & GEOGRAPHIC ABLATION")
        st.title("Our First Ablation Suggested Near-Random Performance Without Geography (0.535) — A Corrected Rebuild Recovers It (0.672)")
        st.markdown(
            """
            <div class="story-hook">
            <strong>The Audit, Corrected:</strong> Our first geography-removal test seemed to show the classifier
            had almost no signal once hospital identity was dropped. That test, however, still retained a
            hospital-derived same-commune flag and lacked fracture-subtype coding. Rebuilt with a stricter,
            correctly-specified patient-only feature set (Act 2), test AUC recovers to 0.672 — nearly matching
            the original with-geography model (0.669).
            </div>
            """,
            unsafe_allow_html=True,
        )

        model_view = st.radio(
            "Inspect the original (with-geography) classifier's drivers via:",
            ["direction", "importance"],
            format_func=lambda x: {
                "direction": "Which direction each factor pushed risk (Logistic Regression)",
                "importance": "Which factors the computer leaned on most (CatBoost)",
            }[x],
            horizontal=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(6.4, 5.0))
            if model_view == "direction":
                labels = [
                    "Primary Diagnosis (ICD_SUBTYPE_TE)",
                    "Same Commune [Geo] (MISMA_COMUNA)",
                    "Patient Commune [Geo] (COMUNA_REGISTRADA_TE)",
                    "Admission: Scheduled (INGRESO_PROGRAMADA)",
                    "Admission: Emergency (INGRESO_URGENCIA)",
                    "Patient Age (EDAD)",
                    "Hospital Commune [Geo] (COMUNA_ESTAB_TE)",
                ]
                vals = [0.001, -0.012, -0.018, -0.047, 0.047, -0.202, 0.655]
                is_geo = [False, True, True, False, False, False, True]
                colors = [OCHRE if g else SLATE_SOFT for g in is_geo]

                bars = ax.barh(labels, vals, color=colors, height=0.58)
                ax.axvline(0, color=INK, linewidth=1.0)
                for idx_b, bar in enumerate(bars):
                    w = bar.get_width()
                    off = 0.018 if w >= 0 else -0.018
                    ha = "left" if w >= 0 else "right"
                    ax.text(w + off, bar.get_y() + bar.get_height() / 2, f"{w:+.3f}",
                            va="center", ha=ha, fontsize=9, fontweight="bold",
                            color=OCHRE if is_geo[idx_b] else INK)
                ax.set_xlim(-0.34, 0.80)
                ax.set_xlabel(
                    "Logistic Regression coefficient — original with-geography model (Train 2019–2021)",
                    fontsize=8.3, color=SLATE,
                )
                ax.set_title("Hospital Commune Has the Largest Coefficient (+0.655)", fontsize=10.8, fontweight="bold", color=INK, pad=12)
            else:
                labels = [
                    "Primary Diagnosis (ICD_SUBTYPE)",
                    "Admission Type (INGRESO_* grouped)",
                    "Same Commune [Geo] (MISMA_COMUNA)",
                    "Patient Commune [Geo] (COMUNA_REGISTRADA)",
                    "Patient Age (EDAD)",
                    "Hospital Commune [Geo] (COMUNA_ESTAB)",
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
                ax.set_xlabel(
                    "CatBoost split importance — original with-geography classifier (Train 2019–2021)",
                    fontsize=8.3, color=SLATE,
                )
                ax.set_title("High-Cardinality Communes Dominate Tree Splits", fontsize=11, fontweight="bold", color=INK, pad=12)

            ax.grid(axis="x", linestyle=":", color=MIST, linewidth=0.7)
            ax.set_axisbelow(True)
            st.pyplot(fig)
            st.caption("Burnt Ochre [Geo] = Geographic / institutional proxy features | Clinical Slate = Patient & admission features.")

        with col2:
            fig, ax = plt.subplots(figsize=(6.4, 4.7))
            family_tag = "LR" if model_view == "direction" else "CatBoost"
            models = [
                f"Full {family_tag} Model\n(With Geography)\n[Val 2022]",
                f"First-Pass {family_tag}\n(Incomplete Ablation)\n[Val 2022]",
                "Rebuilt Patient-Only\n(Corrected CatBoost)\n[Val / Test]",
            ]
            full_val = 0.675 if model_view == "direction" else 0.661
            first_pass_val = 0.525 if model_view == "direction" else 0.535
            rebuilt_val = 0.650
            rebuilt_test = 0.672

            aucs = [full_val, first_pass_val, rebuilt_val]
            bar_colors = [SLATE_SOFT, SLATE_LIGHT, OCHRE]
            edge_colors = [SLATE_SOFT, SLATE, OCHRE]

            bars = ax.bar(models, aucs, color=bar_colors, edgecolor=edge_colors, width=0.45)
            ax.axhline(0.500, color=INK, linestyle="--", linewidth=1.1)
            ax.text(1.0, 0.512, "Random Chance Baseline (0.500)", ha="center", fontsize=8.3, fontweight="bold", color=INK)

            # Label first two bars (2022 validation)
            for idx_b in [0, 1]:
                h = bars[idx_b].get_height()
                ax.text(
                    bars[idx_b].get_x() + bars[idx_b].get_width() / 2,
                    h + 0.015,
                    f"{h:.3f}\n(Val)",
                    ha="center",
                    fontsize=9.5,
                    fontweight="bold",
                    color=INK,
                )

            # Label third bar with both Validation (0.650) and Test (0.672)
            h_reb = bars[2].get_height()
            ax.text(
                bars[2].get_x() + bars[2].get_width() / 2,
                h_reb + 0.015,
                f"Test: {rebuilt_test:.3f}\n(Val: {rebuilt_val:.3f})",
                ha="center",
                fontsize=9.8,
                fontweight="bold",
                color=OCHRE,
            )

            ax.set_ylim(0, 0.78)
            ax.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
            ax.set_axisbelow(True)
            ax.set_ylabel("ROC-AUC (2022 Val / 2023–24 Test)", fontsize=9.2, color=SLATE)
            ax.set_title(
                "Corrected Rebuild Recovers Patient-Only Discrimination (Test AUC 0.672)",
                fontsize=10.3,
                fontweight="bold",
                color=INK,
                pad=12,
            )
            st.pyplot(fig)
            st.caption(
                f"Comparing the original 2022 {family_tag} validation ablation ({full_val:.3f} → {first_pass_val:.3f}) "
                f"against the properly specified patient-only CatBoost rebuild (0.650 validation, 0.672 test — matching "
                "the original 0.669 test AUC)."
            )

        chapter_footer(
            "The original ablation's near-random result was an artifact of an incomplete feature set, not evidence of pure geographic dependence — the corrected patient-only classifier performs comparably to the original.",
            "Classification recovers well patient-only — does regression (exact LOS) fare the same? (Act 4)",
        )


# ==============================================================================
# ACT 4 — THE PATIENT-ONLY TEST (GEOGRAPHY REMOVED, PER INSTRUCTOR GUIDANCE)
# ==============================================================================
elif st.session_state.act_idx == 3:
    if mode == "audience":
        st.caption("ACT 4 OF 5 · THE HONEST TEST")
        st.title("With No Hospital Shortcuts Allowed, Nothing We Tried Beat a Simple Guess")
        st.markdown(
            """
            <div class="story-hook">
            <strong>A Different, Harder Question:</strong> Act 2's screen answers a yes/no question (will this stay
            exceed 15 days) and works well patient-only. Here we ask something harder: can we predict Ana's
            <em>exact</em> number of days? Using only her own information — age, admission type, fracture type,
            even her chronic conditions — no version of this harder task beat simply assuming a typical stay
            (<strong>8.93 days</strong> average error vs. <strong>9.21d</strong> and <strong>9.81d</strong> below).
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("ACT 4 OF 5 · C3 PATIENT-ONLY REGRESSION, GEOGRAPHY REMOVED")
        st.title("Without Geography, Baseline (8.93d) Beats Both Admission-Only (9.21d) and +Comorbidity (9.81d) Models on Test")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Testing the Patient-Only Hypothesis:</strong> Per instructor guidance, geography was removed
            entirely from the regression task. Two patient-only models were fit — admission fields alone, and
            admission fields plus post-admission comorbidity/severity — and compared against a median-LOS baseline
            using the same train/validation/test split as before.
            </div>
            """,
            unsafe_allow_html=True,
        )

    mae_df = pd.DataFrame({
        "Model": ["Baseline\n(median guess)", "Admission-Only\n(no geography)", "+ Comorbidities\n(no geography)"],
        "Validation MAE (2022)": [11.75, 11.82, 11.55],
        "Test MAE (2023–2024)": [8.93, 9.21, 9.81],
    })

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    x = np.arange(3)
    w = 0.35
    bars_val = ax.bar(x - w/2, mae_df["Validation MAE (2022)"], width=w, color=SLATE_LIGHT, edgecolor=SLATE, label="Validation (2022)")
    bars_test = ax.bar(x + w/2, mae_df["Test MAE (2023–2024)"], width=w, color=SLATE_SOFT, label="Test (2023–2024)")
    for bars in (bars_val, bars_test):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.18, f"{h:.2f}d", ha="center", fontsize=9, fontweight="bold", color=INK)

    # Mark which bars failed to beat the baseline — annotation, not misleading color
    for i in [1, 2]:
        h = mae_df["Test MAE (2023–2024)"].iloc[i]
        ax.text(x[i] + w/2, h + 0.85, "✗ worse than\nbaseline", ha="center", fontsize=8, color=OCHRE, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(mae_df["Model"], fontsize=9.3, color=INK)
    ax.set_ylabel(
        "How far off the prediction was, in days" if mode == "audience" else "Mean Absolute Error (days)",
        fontsize=9.5, color=SLATE,
    )
    ax.set_ylim(0, 14.5)
    ax.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.set_title(
        "No Patient-Only Model Beat the Simple Baseline (8.93d on 2023–2024 Test)" if mode == "audience"
        else "Geography Removed: Baseline Wins on Test for Both Candidate Models",
        fontsize=11, fontweight="bold", color=INK, pad=12,
    )
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    st.pyplot(fig)

    if mode == "internal":
        st.warning(
            "**Why this matters:** The +comorbidity model scored best on validation (`11.55d`) — the same pattern "
            "seen in the earlier, geography-included version — then degraded furthest on test (`9.81d`), the worst "
            "result on the chart. This is consistent with the comorbidity-coding drift diagnosed earlier (median "
            "Charlson `1.0 → 2.0` between periods) and confirms this is not a one-off artifact of including "
            "geography: a model fit once on 2019–2021 data does not reliably generalize when it leans on fields "
            "whose distribution shifts over time."
        )
    else:
        st.warning(
            "**Why this matters:** Giving the model Ana's chronic-condition history looked best during development "
            "(`11.55` days off vs. `11.75` for a simple guess) — then turned out to be the *least* accurate on "
            "more recent patients (`9.81` days off vs. `8.93` for a simple guess). A model that looks better in "
            "development isn't always better in practice."
        )

    chapter_footer(
        "With geography removed, no patient-only model beats a simple median guess on real test data (8.93d) — the comorbidity model generalizes worst of all (9.81d).",
        "Given this, what should UGCC directors actually do? (Act 5)",
    )


# ==============================================================================
# ACT 5 — SPLIT RECOMMENDATION: PILOT THE SCREEN, WITHHOLD THE LOS PREDICTOR
# ==============================================================================
else:
    if mode == "audience":
        st.caption("ACT 5 OF 5 · WHAT THIS MEANS FOR UGCC")
        st.title("Pilot the Early-Warning Screen — It Works on Patient Information Alone")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Executive Recommendation:</strong> Using only Ana's own information — no hospital shortcuts —
            we built a screen that still catches <strong>87.4%</strong> of prolonged stays (Act 2). This is ready
            for a careful pilot. Separately, we also tried to predict Ana's <em>exact</em> number of days in
            hospital, and that attempt did not work — no version beat a simple guess (Act 4). We recommend piloting
            the early-warning screen while continuing to withhold the exact-day predictor until it improves.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("ACT 5 OF 5 · SPLIT CONCLUSION: CLASSIFICATION READY, REGRESSION NOT")
        st.title("Patient-Only Classification Recovers Original Performance (AUC 0.672); Patient-Only Regression Does Not Beat Baseline")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Conclusion:</strong> Per instructor guidance, geography was removed from both the
            classification and regression routes. The two routes produced genuinely different answers: the
            binary >15-day classifier, rebuilt patient-only with corrected feature specification, nearly matches
            its original with-geography performance (0.672 vs. 0.669 test AUC). The continuous length-of-stay
            regressor does not — every patient-only variant underperformed a simple median baseline on test.
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 1 · Ready to Pilot" if mode == "audience" else "#### 1 · Classification: Ready to Pilot")
        st.markdown(
            """
            - **Early-warning screen (>15 days):** catches **87.4%** of prolonged stays (`583/667`) using only
              patient-level information — age, admission type, fracture subtype, comorbidity burden.
            - **No hospital shortcuts:** performance barely changed once geography was correctly removed
              (test AUC 0.672 vs. 0.669 originally), confirming this result reflects the patient, not the hospital.
            """
        )

    with c2:
        st.markdown("#### 2 · Not Ready — Withhold" if mode == "audience" else "#### 2 · Regression: Withhold for Now")
        st.markdown(
            """
            - **Exact length-of-stay prediction:** no patient-only model beat a simple median guess on test data
              (baseline 8.93d vs. 9.21d admission-only, 9.81d with comorbidities).
            - **Comorbidity version was least reliable:** it looked best in development (`11.55d`) and performed
              worst once checked against real, more recent patients (`9.81d`) — a caution against trusting
              validation results alone.
            """
        )

    with c3:
        st.markdown("#### 3 · Concrete Next Steps")
        st.markdown(
            """
            1. **Pilot the classification screen** in high-volume orthopedic services, with the usual safeguards —
               screening trigger only, never used to ration or delay care.
            2. **Do not deploy the exact-day predictor** until it beats baseline on held-out data; revisit once
               richer confirmed-admission-time clinical fields are available.
            3. **Recalibrate the screen periodically** given the same comorbidity-coding drift that affected the
               regression route (median Charlson 1.0→2.0 between periods) likely also affects the classifier
               over time, even though it currently tolerates it well.
            """
        )

    if mode == "internal":
        with st.expander("Technical audit notes (methodology, not shown to external audience)"):
            st.markdown(
                """
                - Geography (`COMUNA_ESTAB_TE`, `COMUNA_REGISTRADA_TE`, `MISMA_COMUNA`) removed from all models,
                  classification and regression, per instructor guidance.
                - Classification, no geography: validation AUC 0.650, test AUC 0.672, threshold 0.40
                  (F1-maximized on validation only; test touched once). Confusion matrix: tn=387, fp=863, fn=84, tp=583.
                - An earlier, incompletely-specified ablation (validation AUC 0.535) retained a derived
                  same-commune flag and lacked fracture-subtype coding — superseded by the result above, not
                  contradicted by it; the original test was measuring a different, less complete feature set.
                - Regression, no geography: validation MAE 11.82 (admission-only) / 11.55 (+comorbidity); test MAE
                  9.21 / 9.81, both worse than the 8.93d baseline. The comorbidity model shows the largest
                  validation-to-test gap of any model tested in this project.
                - **Open item unchanged from W2/C2:** whether `IR_29301_SEVERIDAD`/`INDICE_CHARLSON` are available
                  at admission or only finalized at discharge remains unconfirmed.
                """
            )

    st.markdown("---")
    st.caption(
        "**Process & AI Usage Disclosure:** Built from verified C1, C2, C3, and W3 notebook outputs by Group 02 "
        "(Lukas Garrido & Maria Poddubnaya). Per instructor guidance, geography was removed from all models in "
        "this revision. An earlier narrative draft incorrectly recommended piloting a model that underperformed "
        "its own baseline on test data; this was identified and corrected before submission. Generative AI "
        "(Claude) assisted with restructuring the narrative to match the corrected, verified results."
    )