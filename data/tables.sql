-- This file contains the SQL commands to create the tables for the tsunami database.
CREATE TABLE tsunami_attribute (
   SOURCE_ID integer NOT NULL,
   WAVE_ID integer NOT NULL,,
   DISTANCE_FROM_SOURCE integer NOT NULL,
   TRAVEL_TIME_HOURS integer,
   TRAVEL_TIME_MINUTES integer,
   VALIDITY integer,
   MEASUREMENT_TYPE integer,
   wave_PERIOD integer,
   FIRST_MOTION integer,
   MAXIMUM_HEIGHT real,
   HORIZONRTAL_INNUNDATION integer,
);
CREATE TABLE tsunami_destruction (
   WAVE_ID integer NOT NULL,
   INJURIES integer,
   INJURY_ESTIMATE integer,
   FATALITIES integer,
   FATALITY_ESTIMATE integer,
   DAMAGE_MILLIONS_DOLLARS integer,
   DAMAGE_ESTIMATE integer,
   HOUSES_DAMAGED integer,
   HOUSE_DAMAGE_ESTIMATE integer,
   HOUSES_DESTROYED integer,
   HOUSE_DESTRUCTION_ESTIMATE integer,
);

CREATE TABLE tsunami_place_time (
   WAVE_ID integer NOT NULL,
   wave_YEAR integer NOT NULL,
   wave_MONTH text,
   wave_DAY integer,
   REGION_CODE integer,
   COUNTRY text,
   wave_STATE/PROVINCE text,
   wave_LOCATION text,
   LATITUDE real NOT NULL,
   LONGITUDE real NOT NULL,
);

CREATE TABLE tsunami_ids (
   SOURCE_ID integer NOT NULL,
   WAVE_ID integer NOT NULL,
);

-- CREATE TABLE sources (
-- SOURCE_ID integer NOT NULL,
-- SOURCE_YEAR integer,
-- SOURCE_MONTH integer,
-- SOURCE_HOUR integer,MINUTE integer,
-- CAUSE integer,
-- VALIDITY integer,
-- FOCAL_DEPTH integer,
-- PRIMARY_MAGNITUDE real,
-- REGION_CODE integer,
-- COUNTRY text,
-- STATE_PROVINCE text,
-- source_LOCATION text,
-- LATITUDE real,
-- LONGITUDE real,
-- MAXIMUM_HEIGHT real,
-- MAGNITUDE_ABE real,
-- MAGNITUDE_IIDA real,
-- INTENSITY_SOLOVIEV integer,
-- WARNING_STATUS integer,
-- MISSING integer,
-- MISSING_ESTIMATE integer,
-- INJURIES integer,
-- INJURY_ESTIMATE integer,
-- FATALITIES integer,
-- FATALITY_ESTIMATE integer,
-- DAMAGE_MILLIONS_DOLLARS real,
-- DAMAGE_ESTIMATE integer,
-- HOUSES_DAMAGED integer,
-- HOUSE_DAMAGE_ESTIMATE integer,
-- HOUSES_DESTROYED integer,
-- HOUSE_DESTRUCTION_ESTIMATE integer,
-- ALL_MISSING integer,
-- MISSING_TOTAL integer,
-- ALL_INJURIES integer,
-- INJURY_TOTAL integer,
-- ALL_FATALITIES integer,
-- FATALITY_TOTAL integer,
-- ALL_DAMAGE_MILLIONS real,
-- DAMAGE_TOTAL integer,
-- ALL_HOUSES_DAMAGED integer,
-- HOUSE_DAMAGE_TOTAL integer,
-- ALL_HOUSES_DESTROYED integer
-- );

-- CREATE TABLE source_wave (
--     wave_id integer
-- );

