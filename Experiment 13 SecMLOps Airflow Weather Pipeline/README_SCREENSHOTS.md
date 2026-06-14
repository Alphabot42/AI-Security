# Selected screenshots

These screenshots were selected for the GitHub experiment and the future article.

## Included files

1. screenshots/airflow_variables_encrypted.png
   Evidence that Airflow Variables are encrypted at rest with Fernet.

2. screenshots/airflow_fernet_configured_cli.png
   CLI proof that Fernet is configured inside the Airflow container.

3. screenshots/openweather_api_key_test_ok_cli.png
   CLI proof that the OpenWeatherMap API key works without exposing the key.

4. screenshots/airflow_import_errors_none_and_dag_paused_cli.png
   CLI proof that the DAG imports correctly and is paused to avoid uncontrolled scheduled runs.

5. screenshots/airflow_graph_success.png
   Airflow Graph view showing the successful DAG, including security_audit.

6. screenshots/airflow_security_audit_logs.png
   Logs from the security_audit task showing report creation and task success.

7. screenshots/runtime_outputs_model_metadata_security_audit.png
   Terminal evidence of generated artifacts, model metadata, model SHA256, and security_audit status passed.

8. screenshots/airflow_task_duration.png
   Airflow Task Duration view for runtime observability.

9. screenshots/airflow_landing_times.png
   Airflow Landing Times view for execution observability.

10. screenshots/airflow_dag_audit_log.png
    Airflow Audit Log view for traceability.

11. screenshots/airflow_cluster_activity_healthy.png
    Cluster Activity view showing a healthy metadatabase and scheduler after execution.

## Not included

Intermediate screenshots showing failed API key, unencrypted Variables, or running queued states were excluded because they are useful for debugging but not for the final GitHub version.
