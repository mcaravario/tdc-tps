#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json
from funciones import *

# parse the arguments
parser = argparse.ArgumentParser(description='Parsea un json e imprime un histograma')
parser.add_argument('-i', '--input-testname', required=True, type=file_json_s1,
  help='nombre del testname (archivo json en la carpeta output)', metavar='FILE')
args = parser.parse_args()
output_file = output_testtype_ext(args.input_testname,'pie','png')

# parse the json input file
with open(args.input_testname) as f:
    data = json.loads(f.read())

# generate plot data
execfile('plot-functions.py')
symbol_frequency = data['symbol_frequency']
symbol_information = data['symbol_information']
source_entropy = data['source_entropy']

symbols = [k for k,v in symbol_information.items()]
freqs = [symbol_frequency[k] for k,v in symbol_information.items()]

labels = [unused_letter() if info < source_entropy else ''
          for sym, info in symbol_information.items()]

# plot
import matplotlib.pyplot as plt
plt.pie(freqs, labels=labels)
plt.savefig(output_file)

