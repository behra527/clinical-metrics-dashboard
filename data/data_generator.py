from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

RANDOM_SEED = 42
N_PATIENTS = 50
VISITS_PER_PATIENT = 6

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------
# Patient-level data
# ---------------------------------------------------------------------

def generate_patient_data(
    n_patients: int = N_PATIENTS,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Generate one demographic and risk record per patient.
    """

    rng = np.random.default_rng(random_seed)

    patient_ids = [
        f"P{index:04d}"
        for index in range(1, n_patients + 1)
    ]

    ages = rng.integers(
        low=25,
        high=81,
        size=n_patients,
    )

    genders = rng.choice(
        ["Male", "Female"],
        size=n_patients,
    )

    risk_scores = np.round(
        rng.uniform(0.08, 0.92, size=n_patients),
        3,
    )

    return pd.DataFrame(
        {
            "patient_id": patient_ids,
            "age": ages,
            "gender": genders,
            "readmission_risk_score": risk_scores,
        }
    )


# ---------------------------------------------------------------------
# Visit-level vital data
# ---------------------------------------------------------------------

def generate_vital_data(
    patients: pd.DataFrame,
    visits_per_patient: int = VISITS_PER_PATIENT,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Generate longitudinal vital-sign observations
    for every patient.
    """

    rng = np.random.default_rng(random_seed)

    records = []

    for _, patient in patients.iterrows():

        patient_id = patient["patient_id"]
        age = patient["age"]

        # Patient-specific baseline values.
        systolic_baseline = (
            108
            + (age * 0.25)
            + rng.normal(0, 5)
        )

        diastolic_baseline = (
            68
            + (age * 0.12)
            + rng.normal(0, 3)
        )

        glucose_baseline = (
            85
            + (age * 0.35)
            + rng.normal(0, 8)
        )

        visit_dates = pd.date_range(
            end="2026-09-20",
            periods=visits_per_patient,
            freq="30D",
        )

        for visit_number, visit_date in enumerate(
            visit_dates,
            start=1,
        ):

            # Small longitudinal variation.
            trend = visit_number * rng.normal(0.5, 1.2)

            systolic_bp = np.clip(
                systolic_baseline
                + trend
                + rng.normal(0, 5),
                90,
                190,
            )

            diastolic_bp = np.clip(
                diastolic_baseline
                + rng.normal(0, 4),
                55,
                120,
            )

            glucose = np.clip(
                glucose_baseline
                + rng.normal(0, 10),
                60,
                220,
            )

            records.append(
                {
                    "patient_id": patient_id,
                    "visit_number": visit_number,
                    "visit_date": visit_date,
                    "systolic_bp": round(systolic_bp, 1),
                    "diastolic_bp": round(diastolic_bp, 1),
                    "glucose": round(glucose, 1),
                }
            )

    return pd.DataFrame(records)


# ---------------------------------------------------------------------
# Persist datasets
# ---------------------------------------------------------------------

def main() -> None:
    """
    Generate and save the synthetic clinical datasets.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    patients = generate_patient_data()

    vitals = generate_vital_data(
        patients=patients,
    )

    patients.to_csv(
        DATA_DIR / "patients.csv",
        index=False,
    )

    vitals.to_csv(
        DATA_DIR / "vitals.csv",
        index=False,
    )

    print(f"Patients generated: {len(patients)}")
    print(f"Vital records generated: {len(vitals)}")
    print(f"Data directory: {DATA_DIR}")


if __name__ == "__main__":
    main()