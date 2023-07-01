from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv("diaperdata.csv", encoding="latin-1")

df['State'] = df['State'].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                   20, 21, 22, 23, 24, 25], ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL',
                                                             'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
                                                             'MD', 'MA', 'MI', 'MN', 'MS', 'MO'])
df['State'] = df['State'].replace([26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                                   39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 99],
                                  ['MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
                                   'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA',
                                   'WA', 'WV', 'WI', 'WY', "Multiple States"])

df.loc[(df['DiaperBankName'] == 'Emergency Infant Services'), 'State'] = 'OK'
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
regions = df["CensusRegion"].sort_values().unique()
choropleth = ['NumKidsDiapers', 'NumAdults']

external_stylesheets = ['Diaper-Bank-Data/assets/diaperstyles.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
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
                        "Exploring Nationwide Data on Diaper Bank Utilization among Households in 2020"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div([
            dcc.Dropdown(regions, id='dropdown-selection', placeholder="Select Region", value="Middle Atlantic",
                         clearable=False, className="dropdown"),
            html.Br(),
            dcc.Graph(id='graph-content')
        ]),
        html.Div([
            html.Br(),
            dcc.Dropdown(choropleth, id='variable', placeholder="Select Variable", value="NumKidsDiapers",
                         clearable=False, className="dropdown"),
            html.Br(),
            dcc.Graph(id='graph2-content'),
            ]),

    ])



@callback(
   Output('graph-content', 'figure'),
   Input('dropdown-selection', 'value'))

def update_graph(value):
    transport = df[["CensusRegion", "DB_Transport"]]
    dff = transport[transport.CensusRegion == value]
    nrows = dff.shape[0]

    fig = px.histogram(dff, x="DB_Transport",
                    labels={"DB_Transport": "Method", "count": "Count"},
                    title="How Diaper Bank Recipients Access their Diaper Bank",
                    color_discrete_map={'DB_Transport': '#86bce8'})

    fig.update_traces(marker=dict(color='#86bce8'))
    fig.update_layout(
        yaxis_title="Count",
        annotations=[dict(text=f"Figure has a total of {nrows} values")]
    )

    return fig

@callback(
   Output('graph2-content', 'figure'),
   Input('variable', 'value'))



def display_choropleth(variable):
    if str(variable) == "NumKidsDiapers":
        dff = df[['State', str(variable)]].groupby(['State']).mean().reset_index()
        return px.choropleth(dff, locations='State',
                             locationmode="USA-states",
                             color='NumKidsDiapers',
                             labels={"NumKidsDiapers": "# of Kids"},
                             title='Average number of kids in diapers (per household)',
                             scope="usa",
                             hover_data=['State', 'NumKidsDiapers'],
                             color_continuous_scale='Viridis_r')

    if str(variable) == "NumAdults":
        dff = df.loc[df['NumAdults'] == 1][['State', 'NumAdults']].groupby(['State']).sum().reset_index()
        return px.choropleth(dff, locations='State',
                             locationmode="USA-states",
                             color='NumAdults',
                             labels={"NumAdults": "# of Households"},
                             title='Number of households with a single head of household',
                             scope="usa",
                             hover_data=['State', 'NumAdults'],
                             color_continuous_scale='Viridis_r')


if __name__ == '__main__':
    app.run_server(debug=True)
