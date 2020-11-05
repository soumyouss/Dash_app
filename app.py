import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
import pandas as pd

from appFiles.value_boxes import value_boxes_row
from appFiles.basic_boxes import basic_boxes_row

df = pd.read_csv("https://raw.githubusercontent.com/ulklc/covid19-timeseries/master/countryReport/raw/rawReport.csv")
df["day"] = pd.to_datetime(df["day"],format="%Y/%m/%d")
all_country = df.countryName.unique()

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
                id='country-name',
                options=[{'label': i, 'value': i} for i in all_country],
                value='Ivory Coast'
                #multi=True
            ),
        html.Br(),
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='Y-MM-DD',
        min_date_allowed=min(df["day"]),
        max_date_allowed=max(df["day"]),
        initial_visible_month=min(df["day"]),
        end_date=max(df["day"])
    ),  

        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{'label': i, 'value': i} for i in ['barplot', 'lineplot']],
            value='barplot',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Prédiction', style={
            'textAlign': 'center'
        })
        ,
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

# content_first_row = dbc.Row([
#     dbc.Col(
#         dbc.Card(
#             [

#                 dbc.CardBody(
#                     [
#                         html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
#                                 style=CARD_TEXT_STYLE),
#                         html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
#                     ]
#                 )
#             ]
#         ),
#         md=3
#     ),
#     dbc.Col(
#         dbc.Card(
#             [

#                 dbc.CardBody(
#                     [
#                         html.H4('Card Title 2', className='card-title', style=CARD_TEXT_STYLE),
#                         html.P('Sample text.', style=CARD_TEXT_STYLE),
#                     ]
#                 ),
#             ]

#         ),
#         md=3
#     ),
#     dbc.Col(
#         dbc.Card(
#             [
#                 dbc.CardBody(
#                     [
#                         html.H4('Card Title 3', className='card-title', style=CARD_TEXT_STYLE),
#                         html.P('Sample text.', style=CARD_TEXT_STYLE),
#                     ]
#                 ),
#             ]

#         ),
#         md=3
#     ),
#     dbc.Col(
#         dbc.Card(
#             [
#                 dbc.CardBody(
#                     [
#                         html.H4('Card Title 4', className='card-title', style=CARD_TEXT_STYLE),
#                         html.P('Sample text.', style=CARD_TEXT_STYLE),
#                     ]
#                 ),
#             ]
#         ),
#         md=3
#     )
# ])


content = html.Div(
    [
        html.H2('Premier Dashboard avec Dash', style=TEXT_STYLE),
        html.Hr(),
        value_boxes_row,
        basic_boxes_row
        #content_third_row,
        #content_fourth_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


@app.callback(
    Output('graph1', 'figure'),
    [
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     #Input('country-name', 'name_country'),
     Input('radio_items', 'value')])
def update_graph(start_date, end_date, type_plot):
    
    dff = df[(df["day"]>=start_date) & (df["day"]<=end_date)]
    #df1 = dff[dff["countryName"]==name_country]
    dff = dff.groupby(["day"])["confirmed","recovered","death"].sum().reset_index()

    if type_plot == "barplot":
        fig = px.bar(dff, x="day", y=["confirmed","recovered","death"])
    else:
        fig = px.line(dff, x="day", y=["confirmed","recovered","death"])
 
    return fig

@app.callback(
    Output('map', 'figure'),
    Input('radio_items', 'value')
    )
def map_graph(n_map):
    #dd = px.data.gapminder().query('year==2007')
    fig = px.scatter_geo(df, color='region',lat=df.lat,lon=df.lon,
                         hover_name='countryName', size='confirmed')

    fig.update_layout({
        'height': 600
    })
    return fig

@app.callback(
    Output('graph_2', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    fig = {
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 4, 5],
            'type': 'bar'
        }]
    }
    return fig


@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    df = px.data.iris()
    fig = px.density_contour(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.gapminder().query('year==2007')
    fig = px.scatter_geo(df, locations='iso_alpha', color='continent',
                         hover_name='country', size='pop', projection='natural earth')
    fig.update_layout({
        'height': 600
    })
    return fig


@app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.iris()
    fig = px.scatter(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.tips()
    fig = px.bar(df, x='total_bill', y='day', orientation='h')
    return fig


@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card Tile 1 change by call back'


@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    return 'Card text change by call back'


if __name__ == '__main__':
    app.run_server(port='8085')