"""
GROUP_02 — Hip fracture among adult women (C3 storytelling dashboard)
Streamlit app built from saved C1-C2-W3 results only — no raw data file is
loaded or required. Every number below traces to a specific saved output.

Run with: python -m streamlit run dashboard_4.py
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
        "Act 2 · The Value of Post-Intake Screening",
        "Act 3 · Meet Ana: What Shapes Recovery Time",
        "Act 4 · Keeping Predictions Accurate Over Time",
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
    "All metrics trace directly to verified C1/C2/W3 outputs."
    "Team members: Lukas Garrido, Maria Poddubnaya"
    "Business Intelligence; Professor Carlos Pérez"
    "25th of November 2026"
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
            <strong>Why Predicting Prolonged Stays Matters:</strong> Hip fracture is the #1 reason women aged 75+ are
            admitted to public hospitals. Today, discharge teams often discover a complex stay only after two weeks
            have already passed. <strong>Identifying high-risk patients right after initial clinical workup (Days 1–2)
            unlocks nearly a two-week head start</strong> to coordinate home hospitalization, family support, and
            rehabilitation—freeing acute surgical beds for incoming emergencies.
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
            hip fracture (S72) stands out as the leading diagnosis among women aged 75+ and carries a direct
            operational lever: <em>if we identify post-intake who will stay beyond 15 days, UGCC teams can activate
            home-hospitalization and rehab pathways in the first 24–48 hours instead of Day 14.</em>
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
            <p style="color: {INK}; margin: 0;"><strong>Why this matters to hospital teams:</strong> Across 4,361 hip-fracture
            admissions, <strong>42.4% (nearly 1,850 patients) stayed longer than 15 days</strong>. In the oldest
            brackets (75+), patients face both high mortality (up to 10.4%) and growing transfers to home-hospitalization
            programs. Spotting those long-stay cases right after initial clinical workup allows nurses and social
            workers to organize post-acute care immediately instead of reacting to bed gridlock two weeks later.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        chapter_footer(
            "42.4% of older women admitted with hip fractures stay over 15 days, creating major acute-bed pressure.",
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
    tn, fp, fn, tp = 341, 909, 73, 594
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    total_flags = tp + fp

    if mode == "audience":
        st.caption("ACT 2 OF 5 · THE VALUE OF POST-INTAKE SCREENING")
        st.title("Flagging High-Risk Stays (>15 Days) After Initial Workup Catches 9 Out of 10 Prolonged Cases")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Focusing on What Bed Managers Actually Need:</strong> Care teams do not need to guess an exact
            discharge date—they need an early warning once a patient is admitted and evaluated for stays likely to
            exceed <strong>two weeks</strong>. Flagging high-risk patients after initial clinical assessment gives
            discharge planners nearly a two-week window to arrange home care and rehabilitation before bottlenecks form.
            </div>
            """,
            unsafe_allow_html=True,
        )

        k1, k2, k3 = st.columns(3)
        k1.metric("Prolonged Stays Caught Early", "89.1% (9 in 10)", "594 of 667 long-stay patients identified")
        k2.metric("Planning Head Start", "~13–14 Days", "Triggered after initial workup instead of week 2")
        k3.metric("Missed Long Stays", "Only 10.9%", "73 of 667 cases went unflagged")

        st.markdown("### The Operational Trade-Off: Casting a Wide Net to Protect Bed Flow")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">Why High Sensitivity Matters</h4>
                <p style="font-size:1.1rem; color:{SLATE}; margin-bottom:0;">
                An unplanned 25-day stay blocks an acute orthopedic bed and delays surgeries for incoming trauma
                patients. Catching <strong>594 of 667 prolonged stays</strong> right after initial evaluation lets
                liaison nurses start home-care paperwork immediately.
                </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                f"""
                <div class="factor-card">
                <h4 style="color:{INK}; margin-top:0;">What the Extra Flags Mean in Practice</h4>
                <p style="font-size:1.1rem; color:{SLATE}; margin-bottom:0;">
                To catch 9 out of 10 long stays, the screen flags roughly <strong>4 in 5 admissions</strong>
                (about 2 in 5 flagged patients end up staying >15 days). Because an early discharge check-in is
                non-invasive, reviewing extra patients is far less costly than missing a prolonged bed block.
                </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        chapter_footer(
            "Post-intake triage catches 89.1% of >15-day stays, giving care teams a two-week head start on discharge logistics.",
            "What patient health factors recorded after admission drive this prolonged-stay risk? Meet Ana. (Act 3)",
        )

    else:
        st.caption("ACT 2 OF 5 · C2 PROBLEM REFRAMING & THRESHOLD CALIBRATION")
        st.title("Continuous LOS Regression Lost to Median Baseline (11.27d vs. 8.93d) — Binary Classification at τ = 0.38 Achieves 89.1% Recall")
        st.markdown(
            """
            <div class="story-hook">
            <strong>How the problem was reframed:</strong> Our first instinct in C2 was to predict exact length of stay
            in days. A Regression Tree (MAE 11.27 days) lost to a trivial guess of
            "everyone stays 15 days" (baseline MAE 8.93 days). Exact stay length is too noisy — so we
            pivoted to binary triage: <strong>will this stay exceed 15 days?</strong>
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
            st.metric("Test ROC-AUC (ranking power)", "0.669", "Validation: 0.661 (CatBoost) / 0.675 (LR)")

            st.markdown(
                """
                **Why we chose high recall over raw accuracy:**
                - A naive baseline that *never flags anyone* scores **65% accuracy** — and misses **100%** of prolonged stays.
                - Tuning the probability threshold to **0.38** on the 2022 validation set catches **89.1%** of prolonged stays (`594 / 667`), leaving only **73** unflagged long stays.
                - **Operational cost:** Bed managers must review **909 false alarms** (`72.7%` of normal stays). In hospital operations, an unnecessary early discharge check-in is cheap; an unplanned 25-day bed block is expensive.
                """
            )

        chapter_footer(
            "Reframing to binary triage catches 89.1% of prolonged stays at threshold 0.38, trading precision (39.5%) for sensitivity.",
            "What drives risk when comparing hospital location vs. post-admission patient comorbidities? (Act 3)",
        )


