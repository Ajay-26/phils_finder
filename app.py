import pandas as pd
from dash import Dash, dcc, html, Input, Output, Patch, callback
from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc
from dash import html, Output, Input, callback
import dash_ag_grid as dag
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

candidate_selection = dcc.RadioItems(
    id='candidate',
    options=["Joly", "Coderre", "Bergeron"],
    value="Coderre",
    inline=True,
    style=dict(display=None)
)


@callback(Output("geolocation", "update_now"), Input("update_btn", "n_clicks"))
def update_now(click):
    return True if click and click > 0 else False


@callback(
    Output("text_position", "children"),
    Input("geolocation", "local_date"),
    Input("geolocation", "position"),
)
def display_output(date, pos):
    if pos:
        return html.P(
            f"As of {date} your location was: lat {pos['lat']},lon {pos['lon']}, accuracy {pos['accuracy']} meters",
        )
    return "No position data available"

cx_group = html.Div(
    [
        dmc.CheckboxGroup(
            id="checkbox-group",
            label="Select any/all of the following that apply to you!",
            description="",
            withAsterisk=True,
            mb=10,
            children=dmc.Group(
                [
                    dmc.Checkbox(label="Social", value="social"),
                    dmc.Checkbox(label="Academics", value="academics"),
                    dmc.Checkbox(label="Athletic", value="athletic"),
                    dmc.Checkbox(label="Snack", value="snack"),
                    dmc.Checkbox(label="Nature Lover", value="nature"),
                    dmc.Checkbox(label="Quirky", value="quirky"),
                    dmc.Checkbox(label="Artsy", value="artsy"),
                ],
                mt=10,
            ),
            value=["social", "nature"],
        ),
        dmc.Text(id="checkbox-group-output"),
    ]
)


@callback(
    Output("checkbox-group-output", "children"),
    Input("checkbox-group", "value")
)
def checkbox(value):
    # Creating a Patch object
    # patched_figure = Patch()
    # patched_figure["layout"]["title"]["font"]["color"] = new_color
    # return patched_figure
    return ", ".join(value) if value else None


@app.callback(
    Output("graph", "figure"),
    Input("candidate", "value"))
def display_choropleth(candidate=None):
    df = px.data.election() # replace with your own data source
    # df = pd.
    geojson = px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 6500])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


columnDefs = [
    # Name,Social,Academics,Athletic,Snack,Nature Lover,Quirky,Artsy,Latitude,Longitude,Review,total
    # { 'field': 'direction' },
    { 'field': 'Name' },
    { 'field': 'Social' },
    { 'field': 'Academics' },
    { 'field': 'Athletic' },
    { 'field': 'Snack' },
    { 'field': 'Nature Lover' },
    { 'field': 'Quirky' },
    { 'field': 'Artsy' },
    { 'field': 'Latitude' },
    { 'field': 'Longitude' },
    { 'field': 'Review' },
    { 'field': 'total' },
]
df = pd.read_csv('./updated_df.csv')
grid = dag.AgGrid(
    id="get-started-example-basic",
    rowData=df.to_dict("records"),
    columnDefs=columnDefs,
)

aggrid = html.Div([grid])


app.layout = html.Div([
    html.H2("Phil's Finder"),
    html.H4("Recommended Places of Interest for First Years"),

    candidate_selection,

    cx_group,
    dcc.Graph(id="graph"),

    # Geolocation
    html.Br(),
    html.Br(),
    html.Br(),
    html.Button("Update Position", id="update_btn"),
    dcc.Geolocation(id="geolocation"),
    html.Div(id="text_position"),

    # AG grid
    aggrid,
    html.Br(),
    html.Br(),
    html.Br(),
])

if __name__ == '__main__':
    app.run(debug=True)