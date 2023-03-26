# sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE

# plots & dash
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

# other
import pandas as pd
import numpy as np
import json
import nltk
from datetime import datetime as dt
from textwrap import dedent as d

# custom
import tsne_controller
import functions
import data_controller

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dataset_controller = data_controller.dataset()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Skipta appi upp í tabs
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-2', children=[
        dcc.Tab(label='Data', value='tab-2', children=[
            # Selection of datasets {Whole (slow), Post 2018, Example (Different), Example (Similar)}
            html.Div(style={"border": "1px grey solid", 'padding': '10px 10px', 'margin': '10px', 'width': '90%'},
                     children=[
                dcc.Markdown('''
                    # Select a dataset
                    '''),
                dcc.Dropdown(
                    options=[
                        {'label': 'All patents after 1-1-2018',
                            'value': 'subset_post_2018.csv'},
                        {'label': 'Example subset (Similar)',
                         'value': 'subset_similar.csv'},
                        {'label': 'Example subset (different)',
                         'value': 'subset_different.csv'}
                    ],
                    value='subset_different.csv',
                    id='dropdown-datasets',
                    style={'width': '90%%'}
                ),

                html.Div(id='div-size-super'),
            ]),
            html.Div(style={"border": "1px grey solid", 'padding': '10px 10px', 'margin': '10px', 'width': '90%'},
                     children=[


                # Summary statistics

                # 'Size of dataset: X'
                dcc.Markdown('#### Customize your dataset:'),
                dcc.Markdown('###### Add search term:'),
                html.Label('Enter search string here'),
                dcc.Input(
                    id='search-term-box',
                    placeholder='Enter your search term',
                    type='text',
                    value=''),

                html.Button('Add search term', id='button-add-search-term'),

                dcc.Markdown('###### Search terms:'),
                dcc.Dropdown(
                    options=functions.list_to_options(dataset_controller.get_search_terms()),
                    multi=True,
                    value=dataset_controller.get_search_terms(),
                    style={
                        'width': '90%'
                    },
                    id='my-searchterms'
                ),
                html.Button('Make subset with search terms',
                            id='button-make-subset',style={'width':'90%'}),
                # 'Size of subset: X'
                html.Div(id='div-size-sub'),
            ])

            # Create subset with search terms

            # Show statistics about set


        ]),
        dcc.Tab(label='Controls', value='tab-1', children=[
            # Controls
            html.Div(style={"border": "1px grey solid", 'padding': '10px 10px', 'margin': '10px','width':'90%' },
                     children=[
                        html.Label('Enter new label here'),
                        dcc.Input(
                            id='input-box',
                            placeholder='Enter your label string',
                            type='text',
                            value=''),
                        html.Button('Add keyword', id='button-add-keyword'),
                        dcc.Dropdown(
                                options=functions.list_to_options(dataset_controller.get_search_terms()),
                                multi=True,
                                value=None,
                                style={
                                    'width': 600
                                },
                                id='my-keywords'
                            ),
                        # Date
                        
                        html.Div(children=[
                            html.Label('Pick the period you would like to search'),
                            dcc.DatePickerRange(
                                id='date-picker-range',
                                start_date=dataset_controller.get_start_date(),
                                end_date=dataset_controller.get_end_date())
                            ]
                        )
                    ]),
            # Update button
            html.Button('Update Graph', id='button',style={'margin':'10px'}),
            # graph container
            html.Div(
                style={"border": "1px grey solid",'margin':'10px','width':'90%'},
                children=[
                    

                    dcc.Graph(
                        figure=dict(
                            layout=dict(
                                clickmode='event+select'
                            )
                        ),
                        style={'height': '500px', 'width': '100%'},
                        id='my-graph'
                    ),
                    # Placeholders til að geyma values
                    html.Div(id='df-name', style={'display': 'none'},children='Data/subset_different.csv'),
                    html.Div(id='df-subset-name', style={'display': 'none'},children='Data/subset_different.csv'),


                    
                ]),
                # html.Button('Use selected data', id='use-selected',style={'margin':'10px'}),
                html.Div([
                        dcc.Markdown(d("""
                            **Selection Data**

                            Choose the lasso or rectangle tool in the graph's menu
                            bar and then select points in the graph.

                        """)),
                        html.Pre(id='selected-data', style={'border': 'thin lightgrey solid','overflowX': 'scroll','width': 1200}),
                    ], className='three columns'),

        ]),

        
        dcc.Tab(label='Selected Data', value='tab-3',children=[
            dcc.Graph(
                figure=dict(
                    layout=dict(
                        clickmode='event+select'
                    )
                ),
                style={'height': '500px', 'width': '100%'},
                id='graph-area'
            ),
            html.Div(children=[
                 dash_table.DataTable(
                    id='selected-table',
                    columns=[{"name": i, "id": i} for i in dataset_controller.get_col_names()],
                    data=dataset_controller.get_subset().to_dict('records'),
                    style_cell={'textAlign': 'left','padding': '5px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                    style_data={'whiteSpace': 'normal'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                        }],
                )
            ],style={'width':'90%','padding':'20px'})
            
            

        ])

    ]),
    html.Div(id='tabs-content')
])


