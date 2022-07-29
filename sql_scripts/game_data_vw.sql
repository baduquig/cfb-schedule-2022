
SELECT
	G.WEEK_NUM,
	G.GAME_DAY,
	G.GAME_TIME,
	AWY.SCHOOL_NAME,
	AWY.SCHOOL_MASCOT,
	AWY_CONF.CONFERENCE_NAME,
	HOM.SCHOOL_NAME,
	HOM.SCHOOL_MASCOT,
	HOM_CONF.CONFERENCE_NAME,
	G.GAME_LOCATION,
	LOC.LATITUDE,
	LOC.LONGITUDE
FROM
	GAMES_GB G
		LEFT JOIN TEAMS_GB AWY
			ON G.AWAY_TEAM = AWY.TEAM_ID
		LEFT JOIN CONFERENCES_GB AWY_CONF
			ON AWY.CONFERENCE_ID = AWY_CONF.CONFERENCE_ID
		LEFT JOIN TEAMS_GB HOM
			ON G.AWAY_TEAM = HOM.TEAM_ID
		LEFT JOIN CONFERENCES_GB HOM_CONF
			ON HOM.CONFERENCE_ID = HOM_CONF.CONFERENCE_ID
		LEFT JOIN LOCATIONS_GB LOC
			ON G.GAME_LOCATION = LOC.LOCATION_NAME;


