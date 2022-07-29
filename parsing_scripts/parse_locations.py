# 
# 
# 
# 
# 
from operator import index
import requests, pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=GABE_PC\SQLEXPRESS;Database=cfb_schedule;Trusted_Connection=yes')
cursor = conn.cursor()

us_states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

def get_addresses():
    address_list = []
    cursor.execute('SELECT DISTINCT GAME_LOCATION FROM GAMES_GB;')
    for row in cursor:
        address_list.append(row[0])
    return address_list

def convert_abbr_to_state(city_st_str):
    try:
        st_idx = city_st_str.index(', ')
        st_abbr = city_st_str[st_idx + 2:]
        if st_abbr in us_states:
            converted_str = city_st_str.replace(st_abbr, us_states[st_abbr])
            return converted_str
        else:
            return city_st_str
    except:
        return city_st_str

def get_city_state(stadium):
    idx = stadium.index(', ')
    stadium_city_state = stadium[idx + 2:]
    converted_str = convert_abbr_to_state(stadium_city_state)
    print(converted_str)
    return converted_str

def forward_geocode(stadium):
    city_state = get_city_state(stadium)

    forward_geocode = 'https://geocode.maps.co/search?q={' + city_state + '}'
    req = requests.get(forward_geocode)

    location_data = req.json()[0]

    country = location_data['display_name'].split(', ')[-1]

    if country == 'United States':
        lat = location_data['lat']
        lon = location_data['lon']

        city_st_ls = city_state.split(', ')
        city = city_st_ls[0]
        state = city_st_ls[1]
        
        #print('Latitude: {} | Longitude: {} | City: {} | State: {}'.format(lat, lon, city, state))
        cursor.execute('INSERT INTO LOCATIONS_GB (LOCATION_NAME, LATITUDE, LONGITUDE, CITY, STATE) VALUES (\'{}\', {}, {}, \'{}\', \'{}\')'
                        .format(stadium, lat, lon, city, state))
        cursor.commit()
    else:
        print(stadium, ' ', country)


stadiums = get_addresses()

for stadium in stadiums:
    forward_geocode(stadium)