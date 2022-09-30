from pytz import country_timezones
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table
import projetressourcesagricoles.commonqueries as cq


COUNTRIES = cq.get_country_names().rename(columns={
    'Code Pays': 'value',
    'Pays': 'label'
})
COUNTRIES_OPTION = COUNTRIES.to_dict(orient='records')


PRODUITS = cq.get_product_list().rename(columns={
    'Code Produit': 'value',
    'Produit' : 'label'
})
PRODUITS_OPTION = PRODUITS.to_dict(orient='records')


def get_countrie_by_code(countrie_code):
    try:
        return COUNTRIES[COUNTRIES['value'] == countrie_code].iloc[0]['label']
    except:
        return ''

def get_produit_by_code(produit_code):
    try:
        return PRODUITS[PRODUITS['value'] == produit_code].iloc[0]['label']
    except:
        return ''


pays_declarant = dcc.Dropdown(
    id="pays_declarant",
    clearable=True,
    searchable=True,
    options=COUNTRIES_OPTION,
    #value=68,
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)


pays_partenaires = dcc.Dropdown(
    id="pays_partenaires",
    clearable=True,
    searchable=True,
    multi=True,
    options=COUNTRIES_OPTION,
    #value=106,
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)

produits = dcc.Dropdown(
    id="produits",
    clearable=True,
    searchable=True,
    multi=True,
    options=PRODUITS_OPTION,
    #value="France",
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)



# If the user tries to reach a different page, return a 404 message
SELECTION = html.Div(
    [
        html.Div(
            [
                html.Label('Déclarant'),
                html.Div(
                    pays_declarant,
                    style={'flex': '1 1 0px'}
                ),
                html.Div(
                    pays_partenaires,
                    style={'flex': '1 1 0px'}
                ),
                html.Div(
                    produits,
                    style={'flex': '1 1 0px'}
                ),
            ],
            style={
                'display': 'flex',
            }
        ),


        html.Div(
            [
                # dcc.Checklist(
                #     ['Import', 'Export', 'Production'],
                #     ['Import', 'Export', 'Production'],
                #     inline=True,
                #     style={'flex': '1 0 0px'}
                # ),
                html.Button(
                    'Go',
                    id='submit-val',
                    n_clicks=0,
                    style={'flex': '0 0 0px'}
                ),
            ],
            style={
                'display': 'flex',
            }
        ),


        html.Hr()
    ],
    className="",

)


if __name__ == "__main__":
    COUNTRIES = cq.get_country_names().rename(columns={ 'Code Pays': 'value', 'Pays': 'label' })
    #
    print(COUNTRIES)

    print(get_countrie_by_code(68))

    #print(api.get_reference_as_option('pays', encoding='iso-8859-1'))
