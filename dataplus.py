import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

# -- Import and clean data (importing csv into pandas)
df = (
    pd.read_csv("dataplus.csv")
)
states = df["State"].sort_values().unique()

# ------------------------------------------------------------------------------
# App layout
app = Dash(__name__, external_stylesheets=['/assets/avocadostyles.css'])
app.title = "Diaper Bank Household Data!"
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Diaper Bank Household Data", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze the behavior of avocado prices and the number"
                        " of avocados sold in the US between 2015 and 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State", className="menu-title"),
                        dcc.Dropdown(
                            id="slct_state",
                            options=[
                                {"label": state, "value": state}
                                for state in states
                            ],
                            value="Alabama",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(id='output_container', children=[]), #something will go in here.
                html.Br(),

            html.Div(
                    children=dcc.Graph(
                        id="usa_map",
                        figure={}), #cloropleth map will go in the figure
                    className="card",
                ),
                    ],
                className="wrapper",
                ),
        ],
)

    #html.Br(),
    #html.Label('Multi-Select Dropdown'),
    #dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                # ['Montréal', 'San Francisco'],
                 #multi=True),

    #html.Div(id='output_container', children=[]), #something will go in here.
    #html.Br(),

    #dcc.Graph(id='usa_map', figure={}) #cloropleth map will go in the figure




# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'), # use component_id and property.
     # Callback has an input and output.Component id says to which thing to output to.
     Output(component_id='usa_map', component_property='figure')],
    [Input(component_id='slct_state', component_property='value')] #INPUT!
)
def update_graph(option_slctd): #the call-back function to define. Has an argument that connects to an input. Refers
    # to component_property
    print(option_slctd)
    print(type(option_slctd)) #print for good practice

    container = "The state chosen by user was: {}".format(option_slctd) #container is returned before fig.

    dff = df.copy()
    dff = dff[dff["State"] == option_slctd] # only take rows with the year the user selected.
    #dff = dff[dff["NumKidsDiapers"] == "Varroa_mites"]  # only want rows with this disease

    # Plotly Express: building a figure.

    fig = px.choropleth(dff, locations='State',
                        locationmode="USA-states",
                        color='Percent of Median Income',
                        labels={"Percent of Median Income": "% of State Income"},
                        title='Median Diaper Bank Household Income as a Percent of Median State Income',
                        scope="usa",
                        hover_data=['State', 'Percent of Median Income'],
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        template='plotly_dark')

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig    #this goes into the output! Two outputs=return 2 things


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
