# GPW20 minimal viewer

Web application to monitor the top 20 Polish stock market companies, featuring an end-to-end data pipeline built with Apache Airflow, yfinance, pandas, Azure PostgreSQL, and an interactive Streamlit dashboard.

https://gpw20viewer.streamlit.app/

<img width="1500" height="1200" alt="image" src="https://github.com/user-attachments/assets/c60cc7b3-00c1-4b5d-9eab-8be67d528686" />



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
	<img src="gpw20Viewer.drawio.svg" alt="Architecture diagram" width="500" />
</p>


## How it was made

### PostgreSQL on Azure
Pierwsza rzecza ktora postanowilem zrobic byla baza danych postgres zahostowanana na Azure. Rodzaj bazy zostal wybrany w celach zapoznania sie z PostgreSQL. Hostowanie bazy na Azure tez bylo podyktowane wzgledami edukacyjnymi, dzieki github student developer pack (tutaj link) mozna testowac Azure przez rok majac do dysopzycji 100$.

Zalezalo mi aby baza byla jak najprostrza w konfiguracji oraz jak najtańsza, dlatego wyborl padl na `Azure Database for PostgreSQL flexible server`


<img width="400" height="505" alt="image" src="https://github.com/user-attachments/assets/5bea9560-9a05-4fc4-a199-6229c393eb15" />

Dzięki wybraniu minimalnej mocy obliczeniowej i pamięci, cena (po przekreoczeniu darmowych limitów) wynosiłaby około 18$ za miesiac

Po udanym skonfigurwoaniu bazy, dodalem do niej pierwsze dane na kotrych mialbym bazowac i przestowalem jej dzialanie
<img width="1200" height="550" alt="image" src="https://github.com/user-attachments/assets/b3492520-de31-4674-9261-b7fdedf0a2bb" />

Baza danych działała bez zarzutów, a konfiugracja jej z innymi miejscami w projekcie (Apache, VScode, Streamlit) była bezproblemowa. 


### Apache Airflow
Do okiestracji zadan wybralem apache airflow aby nauczyc sie tego narzedzia. Pomaga on zarządzać wykonywaniem data pipelinow w odpowiednim czasie i czestotliwoscia, sam sklada sie z DAGow czyli acyklicznych grafow skierowanych. Polega to na tym ze pojedyncze zadania sa wezlami, i kolejne moga uruchomic sie dopiero wtedy, gdy wczesniejsze wykona sie poprawnie. 

Apache airflow dostarcza plik docker compose ktory sluzy do lokalnego uruchamiania poprzez narzedzie docker compose [link]

Uruchomilem lokalnie Apache Airflow oraz stowrzylem niezbede taski w tym projeckie ktore:
- pobieraja liste tickerow i ich ceny z naszej bazy danych
- fetchuja aktualne ceny tickerow z Yahoo Finance (yfinance [dodaj link])
- zapisuja nowe dane do bazy danych liczac przy tym zmiane procentowa ceny

```python
@dag(
    dag_id="postgres_wa_tickers",
    description="Fetches latest stock prices, gets current prices from yfinance, and stores percent changes",
    start_date=datetime(2026, 3, 28),
    schedule="*/5 9-17 * * 1-5" # Every 5 minutes during Polish stock market hours on weekdays
    catchup=False,
    tags=["postgres", "stocks", "wa", "yfinance"],
)
```

Widok z Airflow UI
<img width="1800" height="700" alt="image" src="https://github.com/user-attachments/assets/e7b6fe79-6b7d-490e-9b4d-cd268bf92f8b" />


Airflow to duze narzedzie, wymagajace poczatkowej konfiguracji, jednak jest bardzo wygodne w korzystaniu. W moim przypadku byc moze daloby sie znalezc prostrze nardziedzie robiace procesowanie danych krok po kroku, jednak Airflow zostal wybrany w celach edukacyjnych. UI dostarczone przez tworcow w bardzo wygodny sposob pozwala kontrolowac wyniki/logi pojedynczyc stepow, co jest pomocny przy debugowaniu. Wiadc ze narzedzie stworzone jest dla wielu dagow o zroznicowanym stopniu zlozonosci sadzac po UI.

(Planowane jest zahostowanie Apache na maszynie wirtualnej w Azure, aby moglo dzialac non stop, aktulanie uruchamiane jest tylko lokalnie na mojej maszynie)

### Streamlit
W zwiazku z tym, ze tworzac ten projekt chcialem skupic sie glownie na aspektach zwiazanych z data engineeringiem, wybralem narzedzie pozwalajace na stworzenie frontendu w sposob najprostrzy i najszybszy. Streamlit wpisal sie idealnie w te wymagania, dodatkowo nie potrzebuje on zadnej dodatkowej konfiguracji w celu hostowania, poniewaz mozna uzyc streamlit community cloud. 

Dodalem klucze do bazy danych dbajac o ich prytwatnosc oraz wyhostowalem aplikacje.
<img width="1800" height="210" alt="image" src="https://github.com/user-attachments/assets/73501284-713c-4bcd-8485-5960d56a0216" />

## Planowane dzialania
- Stworzenie repozytorium do Apache Airflow z automatycznym deploy na Azure
- Automatyczny refresh najnowszych danych na Streamlit (co 5 minut), wraz z mechanizmem sprawiajacym złudne wrażenie ciagłej aktualizacji


