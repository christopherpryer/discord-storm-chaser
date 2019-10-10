coordinates = [
{'lat': 41.109641, 'lon': -75.652588, 'mtn': 'Jfbb, PA'},
{'lat': 42.176219, 'lon': -74.225728, 'mtn': 'Hunter, NY'},
{'lat': 42.959732, 'lon': -72.924865, 'mtn': 'Mt Snow, VT'},
{'lat': 44.528920, 'lon': -72.800973, 'mtn': 'Stowe, VT'},
{'lat': 43.410329, 'lon': -72.747451, 'mtn': 'Okemo, VT'},
{'lat': 44.924510, 'lon': -72.523740, 'mtn': 'Jay, VT'},
{'lat': 44.070258, 'lon': -71.222398, 'mtn': 'Attitash, NH'},
{'lat': 43.005875, 'lon': -71.879827, 'mtn': 'Crotched, NH'},
{'lat': 44.250096, 'lon': -71.219147, 'mtn': 'Wildcat, NH'},
{'lat': 43.321843, 'lon': -72.071415, 'mtn': 'Mt Sunapee, NH'},
{'lat': 39.758995, 'lon': -77.368938, 'mtn': 'Liberty, PA'},
{'lat': 39.742025, 'lon': -77.935373, 'mtn': 'Whitetail, PA'},
{'lat': 40.106815, 'lon': -76.925932, 'mtn': 'Roundtop, PA'},
{'lat': 39.471854, 'lon': -106.079110, 'mtn': 'Breck, CO'},
{'lat': 39.579715, 'lon': -105.941400, 'mtn': 'Keystone, CO'},
{'lat': 50.085187, 'lon': -122.896886, 'mtn': 'Whistler, BC'}]

lookup = \
    {c['mtn'].upper(): {'lat': c['lat'], 'lon': c['lon']} for c in coordinates}
