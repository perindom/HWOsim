from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Import your Python function from the perturbation script
from perturb_s3_to_s3 import process_all_fits_in_s3

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'jwst_perturbation_pipeline',
    default_args=default_args,
    description='Apply perturbations to JWST FITS files from S3 Data_Lake and save to S3 Applied_Perturbations',
    schedule_interval=None,  # Set to None for manual trigger, or use a cron expression
    catchup=False,
) as dag:

    # Define the task
    perturb_task = PythonOperator(
        task_id='apply_perturbations',
        python_callable=process_all_fits_in_s3,
    )
