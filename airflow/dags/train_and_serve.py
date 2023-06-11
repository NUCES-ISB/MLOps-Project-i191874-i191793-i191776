from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import numpy as np

def load_data():
    global df
    df = pd.read_csv('iris_input.csv', header=None, names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])

def check_missing_values():
    global df
    if df.isnull().values.any():
        df = df.replace(np.nan, 0)

def write_data():
    global df
    df.to_csv('iris_output.csv', index=False)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 6, 11),
    'retries': 0,
}

dag = DAG('iris_data_cleaning',
          default_args=default_args,
          description='An Airflow DAG to clean Iris data',
          schedule_interval='@once',
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

check_missing_values_task = PythonOperator(
    task_id='check_missing_values',
    python_callable=check_missing_values,
    dag=dag,
)

write_data_task = PythonOperator(
    task_id='write_data',
    python_callable=write_data,
    dag=dag,
)

load_data_task >> check_missing_values_task >> write_data_task
