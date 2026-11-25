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

