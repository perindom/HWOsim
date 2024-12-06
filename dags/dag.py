from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from batch_ingest import load_data

# DAG configuration
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="astroquery_data_upload",
    default_args=default_args,
    description="Ingest JWST public JPEG files to S3",
    schedule_interval=None,  # Manual trigger
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:
    # Define the task
    astroquery_data_upload = PythonOperator(
        task_id="astroquery_data_upload",
        python_callable=load_data,
        op_kwargs={"limit": 100},  # Adjust limit as needed
    )
astroquery_data_upload
