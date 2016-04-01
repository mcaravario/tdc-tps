#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, os, glob, sys

if len(sys.argv)<=1:
  print "Debe especificar el testname."
  inputs = glob.glob("../output/*.pcap")
  print "***"
  if len(inputs)>0:
    print "Encontré los siguientes testname:"
    for i in inputs:
      head,tail = os.path.split(i)
      name,ext = os.path.splitext(tail)
      print "\t%s"%name
  else:
    print "ERROR: No encontré ningún archivo pcap en la carpeta output!"
  print "***"

# parse the argument
parser = argparse.ArgumentParser(description='Corre los otros scripts')
parser.add_argument('-i', '--input-testname', required=True,
  help='nombre del testname (archivo pcap en la carpeta output)')
parser.add_argument('--full', action='store_true', default=False)
parser.add_argument('--dont-open', action='store_true', default=False)
args = parser.parse_args()

# run the subprocess
from subprocess import Popen, PIPE

if(args.full):
  # Calculo la entropía de S
  process = Popen(["sudo", "./calcular_entropia_s.py", "-i", args.input_testname], stdout=PIPE)
  (output, err) = process.communicate()
  if process.wait() != 0:
    raise Exception("Error al ejecutar calcular_entropia_s.py")
  # Calculo la entropía de S_1
  process = Popen(["sudo", "./calcular_entropia_s1.py", "-i", args.input_testname], stdout=PIPE)
  (output, err) = process.communicate()
  if process.wait() != 0:
    raise Exception("Error al ejecutar calcular_entropia_s1.py")

# Plot histogram
process = Popen(["./plot-histogram-s.py", "-i", args.input_testname], stdout=PIPE)
(output, err) = process.communicate()
if process.wait() != 0:
  raise Exception("Error al ejecutar plot-histogram-s.py")
process = Popen(["./plot-histogram-s1.py", "-i", args.input_testname], stdout=PIPE)
(output, err) = process.communicate()
if process.wait() != 0:
  raise Exception("Error al ejecutar plot-histogram-s1.py")

# Plot pie
process = Popen(["./plot-pie-s.py", "-i", args.input_testname], stdout=PIPE)
(output, err) = process.communicate()
if process.wait() != 0:
  raise Exception("Error al ejecutar plot-pie-s.py")
process = Popen(["./plot-pie-s1.py", "-i", args.input_testname], stdout=PIPE)
(output, err) = process.communicate()
if process.wait() != 0:
  raise Exception("Error al ejecutar plot-pie-s1.py")

if not args.dont_open:
  os.system("xdg-open ../output/%s-s-histogram.png"%args.input_testname)
  os.system("xdg-open ../output/%s-s-pie.png"%args.input_testname)
  os.system("xdg-open ../output/%s-s1-histogram.png"%args.input_testname)
  os.system("xdg-open ../output/%s-s1-pie.png"%args.input_testname)
