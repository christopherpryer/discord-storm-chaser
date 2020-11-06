# TODO: scrape

COORDINATES = [
    # EPIC
    {"lat": 41.109641, "lon": -75.652588, "mtn": "jfbb pa"},
    {"lat": 42.176219, "lon": -74.225728, "mtn": "hunter ny"},
    {"lat": 42.959732, "lon": -72.924865, "mtn": "mt snow vt"},
    {"lat": 44.528920, "lon": -72.800973, "mtn": "stowe vt"},
    {"lat": 43.410329, "lon": -72.747451, "mtn": "okemo vt"},
    {"lat": 44.924510, "lon": -72.523740, "mtn": "jay peak vt"},
    {"lat": 44.924510, "lon": -72.523740, "mtn": "jay vt"},
    {"lat": 44.070258, "lon": -71.222398, "mtn": "attitash nh"},
    {"lat": 43.005875, "lon": -71.879827, "mtn": "crotched nh"},
    {"lat": 44.250096, "lon": -71.219147, "mtn": "wildcat, nh"},
    {"lat": 43.321843, "lon": -72.071415, "mtn": "mt sunapee nh"},
    {"lat": 39.758995, "lon": -77.368938, "mtn": "liberty pa"},
    {"lat": 39.742025, "lon": -77.935373, "mtn": "whitetail pa"},
    {"lat": 40.106815, "lon": -76.925932, "mtn": "roundtop pa"},
    {"lat": 39.471854, "lon": -106.079110, "mtn": "breck co"},
    {"lat": 39.579715, "lon": -105.941400, "mtn": "keystone co"},
    {"lat": 50.085187, "lon": -122.896886, "mtn": "whistler bc"},
]

LOOKUP = {c["mtn"].lower(): {"lat": c["lat"], "lon": c["lon"]} for c in COORDINATES}
