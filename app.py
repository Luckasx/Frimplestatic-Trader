import dash_bootstrap_components as dbc
from dash import dash, dcc, html, Input, Output, State, MATCH
from datetime import date
import common
import webbrowser

app = dash.Dash(title="Frimplestatic Trader",
                external_stylesheets=[dbc.themes.LUX])

def getLinks(stock):
    links = []
    stock_original = stock.lower().replace(".sa","")
    
    ##google
    links.append(            
                dcc.Link(html.Img(src="https://www.google.com/favicon.ico", width="24"), 
                target="_blank" , 
                href=f"https://www.google.com/search?q={stock_original}" , 
                className="ms-3")            
        )

    if(stock.lower().find(".sa") > -1):
        ###suno
        links.append(             
                 dcc.Link(html.Img(src="https://www.suno.com.br/acoes/img/favicon.ico", width="24"), 
                 href=f"https://www.suno.com.br/acoes/{stock_original}/", 
                 target="_blank", 
                 title="SUNO", 
                 id=f"suno_{stock_original}" , 
                 className="ms-3"))        
        links.append(             
                 dcc.Link(html.Img(src="https://statusinvest.com.br/img/favicon/favicon-32x32.png", width="24"), 
                 href=f"https://statusinvest.com.br/acoes/{stock_original}/", 
                 target="_blank", 
                 title="Status Invest", 
                 id=f"status_{stock_original}" , 
                 className="ms-3"))
             

    row = dbc.Row(
        [
            *links
        ], className = "mb-3 input-group"
    )
    return links

def buildChart(stock, start, end):
    fig, data = common.getFigure(stock, start, end)
    links = getLinks(stock)
    return (dbc.Row(
        [
            
            dbc.Col(
                children=[
                    dbc.Card(
                        [
                            dbc.CardBody(

                            children=[
                                    html.H2(stock),                                 
                                    *links
                                    
                            ]
                            )
                        ]
                    )                                
                ], width=12
            ),
            
            dbc.Col(children=[
                dcc.Graph(id={'type':"chart-candle", 'index':f"{stock}"}, figure=fig)
            ], width=12
            )
            
        ], class_name="mt-3"
    ))

def getCharts(tickers):    

    end = date.today().strftime('%m-%d-%Y')

    start = common.getEndDate("m", 36)

    charts = []

    if(tickers == ""):
        tickers = "ABEV3.SA;egie3.sa;flry3.sa;tupy3.sa;wege3.sa"        
        # tickers = "ABEV3.sa"

    stocks = tickers.split(sep=";")

    for stock in stocks:
        try:
            if(stock != ""):
                c = buildChart(stock, start, end)
                charts.append(c)

        except Exception as exc:
            charts.append(
                dbc.Alert(f"Couldn't find historical for {stock} " , color="primary"))
            

    return charts

def clearValue():
    return ""

def loadApp():

    colors = {
        'background': '#111111',
        'text': '#FFFFFF'
    }

    app.layout = dbc.Container(
        html.Div([
            html.Div(
                [
                    html.H1("Frimplestatic Trader (Free, Simple and Static)",className="mt-3 text-center"),                 
                    dbc.Row(
                        [
                            dbc.Col(children=[
                                html.Div(
                                children=[dbc.Input(
                                    autocomplete="off", id='my-input', 
                                    placeholder='Search Tickers', 
                                    size="md", 
                                    type='text', 
                                    value="",
                                    className="form-control"
                                    ),
                                html.Div(    
                                children=[dbc.Button("Load Charts",
                                           id='button_id', className="")
                                ], className="input-group-append"
                                )
                                

                            ], className="input-group"
                            )
                        ], width={"size":6, "offset":"3"}
                    )], className="mt-2"),
                    dbc.Row(
                        [
                            dcc.Loading(
                                color="orange",
                                id="loading-1",
                                fullscreen=False,

                                type="cube",
                                children=html.Div(id="graphics_div"),
                                style={                                    
                                    "position":"absolute",
                                    "top":"20px"
                                }
                            )],
                        className="mt-3"
                    ),
                    dbc.Row
                    (
                        dcc.Link(
                            [
                                dbc.Button("back to the top", size="lg", className="me-1")
                            ], href="#my-input", className="mt-3"
                        )
                    )
                ],
                id='main_div',


            )]), fluid=True
    )

    @app.callback(
        [
            Output(component_id='graphics_div', component_property='children'),
            Output('my-input', "value")
        ],
        Input('button_id', 'n_clicks'),
        State('my-input', 'value')

    )
    def callback_function(nclicks, value):
        tickers = value.replace("\r\n", "")
        tickers = tickers.replace("\n", "")
        tickers = tickers.replace(" ", "")
        tickers = tickers.replace("\s", "")

        charts = getCharts(tickers)

        return charts , ""


    # @app.callback(
    #     Output({'type':'chart_data', 'index': MATCH}, "children"),
    #     [Input({'type':'chart-candle', 'index':MATCH}, 'hoverData')],
    #      State({'type': 'chart-candle', 'index': MATCH}, 'id'),
    #     )
    # def update_y_timeseries(hoverData, id):
    #     stock = (id.get("index"))

    #     print(hoverData)
        
    #     data = hoverData["points"]
        
    #     try:
    #         data = common.filterData(data, 'curveNumber', 0)

    #         cardBody = [ dbc.Badge("Open", className="ms-1"), 
    #                 html.Label(data["open"]),
    #                 dbc.Badge("Close", className="ms-1"),
    #                 html.Label(data["close"]),
    #                 dbc.Badge("Low", className="ms-1"), 
    #                 html.Label(data["low"]),
    #                 dbc.Badge("High", className="ms-1"),
    #                 html.Label(data["high"]),
    #                 dbc.Badge("Date", className="ms-1"), 
    #                 # html.Label(data["date"])
    #     ]
    #     except Exception as err:
    #         print(err)

        

        

    #     print(cardBody)

    #     return cardBody


def runApp():
    loadApp()


if __name__ == '__main__':
    # webbrowser.open("http://localhost:8050")
    runApp()
    app.run_server(debug=True)
    
