from datetime import datetime, timedelta, timezone

from tatc import utils
from tatc.schemas import TwoLineElements, Instrument, Satellite, Point
from tatc.analysis import collect_observations

# TLE from Moodle
tle = [
    "1 43013U 17073A   22195.78278435  .00000038  00000+0  38919-4 0  9996",
    "2 43013  98.7169 133.9110 0001202  63.8768 296.2532 14.19561306241107",
]

# Instrument settings from Moodle
instrument_altitude = 466_000      # meters
swath_width = 1_500_000            # meters

field_of_regard = utils.swath_width_to_field_of_regard(
    instrument_altitude,
    swath_width
)

instrument = Instrument(
    name="PBL_DIAL",
    field_of_regard=field_of_regard
)

satellite = Satellite(
    name="PBLObserver",
    orbit=TwoLineElements(tle=tle),
    instruments=[instrument]
)

# ARM SGP site in Oklahoma
sgp = Point(
    id=0,
    latitude=36.61,
    longitude=-97.49
)

# Mission window from Moodle
start = datetime(2026, 7, 14, 12, 0, 0, tzinfo=timezone.utc)
end = start + timedelta(days=10)

# Collect observation windows
results = collect_observations(sgp, satellite, start, end, instrument_index=0)

print("Field of regard [deg]:", field_of_regard)
print("Number of observation windows:", len(results))
print(results[["start", "end", "epoch", "sat_alt", "sat_az"]])
