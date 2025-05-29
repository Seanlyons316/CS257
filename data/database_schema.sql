CREATE TABLE public.tsunamis_attribute (
    wave_id real NOT NULL,
    source_id real NOT NULL,
    distance_from_source real,
    travel_time_hours real,
    travel_time_minutes real,
    validity text,
    measurement_type real,
    wave_period real,
    first_motion text,
    maximum_height real,
    horizonrtal_innundation real
);


--
-- Name: tsunamis_destruction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tsunamis_destruction (
    wave_id real NOT NULL,
    injuries real,
    injury_estimate real,
    fatalities real,
    fatality_estimate real,
    damage_millions_dollars real,
    damage_estimate real,
    houses_damaged real,
    house_damage_estimate real,
    houses_destroyed real,
    house_destruction_estimate real
);


--
-- Name: tsunamis_ids; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tsunamis_ids (
    source_id real NOT NULL,
    wave_id real NOT NULL
);


--
-- Name: tsunamis_place_time; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tsunamis_place_time (
    wave_id real NOT NULL,
    region_code real,
    country text,
    wave_year real NOT NULL,
    wave_month text,
    wave_day real,
    wave_state text,
    wave_location text,
    latitude real,
    longitude real
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

