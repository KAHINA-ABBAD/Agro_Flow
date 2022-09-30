import pandas as pd
from glob import glob
import os

def concatenate_csv(pattern : str, **kwargs) -> pd.DataFrame:
    """
    Lit les csv répondant au pattern passé en paramètre et
    concatène les lectures selon l'axe 0

    :param str pattern: glob pattern to find files ie '../data/prod_*.csv'
    """
    df = pd.DataFrame()
    files = glob(pattern)
    files = sorted(files)
    for csv_file in files:
        print(f'Loading : {os.path.basename(csv_file)}')
        df = pd.concat(
            [
                df,
                pd.read_csv(csv_file, **kwargs)
            ]
        )
    return df
