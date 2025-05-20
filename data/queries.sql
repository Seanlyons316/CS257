-- Query number 1: Show the countries and max height of tsunamis greater than 10 meters
SELECT tsunamis_place_time.COUNTRY, tsunamis_attribute.MAXIMUM_HEIGHT
FROM tsunamis_attribute, tsunamis_place_time
WHERE tsunamis_attribute.WAVE_ID = tsunamis_place_time.WAVE_ID
AND tsunamis_attribute.MAXIMUM_HEIGHT > 10
LIMIT 5;

-- Query number 2: Show Year and Country and Fatalities for each tsunami
SELECT tsunamis_place_time.wave_YEAR, tsunamis_place_time.COUNTRY, tsunamis_destruction.FATALITIES
FROM tsunamis_place_time, tsunamis_destruction
WHERE tsunamis_place_time.WAVE_ID = tsunamis_destruction.WAVE_ID
LIMIT 10;

-- Query number 3: show first 10 Japanese Tsunamis
SELECT tsunamis_place_time.wave_YEAR, tsunamis_place_time.COUNTRY, tsunamis_place_time.wave_LOCATION 
FROM tsunamis_place_time
WHERE tsunamis_place_time.COUNTRY = 'JAPAN'
ORDER BY tsunamis_place_time.wave_YEAR
LIMIT 10;

