from sre_parse import State
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, dash_table
import plotly.express as px
from projetressourcesagricoles.data import get_data
from projetressourcesagricoles.db import query_db_pandas
import pandas as pd
import plotly.express as px
from functools import lru_cache
import front.selection as selection


@lru_cache(maxsize=4)
def query_production_evolution(ressource_id) -> pd.DataFrame:
    req = f"""
SELECT
	p.`Area Code` as area_code,
	p.`Year` as year,
	SUM(p.Value) AS value
FROM productions p
JOIN items i on p.`Item Code` = i.`Code Produit`
JOIN areas a on p.`Area Code` = a.`Code Pays`
WHERE p.`Item Code` = {ressource_id}
AND p.Value > 0
AND p.`Area Code` < 5000
GROUP BY p.`Area Code`, p.`Year`
ORDER BY p.Year DESC, value DESC
"""

    try:
        prod_history_df = query_db_pandas(req)
        if len(prod_history_df) == 0:
            raise ValueError('No data')
    except Exception as e:
        return None

    prod_history_df = prod_history_df.groupby(by='year')['value'].sum().reset_index()
    return prod_history_df

@lru_cache(maxsize=4)
def plot_prod_evolution(ressource_id):
    prod_df = query_production_evolution(ressource_id)
    if prod_df is None:
        return px.area({})

    return px.area(
        prod_df,
        x='year',
        y='value',
        title="Evolution de la production mondiale",
    )

@lru_cache(maxsize=4)
def query_transit_evolution(item_code):

    req = f'''
    SELECT
        e.`Code Élément`,
        e.`Code Produit`,
        SUM(e.Y1986) as total_1986,
        SUM(e.Y1987) as total_1987,
        SUM(e.Y1988) as total_1988,
        SUM(e.Y1989) as total_1989,
        SUM(e.Y1990) as total_1990,
        SUM(e.Y1991) as total_1991,
        SUM(e.Y1992) as total_1992,
        SUM(e.Y1993) as total_1993,
        SUM(e.Y1994) as total_1994,
        SUM(e.Y1995) as total_1995,
        SUM(e.Y1996) as total_1996,
        SUM(e.Y1997) as total_1997,
        SUM(e.Y1998) as total_1998,
        SUM(e.Y1999) as total_1999,
        SUM(e.Y2000) as total_2000,
        SUM(e.Y2001) as total_2001,
        SUM(e.Y2002) as total_2002,
        SUM(e.Y2003) as total_2003,
        SUM(e.Y2004) as total_2004,
        SUM(e.Y2005) as total_2005,
        SUM(e.Y2006) as total_2006,
        SUM(e.Y2007) as total_2007,
        SUM(e.Y2008) as total_2008,
        SUM(e.Y2009) as total_2009,
        SUM(e.Y2010) as total_2010,
        SUM(e.Y2011) as total_2011,
        SUM(e.Y2012) as total_2012,
        SUM(e.Y2013) as total_2013,
        SUM(e.Y2014) as total_2014,
        SUM(e.Y2015) as total_2015,
        SUM(e.Y2016) as total_2016,
        SUM(e.Y2017) as total_2017,
        SUM(e.Y2018) as total_2018,
        SUM(e.Y2019) as total_2019,
        SUM(e.Y2020) as total_2020
    FROM exchanges e
    WHERE e.`Code Produit` = _%*%
    AND e.`Code Élément` IN (5907, 5908, 5909, 5910)
    GROUP BY e.`Code Élément`, e.`Code Produit`;
    '''.replace('"', "`").replace(r"_%*%", str(item_code))

    try:
        transit_history_df = query_db_pandas(req)
        #print(f"{req = }")
    except Exception as e:
        return None

    #transit_history_df = transit_history_df.groupby(by='year')['value'].sum().reset_index()
    return transit_history_df

