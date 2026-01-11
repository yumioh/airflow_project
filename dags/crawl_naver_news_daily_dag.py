from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# 1. 기본 설정 (Default Args)
default_args = {
    'owner': 'airflow', # 소유자
    'depends_on_past': False, # 작업을 실패애도 예정대로 실행
    'retries': 5, # 재실행 횟수  
    'retry_delay': timedelta(minutes=5), # 재실행 간격
}

# 1번 DAG 정의 : 2017년 1월 ~ 2020년 10월 
with DAG(
    # 1. 여기에 들어가는 이름이 웹 UI에 노출되는 진짜 이름입니다.
    dag_id='crawl_never_news_daily_dag', 
    start_date=datetime(2026, 1, 12),
    end_date=datetime(2026, 1, 13),
    schedule_interval='0 */4 * * *', # 분 시 일 월 요일
    catchup=False
) as dag1: # 중복 불가

    task_crawl = BashOperator(
        task_id='run_python_file', # 중복 불가
        bash_command='python /opt/airflow/dags/news_crawler_selenium.py ',
    )

# 2번 DAG 정의 : 2017년 1월 ~ 2020년 10월 
with DAG(
    # 1. 여기에 들어가는 이름이 웹 UI에 노출되는 진짜 이름입니다.
    dag_id='crawl_never_news_daily_dag2', 
    start_date=datetime(2026, 1, 12),
    end_date=datetime(2026, 1, 13),
    schedule_interval='0 */4 * * *', # 분 시 일 월 요일
    catchup=False
) as dag2:
        task_crawl = BashOperator(
        task_id='run_python_file2',
        bash_command='python /opt/airflow/dags/news_crawler_selenium.py ',
    )