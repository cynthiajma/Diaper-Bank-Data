from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

#change

df = pd.read_csv("diaperdata.csv",encoding="latin-1")

df['State'] = df['State'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO'])
df['State'] = df['State'].replace([26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 99], ['MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', "Multiple States"])

df.loc[(df['DiaperBankName'] == 'Bare Needs Diaper Bank'), 'State'] = 'TN'
df.loc[(df['DiaperBankName'] == 'Basic Necessities'), 'State'] = 'LA'
df.loc[(df['DiaperBankName'] == 'Cradles to Crayons Philadelphia'), 'State'] = 'PA'
df.loc[(df['DiaperBankName'] == 'Diaper Bank of the Ozarks'), 'State'] = 'MO'
df.loc[(df['DiaperBankName'] == 'Greater Philadelphia Diaper Bank'), 'State'] = 'PA'
df.loc[(df['DiaperBankName'] == 'HappyBottoms'), 'State'] = 'MO'
df.loc[(df['DiaperBankName'] == 'Helping Mamas'), 'State'] = 'GA'
df.loc[(df['DiaperBankName'] == 'Keeping Families Covered'), 'State'] = 'IL'
df.loc[(df['DiaperBankName'] == 'Sweet Cheeks Diaper Bank'), 'State'] = 'OH'
df.loc[(df['DiaperBankName'] == 'Sweet Cheeks Diaper Ministry'), 'State'] = 'TN'
df.loc[(df['DiaperBankName'] == 'The Life House'), 'State'] = 'NE'

df.loc[(df['CensusRegion'] == 1), 'CensusRegion'] = 'Northeast'
df.loc[(df['CensusRegion'] == 2), 'CensusRegion'] = 'Middle Atlantic'
df.loc[(df['CensusRegion'] == 3), 'CensusRegion'] = 'South'
df.loc[(df['CensusRegion'] == 4), 'CensusRegion'] = 'West'

df.loc[(df['DB_Transport'] == 1), 'DB_Transport'] = 'Walk'
df.loc[(df['DB_Transport'] == 2), 'DB_Transport'] = 'Public Transportation'
df.loc[(df['DB_Transport'] == 3), 'DB_Transport'] = 'Drove Self'
df.loc[(df['DB_Transport'] == 4), 'DB_Transport'] = 'Got a Ride'
df.loc[(df['DB_Transport'] == 5), 'DB_Transport'] = 'Taxi/Ride Sharing App'

states = df["State"].sort_values().unique()

app = Dash(__name__)
app.title = "Diaper Bank Household Data"
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
                            placeholder="Select State",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            html.Div(
                    children=dcc.Graph(
                        id="usa_map",
                        figure={}
                    ), #cloropleth map will go in the figure
                    className="map",
                ),
            ],
            className="wrapper",
),
],
)

@callback(
     # Callback has an input and output.Component id says to which thing to output to.
     Output(component_id='usa_map', component_property='figure'),
    [Input(component_id='slct_state', component_property='value')]  # INPUT!
)

def update_graph(option_slctd): #the call-back function to define. Has an argument that connects to an input. Refers
    # to component_property
    print(option_slctd)
    print(type(option_slctd)) #print for good practice

    #container = "The state chosen by user was: {}".format(option_slctd) #container is returned before fig.
    bystate = df[['State', 'NumKidsDiapers']].groupby(['State']).mean()
    bystate = bystate.reset_index()
    #numkiddf = bystate.to_frame().reset_index()

    dff = bystate.copy()
    dff = dff[dff["State"] == option_slctd]

    figure = px.choropleth(dff, locations='State',
                        locationmode="USA-states",
                        color='NumKidsDiapers',
                        labels={"NumKidsDiapers": "# of kids in diapers"},
                        title='num kids diapers title',
                        scope="usa",
                        hover_data=['State', 'NumKidsDiapers'],
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        template='plotly_dark')
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
