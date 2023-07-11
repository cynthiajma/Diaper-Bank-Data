from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.io as pio

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

df.loc[(df['Race_PreferNoShare'] == 1), 'Race'] = 'Prefer not to share'
df.loc[(df['Race_AIAN'] == 1), 'Race'] = 'American Indian or Alaska Native'
df.loc[(df['Race_Asian'] == 1), 'Race'] = 'Asian'
df.loc[(df['Race_BlackAA'] == 1), 'Race'] = 'Black'
df.loc[(df['Race_Hispanic'] == 1), 'Race'] = 'Hispanic'
df.loc[(df['Race_NativeHawaiianPI'] == 1), 'Race'] = 'Native Hawaiian or Pacific Islander'
df.loc[(df['Race_White'] == 1), 'Race'] = 'White'
df.loc[(df['Race_MENA'] == 1), 'Race'] = 'Middle East or North Africa'
df.loc[(df['Race_Multiracial'] == 1), 'Race'] = 'Multiracial'
df.loc[((df[['Race_PreferNoShare', 'Race_AIAN', 'Race_Asian', 'Race_BlackAA', 'Race_Hispanic', 'Race_NativeHawaiianPI',
             'Race_White', 'Race_MENA', 'Race_Multiracial']].sum(axis=1)) > 1), 'Race'] = 'Multiracial'
df.loc[((df[['Race_PreferNoShare', 'Race_AIAN', 'Race_Asian', 'Race_BlackAA', 'Race_Hispanic', 'Race_NativeHawaiianPI',
             'Race_White', 'Race_MENA', 'Race_Multiracial']].sum(axis=1)) == 0), 'Race'] = 'Prefer not to share'

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

states = df["State"].sort_values().unique()
regions = df["CensusRegion"].sort_values().unique()
races = df["Race"].sort_values().unique()

filters = {"race": "",
           "region": ""}

