# IMPORT LIBRARIES
import paho.mqtt.client as paho
from queue import Queue
import time
from datetime import datetime, timezone
import json
import tkinter as tk
import matplotlib.pyplot as plt

# IMPORT FILES
import volume_algorithm as va

# MQTT PARAMETERS
MQTT_BROKER = "office.smartsentry.co.uk"
MQTT_PORT = 1883
deviceid = "80E1274DA35F"
# deviceid = "80E1274DA9E8"
# MQTT_TOPIC = [("devices/"+deviceid+"/up/Accel",0),("devices/"+deviceid+"/up/AFE",0),("devices/"+deviceid+"/up/Shock",0),("devices/"+deviceid+"/up/BLE",0)]
MQTT_TOPIC = "devices/"+deviceid+"/up/AFE"
messages_received = 0

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

# APPLICATION 
class App():
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("600x400")
        self.label_time = tk.Label(text="")
        self.label_time.pack()
        self.label_connection_status = tk.Label(text="No Connection")
        self.label_connection_status.pack()
        global messages_received
        self.label_messages_received = tk.Label(text=str(messages_received))
        self.label_messages_received.pack()
        self.update_clock()
        self.root.mainloop()
        print("Press Ctrl+C to terminate")

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label_time.configure(text=now)
        self.root.after(1000,self.update_clock)
        # Application loop
        try:
            message_handling(self)
        except KeyboardInterrupt:
            print("Application terminated")
            plt.close()
            exit()

# MESSAGE HANDLING
def message_handling(App):
    if Connected == True:
        App.label_connection_status.configure(text="Connected")
        mqtt_client.subscribe(MQTT_TOPIC)
        while not q.empty():
            message = q.get()
            if message is None:
                continue
            ts = datetime.now(timezone.utc)
            if message.topic == "devices/"+deviceid+"/up/AFE":
                AFE_data = json.loads(message.payload.decode("utf-8"))
                vol_samples = []
                for value in AFE_data["values"]:
                    vol_samples.append(value)
            fill_level = va.find_peaks_and_troughs(vol_samples)
            global messages_received
            messages_received += 1
            App.label_messages_received.configure(text=str(messages_received))
    else:
        App.label_connection_status.configure(text="Disconnected")
        print("Waiting for connection")

# CREATE APPLICATION
app = App("Kegtracker Volume Data Analyser")