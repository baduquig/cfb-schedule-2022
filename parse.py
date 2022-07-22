#
# Overarching schedule data all housed in <div id='sched-container'>...</div>
#
#
#

from datetime import date
import html
from random import betavariate
from turtle import home
from numpy import printoptions
import requests
from bs4 import BeautifulSoup

sched_page = 'https://www.espn.com/college-football/schedule/_/week/'
team_page = 'https://www.espn.com/college-football/team/_/id/'
season_len = 1

def get_game_id(url_str):
    start_idx = url_str.rfind('/')
    game_id = url_str[start_idx + 1:]
    return game_id

def get_team_id(url_str):
    begin_idx = url_str.index('/id/')
    end_idx = url_str.rfind('/')
    team_id = url_str[begin_idx + 4:end_idx]
    return team_id

def get_game_time(html_td_str):
    start_idx = html_td_str.rfind('/')
    game_url = 'https://www.espn.com/college-football/game/_/gameId/' + html_td_str[start_idx + 1:]
    r = requests.get(game_url)
    sp = BeautifulSoup(r.content, 'html.parser')
    gm_sts = sp.find('div', class_='game-status').findAll('span')[1].attrs
    game_dttm = gm_sts.get('data-date')
    
    if game_dttm == None:
        game_time = 'TBD'
    else:
        begin_idx = game_dttm.index('T')
        end_idx = game_dttm.index('Z')
        game_time = game_dttm[begin_idx + 1:end_idx]
    return game_time

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
            game_id = get_game_id(game_data[2].find('a', href=True)['href'])
            location = game_data[5].text
            game_week_num = week + 1
            game_time = get_game_time(game_data[2].find('a', href=True)['href'])

            away_team_name = game_data[0].find('span').text
            home_team_name = game_data[1].find('span').text
        
            print('GameID: {} | Week: {} | Gameday: {} | Away team ID: {} | Away team: {} | Home team ID: {} | Home team: {} | Location: {} | Time: {}'
            .format(game_id, game_week_num, game_day, away_team_id, away_team_name, home_team_id, home_team_name, location, game_time))
            
    print('\n\n')