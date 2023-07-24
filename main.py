# Import libraries
import paho.mqtt.client as paho
from queue import Queue
from time import sleep
from datetime import datetime, timezone
import json

# MQTT PARAMETERS
MQTT_BROKER = "office.smartsentry.co.uk"
MQTT_PORT = 1883
deviceid = "80E1274DA35F"
MQTT_TOPIC = [("devices/"+deviceid+"/up/Accel",0),("devices/"+deviceid+"/up/AFE",0),("devices/"+deviceid+"/up/Shock",0),("devices/"+deviceid+"/up/BLE",0)]

# MQTT CLIENT
mqtt_client = paho.Client()

# CONNECTION VARIABLES
Connected = False
q = Queue()

# CONNECTION CALLBACK FUNCTIONS
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    q.put(message)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# ATTEMPT CONNECTION
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
mqtt_client.loop_start()

# MESSAGE HANDLING
try:
    print ("Press Ctrl+C to end")
    while 1:
        sleep(0.01)
        if Connected == True:
            mqtt_client.subscribe(MQTT_TOPIC)
            while not q.empty():
                message = q.get()
                if message is None:
                    continue
                ts = datetime.now(timezone.utc)
                if message.topic == "devices/"+deviceid+"/up/AFE":
                    m_decode_AFE = json.loads(message.payload.decode("utf-8"))
                    vol = m_decode_AFE['values']
                    print(str(m_decode_AFE))

    else:
        print("Waiting for connection")
except KeyboardInterrupt:
    print("End")
    pass
