# Threat Model

## Scope

This threat model covers the Airflow weather ML pipeline.

## Assets

| Asset | Security objective |
|---|---|
| API key | Confidentiality |
| Raw weather data | Integrity |
| Transformed CSV files | Integrity |
| Trained model | Integrity |
| Airflow DAG | Integrity |
| Audit reports | Traceability |

## Threats

| Threat | Impact | Control |
|---|---|---|
| API key committed to GitHub | Secret exposure | Use Airflow Variable and example file only |
| Malformed city variable | Failed API calls or unexpected behavior | City validation |
| API response manipulation | Poisoned training data | JSON field validation |
| Empty or corrupted CSV | Bad model training | CSV checks |
| Uncontrolled model overwrite | Integrity loss | Model hash and metadata |
| Untracked automated action | Lack of auditability | Final security audit task |

## Residual risks

| Risk | Comment |
|---|---|
| External API trust | The pipeline still trusts OpenWeatherMap as source of truth |
| Local Airflow secrets | Airflow Variables are acceptable for this lab but not ideal for production |
| Dashboard exposure | The dashboard is exposed locally without authentication |
| Model governance | This experiment does not use a production model registry |
