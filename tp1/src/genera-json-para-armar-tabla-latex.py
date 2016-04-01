### Este programa recibe un archivo json de una medición como parámetro
### y devuelve por standard output un archivo json adecuado para armar 
### una tabla en latex, con las columnas
### | Protocolo | Frecuencia | Información |

import json
import sys

execfile('plot-functions.py')

input_file = sys.argv[1]

with open(input_file) as f:
    data = json.loads(f.read())

symbol_information = data['symbol_information']
symbol_frequency = data['symbol_frequency']
symbols = [k for k, v in symbol_information.items()]

def percent(f):
    f = f * 100
    f = '%.2f'%f+'%'
    return f

res = []
for s in symbols:
    res.append({
        'Protocolo': protocol_title[s],
        'Frecuencia': percent(symbol_frequency[s]),
        'Informacion': '%.2f' % symbol_information[s]
    })

print json.dumps(res)


