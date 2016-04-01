import matplotlib.pyplot as plt
import json, sys
import numpy as np

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    results = json.loads(f.read())


alpha = '0.8'
enes = ['10', '50', '100', '500', '1000']

rtts = [results[n][alpha]['estimated_rtt'] for n in enes]

print rtts

xpos = np.arange(len(enes))
width = 0.5

margen = 10
ymin, ymax = min(rtts) - margen, max(rtts) + margen

plt.bar(xpos, rtts, width)
plt.xticks(xpos + width / 2.0, enes)
plt.ylim(ymin, ymax)
plt.xlabel('Cantidad de paquetes')
plt.ylabel('Round trip time(ms)')

plt.savefig(output_file)



