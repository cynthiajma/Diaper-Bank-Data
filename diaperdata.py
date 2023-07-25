from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

df = pd.read_csv("diaperdata.csv", encoding="latin-1")
acsincome = pd.read_csv("ACS_5year_2021_income.csv")

acsincome.loc[(acsincome['State'] == 'Alabama'), 'State'] = 'AL'
acsincome.loc[(acsincome['State'] == 'Alaska'), 'State'] = 'AK'
acsincome.loc[(acsincome['State'] == 'Arizona'), 'State'] = 'AZ'
acsincome.loc[(acsincome['State'] == 'Arkansas'), 'State'] = 'AR'
acsincome.loc[(acsincome['State'] == 'California'), 'State'] = 'CA'
acsincome.loc[(acsincome['State'] == 'Colorado'), 'State'] = 'CO'
acsincome.loc[(acsincome['State'] == 'Connecticut'), 'State'] = 'CT'
acsincome.loc[(acsincome['State'] == 'Delaware'), 'State'] = 'DE'
acsincome.loc[(acsincome['State'] == 'District of Columbia'), 'State'] = 'DC'
acsincome.loc[(acsincome['State'] == 'Florida'), 'State'] = 'FL'
acsincome.loc[(acsincome['State'] == 'Georgia'), 'State'] = 'GA'
acsincome.loc[(acsincome['State'] == 'Hawaii'), 'State'] = 'HI'
acsincome.loc[(acsincome['State'] == 'Idaho'), 'State'] = 'ID'
acsincome.loc[(acsincome['State'] == 'Illinois'), 'State'] = 'IL'
acsincome.loc[(acsincome['State'] == 'Indiana'), 'State'] = 'IN'
acsincome.loc[(acsincome['State'] == 'Iowa'), 'State'] = 'IA'
acsincome.loc[(acsincome['State'] == 'Kansas'), 'State'] = 'KS'
acsincome.loc[(acsincome['State'] == 'Kentucky'), 'State'] = 'KY'
acsincome.loc[(acsincome['State'] == 'Louisiana'), 'State'] = 'LA'
acsincome.loc[(acsincome['State'] == 'Maine'), 'State'] = 'ME'
acsincome.loc[(acsincome['State'] == 'Maryland'), 'State'] = 'MD'
acsincome.loc[(acsincome['State'] == 'Massachusetts'), 'State'] = 'MA'
acsincome.loc[(acsincome['State'] == 'Michigan'), 'State'] = 'MI'
acsincome.loc[(acsincome['State'] == 'Minnesota'), 'State'] = 'MN'
acsincome.loc[(acsincome['State'] == 'Mississippi'), 'State'] = 'MS'
acsincome.loc[(acsincome['State'] == 'Missouri'), 'State'] = 'MO'
acsincome.loc[(acsincome['State'] == 'Montana'), 'State'] = 'MT'
acsincome.loc[(acsincome['State'] == 'Nebraska'), 'State'] = 'NE'
acsincome.loc[(acsincome['State'] == 'Nevada'), 'State'] = 'NV'
acsincome.loc[(acsincome['State'] == 'New Hampshire'), 'State'] = 'NH'
acsincome.loc[(acsincome['State'] == 'New Jersey'), 'State'] = 'NJ'
acsincome.loc[(acsincome['State'] == 'New Mexico'), 'State'] = 'NM'
acsincome.loc[(acsincome['State'] == 'New York'), 'State'] = 'NY'
acsincome.loc[(acsincome['State'] == 'North Carolina'), 'State'] = 'NC'
acsincome.loc[(acsincome['State'] == 'North Dakota'), 'State'] = 'ND'
acsincome.loc[(acsincome['State'] == 'Ohio'), 'State'] = 'OH'
acsincome.loc[(acsincome['State'] == 'Oklahoma'), 'State'] = 'OK'
acsincome.loc[(acsincome['State'] == 'Oregon'), 'State'] = 'OR'
acsincome.loc[(acsincome['State'] == 'Pennsylvania'), 'State'] = 'PA'
acsincome.loc[(acsincome['State'] == 'Rhode Island'), 'State'] = 'RI'
acsincome.loc[(acsincome['State'] == 'South Carolina'), 'State'] = 'SC'
acsincome.loc[(acsincome['State'] == 'South Dakota'), 'State'] = 'SD'
acsincome.loc[(acsincome['State'] == 'Tennessee'), 'State'] = 'TN'
acsincome.loc[(acsincome['State'] == 'Texas'), 'State'] = 'TX'
acsincome.loc[(acsincome['State'] == 'Utah'), 'State'] = 'UT'
acsincome.loc[(acsincome['State'] == 'Vermont'), 'State'] = 'VT'
acsincome.loc[(acsincome['State'] == 'Virginia'), 'State'] = 'VA'
acsincome.loc[(acsincome['State'] == 'Washington'), 'State'] = 'WA'
acsincome.loc[(acsincome['State'] == 'West Virginia'), 'State'] = 'WV'
acsincome.loc[(acsincome['State'] == 'Wisconsin'), 'State'] = 'WI'
acsincome.loc[(acsincome['State'] == 'Wyoming'), 'State'] = 'WY'

acsincome = acsincome.loc[acsincome["Race"] != 'ALL']
acsincome = acsincome.loc[acsincome["Race"] != 'WHITE']
acsincome = acsincome.loc[acsincome["Race"] != 'SOME OTHER RACE']
acsincome = acsincome.loc[acsincome["State"] != 'United States']

acsincome.loc[(acsincome['Race'] == 'BLACK OR AFRICAN AMERICAN'), 'Race'] = 'Black'
acsincome.loc[(acsincome['Race'] == 'AMERICAN INDIAN AND ALASKA NATIVE'), 'Race'] = 'American Indian or Alaskan Native'
acsincome.loc[(acsincome['Race'] == 'ASIAN'), 'Race'] = 'Asian'
acsincome.loc[(acsincome['Race'] == 'NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER'), 'Race'] = \
    'Native Hawaiian or Pacific Islander'
