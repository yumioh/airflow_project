import requests.exceptions as requests_exceptions
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine # db 연결
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook

## airflow의 mysql hook 사용하여 db 연결
mysql_hook = MySqlHook(mysql_conn_id='fin_mysql')

def upload_data() :
    file_path = '/opt/airflow/dags/data/Credit_Evaluation_Fund_Trans_hist.xlsx'
    df = pd.read_excel(file_path)

    column_mapping = {
        '회계구분코드': 'acc_type_code',
        '이체상태구분코드': 'trans_status_code',
        '이체자금구분코드': 'trans_fund_type_code',
        '거래은행코드': 'bank_code',
        '입금계좌명': 'deposit_account_name',
        '입금의뢰금액': 'request_amount',
        '입금의뢰인명': 'requester_name',
        '거래키': 'trans_key',
        '지급계좌번호': 'payout_account_number',
        '이체일자': 'trans_date',
        '이체시간': 'trans_time',
        '이체금액': 'trans_amount',
        '이체수수료': 'trans_fee',
        '이체오류금액': 'trans_err_amount',
        '이체오류코드': 'trans_err_code',
        '이체본지점거래일시': 'trans_branch_datetime',
        '기타자금청구사유내용': 'other_fund_request_reason',
        '청구자직원번호': 'request_staff_no',
        '확인자직원번호': 'confirm_staff_no',
        '이체자직원번호': 'trans_staff_no',
        '청구합계금액': 'total_request_amount',
        '조회거래KEY': 'search_trans_key',
        '삭제여부': 'delete_yn',
        '최종수정수': 'final_mod_count',
        '처리직원번호': 'proc_staff_no',
        '최초처리직원번호': 'init_proc_staff_no'
    }

    df.rename(columns=column_mapping, inplace=True)
    
    df['trans_date'] = pd.to_datetime(df['trans_date'], errors='coerce')
    df['trans_time'] = pd.to_datetime(df['trans_time'], errors='coerce').dt.time
    df['trans_branch_datetime'] = pd.to_datetime(df['trans_branch_datetime'], errors='coerce')
    df = df.where(pd.notnull(df), None)

    # 형식: mysql+pymysql://아이디:비밀번호@서비스이름:포트/DB이름
    # engine = create_engine('mysql+pymysql://airflow:airflow@external-mysql:3306/fin_db')
    # name : 테이블 이름, if_exists : 교체(replace) 또는 추가(append)
    df.to_sql(name='fund_transfer_history', con=mysql_hook.get_sqlalchemy_engine(), if_exists='replace', index=False)
    print("성공적으로 DB에 저장되었습니다.")

def transform_data() :
    sql = f"""
        SELECT * FROM fund_transfer_history;
    """

    df = pd.read_sql(sql, con=mysql_hook.get_sqlalchemy_engine())

    print(f"가공 전 첫 줄 값: {df['request_amount'].iloc[0]}")

    if df.empty:
        print("가져올 데이터가 없습니다.")
        return

    df['request_amount'] = pd.to_numeric(df['request_amount']) + 1000
    print(f"가공 후 첫 줄 값: {df['request_amount'].iloc[0]}")
    df.to_sql('new_fund_transfer_history', con=mysql_hook.get_sqlalchemy_engine(), if_exists='replace', index=False)
    print(f"{len(df)}건의 데이터를 가공하여 new_fund_transfer_history에 저장했습니다.")

# DAG 설정
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1), # 확실한 과거를 잡아두면 활성화는 즉시 실행 가능한 상태가 됨
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

# with 안에 있는 DAG 해당 DAG에 속해 있음
with DAG(
    dag_id='file_to_mysql',
    default_args=default_args,
    schedule_interval=None,  # 수동 실행
    catchup=False
) as dag:

    # data upload
    upload_task = PythonOperator(
        task_id='upload_excel_data', 
        python_callable=upload_data
    )

    # data transform
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    # task 실행 순서
    upload_task >> transform_task

