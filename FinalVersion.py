from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv("diaperdata.csv", encoding="latin-1")

# Reading and opening census data
acsincome = pd.read_csv("ACS_5year_2021_income.csv", encoding="latin-1")
acsincome = acsincome.loc[acsincome['Race'] != 'ALL']
acsincome = acsincome.loc[acsincome['Race'] != 'WHITE']
acsincome = pd.melt(acsincome, id_vars=['State', 'Race'], value_vars=["<16k", "16-20k", "20-25k", "25-30k",
                                                                      "30-35k", "35-40k", "40-45k", "45-50k",
                                                                      "50-60k", "60-70k", "70-80k", "80k+"])
acsincome['variable'] = acsincome['variable'].replace(["<16k", "16-20k", "20-25k", "25-30k",
                                                       "30-35k", "35-40k", "40-45k", "45-50k",
                                                       "50-60k", "60-70k", "70-80k", "80k+"],
                                                      ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                       '30,000-34,999', '35,000-39,999', '40,000-44,999',
                                                       '45,000-49,999', '50,000-59,999', '60,000-69,999',
                                                       '70,000-79,999', '>=80,000'])
# Renaming race values in census data
acsincome['Race']=acsincome['Race'].replace(['ASIAN','BLACK OR AFRICAN AMERICAN','AMERICAN INDIAN AND ALASKA NATIVE',
                                             'NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER','TWO OR MORE RACES','HISPANIC OR LATINO','WHITE, NOT HISPANIC OR LATINO'
                                            ],['Asian','Black','American Indian or Alaskan Native','Native Hawaiian or Pacific Islander','Multiracial','Hispanic','White'])

# Replacing all state values for initials in census data
acsincome['State']=acsincome['State'].replace(['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut',
                                               'Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois',
                                               'Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts',
                                               'Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada',
                                               'New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota',
                                               'Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota',
                                               'Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'],
                                              ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN',
                                               'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH',
                                               'NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT',
                                               'VT','VA','WA','WV','WI','WY'])

# Replacing all state values with state intiials
df['State'] = df['State'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                   24, 25], ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
                                             'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
                                             'MO'])
df['State'] = df['State'].replace([26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
                                   47, 48, 49, 50, 99], ['MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
                                                         'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                                                         'VA', 'WA', 'WV', 'WI', 'WY', "Multiple States"])

# Adding additional diaper bank state info
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

# Replacing values for transport type
df['DB_Transport']=df['DB_Transport'].replace([1,2,3,4,5],['Walk','Public Transportation','Drove Self','Got a Ride',
                                                           'Taxi/Ride Sharing App'])
df.loc[(df['PartnerAgencyType'] == "HOMEVISIT"), 'DB_Transport'] = 'Home Visit'

# Replacing values for race
df.loc[(df['Race_PreferNoShare'] == 1), 'Race'] = 'Prefer Not to Share'
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
             'Race_White', 'Race_MENA', 'Race_Multiracial']].sum(axis=1)) == 0), 'Race'] = 'Prefer Not to Share'

# Replacing values for education type graph
df['Ad1_EduType']=df['Ad1_EduType'].replace([1,2,3,4,5,6],['High School','GED','Associate\'s/2-year','Bachelor\'s/4-year',
                                                           'Graduate Degree','Enrolled in a Job-Training/Non-Degree Program'])
df['Ad2_EduType']=df['Ad2_EduType'].replace([1,2,3,4,5,6],['High School','GED','Associate\'s/2-year','Bachelor\'s/4-year',
                                                           'Graduate Degree','Enrolled in a Job-Training/Non-Degree Program'])
# Assigning 2020 state median information from FRED data
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

# Replacing values for single household
df.loc[(df['NumAdults'] == 1), 'Single Household'] = 'Yes'
df.loc[(df['NumAdults'] != 1), 'Single Household'] = 'No'
singlehead = ['Yes', 'No']


# Sorting states, setting races
states = df["State"].sort_values().unique()
races = ['American Indian or Alaskan Native', 'Asian', 'Black', 'Hispanic', 'Middle Eastern or North African',
         'Native Hawaiian or Pacific Islander', 'White', 'Multiracial', 'Prefer Not to Share']
df['Income_2020_2'] = df['Income_2020']

# creating filters dictionary to add filters to
filters = {"race": "",
           "region": "", "state": "", 'singlehead': ""}
