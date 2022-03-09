from dash import html, dcc, callback_context
import dash
import dash_bootstrap_components as dbc
from dms_query import *

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

filter_error_file_name = ["ErrorDesc", "ColumnName", "ErrorDate"]

app.layout = html.Div([
    html.Div(
        [
            # dcc.Interval(id='status_table', interval=1000),
            html.Button(id='status_table_update', n_clicks=0, children='Status')
        ]
    ), html.Br(), html.Div(id='table_status'), html.Br(),
    html.Div(
        [
            # dcc.Interval(id='error_table', interval=1000),
            html.Button(id='error_table_update', n_clicks=0, children='Error'),
        ]
    ), html.Br(), html.Div(id='table_error'), html.Br(),

    html.Div(
        [
            html.Button(id='error_table_update_file_name', n_clicks=0, children='Error File Name'),
            dbc.InputGroup([
                dbc.InputGroupText("Format: 'name.csv/json'"),
                dbc.Input(id="input", placeholder="File Name...", type="text"),

            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Format: LIKE, IN or = 'Action'"),
                dbc.Input(id="input_error", placeholder="Action", type="text", value=""),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Format: < ,> or = 'yyyy-mm-dd hh:mm:ss'"),
                dbc.Input(id="input_date", placeholder="Date Time format:yyyy-mm-dd hh:mm:ss", type="text", value=""),

            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Format: LIKE, IN or = 'ColumnName'"),
                dbc.Input(id="input_column", placeholder="Column", type="text", value=""),

            ]),

        ]
    ), html.Div(id='table_error_file_name'),
])


@app.callback(dash.dependencies.Output('table_status', 'children'),
              [dash.dependencies.Input(component_id='status_table_update', component_property='n_clicks')])
def update_graph_scatter(status_table_update):
    df = dms_status_table_message_id()

    return dbc.Table.from_dataframe(
        df,
        hover=True,
        bordered=True,
        striped=True,
        size='sm',
        responsive=True
    )


@app.callback(dash.dependencies.Output('table_error', 'children'),
              [dash.dependencies.Input('error_table_update', 'n_clicks')])
def update_graph_scatter(error_table_update):
    df = dms_error_table()

    return dbc.Table.from_dataframe(
        df,
        hover=True,
        bordered=True,
        striped=True,
        size='sm',
        responsive=True
    )


@app.callback(dash.dependencies.Output('table_error_file_name', 'children'),
              [dash.dependencies.Input('error_table_update_file_name', 'n_clicks'),
               dash.dependencies.Input("input", "value"),
               dash.dependencies.Input("input_error", "value"),
               dash.dependencies.Input("input_date", "value"),
               dash.dependencies.Input("input_column", "value")])
def update_graph_scatter(error_table_update_file_name, value, value1, value2, value3):
    df = dms_error_table_file_name(value, value1, value2, value3)

    return dbc.Table.from_dataframe(
        df,
        hover=True,
        bordered=True,
        striped=True,
        size='sm',
        responsive=True
    )


def run_server():
    app.run_server(debug=True)


run_server()
