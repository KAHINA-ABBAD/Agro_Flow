
import pandas as pd
import numpy as np

crops_df = pd.read_csv('../agriculture-crop-production/data/production_crops_e_europe.csv')


def query_production(
    country_iso_code:int,
    ressource_code: int,
    years: list,
    element: str = 'Production',
) -> pd.DataFrame:
    query = f'item_code == {ressource_code} and area_code == {country_iso_code} and element == "{element}"'
    result_df = crops_df.query(query)

    unit_values = result_df['unit'].unique()
    if len(unit_values):
        production_unit = unit_values[0]
    else:
        production_unit = "MULTIPLE UNITS WARNING"

    values = []
    for year in years:
        year_val = result_df[f'y{year}'].values[0]
        values.append(year_val)

    return pd.DataFrame({
        "years": years,
        "production": values,
    })
