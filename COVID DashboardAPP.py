import pandas as pd
import requests
from datetime import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Fetch data and preprocess
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
data = pd.read_csv(url)
data["date"] = pd.to_datetime(data["date"])

# Filter the data
pop_threshold = 100_000  # Define a population threshold
filtered_data = data[data["population"] > pop_threshold].copy()
filtered_data["deaths_per_capita"] = filtered_data["new_deaths"] / \
    filtered_data["population"]

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container(
    [
        html.H1("COVID-19 Deaths Per Capita Per Day"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": country, "value": country}
                     for country in filtered_data["location"].unique()],
            multi=True,
            value=["United States", "India", "China"],
            style={"margin-bottom": "20px"},
        ),
        dcc.Graph(id="deaths-per-capita"),
    ],
    fluid=True,
)

# Define app callback


@app.callback(
    Output("deaths-per-capita", "figure"),
    Input("country-dropdown", "value"),
)
def update_chart(selected_countries):
    filtered_df = filtered_data[filtered_data["location"].isin(
        selected_countries)]

    fig = px.line(
        filtered_df,
        x="date",
        y="deaths_per_capita",
        color="location",
        labels={"location": "Country", "date": "Date",
                "deaths_per_capita": "Deaths per Capita per Day"},
        title="COVID-19 Deaths per Capita per Day for Selected Countries",
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
