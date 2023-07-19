from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv("diaperdata.csv", encoding="latin-1")

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
regions = df["CensusRegion"].sort_values().unique()
races = ['American Indian or Alaskan Native', 'Asian', 'Black', 'Hispanic', 'Middle Eastern or North African',
         'Native Hawaiian or Pacific Islander', 'White', 'Multiracial', 'Prefer Not To Share']
singleheaddict = ['Yes', 'No']

filters = {"race": "",
           "state": "",
           "region": "",
           "singlehead": ""}

app = Dash(__name__)
app.title = "Diaper Bank Household Data"
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Diaper Bank Household Survey Results', style={'textAlign': 'left'}),
        html.P(children='Exploring survey results from nationwide survey of diaper banks '
                        'conducted by The National Diaper Bank Network from 2019 to 2021.'),
        html.Label(['Select Category:'], style={'font-weight': 'bold', "text-align": "center"}),
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Dropdown(id='variable-dropdown',
                         options=[{'label': 'Adults', 'value': 'Adults-value'},
                                  {'label': 'Children', 'value': "Children-value"},
                                  {'label': 'Income', 'value': "Income-value"}
                                  ],
                         placeholder="Select Category",
                         value="Adults-value",
                         clearable=False,
                         className="dropdown",
                         searchable=False,
                         style={"width": "65%"},
                         optionHeight=40
                         ),
            html.Br(),
            html.Label(["Select Variable:"], style={'font-weight': 'bold', "text-align": "center"}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                id="map-dropdown",
                options=[],
                value=None,
                clearable=False,
                searchable=False,
                style={"width": "65%"},
                className="dropdown"),
        ]),
    ]),
    html.Div([
        html.Br(),
        html.Label(['Select Race (optional):'], style={'font-weight': 'bold', "text-align": "center"}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(id='race',
                     options=races,
                     placeholder="Select Race",
                     clearable=True,
                     searchable=False,
                     className="dropdown",
                     style={"width": "65%"},
                     optionHeight=40
                     ),
        html.Br(),
        html.Label(['Select State (optional):'], style={'font-weight': 'bold', "text-align": "center"}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(id='state',
                     options=states,
                     placeholder="Select State",
                     clearable=True,
                     searchable=False,
                     className="dropdown",
                     style={"width": "65%"},
                     optionHeight=40
                     ),
        html.Br(),
        html.Label(['Select if Single Head of Household (optional):'],
                   style={'font-weight': 'bold', "text-align": "center"}),
        html.Br(),
        html.Br(),
        dcc.Dropdown(id='singlehead',
                     options=singleheaddict,
                     placeholder="Select if Single Head of Household",
                     clearable=True,
                     searchable=False,
                     className="dropdown",
                     style={"width": "65%"},
                     optionHeight=40
                     ),
        html.Br(),
        html.Div([
            dcc.Graph(id='graph2-content'),
            dcc.Graph(id='graph-content'),
            dcc.Graph(id='graph3-content'),
            dcc.Graph(id='graph4-content'),
            dcc.Graph(id='graph5-content'),
            dcc.Graph(id='graph6-content'),
            dcc.Graph(id='graph7-content'),
            dcc.Graph(id='graph8-content'),
            dcc.Graph(id='graph9-content')
        ]),
    ]),
])


@callback(
    Output("map-dropdown", "options"),
    Output("map-dropdown", "value"),
    Input("variable-dropdown", "value"))
