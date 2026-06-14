# Security Notes

## Secrets

The OpenWeatherMap API key must be stored in Airflow Variables and must not be hardcoded in the DAG.

Never commit the following files.

.env
Airflow secrets
API keys
generated raw JSON files
generated CSV files
model pickle files

## Data trust boundary

The pipeline consumes data from an external API. This creates a trust boundary between the external weather provider and the internal ML pipeline.

The DAG validates city names, HTTP response status, expected JSON structure, temperature, pressure, city fields, and empty CSV files.

## Model integrity

The selected model is hashed with SHA256 after training.

The hash is written to model_metadata.json and security_audit.json.

## Operational safety

The Airflow DAG automates external API calls, file creation, transformation, model training, model selection, and model persistence.

The final security_audit task checks that expected outputs exist and are not empty.

## Known limitations

This is a learning experiment, not a production deployment.

Current limitations are no production secret backend, no signed model registry, no dependency scanning pipeline, no API allowlist enforcement outside the DAG, and no dashboard authentication.

## Fernet encryption validation

Airflow Fernet encryption was enabled through AIRFLOW__CORE__FERNET_KEY in the local .env file.

The .env file is ignored by Git and must never be committed.

Runtime validation confirmed that the Airflow container had a configured Fernet key and that Airflow Variables were stored as encrypted values.

Evidence:

screenshots/airflow_fernet_configured_cli.png
screenshots/airflow_variables_encrypted.png

