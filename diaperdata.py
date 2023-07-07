from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.io as pio

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
df.loc[(df['DiaperBankName'] == 'Emergency Infant Services'), 'State'] = 'OK'

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
regions = df["CensusRegion"].sort_values().unique()

app = Dash(__name__, external_stylesheets=["/assets/style.css"])

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Diaper Bank Data', style={'textAlign':'center'}),
        html.Label(['Select Variable:'], style={'font-weight': 'bold', "text-align": "center"}),
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Dropdown(id='variable',
                options=[
                {'label': 'Average Number of Kids in Diapers', 'value': "NumKidsDiapers"},
                {'label': 'Proportion of Households with a Single Head of Household', 'value': "NumAdults"},
                {'label': 'Average Household Income in 2020', 'value': "Income_2020"}],
                placeholder="Select Variable",
                value="NumKidsDiapers",
                clearable=False,
                className="dropdown",
                style={"width": "55%"},
                optionHeight=40
                )],
        style={'width': '60%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(id='state',
                options=states,
                placeholder="Select State",
                clearable=True,
                className="dropdown",
                style={"width": "55%"},
                optionHeight=40
                ),
    ],
    style={'width': '40%', 'float': 'middle', 'display': 'inline-block'}),
    html.Br(),
    dcc.Graph(id='graph2-content'),
    ]),
    html.Div([
    html.Br(),
    html.Label(['Select Region:'], style={'font-weight': 'bold', "text-align": "center"}),
    html.Br(),
    html.Br(),
    dcc.Dropdown(regions, id='dropdown-selection',
                    placeholder="Select Region",
                    value="Middle Atlantic",
                    clearable=False,
                    className="dropdown",
                    style={"width": "40%"},
                    optionHeight=40),
        html.Br(),
        dcc.Graph(id='graph-content'),
        html.Br(),
        dcc.Graph(id='graph3-content'),
    ])
])

@callback(
   Output('graph-content', 'figure'),
   Input('dropdown-selection', 'value'))

def update_graph(value):
    transport = df[["CensusRegion", "DB_Transport"]]
    dff = transport[transport.CensusRegion == value]
    fig = px.histogram(dff, x="DB_Transport",
                        category_orders={"DB_Transport": ["Drove Self", "Got a Ride", "Walk",
                                                          "Public Transportation", "Taxi/Ride Sharing App"]},
                        labels={
                            "DB_Transport": "Method",
                            "count": "Count"},
                        template='plotly_white',
                        title="How diaper bank recipients access their diaper bank")\
                        .update_layout(yaxis_title="Count")
    fig.update_traces(marker_color='#86bce8')
    return fig

@callback(
   Output('graph3-content', 'figure'),
   Input('dropdown-selection', 'value'))

def update_graph(value):
    transport = df[["CensusRegion", "DB_Transport"]]
    dff = transport[transport.CensusRegion == value]
    dff = dff.dropna()
    return px.pie(dff, names="DB_Transport",
                  category_orders={"DB_Transport": ["Drove Self", "Got a Ride", "Walk",
                                                    "Public Transportation", "Taxi/Ride Sharing App"]},
                  labels={"DB_Transport": "Method"})

@callback(
   Output('graph2-content', 'figure'),
   Input('variable', 'value'),
   Input('state', 'value'))

def display_choropleth(variable, state):
    if str(variable) == "NumKidsDiapers":
        dff = df[['State', str(variable)]].groupby(['State']).mean().reset_index()
        dff = dff.loc[(dff['State'] == str(state))]
        return px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='NumKidsDiapers',
                            labels={"NumKidsDiapers": "# of Kids"},
                            title = 'Average number of kids in diapers (per household)',
                            scope="usa",
                            hover_data=['State', 'NumKidsDiapers'],
                            color_continuous_scale='ice_r')
    if str(variable) == "NumAdults":
        dff = df[['State', 'NumAdults']]
        dff.loc[(dff['NumAdults'] == 1), 'Single Household'] = 'Yes'
        dff.loc[(dff['NumAdults'] != 1), 'Single Household'] = 'No'
        dff = dff[['State', 'Single Household']].groupby('State').value_counts(normalize=True).to_frame(name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Single Household'] == 'Yes']
        dff = dff[['State', 'Proportion of Households']]
        dff = dff.loc[(dff['State'] == str(state))]
        return px.choropleth(dff, locations='State',
                      locationmode="USA-states",
                      color='Proportion of Households',
                      labels={"Proportion of Households": "Proportion of Households"},
                      title='Proportion of households with a single head of household',
                      scope="usa",
                      hover_data=['State', 'Proportion of Households'],
                      color_continuous_scale='ice_r')
    if str(variable) == "Income_2020":
        dff = df.groupby(['State']).mean(numeric_only=True)['Income_2020'].round().to_frame().reset_index()
        dff = dff.loc[(dff['State'] == str(state))]
        dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'])

        return px.choropleth(dff, locations='State',
                      locationmode='USA-states',
                      color='Income_2020',
                      color_discrete_sequence=px.colors.qualitative.Prism,
                      category_orders={"Income_2020": ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                       '30,000-34,999', '35,000-39,999', '40,000-44,999',
                                                       '45,000-49,999', '50,000-59,999', '60,000-69,999',
                                                       '70,000-79,999', '>=80,000']},
                      labels={"Income_2020": "Income Range (in dollars)"},
                      scope="usa",
                      title="Average Household Income in 2020")



if __name__ == '__main__':
    app.run_server(debug=True)