def update_map_dropdown(optionslctd):
    if optionslctd == "Adults-value":
        options = [{"label": 'Percentage of Households with a Single Head of Household', "value": 'NumAdults'},
                   {"label": 'Percentage of Households with One or More Working Adult', "value": 'Ad1CurrentWork'},
                   {"label": 'Percentage of Households with One or More Adult in Education or Job Training',
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
    dff = dff[["CensusRegion", "DB_Transport"]]
    dff = dff.sort_values('DB_Transport')
    fig = px.histogram(dff, x="DB_Transport",
                       labels={
                           "DB_Transport": "Method",
                           "count": "Count"},
                       template='plotly_white',
                       title="How Diaper Bank Recipients Access their Diaper Bank Products<br><sup>You have selected "
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
    dff = dff[["CensusRegion", "DB_Transport"]]
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
        y=-0.25,
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
    dff['Income_2019'] = dff['Income_2019'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                    ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                     '30,000-34,999', '35,000-39,999', '40,000-44,999', '45,000-49,999',
                                                     '50,000-59,999', '60,000-69,999', '70,000-79,999', '>=80,000'])
    rows = dff.dropna(subset=['Income_2019']).shape[0]
    dff = dff['Income_2019'].value_counts()
    dff = dff.to_frame('Count').reset_index()
    fig = px.histogram(dff, x='Income_2019', y='Count',
                       labels={"Income_2019": "Income Range (in dollars)",
                               "sum of Count": "Count"},
                       category_orders={"Income_2019": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                        '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                        '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                        '60,000-69,999', '70,000-79,999', '>=80,000']},
                       title="Distribution of Household Incomes in 2019<br><sup>You have selected "
                             + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                             + " for single head household.",
                       template='plotly_white')
    fig.update_layout(yaxis_title="Count")
    fig.update_traces(marker_color='#86bce8')
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
    dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                    ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                     '30,000-34,999', '35,000-39,999', '40,000-44,999', '45,000-49,999',
                                                     '50,000-59,999', '60,000-69,999', '70,000-79,999', '>=80,000'])
    rows = dff.dropna(subset=['Income_2020']).shape[0]
    dff = dff['Income_2020'].value_counts()
    dff = dff.to_frame('Count').reset_index()
    fig = px.histogram(dff, x='Income_2020', y='Count',
                       labels={"Income_2020": "Income Range (in dollars)",
                               "sum of Count": "Count"},
                       category_orders={"Income_2020": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                        '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                        '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                        '60,000-69,999', '70,000-79,999', '>=80,000']},
                       title="Distribution of Household Incomes in 2020<br><sup>You have selected "
                             + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                             + " for single head household.",
                       template='plotly_white')
    fig.update_layout(yaxis_title="Count")
    fig.update_traces(marker_color='#86bce8')
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
    percent_inHome = 16.4
    filters['race'] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff1 = dff[
        ['CH1_EarlyHeadStart', 'CH1_ChildCareCenter', 'CH1_FamilyChildCareHome', 'CH1_Preschool', 'CH1_FamFriendCare']]
    dff1 = dff1.replace(np.nan, 0)
    dff1['Outside'] = dff1['CH1_EarlyHeadStart'] + dff1['CH1_ChildCareCenter'] + dff1['CH1_FamilyChildCareHome'] + dff1[
        'CH1_Preschool'] + dff1['CH1_FamFriendCare']
    dff1.loc[(dff1['Outside'] > 0), 'Outside'] = 1.0
    nrows = dff1.shape[0]
    dff1 = dff1['Outside'].value_counts()
    dff2 = dff[
        ['CH2_EarlyHeadStart', 'CH2_ChildCareCenter', 'CH2_FamilyChildCareHome', 'CH2_Preschool', 'CH2_FamFriendCare']]
    dff2 = dff2.replace(np.nan, 0)
    dff2['Outside'] = dff2['CH2_EarlyHeadStart'] + dff2['CH2_ChildCareCenter'] + dff2['CH2_FamilyChildCareHome'] + dff2[
        'CH2_Preschool'] + dff2['CH2_FamFriendCare']
    dff2.loc[(dff2['Outside'] > 0), 'Outside'] = 1.0
    nrows += dff2.shape[0]
    dff2 = dff2['Outside'].value_counts()
    dff = dff1 + dff2
    dff = dff.to_frame('Number of Children')
    dff = dff.rename_axis('index').reset_index()
    dff.loc[(dff['index'] == 1), 'Type of Childcare'] = 'Outside of home'
    dff.loc[(dff['index'] == 0), 'Type of Childcare'] = 'Not outside of home'
    dff = dff.drop(['index'], axis=1)
    percent_inHome = round(
        (dff['Number of Children'].iloc[1] / (dff['Number of Children'].iloc[0] +
                                              dff['Number of Children'].iloc[1])) * 100, 1)
    fig = px.pie(dff, names="Type of Childcare", values="Number of Children",
                 labels={'Type of Childcare': 'Childcare Type'},
                 template="plotly_white",
                 color_discrete_sequence=px.colors.sequential.RdBu_r,
                 title="Percent of Children in Outside Childcare<br><sup>You have selected "
                       + str(race) + " as race, " + str(state) + " as state, and " + str(singlehead)
                       + " for single head household.",
                 category_orders={"Type of Childcare": ['Outside of home', 'Not outside of home']})
    fig.update_traces(pull=[0.05, 0])
    fig.update_layout(annotations=[dict(
        x=0.5,
        y=-0.19,
        xref='paper',
        yref='paper',
        text=f'Filters match to {nrows} responses (Child 1 and 2 were counted as different responses).',
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
    dff1 = dff[
        ['CH1ChildCare_DiapersRequired_C', 'CH1_ChildCareCenter', 'CH1_FamilyChildCareHome', 'CH1_Preschool',
         'CH1_FamFriendCare']]
    dff1 = dff1.dropna(how='all')
    dff1 = dff1.dropna(subset=['CH1ChildCare_DiapersRequired_C'])
    dff1 = dff1.replace(np.nan, 0)
    nrows = dff1.shape[0]
    dff1['Outside'] = dff1['CH1_FamFriendCare'] + dff1['CH1_ChildCareCenter'] + dff1['CH1_FamilyChildCareHome'] + dff1[
        'CH1_Preschool']
    dff1.loc[(dff1['Outside'] > 0), 'Outside'] = 1.0
    dff1 = dff1.loc[(dff1['Outside'] == 1)]
    dff1 = dff1['CH1ChildCare_DiapersRequired_C'].value_counts()
    dff2 = dff[['CH2ChildCare_DiapersRequired_C', 'CH2_ChildCareCenter', 'CH2_FamilyChildCareHome', 'CH2_Preschool',
                'CH2_FamFriendCare']]
    dff2 = dff2.dropna(how='all')
    dff2 = dff2.dropna(subset=['CH2ChildCare_DiapersRequired_C'])
    dff2 = dff2.replace(np.nan, 0)
    nrows += dff2.shape[0]
    dff2['Outside'] = dff2['CH2_FamFriendCare'] + dff2['CH2_ChildCareCenter'] + dff2['CH2_FamilyChildCareHome'] + dff2[
        'CH2_Preschool']
    dff2.loc[(dff2['Outside'] > 0), 'Outside'] = 1.0
    dff2 = dff2.loc[(dff2['Outside'] == 1)]
    dff2 = dff2['CH2ChildCare_DiapersRequired_C'].value_counts()
    dff = dff1 + dff2
    dff = dff.to_frame().reset_index()
    dff.loc[
        (dff['CH1ChildCare_DiapersRequired_C'] == 1), 'Diaper'] = 'Need to send diapers'
    dff.loc[
        (dff['CH1ChildCare_DiapersRequired_C'] == 2), 'Diaper'] = 'No need to send diapers'
    dff = dff.drop(['CH1ChildCare_DiapersRequired_C'], axis=1)
    fig = px.pie(dff, names='Diaper', values='count',
                 category_orders={"Diaper": ['Need to Send Diapers', 'Do Not Need to Send Diapers']},
                 labels={'Diaper': 'Diaper Requirement'},
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
