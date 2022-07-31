from dash import Dash, html, dcc, Input, Output
import datetime
import plotly.graph_objects as go
import pandas as pd
import pyodbc

app = Dash(__name__)

# Instantiate database connection
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=GABE_PC\SQLEXPRESS;Database=cfb_schedule;Trusted_Connection=yes')
cursor = conn.cursor()

# Instantiate games data frame
sql_select = 'SELECT * FROM GET_ALL_GAMES_VW;'
df = pd.read_sql(sql_select, conn)

# Instantiate initial dropdown values
weeks = df['WEEK_NUM'].unique()
conferences = df['HOME_CONFERENCE'].unique()

# Get current week
today = datetime.datetime.now()
first_week = datetime.datetime(2022, 9, 5)
default_week = 1
while today >= first_week:
    first_week += first_week + datetime.timedelta(days=7)
    default_week += 1


app.layout = html.Div(
    className='app-container',
    children=[

        # Header
        html.H1('College football schedule 2022'),

        # Inputs
        html.Div(
            className='inputs-div',
            children=[

                # Left DIVs
                html.Div(
                    className='time-entries',
                    children=[
                        # Week
                        html.Div(
                            className='week-div',
                            children=[
                                html.Label('Week'),
                                dcc.Dropdown(
                                    weeks,
                                    value=default_week,
                                    id='week'
                                )
                            ]
                        ),# end 'week-div' div

                        # Day
                        html.Div(
                            className='day-div',
                            children=[
                                html.Label('Day'),
                                dcc.Dropdown(
                                    id='day',
                                    multi=True
                                )
                            ]
                        )# end 'day-div' div
                    ]
                ), # end Left DIVs

                # Right DIVs
                html.Div(
                    className='school-entries',
                    children=[
                        # Conference
                        html.Div(
                            className='conf-div',
                            children=[
                                html.Label('Conference'),
                                dcc.Dropdown(
                                    conferences,
                                    id='conf',
                                    multi=True
                                )
                            ]
                        ),# end 'conf-div' div

                        # Day
                        html.Div(
                            className='team-div',
                            children=[
                                html.Label('Team'),
                                dcc.Dropdown(
                                    id='team',
                                    multi=True
                                )
                            ]
                        )# end 'team-div' div
                    ]
                ) # end Right DIVs

            ]
        ),

        # Map
        dcc.Graph(id='map')

    ]# end 'app-container' div
)# end app.layout


#~~~ Callbacks ~~~#

# Game dates dropdown list
@app.callback(
    Output('day', 'options'),
    Input('week', 'value'),
    prevent_initial_call=True
)
def set_gamedate_options(selected_week):
    weeks = df[df['WEEK_NUM'] == selected_week]
    dates = weeks['GAME_DAY'].unique()
    return dates


# Teams dropdown list
@app.callback(
    Output('team', 'options'),
    Input('conf', 'value'),
    prevent_initial_call=True
)
def set_gamedate_options(selected_conferences):
    conferences = df[df['HOME_CONFERENCE'].isin(selected_conferences)]
    teams = conferences['HOME_SCHOOL'].unique()
    return teams


@app.callback(
    Output('map', 'figure'),
    Input('week', 'value'),
    Input('conf', 'value'),
    Input('day', 'value'),
    Input('team', 'value')
)
def plot_games(selected_week, selected_conferences, selected_days, selected_teams):
    games = df
    games = games[games['WEEK_NUM'] == selected_week]

    # only week chosen
    if((selected_conferences is None or selected_conferences == [])
    and (selected_days is None or selected_days == [])
    and (selected_teams is None or selected_teams == [])):
        pass
    # only week and conference chosen
    elif ((selected_days is None or selected_days == [])
    and (selected_teams is None or selected_teams == [])):
        games = games[games['AWAY_CONFERENCE'].isin(selected_conferences)
                or games['HOME_CONFERENCE'].isin(selected_conferences)]
    # only team blank
    elif (selected_teams is None or selected_teams == []):
        games = games[games['GAME_DAY'].isin(selected_days)]
        games = games[games['AWAY_CONFERENCE'].isin(selected_conferences)
                or games['HOME_CONFERENCE'].isin(selected_conferences)]
    # only day blank
    elif (selected_days is None or selected_days == []):
        games = games[games['AWAY_CONFERENCE'].isin(selected_conferences)
                or games['HOME_CONFERENCE'].isin(selected_conferences)]
        games = games[games['AWAY_TEAM'].isin(selected_teams)
                or games['HOME_TEAM'].isin(selected_teams)]
    else:
        games = games[games['GAME_DAY'].isin(selected_days)]
        games = games[games['AWAY_CONFERENCE'].isin(selected_conferences)
                or games['HOME_CONFERENCE'].isin(selected_conferences)]
        games = games[games['AWAY_TEAM'].isin(selected_teams)
                or games['HOME_TEAM'].isin(selected_teams)]
    
    fig = go.Figure(data=go.Scattergeo(
        locationmode='USA-states',
        lat=games['LATITUDE'],
        lon=games['LONGITUDE']
    ))
    fig.update_layout(
        geo = dict(
            scope='usa'
        )
    )

    return fig
#~~~ Callbacks ~~~#


if __name__ == '__main__':
    app.run_server(debug=True)