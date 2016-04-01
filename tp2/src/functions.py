import json, os, pygmaps, random

from collections import defaultdict
from geoip import geolite2

def check_sudo():
    'checks sudo'
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        # Linux
        if os.getuid() != 0:
            raise RuntimeError("\n\nYou need to run this script with sudo!")
    #elif _platform == "darwin":
        # MAC OS X
    #elif _platform == "win32":
        # Windows

# FIXME: memoize with decorator
def get_coords(ip):
    match = geolite2.lookup(ip)
    if match is None:
        return None
    return match.location
        
BASE_WEIGHT = 10.0
        
def plot_routes(input_file, output_file):
    'plots routes with different weights on a google map'
    route_map = pygmaps.maps(37.428, -122.145, 3)

    with open(input_file) as f:
        data = json.loads(f.read())

    previous_node = (-34.5450875, -58.4395502)

    hopn = 0

    route_map.addpoint(previous_node[0], previous_node[1], title=str(hopn))
                
    for hop in data:
        hopn += 1
        n = len(hop)
        freqs = defaultdict(int)
        for med in hop:
            ip = med['ip']
            hostname = med['hostname']
            freqs[ip] += 1
        for ip, freq in freqs.items():
            if ip == '*': continue
            coords = get_coords(ip)
            if coords is None: continue
            path = [previous_node, coords]
            weight = BASE_WEIGHT * float(freq) / n
            route_map.addpath(path, "#FF0000", weight)
            route_map.addpoint(coords[0] + random.random(), coords[1] + random.random(), title=str(hopn))

        sorted_freqs = freqs.items()
        sorted_freqs.sort(key=lambda x: x[1], reverse=True)
        most_frequent_ip = sorted_freqs[0][0]
        if most_frequent_ip == '*': continue
        coords = get_coords(most_frequent_ip)
        if coords is not None:
            previous_node = coords
        
    route_map.draw(output_file)
