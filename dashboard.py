# _________Imports_________________
from re import template
from typing import Dict
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Line

import numpy as np
import pandas as pd
import json
# ________________________________________
# MANIPULAR DADOS
# df=pd.read_csv("HIST_PAINEL_COVIDBR_13mai2021.csv",sep=";")
# tirar a coluna de estados sem informacao
#df_states= df[(~df['estado'].isna())& (df['codmun'].isna())]
#df_brasil= df[df['regiao']=='Brasil']
# df_brasil.to_csv('df_brasil.csv')
# df_states.to_csv('df_states.csv')
#________________________________________________
#____________CenterLatitude,Long___________________________________
CENTER_LAT,CENTER_LON = -10.720569,-55.491485
#__________________________________________________________________


# _____________FILTRAR DETERMINADOS DADOS_________________________
df_states = pd.read_csv('df_states.csv')
df_brasil = pd.read_csv('df_brasil.csv')

df_states_ = df_states[df_states["data"] == '2020-05-14']

brazil_states = json.load(open('geojson/brazil_geo.json', 'r'))
brazil_states["features"][0].keys()

df_data = df_states[df_states['estado'] == 'RJ']
df_data.columns
#_____________________________________renomeando as colunas + gambiarra para aparecer no Dropdown_______________________________
select_columns={'Casos Acumulados':'casosAcumulado','Novos Casos':'casosNovos','Totais de Obitos':'obitosAcumulado','Obitos por Dia':'obitosNovos'}

# ___________________Instacia Dash__________________________
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# __________________MAPA__________________________
fig = px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos", center={'lat':-9.115934 , 'lon':-53.064280}, zoom=3, geojson=brazil_states,
                           color_continuous_scale='Redor', opacity=0.4, hover_data={'casosAcumulado': True, 'casosNovos': True, 'obitosAcumulado': True, 'estado': True})
fig.update_layout(mapbox_style='carto-darkmatter', paper_bgcolor='#242424',
                  autosize=True, margin=go.Margin(l=0, r=0, t=0, b=0), showlegend=False)
df_data = df_states[df_states["estado"] == "RO"]
# _____________________Grafico de Barras____________________________
fig2 = go.Figure(layout={'template': 'plotly_dark'})
# add conjunto de dados na figure
fig2.add_trace(go.Scatter(x=df_data['data'], y=df_data['casosAcumulado']))
fig2.update_layout(paper_bgcolor='#242424', plot_bgcolor='#242424',
                   autosize=True, margin=dict(l=10, r=10, t=10, b=10))


# ________________________EXIBICAO DO GRAFICOS_________________________________________________

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
                html.Div([
                    html.H3('Evolução Covid-19'),
                    html.H5('Fevereiro 2020 - Maio 2021'),
                    dbc.Button('BRASIL', color='primary',
                               id='button-location', size='lg')

                ], style={}),
            html.P('Informe a data para obter informações:',
                   style={'margin-top': '40px'}),
            html.Div(id='test', children=[
                # ___________________________ESCOLHER UMA DATA POR VEZ___________________________________
                dcc.DatePickerSingle(
                        id='date-picker',
                        min_date_allowed=df_brasil['data'].min(),
                        max_date_allowed=df_brasil['data'].max(),
                        initial_visible_month=df_brasil['data'].min(),
                        date=df_brasil['data'].max(),
                        display_format='MMMM D,YYYY',
                        style={'border': '0px solid white'}
                )

            ]),
            # ____________________________________CARDS___________________________________________
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos Recuperados'),
                            html.H3(style={'color': '#adfc92'},
                                    id='casos-recuperados-text'),
                            html.Span('Em Acompanhamento'),
                            html.H5(id='casos-acompanhamento'),

                        ])
                    ], color='ligth', outline=True, style={'margin-top': "10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                           "color": "#FFFFFF"})
                ], md=4),
                   dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos Confirmados'),
                            html.H3(style={'color': '#389fd6'},
                                    id='casos-confirmados'),
                            html.Span('Novos casos nesta Data'),
                            html.H5(id='novos-casos-data'),

                        ])
                    ], color='ligth', outline=True, style={'margin-top': "10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                           "color": "#FFFFFF"})
                ], md=4),
                       dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Obitos Confirmados'),
                            html.H3(style={'color': '#df2935'},
                                    id='Obitos-Confirmados'),
                            html.Span('Obitos nesta data'),
                            html.H5(id='Obitos na data'),

                        ])
                    ], color='ligth', outline=True, style={'margin-top': "10px",
                                                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                           "color": "#FFFFFF"})
                ], md=4)

                # _______________________DropDown abaixo dos CARDS_____________________________________________
            ]),
            html.Div([
                 html.P('Selecione o tipo de dado que deseja visualizar:',style={'margin-top': '25px'}),
                 dcc.Dropdown(id='location-dropdown',
                              options=[{'label':d,'value':a }for d,a in select_columns.items()],
                              value='casosNovos',
                              style={'margin-top':'10px'}
                              ),
                 #________________GRAFICO DE BARRAS________________________________________________________________
                 dcc.Graph(id='linegraph', figure=fig2)
            ]),
    
        ],md=5,style={'padding':'25px', 'background-color':'#242424'}),
        # _______________PLOTAR MAPA____________________________
        dbc.Col([
            dcc.Loading(id='loading-1',type='default',
            children=[
                (dcc.Graph(id='cholopleth-map', figure=fig, style={'height':'100vh','margin-right':'10px'}))
                      ]            ),
            
        ],md=7)
    ])
