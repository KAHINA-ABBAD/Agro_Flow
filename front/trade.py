import pandas as pd
from projetressourcesagricoles.data import get_data
from projetressourcesagricoles.db import query_db_pandas
from projetressourcesagricoles.params import *
from front.selection import COUNTRIES
import plotly.graph_objs as go

def trade_balance_data(
    pays,
    produit,
    years = ['2013','2014', '2015','2016','2017','2018','2019','2020'],
    df=None
):

    if df is not None:
        df3 = df[df['Code Élément'] != CODE_PRODUCTION]
    else:
        df3 = get_data(pays,CODES_IMPORT_QTES + CODES_EXPORT_QTES, itemcodes_list= produit)

    try:
        df3.iloc[0]
        #years = [f"{y}".replace('y', 'Y') for y in years]
    except Exception as e:
        print(e)
        return go.Bar({})


    if len(df3) == 0:
        return go.Bar({})

    pays_label = df3.iloc[0]['Pays']
    produit_label = df3.iloc[0]['Produit']

    df3 = df3.loc[: ,['Code pays déclarant', 'Code pays partenaire', 'Code Produit',
       'Code Élément', 'Élément', 'Unité']+years]
    df3 = df3.groupby('Élément').agg({f'{year}':'sum' for year in years})
    df3.loc['Trade - Balance']= [ (df3.iloc[0,i] - df3.iloc[1,i]) for i in range (df3.shape[1])]
    df3 = df3.T
    df3.reset_index(inplace = True)
    df3['index'] = df3['index'].apply(lambda x: x.strip('y'))
    df3.rename(columns={"index": "Année"}, inplace = True)
    df3.set_index('Année', inplace = True)


    #Graphe
    trace1 = go.Bar(
                    x = df3.index,
                    y = df3['Importations - Quantité'],
                    name = "Import",
                    marker = dict(color = 'rgba(0,191,255, 1)',
                                line=dict(color='rgb(0,0,0)',width=1.5)),
                    #text = df3['Importations - Quantité']
                )

    trace2 = go.Bar(
                    x = df3.index,
                    y = df3['Exportations - Quantité'],
                    name = "Export",
                    marker = dict(color = 'rgba(1, 255, 130, 1)',
                                line=dict(color='rgb(0,0,0)',width=1.5)),
                    #text = df3['Exportations - Quantité']
                )

    trace3 = go.Bar(
                    x = df3.index,
                    y =  df3['Trade - Balance'],
                    name = "Trade Deficit",
                    marker = dict(color = 'rgba(220, 20, 60, 1)',
                                line=dict(color='rgb(0,0,0)',width=1.5)),
                    #text = df3['Trade - Balance']
                )


    data = [trace1, trace2, trace3]
    layout = go.Layout(barmode = "group")
    fig = go.Figure(data = data, layout = layout)
    fig.update_layout(
        title=go.layout.Title(
            text=f"Balance des imports et exports pour {pays_label} et {produit_label}",
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Année",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Quantité",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )
    return fig
