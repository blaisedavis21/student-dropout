import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RetainAI — Student Success Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom styling ─────────────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Instrument+Serif:ital@0;1&display=swap');

    .stApp {
        background: linear-gradient(165deg, #0f172a 0%, #1e293b 42%, #0f172a 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1222 0%, #151d33 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }
    [data-testid="stSidebar"] .stMarkdown { color: #cbd5e1; }
    [data-testid="stHeader"] { background: transparent; }

    .hero-wrap {
        background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 55%, #db2777 100%);
        border-radius: 20px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 24px 48px rgba(29, 78, 216, 0.35);
        border: 1px solid rgba(255,255,255,0.15);
    }
    .hero-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 2.6rem;
        font-weight: 400;
        color: #fff;
        margin: 0 0 0.5rem 0;
        line-height: 1.15;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.05rem;
        color: rgba(255,255,255,0.92);
        margin: 0;
        max-width: 640px;
        line-height: 1.55;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(8px);
        color: #fff;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.25);
    }

    .section-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }
    .section-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #94a3b8;
        margin: 0 0 0.25rem 0;
    }
    .section-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 0 0 0.75rem 0;
    }

    .result-hero {
        border-radius: 20px;
        padding: 2rem 2.25rem;
        margin: 1.25rem 0 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.12);
        text-align: center;
    }
    .result-hero.low {
        background: linear-gradient(135deg, rgba(16,185,129,0.25) 0%, rgba(5,150,105,0.15) 100%);
        box-shadow: 0 16px 40px rgba(16, 185, 129, 0.2);
    }
    .result-hero.medium {
        background: linear-gradient(135deg, rgba(245,158,11,0.28) 0%, rgba(217,119,6,0.15) 100%);
        box-shadow: 0 16px 40px rgba(245, 158, 11, 0.2);
    }
    .result-hero.high {
        background: linear-gradient(135deg, rgba(239,68,68,0.3) 0%, rgba(185,28,28,0.18) 100%);
        box-shadow: 0 16px 40px rgba(239, 68, 68, 0.25);
    }
    .risk-pct {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 4rem;
        font-weight: 400;
        color: #fff;
        line-height: 1;
        margin: 0;
    }
    .risk-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.85);
        margin: 0.5rem 0 0 0;
    }
    .risk-msg {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.05rem;
        color: rgba(255,255,255,0.9);
        margin: 1rem auto 0;
        max-width: 520px;
        line-height: 1.5;
    }

    .stat-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        text-align: center;
        height: 100%;
    }
    .stat-val {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
    }
    .stat-lbl {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
        margin: 0.35rem 0 0 0;
    }

    .intervention-card {
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.65rem;
        border-left: 4px solid;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        line-height: 1.5;
        color: #e2e8f0;
    }
    .intervention-card.financial { background: rgba(239,68,68,0.12); border-color: #ef4444; }
    .intervention-card.academic { background: rgba(59,130,246,0.12); border-color: #3b82f6; }
    .intervention-card.declining { background: rgba(168,85,247,0.12); border-color: #a855f7; }
    .intervention-card.scholarship { background: rgba(34,197,94,0.1); border-color: #22c55e; }
    .intervention-card.accommodation { background: rgba(14,165,233,0.12); border-color: #0ea5e9; }
    .intervention-card.mature { background: rgba(251,191,36,0.1); border-color: #fbbf24; }
    .intervention-card.wellbeing { background: rgba(244,63,94,0.15); border-color: #f43f5e; }
    .intervention-card.low { background: rgba(16,185,129,0.1); border-color: #10b981; }
    .intervention-card.default { background: rgba(148,163,184,0.1); border-color: #64748b; }
    .int-tag {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.9;
        display: block;
        margin-bottom: 0.35rem;
    }

    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        padding: 1.5rem 1.75rem 0.5rem;
    }
    .stFormSubmitButton button {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: white !important;
        font-weight: 700 !important;
        font-family: 'DM Sans', sans-serif !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stFormSubmitButton button:hover {
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45) !important;
        transform: translateY(-1px);
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        border: 1px solid rgba(148,163,184,0.1);
    }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    [data-testid="stMetricValue"] { color: #f1f5f9 !important; }

    .disclaimer {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.5;
        padding: 1rem 1.25rem;
        background: rgba(0,0,0,0.2);
        border-radius: 10px;
        border: 1px solid rgba(148,163,184,0.08);
    }

    h1, h2, h3, label, p, span, .stMarkdown { font-family: 'DM Sans', sans-serif; }
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
    except FileNotFoundError:
        return None, None, None, None

model, scaler, le, feature_cols = load_artifacts()

# ── Intervention rules ─────────────────────────────────────────────────────────
def get_interventions(inputs, dropout_pct):
    recs = []
    s1_enrolled = inputs.get("Curricular units 1st sem (enrolled)", 1)
    s1_approved = inputs.get("Curricular units 1st sem (approved)", 0)
    s1_grade    = inputs.get("Curricular units 1st sem (grade)", 0)
    s1_rate = s1_approved / max(s1_enrolled, 1)

    s2_enrolled = inputs.get("Curricular units 2nd sem (enrolled)", 1)
    s2_approved = inputs.get("Curricular units 2nd sem (approved)", 0)
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
        f'<div class="intervention-card {css}">'
        f'<span class="int-tag">{tag.strip()}</span>{body.strip()}'
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
    total_enrolled = s1e + s2e
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
    st.markdown("### 🎯 Why this matters")
    st.markdown(
        "Every student who drops out represents lost potential — and preventable cost "
        "for the institution. **RetainAI** turns academic data into **actionable insight** "
        "in seconds, so advisors intervene *before* it's too late."
    )
    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown("1. Enter student profile & grades  \n2. XGBoost model scores dropout risk  \n3. Get tiered risk + tailored interventions")
    st.markdown("---")
    st.markdown("**Group F · Makerere University**  \nMachine Learning Project")
    if model is not None:
        st.success("✓ Model loaded & ready")
    st.markdown("---")
    st.caption("Powered by 46 engineered features · UCI-trained XGBoost")

# ── Hero ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">Group F · Student Success Intelligence</div>
    <h1 class="hero-title">Spot at-risk students before they leave.</h1>
    <p class="hero-sub">
        Data-driven dropout screening for academic advisors. Enter a student profile,
        get an instant risk score, and receive evidence-based intervention recommendations
        — so you can act with confidence, not guesswork.
    </p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("Model files not found. Please ensure best_model.pkl, scaler.pkl, label_encoder.pkl, and feature_columns.pkl are in the same folder as this app.")
    st.stop()

# ── Input form ─────────────────────────────────────────────────────────────────
col_form, col_info = st.columns([2, 1])

with col_info:
    st.markdown("""
    <div class="section-card">
        <p class="section-label">Advisor tip</p>
        <p class="section-title">Better inputs → sharper predictions</p>
        <p style="color:#94a3b8; font-size:0.9rem; line-height:1.55; margin:0;">
            Semester grades and financial status are the strongest signals in our model.
            Update figures after each exam period for the most reliable risk score.
        </p>
    </div>
    <div class="section-card">
        <p class="section-label">Risk tiers</p>
        <p style="color:#10b981; font-size:0.85rem; margin:0.25rem 0;"><strong>Low</strong> — under 30%</p>
        <p style="color:#f59e0b; font-size:0.85rem; margin:0.25rem 0;"><strong>Medium</strong> — 30–59%</p>
        <p style="color:#ef4444; font-size:0.85rem; margin:0.25rem 0;"><strong>High</strong> — 60%+</p>
    </div>
    """, unsafe_allow_html=True)

with col_form:
    with st.form("student_form"):
        st.markdown('<p class="section-label">Step 1</p><p class="section-title">Student background</p>', unsafe_allow_html=True)
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

        st.markdown('<p class="section-label">Step 2</p><p class="section-title">1st semester performance</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            s1_enrolled = st.number_input("Units Enrolled (Sem 1)", 0, 30, 6)
        with c2:
            s1_approved = st.number_input("Units Approved (Sem 1)", 0, 30, 5)
        with c3:
            s1_grade    = st.number_input("Average Grade (Sem 1)", 0.0, 20.0, 12.0)
        s1_evals = st.number_input("Evaluations Attended (Sem 1)", 0, 40, 6)

        st.markdown('<p class="section-label">Step 3</p><p class="section-title">2nd semester performance</p>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            s2_enrolled = st.number_input("Units Enrolled (Sem 2)", 0, 30, 6)
        with c5:
            s2_approved = st.number_input("Units Approved (Sem 2)", 0, 30, 4)
        with c6:
            s2_grade    = st.number_input("Average Grade (Sem 2)", 0.0, 20.0, 11.0)
        s2_evals = st.number_input("Evaluations Attended (Sem 2)", 0, 40, 6)

        submitted = st.form_submit_button("🔍 Analyze Dropout Risk", use_container_width=True)

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
        proba = model.predict_proba(X_scaled)[0]
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
    st.markdown('<p class="section-label">Results</p><p class="section-title">Student risk assessment</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-hero {tier_icon}">
        <p class="risk-pct">{dropout_pct:.1f}%</p>
        <p class="risk-label">{label} · Dropout probability</p>
        <p class="risk-msg">{risk_message(tier, pred_class, dropout_pct)}</p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-box"><p class="stat-val">{pred_class}</p><p class="stat-lbl">Predicted outcome</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="stat-box"><p class="stat-val">{label}</p><p class="stat-lbl">Risk tier</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="stat-box"><p class="stat-val">{raw["Overall Approval Rate"]*100:.0f}%</p><p class="stat-lbl">Pass rate</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="stat-box"><p class="stat-val">{raw["Average Grade Both Sems"]:.1f}</p><p class="stat-lbl">Avg grade</p></div>', unsafe_allow_html=True)

    st.progress(float(min(dropout_pct / 100, 1.0)))
    st.caption("Dropout probability scale — higher bar means greater urgency for intervention.")

    st.markdown('<p class="section-label">Action plan</p><p class="section-title">Recommended interventions for academic advisor</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#94a3b8; font-size:0.9rem; margin-bottom:1rem;">'
        'Prioritized by severity. Address <strong style="color:#ef4444;">Financial</strong> and '
        '<strong style="color:#f43f5e;">Wellbeing</strong> flags first.</p>',
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
    st.info("👆 Fill in the student profile above and click **Analyze Dropout Risk** to generate a personalized assessment.")
