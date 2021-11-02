import dash_bootstrap_components as dbc
from dash import dash, dcc, html, Input, Output, State
from datetime import date
import common

app = dash.Dash(title="Frimplestatic Trader",
                external_stylesheets=[dbc.themes.LUX])


def getCharts(tickers):
    end = date.today().strftime('%m-%d-%Y')

    start = common.getEndDate("m", 36)

    charts = []

    if(tickers == ""):
        tickers = "AAPL;PETR3.SA"

    stocks = tickers.split(sep=";")

    for stock in stocks:
        try:
            if(stock != ""):
                fig = common.getFigure(stock, start, end)
                charts.append(dbc.Row(
                    [
                        html.H2(stock),
                        dcc.Graph(id=f"{stock}", figure=fig)
                    ]
                ))

        except Exception as exc:
            charts.append(
                dbc.Alert(f"Couldn't find historical for {stock}", color="primary"))

    return charts


def loadApp():

    colors = {
        'background': '#111111',
        'text': '#FFFFFF'
    }

    app.layout = dbc.Container(
        html.Div([
            html.Div(
                [
                    html.H1("Frimplestatic Trader (Free, Simple and Static)"),
                    dbc.Row(
                        [
                            dbc.Col(children=[

                                dbc.Input(
                                    autocomplete="off", id='my-input', placeholder='Search Tickers', size="md", type='text', value=""),
                                dbc.Button("Load Charts",
                                           id='button_id', className="mt-3")

                            ]
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dcc.Loading(
                                id="loading-1",
                                fullscreen=False,
                                type="cube",
                                children=html.Div(id="graphics_div")
                            )],
                        className="mt-3"
                    )
                ],
                id='main_div',


            )]), fluid=True
    )

    @app.callback(
        Output(component_id='graphics_div', component_property='children'),
        Input('button_id', 'n_clicks'),
        State('my-input', 'value')

    )
    def callback_function(nclicks, value):
        tickers = value.replace("\r\n", "")
        tickers = tickers.replace("\n", "")
        tickers = tickers.replace(" ", "")
        tickers = tickers.replace("\s", "")

        return getCharts(tickers)


def runApp():
    loadApp()


if __name__ == '__main__':
    runApp()
    app.run_server(debug=True)
