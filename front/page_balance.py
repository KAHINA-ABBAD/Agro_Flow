from sre_parse import State
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, dash_table
import plotly.express as px
from projetressourcesagricoles.data import get_data
from projetressourcesagricoles.db import query_db_pandas
from projetressourcesagricoles.params import *

import pandas as pd
import plotly.express as px
from functools import lru_cache
import front.selection as selection
import front.trade as trade_fct
import numpy as np


def data_for_plot (data):
    data = data.replace(np.nan, 0)
    name_col_data = data.columns
    for col in name_col_data:
        if col.endswith('f'):
            del data[col]
    name_col = list(data.iloc[0:,:9].columns)
    new_data = data.set_index(name_col).stack().reset_index().rename(columns = {'level_9':"Annee", 0 :'Production' })
    return new_data


def Plot_Import_Export_pays(code_pays, code_produit, df=None):

    if df is None:
        prod_import_export = get_data(
            code_pays, CODES_EXPORT_QTES + CODES_IMPORT_QTES + [CODE_PRODUCTION],
            itemcodes_list=code_produit,
            year_start=1986,
            year_end=2020
        )
    else:
        prod_import_export=df

    prod_import_export = data_for_plot(prod_import_export)
    nom_produit = prod_import_export.iloc[0]['Produit']
    nom_pays = prod_import_export.iloc[0]['Pays']

    prod_import_export = prod_import_export.groupby(by=['Annee', 'Élément'])['Production'].sum().reset_index()
    fig = px.line(prod_import_export, x="Annee", y="Production", color='Élément', title=f'Évolution des Imports / Exports / Production des {nom_produit} en {nom_pays}')

    return fig



def get_trade_balance(pays, produit, years, df=None):
    trade_plot = trade_fct.trade_balance_data(pays, produit, [f'y{y}' for y in years], df=df)
    return trade_plot


def per_balance_page(app):
    return html.Div([
        dcc.Dropdown(
            id="per_balance_pays",
            clearable=True,
            searchable=True,
            multi=False,
            options=selection.COUNTRIES_OPTION,
            #value=68,
            style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
        ),
        dcc.Dropdown(
            id="per_balance_produits",
            clearable=True,
            searchable=True,
            multi=False,
            options=selection.PRODUITS_OPTION,
            #value=515,
            style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
        ),
        dcc.Dropdown(
            id="per_balance_years",
            clearable=True,
            searchable=True,
            multi=True,
            options=np.arange(1986, 2021, 1),
            value=np.arange(1986, 2020, 1),
            style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
        ),
        html.Button(
            'Go',
            id='submit-trade',
            n_clicks=0,
            style={'flex': '0 0 0px'}
        ),
        html.Hr(),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=[
                dcc.Graph(
                    id='per_balance_trade',
                ),
            ]
        ),
        html.Hr(),
        dcc.Loading(
            id="loading-2",
            type="default",
            children=[
                dcc.Graph(
                    id='per_balance_evolution',
                ),
            ]
        ),
    ])
