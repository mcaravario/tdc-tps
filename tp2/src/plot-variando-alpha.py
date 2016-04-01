import matplotlib.pyplot as plt
import json, sys
import numpy as np

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    all_results = json.loads(f.read())

n = '50'
alphas = ['0.2', '0.4', '0.6', '0.8']

results = all_results[n]

rtts = [results[alpha]['estimated_rtt'] for alpha in alphas]

xpos = np.arange(len(alphas))
width = 0.5

margen = 10
ymin, ymax = min(rtts) - margen, max(rtts) + margen

plt.bar(xpos, rtts, width)
plt.xticks(xpos + width / 2.0, alphas)
plt.ylim(ymin, ymax)
plt.xlabel('Alpha')
plt.ylabel('Round trip time(ms)')

plt.savefig(output_file)



