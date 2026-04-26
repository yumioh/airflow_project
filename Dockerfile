FROM apache/airflow:2.10.5

# 필요한 패키지들을 한 번에 설치합니다.
RUN pip install --no-cache-dir \
    "WTForms<3.0.0" \
    openpyxl \
    "typing-extensions>=4.5.0" \
    selenium \
    beautifulsoup4 \
    pandas \
    cryptography \
    pymysql \
    apache-airflow-providers-fab==1.3.0 \
    apache-airflow-providers-mysql