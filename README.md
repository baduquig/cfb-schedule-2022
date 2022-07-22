# cfb-schedule-2022
Project repository to practice web scraping, data wrangling and transformation, and geographical data visualization for NCAA FBS college football games in Fall 2022.

<br>
<br>

## Data source
[ESPN FBS (I-A) Conference Schedule](https://www.espn.com/college-football/schedule)

<u>Top level URL</u>: https://[]()www.espn.com/college-football/schedule


<u>Sub level URL</u>: https://[]()www.espn.com/college-football/schedule/_/week/**week number**


<br>
<br>

## Resources
- [GeeksforGeeks web scraping tutorial](https://www.geeksforgeeks.org/python-web-scraping-tutorial/)

<br>
<br>

## Tentative project schedule and tasks
----

<br>

# College football 2022 season project phases

<br>

## _Iteration 1_
__Phase 1 - Data model planning__
- Plan desired data/information for project
- Normalize data model
- Create and document ERD

__Phase 2 - High-level Web scraping__
- Locate web pages/URLs with FBS football schedules and associated data
- Research and get familiarized with web scraping in Python
- Write python web scraping script(s)

__Phase 3 - Data parsing__
- Limit web scraping scripts to relevant HTML elements/data fields
- Cleanse/prepare/transform data

<br>

## _Iteration 2_

__Phase 4 - Database creation__
- Update ERD as needed
- Create database and tables

__Phase 5 - Data load__
- Locate latitude/longitude API for game locations
- Create team-conference dictionary
- Insert parsed data into database

__Phase 6 - Visualization skeleton__
- Research US geography data visualization in Python
- Create skeleton dashboard
- Create views/stored procedures for location-based data points

## _Iteration 3_

__Phase 7 - Polish visualization__
- Display additional data on hover action
- Improve styling
- Additional cleanup, shakeout