#________preencher a tela________________________
,fluid=True)
#__________________________________________________
#_______________INTERATIVIDADE COM O DASHBOARD_________________________________________
@app.callback(
       [
            Output('casos-recuperados-text','children'),
            Output('casos-acompanhamento','children'),
            Output('casos-confirmados','children'),
            Output('novos-casos-data','children'),
            Output('Obitos-Confirmados','children'),
            Output('Obitos na data','children')
       
        
        ],
    [Input('date-picker','date'),Input('button-location','children')]
    )
#____________________________________________FUNCAO PARA  APARECER OS DADOS CORRETAMENTE NO CARD________________________________
def display_status(date, location):
    
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        df_data_on_date = df_states[(df_states["estado"] == location) & (df_states["data"] == date)]
#_____________________________________DADOS DOS CARDS_____________________________________________APARECER OS DADOS EM NUMEROS DECIMAIS__________________
    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".") 
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )
 #__________Funcao para mexer no dropdown e o grafico se alterar_________________________________
@app.callback(Output('linegraph','figure'),
               
               [Input('location-dropdown','value'),
                Input('button-location','children')]
               )
def plot_line_graph(plot_type,location):
     if location=='BRASIL':
         df_data_on_location = df_brasil.copy()
         
     else:
         df_data_on_location = df_states[df_states["estado"] ==location]
     
     plot_bar = ['casosNovos','obitosNovos']
     
     fig2 = go.Figure(layout={'template':'plotly_dark'})
     if plot_type in plot_bar:
         fig2.add_trace(go.Bar(x=df_data_on_location['data'], y=df_data_on_location[plot_type]))
     else:
          fig2.add_trace(go.Scatter(x=df_data_on_location['data'], y=df_data_on_location[plot_type]))
          
#______________alterar parametros de layout para ficar padronizado______________________________________          
     fig2.update_layout(paper_bgcolor='#242424', plot_bgcolor='#242424',
                   autosize=True, margin=dict(l=10, r=10, t=10, b=10))

     return fig2
        
#______________________________Mudar o mapa de acordo com a data_____________________________________
@app.callback(
    Output("cholopleth-map", "figure"), 
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states, 
        center={"lat": CENTER_LAT, "lon": CENTER_LON},  # https://www.google.com/maps/ -> right click -> get lat/lon
        zoom=4, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False}
        )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig
#_______________FUNCTION PARA CLICAR NO MAPA E FILTRAR DADOS___________________________________
@app.callback(
    Output('button-location','children'),
    [Input('cholopleth-map','clickData'),Input('button-location','n_clicks')]
    
    
)
def update_location(click_data,n_clicks):
    change_id = [p['prop_id']for p in dash.callback_context.triggered][0]
    if click_data is not None and change_id !='button-location.n_clicks':
        state = click_data['points'] [0] ['location']
        return '{}'.format(state)
    else:
        return'BRASIL'    
    
# ________________Iniciar o Dash_____________________________________________________________________
if __name__ == '__main__':
    app.run_server(debug=True)
