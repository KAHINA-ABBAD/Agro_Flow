import os
from dotenv import load_dotenv

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__),
    '..',
    'raw_data'
)


 ## SQL FROM .ENV FILE ##
load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PUBLIC_IP_ADDRESS = os.getenv("DB_PUBLIC_IP_ADDRESS")
DB_NAME = os.getenv("DB_NAME")
DB_CNX = f"mysql+pymysql://root:{DB_PASSWORD}@{DB_PUBLIC_IP_ADDRESS}/{DB_NAME}"
##

USE_SQLITE=os.getenv('USE_SQLITE') == "1"


MAP_BOX_TOKEN=os.getenv('MAP_BOX_TOKEN')

ENCODING = 'iso-8859-1'


# CHIFFRES DATA
NB_LIGNES_CCE = 5604339
NB_LIGNES_PROD = 13224
CODE_PRODUCTION = 5510
CODES_EXPORT_QTES = [5907, 5908, 5909, 5910]
CODES_IMPORT_QTES = [5607, 5608, 5609, 5610]

# CHEMINS LOCAUX
"""
PROJECT_FOLDER = os.path.join("..", '..', 'projetressourcesagricoles')
TMP_FOLDER = os.path.join(DATA_FOLDER, 'tmp')
COUNTRY_CODES_PATH = f"{RAW_DATA_FOLDER}/Codes_pays.csv"
PRODUCTS_CODES_PATH = f"{RAW_DATA_FOLDER}/Codes_produits.csv"
"""

FAO_FOLDER = os.path.join(DATA_FOLDER, 'commerce')
PROD_FOLDER = os.path.join(DATA_FOLDER, 'production')


# GCP
# gcloud config set project wagon-bootcamp-348315
BUCKET_NAME = 'wagon-resagriproj-data'
# Pour accès authentififé à GCP:
#RAW_DATA_FOLDER = f"gs://{BUCKET_NAME}/raw_data"
# Pour accès ouvert à GCP
RAW_DATA_FOLDER = r"https://storage.googleapis.com/wagon-resagriproj-data/raw_data"
BUCKET_COMMERCE_FOLDER = f"{RAW_DATA_FOLDER}/commerce"
BUCKET_PRODUCTION_FOLDER = f"{RAW_DATA_FOLDER}/production"
COUNTRY_CODES_PATH = f"{RAW_DATA_FOLDER}/Codes_pays.csv"
PRODUCTS_CODES_PATH = f"{RAW_DATA_FOLDER}/Codes_produits.csv"