acsincome.loc[(acsincome['Race'] == 'TWO OR MORE RACES'), 'Race'] = 'Multiracial'
acsincome.loc[(acsincome['Race'] == 'WHITE, NOT HISPANIC OR LATINO'), 'Race'] = 'White'
acsincome.loc[(acsincome['Race'] == 'HISPANIC OR LATINO'), 'Race'] = 'Hispanic'

acsincome = pd.melt(acsincome, id_vars=['State', 'Race'], value_vars=["<16k", "16-20k", "20-25k", "25-30k", "30-35k",
                                                                      "35-40k", "40-45k", "45-50k", "50-60k", "60-70k",
                                                                      "70-80k", "80k+"])

acsincome.loc[(acsincome['variable'] == '<16k'), 'variable'] = '<=15,999'
acsincome.loc[(acsincome['variable'] == '16-20k'), 'variable'] = '16,000-19,999'
acsincome.loc[(acsincome['variable'] == '20-25k'), 'variable'] = '20,000-24,999'
acsincome.loc[(acsincome['variable'] == '25-30k'), 'variable'] = '25,000-29,999'
acsincome.loc[(acsincome['variable'] == '30-35k'), 'variable'] = '30,000-34,999'
acsincome.loc[(acsincome['variable'] == '35-40k'), 'variable'] = '35,000-39,999'
acsincome.loc[(acsincome['variable'] == '40-45k'), 'variable'] = '40,000-44,999'
acsincome.loc[(acsincome['variable'] == '45-50k'), 'variable'] = '45,000-49,999'
acsincome.loc[(acsincome['variable'] == '50-60k'), 'variable'] = '50,000-59,999'
acsincome.loc[(acsincome['variable'] == '60-70k'), 'variable'] = '60,000-69,999'
acsincome.loc[(acsincome['variable'] == '70-80k'), 'variable'] = '70,000-79,999'
acsincome.loc[(acsincome['variable'] == '80k+'), 'variable'] = '>=80,000'

df['State'] = df['State'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                   24, 25], ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
                                             'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
                                             'MO'])
