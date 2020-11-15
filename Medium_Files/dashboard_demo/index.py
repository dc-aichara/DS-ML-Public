from app import app
from app import server
import flask
import json
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
from data import get_coin_data, get_coin_price
from users import users_info

coin_list = ["bitcoin", "ethereum", "ripple", "bitcoin-cash"]

colors = {"background": "white", "background2": "#D0D3D4", "text": "#263a90"}
tabs_styles = {"height": "51px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "2px",
    "fontWeight": "bold",
    "vertical-align": "middle",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "white",
    "color": "blue",
    "padding": "5px",
    "font-size": 15,
}

y_axis = {
    "title": "Price",
    "showspikes": True,
    "spikedash": "dot",
    "spikemode": "across",
    "spikesnap": "cursor",
}

x_axis = {
    "title": "Time",
    "showspikes": True,
    "spikedash": "dot",
    "spikemode": "across",
    "spikesnap": "cursor",
}

user_pwd, user_names = users_info()

_app_route = "/"


# Create a login route
@app.server.route("/login", methods=["POST"])
def route_login():
    data = flask.request.form
    username = data.get("username")
    password = data.get("password")

    if username not in user_pwd.keys() or user_pwd[username] != password:
        return flask.redirect("/login")
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)

        # Here we just store the given username in a cookie.
        # Actual session cookies should be signed or use a JWT token.
        rep.set_cookie("custom-auth-session", username)
        return rep


# Simple dash component login form.
login_form = html.Div(
    [
        html.Form(
            [
                dcc.Input(placeholder="username", name="username", type="text"),
                dcc.Input(placeholder="password", name="password",
                          type="password"),
                html.Button("Login", type="submit"),
            ],
            action="/login",
            method="post",
        )
    ]
)


# create a logout route
@app.server.route("/logout", methods=["POST"])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect("/login")
    rep.set_cookie("custom-auth-session", "", expires=0)
    return rep


app.layout = html.Div(
    [
        html.H1(
            "Cryptocurrency Indicators Dashboard",
            style={"textAlign": "center",
                   "color": "white",
                   # "background": "yellow"
                   },
        ),
        html.Div(id="custom-auth-frame"),  # Input for buttons
        html.Div(
            className="auth",
            id="custom-auth-frame-1",  # Output after Login or Logout
            # style={"textAlign": "right",
            #        "background": "black",
            #        },
        ),
        html.Div(
            [
                "Date selector for graphs",
                dcc.DatePickerRange(
                    id="date-input",
                    stay_open_on_select=False,
                    min_date_allowed=datetime(2013, 4, 28),
                    max_date_allowed=datetime.now(),
                    initial_visible_month=datetime.now(),
                    start_date=datetime(2019, 1, 1),
                    end_date=datetime.now(),
                    number_of_months_shown=2,
                    month_format="MMMM,YYYY",
                    display_format="YYYY-MM-DD",
                    style={
                        "color": "#11ff3b",
                        "font-size": "18px",
                        "margin": 0,
                        "padding": "8px",
                        "background": "yellow",
                    },
                ),
                "Select coin here",
                dcc.Dropdown(
                    id="dropdown",
                    options=[{"label": i, "value": i} for i in coin_list],
                    value="bitcoin",
                    optionHeight=10,
                    style={
                        "height": "50px",
                        "font-weight": 100,
                        "font-size": "16px",
                        "line-height": "10px",
                        "textAlign": "center",
                        "color": "gray",
                        "margin": 0,
                        "padding": "8px",
                        "background": "yellow",
                        "position": "middle",
                        "display": "inline-block",
                        "width": "150px",
                        "vertical-align": "middle",
                    },
                ),
                "Price: $",
                html.Div(id="led-display", style={"display": "inline-block"}),
                html.Div(id="date-output"),
                html.Div(id="intermediate-value", style={"display": "none"}),
            ],
            className="selectors",
            style={
                "marginTop": 0,
                "marginBottom": 0,
                "font-size": 30,
                "color": "white",
                "display": "inline-block",
            },
        ),
        dcc.Tabs(
            id="all-tabs-inline",
            className="all-tabs-inline",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="Simple Moving Average",
                    value="tab-1",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Volatility Index",
                    value="tab-2",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Relative Strength Index",
                    value="tab-3",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Moving Average Divergence Convergence",
                    value="tab-4",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Exponential Moving Average",
                    value="tab-5",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Bollinger Bands",
                    value="tab-6",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
            ],
            style=tabs_styles,
            colors={"border": "yellow", "primary": "red",
                    "background": "orange", },
        ),
        html.Div(id="graph-output", className="graph-display"),
        html.Div(
            children=[
                html.H1(
                    children="Data Table",  # html for table
                    style={"textAlign": "center", "background": "yellow"},
                )
            ]
        ),
        html.Div(className="data-table",
            children=[html.Table(id="table"), html.Div(id="table-output")]),
        html.Div(
            children=[
                dcc.Markdown(  # markdown
                    " © 2019 [DCAICHARA](https://github.com/dc-aichara)  All Rights Reserved."
                )
            ],
            style={"textAlign": "center", "background": "yellow"},
        ),
    ],
    style={"background": "#000080"},
)


