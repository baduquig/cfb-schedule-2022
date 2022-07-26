#
# Overarching schedule data all housed in <div id='sched-container'>...</div>
#
#
#
import requests, pyodbc
from bs4 import BeautifulSoup

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=GABE_PC\SQLEXPRESS;Database=cfb_schedule;Trusted_Connection=yes')
cursor = conn.cursor()

sched_page = 'https://www.espn.com/college-football/schedule/_/week/'
season_len = 13

def get_game_id(url_str):
    start_idx = url_str.rfind('/')
    game_id = url_str[start_idx + 1:]
    return game_id

def get_team_id(url_str):
    begin_idx = url_str.index('/id/')
    end_idx = url_str.rfind('/')
    team_id = url_str[begin_idx + 4:end_idx]
    return team_id

def convert_zulu_to_standard(z_time_str):
    colon_index = z_time_str.index(':')
    zulu_hour = int(z_time_str[:colon_index])
    zulu_min = z_time_str[colon_index + 1:]

    if zulu_hour < 6:
        zulu_hour += 4
        am_pm = 'PM'
    elif zulu_hour >= 6 and zulu_hour < 18:
        zulu_hour -= 6
        am_pm = 'AM'
    elif zulu_hour == 18:
        zulu_hour -= 7
        am_pm = 'AM'
    else:
        zulu_hour -= 18
        am_pm = 'PM'

    standard_time = str(zulu_hour) + ':' + str(zulu_min) + ' ' + am_pm
    return standard_time

def get_game_time(game_id):
    game_url = 'https://www.espn.com/college-football/game/_/gameId/' + game_id
    r = requests.get(game_url)
    sp = BeautifulSoup(r.content, 'html.parser')

    gm_sts = sp.find('div', class_='game-status').findAll('span')[1].attrs
    game_dttm = gm_sts.get('data-date')
    
    if game_dttm == None:
        game_time = 'TBD'
    else:
        begin_idx = game_dttm.index('T')
        end_idx = game_dttm.index('Z')
        game_time_zulu = game_dttm[begin_idx + 1:end_idx]
        game_time = convert_zulu_to_standard(game_time_zulu)

    return game_time

def parse_schedule_page(season_len, sched_page):
    cursor.execute('EXEC drop_tables; EXEC create_schedule_db;')
    cursor.commit()

    for week in range(season_len):
        req = requests.get(sched_page + str(week + 1))
        soup = BeautifulSoup(req.content, 'html.parser')

        sched_container = soup.find('div', id='sched-container')
        for game_days in sched_container.find_all('h2', class_='table-caption'):
            game_day = game_days.text
            game_date = game_days.find_next_sibling('div').find('tbody').find_all('tr')
            
            for game in game_date:
                game_data = game.find_all('td')
                
                away_team_id = get_team_id(game_data[0].find('a', class_='team-name', href=True)['href'])
                home_team_id = get_team_id(game_data[1].find('a', class_='team-name', href=True)['href'])
                #away_team_name = game_data[0].find('span').text
                #home_team_name = game_data[1].find('span').text
                game_id = get_game_id(game_data[2].find('a', href=True)['href'])
                location = game_data[5].text
                game_week_num = week + 1
                game_time = get_game_time(game_id)
                
                print('Game week: {} | Game day: {} | Game ID: {} | Away Team ID: {} | Home Team ID: {} | Location: {} | Game time: {}'
                        .format(game_week_num, game_day, game_id, away_team_id, home_team_id, location, game_time))
                
                cursor.execute('INSERT INTO GAMES_GB (GAME_ID, AWAY_TEAM, HOME_TEAM, GAME_LOCATION, GAME_DAY, GAME_TIME, WEEK_NUM) VALUES ({}, {}, {}, \'{}\', \'{}\', \'{}\', {})'
                                .format(game_id, away_team_id, home_team_id, location, game_day, game_time, game_week_num))
                cursor.commit()
                
        print()
    print()
    print()

parse_schedule_page(season_len, sched_page)