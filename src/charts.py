import pandas as pd
import plotly.graph_objects as go


def create_vital_trend_chart(
    patient_vitals: pd.DataFrame,
) -> go.Figure:
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=patient_vitals["visit_date"],
            y=patient_vitals["systolic_bp"],
            mode="lines+markers",
            name="Systolic BP",
            hovertemplate=(
                "Date: %{x|%Y-%m-%d}"
                "<br>Systolic BP: %{y:.1f} mmHg"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=patient_vitals["visit_date"],
            y=patient_vitals["diastolic_bp"],
            mode="lines+markers",
            name="Diastolic BP",
            hovertemplate=(
                "Date: %{x|%Y-%m-%d}"
                "<br>Diastolic BP: %{y:.1f} mmHg"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=patient_vitals["visit_date"],
            y=patient_vitals["glucose"],
            mode="lines+markers",
            name="Glucose",
            yaxis="y2",
            hovertemplate=(
                "Date: %{x|%Y-%m-%d}"
                "<br>Glucose: %{y:.1f} mg/dL"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        title="Patient Vital Sign Trends",
        xaxis=dict(
            title="Visit Date",
            type="date",
            tickformat="%b %d",
        ),
        yaxis=dict(
            title="Blood Pressure (mmHg)",
        ),
        yaxis2=dict(
            title="Glucose (mg/dL)",
            overlaying="y",
            side="right",
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        margin=dict(
            l=20,
            r=20,
            t=80,
            b=20,
        ),
        height=500,
    )

    return figure