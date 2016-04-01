#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json, math
from funciones import *

parser = argparse.ArgumentParser(description='Parsea un pcap y calcula la entropia')
parser.add_argument('-i', '--input-testname', required=True, type=file_pcap,
  help='nombre del testname (archivo pcap en la carpeta output)', metavar='FILE')
parser.add_argument('-v','--verbose', action='store_true', default=False)
args = parser.parse_args()

symbol_count = dict()
pkts_count = 0

def parse_ethertype(pkt):
    global pkts_count,symbol_count
    if args.verbose:
        pkt.show
    # check if field is type or payload size
    try:
        pkt_type = pkt.type
    except AttributeError:
        pkt_type = "802.3"
    pkts_count += 1
    symbol_count[pkt_type] = symbol_count.get(pkt_type, 0) + 1

# sniff
check_sudo()
from scapy.all import sniff
pkts = sniff(offline='../output/'+args.input_testname, store=0, prn=parse_ethertype)

symbol_frequency = {k: v/float(pkts_count) for k,v in symbol_count.items()}
symbol_information = {k: -(math.log(v, 2)) for k,v in symbol_frequency.items()}
source_entropy = sum({k: (v * symbol_information[k]) 
  for k,v in symbol_frequency.items()}.values())

result = {
  'symbol_frequency': symbol_frequency,
  'symbol_information': symbol_information,
  'source_entropy': source_entropy
}

with open(output_testtype_ext(args.input_testname,'s','json'), 'w') as f:
  f.write(json.dumps(result))
