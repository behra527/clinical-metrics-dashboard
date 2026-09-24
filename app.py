import pandas as pd
import streamlit as st

from src.charts import create_vital_trend_chart
from src.data_loader import load_clinical_data
from src.metrics import (
    calculate_patient_metrics,
    get_patient_summary,
    get_patient_vitals,
)

# Page configuration
st.set_page_config(
    page_title="Clinical Metrics Dashboard",
    page_icon="🩺",
    layout="wide",
)

# ------------------------------------------------------------------------------
# Pro Medical SaaS UI Theme (Obsidian & Slate Navy Palette)
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Dark Obsidian Canvas Background */
    html, body, [class*="st-"], .stApp {
        background-color: #0B0F17 !important;
        color: #E2E8F0 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Headings Styling */
    h1 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
        font-size: 2.1rem !important;
    }
    
    h2, h3 {
        color: #38BDF8 !important; /* Medical Cyan Accent */
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-bottom: 1px solid #1F2937;
        padding-bottom: 6px;
        margin-top: 1.8rem !important;
        margin-bottom: 1rem !important;
    }

    /* Professional Elevated Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease-in-out;
        margin-bottom: 12px;
    }

    .metric-card:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(56, 189, 248, 0.15);
    }

    .metric-label {
        color: #9CA3AF;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    /* Clinical Risk Badges */
    .badge-low {
        color: #4ADE80 !important; /* Soft Emerald Green */
    }
    .badge-medium {
        color: #FBBF24 !important; /* Amber Yellow */
    }
    .badge-high {
        color: #F87171 !important; /* Coral Red */
    }

    /* Widget Labels */
    label[data-testid="stWidgetLabel"] {
        color: #9CA3AF !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* Dropdown Overrides */
    div[data-baseweb="select"] {
        background-color: #111827 !important;
        border-radius: 8px !important;
        border: 1px solid #1F2937 !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: #38BDF8 !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        background-color: transparent !important;
    }

    /* Dataframe Table Container */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1F2937 !important;
        border-radius: 10px !important;
        background-color: #111827 !important;
        padding: 4px;
    }

    /* Subtitle Caption */
    .stCaption {
        color: #64748B !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def custom_metric(label: str, value: str, badge_class: str = ""):
    """Clean custom HTML card widget without nested Streamlit metric boxes."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {badge_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Load clinical data safely
try:
    patients, vitals = load_clinical_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Unable to load clinical data: {exc}")
    st.stop()

# Basic empty-data validation
if patients.empty:
    st.error("Patient dataset is empty.")
    st.stop()

if vitals.empty:
    st.error("Vitals dataset is empty.")
    st.stop()

# Dashboard title
st.title("Clinical Metrics Dashboard")

st.caption(
    "Synthetic clinical data for dashboard demonstration. "
    "This application is not a clinical decision-support system."
)

# Dashboard overview
st.subheader("Dashboard Overview")

overview_columns = st.columns(4)

with overview_columns[0]:
    custom_metric("Total Patients", str(len(patients)))

with overview_columns[1]:
    custom_metric("Total Visits", str(len(vitals)))

with overview_columns[2]:
    custom_metric("Average Age", f"{patients['age'].mean():.1f} years")

with overview_columns[3]:
    custom_metric("Average Risk", f"{patients['readmission_risk_score'].mean() * 100:.1f}%")

# Patient selection
st.subheader("Patient Selection")

patient_options = patients["patient_id"].tolist()

patient_labels = {
    row["patient_id"]: (
        f"{row['patient_id']} — "
        f"{row['gender']} — "
        f"Age {int(row['age'])}"
    )
    for _, row in patients.iterrows()
}

select_col, _ = st.columns([2, 3])

with select_col:
    selected_patient = st.selectbox(
        "Select Patient",
        options=patient_options,
        format_func=lambda patient_id: patient_labels[patient_id],
    )

# Selected patient demographics
selected_patient_data = patients.loc[
    patients["patient_id"] == selected_patient
].iloc[0]

st.subheader("Patient Demographics")

demographic_columns = st.columns(3)

with demographic_columns[0]:
    custom_metric("Patient ID", str(selected_patient))

with demographic_columns[1]:
    custom_metric("Gender", str(selected_patient_data["gender"]))

with demographic_columns[2]:
    custom_metric("Age", f"{int(selected_patient_data['age'])} years")

# Get selected patient data
try:
    patient = get_patient_summary(
        patients,
        selected_patient,
    )

    patient_vitals = get_patient_vitals(
        vitals,
        selected_patient,
    )

    patient_metrics = calculate_patient_metrics(
        patient,
        patient_vitals,
    )

except ValueError as exc:
    st.error(str(exc))
    st.stop()

# Patient metrics
st.subheader("Patient Metrics")

metric_columns = st.columns(4)

bp_val = (
    f"{patient_metrics['latest_systolic_bp']:.1f}/"
    f"{patient_metrics['latest_diastolic_bp']:.1f} mmHg"
)
glucose_val = f"{patient_metrics['latest_glucose']:.1f} mg/dL"
risk_val = f"{patient_metrics['risk_score']:.1f}%"
risk_level = str(patient_metrics["risk_level"])

# Color badge selection based on risk status
risk_class = ""
if "low" in risk_level.lower():
    risk_class = "badge-low"
elif "high" in risk_level.lower():
    risk_class = "badge-high"
else:
    risk_class = "badge-medium"

with metric_columns[0]:
    custom_metric("Blood Pressure", bp_val)

with metric_columns[1]:
    custom_metric("Glucose", glucose_val)

with metric_columns[2]:
    custom_metric("Readmission Risk", risk_val)

with metric_columns[3]:
    custom_metric("Risk Level", risk_level, badge_class=risk_class)

# Vital trend analysis
st.subheader("Vital Trend Analysis")

figure = create_vital_trend_chart(patient_vitals)

# Dynamic dark theme application for Plotly chart
figure.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E2E8F0"),
    xaxis=dict(
        gridcolor="#1F2937",
        showgrid=True,
        zerolinecolor="#1F2937",
    ),
    yaxis=dict(
        gridcolor="#1F2937",
        showgrid=True,
        zerolinecolor="#1F2937",
    ),
    legend=dict(
        font=dict(color="#9CA3AF"),
        bgcolor="rgba(0,0,0,0)",
    ),
)

st.plotly_chart(
    figure,
    use_container_width=True,
)

# Visit history
st.subheader("Visit History")

display_columns = [
    "visit_number",
    "visit_date",
    "systolic_bp",
    "diastolic_bp",
    "glucose",
]

table_df = patient_vitals[display_columns].copy()

if "visit_date" in table_df.columns:
    table_df["visit_date"] = pd.to_datetime(table_df["visit_date"]).dt.strftime("%Y-%m-%d")

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "visit_number": st.column_config.NumberColumn(
            "Visit #",
            format="%d",
            width="small",
        ),
        "visit_date": st.column_config.TextColumn(
            "Visit Date",
            width="medium",
        ),
        "systolic_bp": st.column_config.NumberColumn(
            "Systolic BP (mmHg)",
            format="%.1f",
            width="medium",
        ),
        "diastolic_bp": st.column_config.NumberColumn(
            "Diastolic BP (mmHg)",
            format="%.1f",
            width="medium",
        ),
        "glucose": st.column_config.NumberColumn(
            "Glucose (mg/dL)",
            format="%.1f",
            width="medium",
        ),
    },
)