df['State'] = df['State'].replace([26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
                                   47, 48, 49, 50, 99], ['MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
                                                         'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                                                         'VA', 'WA', 'WV', 'WI', 'WY', "Multiple States"])

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
df.loc[(df['PartnerAgencyType'] == "HOMEVISIT"), 'DB_Transport'] = 'Home Visit'

df.loc[(df['Race_PreferNoShare'] == 1), 'Race'] = 'Prefer Not To Share'
df.loc[(df['Race_AIAN'] == 1), 'Race'] = 'American Indian or Alaskan Native'
df.loc[(df['Race_Asian'] == 1), 'Race'] = 'Asian'
df.loc[(df['Race_BlackAA'] == 1), 'Race'] = 'Black'
df.loc[(df['Race_Hispanic'] == 1), 'Race'] = 'Hispanic'
df.loc[(df['Race_NativeHawaiianPI'] == 1), 'Race'] = 'Native Hawaiian or Pacific Islander'
df.loc[(df['Race_White'] == 1), 'Race'] = 'White'
df.loc[(df['Race_MENA'] == 1), 'Race'] = 'Middle Eastern or North African'
df.loc[(df['Race_Multiracial'] == 1), 'Race'] = 'Multiracial'
df.loc[((df[['Race_PreferNoShare', 'Race_AIAN', 'Race_Asian', 'Race_BlackAA', 'Race_Hispanic', 'Race_NativeHawaiianPI',
             'Race_White', 'Race_MENA', 'Race_Multiracial']].sum(axis=1)) > 1), 'Race'] = 'Multiracial'
df.loc[((df[['Race_PreferNoShare', 'Race_AIAN', 'Race_Asian', 'Race_BlackAA', 'Race_Hispanic', 'Race_NativeHawaiianPI',
             'Race_White', 'Race_MENA', 'Race_Multiracial']].sum(axis=1)) == 0), 'Race'] = 'Prefer Not To Share'

df.loc[(df['State'] == 'AL'), 'State_2020_Median'] = 57243
df.loc[(df['State'] == 'CA'), 'State_2020_Median'] = 81278
df.loc[(df['State'] == 'CO'), 'State_2020_Median'] = 87689
df.loc[(df['State'] == 'FL'), 'State_2020_Median'] = 60460
df.loc[(df['State'] == 'GA'), 'State_2020_Median'] = 62033
df.loc[(df['State'] == 'HI'), 'State_2020_Median'] = 84600
df.loc[(df['State'] == 'IA'), 'State_2020_Median'] = 72030
df.loc[(df['State'] == 'IL'), 'State_2020_Median'] = 77805
df.loc[(df['State'] == 'LA'), 'State_2020_Median'] = 53576
df.loc[(df['State'] == 'MD'), 'State_2020_Median'] = 99215
df.loc[(df['State'] == 'ME'), 'State_2020_Median'] = 66667
df.loc[(df['State'] == 'MI'), 'State_2020_Median'] = 67399
df.loc[(df['State'] == 'MO'), 'State_2020_Median'] = 65081
df.loc[(df['State'] == 'MS'), 'State_2020_Median'] = 47242
df.loc[(df['State'] == 'NC'), 'State_2020_Median'] = 63252
df.loc[(df['State'] == 'NE'), 'State_2020_Median'] = 75622
df.loc[(df['State'] == 'NJ'), 'State_2020_Median'] = 89543
df.loc[(df['State'] == 'NV'), 'State_2020_Median'] = 64020
df.loc[(df['State'] == 'NY'), 'State_2020_Median'] = 71865
df.loc[(df['State'] == 'OH'), 'State_2020_Median'] = 63198
df.loc[(df['State'] == 'OK'), 'State_2020_Median'] = 54921
df.loc[(df['State'] == 'PA'), 'State_2020_Median'] = 74094
df.loc[(df['State'] == 'SC'), 'State_2020_Median'] = 63159
df.loc[(df['State'] == 'SD'), 'State_2020_Median'] = 73467
df.loc[(df['State'] == 'TN'), 'State_2020_Median'] = 57542
df.loc[(df['State'] == 'TX'), 'State_2020_Median'] = 71599
df.loc[(df['State'] == 'UT'), 'State_2020_Median'] = 87915
df.loc[(df['State'] == 'WA'), 'State_2020_Median'] = 85157
df.loc[(df['State'] == 'WY'), 'State_2020_Median'] = 68506

df.loc[(df['NumAdults'] == 1), 'Single Household'] = 'Yes'
df.loc[(df['NumAdults'] != 1), 'Single Household'] = 'No'

global percent_inHome

states = df["State"].sort_values().unique()
races = ['American Indian or Alaskan Native', 'Asian', 'Black', 'Hispanic', 'Middle Eastern or North African',
         'Native Hawaiian or Pacific Islander', 'White', 'Multiracial', 'Prefer Not To Share']
singleheaddict = ['Yes', 'No']

filters = {"race": "",
           "state": "",
           "singlehead": ""}

external_stylesheets = ['assets/sarahstyles.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Diaper Bank Household Data"
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Diaper Bank Household Data", className="header-title"),
                html.P(
                    children=(
                        "Hover over on the map, or select filters to start exploring."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div([
                    html.Div([
                    html.Label(['Race'], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id='race',
                        options=races,
                        placeholder="Select Race",
                        clearable=True,
                        searchable=False,
                        className="dropdown",
                     ),
                    ], className='filter'
                ),
                html.Div([
                    html.Label(['State'], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id='state',
                        options=states,
                        placeholder="Select State",
                        clearable=True,
                        searchable=False,
                        className="dropdown"
                     ),
                    ], className='filter'
                ),
                html.Div([
                    html.Label(['Single Head of Household'],
                                className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id='singlehead',
                        options=singleheaddict,
                        placeholder="Select if Single Head of Household",
                        clearable=True,
                        searchable=False,
                        className="dropdown"
                        ),
                    ],  className='filter'
                )
            ],
            className='all_filters'
        ),
        html.Br(),
        html.H3(children="Choropleth", className='subheader-title'),
        html.Div(
            children=[
                html.Div([
                    html.Label(['Category'], className='label'),
                    html.Br(),
                    dcc.Dropdown(id='variable-dropdown',
                            options=[{'label': 'Adults', 'value': 'Adults-value'},
                                    {'label': 'Children', 'value': "Children-value"},
                                    {'label': 'Income', 'value': "Income-value"}
                                    ],
                            placeholder="Select Category",
                            value="Adults-value",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                            )],
                        className='filter2'),
                html.Div([
                    html.Label(["Map Variable"], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id="map-dropdown",
                        options=[],
                        value=None,
                        clearable=False,
                        searchable=False,
                        className="dropdown"
                    ),
                ], className='filter2')], className='map_filters'),
        html.Div([
            dcc.Graph(id='graph2-content'),
            html.H3(children="Additional Information", className='subheader2-title'),
            dcc.Graph(id='graph-content', className='transport'),
            dcc.Graph(id='graph3-content', className='transport'),
            dcc.Graph(id='graph4-content', className='preterm'),
            dcc.Graph(id='graph5-content', className='preterm'),
            dcc.Graph(id='graph8-content', className='childcare'),
            dcc.Graph(id='graph9-content', className='childcare'),
            dcc.Graph(id='graph6-content', className='income'),
            dcc.Graph(id='graph7-content', className='income'),
            dcc.Graph(id='DR-content', className="sankey"),
            dcc.Graph(id='SevDR-content', className="sankey"),
            dcc.Graph(id='UTI-content', className="sankey"),

        ])
        ])
    ])


@callback(
    Output("map-dropdown", "options"),
    Output("map-dropdown", "value"),
    Input("variable-dropdown", "value"))
def update_map_dropdown(optionslctd):
    if optionslctd == "Adults-value":
        options = [{"label": 'Single Head of Household', "value": 'NumAdults'},
                   {"label": 'One or More Working Adult', "value": 'Ad1CurrentWork'},
                   {"label": 'One or More Adult in Education or Job Training',
                    "value": 'Ad1_School'}]
        value = "NumAdults"
    elif optionslctd == "Income-value":
        options = [{'label': 'Average Household Income in 2019', 'value': 'Income_2019'},
                   {'label': 'Average Household Income in 2020', 'value': 'Income_2020'},
                   {'label': 'Median Income of Households Relative to their State\'s 2020 Median Income',
                    "value": 'Income_2020_2'}]
        value = "Income_2019"
    elif optionslctd == "Children-value":
        options = [{"label": 'Average Number of Children in Diapers (per household)', "value": 'NumKidsDiapers'},
                   {"label": 'Average Number of Children in Childcare (per household)', "value": 'AnyCareforCHILD1_C'}]
        value = "NumKidsDiapers"
    else:
        options = []
        value = None
    return options, value


@callback(
    Output('graph-content', 'figure'),
    Input('state', 'value'),
    Input('race', 'value'),
    Input('singlehead', 'value'))
def update_graph(state, race, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff = dff[["DB_Transport"]]
    dff = dff.sort_values('DB_Transport')
    fig = px.histogram(dff, x="DB_Transport",
                       labels={
                           "DB_Transport": "Method",
                           "count": "Count"},
                       template='plotly_white',
                       title="How Diaper Bank Recipients Access Diaper Bank Products<br><sup>You have selected "
                             + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                             + " for single head household.",
                       category_orders={"DB_Transport": ["Drove Self", "Got a Ride", "Public Transportation",
                                                         "Taxi/Ride Sharing App", "Walk", "Home Visit"
                                                         ]}
                       )
    fig.update_layout(yaxis_title="Count")
    fig.update_traces(marker_color='#86bce8')
    return fig


@callback(
    Output('graph3-content', 'figure'),
    Input('state', 'value'),
    Input('race', 'value'),
    Input('singlehead', 'value'))
def update_pie(state, race, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff = dff[["DB_Transport"]]
    dff = dff.dropna()
    fig = px.pie(dff, names="DB_Transport",
                 category_orders={"DB_Transport": ["Drove Self", "Got a Ride", "Public Transportation",
                                                   "Taxi/Ride Sharing App", "Walk", "Home Visit"
                                                   ]},
                 labels={"DB_Transport": "Method"},
                 template='plotly_white',
                 color_discrete_sequence=px.colors.sequential.RdBu_r
                 )
    rows = dff.shape[0]
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.19,
        xref='paper',
        yref='paper',
        text=f'Filters matched to {rows} responses.',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph4-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def update_bar(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff = dff[
        ['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm', 'CH7Preterm', 'CH8Preterm',
         'Race']]
    dff = dff.dropna(how='all')
    rows = dff.shape[0]
    dfff = dff.replace(np.nan, 0)
    dfff = dfff.replace(2, 1)
    dfff['Total Children'] = dfff[
        ['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm', 'CH7Preterm',
         'CH8Preterm']].sum(axis=1)
    dfff = dfff[['Race', 'Total Children']].groupby(['Race']).sum('Total Children').reset_index()
    dfff['Total Children'] = dfff['Total Children'].astype(int)
    dff = dff.replace(np.nan, 0)
    dff = dff.replace(2, 0)
    dff['Sum'] = dff[['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm', 'CH7Preterm',
                      'CH8Preterm']].sum(axis=1)
    dff = dff[['Race', 'Sum']].groupby('Race').sum().astype(int).reset_index()
    dff = dff.merge(dfff)
    dff['Preterm'] = dff['Sum'] / dff['Total Children'] * 100
    dff['Term'] = 100 - dff['Preterm']
    dff = dff.drop(['Sum', 'Total Children'], axis=1)
    dff = dff.sort_values(by='Preterm')
    fig = px.bar(dff, y='Race', x=['Preterm', 'Term'],
                 template='plotly_white',
                 color_discrete_map={
                     "Preterm": "#e81e36",
                     "Term": "#86bce8"},
                 labels={"variable": "Preterm or Term",
                         "value": "Percent"},
                 title="Distribution of Preterm vs Term Babies by Race or Ethnic Identity<br><sup>You have selected "
                       + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                       + " for single head household.",
                 barmode='stack')
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.25,
        xref='paper',
        yref='paper',
        text=f'Filters matched to {rows} responses.',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph5-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def update_pie(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff = dff[
        ['CH1HaveRashBefore', 'CH1HaveRashAfter', 'CH1HaveSevRashBefore', 'CH1HaveSevRashAfter', 'CH1HaveUTIBefore',
         'CH1HaveUTIAfter', 'CH2HaveRashBefore', 'CH2HaveRashAfter', 'CH2HaveSevRashBefore', 'CH2HaveSevRashAfter',
         'CH2HaveUTIBefore', 'CH2HaveUTIAfter']]
    dff = dff.replace(2, 0)
    dff1 = dff[
        ['CH1HaveRashBefore', 'CH1HaveRashAfter', 'CH1HaveSevRashBefore', 'CH1HaveSevRashAfter', 'CH1HaveUTIBefore',
         'CH1HaveUTIAfter']]
    dff1 = dff1.dropna(how='all')
    dff1['CH1BeforeSum'] = dff1[['CH1HaveRashBefore', 'CH1HaveSevRashBefore', 'CH1HaveUTIBefore']].sum(axis=1)
    dff1['CH1AfterSum'] = dff1[['CH1HaveRashAfter', 'CH1HaveSevRashAfter', 'CH1HaveUTIAfter']].sum(axis=1)
    dff2 = dff[
        ['CH2HaveRashBefore', 'CH2HaveRashAfter', 'CH2HaveSevRashBefore', 'CH2HaveSevRashAfter', 'CH2HaveUTIBefore',
         'CH2HaveUTIAfter']]
    dff2 = dff2.dropna(how='all')
    rows = dff1.shape[0] + dff2.shape[0]
    dff2['CH2BeforeSum'] = dff2[['CH2HaveRashBefore', 'CH2HaveSevRashBefore', 'CH2HaveUTIBefore']].sum(axis=1)
    dff2['CH2AfterSum'] = dff2[['CH2HaveRashAfter', 'CH2HaveSevRashAfter', 'CH2HaveUTIAfter']].sum(axis=1)
    if dff1.shape[0] != 0:
        dff1.loc[(dff1['CH1BeforeSum'] > 0), 'Ch1BeforeSum'] = 1.0
        dff1.loc[(dff1['CH1AfterSum'] > 0), 'Ch1AfterSum'] = 1.0
    if dff2.shape[0] != 0:
        dff2.loc[(dff2['CH2BeforeSum'] > 0), 'Ch2BeforeSum'] = 1.0
        dff2.loc[(dff2['CH2AfterSum'] > 0), 'Ch2AfterSum'] = 1.0
    dff1 = dff1.replace(np.nan, 0)
    dff2 = dff2.replace(np.nan, 0)
    if dff1.shape[0] != 0:
        dff1.loc[(dff1['Ch1BeforeSum'] == 1) & (dff1['Ch1AfterSum'] == 0), 'Outcome'] = 'No more diaper related illness'
        dff1.loc[(dff1['Ch1BeforeSum'] == 0) & (dff1['Ch1AfterSum'] == 0), 'Outcome'] = 'No diaper related illness'
        dff1.loc[
            (dff1['Ch1BeforeSum'] == 1) & (dff1['Ch1AfterSum'] == 1), 'Outcome'] = 'Still got diaper related illness'
        dff1.loc[(dff1['Ch1BeforeSum'] == 0) & (dff1['Ch1AfterSum'] == 1), 'Outcome'] = 'Got diaper related illness'
    if dff2.shape[0] != 0:
        dff2.loc[(dff2['Ch2BeforeSum'] == 1) & (dff2['Ch2AfterSum'] == 0), 'Outcome'] = 'No more diaper related illness'
        dff2.loc[(dff2['Ch2BeforeSum'] == 0) & (dff2['Ch2AfterSum'] == 0), 'Outcome'] = 'No diaper related illness'
        dff2.loc[
            (dff2['Ch2BeforeSum'] == 1) & (dff2['Ch2AfterSum'] == 1), 'Outcome'] = 'Still got diaper related illness'
        dff2.loc[(dff2['Ch2BeforeSum'] == 0) & (dff2['Ch2AfterSum'] == 1), 'Outcome'] = 'Got diaper related illness'
    if (dff1.shape[0] != 0) & (dff2.shape[0] != 0):
        dff1 = dff1[['Outcome']]
        dff2 = dff2[['Outcome']]
        dff1 = dff1.value_counts()
        dff2 = dff2.value_counts()
        dff = dff1 + dff2
    elif dff1.shape[0] == 0:
        dff = dff2.value_counts()
    elif dff2.shape[0] == 0:
        dff = dff1.value_counts()
    dff = dff.to_frame('Number of Children')
    dff = dff.reset_index()
    dff['Outcome'] = dff['Outcome'].astype('str')
    dff['Number of Children'] = dff['Number of Children'].astype(float).fillna(0).astype(int)
    fig = px.pie(dff, names="Outcome", values="Number of Children",
                 labels={"Outcome": "Outcome"},
                 template='plotly_white',
                 color_discrete_sequence=px.colors.sequential.RdBu_r,
                 title="Distribution of diaper related illnesses among children after receiving diapers"
                 "<br><sup>You have selected "
                 + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                 + " for single head household.",
                 )
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.3,
        xref='paper',
        yref='paper',
        text=f'Filters matched to {rows} responses.',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph6-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def update_pie(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    filters["race"] = race if race else ""
    acs = acsincome.loc[(acsincome['Race']) == filters["race"]] if filters["race"] else acsincome
    filters["state"] = state if state else ""
    acs = acs.loc[(acsincome['State']) == filters["state"]] if filters["state"] else acs

    rows = dff.shape[0] + acs.shape[0]
    dff['Income_2019'] = dff['Income_2019'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                    ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                     '30,000-34,999', '35,000-39,999', '40,000-44,999', '45,000-49,999',
                                                     '50,000-59,999', '60,000-69,999', '70,000-79,999', '>=80,000'])
    dff = dff['Income_2019'].value_counts(normalize=True)
    dff = dff.to_frame('Proportion').rename_axis('Income Range').reset_index()
    dff['Percentage'] = dff['Proportion'] * 100
    acs = acs.groupby('variable').sum(numeric_only=True)
    acs['Percentage'] = acs['value'] / acs['value'].sum() * 100
    acs = acs.rename_axis('Income Range').reset_index()
    acs['Type'] = 'National Data'
    dff['Type'] = 'Diaper Bank Recipient'

    dff = dff[['Income Range', 'Percentage', 'Type']]
    acs = acs[['Income Range', 'Percentage', 'Type']]

    acsdff = pd.concat([acs, dff])

    fig = px.histogram(acsdff, x='Income Range', y='Percentage', color='Type',
                       labels={"Income Range": "Income Range (in dollars)"},
                       category_orders={"Income Range": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                         '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000']},
                       title="Distribution of Household Incomes in 2019<br><sup>You have selected "
                             + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                             + " for single head household.",
                       template='plotly_white')
    fig.update_layout(yaxis_title="Percentage")
    fig.update_traces(hovertemplate="Income Range: $%{x}<br>Percentage: %{y}%")
    fig.update_layout(barmode='overlay', bargap=0, bargroupgap=0)
    fig.update_traces(opacity=0.40)
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.3,
        xref='paper',
        yref='paper',
        text=f'Filters matched to {rows} responses.',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph7-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def update_pie(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    filters["race"] = race if race else ""
    acs = acsincome.loc[(acsincome['Race']) == filters["race"]] if filters["race"] else acsincome
    filters["state"] = state if state else ""
    acs = acs.loc[(acsincome['State']) == filters["state"]] if filters["state"] else acs

    rows = dff.shape[0] + acs.shape[0]
    dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                    ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                     '30,000-34,999', '35,000-39,999', '40,000-44,999', '45,000-49,999',
                                                     '50,000-59,999', '60,000-69,999', '70,000-79,999', '>=80,000'])
    dff = dff['Income_2020'].value_counts(normalize=True)
    dff = dff.to_frame('Proportion').rename_axis('Income Range').reset_index()
    dff['Percentage'] = dff['Proportion'] * 100
    acs = acs.groupby('variable').sum(numeric_only=True)
    acs['Percentage'] = acs['value'] / acs['value'].sum() * 100
    acs = acs.rename_axis('Income Range').reset_index()
    acs['Type'] = 'National Data'
    dff['Type'] = 'Diaper Bank Recipient'

    dff = dff[['Income Range', 'Percentage', 'Type']]
    acs = acs[['Income Range', 'Percentage', 'Type']]

    acsdff = pd.concat([acs, dff])

    fig = px.histogram(acsdff, x='Income Range', y='Percentage', color='Type',
                       labels={"Income Range": "Income Range (in dollars)"},
                       category_orders={"Income Range": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                         '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000']},
                       title="Distribution of Household Incomes in 2020<br><sup>You have selected "
                             + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                             + " for single head household.",
                       template='plotly_white')
    fig.update_layout(yaxis_title="Percentage")
    fig.update_traces(hovertemplate="Income Range: $%{x}<br>Percentage: %{y}%")
    fig.update_layout(barmode='overlay', bargap=0, bargroupgap=0)
    fig.update_traces(opacity=0.40)
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.25,
        xref='paper',
        yref='paper',
        text=f'Filters matched to {rows} responses.',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph8-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def childcare_pie1(race, state, singlehead):
    global percent_inHome
    percent_inHome = 24.7
    filters['race'] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    dff = dff[['NoChildCare']].dropna()
    dff = dff.replace(np.nan, 0)
    dff = dff.replace(1, 0)
    dff = dff.replace(2, 0)
    dff = dff.replace(0, 'No Outside Childcare')
    dff = dff.replace(9, 'Outside Childcare')
    rows = dff.shape[0]
    dff = dff.value_counts().to_frame("Number of Households").reset_index()

    percent_inHome = round(
        (dff['Number of Households'].iloc[1] / (dff['Number of Households'].iloc[0] +
                                                dff['Number of Households'].iloc[1])) * 100, 1)

    fig = px.pie(dff, names="NoChildCare", values="Number of Households",
                 labels={'NoChildCare': 'Childcare Type'},
                 template="plotly_white",
                 color_discrete_sequence=px.colors.sequential.RdBu_r,
                 title="Percent of Households that use Outside Childcare<br><sup>You have selected "
                       + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                       + " for single head household.",
                 category_orders={"NoChildCare": ['Outside Childcare', 'No Outside Childcare']})
    fig.update_traces(pull=[0.05, 0])
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.19,
        xref='paper',
        yref='paper',
        text=f'Filters match to {rows} responses.',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph9-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def childcare_pie2(race, state, singlehead):
    global percent_inHome
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff = dff[['NoChildCare', 'CH1ChildCare_DiapersRequired_C', 'CH2ChildCare_DiapersRequired_C']]

    dff = dff.loc[(dff['NoChildCare'] == 9)]

    dff.dropna(how='all')
    dff = dff.replace(2, 0)
    dff = dff.replace(np.nan, 0)

    dff['Sum'] = dff['CH1ChildCare_DiapersRequired_C'] + dff['CH2ChildCare_DiapersRequired_C']

    dff.loc[(dff['Sum'] >= 1), 'Diaper Required'] = 'Diapers Required'
    dff.loc[(dff['Sum'] == 0), 'Diaper Required'] = 'No Diapers Required'

    nrows = dff.shape[0]

    dff = dff['Diaper Required'].value_counts().to_frame("Number of Households").rename_axis(
        'Diaper Required').reset_index()

    fig = px.pie(dff, names="Diaper Required", values="Number of Households",
                 category_orders={"Diaper Required": ['Diapers Required', 'No Diapers Required']},
                 labels={'Diaper Required': 'Diaper Requirement'},
                 template="plotly_white",
                 color_discrete_sequence=px.colors.sequential.RdBu_r,
                 title=f"Of the {percent_inHome}% that Use Childcare Outside of Home:<br><sup>You have selected "
                       + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                       + " for single head household.")
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.19,
        xref='paper',
        yref='paper',
        text=f'Filters match to {nrows} responses.',
        showarrow=False,
    )])
    return fig


