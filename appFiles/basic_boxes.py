import dash_html_components as html
import dash_core_components as dcc
import dash_admin_components as dac
import dash_bootstrap_components as dbc
import plotly.express as px


basic_boxes_row = html.Div(
        [ 
            html.Div([
                dac.SimpleBox(
                style = {'height': "600px", 'width': '70vw'},
                title = "Evolution COVID-19",
                children=[
                    dcc.Graph(
                        id='graph1',
                        config=dict(displayModeBar=False)
                        #style={'width': '100vw'}
                    )
                ]
            ),
                ],className="row"),
            html.Div([
                    dbc.Row(
    
        dbc.Col(
            dcc.Graph(id='map'), md=12
        )
    
)
                ])

        
])