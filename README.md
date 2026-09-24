# Clinical Metrics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-3F4F75?style=for-the-badge\&logo=plotly\&logoColor=white)

A clinical analytics dashboard built with **Streamlit, Pandas, and Plotly** for exploring synthetic patient data, monitoring clinical metrics, analyzing vital trends, and reviewing visit history.


## Features

* Patient selection with demographic information
* Cohort-level patient and visit statistics
* Date-based visit filtering
* Blood pressure and glucose monitoring
* Readmission risk and risk-level display
* Interactive vital trend charts
* Structured patient visit history
* Clean and responsive healthcare dashboard UI



## Tech Stack

| Technology | Purpose                 |
| ---------- | ----------------------- |
| Python     | Application development |
| Streamlit  | Dashboard and UI        |
| Pandas     | Data processing         |
| Plotly     | Interactive charts      |



## Project Structure

```text
Clinical-Metrics-Dashboard/
│
├── src/
│   ├── charts.py
│   ├── data_loader.py
│   └── metrics.py
│
├── app.py
├── requirements.txt
└── README.md
```



## Getting Started

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
streamlit run app.py
```



## Data

The dashboard uses **synthetic clinical data** for development, visualization, and demonstration purposes.

The data includes:

* Patient demographics
* Clinical visits
* Blood pressure
* Glucose levels
* Readmission risk



## Disclaimer

This dashboard uses synthetic data and is intended for software demonstration and analytics development only. It is not intended for medical diagnosis, treatment, or clinical decision-making.



## License

This project is licensed under the **MIT License**.
