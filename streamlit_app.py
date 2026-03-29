import os

import altair as alt
import pandas as pd
import psycopg2
import streamlit as st


st.set_page_config(page_title="GPW20 Viewer", page_icon="📈")


def require_env(var_name: str) -> str:
	value = os.getenv(var_name)
	if not value:
		st.error(f"Brak wymaganej zmiennej środowiskowej: {var_name}")
		st.stop()
	return value


def get_db_config() -> dict[str, str | int]:
	return {
		"host": require_env("PGHOST"),
		"user": require_env("PGUSER"),
		"port": int(require_env("PGPORT")),
		"dbname": require_env("PGDATABASE"),
		"password": require_env("PGPASSWORD"),
		"sslmode": os.getenv("PGSSLMODE", "require"),
	}


@st.cache_data(show_spinner=False)
def load_companies() -> pd.DataFrame:
	config = get_db_config()
	query = """
		SELECT ticker, description
		FROM stock_info
		WHERE ticker LIKE '%.WA'
		ORDER BY ticker
	"""
	with psycopg2.connect(**config) as conn:
		return pd.read_sql_query(query, conn)


@st.cache_data(show_spinner=False)
def load_recent_prices(tickers: tuple[str, ...]) -> pd.DataFrame:
	if not tickers:
		return pd.DataFrame(columns=["ticker", "price", "update_at", "percentage_change"])

	config = get_db_config()
	query = """
		SELECT ticker, price, update_at, percentage_change
		FROM stock_prices
		WHERE ticker = ANY(%s)
		  AND update_at >= NOW() - INTERVAL '14 days'
		ORDER BY update_at
	"""
	with psycopg2.connect(**config) as conn:
		df = pd.read_sql_query(query, conn, params=(list(tickers),))

	if df.empty:
		return df

	df["update_at"] = pd.to_datetime(df["update_at"], utc=True)
	return df


st.title("GPW20 Viewer")

companies_df = load_companies()
if companies_df.empty:
	st.warning("Nie znaleziono spółek z tickerem kończącym się na .WA w tabeli stock_info.")
	st.stop()

ticker_list = tuple(companies_df["ticker"].tolist())
prices_df = load_recent_prices(ticker_list)
if prices_df.empty:
	st.warning("Brak danych w stock_prices z ostatnich 14 dni dla pobranych tickerów.")
	st.stop()

label_to_ticker: dict[str, str] = {}
labels: list[str] = []
for row in companies_df.itertuples(index=False):
	description = (row.description or "").strip()
	label = f"{description} ({row.ticker})" if description else row.ticker
	label_to_ticker[label] = row.ticker
	labels.append(label)

default_selection = labels[: min(3, len(labels))]
selected_labels = st.multiselect("Choose companies", options=labels, default=default_selection)
metric = st.radio("Metric", ["Price", "Procent change"], horizontal=True)
scope = st.radio("Scope", ["1d", "7d", "14d"], horizontal=True)

if not selected_labels:
	st.info("Wybierz co najmniej jedną spółkę, aby wyświetlić wykres.")
	st.stop()

selected_tickers = [label_to_ticker[label] for label in selected_labels]
filtered = prices_df[prices_df["ticker"].isin(selected_tickers)].copy()

days_by_scope = {"1d": 1, "7d": 7, "14d": 14}
latest_timestamp = filtered["update_at"].max()
cutoff = latest_timestamp - pd.Timedelta(days=days_by_scope[scope])
filtered = filtered[filtered["update_at"] >= cutoff]

value_column = "price" if metric == "Price" else "percentage_change"
value_title = "Price" if metric == "Price" else "Procent change"

if scope in {"7d", "14d"}:
	chart_df = (
		filtered.sort_values("update_at")
		.assign(x_time=lambda df: df["update_at"].dt.floor("D"))
		.groupby(["ticker", "x_time"], as_index=False)[value_column]
		.last()
	)
	x_axis = alt.Axis(title="Day", format="%d")
else:
	chart_df = filtered[["ticker", "update_at", value_column]].rename(columns={"update_at": "x_time"})
	x_axis = alt.Axis(title="Czas", format="%H:%M")

if chart_df.empty:
	st.info("Brak danych do narysowania wykresu dla wybranego zakresu.")
else:
	chart = (
		alt.Chart(chart_df)
		.mark_line()
		.encode(
			x=alt.X("x_time:T", axis=x_axis),
			y=alt.Y(f"{value_column}:Q", title=value_title),
			color=alt.Color("ticker:N", title="Ticker"),
			tooltip=[
				alt.Tooltip("ticker:N", title="Ticker"),
				alt.Tooltip("x_time:T", title="Data"),
				alt.Tooltip(f"{value_column}:Q", title=value_title),
			],
		)
	)
	st.altair_chart(chart, use_container_width=True)