@app.callback(Output("led-display", "children"), [Input("dropdown", "value")])
def display_price(coin):
    price = get_coin_price(coin)
    return daq.LEDDisplay(
        label={
            "label": "",
            "style": {
                "font-size": "14px",
                "color": "green",
                "font-family": "sans-serif",
                "background": "black",
                "padding": "2px",
            },
        },
        labelPosition="left",
        value=str(price),
        backgroundColor="black",
        size=18,
        # family='sans-serif',
        style={"display": "inline-block", },
    )


def get_data_table(df):
    df["date"] = pd.to_datetime(df["date"])
    data_table = dash_table.DataTable(
        id="datatable-data",
        data=df.to_dict("records"),
        columns=[{"id": c, "name": c} for c in df.columns],
        style_table={"overflowY": "scroll"},
        fixed_rows={"headers": True, "data": 10},
        style_cell={"width": "100px"},
        style_header={"backgroundColor": "rgb(230, 230, 230)",
                      "fontWeight": "bold", },
    )
    return data_table


@app.callback(Output("intermediate-value", "children"),
              [Input("dropdown", "value")])
def get_data(option):
    df = get_coin_data(crypto=option, save_data=None)
    return df.to_json(date_format="iso", orient="split")


@app.callback(
    [
        Output("graph-output", "children"),
        Output("table-output", "children"),
        Output("custom-auth-frame-1", "children"),
    ],
    [
        Input("intermediate-value", "children"),
        Input("all-tabs-inline", "value"),
        Input("date-input", "start_date"),
        Input("date-input", "end_date"),
    ],
)
def render_content(data, tab, start_date, end_date):
    session_cookie = flask.request.cookies.get("custom-auth-session")

    if not session_cookie:
        # If there's no cookie we need to login.
        return [
            html.Div(
                html.H2(
                    "Charts will be displayed here after user's authentication."),
                style={"textAlign": "center", "color": "red"},
            ),
            "",
            login_form,
        ]
    else:
        df = pd.read_json(data, orient="split")
        data_table = get_data_table(df)
        df = df[(df.date >= start_date) & (df.date <= end_date)]
        logout_output = html.Div(
            children=[
                html.Div(
                    html.H3("Hello {} !".format(user_names[session_cookie])),
                    style={"display": "inline-block"},
                ),
                html.Div(
                    dcc.LogoutButton(logout_url="/logout"),
                    style={"display": "inline-block"},
                ),
            ],
            style={"color": "green", "height": "50px"},
        )
        graph_output = ""

        if tab == "tab-1":
            graph_output = html.Div(
                [
                    html.H3(
                        dcc.Graph(
                            id="SMA",
                            figure={
                                "data": [
                                    {
                                        "x": df["date"],
                                        "y": df["price"],
                                        "type": "line",
                                        "name": "Price",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["SMA"],
                                        "type": "line",
                                        "name": "SMA",
                                        "secondary_y": True,
                                    },
                                ],
                                "layout": {
                                    "title": "Simple Moving Average",
                                    "height": 700,
                                    "xaxis": x_axis,
                                    "yaxis": y_axis,
                                    "plot_bgcolor": colors["background2"],
                                    "paper_bgcolor": colors["background"],
                                    "font": {"color": colors["text"],
                                             "size": 18, },
                                },
                            },
                        )
                    )
                ]
            )
        elif tab == "tab-2":
            graph_output = html.Div(
                [
                    html.H3(
                        dcc.Graph(
                            id="BVOL",
                            figure={
                                "data": [
                                    {
                                        "x": df["date"],
                                        "y": df["price"],
                                        "type": "line",
                                        "name": "Price",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["BVOL_Index"],
                                        "type": "line",
                                        "name": "VOL Index",
                                        "yaxis": "y2",
                                    },
                                ],
                                "layout": {
                                    "title": "Volatility Index",
                                    "height": 700,
                                    "plot_bgcolor": colors["background2"],
                                    "paper_bgcolor": colors["background"],
                                    "font": {"color": colors["text"],
                                             "size": 18, },
                                    "legend": {"x": 1.04, "y": 1.04},
                                    "xaxis": x_axis,
                                    "yaxis": y_axis,
                                    "yaxis2": {
                                        "title": "Volatility Index",
                                        "titlefont": {"color": "orange"},
                                        "tickfont": {"color": "orange"},
                                        "overlaying": "y",
                                        "side": "right",
                                        "showspikes": True,
                                        "spikedash": "dot",
                                        "spikemode": "across",
                                        "spikesnap": "cursor",
                                    },
                                },
                            },
                        )
                    ),
                ]
            )
        elif tab == "tab-3":
            graph_output = html.Div(
                [
                    html.H3(
                        dcc.Graph(
                            id="RSI",
                            figure={
                                "data": [
                                    {
                                        "x": df["date"],
                                        "y": df["price"],
                                        "type": "line",
                                        "name": "Price",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["RSI"],
                                        "type": "line",
                                        "name": "RSI",
                                        "yaxis": "y2",
                                    },
                                ],
                                "layout": {
                                    "title": "Relative Strength Index",
                                    "height": 700,
                                    "plot_bgcolor": colors["background2"],
                                    "paper_bgcolor": colors["background"],
                                    "font": {"color": colors["text"],
                                             "size": 18, },
                                    "legend": {"x": 1.04, "y": 1.04},
                                    "xaxis": x_axis,
                                    "yaxis": y_axis,
                                    "yaxis2": {
                                        "title": "Relative Strength Index",
                                        "titlefont": {"color": "orange"},
                                        "tickfont": {"color": "orange"},
                                        "overlaying": "y",
                                        "side": "right",
                                        "showspikes": True,
                                        "spikedash": "dot",
                                        "spikemode": "across",
                                        "spikesnap": "cursor",
                                    },
                                },
                            },
                        )
                    ),
                ]
            )
        elif tab == "tab-4":
            graph_output = html.Div(
                [
                    html.H3(
                        dcc.Graph(
                            id="MACD",
                            figure={
                                "data": [
                                    {
                                        "x": df["date"],
                                        "y": df["price"],
                                        "type": "line",
                                        "name": "Price",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["MACD"],
                                        "type": "line",
                                        "name": "MACD",
                                        "yaxis": "y2",
                                    },
                                ],
                                "layout": {
                                    "title": "Moving Average Divergence Convergence",
                                    "height": 700,
                                    "plot_bgcolor": colors["background2"],
                                    "paper_bgcolor": colors["background"],
                                    "font": {"color": colors["text"],
                                             "size": 18, },
                                    "legend": {"x": 1.04, "y": 1.04},
                                    "xaxis": x_axis,
                                    "yaxis": y_axis,
                                    "yaxis2": {
                                        "title": "Moving Average Divergence Convergence",
                                        "titlefont": {"color": "orange"},
                                        "tickfont": {"color": "orange"},
                                        "overlaying": "y",
                                        "side": "right",
                                        "showspikes": True,
                                        "spikedash": "dot",
                                        "spikemode": "across",
                                        "spikesnap": "cursor",
                                    },
                                },
                            },
                        )
                    ),
                ]
            )
        elif tab == "tab-5":
            graph_output = html.Div(
                [
                    html.H3(
                        dcc.Graph(
                            id="EMA",
                            figure={
                                "data": [
                                    {
                                        "x": df["date"],
                                        "y": df["price"],
                                        "type": "line",
                                        "name": "Price",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["EMA_20"],
                                        "type": "line",
                                        "name": "EMA-20",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["EMA_50"],
                                        "type": "line",
                                        "name": "EMA-50",
                                    },
                                ],
                                "layout": {
                                    "title": "Exponential Moving Average",
                                    "height": 700,
                                    "xaxis": x_axis,
                                    "yaxis": y_axis,
                                    "plot_bgcolor": colors["background2"],
                                    "paper_bgcolor": colors["background"],
                                    "font": {"color": colors["text"],
                                             "size": 18, },
                                },
                            },
                        )
                    ),
                ]
            )
        elif tab == "tab-6":
            graph_output = html.Div(
                [
                    html.H3(
                        dcc.Graph(
                            id="SMA",
                            figure={
                                "data": [
                                    {
                                        "x": df["date"],
                                        "y": df["price"],
                                        "type": "line",
                                        "name": "Price",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["BB_upper"],
                                        "type": "line",
                                        "name": "Upper BB",
                                    },
                                    {
                                        "x": df["date"],
                                        "y": df["BB_lower"],
                                        "type": "line",
                                        "name": "Upper BB",
                                    },
                                ],
                                "layout": {
                                    "title": "Bollinger Bands",
                                    "height": 700,
                                    "xaxis": x_axis,
                                    "yaxis": y_axis,
                                    "plot_bgcolor": colors["background2"],
                                    "paper_bgcolor": colors["background"],
                                    "font": {"color": colors["text"],
                                             "size": 18, },
                                },
                            },
                        )
                    ),
                ]
            )
        return [graph_output, data_table, logout_output]


if __name__ == "__main__":
    app.run_server(debug=True)