@callback(
   Output('DR-content', 'figure'),
   [Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def update_illness1(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    dff['NumbKidsPositivelyImpacted_DR'] = 0
    dff.loc[((dff['CH1HaveRashBefore']) == 1) & (dff['CH1HaveRashAfter'] == 2), 'NumbKidsPositivelyImpacted_DR'] = dff['NumbKidsPositivelyImpacted_DR'] + 1
    dff.loc[((dff['CH2HaveRashBefore']) == 1) & (dff['CH2HaveRashAfter'] == 2), 'NumbKidsPositivelyImpacted_DR'] = dff['NumbKidsPositivelyImpacted_DR'] + 1

    dff['NumbKidsNegativelyImpacted_DR'] = 0
    dff.loc[((dff['CH1HaveRashBefore']) == 2) & (dff['CH1HaveRashAfter'] == 1), 'NumbKidsNegativelyImpacted_DR'] = dff['NumbKidsNegativelyImpacted_DR'] + 1
    dff.loc[((dff['CH2HaveRashBefore']) == 2) & (dff['CH2HaveRashAfter'] == 1), 'NumbKidsNegativelyImpacted_DR'] = dff['NumbKidsNegativelyImpacted_DR'] + 1

    dff['NumbKidsUnaffected_DR'] = 0
    dff.loc[((dff['CH1HaveRashBefore'])) == 1 & (dff['CH1HaveRashAfter'] == 1), 'NumbKidsUnaffected_DR'] = dff['NumbKidsUnaffected_DR'] + 1
    dff.loc[((dff['CH2HaveRashBefore'])) == 1 & (dff['CH2HaveRashAfter'] == 1), 'NumbKidsUnaffected_DR'] = dff['NumbKidsUnaffected_DR'] + 1

    nodes = [{'label': ''}, {'label': 'Positively Impacted'}, {'label': 'Unaffected'}, {'label': 'Negatively Impacted'}]
    links = [{'source': 0, 'target': 1, 'value': dff['NumbKidsPositivelyImpacted_DR'].sum()}
        , {'source': 0, 'target': 2, 'value': dff['NumbKidsUnaffected_DR'].sum()}
        , {'source': 0, 'target': 3, 'value': dff['NumbKidsNegativelyImpacted_DR'].sum()}]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=[node['label'] for node in nodes]
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
        )
    )])
    fig.update_layout(title_text='Effect of Diapers on Diaper Rash')
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.25,
        xref='paper',
        yref='paper',
        showarrow=False
    )])
    return fig

