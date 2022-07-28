#
#
#
#
#
import requests, pyodbc
from bs4 import BeautifulSoup

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=GABE_PC\SQLEXPRESS;Database=cfb_schedule;Trusted_Connection=yes')
cursor = conn.cursor()

team_page = 'https://www.espn.com/college-football/team/_/id/'

conferene_dict = {
    'ACC': '1',
    'American': '151',
    'Big 12': '4',
    'Big Ten': '5',
    'C-USA': '12',
    'FBS Indep.': '18',
    'MAC': '15',
    'Mountain West': '17',
    'Pac-12': '9',
    'SEC': '8',
    'Sun Belt': '37'
}

def get_all_teams():
    team_id_list = []
    cursor.execute('SELECT DISTINCT HOME_TEAM FROM GAMES_GB;')
    for row in cursor:
        team_id_list.append(row[0])
    return team_id_list

def parse_team_page(team_id):
    team_url = team_page + str(team_id)
    req = requests.get(team_url)
    soup = BeautifulSoup(req.content, 'html.parser')

    standings_card_header = soup.find('section', class_='TeamStandings').find('h3').text
    conf_name = standings_card_header[5:].replace(' Standings', '')
    conf_id = conferene_dict[conf_name]
    
    school_header = soup.find('h1', class_='ClubhouseHeader__Name').find('span', class_='flex-wrap').find_all('span', class_='db')
    school_name = school_header[0].text
    school_mascot = school_header[1].text

    print('Team ID: {} | Conference ID: {} | School Name: {} | School Mascot: {}'.format(team_id, conf_id, school_name, school_mascot))
    cursor.execute('INSERT INTO TEAMS_GB (TEAM_ID, CONFERENCE_ID, SCHOOL_NAME, SCHOOL_MASCOT) VALUES ({}, {}, \'{}\', \'{}\')'
                    .format(team_id, conf_id, school_name.replace('\'', ''), school_mascot.replace('\'', '')))
    cursor.commit()


teams_list = get_all_teams()

for team in teams_list:
    parse_team_page(team)