# Uppfæra dataset í data controller þegar nýtt datasett er valið af lista
@app.callback(
    [Output('div-size-super', 'children')],
    [Input('dropdown-datasets', 'value')]
)
def update_keyword_list(value):
    dataset_controller.set_df_filename('Data/%s'%(value))
    df_size = dataset_controller.get_df_len()
    print(dataset_controller.get_name())
    return ['Size of dataset: %s'%(df_size)]

# Þegar creation listinn uppfærist, búa til subset með leitarorðum
@app.callback(
    [Output('div-size-sub', 'children')],
    [Input('button-make-subset', 'n_clicks')],
    [State('my-searchterms', 'value'),State('df-name','children')]
)
def update_subset(n_clicks, value, df_name):
    if n_clicks is None:
        raise PreventUpdate
    dataset_controller.clear_search_terms()
    for term in value:
        dataset_controller.add_search_term(term)

    dataset_controller.make_subset_words()
     
    return ['Size of subset:%s' %(dataset_controller.get_df_subset_len())]

# Bæta í creation lista
@app.callback(
    Output('my-searchterms', 'options'),
    [Input('button-add-search-term', 'n_clicks')],
    [State('search-term-box', 'value')]
)
def update_keyword_create_list(n_clicks, searchString):
    if n_clicks is None:
        raise PreventUpdate
    if len(searchString) > 0:
        dataset_controller.add_search_term(searchString)
    sTerms = dataset_controller.get_search_terms()
    options = functions.list_to_options(sTerms)

    return options

# Bæta í selection lista
@app.callback(
    Output('my-keywords', 'options'),
    [Input('button-add-keyword', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_keyword_label_list(n_clicks, labelString):
    if n_clicks is None:
        raise PreventUpdate

    dataset_controller.add_label_terms(labelString)
    lTerms = dataset_controller.get_label_terms()

    return functions.list_to_options(lTerms)


# Uppfæra graf
@app.callback(
    Output('my-graph', 'figure'),
    [Input('button', 'n_clicks')],
    [State('my-keywords', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date'),
     State('df-subset-name', 'children')])
def update_output(n_Clicks, searchStrings, start_date, end_date, df_subset_name):
    if n_Clicks is None:
        raise PreventUpdate
    
    

    print('creating graph for subset: %s'%(dataset_controller.get_name()))

    # set the relevant dates for the dataset
    dataset_controller.set_start_date(start_date)
    dataset_controller.set_end_date(end_date)
    
    # Make the data controller update the dataset with current settings
    
    dataset_controller.make_subset()
    dataset_controller.label_subset()
    labels = dataset_controller.get_labels()

    # Nýta gamla plottable df ef það er með sömu indexes
    # plotable_df = dataset_controller.get_plotable()
    
    plotable_df = tsne_controller.without_PCA(dataset_controller.get_subset())
    
    dataset_controller.set_plotable(plotable_df)

        
    returnable_dict = functions.df_to_plot_dict(plotable_df,labels)

    return returnable_dict

# Þegar gögn eru valin á grafinu, setja þau í json formatti fyrir neðan grafið og á plottið á næsta tab. 
@app.callback(
    [Output('selected-data', 'children'),Output('graph-area','figure'),Output('selected-table','data')],
    [Input('my-graph', 'selectedData')])
def display_selected_data(selectedData):
    if selectedData is None:
        raise PreventUpdate
    dataset_controller.set_selected_df(selectedData) #Potential week spot
    selected = dataset_controller.get_selected_df()
    labels = dataset_controller.get_labels()
    plot_dict = functions.df_to_area_plot_dict(selected,labels)

    return json.dumps(selectedData, indent=2),plot_dict,selected.to_dict('records')

# @app.callback(
#     Output('selected-table','data'),
#     [Input('use-selected','n_clicks')]
# )
# def use_selected_data(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate

#     return dataset_controller.get_selected_df().to_dict('records')
    

if __name__ == '__main__':
    app.run_server(debug=True)