@callback(
   Output('SevDR-content', 'figure'),
   [Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def update_illness1(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    dff['NumbKidsPositivelyImpacted_SevDR'] = 0
    dff.loc[((dff['CH1HaveSevRashBefore']) == 1) & (dff['CH1HaveSevRashAfter'] == 2), 'NumbKidsPositivelyImpacted_SevDR'] = dff['NumbKidsPositivelyImpacted_SevDR'] + 1
    dff.loc[((dff['CH2HaveSevRashBefore']) == 1) & (dff['CH2HaveSevRashAfter'] == 2), 'NumbKidsPositivelyImpacted_SevDR'] = dff['NumbKidsPositivelyImpacted_SevDR'] + 1

    dff['NumbKidsNegativelyImpacted_SevDR'] = 0
    dff.loc[((dff['CH1HaveSevRashBefore']) == 2) & (dff['CH1HaveSevRashAfter'] == 1), 'NumbKidsNegativelyImpacted_SevDR'] = dff['NumbKidsNegativelyImpacted_SevDR'] + 1
    dff.loc[((dff['CH2HaveSevRashBefore']) == 2) & (dff['CH2HaveSevRashAfter'] == 1), 'NumbKidsNegativelyImpacted_SevDR'] = dff['NumbKidsNegativelyImpacted_SevDR'] + 1

    dff['NumbKidsUnaffected_SevDR'] = 0
    dff.loc[((dff['CH1HaveSevRashBefore'])) == 1 & (dff['CH1HaveSevRashAfter'] == 1), 'NumbKidsUnaffected_SevDR'] = dff['NumbKidsUnaffected_SevDR'] + 1
    dff.loc[((dff['CH2HaveSevRashBefore'])) == 1 & (dff['CH2HaveSevRashAfter'] == 1), 'NumbKidsUnaffected_SevDR'] = dff['NumbKidsUnaffected_SevDR'] + 1

    nodes = [{'label': ''}, {'label': 'Positively Impacted'}, {'label': 'Unaffected'}, {'label': 'Negatively Impacted'}]
    links = [{'source': 0, 'target': 1, 'value': dff['NumbKidsPositivelyImpacted_SevDR'].sum()}
        , {'source': 0, 'target': 2, 'value': dff['NumbKidsUnaffected_SevDR'].sum()}
        , {'source': 0, 'target': 3, 'value': dff['NumbKidsNegativelyImpacted_SevDR'].sum()}]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=[node['label'] for node in nodes]
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
        )
    )])
    fig.update_layout(title_text='Effect of Diapers on Severe Diaper Rash')
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.25,
        xref='paper',
        yref='paper',
        showarrow=False
    )])
    return fig

