from xml.etree import ElementTree as ET
import json
import sys
from render import render_print_image

orig_stdout = sys.stdout
f = open('output-testrender.txt', 'w')
sys.stdout = f

with open("batch_response_data.json") as json_file:
    json_data = json.load(json_file)


ns = {'ns': 'http://www.transunion.com/namespace/pfs/v4'}
for data in json_data:
    print(render_print_image(data))

sys.stdout = orig_stdout
f.close()