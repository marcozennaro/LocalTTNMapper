#!/usr/bin/python
# ----------------------------------------------------------------
# File: add_gateways.py
#
# This script downloads the list of TTN gateways around a certain central point.

import os

filePath = '/var/www/html/coverage/js/gateways.js';
 
# As file at filePath is deleted now, so we should check if file exists or not not before deleting them
if os.path.exists(filePath):
    os.remove(filePath)

import urllib, json
url = "https://www.thethingsnetwork.org/gateway-data/location?latitude=45.673153&longitude=13.760440&distance=20000"
response = urllib.urlopen(url)
data = json.loads(response.read())
#print data
print("The following Gateways are added to the coverage map:")

for key in data:
    #print key, 'corresponds to', data[key]
    #print(data[key]['description'])
    gateway_name=data[key]['description'] 
    gtw_id=data[key]['id']
    print(data[key]['id'])    
    print(data[key]['description'])
     #print(data[key]['location']['latitude'])
    lat = data[key]['location']['latitude']  
    lon = data[key]['location']['longitude']
    alt = data[key]['location']['altitude'] 
    #print(data[key]['location']['longitude'])
    #print(data[key]['location']['altitude']) 
    file = open("/var/www/html/coverage/js/gateways.js","a")
    file.write('var marker = L.marker([')
    file.write("%f," % lat)
    file.write("%f," % lon)
    file.write("]).addTo(mymap).bindPopup(\"")
    file.write("<b>%s</b> " % gtw_id)
    file.write("<br>%s. " % gateway_name)
    file.write("<br>Antenna height: %i meters." % alt)
    file.write("\");\n") 
    file.write("\n")
    file.close()