@callback(
   Output('UTI-content', 'figure'),
   [Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def update_illness2(race, state, singlehead):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    dff['NumbKidsPositivelyImpacted_UTI'] = 0
    dff.loc[((dff['CH1HaveUTIBefore']) == 1) & (dff['CH1HaveUTIAfter'] == 2), 'NumbKidsPositivelyImpacted_UTI'] = dff['NumbKidsPositivelyImpacted_UTI'] + 1
    dff.loc[((dff['CH2HaveUTIBefore']) == 1) & (dff['CH2HaveUTIAfter'] == 2), 'NumbKidsPositivelyImpacted_UTI'] = dff['NumbKidsPositivelyImpacted_UTI'] + 1

    dff['NumbKidsNegativelyImpacted_UTI'] = 0
    dff.loc[((dff['CH1HaveUTIBefore']) == 2) & (dff['CH1HaveUTIAfter'] == 1), 'NumbKidsNegativelyImpacted_UTI'] = dff['NumbKidsNegativelyImpacted_UTI'] + 1
    dff.loc[((dff['CH2HaveUTIBefore']) == 2) & (dff['CH2HaveUTIAfter'] == 1), 'NumbKidsNegativelyImpacted_UTI'] = dff['NumbKidsNegativelyImpacted_UTI'] + 1

    dff['NumbKidsUnaffected_UTI'] = 0
    dff.loc[((dff['CH1HaveUTIBefore'])) == 1 & (dff['CH1HaveUTIAfter'] == 1), 'NumbKidsUnaffected_UTI'] = dff['NumbKidsUnaffected_UTI'] + 1
    dff.loc[((dff['CH2HaveUTIBefore'])) == 1 & (dff['CH2HaveUTIAfter'] == 1), 'NumbKidsUnaffected_UTI'] = dff['NumbKidsUnaffected_UTI'] + 1

    nodes = [{'label': ''}, {'label': 'Positively Impacted'}, {'label': 'Unaffected'}, {'label': 'Negatively Impacted'}]
    links = [{'source': 0, 'target': 1, 'value': dff['NumbKidsPositivelyImpacted_UTI'].sum()}
        , {'source': 0, 'target': 2, 'value': dff['NumbKidsUnaffected_UTI'].sum()}
        , {'source': 0, 'target': 3, 'value': dff['NumbKidsNegativelyImpacted_UTI'].sum()}]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=[node['label'] for node in nodes]
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
        )
    )])
    fig.update_layout(title_text='Effect of Diapers on UTIs')
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.25,
        xref='paper',
        yref='paper',
        showarrow=False
    )])
    return fig


