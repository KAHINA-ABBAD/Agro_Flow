import pandas as pd


def get_exchange_balance(
    df : pd.DataFrame,
    from_country_name: str,
    to_country_name:str,
    ressource_code: int,
    year: int
):

    if ressource_code:
        query = f"`Code Produit (FAO)` == {ressource_code} & `Pays déclarants (ISO)` == '{from_country_name}' & `Pays partenaire (ISO)` == '{to_country_name}' & `Année` == {year}"
        print(query)
        exchange_data = df.query(query)
        ressource_name = exchange_data['Produit'].iloc[0]

    else:
        raise NotImplementedError('Ressource name query not implemented => use product code for now')

    IMPORT_QTE = 'Importations - Quantité'
    IMPORT_VAL = 'Importations - Valeur'

    EXPORT_QTE = 'Exportations - Quantité'
    EXPORT_VAL = 'Exportations - Valeur'



    return pd.DataFrame({
        'import_qte': []
    })
