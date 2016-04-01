import json, os, sys
import functions

input_file = sys.argv[1]
output_file = sys.argv[2]

functions.plot_routes(input_file, output_file)

cmd = 'xdg-open %s' % output_file
if sys.platform == 'darwin':
    cmd = 'open %s' % output_file
os.system(cmd)
