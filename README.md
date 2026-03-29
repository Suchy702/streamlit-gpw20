# GPW20 Minimal Viewer

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Status: In Progress](https://img.shields.io/badge/status-in%20progress-orange)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-ff4b4b?logo=streamlit&logoColor=white)](https://gpw20viewer.streamlit.app/)

GPW20 Minimal Viewer is a web application for tracking the top 20 companies listed on the Polish stock exchange. It includes an end-to-end data pipeline built with [Apache Airflow](https://airflow.apache.org/), yfinance, pandas, [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/products/postgresql/), and an interactive [Streamlit](https://streamlit.io/) dashboard.

## Live App

[gpw20viewer.streamlit.app](https://gpw20viewer.streamlit.app/)

<img width="1500" height="1200" alt="Dashboard preview" src="https://github.com/user-attachments/assets/c60cc7b3-00c1-4b5d-9eab-8be67d528686" />

## Local Hosting

```bash
./main up   # Run Streamlit app locally
./main down # Stop Streamlit app
```

## Architecture

1. **Data collection**: Apache Airflow orchestrates the pipeline and schedules periodic downloads from yfinance.
2. **Data storage**: Market data is stored in Azure Database for PostgreSQL.
3. **Data visualization**: Streamlit reads data from PostgreSQL and presents it in an interactive dashboard.

<p align="center">
    <img src="gpw20Viewer.drawio.svg" alt="Architecture diagram" width="500" />
</p>

## How This Project Was Built

### PostgreSQL on Azure

The first major step was setting up a PostgreSQL database on Azure. I chose this stack mainly for learning purposes: I wanted practical experience with PostgreSQL and cloud deployment. The [GitHub Student Developer Pack](https://education.github.com/pack) also made Azure experimentation more accessible.

To keep setup and costs low, I selected **Azure Database for PostgreSQL Flexible Server** with the minimum compute and memory configuration.

<img width="400" height="505" alt="Azure PostgreSQL setup" src="https://github.com/user-attachments/assets/5bea9560-9a05-4fc4-a199-6229c393eb15" />

With this minimal plan, estimated monthly cost after free limits would be around **$18/month**.

After configuration, I seeded the database with initial records and validated queries and connectivity.

<img width="1200" height="550" alt="Database test results" src="https://github.com/user-attachments/assets/b3492520-de31-4674-9261-b7fdedf0a2bb" />

The database ran reliably, and integration with Airflow, VS Code, and Streamlit was straightforward.

### Apache Airflow

I chose Apache Airflow to orchestrate tasks and to learn the tool in practice. Airflow manages pipeline execution with DAGs (Directed Acyclic Graphs), where each task depends on previous successful steps.

For local development, I used the official Airflow Docker Compose setup:

- <https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html>

I created tasks that:

- read the ticker list and baseline prices from PostgreSQL,
- fetch current prices from Yahoo Finance using [yfinance](https://github.com/ranaroussi/yfinance),
- store fresh records and compute percentage price changes.

```python
@dag(
        dag_id="postgres_wa_tickers",
        description="Fetches latest stock prices, gets current prices from yfinance, and stores percent changes",
        start_date=datetime(2026, 3, 28),
        schedule="*/5 9-17 * * 1-5",  # Every 5 minutes during Polish market hours (weekdays)
        catchup=False,
        tags=["postgres", "stocks", "wa", "yfinance"],
)
```

Airflow UI preview:

<img width="1800" height="700" alt="Airflow UI" src="https://github.com/user-attachments/assets/e7b6fe79-6b7d-490e-9b4d-cd268bf92f8b" />

Airflow requires initial setup, but it is very convenient for monitoring task logs and debugging pipelines. A simpler scheduler could work for this project, but Airflow was intentionally selected as a learning goal.

Planned next step: host Airflow on an Azure VM so it can run continuously. Right now, it runs only on my local machine.

### Streamlit

Because this project is focused on data engineering, I chose Streamlit as the fastest way to build a frontend. It matches the project needs well and can be deployed easily through [Streamlit Community Cloud](https://streamlit.io/cloud).

I added database credentials securely and deployed the application.

<img width="1800" height="210" alt="Streamlit secrets configuration" src="https://github.com/user-attachments/assets/73501284-713c-4bcd-8485-5960d56a0216" />

## Planned Improvements

- Create a dedicated Airflow repository with automated deployment to Azure.
- Add automatic Streamlit data refresh every 5 minutes, plus a smoother near-real-time update experience.


