#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, sys, os
from funciones import *

# verifies that the protocol parameter is valid
def protocol_ok(x):
  protocols = ['tcp','icmp','arp','udp','']
  if not x in protocols:
    parser.error('Invalid protocol. Valids protocols are: %s'%str(protocols))
  return x

# verifies that testname parameter is valid
def file_ok(x):
  if '/' in x or '.' in x:
    parser.error('''Invalid testname.
      Please, don't use "/" nor "." in your testname.
      Valid testnames, ie: "shopping1", "trabajo5", "casa2", etc.''')
  y = '../output/'+x+'.pcap'
  return y

# sniffer callback for every packet
def sniff_callback(packet):
  if args.verbose:
    packet.show()

parser = argparse.ArgumentParser(description='''network traffic capture 
  (a.k.a. sniffing) tool.''',
  epilog='''If you set max_running_time=0, there will be no time limit.
  If you set max_running_packets=0, there will be no packets limit.
  (but you can't set both at the same time).''')
parser.add_argument('-t', '--max-running-time', required=True, type=int, 
  help='max running time in seconds')
parser.add_argument('-p', '--max-captured-packets', required=True, type=int, 
  help='max captured packets')
parser.add_argument('-o', '--output-testname', required=True, type=file_ok,
  help='non-existent testname to save the sniffing output', metavar='FILE')
parser.add_argument('--overwrite', dest='overwrite_output_file',
  action='store_true', default=False, help='overwrite file if already exists')
parser.add_argument('-f','--filter-protocol', type=protocol_ok)
parser.add_argument('-v','--verbose', action='store_true', default=False,
  help='set verbose mode')

args = parser.parse_args()

outputfile = output_testtype_ext(args.output_testname, 
  str(args.max_running_time),'pcap')

# Check if output file exists
if not args.overwrite_output_file:
  if os.path.isfile(outputfile) or os.path.exists(outputfile):
    parser.error('''The file {} already exists.
    Please, use a non-existent path'''.format(outputfile))

# Parse the filter limits
if args.max_running_time <= 0 and args.max_captured_packets <= 0:
  parser.error('''Can't set no "max running time limit" and no "max captured 
  packets limit" at the same time. You need to provide at least one positive 
  limit.''')
if args.max_running_time <= 0:
  args.max_running_time = None
if args.max_captured_packets <= 0:
  args.max_captured_packets = None

# Print capture status
print '''capturing packets with parameters:
    max_running_time=%s, max_captured_packets=%s
    output_testname=%s, overwrite=%s
    filter_protocol=%s
    verbose=%s'''%(
  args.max_running_time, args.max_captured_packets, args.output_testname,
  args.overwrite_output_file, args.filter_protocol, args.verbose)

# Sniff
from scapy.all import sniff,wrpcap
if not args.verbose:
  pkts = sniff(count=args.max_captured_packets, timeout=args.max_running_time,
    filter=args.filter_protocol, offline=args.output_testname)
else:
  pkts = sniff(count=args.max_captured_packets, timeout=args.max_running_time,
    filter=args.filter_protocol, prn=sniff_callback, offline=args.output_testname)

# Save sniffing output
if pkts == []:
  print "sorry, no packets captured :(\ntry with a higher running time"
else:
  wrpcap(outputfile,pkts)
  print 'output saved in file {}'.format(outputfile)