#Creating a filtering function
def filter(race, state, singlehead,dff):
    filters["race"] = race if race else ""
    filters['state'] = state if state else ""
    filters['singlehead'] = singlehead if singlehead else ""
    if 'race' in filters or 'state' in filters or 'singlehead' in filters:
        if filters['race']:
            dff = dff.loc[dff['Race'] == filters['race']]
        if filters['state']:
            dff = dff.loc[dff['State'] == filters['state']]
        if filters['singlehead']:
            dff = dff.loc[dff['Single Household'] == filters['singlehead']]
    return(dff)
#Creating a function that prevents graphs from displaying info if less than 10 people fit the filters
def under10(title):
    fig = go.Figure(layout=dict(template='plotly_white'))
    fig.update_layout(
        title=title,
        title_font=dict(
            family='Merriweather',
            size=21,
            color='black'
        ),
        title_x=0.5,
        annotations=[dict(text=f'Figure hidden. Filters match to less than 10 values.',
                          font=dict(
                              family="Montserrat",
                              size=12
                          ),
                          showarrow=False)])

    return fig

#Creating a function that updates each figure's annotations
def updatedlayout(fig,race,state,singlehead,rows,x1,x2,y1,y2):
    fig=fig.update_layout(
            annotations=[
                # displaying selected filters
                dict(
                    x=-0.004,
                    y=1.17,
                    text=f'You have selected {race} as race, {state} as state, and {singlehead} for single head of household',
                    font=dict(
                        family="Montserrat",
                        size=13
                    ),
                    showarrow=False
                ),
                # displaying number of matching responses
                dict(
                    x=0.5,
                    y=-0.19,
                    xref='paper',
                    yref='paper',
                    text=f'Filters match to {rows} responses',
                    font=dict(
                        family="Montserrat",
                        size=12
                    ),
                    showarrow=False
                )
            ],
            # changing font
            title_font=dict(
                family='Merriweather',
                size=18,
                color='black'
            ),
            dragmode=False
        )
    return fig

#Function that updates income for the 2 income graphs
def updatedlayoutincome(fig,rows):
    fig.update_layout(
        font_family="Montserrat",
        font_color="black",
        yaxis=dict(title='Percentage %'),
        barmode='overlay', bargap=0, bargroupgap=0,
        annotations=[dict(
            x=0.5,
            y=1,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )],
        title_font=dict(size=21),
        title_x=0.42,
        title_y=0.85
    )

    # Change hover data to income range, and opacity of the bars
    fig.update_traces(hovertemplate="Income Range: $%{x}<br>Percentage: %{y}%",
                      opacity=0.75)

    return fig

global percent_inHome

