import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RetainAI — Student Success Dashboard",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom styling ─────────────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

    :root {
        --bg:       #080c10;
        --bg-2:     #0d1117;
        --bg-3:     #111820;
        --border:   rgba(255,255,255,0.07);
        --border-2: rgba(255,255,255,0.12);
        --accent:   #00e5ff;
        --accent-2: #00b8cc;
        --red:      #ff3b3b;
        --amber:    #ffb300;
        --green:    #00e676;
        --text-1:   #f0f4f8;
        --text-2:   #8b98a9;
        --text-3:   #4a5568;
    }

    * { box-sizing: border-box; }

    .stApp {
        background: var(--bg);
        font-family: 'IBM Plex Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: var(--bg-2) !important;
        border-right: 1px solid var(--border-2);
    }
    [data-testid="stSidebar"] > div { padding-top: 2rem; }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span { color: var(--text-2) !important; }
    [data-testid="stHeader"] { background: transparent !important; }

    /* ── HEADER BANNER ─────────────────────────────── */
    .banner {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding: 2.5rem 2.75rem;
        margin-bottom: 2rem;
        background: var(--bg-2);
        border: 1px solid var(--border-2);
        border-left: 3px solid var(--accent);
        position: relative;
        overflow: hidden;
    }
    .banner::before {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 320px; height: 100%;
        background: linear-gradient(135deg, transparent 60%, rgba(0,229,255,0.03) 100%);
        pointer-events: none;
    }
    .banner-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        font-weight: 400;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 0;
    }
    .banner-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--text-1);
        margin: 0;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }
    .banner-sub {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.95rem;
        font-weight: 300;
        color: var(--text-2);
        margin: 0;
        max-width: 580px;
        line-height: 1.6;
    }

    /* ── SECTION HEADINGS ──────────────────────────── */
    .step-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 1.5rem 0 0.2rem 0;
    }
    .step-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-1);
        margin: 0 0 0.9rem 0;
        letter-spacing: -0.01em;
    }

    /* ── FORM CONTAINER ────────────────────────────── */
    div[data-testid="stForm"] {
        background: var(--bg-2) !important;
        border: 1px solid var(--border-2) !important;
        border-radius: 0 !important;
        padding: 1.75rem 2rem 0.75rem !important;
    }

    /* ── INPUTS ────────────────────────────────────── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: var(--bg-3) !important;
        border: 1px solid var(--border-2) !important;
        border-radius: 0 !important;
        color: var(--text-1) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }
    label { color: var(--text-2) !important; font-size: 0.82rem !important; }

    /* ── SUBMIT BUTTON ─────────────────────────────── */
    .stFormSubmitButton button {
        background: var(--accent) !important;
        color: #000 !important;
        font-weight: 700 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0.8rem 2rem !important;
        transition: background 0.15s ease, transform 0.1s ease !important;
    }
    .stFormSubmitButton button:hover {
        background: var(--accent-2) !important;
        transform: translateY(-1px) !important;
    }

    /* ── RESULT HERO ───────────────────────────────── */
    .result-wrap {
        padding: 2.5rem 2.75rem;
        margin: 1.5rem 0;
        border-left: 3px solid;
        background: var(--bg-2);
        position: relative;
    }
    .result-wrap.low  { border-color: var(--green); }
    .result-wrap.medium { border-color: var(--amber); }
    .result-wrap.high { border-color: var(--red); }

    .result-pct {
        font-family: 'Syne', sans-serif;
        font-size: 5rem;
        font-weight: 800;
        line-height: 1;
        margin: 0;
        letter-spacing: -0.04em;
    }
    .result-wrap.low  .result-pct { color: var(--green); }
    .result-wrap.medium .result-pct { color: var(--amber); }
    .result-wrap.high .result-pct { color: var(--red); }

    .result-tier {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--text-2);
        margin: 0.5rem 0 1rem 0;
    }
    .result-msg {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.95rem;
        font-weight: 300;
        color: var(--text-2);
        line-height: 1.6;
        max-width: 560px;
        margin: 0;
    }
    .result-msg strong { color: var(--text-1); font-weight: 600; }

    /* ── STAT BOXES ────────────────────────────────── */
    .stat-row { display: flex; gap: 1px; margin: 1.5rem 0; background: var(--border); }
    .stat-cell {
        flex: 1;
        background: var(--bg-2);
        padding: 1.2rem 1.4rem;
    }
    .stat-val {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-1);
        margin: 0;
        letter-spacing: -0.02em;
    }
    .stat-key {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--text-3);
        margin: 0.4rem 0 0 0;
    }

    /* ── PROGRESS BAR ──────────────────────────────── */
    .stProgress > div > div > div {
        background: var(--accent) !important;
        border-radius: 0 !important;
        height: 3px !important;
    }
    .stProgress > div > div {
        background: var(--border-2) !important;
        border-radius: 0 !important;
        height: 3px !important;
    }

    /* ── INTERVENTION CARDS ────────────────────────── */
    .int-card {
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        padding: 1rem 1.25rem;
        margin-bottom: 2px;
        background: var(--bg-2);
        border-left: 2px solid;
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.88rem;
        line-height: 1.55;
        color: var(--text-2);
    }
    .int-card.financial    { border-color: var(--red); }
    .int-card.academic     { border-color: #448aff; }
    .int-card.declining    { border-color: #d500f9; }
    .int-card.scholarship  { border-color: var(--green); }
    .int-card.accommodation { border-color: #00b0ff; }
    .int-card.mature       { border-color: var(--amber); }
    .int-card.wellbeing    { border-color: #ff4081; }
    .int-card.low          { border-color: var(--green); }
    .int-card.default      { border-color: var(--border-2); }

    .int-tag {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        white-space: nowrap;
        padding-top: 0.15rem;
        min-width: 110px;
    }
    .int-card.financial    .int-tag { color: var(--red); }
    .int-card.academic     .int-tag { color: #448aff; }
    .int-card.declining    .int-tag { color: #d500f9; }
    .int-card.scholarship  .int-tag { color: var(--green); }
    .int-card.accommodation .int-tag { color: #00b0ff; }
    .int-card.mature       .int-tag { color: var(--amber); }
    .int-card.wellbeing    .int-tag { color: #ff4081; }
    .int-card.low          .int-tag { color: var(--green); }
    .int-card.default      .int-tag { color: var(--text-3); }

    /* ── SIDEBAR CARDS ─────────────────────────────── */
    .side-block {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
    }
    .side-block-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 0 0 0.6rem 0;
    }
    .side-block p {
        font-size: 0.85rem !important;
        line-height: 1.55;
    }
    .tier-row {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.35rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
    }
    .tier-dot {
        width: 6px; height: 6px;
        flex-shrink: 0;
    }

    /* ── DISCLAIMER ────────────────────────────────── */
    .disclaimer {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.78rem;
        font-weight: 300;
        color: var(--text-3);
        line-height: 1.6;
        padding: 1rem 1.25rem;
        border: 1px solid var(--border);
        border-left: 2px solid var(--text-3);
        margin-top: 1.5rem;
    }

    /* ── INFO BOX ──────────────────────────────────── */
    .stInfo {
        background: var(--bg-2) !important;
        border: 1px solid var(--border-2) !important;
        border-left: 2px solid var(--accent) !important;
        border-radius: 0 !important;
        color: var(--text-2) !important;
    }
    .stAlert { border-radius: 0 !important; }

    /* ── DIVIDERS ──────────────────────────────────── */
    hr { border-color: var(--border) !important; }

    /* ── METRICS ───────────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--bg-2) !important;
        border-radius: 0 !important;
        border: 1px solid var(--border) !important;
        padding: 0.9rem 1.1rem !important;
    }
    [data-testid="stMetricLabel"] { color: var(--text-3) !important; }
    [data-testid="stMetricValue"] { color: var(--text-1) !important; }

    /* ── ADVISOR INFO PANEL ────────────────────────── */
    .info-panel {
        background: var(--bg-2);
        border: 1px solid var(--border-2);
        border-left: 2px solid var(--accent);
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
    }
    .info-panel-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 0 0 0.35rem 0;
    }
    .info-panel-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-1);
        margin: 0 0 0.6rem 0;
    }
    .info-panel p {
        color: var(--text-2);
        font-size: 0.85rem;
        line-height: 1.55;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

inject_styles()

# ── Load saved model artifacts ─────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    try:
        with open("best_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        with open("label_encoder.pkl", "rb") as f:
            le = pickle.load(f)
        with open("feature_columns.pkl", "rb") as f:
            feature_cols = pickle.load(f)
        return model, scaler, le, feature_cols
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.stop()
        return None, None, None, None
model, scaler, le, feature_cols = load_artifacts()

# ── Intervention rules ─────────────────────────────────────────────────────────
def get_interventions(inputs, dropout_pct):
    recs = []
    s1_enrolled = inputs.get("Curricular units 1st sem (enrolled)", 1)
    s1_approved = inputs.get("Curricular units 1st sem (approved)", 0)
    s1_grade    = inputs.get("Curricular units 1st sem (grade)", 0)
    s1_rate     = s1_approved / max(s1_enrolled, 1)

    s2_grade    = inputs.get("Curricular units 2nd sem (grade)", 0)

    if inputs.get("Debtor", 0) == 1:
        recs.append("FINANCIAL: Student has outstanding debt. Refer to financial aid office immediately.")
    if inputs.get("Tuition fees up to date", 1) == 0:
        recs.append("FINANCIAL: Tuition fees are not up to date. Risk of administrative withdrawal — urgent.")
    if s1_rate < 0.40:
        recs.append(f"ACADEMIC: Only {s1_rate*100:.0f}% of Sem 1 units were passed. Assign a peer tutor and increase contact with lecturer.")
    if s1_grade > 0 and s1_grade < 10:
        recs.append("ACADEMIC: Average Sem 1 grade is below 10. Schedule a study skills workshop and weekly progress check-ins.")
    if s1_grade > 0 and s2_grade > 0 and (s2_grade - s1_grade) < -2:
        recs.append(f"DECLINING PERFORMANCE: Grade dropped by {s2_grade - s1_grade:.1f} from Sem 1 to Sem 2. Investigate for personal difficulties or disengagement.")
    if inputs.get("Scholarship holder", 0) == 0:
        recs.append("SCHOLARSHIP: Student has no scholarship. Check eligibility for merit-based or need-based awards.")
    if inputs.get("Displaced", 0) == 1:
        recs.append("ACCOMMODATION: Student is displaced. Check whether housing difficulties are affecting attendance.")
    if inputs.get("Age at enrollment", 20) > 30:
        recs.append(f"MATURE STUDENT: Enrolled at age {inputs.get('Age at enrollment', 20)}. May have work or family commitments — explore flexible learning options.")
    if dropout_pct >= 60:
        recs.append("WELLBEING: High dropout risk detected. Proactively offer counselling referral — do not wait for the student to self-refer.")
    if not recs:
        recs.append("LOW RISK: No major risk factors detected. Continue standard check-ins.")
    return recs

def intervention_css_class(rec):
    tag = rec.split(":")[0].strip().lower()
    mapping = {
        "financial": "financial",
        "academic": "academic",
        "declining performance": "declining",
        "scholarship": "scholarship",
        "accommodation": "accommodation",
        "mature student": "mature",
        "wellbeing": "wellbeing",
        "low risk": "low",
    }
    return mapping.get(tag, "default")

def render_intervention(rec):
    tag, _, body = rec.partition(":")
    css = intervention_css_class(rec)
    st.markdown(
        f'<div class="int-card {css}">'
        f'<span class="int-tag">{tag.strip()}</span>'
        f'<span>{body.strip()}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def risk_message(tier, pred_class, dropout_pct):
    if tier == "HIGH":
        return (
            f"This student shows a <strong>{dropout_pct:.0f}%</strong> probability of dropping out. "
            "Early, coordinated intervention can still change the outcome — act within this week."
        )
    if tier == "MEDIUM":
        return (
            f"Moderate risk ({dropout_pct:.0f}% dropout probability). "
            f"Likely trajectory: <strong>{pred_class}</strong>. Schedule a structured check-in before the next term."
        )
    return (
        f"Strong retention signals ({dropout_pct:.0f}% dropout risk). "
        f"Predicted outcome: <strong>{pred_class}</strong>. Maintain supportive contact and celebrate progress."
    )

# ── Feature engineering ────────────────────────────────────────────────────────
def engineer_features(inputs):
    s1e = inputs["Curricular units 1st sem (enrolled)"]
    s1a = inputs["Curricular units 1st sem (approved)"]
    s1g = inputs["Curricular units 1st sem (grade)"]
    s2e = inputs["Curricular units 2nd sem (enrolled)"]
    s2a = inputs["Curricular units 2nd sem (approved)"]
    s2g = inputs["Curricular units 2nd sem (grade)"]

    inputs["Total Units Approved"]       = s1a + s2a
    inputs["Total Units Enrolled"]       = s1e + s2e
    inputs["Approval Rate 1st Sem"]      = s1a / max(s1e, 1)
    inputs["Approval Rate 2nd Sem"]      = s2a / max(s2e, 1)
    total_enrolled                        = s1e + s2e
    inputs["Overall Approval Rate"]      = (s1a + s2a) / max(total_enrolled, 1)
    inputs["Average Grade Both Sems"]    = (s1g + s2g) / 2
    inputs["Grade Improvement"]          = s2g - s1g
    inputs["Financial Risk Score"]       = inputs["Debtor"] + (1 - inputs["Tuition fees up to date"])
    s1_evals = inputs.get("Curricular units 1st sem (evaluations)", 0)
    s2_evals = inputs.get("Curricular units 2nd sem (evaluations)", 0)
    inputs["Academic Engagement Score"]  = (s1_evals + s2_evals) / max(total_enrolled, 1)
    inputs["Sem2 vs Sem1 Units Ratio"]   = s2e / max(s1e, 1)
    return inputs

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family: Syne, sans-serif; font-size: 1.1rem; font-weight: 800; color: #f0f4f8; letter-spacing: -0.02em; margin-bottom: 1.5rem;">RetainAI</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="side-block">
        <p class="side-block-title">About</p>
        <p>RetainAI turns academic data into actionable insight in seconds, so advisors can intervene before it is too late.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="side-block">
        <p class="side-block-title">Workflow</p>
        <p>01 — Enter student profile and grades<br>02 — XGBoost model scores dropout risk<br>03 — Receive tiered risk and tailored interventions</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="side-block">
        <p class="side-block-title">Risk Tiers</p>
        <div class="tier-row">
            <div class="tier-dot" style="background:#00e676;"></div>
            <span style="color:#8b98a9;">Low — under 30%</span>
        </div>
        <div class="tier-row">
            <div class="tier-dot" style="background:#ffb300;"></div>
            <span style="color:#8b98a9;">Medium — 30 to 59%</span>
        </div>
        <div class="tier-row">
            <div class="tier-dot" style="background:#ff3b3b;"></div>
            <span style="color:#8b98a9;">High — 60% and above</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="side-block">
        <p class="side-block-title">Project</p>
        <p>Group F · Makerere University<br>Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    if model is not None:
        st.markdown('<p style="font-family: IBM Plex Mono, monospace; font-size: 0.65rem; color: #00e676; letter-spacing: 0.15em; text-transform: uppercase; margin-top: 1rem;">Model loaded</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-family: IBM Plex Mono, monospace; font-size: 0.65rem; color: #ff3b3b; letter-spacing: 0.15em; text-transform: uppercase; margin-top: 1rem;">Model not found</p>', unsafe_allow_html=True)

    st.markdown('<p style="font-family: IBM Plex Mono, monospace; font-size: 0.6rem; color: #4a5568; margin-top: 0.5rem;">46 engineered features · XGBoost</p>', unsafe_allow_html=True)

# ── Banner ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner">
    <p class="banner-eyebrow">Group F · Student Success Intelligence</p>
    <h1 class="banner-title">Spot at-risk students<br>before they leave.</h1>
    <p class="banner-sub">
        Data-driven dropout screening for academic advisors. Enter a student profile,
        get an instant risk score, and receive evidence-based intervention recommendations.
    </p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("Model files not found. Ensure best_model.pkl, scaler.pkl, label_encoder.pkl, and feature_columns.pkl are in the same directory as this app.")
    st.stop()

# ── Input form ─────────────────────────────────────────────────────────────────
col_form, col_info = st.columns([2, 1])

with col_info:
    st.markdown("""
    <div class="info-panel">
        <p class="info-panel-label">Advisor note</p>
        <p class="info-panel-title">Better inputs, sharper predictions</p>
        <p>Semester grades and financial status are the strongest signals. Update after each exam period for the most reliable risk score.</p>
    </div>
    """, unsafe_allow_html=True)

with col_form:
    with st.form("student_form"):
        st.markdown('<p class="step-label">Step 01</p><p class="step-title">Student background</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age          = st.number_input("Age at Enrollment", 17, 70, 20)
            gender       = st.selectbox("Gender", ["Female (0)", "Male (1)"])
            scholarship  = st.selectbox("Scholarship Holder", ["No (0)", "Yes (1)"])
            displaced    = st.selectbox("Displaced Student", ["No (0)", "Yes (1)"])
        with col2:
            debtor       = st.selectbox("Has Outstanding Debt", ["No (0)", "Yes (1)"])
            tuition_paid = st.selectbox("Tuition Fees Up to Date", ["No (0)", "Yes (1)"])
            admission_g  = st.number_input("Admission Grade (0–200)", 0.0, 200.0, 120.0)
            prev_qual_g  = st.number_input("Previous Qualification Grade (0–200)", 0.0, 200.0, 130.0)

        st.markdown('<p class="step-label">Step 02</p><p class="step-title">1st semester performance</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            s1_enrolled = st.number_input("Units Enrolled (Sem 1)", 0, 30, 6)
        with c2:
            s1_approved = st.number_input("Units Approved (Sem 1)", 0, 30, 5)
        with c3:
            s1_grade    = st.number_input("Average Grade (Sem 1)", 0.0, 20.0, 12.0)
        s1_evals = st.number_input("Evaluations Attended (Sem 1)", 0, 40, 6)

        st.markdown('<p class="step-label">Step 03</p><p class="step-title">2nd semester performance</p>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            s2_enrolled = st.number_input("Units Enrolled (Sem 2)", 0, 30, 6)
        with c5:
            s2_approved = st.number_input("Units Approved (Sem 2)", 0, 30, 4)
        with c6:
            s2_grade    = st.number_input("Average Grade (Sem 2)", 0.0, 20.0, 11.0)
        s2_evals = st.number_input("Evaluations Attended (Sem 2)", 0, 40, 6)

        submitted = st.form_submit_button("Analyze Dropout Risk", use_container_width=True)

# ── Prediction ─────────────────────────────────────────────────────────────────
if submitted:
    def option_value(label):
        return 1 if "(1)" in label else 0

    raw = {
        "Age at enrollment": age,
        "Gender": option_value(gender),
        "Scholarship holder": option_value(scholarship),
        "Displaced": option_value(displaced),
        "Debtor": option_value(debtor),
        "Tuition fees up to date": option_value(tuition_paid),
        "Admission grade": admission_g,
        "Previous qualification (grade)": prev_qual_g,
        "Curricular units 1st sem (enrolled)": s1_enrolled,
        "Curricular units 1st sem (approved)": s1_approved,
        "Curricular units 1st sem (grade)": s1_grade,
        "Curricular units 1st sem (evaluations)": s1_evals,
        "Curricular units 2nd sem (enrolled)": s2_enrolled,
        "Curricular units 2nd sem (approved)": s2_approved,
        "Curricular units 2nd sem (grade)": s2_grade,
        "Curricular units 2nd sem (evaluations)": s2_evals,
        "Marital status": 1,
        "Application mode": 1,
        "Application order": 1,
        "Course": 1,
        "Daytime/evening attendance": 1,
        "Previous qualification": 1,
        "Nacionality": 1,
        "Mother's qualification": 1,
        "Father's qualification": 1,
        "Mother's occupation": 1,
        "Father's occupation": 1,
        "Educational special needs": 0,
        "International": 0,
        "Curricular units 1st sem (credited)": 0,
        "Curricular units 1st sem (without evaluations)": 0,
        "Curricular units 2nd sem (credited)": 0,
        "Curricular units 2nd sem (without evaluations)": 0,
        "Unemployment rate": 10.8,
        "Inflation rate": 1.4,
        "GDP": 1.74,
    }

    raw = engineer_features(raw)
    row = {col: raw.get(col, 0) for col in feature_cols}
    X = pd.DataFrame([row])
    X_scaled = scaler.transform(X)

    dropout_idx = list(le.classes_).index("Dropout")
    if hasattr(model, "predict_proba"):
        proba       = model.predict_proba(X_scaled)[0]
        dropout_pct = float(proba[dropout_idx] * 100)
        pred_class  = le.classes_[np.argmax(proba)]
    else:
        pred_class  = le.classes_[model.predict(X_scaled)[0]]
        dropout_pct = 100.0 if pred_class == "Dropout" else 10.0

    if dropout_pct >= 60:
        tier, label, tier_icon = "HIGH", "High Risk", "high"
    elif dropout_pct >= 30:
        tier, label, tier_icon = "MEDIUM", "Medium Risk", "medium"
    else:
        tier, label, tier_icon = "LOW", "Low Risk", "low"

    st.markdown("---")
    st.markdown('<p class="step-label">Results</p><p class="step-title">Student risk assessment</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-wrap {tier_icon}">
        <p class="result-pct">{dropout_pct:.1f}%</p>
        <p class="result-tier">Dropout probability &nbsp;·&nbsp; {label}</p>
        <p class="result-msg">{risk_message(tier, pred_class, dropout_pct)}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-cell">
            <p class="stat-val">{pred_class}</p>
            <p class="stat-key">Predicted outcome</p>
        </div>
        <div class="stat-cell">
            <p class="stat-val">{label}</p>
            <p class="stat-key">Risk tier</p>
        </div>
        <div class="stat-cell">
            <p class="stat-val">{raw["Overall Approval Rate"]*100:.0f}%</p>
            <p class="stat-key">Pass rate</p>
        </div>
        <div class="stat-cell">
            <p class="stat-val">{raw["Average Grade Both Sems"]:.1f}</p>
            <p class="stat-key">Avg grade</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(float(min(dropout_pct / 100, 1.0)))
    st.caption("Dropout probability scale — higher bar means greater urgency.")

    st.markdown('<p class="step-label" style="margin-top:1.5rem;">Action plan</p><p class="step-title">Recommended interventions</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#4a5568; font-size:0.82rem; font-family: IBM Plex Mono, monospace; '
        'letter-spacing: 0.05em; margin-bottom: 0.75rem;">'
        'Prioritized by severity. Address FINANCIAL and WELLBEING flags first.</p>',
        unsafe_allow_html=True,
    )

    recs = get_interventions(raw, dropout_pct)
    for rec in recs:
        render_intervention(rec)

    st.markdown("""
    <div class="disclaimer">
        <strong>Responsible use:</strong> This is a screening tool, not a final decision.
        Predictions should be reviewed by a qualified academic advisor. The model was trained on
        Portuguese polytechnic data and may not fully reflect local patterns at Makerere.
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("---")
    st.info("Fill in the student profile above and click Analyze Dropout Risk to generate a personalized assessment.")