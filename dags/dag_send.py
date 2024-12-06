from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from mysqlcode import send_images

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
    dag_id="send_to_mysql",
    default_args=default_args,
    description="Send to MySQL",
    schedule_interval=None,  # Manual trigger
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:
    # Define the task
    send_images = PythonOperator(
        task_id="send_images",
        python_callable=send_images,
        op_kwargs={},  # Adjust limit as needed
    )
send_images
