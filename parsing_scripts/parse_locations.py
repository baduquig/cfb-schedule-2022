# 
# 
# 
# 
# 
from tkinter import CURRENT
from urllib import response
import requests, pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=GABE_PC\SQLEXPRESS;Database=cfb_schedule;Trusted_Connection=yes')
cursor = conn.cursor()

def get_addresses():
    address_list = []
    cursor.execute('SELECT DISTINCT GAME_LOCATION FROM GAMES_GB;')
    for row in cursor:
        if row[0] == 'Acrisure Stadium, Pittsburgh, PA':
            row[0] = row[0].replace('Acrisure Stadium', 'Heinz field')

        address_list.append(row[0])
    return address_list

def get_city_state(stadium):
    idx = stadium.index(', ')
    stadium_city_state = stadium[idx + 2:]
    return stadium_city_state

def forward_geocode(stadium):
    forward_geocode = 'https://geocode.maps.co/search?q={' + stadium + '}'
    res = requests.get(forward_geocode)
    city_state = get_city_state(stadium)

    if(len(res.json()) == 0):
        res = requests.get('https://geocode.maps.co/search?q={' + city_state + '}')
    
    location_data = res.json()[0]

    country = location_data['display_name'].split(', ')[-1]
    
    if country == 'United States':
        lat = location_data['lat']
        lon = location_data['lon']

        city_st_ls = city_state.split(',')
        city = city_st_ls[0]
        state = city_st_ls[1]
        
        print('Latitude: {} | Longitude: {} | City: {} | State: {}'.format(lat, lon, city, state))
        cursor.execute('INSERT INTO LOCATIONS_GB (LOCATION_NAME, LATITUDE, LONGITUDE, CITY, STATE) VALUES (\'{}\', {}, {}, \'{}\', \'{}\')'
                        .format(stadium, lat, lon, city, state))
        cursor.commit()


stadiums = get_addresses()

for stadium in stadiums:
    forward_geocode(stadium)