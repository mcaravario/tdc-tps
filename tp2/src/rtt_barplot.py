import json, sys
import matplotlib.pyplot as plt
import numpy as np
from zrtt import calculate_zrtt

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    hops = json.loads(f.read())

rtt_acumulado = []

for hop in hops:
    rtts_hop = [int(medicion['rtt'][:-3]) for medicion in hop if medicion['rtt'] != '*']
    rtt_acumulado.append ( np.average( rtts_hop ) if len(rtts_hop) >0 else 0  )

zrtt = calculate_zrtt(input_file)

hop_number = range(1, len(rtt_acumulado) + 1)
ind = np.arange(len(hop_number))
width = 1.0

fig, ax1 = plt.subplots()
ax1.bar(ind, rtt_acumulado, width)

ax1.set_xticks(ind + width / 2.0)
ax1.set_xticklabels(hop_number)

ax1.set_xlabel('Hop number')
ax1.set_ylabel('Round trip time(ms)', color='b')

ax2 = ax1.twinx()
ax2.plot(ind, zrtt, 'rx', markersize=10, markeredgewidth=3)
ax2.set_ylabel('zrtt', color='r')

plt.savefig(output_file)
