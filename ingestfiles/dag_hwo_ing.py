from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

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
    dag_id="jwst_data_ingestion",
    default_args=default_args,
    description="Ingest JWST public FITS files to S3",
    schedule_interval=None,  # Manual trigger
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:

    def run_ingestion(limit):
        import sys
        sys.path.append("/root/airflow/dags")  # Ensure batch_ingest is found
        from batch_ingest import fetch_and_upload_jwst_data
        fetch_and_upload_jwst_data(limit)

    # Define the task
    ingest_jwst_data_task = PythonOperator(
        task_id="ingest_jwst_data",
        python_callable=run_ingestion,
        op_kwargs={"limit": 100},  # Adjust limit as needed
    )

    ingest_jwst_data_task
