from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import pyodbc

app = Dash(__name__)

# Instantiate database connection
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=GABE_PC\SQLEXPRESS;Database=cfb_schedule;Trusted_Connection=yes')
cursor = conn.cursor()

# Instantiate games data frame
sql_select = 'SELECT * FROM GET_ALL_GAMES_VW;'
df = pd.read_sql(sql_select, conn)
print(list(df['WEEK_NUM']))
# Instantiate initial dropdown values
weeks = df['WEEK_NUM'].unique()
conferences = df['HOME_CONFERENCE'].unique()


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
                                    id='week',
                                    multi=True
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
        dcc.Graph()

    ]# end 'app-container' div
)# end app.layout


#~~~ Callbacks ~~~#

# Game dates dropdown list
@app.callback(
    Output('day', 'options'),
    Input('week', 'value'),
    prevent_initial_call=True
)
def set_gamedate_options(selected_weeks):
    weeks = df[df['WEEK_NUM'].isin(selected_weeks)]
    dates = weeks['GAME_DAY'].unique()
    return dates

#~~~ Callbacks ~~~#


if __name__ == '__main__':
    app.run_server(debug=True)