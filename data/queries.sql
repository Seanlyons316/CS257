-- Query number 1
SELECT tsunami_place_time.COUNTRY, tsunami_attribute.MAXIMUM_HEIGHT
FROM tsunami_attribute, tsunami_place_time
WHERE tsunami_attribute.WAVE_ID = tsunami_place_time.WAVE_ID
AND tsunami_attribute.MAXIMUM_HEIGHT > 10
LIMIT 5;

-- Query number 2
SELECT tsunami_place_time.wave_YEAR, tsunami_place_time.COUNTRY, tsunami_destruction.FATALITIES
FROM tsunami_place_time, tsunami_destruction
WHERE tsunami_place_time.WAVE_ID = tsunami_destruction.WAVE_ID;

-- Query number 3
SELECT tsunami_place_time.wave_YEAR, tsunami_place_time.COUNTRY, tsunami_place_time.wave_LOCATION
FROM tsunami_place_time
WHERE tsunami_place_time.COUNTRY = 'JAPAN'
ORDER BY tsunami_place_time.wave_YEAR;
 
