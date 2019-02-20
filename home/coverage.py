#!/usr/bin/python
# ----------------------------------------------------------------
# File: coverage.py 
#
# This file executes an MQTT subscriber to TTN and then adds the poins to the coverage map. 

import json
import sys
import time
import base64

import paho.mqtt.client as mqtt

THE_BROKER = "eu.thethings.network"
THE_TOPIC = "+/devices/+/up"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(THE_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    themsg = json.loads(str(msg.payload))
    #print(themsg)

    #print(len(themsg['metadata']['gateways']))

    payload_raw = themsg["payload_raw"]
    payload_plain = base64.b64decode(payload_raw)
    device = themsg["dev_id"]
    #print(device) 
    lat = themsg["payload_fields"]["lat"]
    lon = themsg["payload_fields"]["lon"]

    freq = themsg["metadata"]["frequency"]
    rssi = themsg['metadata']['gateways'][0]['rssi']
    snr = themsg['metadata']['gateways'][0]['snr']
    dr = themsg['metadata']['data_rate']
    gtw = themsg['metadata']['gateways'][0]['gtw_id']

    if rssi < -110:
       #print("Red")
      clr = 'red'
    elif -90 > rssi > -110:
       #print("Yellow")
      clr = 'yellow'
    else:
       #print("Green")    
      clr = 'green'

    print(clr) 
    file = open("/var/www/html/coverage/js/nodes.js","a")
    file.write('var circle = L.circle([')
    file.write("%f," % lat)
    file.write("%f" % lon)
    file.write('], {\n') 
    file.write('color: \'%s\',' % clr)
    file.write('fillColor: \'%s\',' % clr)
    file.write('fillOpacity: 0.5,\n')
    file.write('radius: 40 \n')
    file.write('}).addTo(mymap).bindPopup("Device: <b> %s </b>' % device)
    file.write('<br>Freq: %s' % themsg["metadata"]["frequency"])
    file.write('<br>DR: %s' % themsg['metadata']['data_rate'])
    file.write('<br><b>Gateway 1</b>: %s' % themsg['metadata']['gateways'][0]['gtw_id'])
    file.write('<br>RSSI: %s' % themsg['metadata']['gateways'][0]['rssi'])
    file.write('<br>SNR: %s' % themsg['metadata']['gateways'][0]['snr'])
    if len(themsg['metadata']['gateways']) == 1: 
      file.write('");')
    elif len(themsg['metadata']['gateways']) == 2:
      file.write('<br><b>Gateway 2</b>: %s' % themsg['metadata']['gateways'][1]['gtw_id'])
      file.write('<br>RSSI: %s' % themsg['metadata']['gateways'][1]['rssi'])
      file.write('<br>SNR: %s' % themsg['metadata']['gateways'][1]['snr'])
      file.write('");')
    elif len(themsg['metadata']['gateways']) == 3:
      file.write('<br><b>Gateway 2</b>: %s' % themsg['metadata']['gateways'][1]['gtw_id'])
      file.write('<br>RSSI: %s' % themsg['metadata']['gateways'][1]['rssi'])
      file.write('<br>SNR: %s' % themsg['metadata']['gateways'][1]['snr'])
      file.write('<br><b>Gateway 3</b>: %s' % themsg['metadata']['gateways'][2]['gtw_id'])
      file.write('<br>RSSI: %s' % themsg['metadata']['gateways'][2]['rssi'])
      file.write('<br>SNR: %s' % themsg['metadata']['gateways'][2]['snr'])
      file.write('");')
    file.write("\n")       
    file.close()

 
client = mqtt.Client()
client.username_pw_set("coverage_mapping_XXX", password="ttn-account-v2.KQrXXBVBVX2pia39eFBUNpLMzXNNH1gZxFXsr2eNxY")

client.on_connect = on_connect
client.on_message = on_message

client.connect(THE_BROKER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


