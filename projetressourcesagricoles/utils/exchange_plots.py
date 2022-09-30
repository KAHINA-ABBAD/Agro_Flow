import string
from libcst import Raise
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


def explot_country_ressource_year(
    df: pd.DataFrame,
    from_country_name: str,
    to_country_name: str,
    ressource_code: int,
    year: int,
    fig_size: tuple=(15,10),
    ressource_name: str = None,
):


    if ressource_code:
        query = f"`Code Produit (FAO)` == {ressource_code} & `Pays déclarants (ISO)` == '{from_country_name}' & `Pays partenaire (ISO)` == '{to_country_name}' & `Année` == {year}"
        exchange_data = df.query(query)
        ressource_name = exchange_data['Produit'].iloc[0]
    else:
        raise NotImplementedError('Ressource name query not implemented => use product code for now')


    from_country = world.query(f'`name` == "{from_country_name}"').to_crs('EPSG:4326')
    to_country = world.query(f'`name` == "{to_country_name}"').to_crs('EPSG:4326')

    from_country_center = from_country.centroid
    from_country_center = (float(from_country_center.x), float(from_country_center.y))

    to_country_center = to_country.centroid
    to_country_center = (float(to_country_center.x), float(to_country_center.y))


    with plt.style.context(("seaborn", "ggplot")):
        fig, axes = plt.subplots(1, 2, figsize=fig_size)


        from_country.plot( ax=axes[0] )
        to_country.plot( ax=axes[0] )

        arrow = mpatches.FancyArrowPatch(
            from_country_center,
            to_country_center,
            mutation_scale=50,
            color='gold'
        )

        axes[0].add_patch(arrow)
        plt.suptitle(f'Echange {from_country_name} / {to_country_name}\n{ressource_name} in {year}', fontsize=35, color='blue')

    return from_country, to_country, fig
