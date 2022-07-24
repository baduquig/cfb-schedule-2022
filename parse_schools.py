#
#
#
#
#
import requests
from bs4 import BeautifulSoup

team_page = 'https://www.espn.com/college-football/team/_/id/'
team_id_list = []

conferene_dict = {
    '1': 'ACC',
    '151': 'American',
    '4': 'Big 12',
    '5': 'Big Ten',
    '12': 'C-USA',
    '18': 'FBS Indep.',
    '15': 'MAC',
    '17': 'Mountain West',
    '9': 'Pac-12',
    '8': 'SEC',
    '37': 'Sun Belt',
    '': ''
}

def parse_team_page(team_id):
    team_url = team_page + team_id
    req = requests.get(team_url)
    soup = BeautifulSoup(req.content, 'html.parser')

