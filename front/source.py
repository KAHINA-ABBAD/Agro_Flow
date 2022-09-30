from dash import Input, Output, dcc, html, dash_table


def update_datatable(app, df):

    table = dash_table.DataTable(
        data = df.to_dict('records'),
        columns = [{"name": i, "id": i} for i in df.columns],
        id='dt_source',
        page_size=100,
        fixed_rows={'headers': True},
        style_table={
            'height': '95%',
            'width': '100%',
            'overflowY': 'auto',
            'overflowX': 'auto',
        }
    )

    return table
