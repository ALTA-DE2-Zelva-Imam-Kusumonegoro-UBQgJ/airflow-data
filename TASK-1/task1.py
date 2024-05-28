from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'xcom_task1',
    default_args=default_args,
    description='DAG akan berjalan setiap 5 jam',
    schedule_interval=timedelta(hours=5),
)

def push_to_xcom(**kwargs):
    task_instance = kwargs['ti']
    task_instance.xcom_push(key='key1', value='value1')
    task_instance.xcom_push(key='key2', value='value2')

push_task = PythonOperator(
    task_id='push_to_xcom',
    python_callable=push_to_xcom,
    provide_context=True,
    dag=dag,
)

def pull_from_xcom(**kwargs):
    task_instance = kwargs['ti']

    value1 = task_instance.xcom_pull(task_ids='push_to_xcom', key='key1')
    value2 = task_instance.xcom_pull(task_ids='push_to_xcom', key='key2')

    print(f'Nilai yang ditarik: {value1}, {value2}')

pull_task = PythonOperator(
    task_id='pull_from_xcom',
    python_callable=pull_from_xcom,
    provide_context=True,
    dag=dag,
)

push_task >> pull_task
