import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
from functools import lru_cache

from projetressourcesagricoles.data import get_data
from projetressourcesagricoles.db import query_db_pandas
import front.selection as selection


def top_products_per_country(code_pays, Annee, nb_produits):
    """ Production: top5 produits par année - return: dict{produit: quantité} """
    """5510 : Correspond au code élément, qui représente la production d'un pays
    """
    data = get_data(code_pays, 5510, '*', '*', Annee, Annee)
    data = data.sort_values(by=['y' + str(Annee)], ascending=False)
    top_5 = data[['Produit','y' + str(Annee)]].head(nb_produits)
    top_5.rename(columns={'y' + str(Annee) : 'Qantité'}, inplace=True)
    return top_5


def plot_top_products_per_country(code_pays, annee, nb_produits):
    """ La fonction qui plot les top 5 produit d'un pays
    """
    top5 = top_products_per_country(code_pays, annee, nb_produits)
    fig = px.bar(
        top5,
        x='Produit',
        y='Qantité',
        text='Qantité',
        title=f"Les {nb_produits} ressources les plus produites"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig



def top_products_imported_per_country(code_pays, Annee, nb_produits=5):
    """ Import: top5 produits par année - return: dict{produit: quantité} """
    """5610 : Correspond au code élément, qui représente l'importation d'un pays
    """
    data = get_data(code_pays, 5610, '*', '*', Annee, Annee)
    data = data.sort_values(by=['y' + str(Annee)], ascending=False)
    top_5_Import = data[['Produit','y' + str(Annee)]].head(5)
    top_5_Import.rename(columns={'y' + str(Annee) : 'Qantité'}, inplace=True)
    top_5_Import = top_5_Import.set_index('Produit').T.to_dict('list')
    return top_5_Import


def top_products_exported_per_country(code_pays, Annee, nb_produits=5):
    """ Export: top5 produits par année - return: dict{produit: quantité} """
    """5910 : Correspond au code élément, qui représente l'exportation d'un pays
    """
    data = get_data(code_pays, 5910, '*', '*', Annee, Annee)
    data = data.sort_values(by=['y' + str(Annee)], ascending=False)
    top_5_Export = data[['Produit','y' + str(Annee)]].head(5)
    top_5_Export.rename(columns={'y' + str(Annee) : 'Qantité'}, inplace=True)
    top_5_Export = top_5_Export.set_index('Produit').T.to_dict('list')

    return top_5_Export



def page_per_pays(app):
    return html.Div([
        dcc.Dropdown(
            id="per_pays_pays",
            clearable=True,
            searchable=True,
            multi=False,
            options=selection.COUNTRIES_OPTION,
            #value=68,
            style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
        ),
        dcc.Dropdown(
            id="per_pays_year",
            clearable=True,
            searchable=True,
            multi=False,
            options=np.arange(2021, 1960, -1),
            #value=2019,
            style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
        ),
        html.Button(
            'Go',
            id='submit-pays',
            n_clicks=0,
            style={'flex': '0 0 0px'}
        ),
        html.Hr(),
        dcc.Loading(
            id="loading-3",
            type="default",
            children=[
                dcc.Graph(
                    id='per_pays_top_products',
                ),
            ]
        ),
    ])
