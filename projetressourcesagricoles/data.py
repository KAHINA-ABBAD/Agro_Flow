from projetressourcesagricoles.params import *
import plotly.express as px
import pandas as pd
import os
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


def get_IOS3_pays(df):

    countrycodes_df = pd.read_csv(COUNTRY_CODES_PATH, low_memory=False)[['Code Pays', 'Code ISO3']]

    df = pd.merge(df, countrycodes_df, left_on='Code pays déclarant', right_on='Code Pays')
    df.drop(columns=['Code Pays'], inplace=True)

    first_cols = ['Code pays déclarant', 'Pays', 'Code ISO3', 'Code pays partenaire', 'Pays_partenaire', 'Code Produit', 'Produit']
    other_cols = [head for head in df.columns.to_list() if head  not in first_cols]
    good_order_cols = first_cols + other_cols
    df = df[good_order_cols]

    return df

def manage_list_type(input_list):
    """
    Dans une liste, retire les doublons
    Si input n'est pas une liste, transforme en liste
    """
    if isinstance(input_list, list):
        return list(set(input_list))
    return [input_list]


def select_valeurs(df, values_list, column):
    """
    Applique un masque booléen sur une colonne et une liste de values
    """
    values_list = manage_list_type(values_list)

    if values_list == ['*']:
        values_list = df[column].unique()

    return df.loc[df[column].isin(values_list)]

def merge_prod_exch(countrycodes_list, gcp=True):
    """
    Renvoie les données de production et d'échange des countries dans un même dataframe
    """
    countrycodes_list = manage_list_type(countrycodes_list)

    # For authenticated GCP connexion
    #client = storage.Client()
    merged_df = pd.DataFrame()
    for countrycode in countrycodes_list:
        filename = str(countrycode) + '.csv'

        if gcp:
            fao_filepath = f"{BUCKET_COMMERCE_FOLDER}/{filename}"
            prod_filepath = f"{BUCKET_PRODUCTION_FOLDER}/{filename}"
        else:
            prod_filepath = os.path.join(PROD_FOLDER, filename)
            fao_filepath = os.path.join(FAO_FOLDER, filename)

        try:
            df_fao = pd.read_csv(fao_filepath, low_memory=False)
        except:
            df_fao = None
        try:
            df_prod = pd.read_csv(prod_filepath, low_memory=False)
        except:
            df_prod=None

        if df_fao is not None:
            if df_prod is not None:
                country_df = pd.concat([df_fao, df_prod])
            else:
                country_df = df_fao
        elif df_prod is not None:
            country_df = df_prod
        else:
            raise IOError("Impossible de trouver le pays {}.".format(countrycode))

        country_df = country_df[country_df['Code Produit']!='Code Produit']
        merged_df = pd.concat([merged_df, country_df])

    return merged_df

def select_payspart(df, partnercodes_list):
    """
    Filtre la colonne "Code pays partenaire" avec partnercodes_list
    """

    return select_valeurs(df, partnercodes_list, 'Code pays partenaire')

def select_products(df, itemcodes_list):
    """
    Filtre la colonne "Code Produit" avec itemcodes_list
    """
    return select_valeurs(df, itemcodes_list, 'Code Produit')

def select_element(df, elementcodes_list):
    """
    Filtre la colonne "Code Élément" avec elementcodes_list
    """
    return select_valeurs(df, elementcodes_list, 'Code Élément')

def get_years_only(df, year_min, year_max):
    """
    Renvoie les colonnes year_min à year_max_f
    """
    year_min = 'y' + str(year_min)
    year_max = 'y' + str(year_max)
    if not year_max.endswith('f'):
        year_max += 'f'

    return df.loc[:, year_min:year_max]


def filter_rangeyears(df, year_min, year_max):
    """
    Renvoie le df complet sauf les years externes à [year_min, year_max]
    """
    yearscols_to_keep = ['y' + str(y) for y in range(year_min, year_max+1)]
    yearsfcols_to_keep = [y + 'f' for y in yearscols_to_keep]
    cols_to_keep = set(yearscols_to_keep + yearsfcols_to_keep)

    all_years = set('y' + str(y) for y in range(1961, 2021))
    all_years_f = set(y +'f' for y in all_years)
    all_years.update(all_years_f)
    cols_to_del = list(all_years - cols_to_keep)

    return df.drop(columns=cols_to_del)


def add_labels_columns(df, inner_labels=True):
    countrycodes_df = pd.read_csv(COUNTRY_CODES_PATH, low_memory=False)[['Code Pays', 'Pays']]
    itemcodes_df = pd.read_csv(PRODUCTS_CODES_PATH, low_memory=False)[['Code Produit', 'Produit']]

    if inner_labels:
        df = pd.merge(df, countrycodes_df, left_on='Code pays déclarant', right_on='Code Pays',
                    #suffixes=(None, '_déclarant')
                    )
        df = pd.merge(df, countrycodes_df, left_on='Code pays partenaire', right_on='Code Pays', suffixes=(None, '_partenaire'))
        df = pd.merge(df, itemcodes_df, left_on='Code Produit', right_on='Code Produit')
    else:
        df = pd.merge(df, countrycodes_df, left_on='Code pays déclarant', right_on='Code Pays', how='left',
                    #suffixes=(None, '_déclarant')
                    )
        df = pd.merge(df, countrycodes_df, left_on='Code pays partenaire', right_on='Code Pays',
                      suffixes=(None, '_partenaire'), how='left')
        df = pd.merge(df, itemcodes_df, left_on='Code Produit', right_on='Code Produit', how='left')

    df.drop(columns=['Code Pays', 'Code Pays_partenaire'], inplace=True)

    first_cols = ['Code pays déclarant', 'Pays', 'Code pays partenaire', 'Pays_partenaire', 'Code Produit', 'Produit']
    other_cols = [head for head in df.columns.to_list() if head  not in first_cols]
    good_order_cols = first_cols + other_cols
    df = df[good_order_cols]

    return df


def get_data(countrycodes_list, elementcodes_list, partnercodes_list='*', itemcodes_list='*',
             year_start=1961, year_end=2020, gcp=True, inner_labels = True):

    """
    Appelle merge_prod_exch sur les countrycodes
    puis filtre les partnercodes et autres params
    puis ajoute les colonnes de labels pays/partenaire/item à partir de la table ISO3
    """
    gcp = not(USE_SQLITE)
    print(f"{gcp= }")

    countrycodes_list = manage_list_type(countrycodes_list)
    partnercodes_list = manage_list_type(partnercodes_list)

    if partnercodes_list != ['*']:
        partnercodes_list += countrycodes_list

    df = merge_prod_exch(countrycodes_list, gcp)
    df = select_payspart(df, partnercodes_list)
    df = select_products(df, itemcodes_list)
    df = select_element(df, elementcodes_list)
    df = filter_rangeyears(df, year_start, year_end)
    df = add_labels_columns(df, inner_labels)

    return df
