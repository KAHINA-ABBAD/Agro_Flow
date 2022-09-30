
import sqlalchemy
from sqlalchemy import text
import pandas as pd
from dotenv import load_dotenv
import os
from projetressourcesagricoles.params import *

def query_db_pandas(query, params=None) -> pd.DataFrame:

    try:
        if USE_SQLITE:
            sqllitepath = os.path.join(DATA_FOLDER, 'exch.db')
            engine = sqlalchemy.create_engine(f"sqlite:///{sqllitepath}")
        else:
            engine = sqlalchemy.create_engine(DB_CNX)

        with engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn
            )
    except Exception as e:
        print(e)
        return None

    return df

if __name__ == '__main__':
    load_dotenv()
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PUBLIC_IP_ADDRESS = os.getenv("DB_PUBLIC_IP_ADDRESS")
    DB_NAME = os.getenv("DB_NAME")

    DB_CNX = f"mysql+pymysql://root:{DB_PASSWORD}@{DB_PUBLIC_IP_ADDRESS}/{DB_NAME}"

    engine = sqlalchemy.create_engine(DB_CNX, echo=True)
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES"))
        print(result.all())