@callback(
    Output('graph2-content', 'figure'),
    [Input('map-dropdown', 'value'),
     Input('race', 'value'),
     Input('singlehead', 'value'),
     Input('state', 'value')])
def display_choropleth(variable, race, singlehead, state):
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    if str(variable) == "NumKidsDiapers":
        dff = dff[['State', str(variable)]]
        rows = dff.shape[0]
        dff = dff.groupby(['State']).median(numeric_only=True).reset_index()
        fig = px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='NumKidsDiapers',
                            labels={"NumKidsDiapers": "# of Children"},
                            title='Average Number of Children in Diapers (per household)<br><sup>You have selected '
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.",
                            scope="usa",
                            hover_data=['State', 'NumKidsDiapers'],
                            color_continuous_scale='ice_r')
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == "NumAdults":
        dff = dff[['State', 'Single Household']]
        rows = dff.shape[0]
        dff = dff.groupby('State').value_counts(normalize=True) \
            .to_frame(name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Single Household'] == 'Yes']
        dff = dff[['State', 'Proportion of Households']]
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100

        fig = px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='Percentage of Households',
                            labels={"Percentage of Households": "% of Households"},
                            title='Percentage of Households with a Single Head of Household<br><sup>You have selected '
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.",
                            scope="usa",
                            hover_data=['State', 'Percentage of Households'],
                            color_continuous_scale='ice_r')
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == 'Income_2020':
        dff = dff[['State', 'Income_2020']]
        rows = dff.shape[0]
        dff.dropna(subset=['Income_2020'])
        dff['Income_2020'] = dff['Income_2020'].replace(
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'],
                                                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        dff = dff.groupby(['State']).median(numeric_only=True)
        dff = dff['Income_2020'].round().to_frame().reset_index()
        dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'])
        fig = px.choropleth(dff, locations='State',
                            locationmode='USA-states',
                            color='Income_2020',
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            category_orders={"Income_2020": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                             '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                             '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                             '60,000-69,999', '70,000-79,999', '>=80,000']},
                            labels={"Income_2020": "Income Range (in dollars)"},
                            scope="usa",
                            title="Median Household Income in 2020<br><sup>You have selected "
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.")
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == 'Income_2019':
        dff = dff[['State', 'Income_2019']]
        rows = dff.shape[0]
        dff = dff.dropna(subset=['Income_2019'])
        dff['Income_2019'] = dff['Income_2019'].replace(
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'],
                                                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        dff = dff.groupby(['State']).median(numeric_only=True)['Income_2019'].round().to_frame().reset_index()
        dff['Income_2019'] = dff['Income_2019'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'])
        fig = px.choropleth(dff, locations='State',
                            locationmode='USA-states',
                            color='Income_2019',
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            category_orders={"Income_2019": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                             '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                             '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                             '60,000-69,999', '70,000-79,999', '>=80,000']},
                            labels={"Income_2019": "Income Range (in dollars)"},
                            scope="usa",
                            title="Median Household Income in 2019<br><sup>You have selected "
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.")
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == "Ad1CurrentWork":
        dff = dff[['State', 'Ad1CurrentWork', 'Ad2CurrentWork']]
        dff = dff.dropna(how='all')
        dff = dff.replace(2, 0)
        dff = dff.replace(np.nan, 0)
        rows = dff.shape[0]
        dff['Sum'] = dff['Ad1CurrentWork'] + dff['Ad2CurrentWork']
        dff.loc[(dff['Sum'] >= 1), '1+ Adult Working'] = 'Yes'
        dff.loc[(dff['Sum'] == 0), '1+ Adult Working'] = 'No'
        dff = dff[['State', '1+ Adult Working']].groupby('State').value_counts(normalize=True).to_frame(
            name='Proportion of Households').reset_index()
        dff = dff.loc[dff['1+ Adult Working'] == 'Yes']
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        fig = px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='Percentage of Households',
                            labels={"Percentage of Households": "% of Households"},
                            title='Percentage of Households with One or More Working Adult<br><sup>You have selected '
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.",
                            scope="usa",
                            hover_data=['State', 'Percentage of Households'],
                            color_continuous_scale='ice_r')
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == "Ad1_School":
        dff = dff[['State', 'Ad1_School', 'Ad2_School']]
        dff = dff.dropna(how='all')
        dff = dff.replace(2, 0)
        dff = dff.replace(np.nan, 0)
        dff['Sum'] = dff['Ad1_School'] + dff['Ad2_School']
        dff.loc[(dff['Sum'] >= 1), 'Education or Job Training'] = 'Yes'
        dff.loc[(dff['Sum'] == 0), 'Education or Job Training'] = 'No'
        rows = dff.shape[0]
        dff = dff[['State', 'Education or Job Training']].groupby('State').value_counts(normalize=True).to_frame(
            name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Education or Job Training'] == 'Yes']
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        fig = px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='Percentage of Households',
                            labels={"Percentage of Households": "% of Households"},
                            title='Percentage of Households with One or More Adult in Education or Job Training'
                            '<br><sup>You have selected '
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.",
                            scope="usa",
                            hover_data=['State', 'Percentage of Households'],
                            color_continuous_scale='ice_r')
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == "AnyCareforCHILD1_C":
        dff = dff[['State', 'AnyCareforCHILD1_C', 'AnyCareforCHILD2_C']]
        dff = dff.loc[(dff["AnyCareforCHILD1_C"] != 99) | (dff["AnyCareforCHILD2_C"] != 99)]
        dff = dff.replace(2, 0)
        dff = dff.replace(99, 0)
        dff['Sum'] = dff['AnyCareforCHILD1_C'] + dff['AnyCareforCHILD2_C']
        rows = dff.shape[0]
        dff = dff.groupby('State').mean(numeric_only=True).reset_index()
        dff = dff[['State', 'Sum']]
        fig = px.choropleth(dff,
                            locations='State',
                            locationmode="USA-states",
                            color_continuous_scale='ice_r',
                            color='Sum',
                            labels={"Sum": '# of Children'},
                            title='Average Number of Children in Childcare (per household)<br><sup>You have selected '
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.",
                            scope="usa")
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig
    if str(variable) == "Income_2020_2":
        dff = dff[['State', 'Income_2020', 'State_2020_Median']]
        rows = dff.shape[0]
        dff.dropna(subset=['Income_2020'])
        dff['Income_2020'] = dff['Income_2020'].replace(
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'],
                                                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        dff = dff.groupby(['State']).median(numeric_only=True).reset_index()
        dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        [15999, 19999, 24999, 29999, 34999, 39999, 44999, 49999, 59999,
                                                         69999, 79999, 89999])
        dff['Proportion of State Median'] = dff['Income_2020'] / dff['State_2020_Median']
        dff['Percent of State Median'] = dff['Proportion of State Median'] * 100
        fig = px.choropleth(dff,
                            locations='State',
                            locationmode="USA-states",
                            color_continuous_scale='ice_r',
                            color='Percent of State Median',
                            labels={"Percent of State Median": '% of state median income'},
                            title='Median Income of Households Relative to their State\'s 2020 Median Income'
                                  '<br><sup>You have selected '
                            + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead) +
                            " for single head household.",
                            scope="usa")
        fig.update_layout(annotations=[dict(
            x=0.5,
            y=-0.19,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )])
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
