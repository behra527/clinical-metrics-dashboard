from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

PATIENTS_FILE = DATA_DIR / "patients.csv"
VITALS_FILE = DATA_DIR / "vitals.csv"


PATIENT_REQUIRED_COLUMNS = {
    "patient_id",
    "age",
    "gender",
    "readmission_risk_score",
}

VITAL_REQUIRED_COLUMNS = {
    "patient_id",
    "visit_number",
    "visit_date",
    "systolic_bp",
    "diastolic_bp",
    "glucose",
}


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def _validate_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    dataset_name: str,
) -> None:
    """Validate that a dataset contains all required columns."""

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{sorted(missing_columns)}"
        )


def _validate_patient_relationship(
    patients: pd.DataFrame,
    vitals: pd.DataFrame,
) -> None:
    """Validate the relationship between patients and vital records."""

    patient_ids = set(patients["patient_id"])
    vital_patient_ids = set(vitals["patient_id"])

    unknown_patient_ids = vital_patient_ids - patient_ids

    if unknown_patient_ids:
        raise ValueError(
            "Vitals contain patient IDs that do not exist "
            f"in the patient dataset: {sorted(unknown_patient_ids)}"
        )


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

@st.cache_data
def load_patient_data() -> pd.DataFrame:
    """
    Load and validate patient-level clinical data.
    """

    if not PATIENTS_FILE.exists():
        raise FileNotFoundError(
            f"Patient dataset not found: {PATIENTS_FILE}"
        )

    patients = pd.read_csv(PATIENTS_FILE)

    _validate_columns(
        patients,
        PATIENT_REQUIRED_COLUMNS,
        "patients.csv",
    )

    if patients["patient_id"].duplicated().any():
        raise ValueError(
            "patients.csv contains duplicate patient IDs."
        )

    return patients


@st.cache_data
def load_vital_data() -> pd.DataFrame:
    """
    Load and validate longitudinal vital-sign data.
    """

    if not VITALS_FILE.exists():
        raise FileNotFoundError(
            f"Vitals dataset not found: {VITALS_FILE}"
        )

    vitals = pd.read_csv(VITALS_FILE)

    _validate_columns(
        vitals,
        VITAL_REQUIRED_COLUMNS,
        "vitals.csv",
    )

    vitals["visit_date"] = pd.to_datetime(
        vitals["visit_date"],
        errors="coerce",
    )

    if vitals["visit_date"].isna().any():
        raise ValueError(
            "vitals.csv contains invalid visit dates."
        )

    if vitals["patient_id"].isna().any():
        raise ValueError(
            "vitals.csv contains missing patient IDs."
        )

    patients = load_patient_data()

    _validate_patient_relationship(
        patients,
        vitals,
    )

    return vitals


# ---------------------------------------------------------------------
# Combined data access
# ---------------------------------------------------------------------

def load_clinical_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load both patient and vital datasets.
    """

    patients = load_patient_data()
    vitals = load_vital_data()

    return patients, vitals