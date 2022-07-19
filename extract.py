# 
#
#
#
#

import requests
from bs4 import BeautifulSoup

sched_page = 'https://www.espn.com/college-football/schedule/_/week/'
week_num = 1

team_page = 'https://www.espn.com/college-football/team/_/id/166/'
team_id = 166

def make_request(top_lvl_page, sub_page):
    full_url = top_lvl_page + str(sub_page)
    req = requests.get(full_url)

    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

#print(make_request(sched_page, week_num))
#print(('\n\n'))
#print(make_request(team_page, team_id))