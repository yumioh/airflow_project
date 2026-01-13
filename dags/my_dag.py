from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# 1. 기본 설정 (Default Args)
default_args = {
    'owner': 'airflow', # 소유자
    'start_date': datetime(2017, 1, 1), # 시작날짜 필수적으로 지정
    'depends_on_past': False, # 작업을 실패애도 예정대로 실행
    'retries': 5, # 재실행 횟수  
    'retry_delay': timedelta(minutes=5), # 재실행 간격
}

# 2. 파이썬 함수 정의
def print_hello():
    return 'Hello! This is my first Airflow DAG.'

# 3. DAG 정의
with DAG(
    'my_simple_airflow_dag',      # DAG ID (중복 불가)
    default_args=default_args,
    description='Sample DAG',
    schedule=timedelta(days=1),  # 매일 실행
    ## start_date=datetime(2026, 1, 13),
    ## end_date=datetime(2026, 1, 13),
    catchup=False,
) as dag:

    # Task 1: Bash 명령 실행
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    # Task 2: 파이썬 함수 실행
    t2 = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello,
    )

    # 4. 태스크 순서 설정 (t1 실행 후 t2 실행)
    t1 >> t2