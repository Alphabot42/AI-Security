# Architecture

## Overview

This experiment uses Apache Airflow to orchestrate a weather machine learning pipeline.

The pipeline collects weather data, transforms it, trains regression models, selects the best model, and performs a security audit on the generated artifacts.

## Components

| Component | Responsibility |
|---|---|
| OpenWeatherMap API | External weather data source |
| Airflow DAG | Pipeline orchestration |
| Airflow Variables | Runtime configuration and API key storage |
| raw_files | Raw JSON storage |
| clean_data | CSV, model, metadata and audit output storage |
| scikit learn | Model training |
| Dashboard | Visualization layer |

## Data flow

OpenWeatherMap API
        |
        v
fetch_weather_data
        |
        v
raw JSON files
        |
        v
transform_recent_data and transform_full_data
        |
        v
CSV datasets
        |
        v
model training task group
        |
        v
best model selection
        |
        v
model metadata and SHA256 hash
        |
        v
security audit report

## Runtime outputs

| Output | Location |
|---|---|
| Raw weather JSON | /app/raw_files |
| Transformed CSV | /app/clean_data |
| Best model | /app/clean_data/best_model.pickle |
| Model metadata | /app/clean_data/model_metadata.json |
| Security audit | /app/clean_data/security_audit.json |
