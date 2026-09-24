import pandas as pd


def get_patient_summary(
    patients: pd.DataFrame,
    patient_id: str,
) -> pd.Series:
    patient = patients.loc[
        patients["patient_id"] == patient_id
    ]

    if patient.empty:
        raise ValueError(
            f"Patient '{patient_id}' was not found."
        )

    return patient.iloc[0]


def get_patient_vitals(
    vitals: pd.DataFrame,
    patient_id: str,
) -> pd.DataFrame:
    patient_vitals = vitals.loc[
        vitals["patient_id"] == patient_id
    ].copy()

    if patient_vitals.empty:
        raise ValueError(
            f"No vital records found for patient '{patient_id}'."
        )

    return (
        patient_vitals
        .sort_values("visit_date")
        .reset_index(drop=True)
    )


def format_risk_score(
    risk_score: float,
) -> float:
    return round(risk_score * 100, 1)


def classify_risk_level(
    risk_score: float,
) -> str:
    if risk_score < 0.30:
        return "Low"
    elif risk_score < 0.70:
        return "Moderate"
    return "High"


def calculate_patient_metrics(
    patient: pd.Series,
    patient_vitals: pd.DataFrame,
) -> dict[str, float | int | str]:
    latest_visit = patient_vitals.iloc[-1]

    raw_risk_score = float(
        patient["readmission_risk_score"]
    )

    return {
        "age": int(patient["age"]),
        "risk_score": format_risk_score(
            raw_risk_score
        ),
        "risk_level": classify_risk_level(
            raw_risk_score
        ),
        "latest_systolic_bp": float(
            latest_visit["systolic_bp"]
        ),
        "latest_diastolic_bp": float(
            latest_visit["diastolic_bp"]
        ),
        "latest_glucose": float(
            latest_visit["glucose"]
        ),
        "total_visits": len(patient_vitals),
    }