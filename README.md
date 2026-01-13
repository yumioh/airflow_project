# AIRFLOW PROJECT
* version : 3.1.3
* version : 2.10.4으로 변경

# Folder Structure
airflow_project/
├── dags/                # DAG 파일들이 위치하는 곳
│   └── my_dag.py  # 여기에 코드를 작성합니다
├── logs/                # 실행 로그가 저장되는 곳
├── plugins/             # 커스텀 플러그인 
└── .venv/               # 파이썬 가상환경 

# docker 
* 명령어 : 
 - docker-compose up : yaml 파일에 적힌 컨테이너들을 한꺼번에 만들고 네트워크 연결하고, 실행까지 하는 명령어
 - docker-compose up -d : 터미널을 닫아도 배경(Background)에서 Airflow가 계속 돌아감
 - docker ps : docker 상태 확인
 - docker-compose down : shut down docker
 - docker ps --format "{{.Names}}" : 현재 컴퓨터에 돌아가고 있는 서비스 목록
 - docker-compose down --volumes --remove-orphans : 기존 환경 삭제 
 - curl -LfO https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml : 2.10.4 설정 파일 다운로드
 - docker-compose up airflow-init : 초기회(DB와 계정 생성)

 * 서비스명
 * airflow_project-airflow-webserver-1 : WEB서비스

 * DAG 실행은 파이썬 코드로 직접 실행하는게 아니라 웹브라우저에서 접속하여 실행 

 * PythonOperator : 파이썬으로 적성한 로직을 airflow 안에서 직접 실행할때 사용 예) 데이터 가공, api호출, db연동 등 파이썬 라이브러리 활용 
 * BashOperator : 쉘 명령어 또는 쉘 스크립 파일 실행시 사용 예) java, jar실행, 파일 시스템 조작 등 

 * StartDate와 endDate는 DAG 작업 자체가 생성이 되고 유효 기간을 의미 => 과거 일자로 설정해도 Airflow의 backfill과 catchup 기능으로 과거에 밀린 작업들을 현재 시점에서 한꺼번에 순차적으로 실행

 * 경로 확인 
    docker exec -it e3024f24a4b4 ls -l //opt/airflow/dags/scripts/_news_crawler_selenium.py