import csv, datetime, json, math, subprocess, sys
from scapy.all import sr, sr1, ICMP, TCP, IP, RandShort

MSS = 1460

host = sys.argv[1]  # host al que hace el ping
output_file = sys.argv[2]

enes = [10, 50, 100, 500, 1000]
alphas = [0.2, 0.4, 0.6, 0.8]

sample_rtts = {str(n): [] for n in enes}

for i in range(enes[-1]):
    packet = IP(dst=host) / ICMP(type="echo-request")
    start = datetime.datetime.now()
    ans, unans = sr(packet, timeout=0.5, retry=0, verbose=False)
    end = datetime.datetime.now()
    sample_rtt = (end - start).microseconds / 1000
    if len(ans) == 1 and len(unans) == 0:
        for n in enes:
            if i < n:
                sample_rtts[str(n)].append(sample_rtt)

results = {str(n): {str(alpha): {'estimated_rtt': sample_rtts[str(n)][0]
                                 if len(sample_rtts[str(n)]) > 0 else None,
                                 'p': 1.0 - (float(len(sample_rtts[str(n)])) / float(n)),
                                 'mathis_throughput': None}
                    for alpha in alphas}
           for n in enes}

for n in enes:
    for alpha in alphas:
        my_results = results[str(n)][str(alpha)]
        estimated_rtt = my_results['estimated_rtt']
        for i in range(1, len(sample_rtts[str(n)])):
            estimated_rtt = alpha * estimated_rtt + (1 - alpha) * sample_rtts[str(n)][i]
        my_results['estimated_rtt'] = estimated_rtt
        p = my_results['p']
        if p is not None and p != 0.0:
            my_results['mathis_throughput'] = MSS / (estimated_rtt * math.sqrt(p))

with open(output_file, 'w') as f:
    f.write(json.dumps(results, indent=4))
