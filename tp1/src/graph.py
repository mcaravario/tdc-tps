#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json, math, pprint
from funciones import *

parser = argparse.ArgumentParser(description='Parsea un pcap y calcula la entropia')
parser.add_argument('-i', '--input-testname', required=True, type=file_pcap,
                    help='nombre del testname (archivo pcap en la carpeta output)', metavar='FILE')
parser.add_argument('-v','--verbose', action='store_true', default=False)
args = parser.parse_args()

# sniff
# check_sudo()
from scapy.all import sniff
pkts = sniff(offline='../output/'+args.input_testname)

adjacency = {}

for pkt in pkts:
    if not "ARP" in pkt: pass
    src, dst = pkt.src, pkt.dst
    if not src in adjacency:
        adjacency[src] = {}
    if not dst in adjacency[src]:
        adjacency[src][dst] = 0
    adjacency[src][dst] += 1

edges = []
nodes = set()

for u, adj in adjacency.items():
    for v, count in adj.items():
        nodes.add(u)
        nodes.add(v)

nodes = list(nodes)

def get_node(mac):
    return nodes.index(mac)


for u, adj in adjacency.items():
    for v, count in adj.items():
        edges.append({
            'source': get_node(u),
            'target': get_node(v),
            'value': count
        })

nodes = [{} for n in nodes]
    
result = {
    'nodes': nodes,
    'links': edges
}
        
with open(output_testtype_ext(args.input_testname,'graph','json'), 'w') as f:
    f.write(json.dumps(result, indent=4))
