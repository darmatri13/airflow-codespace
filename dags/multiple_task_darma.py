from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define a Python function to print "Hello, World!"
def print_hello():
    print("Hello, World!")

# Default arguments
    default_args={
    'owner': 'airflow', 
    'email': 'airflow@example.com', 
    'retries': 3,  # Number of retries for failed tasks
    'retry_delay': timedelta(minutes=5),  # Delay between retries
    'depends_on_past': False,  # Set to True to consider past runs when determining if a DAG should be triggered
    'wait_for_downstream': False,  # Set to True to wait for all immediate downstream tasks to finish before marking the current task as complete
    'email_on_failure': True,  # Set to False to disable email notifications on task failure
    'email_on_retry': True,  # Set to False to disable email notifications on task retries
    'execution_timeout': timedelta(hours=1),  # Time limit for task execution
    'sla': timedelta(hours=2)  # Service Level Agreement for task execution
}


# Define the DAG
dag = DAG(
    dag_id='multiple_task_darma',
    description='My DAG Description',
    schedule_interval='@daily',
    start_date=datetime(2022, 1, 1),
    end_date=datetime(2022, 1, 31),  # Optional end date
    default_args={'owner': 'airflow', 'email': 'airflow@example.com'},  # Default arguments
    catchup=False,  # Disable backfilling
    tags=['example', 'tag']  # Tags for categorization
)

# Define tasks
start_task = DummyOperator(task_id='start', dag=dag)

hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag
)

end_task = DummyOperator(task_id='end', dag=dag)

# Define task dependencies
start_task >> hello_task >> end_task