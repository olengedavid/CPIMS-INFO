import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Output, Input

data = pd.read_csv("avocado.csv")
data_k = pd.read_csv("kakamega.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CPMIS INFOGRAPHICS!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="CPIMS INFOGRAPHICS", className="header-title"
                ),
                html.P(
                    children="Analyze the reported child cases"
                    " within a given county in a specific county",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.P(children="County"),
                dcc.Dropdown(
                id="dropdown",
                options=[{"label": x, "value": x} for x in data_k["county"].unique()],
                value=""
                ),
            ],
            className="menu-title",
        ),
        
            html.Div([
                html.P("Sub county"),
            dcc.Dropdown(
                id="dropdown2",
                options=[{"label": x, "value": x} for x in data_k["sub_county"].unique()],
                value="",
                className="menu-title",
                clearable=False
            ),

                dcc.Graph(id="pie-chart", className="card"), 
                dcc.Graph(id="bar-chart", className="card"), 
                dcc.Graph(id="bar-chart1", className="card"), 
                dcc.Graph(id="bar-chart2", className ="card"),
                dcc.Graph(id="bar-chart3", className ="card"),
                dcc.Graph(id="scatter-chart", className="card")
              ])
     ]
)


@app.callback(
    [Output("price-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)

@app.callback(
    [Output("bar-chart", "figure"),
     Output("bar-chart1", "figure"), 
     Output("bar-chart2", "figure"),
     Output("pie-chart", "figure"), 
     Output("bar-chart3", "figure"),
     Output("scatter-chart","figure")
    ], 
    [Input("dropdown2", "value")])
def update_bar_chart(day):
    mask = data_k["sub_county"] == day
    fig2 = px.bar(data_k[mask], x="case category", y="age", 
    color="agerange", barmode="group")
    
    fig3 = px.bar(data_k[mask], x="case category", y="case_reporter", 
    color="case_reporter", barmode="group")

    fig4 = px.bar(data_k[mask], x="case category", y="risk_level", 
    color="risk_level", barmode="group")

    fig5 = px.bar(data_k[mask], x="sex", y="age", 
    color="agerange", barmode="group")

    fig = px.pie(data_k[mask], values="age", names="case category")
    
    fig6 = px.scatter(data_k[mask], x= "case category", y= "intervention",
    color = "case category")



    return fig, fig2, fig3, fig4, fig5, fig6

if __name__ == "__main__":
    app.run_server(debug=True)