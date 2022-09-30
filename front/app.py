from sre_parse import State
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, dash_table
from matplotlib.pyplot import title
import pandas as pd
import plotly.express as px
import sqlalchemy
from front.sankey import get_sankey

from projetressourcesagricoles.data import get_data
import projetressourcesagricoles.commonqueries as cq
from projetressourcesagricoles.params import *


import front.evolution as evl
import front.selection as selection
import front.per_ressource as pr
import front.page_balance as per_balance
import front.per_pays as per_pays

app = dash.Dash(name='Agro Flow', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

test_product_id = 109
evolution = evl.get_history(None, 68, test_product_id)
evolution_bar = evl.get_bar_plot(
    None, area_code=[68],
    partenaires_codes=[16],
    products_codes=test_product_id)
#sankey_fig = sankey.get_sankey()


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("", className="display-4"),
        html.Hr(),
        html.P(
            "Sélection du graphique", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Production mondiale", href="/per_ressource", active="exact"),
                dbc.NavLink("Balance import export", href="/trade", active="exact"),
                dbc.NavLink("Top productions", href="/per_countrie", active="exact"),
                dbc.NavLink("Détails entre 2 pays", href="/evolution", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("chloro_production", component_property='figure'),
    Output("ressource_prod_evolution", component_property='figure'),
    Output("ressource_top_producers", component_property='figure'),
    Output("ressource_evolution_ie", component_property='figure'),
    Input("per_products_produits", "value"),
)
def update_per_product(produits_id):

    p_top_prod = pr.plot_top_producers(produits_id, 2019, 5)
    p_chloro = pr.plot_prod_chloro(produits_id)
    p_evol = pr.plot_prod_evolution(produits_id)
    p_trade_history = pr.plot_transit_evolution(produits_id)

    return p_chloro, p_evol, p_top_prod, p_trade_history


@app.callback(
    Output("per_balance_evolution", component_property='figure'),
    Output("per_balance_trade", component_property='figure'),
    Input("submit-trade", "n_clicks"),
    State("per_balance_pays", "value"),
    State("per_balance_produits", "value"),
    State("per_balance_years", "value"),
)
def update_balance(btn, pays, produits, years):

    df = get_data(pays,CODES_EXPORT_QTES + CODES_IMPORT_QTES + [CODE_PRODUCTION], itemcodes_list=produits)

    evolution = per_balance.Plot_Import_Export_pays(pays, produits, df=df)
    balance = per_balance.get_trade_balance(pays, produits, years, df=df)
    return evolution, balance


@app.callback(
    Output("per_pays_top_products", component_property='figure'),
    Input("submit-pays", "n_clicks"),
    State("per_pays_pays", "value"),
    State("per_pays_year", "value"),
)
def update_pays(btn, pays, year):
    top_plot_product = per_pays.plot_top_products_per_country(pays, year, 10)
    return top_plot_product



@app.callback(
    Output("graph_line_produit_evolution", component_property='figure'),
    Output("graph_bar_import_export_production", component_property='figure'),
    Input('submit-val', 'n_clicks'),
    State("pays_declarant", "value"),
    State("pays_partenaires", "value"),
    State("produits", "value"),
)
def update_ressource(btn, declarant_id, partenaires_id, produits_id):

    import_export_codes = [5607,5608,5609,5610,5622,5907,5908,5909,5910,5922]

    data_df = get_data([declarant_id], '*', partenaires_id, produits_id)
    df_prod = data_df.query(f"`Élément` == 'Production'")
    df_exc  = data_df.query(f"`Code Élément` in {import_export_codes}")
    history = evl.get_history(df_prod, declarant_id, produits_id)
    iep = evl.get_bar_plot(
        df_exc,
        area_code=[declarant_id],
        partenaires_codes=partenaires_id,
        products_codes=produits_id
    )
    return history, iep



@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")


    elif pathname == "/trade":
        return per_balance.per_balance_page(app),


    elif pathname == "/evolution":
        return html.Div(
            [
                selection.SELECTION,
                html.Div(
                    id='content_graphs'
                ),
                dcc.Graph(
                    figure=evolution,
                    id='graph_line_produit_evolution',
                ),
                dcc.Graph(
                    figure=evolution_bar,
                    id='graph_bar_import_export_production',
                ),
            ]
        )

    elif pathname == "/per_countrie":
        return per_pays.page_per_pays(app)

    elif pathname == "/sankey":
        return dcc.Loading(
            id="loading-8",
            type="default",
            children=[
                dcc.Graph(
                    figure=get_sankey(code_pays=68, code_produit=515, annee=2019),
                    id='graph_sankey_produit_evolution',
                ),
            ]
        ),

    elif pathname == "/per_ressource":
        return html.Div([
            html.H2('Evolution de la productions par ressource'),
            html.Hr(),
            pr.per_ressource_page(app)
        ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8000) # (8)
