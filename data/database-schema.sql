CREATE TABLE public.tsunamis_attribute (
    source_id real NOT NULL,
    wave_id real NOT NULL,
    distance_from_source real,
    travel_time_hours real,
    travel_time_minutes real,
    validity real,
    measurement_type real,
    wave_period real,
    first_motion real,
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
