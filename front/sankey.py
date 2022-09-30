from dotenv import load_dotenv
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from projetressourcesagricoles.data import get_data
from projetressourcesagricoles.db import query_db_pandas
from projetressourcesagricoles.params import *



def get_sankey_data(code_pays, code_produit, annee):
    req_prod = f"""
    SELECT *
    from productions p
    WHERE p."Area Code" = {code_pays}
    AND p."Item Code" = {code_produit}
    AND p."Element Code" = 5510
    AND p."Year" = {annee}
    """.replace('"', "`")

    req_exc = f"""
    SELECT
        e."Code pays déclarant",
        a.Pays,
        e."Code pays partenaire",
        ap.Pays as 'Pays partenaire',
        e."Code Produit",
        e."Code Élément",
        e.Unité,
        e.Y{annee}
    FROM exchanges e
    JOIN areas ap on e."Code pays partenaire" = ap."Code Pays"
    JOIN areas a on e."Code pays déclarant" = a."Code Pays"
    WHERE e."Code Produit" = {code_produit}
    AND e."Code pays déclarant" = {code_pays}
    AND e."Code Élément" in (5610, 5910)
    """.replace('"', "`")

    prod_df = query_db_pandas(req_prod)
    exch_df = query_db_pandas(req_exc)

    return prod_df, exch_df




def get_sankey(code_pays, code_produit, annee, nb_voisins = 15):

    prod_df, exch_df = get_sankey_data(code_pays, code_produit, annee)
    prod = prod_df.iloc[0]['Value']

    import_df = exch_df[exch_df['Code Élément'].isin(CODES_IMPORT_QTES)]
    export_df = exch_df[exch_df['Code Élément'].isin(CODES_EXPORT_QTES)]

    imp = import_df.dropna().sort_values(by=f'Y{annee}', ascending=False).head(nb_voisins)
    exp = export_df.dropna().sort_values(by=f'Y{annee}', ascending=False).head(nb_voisins)

    nodes = imp['Pays partenaire'].tolist() + ['AUTOPRODUCTION', 'FRANCE'] + exp['Pays partenaire'].tolist()
    sources = list(np.arange(0, len(imp) + 2)) + [len(imp) + 1] * (len(exp))
    targets = [len(imp) + 1] * (len(imp) + 1) + list(np.arange(len(imp) + 2, len(imp) + 2 + len(exp)))
    values = imp[f'Y{annee}'].tolist() + [prod] + exp[f'Y{annee}'].tolist()

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = nodes,
        color = "blue"
        ),
        link = dict(
        source = sources,
        target = targets,
        value = values
        )
    )])

    fig.update_layout(title_text="Flow Imports et exports", font_size=10)
    return fig
