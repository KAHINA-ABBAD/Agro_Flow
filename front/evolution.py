from sys import maxsize
import pandas as pd
import plotly.express as px
from dash import dcc
import numpy as np
from front.selection import get_produit_by_code, get_countrie_by_code
from functools import lru_cache

def line_values_to_columns(df):
    years = np.arange(2000, 2021, 1, dtype=np.int16)
    years_labels = [f'y{y}' for y in years]
    years_flags = [f'y{y}f' for y in years]

    values = df[years_labels].T.values.ravel()
    flags  = df[years_flags].T.values.ravel()
    if len(df) == 0:
        values = np.zeros(len(years))
        flags = [np.nan] * len(years)

    final_df = pd.DataFrame({
        'years': years,
        'values': values,
        'flags': flags,
    })

    return final_df


def get_history(df_prod, area_code, item_codes, query=""):

    if not isinstance(area_code, list):
        area_code = [area_code]

    if not isinstance(item_codes, list):
        item_codes = [item_codes]

    if df_prod is None or len(df_prod) == 0:
        return px.area()

    years = np.arange(1961, 2020, 1, dtype=np.int16)
    years_labels = [f'y{y}' for y in years]
    if not query:
        query = f"`Code pays déclarant` == {area_code} and `Code Produit` in {item_codes} and `Unité` == 'tonnes'"
    val_df = df_prod.query(query)[years_labels]
    values = val_df.T.values.ravel()
    if len(values) == 0:
        values = np.zeros(len(years))

    final_df = pd.DataFrame({
        'years': years,
        'values': values
    })

    item_label = df_prod.iloc[0]['Produit']
    pays_label = df_prod.iloc[0]['Pays']
    fig = px.area(
        final_df,
        x="years",
        y="values",
        title=f'Evolution de la production de <b>{item_label}</b> en <b>{pays_label}</b>'
    )
    return fig



def get_bar_plot(df, area_code, partenaires_codes, products_codes, query=None):

    if not isinstance(area_code, list):
        area_code = [area_code]

    if not isinstance(products_codes, list):
        products_codes = [products_codes]

    if not isinstance(partenaires_codes, list):
        partenaires_codes = [partenaires_codes]

    if df is None:
        return px.bar()

    if not query:
        query_export = f"`Code pays partenaire` in {partenaires_codes} and `Code Produit` in {products_codes} and `Élément` == 'Exportations - Quantité'"
        query_import = f"`Code pays partenaire` in {partenaires_codes} and `Code Produit` in {products_codes} and `Élément` == 'Importations - Quantité'"

    df_export = line_values_to_columns(df.query(query_export))
    df_export['element'] = 'export'
    df_export.replace(-100_000, 0, inplace=True)

    df_import = line_values_to_columns(df.query(query_import))
    df_import['element'] = 'import'
    df_import.replace(-100_000, 0, inplace=True)

    df = pd.concat([df_export, df_import], axis=0)

    produit_label = get_produit_by_code(products_codes[0])
    pays_label = get_countrie_by_code(area_code[0])
    pays_part_label = get_countrie_by_code(partenaires_codes[0])

    fig = px.bar(
        df,
        x="years",
        y="values",
        color="element",
        barmode="group",
        title=f'Imports et Exports du produit <b>{produit_label}</b> entre pays déclarant <b>{pays_label}</b> & pays partenaires <b>{pays_part_label}</b>'
    )

    return fig

if __name__ == '__main__':
    pass