@lru_cache(maxsize=4)
def plot_transit_evolution(ressource_id):
    transit_df = query_transit_evolution(ressource_id)
    if transit_df is None:
        return px.area()

    transit_df.drop(columns=['Code Élément', 'Code Produit'], inplace=True)
    qty = transit_df.columns.to_list()
    year = transit_df.values[0]
    return px.area(
        x=qty,
        y=year,
        labels={"x": "Année", "y": "Quantité"},
        title="Evolution de la somme des exports"
    )

@lru_cache(maxsize=4)
def plot_prod_chloro(ressource_id):

    req_production = f'''
    SELECT
        p."Area Code",
        a."Code ISO3",
        a.Pays,
        p.`Item Code`,
        i.Produit,
        p.`Element Code`,
        p.`Year`,
        p.Unit,
        p.Value,
        p.Flag
    FROM productions p
    JOIN items i on i.`Code Produit` = p.`Item Code`
    JOIN areas a ON a."Code Pays" = p."Area Code"
    WHERE p.`Item Code` = {ressource_id}
    AND p.`Element Code` = 5510
    AND p.Value > 0
    '''.replace('"', "`")

    try:
        prod = query_db_pandas(req_production)
        if len(prod) == 0:
            raise ValueError('No data')
    except Exception as e:
        return px.choropleth({})


    config = { "displayModeBar": False}
    p_chloro = px.choropleth(
            prod,
            locations="Code ISO3",
            color="Value", # lifeExp is a column of gapminder
            hover_name="Pays", # column to add to hover information
            color_continuous_scale=px.colors.sequential.speed,
            animation_frame='Year',
            title="Evolution de la production "
        )
    p_chloro.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return p_chloro


def get_top_producers(item_code, years, nb_producers):

    req_top_producer = f'''
    SELECT
        p."Area Code",
        a."Code ISO3",
        a.Pays,
        p.`Item Code`,
        i.Produit,
        p.`Element Code`,
        p.`Year`,
        p.Unit,
        p.Value,
        p.Flag
    FROM productions p
    JOIN items i on i.`Code Produit` = p.`Item Code`
    JOIN areas a ON a."Code Pays" = p."Area Code"
    WHERE p.`Item Code` = {item_code}
    AND p.Year = {years}

    AND p.`Element Code` = 5510
    AND p.Value > 0
    AND p."Area Code" < 5000
    '''.replace('"', "`")

    try:
        prod = query_db_pandas(req_top_producer).drop_duplicates(['Value']).sort_values(by='Value', ascending=True)
    except Exception as e:
        return None

    return prod.tail(nb_producers)


def plot_top_producers(item_code, annee, nb_producers=5):
    top10_producer = get_top_producers(item_code, annee, nb_producers)

    if not isinstance(top10_producer, pd.DataFrame):
        return px.bar({})

    if len(top10_producer) == 0:
        return px.bar({})

    nom_produit = top10_producer.iloc[0]['Produit']

    fig = px.bar(top10_producer, x='Value', y='Pays', text='Value', title=f'Top {nb_producers} des producteurs de {nom_produit} au monde pour l\'année {annee}')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig


def per_ressource_page(app):
    return html.Div([
        dcc.Dropdown(
            id="per_products_produits",
            clearable=True,
            searchable=True,
            multi=False,
            options=selection.PRODUITS_OPTION,
            #value=515,
            style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
        ),
        html.Hr(),
        dcc.Loading(
            id="loading-4",
            type="default",
            children=[
                dcc.Graph(
                    id='ressource_prod_evolution',
                    config= {'displayModeBar': False}
                ),
            ]
        ),

        html.Hr(),
        dcc.Loading(
            id="loading-5",
            type="default",
            children=[
                dcc.Graph(
                    id='ressource_evolution_ie',
                    config= {'displayModeBar': False}
                ),
            ]
        ),

        html.Hr(),
        dcc.Loading(
            id="loading-6",
            type="default",
            children=[
                dcc.Graph(
                    id='ressource_top_producers',
                    config= {'displayModeBar': False}
                ),
            ]
        ),


        html.Hr(),
        dcc.Loading(
            id="loading-7",
            type="default",
            children=[
                dcc.Graph(
                    id='chloro_production',
                ),
            ]
        ),



    ])
