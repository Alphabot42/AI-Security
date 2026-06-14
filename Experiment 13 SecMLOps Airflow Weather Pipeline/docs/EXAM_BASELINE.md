# Airflow Weather Pipeline

This archive contains the Airflow evaluation DAG.

## Objective

The DAG collects weather data from OpenWeatherMap, stores raw JSON files, transforms the data into CSV files, trains several regression models, selects the best model and saves it for the dashboard.

## Main files

- dags/weather_secmlops_dag.py: complete Airflow DAG
- docker-compose.yaml: Airflow and dashboard stack
- raw_files/: generated raw weather JSON files
- clean_data/: generated CSV files and best_model.pickle

## Airflow Variables

The DAG expects two Airflow Variables:

- cities: list of city names
- api_key: OpenWeatherMap API key

The API key is not hardcoded in the Python file.

## Minimal security controls

- API key stored in an Airflow Variable
- cities validated before API calls
- timeout on API requests
- HTTP status checked
- JSON fields checked before transformation
- empty CSV files rejected
- generated files verified after execution
