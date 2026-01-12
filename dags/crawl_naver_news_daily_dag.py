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

years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

for year in years:
    dag_id = f'naver_news_crawler_{year}'
    
    with DAG(
        dag_id=dag_id,
        default_args=default_args,
        start_date=datetime(year, 1, 1),
        end_date=datetime(year, 12, 31),
        schedule_interval='@daily', # 매일 하루치씩
        catchup=True,               # 과거 데이터 수집 활성화
        max_active_runs=1           # 연도별로 딱 하나씩만 실행 (IP 차단 방지)
    ) as dag:
        
        task = BashOperator(
            task_id=f'crawl_task_{year}',
            bash_command=f'python /opt/airflow/dags/news_crawler_selenium.py {{{{ ds }}}}',
        )
        
        # 이 변수가 전역 범위에 있어야 Airflow가 DAG를 인식합니다.
        globals()[dag_id] = dag

'''
# 1번 DAG 정의 : 2016년 1월 ~ 2020년 12월 

with DAG(
    # 1. 여기에 들어가는 이름이 웹 UI에 노출되는 진짜 이름입니다.
    dag_id='crawl_news_2016_2020_daily_dag', 
    start_date=datetime(2016, 1, 1),
    end_date=datetime(2020, 12, 31),
    ## schedule_interval='5 * * * *', # 분 시 일 월 요일
    ## chedule_interval='5 */4 * * *', # 분 시 일 월 요일
    catchup=True, # catchup=False : 백필 작업을 하지 않음
    max_active_runs=1 # IP 차단 방지 (하나씩 실행)

) as dag1: # 중복 불가

    task_crawl = BashOperator(
        task_id='run_python_file', # 중복 불가
        bash_command='python /opt/airflow/dags/news_crawler_selenium.py {{ ds }}',
    )

# 2번 DAG 정의 : 2021년 1월 ~ 2025년 12월 
with DAG(
    # 1. 여기에 들어가는 이름이 웹 UI에 노출되는 진짜 이름입니다.
    dag_id='crawl_news_2021_2025_daily_dag', 
    start_date=datetime(2021, 1, 1),
    end_date=datetime(2025, 12, 31),
    schedule_interval='5 * * * *', # 분 시 일 월 요일
   ## schedule_interval='0 */4 * * *', # 분 시 일 월 요일
    catchup=True,
    max_active_runs=1  
) as dag2:
        task_crawl = BashOperator(
        task_id='run_python_file2',
        bash_command='python /opt/airflow/dags/news_crawler_selenium.py {{ ds }}',
    )
    '''