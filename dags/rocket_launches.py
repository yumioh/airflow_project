import json
import pathlib
import airflow
import requests
import requests.exceptions as requests_exceptions

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


dag = DAG(
    dag_id = "download_rockect_launches", # airflow에 표시되는 DAG 이름
    start_date = airflow.utils.dates.days_ago(14), # workflow가 처음 실행되는 날짜/시간
    schedule_interval='5 * * * *', # dag 실행 간격 
    catchup=False, # 현재부터 실행되지 않는 과거의 구간부터 시작 , FALSE 과거 기록은 무시하고 현재시점에 가까운 스케줄부터 실행
)

download_launches = BashOperator (
    task_id = "downlad_lauches", # Task Name
    bash_command = "curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'", # 실행할 bash 명령어
    dag=dag, # DAG 변수에 대한 참조
)

def _get_pictures():
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True) # 폴더 생성
    with open("/tmp/launches.json") as f: 
        launches = json.load(f) # lausches 변수에 딕션너리로 읽기 
        image_urls = [launch["image"] for launch in launches["results"]] # launches["results"]안에 있는 각 발사 정보에서 image 필드를 뽑아 image_urls 리스트 생성
    for image_url in image_urls:
        try:
            response = requests.get(image_url)
            image_filename = image_url.split("/")[-1]
            target_file = f"/tmp/images/{image_filename}"
            with open(target_file, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {image_url} to {target_file}")
        except requests_exceptions.MissingSchema:
            print(f"{image_url} appears to be an invalid URL.")
        except requests_exceptions.ConnectionError:
            print(f"Could not connect to {image_url}.")

get_pictures = PythonOperator( # 지정한 파이썬 함수 하나를 실행하는 task
    task_id="get_pictures",
    python_callable=_get_pictures, # 실제 테스크 작업으로 사용
    dag=dag,
)

notify = BashOperator(
    task_id="notify", # 디렉토리에 있는 파일 개수를 세서 출력하는 task 명
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."', # 디렉토리 안 파일 개수
    dag=dag,
)

# 태스크 실행 순서
download_launches >> get_pictures >> notify