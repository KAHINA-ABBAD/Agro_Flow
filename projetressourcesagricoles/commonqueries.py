import sqlalchemy
from projetressourcesagricoles.params import *
import pandas as pd
import html.entities


def get_country_names(connexion=None):
    countries_query = f'''
SELECT "Code Pays", "Pays" FROM areas a
    '''.replace('"', "`")

    if connexion:
        with connexion:
            result = pd.read_sql(countries_query, connexion)
    else:
        engine = sqlalchemy.create_engine(DB_CNX)
        with engine.connect() as conn:
            result = pd.read_sql(countries_query, conn)

    table = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}
    return result


def get_product_list(connexion=None):
    product_query = f'''
SELECT "Code Produit", "Produit" FROM items
    '''.replace('"', "`")

    if connexion:
        with connexion:
            result = pd.read_sql(product_query, connexion)
    else:
        engine = sqlalchemy.create_engine(DB_CNX)
        with engine.connect() as conn:
            result = pd.read_sql(product_query, conn)

    table = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}
    return result



def get_production(item_code, years):

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
    AND p.Year = 2020
    AND p.`Element Code` = 5510
    AND p.Value > 0
    '''.replace('"', "`")

    engine = sqlalchemy.create_engine(DB_CNX)
    with engine.connect() as conn:
        prod = pd.read_sql(prod_one_year_req, conn)

    return prod