app = Dash(__name__)# external_stylesheets=external_stylesheets)
app.title = "Diaper Bank Household Data"
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Diaper Bank Household Data", className="header-title"),
                html.P(
                    children=(
                        "Exploring Nationwide Data on Diaper Bank Utilization among Households in 2020"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div([
            html.Br(),
            html.Label(['Select Category:'], className='label'),
            dcc.Dropdown(id='variable-dropdown',
                         options=[{'label': 'Adults', 'value': 'Adults-value'},
                         {'label': 'Children', 'value': "Children-value"},
                         {'label': 'Income', 'value': "Income-value"}
                         ],
                         placeholder="Select Category",
                         value="Adults-value",
                         clearable=False,
                         className="dropdown"),

            html.Br(),
            html.Label("Select Variable"),
            dcc.Dropdown(
                        id="map-dropdown",
                        options=[],
                        value=None,
                        clearable=False,
                        className="dropdown"),
            html.Br(),
            html.Label("Select Race (Optional)"),
            dcc.Dropdown(id='race',
                         options=races,
                         placeholder="Filter by Race",
                         clearable=True,
                         className="dropdown"),
            html.Br(),
            html.Label(['Select Region:'], className='label'),
            html.Br(),
            dcc.Dropdown(regions, id='region',
                         placeholder="Select Region",
                         clearable=True,
                         className="dropdown"),
            ]),
        html.Div([
            html.Br(),
            dcc.Graph(id='graph2-content'),
            dcc.Graph(id='graph-content'),
            html.Br(),
            dcc.Graph(id='graph3-content'),
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
   Input('region', 'value'),
   Input('race', 'value'))
def update_graph(region, race):
    filters["race"] = str(race) if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["region"] = str(region) if region else ""
    dff = dff.loc[(dff['CensusRegion']) == filters["region"]] if filters["region"] else dff
    dff = dff[["CensusRegion", "DB_Transport"]]
    dff = dff.sort_values('DB_Transport')
    title = f"How "
    if race is not None:
        title += f"{race} "
    if region is not None:
        title += f"Diaper Bank Recipients Access their Diaper Bank in the {region} region"
    else:
        title += 'Diaper Bank Recipients Access their Diaper Bank'
    fig = px.histogram(dff, x="DB_Transport",
                       labels={
                            "DB_Transport": "Method",
                            "count": "Count"},
                       template='plotly_white',
                       title=title)
    fig.update_layout(yaxis_title="Count")
    fig.update_traces(marker_color='#86bce8')
    return fig


@callback(
   Output('graph3-content', 'figure'),
   Input('region', 'value'),
   Input('race', 'value'))
def update_pie(region, race):
    filters["race"] = str(race) if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["region"] = str(region) if region else ""
    dff = dff.loc[(dff['CensusRegion']) == filters["region"]] if filters["region"] else dff
    dff = dff[["CensusRegion", "DB_Transport"]]
    dff = dff.dropna()
    return px.pie(dff, names="DB_Transport",
                  category_orders={"DB_Transport": ["Drove Self", "Got a Ride",
                                                    "Public Transportation", "Taxi/Ride Sharing App", 'Walk']},
                  labels={"DB_Transport": "Method"})


@callback(
   Output('graph2-content', 'figure'),
   Input('map-dropdown', 'value'),
   Input('race', 'value'))
def display_choropleth(variable, race):
    filters["race"] = str(race) if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    if str(variable) == "NumKidsDiapers":
        dff = dff[['State', str(variable)]]
        dff = dff.groupby(['State']).mean(numeric_only=True).reset_index()
        return px.choropleth(dff, locations='State',
                             locationmode="USA-states",
                             color='NumKidsDiapers',
                             labels={"NumKidsDiapers": "# of Children"},
                             title='Average number of children in diapers (per household)',
                             scope="usa",
                             hover_data=['State', 'NumKidsDiapers'],
                             color_continuous_scale='ice_r')
    if str(variable) == "NumAdults":
        dff = dff[['State', str(variable)]]
        dff.loc[(dff['NumAdults'] == 1), 'Single Household'] = 'Yes'
        dff.loc[(dff['NumAdults'] != 1), 'Single Household'] = 'No'
        dff = dff[['State', 'Single Household']].groupby('State').value_counts(normalize=True).to_frame(name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Single Household'] == 'Yes']
        dff = dff[['State', 'Proportion of Households']]
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        return px.choropleth(dff, locations='State',
                             locationmode="USA-states",
                             color='Percentage of Households',
                             labels={"Percentage of Households": "Percentage of Households"},
                             title='Percentage of households with a single head of household',
                             scope="usa",
                             hover_data=['State', 'Percentage of Households'],
                             color_continuous_scale='ice_r')
    if str(variable) == "Income_2020":
        dff = dff[['State', str(variable)]]
        dff = dff.groupby(['State']).mean(numeric_only=True)['Income_2020'].round().to_frame().reset_index()
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
                             category_orders={"Income_2020": ['<=15,999', '16,000-19,999', '20,000-24,999', '25,'
                                                                                                            '000-29,999',
                                                       '30,000-34,999', '35,000-39,999', '40,000-44,999',
                                                       '45,000-49,999', '50,000-59,999', '60,000-69,999',
                                                       '70,000-79,999', '>=80,000']},
                             labels={"Income_2020": "Income Range (in dollars)"},
                             scope="usa",
                             title="Average Household Income in 2020")
    if str(variable) == "Income_2019":
        dff = dff[['State', str(variable)]]
        dff = dff.groupby(['State']).mean(numeric_only=True)['Income_2019'].round().to_frame().reset_index()
        dff['Income_2019'] = dff['Income_2019'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'])

        return px.choropleth(dff, locations='State',
                             locationmode='USA-states',
                             color='Income_2019',
                             color_discrete_sequence=px.colors.qualitative.Prism,
                             category_orders={"Income_2019": ['<=15,999', '16,000-19,999', '20,000-24,999', '25,'
                                                                                                            '000-29,999',
                                                       '30,000-34,999', '35,000-39,999', '40,000-44,999',
                                                       '45,000-49,999', '50,000-59,999', '60,000-69,999',
                                                       '70,000-79,999', '>=80,000']},
                             labels={"Income_2019": "Income Range (in dollars)"},
                             scope="usa",
                             title="Average Household Income in 2019")
    if str(variable) == "Ad1CurrentWork":
        dff = dff[['State', 'Ad1CurrentWork', 'Ad2CurrentWork']]
        dff = dff.dropna(subset=['Ad1CurrentWork', 'Ad2CurrentWork'])
        dff = dff.replace(2, 0)
        dff['Sum'] = dff['Ad1CurrentWork'] + dff['Ad2CurrentWork']
        dff.loc[(dff['Sum'] > 1), '1+ Adult Working'] = 'Yes'
        dff.loc[(dff['Sum'] <= 1), '1+ Adult Working'] = 'No'
        dff = dff[['State', '1+ Adult Working']].groupby('State').value_counts(normalize=True).to_frame(
            name='Proportion of Households').reset_index()
        dff = dff.loc[dff['1+ Adult Working'] == 'Yes']
        dff = dff[['State', 'Proportion of Households']]
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        return px.choropleth(dff, locations='State',
                             locationmode="USA-states",
                             color='Percentage of Households',
                             labels={"Percentage of Households": "Percentage of Households"},
                             title='Percentage of households with one or more working adult',
                             scope="usa",
                             hover_data=['State', 'Percentage of Households'],
                             color_continuous_scale='ice_r')
    if str(variable) == "Ad1_School":
        dff = dff[['State', 'Ad1_School', 'Ad2_School']]
        dff = dff.dropna(subset=['Ad1_School', 'Ad2_School'])
        dff = dff.replace(2, 0)
        dff['Sum'] = dff['Ad1_School'] + dff['Ad2_School']
        dff.loc[(dff['Sum'] >= 1), 'Education or Job Training'] = 'Yes'
        dff.loc[(dff['Sum'] == 0), 'Education or Job Training'] = 'No'
        dff = dff[['State', 'Education or Job Training']].groupby('State').value_counts(normalize=True).to_frame(
            name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Education or Job Training'] == 'Yes']
        dff = dff[['State', 'Proportion of Households']]
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        return px.choropleth(dff, locations='State',
                             locationmode="USA-states",
                             color='Percentage of Households',
                             labels={"Percentage of Households": "Percentage of Households"},
                             title='Percentage of households with one or more adult in education or job training',
                             scope="usa",
                             hover_data=['State', 'Percentage of Households'],
                             color_continuous_scale='ice_r')
    if str(variable) == "AnyCareforCHILD1_C":
        dff = dff[['State', 'AnyCareforCHILD1_C', 'AnyCareforCHILD2_C']]
        dff = dff.loc[(dff["AnyCareforCHILD1_C"] != 99) | (dff["AnyCareforCHILD2_C"] != 99)]
        dff = dff.replace(2, 0)
        dff = dff.replace(99, 0)
        dff['Sum'] = dff['AnyCareforCHILD1_C'] + dff['AnyCareforCHILD2_C']
        dff = dff.groupby('State').mean(numeric_only=True).reset_index()
        dff = dff[['State', 'Sum']]
        return px.choropleth(dff,
                             locations='State',
                             locationmode="USA-states",
                             color_continuous_scale='ice_r',
                             color='Sum',
                             labels={"Sum": '# of Children'},
                             title='Average number of children in childcare (per household)',
                             scope="usa")
    if str(variable) == "Income_2020_2":
        dff = dff[['State', 'Income_2020', 'State_2020_Median']]
        dff = dff.groupby(['State']).median(numeric_only=True).reset_index()
        dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        [15999, 19999, 24999, 29999, 34999, 39999, 44999, 49999, 59999,
                                                         69999, 79999, 89999])
        dff['Proportion of State Median'] = dff['Income_2020'] / dff['State_2020_Median']
        dff['Percent of State Median'] = dff['Proportion of State Median'] * 100
        return px.choropleth(dff,
                             locations='State',
                             locationmode="USA-states",
                             color_continuous_scale='ice_r',
                             color='Percent of State Median',
                             labels={"Percent of State Median": '% of state median income'},
                             title='Median income of households relative to their state\'s 2020 median income',
                             scope="usa")

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
