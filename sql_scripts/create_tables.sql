USE [CFB_SCHEDULE]
GO
/****** Object:  StoredProcedure [dbo].[create_schedule_db]    Script Date: 7/25/2022 6:09:50 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


ALTER PROCEDURE [dbo].[create_schedule_db]

AS


CREATE TABLE GAMES_GB (
	GAME_ID				INT			NOT NULL	PRIMARY KEY,
	AWAY_TEAM			INT			NOT NULL,
	HOME_TEAM			INT			NOT NULL,
	GAME_LOCATION		VARCHAR(64) NOT NULL,
	GAME_DAY			VARCHAR(32) NULL,
	GAME_TIME			VARCHAR(16)	NULL,
	WEEK_NUM			TINYINT		NULL
);

CREATE TABLE TEAMS_GB (
	TEAM_ID				INT			NOT NULL	PRIMARY KEY,
	CONFERENCE_ID		TINYINT		NOT NULL,
	SCHOOL_NAME			VARCHAR(64) NULL,
	SCHOOL_MASCOT		VARCHAR(64) NULL
);

CREATE TABLE CONFERENCES_GB (
	CONFERENCE_ID		TINYINT		NOT NULL	PRIMARY KEY,
	CONFERENCE_NAME		VARCHAR(32) NULL
);

CREATE TABLE LOCATIONS_GB (
	LOCATION_NAME		VARCHAR(64)		NOT NULL	PRIMARY KEY,
	LATITUDE			DECIMAL(8,5)	NOT NULL,
	LONGITUDE			DECIMAL(8,5)	NOT NULL,
	CITY				VARCHAR(64)		NULL,
	STATE				VARCHAR(32)		NULL
);



