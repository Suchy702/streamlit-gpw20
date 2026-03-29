# GPW20 minimal viewer

Web application to monitor the top 20 Polish stock market companies, featuring an end-to-end data pipeline built with Apache Airflow, yfinance, pandas, Azure PostgreSQL, and an interactive Streamlit dashboard.

https://gpw20viewer.streamlit.app/

<img width="1985" height="1601" alt="image" src="https://github.com/user-attachments/assets/c60cc7b3-00c1-4b5d-9eab-8be67d528686" />



## Lokalnie

1. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

2. Uruchom aplikację:

```bash
streamlit run streamlit_app.py
```

## Streamlit Community Cloud

1. Wypchnij repozytorium na GitHub.
2. W Streamlit Community Cloud wybierz to repozytorium.
3. Jako Main file path ustaw `streamlit_app.py`.
4. Deploy.
