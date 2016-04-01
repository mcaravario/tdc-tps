#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json, math, pprint
from funciones import *

parser = argparse.ArgumentParser(description='Parsea un pcap y calcula la entropia')
parser.add_argument('-i', '--input-testname', required=True, type=file_pcap,
                    help='nombre del testname (archivo pcap en la carpeta output)', metavar='FILE')
parser.add_argument('-v','--verbose', action='store_true', default=False)
args = parser.parse_args()

symbol_count = dict()
pkts_count = 0

def parse_art(pkt):
    global pkts_count,symbol_count
    if ARP in pkt: #and pkt[ARP].op in (1,2): #who-has or is-at
        ip_dst = pkt.pdst
        pkts_count += 1
        symbol_count[ip_dst] = symbol_count.get(ip_dst, 0) + 1
        if args.verbose:
            pkt.show()

# sniff
check_sudo()
from scapy.all import sniff,ARP
pkts = sniff(offline='../output/'+args.input_testname, filter="arp", store=0, prn=parse_art)

symbol_frequency = {k: v/float(pkts_count) for k,v in symbol_count.items()}
symbol_information = {k: -(math.log(v, 2)) for k,v in symbol_frequency.items()}
source_entropy = sum({k: (v * symbol_information[k]) 
                      for k,v in symbol_frequency.items()}.values())

result = {
    'symbol_frequency': symbol_frequency,
    'symbol_information': symbol_information,
    'source_entropy': source_entropy
}

with open(output_testtype_ext(args.input_testname,'s1','json'), 'w') as f:
    f.write(json.dumps(result, indent=4))
