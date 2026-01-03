from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(0, '/opt/airflow/src')

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='Production weather data pipeline',
    schedule_interval='0 2 * * *',
    catchup=False,
) as dag:
    
    def extract_weather():
        print("Extracting weather data...")
        return "Data extracted"
    
    def transform_data():
        print("Transforming data...")
        return "Data transformed"
    
    def quality_check():
        print("Running quality checks...")
        return "Quality checks passed"
    
    extract = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract_weather,
    )
    
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )
    
    quality = PythonOperator(
        task_id='quality_check',
        python_callable=quality_check,
    )
    
    extract >> transform >> quality