# app layout
external_stylesheets = ['assets/diaperstyles.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Diaper Bank Household Data"
app.layout = html.Div(
    children=[
        # main dash title
        html.Div(
            children=[
                html.H1(children="Diaper Bank Household Data", className="header-title"),
                html.P(
                    children=(
                        "Hover over on the map, or select filters to start exploring"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # race dropdown
        html.Div([
            html.Div([
                    html.Label(["Race"], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id='race',
                        options=races,
                        placeholder="Select Race",
                        clearable=True,
                        className="dropdown"
                    ),
                ], className='filter',
                ),
            # state dropdown
            html.Div([
                    html.Label(["State"], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id='state',
                        options=states,
                        placeholder="Select State",
                        clearable=True,
                        className="dropdown"
                    ),
                ], className='filter',
                ),
            # single head of household dropdown
            html.Div([
                    html.Label(['Single Head of Household'],
                               className='label'),
                    html.Br(),
                    dcc.Dropdown(id='singlehead',
                                 options=singlehead,
                                 placeholder="Select if Single Head of Household",
                                 clearable=True,
                                 searchable=False,
                                 className="dropdown",
                                 optionHeight=40
                                 ),
                    ], className='filter',
                )
            ],
            className='filtersRow1'
        ),
        # choropleth section
        html.H3(children='Map Filters', className='mapHeader'),
        html.Div(
            children=[
                html.Div([
                    # category dropdown
                    html.Label(['Category'], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id='variable-dropdown',
                        options=[
                            {'label': 'Adults', 'value': 'Adults-value'},
                            {'label': 'Children', 'value': 'Children-value'},
                            {'label': 'Income', 'value': 'Income-value'}
                        ],
                        placeholder="Select Category",
                        value="Adults-value",
                        clearable=False,
                        className="dropdown"
                    ),
                ], className='filter2'),
                html.Div([
                    # variable dropdown
                    html.Label(["Map Variable"], className='label'),
                    html.Br(),
                    dcc.Dropdown(
                        id="map-dropdown",
                        options=[],
                        value=None,
                        clearable=False,
                        className="dropdown"
                    ),
                ], className='filter2')
            ], className='filtersRow2'
        ),
        html.Div(
            children=[
                # choropleth
                dcc.Graph(id='map-content'),
                # additional visualization section
                html.H3(children='Additional Visualizations', className='part2-header'),
                html.Div([
                    # income graphs
                    html.H3(children="Comparison of Income Distributions for Diaper Bank Households and U.S. Census "
                            "Data", className='income-title'),
                    html.Div(id='display-selected-filtersINCOME', className='subtitle'),
                    dcc.Graph(id='income2019-content', className='income-graphs'),
                    dcc.Graph(id='income2020-content', className='income-graphs'),
                ]),
                html.Br(),
                html.Div([
                    # preterm graph
                    dcc.Graph(id='preterm-content', className='row2-graphs'),
                    # education graph
                    dcc.Graph(id='education-content', className='row2-graphs'),
                ]),
                # education graph
                dcc.Graph(id='transport-pie-content', className='static-section'),
                # extra statistics
                html.Div(children=[html.H3(children="Extra Statistics", className='stats-title'),
                                   html.Img(src="assets/static.png", className='preterm-stats')],
                         className='static-section')
            ]),
    ])

# display filters for income
@callback(
    Output('display-selected-filtersINCOME', 'children'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def income_subtitle(race, state, singlehead):
    return f'You have selected {race} as race, {state} as state, and {singlehead} for single head of household.'

# connects variable dropdown to category dropdown
@callback(
    Output("map-dropdown", "options"),
    Output("map-dropdown", "value"),
    Input("variable-dropdown", "value"))
def update_map_dropdown(optionslctd):
    if optionslctd == "Adults-value":
        options = [{"label": 'One or More Working Adult', "value": 'Ad1CurrentWork'},
                   {"label": 'Single Head of Household', "value": 'NumAdults'},
                   {"label": 'One or More Adult in Education or Job Training',
                    "value": 'Ad1_School'}]
        value = "Ad1CurrentWork"
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

# choropleth graph
@callback(
   Output('map-content', 'figure'),
   [Input('map-dropdown', 'value'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def display_choropleth(variable, race, state, singlehead):
    # filtering dataframe
    filters["race"] = race if race else ""
    filters['state'] = state if state else ""
    filters['singlehead'] = singlehead if singlehead else ""
    dff = pd.DataFrame()
    dff = df[['Race', 'State', str(variable), 'Single Household']]
    dff=filter(race, state, singlehead,dff)
    # average number of children in diapers
    if variable == "NumKidsDiapers":
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shownif less than 10 responses
        if rows < 10:
            fig = under10("Average Number of Kids in Diapers Per Household")
            return fig

        # group by state and calculate means for numeric variables
        dff = dff.groupby(['State']).mean(numeric_only=True).reset_index()
        # make choropleth for average number of kids in diapers
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='NumKidsDiapers',
                            labels={"NumKidsDiapers": "# of Children"},
                            title="Average Number of Children in Diapers (per Household)",
                            scope="usa",
                            hover_data=['State', 'NumKidsDiapers'],
                            color_continuous_scale='ice_r')
        #Calling the function to update layout
        fig=updatedlayout(fig,race,state,singlehead,rows,-0.004,0.5,1.17,-0.19)
        return fig

    # percentage of households with a single head of household
    if variable == "NumAdults":
        # creating single household variable
        dff.loc[(dff['NumAdults'] == 1), 'Single Household'] = 'Yes'
        dff.loc[(dff['NumAdults'] != 1), 'Single Household'] = 'No'
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig=under10("Percentage of Households with a Single Head of Household")
            return fig
        # grouping by state and counting how many responses are "Yes" for single households variable
        dff = dff[['State', 'Single Household']].groupby('State').value_counts(normalize=True)\
            .to_frame(name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Single Household'] == 'Yes']
        dff = dff[['State', 'Proportion of Households']]
        # converting proportion to percentage
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        # creating choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff, locations='State',
                            locationmode="USA-states",
                            color='Percentage of Households',
                            labels={"Percentage of Households": "% of Households"},
                            title="Percentage of Households with a Single Head of Household",
                            scope="usa",
                            hover_data=['State', 'Percentage of Households'],
                            color_continuous_scale='ice_r')
        #Calling the function to update layout
        fig=updatedlayout(fig,race,state,singlehead,rows,-0.004,0.5,1.17,-0.19)
        return fig

    # median household income in 2019
    if variable == "Income_2019":
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig = under10('Median Household Income in 2019')
            return fig

        # replace income ranges to numbers to calculate median
        dff['Income_2019'] = dff['Income_2019'].replace(['<=15,999', '<=15,999', '16,'
                                                                               '000-19,999',
                                                       '20,000-24,999',
                                                       '25,000-29,999', '30,000-34,999',
                                                       '35,000-39,999', '40,000-44,999',
                                                       '45,000-49,999', '50,000-59,999',
                                                       '60,000-69,999', '70,000-79,999', '>=80,000'],
                                                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        # grouping by state and calculating medians
        dff = dff.groupby(['State']).median(numeric_only=True)['Income_2019'].apply(
            lambda x: round(x)).to_frame().reset_index()
        # replacing numbers back to ranges
        dff['Income_2019'] = dff['Income_2019'].replace([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        ['<=15,999', '<=15,999', '16,'
                                                                                 '000-19,999',
                                                         '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'])
        # creating choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff, locations='State',
                            locationmode='USA-states',
                            color='Income_2019',
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            category_orders={"Income_2019": ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,'
                                                                                                           '999',
                                                             '30,000-34,999', '35,000-39,999', '40,000-44,999',
                                                             '45,000-49,999', '50,000-59,999', '60,000-69,999',
                                                             '70,000-79,999', '>=80,000']},
                            labels={"Income_2019": "Income Range (in dollars)"},
                            scope="usa",
                            title='Median Household Income in 2019')

        #Calling the function to update layout
        fig=updatedlayout(fig,race,state,singlehead,rows,-0.004,0.5,1.17,-0.19)
        return fig

    # median household income in 2020
    if variable == "Income_2020":
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig = under10('Median Household Income in 2020')
            return fig

        # grouping by state to calculate median income
        dff = dff.groupby(['State']).median(numeric_only=True)['Income_2020'].apply(
            lambda x: round(x)).to_frame().reset_index()
        # replacing numbers back to income ranges
        dff['Income_2020'] = dff['Income_2020'].replace([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                        ['<=15,999', '<=15,999', '16,'
                                                                                 '000-19,999',
                                                         '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999',
                                                         '35,000-39,999', '40,000-44,999',
                                                         '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000'])
        # creating choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff, locations='State',
                            locationmode='USA-states',
                            color='Income_2020',
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            category_orders={"Income_2020": ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,'
                                                                                                         '999',
                                                           '30,000-34,999', '35,000-39,999', '40,000-44,999',
                                                           '45,000-49,999', '50,000-59,999', '60,000-69,999',
                                                           '70,000-79,999', '>=80,000']},
                            labels={"Income_2020": "Income Range (in dollars)"},
                            scope="usa",
                            title='Median Household Income in 2020')
        #Calling the function to update layout
        fig=updatedlayout(fig,race,state,singlehead,rows,-0.004,0.5,1.17,-0.19)
        return fig
    # percentage of households with one or more working adult
    if variable == "Ad1CurrentWork":
        dff['Ad1CurrentWork'] = df['Ad1CurrentWork']
        dff['Ad2CurrentWork'] = df['Ad2CurrentWork']
        # dropping rows where there were no responses for both columns
        dff = dff.dropna(how='all')
        # changing not working (2) to 0
        dff = dff.replace(2, 0)
        # changing NA to 0
        dff = dff.replace(np.nan, 0)
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig = under10('Percentage of Households with One or More Working Adult')
            return fig

        # summing up number of adults working
        dff['Sum'] = dff['Ad1CurrentWork'] + dff['Ad2CurrentWork']
        # calculating if household has one or more adult working
        dff.loc[(dff['Sum'] >= 1), '1+ Adult Working'] = 'Yes'
        dff.loc[(dff['Sum'] == 0), '1+ Adult Working'] = 'No'
        # grouping by state to see how many households have one or more working adult ('Yes')
        dff = dff[['State', '1+ Adult Working']].groupby('State').value_counts(normalize=True).to_frame(
            name='Proportion of Households').reset_index()
        dff = dff.loc[dff['1+ Adult Working'] == 'Yes']
        # converting proportion to percentage
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        # creating choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff, locations='State',
                          locationmode="USA-states",
                          color='Percentage of Households',
                          labels={"Percentage of Households": "% of Households"},
                          title='Percentage of Households with One or More Working Adult',
                          scope="usa",
                          hover_data=['State', 'Percentage of Households'],
                          color_continuous_scale='ice_r')
        fig=updatedlayout(fig,race,state,singlehead,rows,-0.004,0.5,1.17,-0.19)
        return fig

    # percentage of households with one or more adult in education or job training
    if str(variable) == "Ad1_School":
        dff['Ad1_School'] = df['Ad1_School']
        dff['Ad2_School'] = df['Ad2_School']
        # dropping rows where both columns had to responses
        dff = dff.dropna(how='all')
        # changing not in education/job training (2) to 0
        dff = dff.replace(2, 0)
        # changing NA to 0
        dff = dff.replace(np.nan, 0)
        # adding up number of adults in edu/job training
        dff['Sum'] = dff['Ad1_School'] + dff['Ad2_School']
        dff.loc[(dff['Sum'] >= 1), 'Education or Job Training'] = 'Yes'
        dff.loc[(dff['Sum'] == 0), 'Education or Job Training'] = 'No'
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig = under10('Percentage of Households with One or More Adult in Education or Job Training')
            return fig

        # grouping by state and counting how many have one or more adult in edu/job training
        dff = dff[['State', 'Education or Job Training']].groupby('State').value_counts(normalize=True).to_frame(
            name='Proportion of Households').reset_index()
        dff = dff.loc[dff['Education or Job Training'] == 'Yes']
        # converting proportion to percentage
        dff['Percentage of Households'] = dff['Proportion of Households'] * 100
        # creating choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff, locations='State',
                          locationmode="USA-states",
                          color='Percentage of Households',
                          labels={"Percentage of Households": "% of Households"},
                          title='Percentage of Households with One or More Adult in Education or Job Training',
                          scope="usa",
                          hover_data=['State', 'Percentage of Households'],
                          color_continuous_scale='ice_r')
        fig = updatedlayout(fig, race, state, singlehead, rows, -0.004, 0.5, 1.17, -0.19)
        return fig

    # average number of children in childcare
    if str(variable) == "AnyCareforCHILD1_C":
        dff['AnyCareforCHILD1_C'] = df['AnyCareforCHILD1_C']
        dff['AnyCareforCHILD2_C'] = df['AnyCareforCHILD2_C']
        # select rows where there are responses to at least one of two columns
        dff = dff.loc[(dff["AnyCareforCHILD1_C"] != 99) | (dff["AnyCareforCHILD2_C"] != 99)]
        # replacing not in childcare/was in childcare as 0
        dff = dff.replace(2, 0)
        dff = dff.replace(99, 0)
        # adding up number of kids in childcare
        dff['Sum'] = dff['AnyCareforCHILD1_C'] + dff['AnyCareforCHILD2_C']
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig = under10('Average Number of Children in Childcare (per Household)')
            return fig

        # grouping by state and calculating mean for numeric variables
        dff = dff.groupby('State').mean(numeric_only=True).reset_index()
        dff = dff[['State', 'Sum']]
        # create choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff,
                          locations='State',
                          locationmode="USA-states",
                          color_continuous_scale='ice_r',
                          color='Sum',
                          labels={"Sum": '# of Children'},
                          title='Average Number of Children in Childcare (per Household)',
                          scope="usa")
        fig = updatedlayout(fig, race, state, singlehead, rows, -0.004, 0.5, 1.17, -0.19)
        return fig

    # median income of households relative to their state's 2020 median income
    if str(variable) == "Income_2020_2":
        dff['State_2020_Median'] = df['State_2020_Median']
        # counting number of responses
        rows = dff.shape[0]
        # no choropleth shown if less than 10 responses
        if rows < 10:
            fig = under10('Median Income of Households Relative to Their State\'s 2020 Median Income')
            return fig

        # grouping by state to calculate medians
        dff = dff.groupby(['State']).median(numeric_only=True).reset_index()
        # converting numbers to end of income ranges
        dff['Income_2020_2'] = dff['Income_2020_2'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                            [15999, 19999, 24999, 29999, 34999, 39999, 44999, 49999,
                                                             59999,
                                                             69999, 79999, 89999])
        # calculating proportion and converting to percentage
        dff['Proportion of State Median'] = dff['Income_2020_2'] / dff['State_2020_Median']
        dff['Percent of State Median'] = dff['Proportion of State Median'] * 100
        # creating choropleth
        fig = go.Figure(layout=dict(template='plotly'))
        fig = px.choropleth(dff,
                          locations='State',
                          locationmode="USA-states",
                          color_continuous_scale='ice_r',
                          color='Percent of State Median',
                          labels={"Percent of State Median": '% of state median income'},
                          title='Median Income of Households Relative to Their State\'s 2020 Median Income',
                          scope="usa")
        fig = updatedlayout(fig, race, state, singlehead, rows, -0.004, 0.5, 1.17, -0.19)
        return fig

@callback(
   Output('income2019-content', 'figure'),
   [Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def update_income2019(race, state, singlehead):
    # Filter df dataframe based on selected filters
    filters["race"] = race if race else ""
    filters['state'] = state if state else ""
    filters['singlehead'] = singlehead if singlehead else ""
    dff = pd.DataFrame()
    acs = acsincome.copy()

    if 'race' in filters or 'state' in filters or 'singlehead' in filters:
        dff = df[
            ['Race', 'State', 'Single Household', 'Income_2019']]
        if filters['race']:
            dff = dff.loc[dff['Race'] == filters['race']]
            acs = acs.loc[acsincome['Race'] == filters['race']]
        if filters['state']:
            dff = dff.loc[dff['State'] == filters['state']]
            acs = acs.loc[acsincome['State'] == filters['state']]
        if filters['singlehead']:
            dff = dff.loc[dff['Single Household'] == filters['singlehead']]

    # Find number of rows and if the number < 10, hide graph
    rows = dff.dropna(subset=['Income_2019']).shape[0]
    if rows < 10:
        fig = under10('2019')
        return fig

    # Convert 'Income_2019' to income ranges.
    dff['Income_2019'] = dff['Income_2019'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                    ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                     '30,000-34,999', '35,000-39,999', '40,000-44,999', '45,000-49,999',
                                                     '50,000-59,999', '60,000-69,999', '70,000-79,999', '>=80,000'])

    # Calculate percentage for distribution
    dff = dff['Income_2019'].value_counts(normalize=True)
    dff = dff.to_frame('Count').rename_axis('Income Range').reset_index()
    dff['Percentage'] = dff['Count'] * 100
    acs = acs.groupby('variable').sum()
    acs['Percentage'] = acs['value'] / acs['value'].sum() * 100
    acs = acs.rename_axis('Income Range').reset_index()
    acs['Type'] = 'ACS 5-Year Survey'
    dff['Type'] = 'Diaper Bank Recipients'

    # Merge dff and acs dataframes into 1
    dff = dff[['Income Range', 'Percentage', 'Type']]
    acs = acs[['Income Range', 'Percentage', 'Type']]
    acsdff = pd.concat([acs, dff])

    # Create income 2019 bar graph
    fig = go.Figure(layout=dict(template='plotly'))
    fig = px.histogram(acsdff, x='Income Range', y='Percentage', color='Type',
                       labels={"Income Range": "Income Range ($)"},
                       category_orders={"Income Range": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                         '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000']},
                       title="2019",
                       template='plotly_white',
                       color_discrete_map={
                           "Diaper Bank Recipients": "#e81e36",
                           "ACS 5-Year Survey": "#86bce8"})

    # Change title font and size, and add filters matched to responses annotation
    fig = updatedlayoutincome(fig,rows)
    return fig

#Income 2020 graph
@callback(
   Output('income2020-content', 'figure'),
   [Input('race', 'value'),
   Input('state', 'value'),
    Input('singlehead', 'value')])
def update_income2020(race, state, singlehead):
    # Filter df dataframe based on selected filters
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    # Modify acs dataframe based on selected filters
    acs = acsincome.loc[(acsincome['Race']) == filters["race"]] if filters["race"] else acsincome
    acs = acs.loc[(acsincome['State']) == filters["state"]] if filters["state"] else acs

    # Convert 'Income_2020' to income ranges.
    dff['Income_2020'] = dff['Income_2020'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                                    ['<=15,999', '16,000-19,999', '20,000-24,999', '25,000-29,999',
                                                     '30,000-34,999', '35,000-39,999', '40,000-44,999', '45,000-49,999',
                                                     '50,000-59,999', '60,000-69,999', '70,000-79,999', '>=80,000'])

    # Find number of rows and if the number < 10, hide graph
    rows = dff.dropna(subset=['Income_2020']).shape[0]
    if rows < 10:
        fig = under10('2020')
        return fig

    # Calculate percentage for distribution
    dff = dff['Income_2020'].value_counts(normalize=True)
    dff = dff.to_frame('Count').rename_axis('Income Range').reset_index()
    dff['Percentage'] = dff['Count'] * 100
    acs = acs.groupby('variable').sum()
    acs['Percentage'] = acs['value'] / acs['value'].sum() * 100
    acs = acs.rename_axis('Income Range').reset_index()
    acs['Type'] = 'ACS 5-Year Survey'
    dff['Type'] = 'Diaper Bank Recipients'

    # Merge together 2 dataframes into 1
    dff = dff[['Income Range', 'Percentage', 'Type']]
    acs = acs[['Income Range', 'Percentage', 'Type']]
    acsdff = pd.concat([acs, dff])

    # Create income 2020 histogram
    fig = go.Figure(layout=dict(template='plotly'))
    fig = px.histogram(acsdff, x='Income Range', y='Percentage', color='Type',
                       labels={"Income Range": "Income Range ($)"},
                       category_orders={"Income Range": ['<=15,999', '16,000-19,999', '20,000-24,999',
                                                         '25,000-29,999', '30,000-34,999', '35,000-39,999',
                                                         '40,000-44,999', '45,000-49,999', '50,000-59,999',
                                                         '60,000-69,999', '70,000-79,999', '>=80,000']},
                       title="2020",
                       template='plotly_white',
                       color_discrete_map={
                           "Diaper Bank Recipients": "#e81e36",
                           "ACS 5-Year Survey": "#86bce8"})

    # Change title font and size, and add filters matched to responses annotation
    fig = updatedlayoutincome(fig, rows)
    return fig

# Preterm graph
@callback(
   Output('preterm-content', 'figure'),
   [Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def update_preterm(race, state, singlehead):
    # Filter dataframe based on selected filters
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff
    dff = dff[
        ['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm', 'CH7Preterm', 'CH8Preterm',
         'Race']]

    # Drop null values in this subset of the dataframe
    dff = dff.dropna(subset = ['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm',
                               'CH7Preterm', 'CH8Preterm'], how='all')

    # Find number of rows and if the number < 10, hide graph
    rows = dff.shape[0]
    if rows < 10:
        fig = under10(f"Distribution of Preterm vs Term Babies by Race or Ethnic Identity<br><sup><sup>You have "f"selected "
                      f"{race} as race, {state} as state, and {singlehead} for single head of household.")
        return fig

    # Drop null values
    dfff = dff.replace(np.nan, 0)

    # Calculate the total number of babies by race
    dfff = dfff.replace(2, 1)
    dfff['Total Children'] = dfff[
        ['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm', 'CH7Preterm',
         'CH8Preterm']].sum(axis=1)
    dfff = dfff[['Race', 'Total Children']].groupby(['Race']).sum('Total Children').reset_index()
    dfff['Total Children'] = dfff['Total Children'].astype(int)

    # Calculate the total number of preterm babies by race
    dff = dff.replace(np.nan, 0)
    dff = dff.replace(2, 0)
    dff['SumPreterm'] = dff[
        ['CH1Preterm', 'CH2Preterm', 'CH3Preterm', 'CH4Preterm', 'CH5Preterm', 'CH6Preterm', 'CH7Preterm',
         'CH8Preterm']].sum(axis=1)
    dff = dff[['Race', 'SumPreterm']].groupby('Race').sum().astype(int).reset_index()
    dff = dff.merge(dfff)

    # Calculate the percentage of preterm babies
    dff['Preterm'] = dff['SumPreterm'] / dff['Total Children'] * 100
    dff['Term'] = 100 - dff['Preterm']
    dff['SumTerm'] = dff['Total Children'] - dff['SumPreterm']
    dff = dff.sort_values(by='Preterm')

    # Create stacked bar chart for preterm and term babies by race
    fig = go.Figure(layout=dict(template='plotly'))
    fig = px.bar(dff, y='Race', x=['Preterm', 'Term'],
                 template='plotly_white',
                 color_discrete_map={
                     "Preterm": "#e81e36",
                     "Term": "#86bce8"},
                 labels={"variable": "Preterm or Term",
                         "value": "Percent",
                         'Total Children': 'Total Children in Race'},
                 hover_data = ['Total Children'],
                 title=f"Distribution of Preterm vs Term Babies by Race or Ethnic Identity",
                 barmode='stack')

    # Changing title font and size, and adding filters selected annotation
    fig.update_layout(
        font_family="Montserrat",
        font_color="black",
        title_font=dict(size=21),
        title_x=0.5)
    fig.add_annotation(
            x=0.4,
            y=1.16,
            xref='paper',
            yref='paper',
            text=f"You have selected {race} as race, {state} as state, and {singlehead} for single "
                        "head of household.",
            showarrow=False)
    # Adding how many matching responses annotation
    fig.add_annotation(
        x=0.5,
        y=-0.25,
        xref='paper',
        yref='paper',
        text=f'Filters matched to {rows} responses.',
        showarrow=False
    )
    return fig


# Education pie chart
@callback(
    Output('education-content', 'figure'),
    Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value'))
def update_education(race, state, singlehead):
    # Filter dataframe based on selected filters
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    # Removing null values, modifying dataframe
    dff1 = dff[['Ad1_School', 'Ad1_EduType']]
    dff2 = dff[['Ad2_School', 'Ad2_EduType']]
    dff1 = dff1.loc[(dff1['Ad1_School']) == 1]
    dff2 = dff2.loc[(dff2['Ad2_School']) == 1]
    dff1 = dff1.dropna(subset=['Ad1_EduType'])
    dff2 = dff2.dropna(subset=['Ad2_EduType'])

    # Find number of rows and if the number < 10, hide graph
    rows = dff1.shape[0] + dff2.shape[0]
    if rows < 10:
        fig = under10('Distribution of Education Type<br><sup><sup>You have selected ' + str(race) + " as race, "
                      + str(state) + " as state, and " + str(singlehead) + " for single head of household.")
        return (fig)

    #Modifying dataframe columns and values
    dff = dff1['Ad1_EduType'].value_counts() + dff2['Ad2_EduType'].value_counts()
    dff = dff.to_frame('Number of Adults').rename_axis('Education Type').reset_index()

    # Create education pie chart
    fig = px.pie(dff, names="Education Type", values="Number of Adults",
                 template="plotly_white",
                 color_discrete_sequence=px.colors.sequential.RdBu_r,
                 title="Distribution of Education Type",
                 category_orders={
                     "Education Type": ['High School', 'GED', 'Associate’s/2-year', 'Bachelor’s/4-year',
                                        'Graduate degree', 'Enrolled in a Job-Training/Non-Degree Program']})

    # Changing title font, adding how many responses annotation
    fig.update_layout(
        font_family="Montserrat",
        font_color="black",
        annotations=[dict(
            x=0.5,
            y=-0.25,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )],
        title_font=dict(size=21),
        title_x=0.5,
        legend_title="Education Level",
    )

    # Add filters annotation
    fig.add_annotation(x=0.1,
                       y=1.162,
                       xref='paper',
                       yref='paper',
                       text=f"You have selected {race} as race, {state} as state, and {singlehead} for single "
                       "head of household.",
                       showarrow=False)
    return fig


# Transportation pie chart
@callback(
   Output('transport-pie-content', 'figure'),
   [Input('race', 'value'),
    Input('state', 'value'),
    Input('singlehead', 'value')])
def update_transport_pie(race, state, singlehead):
    # Filter dataframe based on selected filters
    filters["race"] = race if race else ""
    dff = df.loc[(df['Race']) == filters["race"]] if filters["race"] else df
    filters["state"] = state if state else ""
    dff = dff.loc[(df['State']) == filters["state"]] if filters["state"] else dff
    filters["singlehead"] = singlehead if singlehead else ""
    dff = dff.loc[(df['Single Household']) == filters["singlehead"]] if filters["singlehead"] else dff

    # Removing null values, modifying dataframe
    dff = dff[["DB_Transport", 'AccessDB']].dropna(subset=['AccessDB'])
    dff.loc[(dff['AccessDB'] == 1), 'DB_Transport'] = 'Home Visit'
    dff = dff.dropna(subset=['DB_Transport'])

    # Find number of rows and if the number < 10, hide graph
    rows = dff.shape[0]
    if rows < 10:
        fig = under10("How Diaper Bank Recipients Access Diaper Bank Products")
        return fig

    # Create transportation pie chart
    fig = go.Figure(layout=dict(template='plotly'))
    fig = px.pie(dff, names="DB_Transport",
                 category_orders={"DB_Transport": ["Drove Self", "Got a Ride", "Public Transportation",
                                                   "Taxi/Ride Sharing App", "Walk", "Home Visit"
                                                   ]},
                 labels={"DB_Transport": "Method"},
                 template='plotly_white',
                 title="How Diaper Bank Recipients Access Diaper Bank Products",
                 color_discrete_sequence=px.colors.sequential.RdBu_r
                 )

    # Add how many responses match annotation
    fig.update_layout(
        font_family="Montserrat",
        font_color="black",
        annotations=[dict(
            x=0.25,
            y=-0.17,
            xref='paper',
            yref='paper',
            text=f'Filters matched to {rows} responses.',
            showarrow=False
        )],
        title_font=dict(size=21),
        title_x=0.5,
    )

    # Add filter selection annotation
    fig.add_annotation(
            x=0,
            y=1.162,
            text=f"You have selected {race} as race, {state} as state, and {singlehead} for single "
                 "head of household.",
            showarrow=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)