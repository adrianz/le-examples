import paho.mqtt.client as mqtt
import json
import csv
import argparse
import time

#
# Command Line Interface
#
parser = argparse.ArgumentParser(description="Kontakt.io Location Engine MQTT2CSV")
parser.add_argument("-m", "--messages", dest="max_messages", default=5, type=int, help="Number of MQTT messages to collect. Optional.")
parser.add_argument("-a", "--apikey", dest="api_key", required=True, help="Kontakt.io API Key from Web Panel. Required.")
parser.add_argument("-t", "--topic", dest="topic", choices=["receiver", "place", "health", "accelerometer", "sensor"], required=True, help="Topic type: receiver (Presence data from a single Gateway), place (Presence data from a whole Place), health (beacon health from Telemetry), accelerometer (accelerometer data from Telemetry) or sensor (sensor data from Telemetry). Required.")
parser.add_argument("-i", "--id", dest="data_source_id", required=True, help="ID of the data's source - either Gateway's or Beacon's Unique ID, or Place's UUID. Required.")

args = parser.parse_args()

#
# Global Constants & Variables
#
max_messages = args.max_messages
api_key = args.api_key
topic = args.topic
data_source_id = args.data_source_id

counter = 0
first_message = True
topic_address = ""
fieldnames = []
filename = "le-" + topic + "-" + str(time.time()) + ".csv"

#
# Enviroment Setup
#
if topic == "receiver" or topic == "place":
    topic_address = "/presence/stream/" + data_source_id
    fieldnames = ["timestamp", "sourceId", "trackingId", "rssi", "proximity", "scanType", "deviceAddress"]
else:
    topic_address = "/stream/" + data_source_id + "/" + topic
    if topic == "health":
        fieldnames = ["utcTime", "batteryLevel"]
    elif topic == "accelerometer":
        fieldnames = ["sensitivity", "x", "y", "z", "lastDoubleTap", "lastThreshold"]
    elif topic == "sensor":
        fieldnames = ["lightLevel", "temperature"]

#
# MQTT Client Setup
#
mqttc = mqtt.Client("MQTT2CSV") # client_id has to be set, but the value doesn't matter
mqttc.username_pw_set("user", api_key) # username has to be set, but the value doesn't matter
mqttc.tls_set_context()

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + mqtt.connack_string(rc))

def on_message(client, userdata, message):
    global counter
    global first_message
    global fieldnames
    global filename
    json_payload = json.loads(message.payload)

    with open(filename, "a+t", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        if first_message:
            writer.writeheader()
        writer.writerows(json_payload)
        
    counter += 1
    first_message = False
    print("Received message number: " + str(counter))

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("ovs.kontakt.io", 8083, 60)    

mqttc.subscribe(topic_address)

#
# Run Loop
#
while counter < max_messages:
    mqttc.loop()