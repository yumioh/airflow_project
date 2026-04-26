# AIRFLOW PROJECT
* version : 3.1.3
* version : 2.10.4으로 변경 -- selenium 

# Folder Structure
airflow_project/
├── dags/                # DAG 파일들이 위치하는 곳
│   └── my_dag.py  # 테스트용 DAG
│   └── rocket_launches.py # thespacedevs 데이터 들고 오는 DAG
├── logs/                # 실행 로그가 저장되는 곳
├── plugins/             # 커스텀 플러그인 
└── .venv/               # 파이썬 가상환경 


# 도커 핵심 요소 
- 이미지 : 설계도 실행에 필욯나 모든 파일을 모아둔 읽기 전용 파일 
- 컨테이너 : 실제 건물 이미지를 실행시킨 상태. 독립된 가상 공간에서 실제로 프로그램이 돌아가는 환경
- 레지스트리 : 중앙 창고(docker hub) 이미지를 저장하여 똑같은 환경을 다시 꺼내 쓰기 위한 영구 저장소 => github와 유사

# docker 
* 명령어 : 
 - docker-compose up : yaml 파일에 적힌 컨테이너들을 한꺼번에 만들고 네트워크 연결하고, 실행까지 하는 명령어
 - docker-compose up -d : 터미널을 닫아도 배경(Background)에서 Airflow가 계속 돌아감
 - docker ps : docker 상태 확인
 - docker-compose down : shutdown docker
 - docker-comopse down --volumes : 기존 컨테이너 정리 
 - docker ps --format "{{.Names}}" : 현재 컴퓨터에 돌아가고 있는 서비스 목록
 - docker-compose down --volumes --remove-orphans : 기존 환경 삭제 
 - curl -LfO https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml : 2.10.4 설정 파일 다운로드
 - docker-compose up airflow-init : 초기회(DB와 계정 생성)
 - docker exec -it e3024f24a4b4 ls -l //opt/airflow/dags/scripts/_news_crawler_selenium.py : 경로 확인 
 - docker exec -it airflow-airflow-scheduler-1 //bin/bash  : scheduler 들어가기
 - docker exec -u airflow -it airflow_project-airflow-scheduler-1 /bin/bash -c "pip install selenium beautifulsoup4 pandas"
 - docker exec -u airflow -it airflow_project-airflow-worker-1 pip install --upgrade pip
 - docker-compose restart airflow-worker airflow-scheduler : 해당 부분 재시작
 - docker exec -u 0 -it airflow_project-airflow-worker-1 apt-get update
 - docker exec -u 0 -it airflow_project-airflow-worker-1 apt-get install -y wget gnupg unzip libgconf-2-4 libnss3 libxss1 libasound2
 - docker exec -u 0 -it airflow_project-airflow-worker-1 /bin/bash -c "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list && apt-get update && apt-get install -y google-chrome-stable"

 - docker-compose restart airflow-scheduler : 서비스를 끄지 않고 실행 중인 프로세스만 재실행

 * 서비스명
 * airflow_project-airflow-webserver-1 : WEB서비스

 * DAG 실행은 파이썬 코드로 직접 실행하는게 아니라 웹브라우저에서 접속하여 실행 

 * PythonOperator : 파이썬으로 적성한 로직을 airflow 안에서 직접 실행할때 사용 예) 데이터 가공, api호출, db연동 등 파이썬 라이브러리 활용 
 * BashOperator : 쉘 명령어 또는 쉘 스크립 파일 실행시 사용 예) java, jar실행, 파일 시스템 조작 등 

 * StartDate와 endDate는 DAG 작업 자체가 생성이 되고 유효 기간을 의미 => 과거 일자로 설정해도 Airflow의 backfill과 catchup 기능으로 과거에 밀린 작업들을 현재 시점에서 한꺼번에 순차적으로 실행

 * 리눅스 패키지 설치 
apt-get update \
   &&  apt-get install -y --no-install-recommends \ 필수적이지 않는거 설치 하지 않음
   chromium \
   && apt-get autoremove -yqq --purge \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

컨테이너 중지 및 삭제
- docker-compose down 기존 컨테이너 삭제
- docker-compose down -v (기존에 생성된 DB 볼륨까지 지움)
- docker compose build --no-cache 이전 이미지 캐시 삭제


해당하는 dag list 확인하기 
- docker exec -it airflow_project-airflow-scheduler-1 airflow dags list

postgres 컨테이너 meta DB 접속
- docker exec -it airflow-postgres psql -U airflow
- \dt : 목록 확인, \q 종료

mysql 접속
- docker exec -it external-mysql mysql -u airflow -p
- SET NAMES utf8mb4;

수동 설치 명령어(root)
- docker exec -u 0 -it airflow_project-airflow-worker-1 python3 -m pip install openpyxl
- -u 0 (관리자 권환으로 강제 실행)
- -it (표준입력)

설정 파일 수정한 후 컨테이너를 새로 생성하는 명시 하는 명령어
- docker-compose up -d --force-recreate

도커
- 볼륨을 생성한다는 건 컨테이너가 사라져도 데이터는 삭제되지 않게 별도의 저장 공간을 만드는것 
- 컨테이너 내부에 파일을 저장하면, 컨테이너를 삭제하는 순간 그 안의 데이터는 영구적으로 삭제 => 중요한 데이터는 외부인 호스트 PC에 따로 빼두어야함
- Named Volume (도커가 관리) : 도커가 호스트 pc의 특정 안전한 구역에 폴더를 만들고 관리 => 사용자는 실제 경로가 어디인지 신경쓸 필요없이 이름만 붙여서 사용
- Blind Mount(내가 직접 경로 지정) : 내 컴퓨터의 특정 폴더와 컩테이너 내부 폴더를 직접 연결


** 공공데이터 api url만 변경하여 airflow 끌고 올 수 있도록 만들기
** mission : airflow -> elasticsearch로 넣어서 처리하는 방법 생각해보기 