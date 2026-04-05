FROM apache/airflow:2.10.5

RUN pip install --no-cache-dir \
    typing-extensions>=4.5.0 \
    selenium \
    beautifulsoup4 \
    pandas \
    apache-airflow-providers-fab==1.3.0 