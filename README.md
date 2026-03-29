# GPW20 minimal viewer

Web application to monitor the top 20 Polish stock market companies, featuring an end-to-end data pipeline built with Apache Airflow, yfinance, pandas, Azure PostgreSQL, and an interactive Streamlit dashboard.

https://gpw20viewer.streamlit.app/

<img width="1985" height="1601" alt="image" src="https://github.com/user-attachments/assets/c60cc7b3-00c1-4b5d-9eab-8be67d528686" />



## Local hosting
```bash
./main up # run Streamlit app locally
```

```bash
./main down # stop Streamlit app
```

## Architecture
1. **Data Collection**: Apache Airflow orchestrates the data pipeline, scheduling regular data collection from yfinance.
2. **Data Storage**: Collected data is stored in an Azure PostgreSQL database.
3. **Data Visualization**: A Streamlit application retrieves data from the database and provides an interactive dashboard for users to monitor stock performance.

<p align="center">
	<img src="gpw20Viewer.drawio.svg" alt="Architecture diagram" width="900" />
</p>


## How it was made

# PostgreSQL on Azure