# ==============================================================================
# ACT 3 — PATIENT PERSONA (AUDIENCE) VS. FEATURE AUDIT (INTERNAL)
# ==============================================================================
elif st.session_state.act_idx == 2:
    if mode == "audience":
        st.caption("ACT 3 OF 5 · MEET ANA: SEPARATING THE PATIENT FROM THE HOSPITAL")
        st.title("Ana Is an 82-Year-Old Woman With a Hip Fracture — But Her Risk Score Was Mostly About Her Hospital, Not Her")

        st.markdown(
            f"""
            <div class="persona-card">
            <h3 style="color:{INK}; margin-top:0;">Patient Profile: Ana, 82 Years Old</h3>
            <p style="font-size:1.2rem; color:{INK}; margin-bottom:0;">
            Ana is admitted with a <strong>closed femoral neck fracture (S72.00)</strong>. When we checked what our
            tool was actually using to judge her risk, we found an uncomfortable answer: <strong>most of its signal
            came from which hospital she walked into, not from anything about Ana herself.</strong> That's a
            different question than the one we set out to answer — so we rebuilt the model using only
            Ana's own information, with no hospital or location shortcuts.
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
            patient-level factors — nothing about hospital or location — can we predict Ana's stay length at all?
            That's the honest test in Act 4.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        chapter_footer(
            "Ana's risk score was mostly measuring her hospital, not her — so we removed geography entirely and started over.",
            "Does a patient-only model, with no hospital shortcuts, actually predict length of stay? (Act 4)",
        )

    else:
        st.caption("ACT 3 OF 5 · W3 ATTRIBUTION AUDIT & GEOGRAPHIC ABLATION")
        st.title("Hospital Commune Dominates Both Log-Odds (+0.655) and Split Importance (44.0); Removing Geography Collapses AUC to Near-Random (0.535 / 0.525)")
        st.markdown(
            """
            <div class="story-hook">
            <strong>The Honest Audit:</strong> Inspecting the classification model's weights and running an ablation
            test removing geography revealed the model was primarily learning hospital and regional identity, not
            individual patient biology. Per instructor guidance, geography is now omitted entirely from every model
            in this project going forward — the question shifts from "how long will this patient stay" to
            "does the patient's own clinical picture, independent of institution, predict stay length."
            </div>
            """,
            unsafe_allow_html=True,
        )

        model_view = st.radio(
            "Inspect the original (with-geography) classifier's drivers via:",
            ["direction", "importance"],
            format_func=lambda x: {
                "direction": "Which direction each factor pushed risk",
                "importance": "Which factors the computer leaned on most",
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
            models = ["Full Model\n(With Geography)", "No-Geography Model\n(Clinical & Admin Only)"]
            aucs = [0.675, 0.525] if model_view == "direction" else [0.661, 0.535]
            auc_drop = aucs[0] - aucs[1]
            drop_pct = auc_drop / (aucs[0] - 0.5) * 100

            bars = ax.bar(models, aucs, color=[SLATE_SOFT, SLATE_SOFT], width=0.40)
            ax.axhline(0.500, color=INK, linestyle="--", linewidth=1.1)
            ax.text(0.50, 0.512, "Random Chance Baseline (0.500)", ha="center", fontsize=8.5, fontweight="bold", color=INK)
            for idx_b, bar in enumerate(bars):
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.015, f"{h:.3f}",
                        ha="center", fontsize=11.5, fontweight="bold", color=INK)
            ax.annotate(
                f"Both models shown for reference —\nneither is used going forward",
                xy=(0.5, 0.74), ha="center", fontsize=8.5, style="italic", color=SLATE,
            )
            ax.set_ylim(0, 0.78)
            ax.grid(axis="y", linestyle=":", color=MIST, linewidth=0.7)
            ax.set_axisbelow(True)
            ax.set_ylabel("Validation ROC-AUC (2022, n = 914)", fontsize=9.5, color=SLATE)
            ax.set_title(f"Without Geography, AUC Drops {drop_pct:.0f}% Toward Random", fontsize=11, fontweight="bold", color=INK, pad=12)
            st.pyplot(fig)
            st.caption(
                "This result is why geography is excluded from every model from this point forward — "
                "not because the signal was wrong, but because it answered a different question than intended."
            )

        chapter_footer(
            "The original classifier's signal was almost entirely geographic. Per instructor guidance, geography is removed from all models going forward.",
            "With geography fully removed, does a patient-only model predict length of stay at all? (Act 4)",
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
            <strong>What we found:</strong> Using only Ana's own information — age, admission type, fracture type,
            and even her chronic conditions — no model we built predicted her length of stay better than simply
            assuming a typical stay. The version using her chronic conditions looked most promising while we were
            still developing it, then performed worst of all once tested on real, more recent patients.
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
    baseline_test = mae_df["Test MAE (2023–2024)"].iloc[0]
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
        "No Patient-Only Model Beat the Simple Baseline" if mode == "audience"
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
            "**Why this matters:** Giving the model Ana's chronic-condition history looked like the best approach "
            "while we were still building it — then turned out to be the *least* accurate once we checked it "
            "against real, more recent patients. This is an important caution: a model that looks better in "
            "development isn't always better in practice."
        )

    chapter_footer(
        "With geography removed, no patient-only model beats a simple median guess on real test data — the comorbidity model generalizes worst of all.",
        "Given this, what should UGCC directors actually do? (Act 5)",
    )


# ==============================================================================
# ACT 5 — HONEST RECOMMENDATION: REDIRECT, DON'T DEPLOY
# ==============================================================================
else:
    if mode == "audience":
        st.caption("ACT 5 OF 5 · WHAT THIS MEANS FOR UGCC")
        st.title("We Don't Yet Have a Patient-Level Tool That Works — But We Found a Different, Real Question Worth Investigating")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Honest Recommendation:</strong> Using only information about the patient, we could not build a
            tool that reliably predicts length of stay better than a simple guess. What we <em>did</em> find is
            that stay length varies a great deal by hospital — which raises a legitimate, separate question worth
            investigating directly: are some hospitals' treatment processes producing longer stays than others,
            independent of who their patients are?
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("ACT 5 OF 5 · HONEST CONCLUSION & REDIRECTED NEXT STEP")
        st.title("Patient-Only Models Do Not Currently Outperform the Baseline — The Real Signal Is Institutional, Not Individual")
        st.markdown(
            """
            <div class="story-hook">
            <strong>Conclusion:</strong> Per instructor guidance, geography was removed from every model to isolate
            patient-level signal. None of the resulting models beat a median-LOS baseline on test data. The
            project's one consistent, well-replicated finding is that most of the originally observed predictive
            power came from hospital/commune identity — a genuine, instructor-prompted redirection of the question
            from "can we predict this patient's stay" to "why does stay length vary so much by institution."
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 1 · What We Can Say With Confidence")
        st.markdown(
            """
            - Patient-level clinical fields currently available at or after admission (age, admission type, fracture
              subtype, comorbidity burden) do not predict length of stay better than a simple baseline.
            - Length of stay varies substantially by hospital — this is a real, repeatedly confirmed pattern,
              not a modeling artifact.
            """
        )
    with c2:
        st.markdown("#### 2 · What We Recommend Against")
        st.markdown(
            """
            - Do not deploy a patient-level length-of-stay prediction tool on the current data — none tested
              outperforms simply assuming a typical stay.
            - Do not interpret the earlier "hospital commune" signal as a patient risk score — it reflects
              institutional variation, not individual biology.
            """
        )
    with c3:
        st.markdown("#### 3 · What We Recommend Instead")
        st.markdown(
            """
            1. **Investigate institutional variation directly:** treat "why do some hospitals have longer stays"
               as its own question — a treatment-quality and capacity audit, not a patient-prediction problem.
            2. **Collect richer patient-level data:** pre-operative ASA status, time-to-surgery, and confirmed
               admission-time severity scores could change this conclusion — none were available here.
            3. **Revisit prediction only once institutional variation is understood or controlled for.**
            """
        )

    if mode == "internal":
        with st.expander("Technical audit notes (methodology, not shown to external audience)"):
            st.markdown(
                """
                - Geography (`COMUNA_ESTAB_TE`, `COMUNA_REGISTRADA_TE`, `MISMA_COMUNA`) was removed from all
                  features per instructor guidance, for both the classification route (Act 2/3) and the
                  regression route (Act 4), since its presence answered an institutional question rather than
                  a patient-level one.
                - Classification AUC without geography: CatBoost 0.535, Logistic Regression 0.525 — both near
                  random chance (0.500).
                - Regression MAE without geography (test): baseline 8.93d, admission-only 9.21d, +comorbidity
                  9.81d — baseline wins; the comorbidity model again shows the largest validation-to-test gap.
                - **Open scope question:** the original Act 2 classification tool (89.1% recall, AUC 0.669) was
                  also built with geography. If "omit geography entirely" applies project-wide, that result and
                  its pilot recommendation should be revisited using the same no-geography framing shown here.
                """
            )

    st.markdown("---")
    st.caption(
        "**Process & AI Usage Disclosure:** Built from verified C1, C2, C3, and W3 notebook outputs by Group 02 "
        "(Lukas Garrido & Maria Poddubnaya). Per instructor guidance, geography was removed from all models in "
        "this revision; prior versions using geography are documented separately. Generative AI (Claude) assisted "
        "with restructuring the narrative to match the corrected, verified results."
    )