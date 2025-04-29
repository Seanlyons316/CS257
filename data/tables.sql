CREATE TABLE tsunami_attribute (
   SOURCE_ID real NOT NULL,
   WAVE_ID real NOT NULL,,
   DISTANCE_FROM_SOURCE real NOT NULL,
   TRAVEL_TIME_HOURS real,
   TRAVEL_TIME_MINUTES real,
   VALIDITY real,
   MEASUREMENT_TYPE real,
   wave_PERIOD real,
   FIRST_MOTION real,
   MAXIMUM_HEIGHT real,
   HORIZONRTAL_INNUNDATION real,
);
CREATE TABLE tsunami_destruction (
   WAVE_ID real NOT NULL,
   INJURIES real,
   INJURY_ESTIMATE real,
   FATALITIES real,
   FATALITY_ESTIMATE real,
   DAMAGE_MILLIONS_DOLLARS real,
   DAMAGE_ESTIMATE real,
   HOUSES_DAMAGED real,
   HOUSE_DAMAGE_ESTIMATE real,
   HOUSES_DESTROYED real,
   HOUSE_DESTRUCTION_ESTIMATE real,
);

CREATE TABLE tsunami_place_time (
   WAVE_ID real NOT NULL,
   wave_YEAR real NOT NULL,
   wave_MONTH text,
   wave_DAY real,
   REGION_CODE real,
   COUNTRY text,
   wave_STATE/PROVINCE text,
   wave_LOCATION text,
   LATITUDE real NOT NULL,
   LONGITUDE real NOT NULL,
);

CREATE TABLE tsunami_ids (
   SOURCE_ID real NOT NULL,
   WAVE_ID real NOT NULL,
);

-- CREATE TABLE sources (
-- SOURCE_ID real NOT NULL,
-- SOURCE_YEAR real,
-- SOURCE_MONTH real,
-- SOURCE_HOUR real,MINUTE real,
-- CAUSE real,
-- VALIDITY real,
-- FOCAL_DEPTH real,
-- PRIMARY_MAGNITUDE real,
-- REGION_CODE real,
-- COUNTRY text,
-- STATE_PROVINCE text,
-- source_LOCATION text,
-- LATITUDE real,
-- LONGITUDE real,
-- MAXIMUM_HEIGHT real,
-- MAGNITUDE_ABE real,
-- MAGNITUDE_IIDA real,
-- INTENSITY_SOLOVIEV real,
-- WARNING_STATUS real,
-- MISSING real,
-- MISSING_ESTIMATE real,
-- INJURIES real,
-- INJURY_ESTIMATE real,
-- FATALITIES real,
-- FATALITY_ESTIMATE real,
-- DAMAGE_MILLIONS_DOLLARS real,
-- DAMAGE_ESTIMATE real,
-- HOUSES_DAMAGED real,
-- HOUSE_DAMAGE_ESTIMATE real,
-- HOUSES_DESTROYED real,
-- HOUSE_DESTRUCTION_ESTIMATE real,
-- ALL_MISSING real,
-- MISSING_TOTAL real,
-- ALL_INJURIES real,
-- INJURY_TOTAL real,
-- ALL_FATALITIES real,
-- FATALITY_TOTAL real,
-- ALL_DAMAGE_MILLIONS real,
-- DAMAGE_TOTAL real,
-- ALL_HOUSES_DAMAGED real,
-- HOUSE_DAMAGE_TOTAL real,
-- ALL_HOUSES_DESTROYED real
-- );

-- CREATE TABLE source_wave (
--     wave_id real
-- );

