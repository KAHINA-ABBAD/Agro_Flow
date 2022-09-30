from projetressourcesagricoles.params import *
from projetressourcesagricoles.data import get_data
import plotly.express as px
import pandas as pd
import numpy as np
import sqlalchemy

def get_10_top_producer(item_code, years):
    prod_one_year_req = f'''
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

    engine = sqlalchemy.create_engine(DB_CNX)
    with engine.connect() as conn:
        prod = pd.read_sql(prod_one_year_req, conn).sort_values(by='Value', ascending=False)

    return prod.head(10)

def topFive_produits(code_pays, Annee):
    """ Production: top5 produits par année - return: dict{produit: quantité} """
    """5510 : Correspond au code élément, qui représente la production d'un pays
    """
    data = get_data(code_pays, 5510, '*', '*', Annee, Annee)
    data = data.sort_values(by=['y' + str(Annee)], ascending=False)
    top_5 = data[['Produit','y' + str(Annee)]].head(5)
    top_5.rename(columns={'y' + str(Annee) : 'Qantité'}, inplace=True)

    # top_5 = top_5.to_dict('index')
    # top_5 = top_5.set_index('Produit').T.to_dict('list')
    return top_5

def plot_topFiveProd(code_pays, annee):
    """ La fonction qui plot les top 5 produit d'un pays
    """

    top5 = topFive_produits(code_pays, annee)
    fig = px.bar(top5, x='Produit', y='Qantité', text='Qantité')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()

def topFive_produitsImport(code_pays, Annee):
    """ Import: top5 produits par année - return: dict{produit: quantité} """
    """5610 : Correspond au code élément, qui représente l'importation d'un pays
    """

    data = get_data(code_pays, 5610, '*', '*', Annee, Annee)
    data = data.sort_values(by=['y' + str(Annee)], ascending=False)
    top_5_Import = data[['Produit','y' + str(Annee)]].head(5)
    top_5_Import.rename(columns={'y' + str(Annee) : 'Qantité'}, inplace=True)

    # top_5 = top_5.to_dict('index')
    top_5_Import = top_5_Import.set_index('Produit').T.to_dict('list')

    return top_5_Import

def topFive_produitsExport(code_pays, Annee):
    """ Export: top5 produits par année - return: dict{produit: quantité} """
    """5910 : Correspond au code élément, qui représente l'exportation d'un pays
    """
    data = get_data(code_pays, 5910, '*', '*', Annee, Annee)

    data = data.sort_values(by=['y' + str(Annee)], ascending=False)
    top_5_Export = data[['Produit','y' + str(Annee)]].head(5)
    top_5_Export.rename(columns={'y' + str(Annee) : 'Qantité'}, inplace=True)

    # top_5 = top_5.to_dict('index')
    top_5_Export = top_5_Export.set_index('Produit').T.to_dict('list')

    return top_5_Export

def get_10_top_producer(item_code, years):

    prod_one_year_req = f'''
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

    engine = sqlalchemy.create_engine(DB_CNX)
    with engine.connect() as conn:
        prod = pd.read_sql(prod_one_year_req, conn).sort_values(by='Value', ascending=False)

    return prod.head(10)

def evolution_pruduit(item_code):
    evolu_produit = f'''
    SELECT
        p.`Year`,
        a.Pays,
	    SUM(p.Value) AS total_pays
    FROM productions p
    JOIN items i on p.`Item Code` = i.`Code Produit`
    JOIN areas a on p.`Area Code` = a.`Code Pays`
    WHERE p.`Item Code` = {item_code}
    AND p.Value > 0
    AND p.`Area Code` < 5000
    GROUP BY a.Pays, p.`Year`
    ORDER BY p.Year DESC, total_pays DESC;
    '''.replace('"', "`")

    engine = sqlalchemy.create_engine(DB_CNX)
    with engine.connect() as conn:
        prod = pd.read_sql(evolu_produit, conn).groupby(by='Year').sum()
        prod = prod.reset_index().rename(columns = {'Year' : 'Année', 'total_pays' : 'Production mondial'})

    return prod

def plot_evolution(item_code):

    data = evolution_pruduit(item_code)
    fig = px.line(data, x='Année', y='Production mondial', markers=True, title=f'Evolution mondiale de la production de Blé.')
    fig.show()

def plot_10TopProducer(item_code, annee):
    top10_producer = get_10_top_producer(item_code, annee)

    nom_produit = top10_producer.iloc[0]['Produit']

    fig = px.bar(top10_producer, x='Value', y='Pays', text='Value', title=f'Top 10 des producteurs de {nom_produit} au monde')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()


def data_for_plot (data):

    #Remplacer les Nan par 0 pour pouvoir utiliser la methode stack()
    data = data.replace(np.nan, 0)
    name_col_data = data.columns
    for col in name_col_data:
        if col.endswith('f'):
            del data[col]
    name_col = list(data.iloc[0:,:9].columns)
    new_data = data.set_index(name_col).stack().reset_index().rename(columns = {'level_9':"Annee", 0 :'Production' })

    return new_data

def Plot_Import_Export_pays(code_pays, code_produit):

    prod_import_export = get_data(code_pays, CODES_EXPORT_QTES + CODES_IMPORT_QTES + [CODE_PRODUCTION] , itemcodes_list=code_produit, year_start=1986, year_end=2020)
    prod_import_export = data_for_plot(prod_import_export)
    nom_produit = prod_import_export.iloc[0]['Produit']
    nom_pays = prod_import_export.iloc[0]['Pays']

    prod_import_export = prod_import_export.groupby(by=['Annee', 'Élément'])['Production'].sum().reset_index()
    fig = px.line(prod_import_export, x="Annee", y="Production", color='Élément', title=f'Évolution des Imports / Exports / Production des {nom_produit} en {nom_pays}')

    return fig
