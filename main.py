import ParseTrade
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

start_time = time.time()
#filename = "03272019.NASDAQ_ITCH50.gz"
filename = "01302019.NASDAQ_ITCH50.gz"
parser = PARSER()
parser.ProcessMessage(filename)
dict_vwap = parser.VWAP()
print(dict_vwap['AAPL'])
elapsed_time = time.time() - start_time
print(elapsed_time)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.Div([html.Label('Volume Weighted Average Price '),
              html.H6('filename: {}'.format(filename)),
    #Hr() is a horizontal line
    html.Hr()],style={'color':'#045FB4','fontSize' : '30px'}),

    html.Div(className = 'Selections',children=[

        html.Label('Tickers'),
        dcc.Dropdown(
            id = 'Tickers',
            options=[{'label': i, 'value' : i} for i in parser.tickers],
            value='AAPL'
            )]),
    html.Div(id='Graph'),

            ],style={'width':'39%', 'display': 'inline-block'}
            )

@app.callback(
    Output(component_id ='Graph', component_property='children'),
    [Input(component_id='Tickers',component_property='value')]
)
def update(ticker):
    return html.Div([
                html.Div([
                    dash_table.DataTable(
                        data=dict_vwap[ticker].to_dict('records'),
                        columns=[{"name": i, "id": i} for i in dict_vwap[ticker].columns]
                    ),],className='col-md-5'),
                    html.Div([
                    dcc.Graph(id='VWAPGraph',
                                 figure={
                                    'data':[
                                            go.Scatter(
                                                        x = parser.times,
                                                        y = dict_vwap[ticker]['VWAP'],
                                                        mode = 'lines+markers',
                                                        name = 'VWAP from NASDAQ_ITCH50')
                                                ],
                                     'layout': go.Layout(yaxis=go.layout.YAxis(title='VWAP'),
                                    xaxis=go.layout.XAxis(title='Time'))
                                 })
                    ],className='col-md-7')
                    ],className='row')


if __name__ == '__main__':
    app.run_server(debug=True)
