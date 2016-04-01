#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                                                                      │

import json,os,numpy as np


def calculate_zrtt(filename):
    """ 
    Calcula el zrtt de cada hop y lo imprime por pantalla
    """
    
    with open(filename) as f:
        data = json.loads(f.read())

    avg_rtt_accum = []
    # Calculo el rtt de cada hop haciendo el promedio entre todos los paquetes
    # enviados
    for hop in data:
        rtts_hop = [int(medicion['rtt'][:-3]) for medicion in hop if medicion['rtt'] != '*']
        avg_rtt_accum.append ( np.average( rtts_hop ) if len(rtts_hop) > 0 else None  )
   
    #calculo de rtt haciendo la diferencia entre saltos
    avg_rtt = []
    last_rtt = 0
    for i in range(len(avg_rtt_accum)):
        rtt_accum = avg_rtt_accum[i]
        if rtt_accum == None:
            avg_rtt.append(rtt_accum)
        else:
            avg_rtt.append(rtt_accum - last_rtt)
            last_rtt = rtt_accum

    #calculo el rtt promedio total y el desvio estandar
    filtered = [x for x in avg_rtt if x is not None]
    avg_rtt_total = np.average(filtered)
    rtt_std = np.std(filtered)

    zrtt_list = []
    for rtt in avg_rtt:
        if rtt is None:
            zrtt_list.append(None)
        else:
            zrtt_list.append( (rtt - avg_rtt_total) / rtt_std )
       
    return zrtt_list

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    res = calculate_zrtt(filename)
    print res
