#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json
from funciones import *

# parse the arguments
parser = argparse.ArgumentParser(description='Parsea un json e imprime un histograma')
parser.add_argument('-i', '--input-testname', required=True, type=file_json_s,
  help='nombre del testname (archivo json en la carpeta output)', metavar='FILE')
args = parser.parse_args()
output_file = output_testtype_ext(args.input_testname,'pie','png')

# parse the json input file
with open(args.input_testname) as f:
    data = json.loads(f.read())

# generate plot data
execfile('plot-functions.py')
symbol_frequency = data['symbol_frequency']
symbols, freqs = zip(*(symbol_frequency.items()))
protocols = [get_protocol_title(s) for s in symbols]

# plot
import matplotlib.pyplot as plt
plt.pie(freqs, labels=protocols)
plt.legend()
plt.savefig(output_file)
