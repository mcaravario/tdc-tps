#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json, sys
from funciones import *

# parse the arguments
parser = argparse.ArgumentParser(description='Parsea un json e imprime un histograma')
parser.add_argument('-i', '--input-testname', required=True, type=file_json_s,
  help='nombre del testname (archivo json en la carpeta output)', metavar='FILE')
args = parser.parse_args()
output_file = output_testtype_ext(args.input_testname,'histogram','png')

# parse the json input file
with open(args.input_testname) as f:
    data = json.loads(f.read())
symbol_information = data['symbol_information']
symbol_frequency = data['symbol_frequency']
source_entropy = data['source_entropy']

# generate plot data
import numpy as np
execfile('plot-functions.py')
symbols, information = zip(*(symbol_information.items()))
protocols = [get_protocol_title(s) for s in symbols]
posicion_x = np.arange(len(protocols))

# plot
import matplotlib.pyplot as plt
width = 0.5
plt.bar(posicion_x, information, align='center', width=width)
plt.xticks(posicion_x, protocols)
plt.xlabel('Protocolo')
plt.title('Informacion segun protocolo')

plt.plot([0 - width / 2.0, posicion_x[-1] + width / 2.0], [source_entropy, source_entropy], color='red', lw=2)

plt.savefig(output_file)
