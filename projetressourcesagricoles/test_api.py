from sys import flags
import pandas as pd
import numpy as np
import os
from projetressourcesagricoles.params import RAW_DATA_FOLDER
from projetressourcesagricoles.data import get_data

COMMERCE_MATRIX_PATH = os.path.join(
    RAW_DATA_FOLDER,
    'commerce',
    '68.csv'
)

PRODUCTION_MATRIX_PATH = os.path.join(
    RAW_DATA_FOLDER,
    'production',
    '68.csv'
)

def load_df_prod():
    df_test = pd.read_csv(PRODUCTION_MATRIX_PATH, low_memory=False)
    return df_test

def load_df_exc():
    df_test = pd.read_csv(COMMERCE_MATRIX_PATH, low_memory=False)
    return df_test

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


def get_reference_as_option(ref_name, **kwargs):
    """
    Retourne une lsite utilisée par un composant option sur le front
    avec les clefs keys, value pour chaque élément
    """
    df = get_reference(ref_name, **kwargs)
    return [{'label': y, 'value': x} for x, y in zip(df[df.columns[0]], df[df.columns[1]])]


def get_reference(ref_name, **kwargs):
    '''
    Retourne un dataframe du fichier de referentiel
    '''

    filename = os.path.join(
        RAW_DATA_FOLDER,
        f'Codes_{ref_name}.csv'
    )

    return pd.read_csv(filename, **kwargs)


if __name__ == "__main__":
    print(get_reference_as_option('pays', encoding='iso-8859-1'))
