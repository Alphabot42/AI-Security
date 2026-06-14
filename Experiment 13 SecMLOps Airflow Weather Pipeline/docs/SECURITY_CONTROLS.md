# Security Controls

## Implemented controls

Secret separation:
The OpenWeatherMap API key is loaded from an Airflow Variable.

Input validation:
The city list is validated before API calls.

API timeout:
The requests timeout is set to 10 seconds.

HTTP validation:
Non successful API responses raise an error.

JSON field validation:
Required fields are checked before writing the CSV files.

Empty dataset protection:
Empty CSV files raise an error.

Model integrity:
The selected model is hashed with SHA256.

Model metadata:
model_metadata.json documents the selected model, score, features, training rows and SHA256 hash.

Auditability:
security_audit.json documents the final checks.

## Generated audit fields

The final audit report contains:

data_csv
fulldata_csv
model
model_metadata
model_sha256
checked_at_utc
status

## Future improvements

Use a production secret backend.
Add dependency scanning.
Add Docker image pinning by digest.
Add schema validation with Pydantic.
Add model registry integration.
Add dashboard authentication.
Add CI checks for secrets and Python syntax.

## Fernet based variable encryption

Airflow Variables are encrypted at rest using Fernet.

The Fernet key is configured locally with AIRFLOW__CORE__FERNET_KEY and stored only in the ignored .env file.

The api_key variable was validated in the Airflow UI with Is Encrypted set to True.

