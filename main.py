# IMPORT LIBRARIES
import paho.mqtt.client as paho
from queue import Queue
import time
from datetime import datetime, timezone
import json
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd

# IMPORT FILES
import volume_algorithm as va

# MQTT PARAMETERS
MQTT_BROKER = "office.smartsentry.co.uk"
MQTT_PORT = 1883
deviceid = "80E1274DA35F"
#deviceid = "80E1274DA9E8"
#deviceid = "80E1274DA988"
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

# Variables
samples = []
average_sample = []
samples_fl = []
average_samples_fl = []
filllevel_defined = False
filllevel_actual = -1
messages_received_fl = 0

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
        self.filllevel_entry = tk.Entry(justify="center")
        self.filllevel_entry.pack()
        self.filllevel_define_btn = tk.Button(text="Fill Level Change", command=lambda : set_fill_level(self))
        self.filllevel_define_btn.pack()
        self.filllevel_label = tk.Label(text="Fill level not set")
        self.filllevel_label.config(bg="red")
        self.filllevel_label.pack()
        self.label_lastmessagetime = tk.Label(text="N/A")
        self.label_lastmessagetime.pack()
        self.update_clock()
        self.root.mainloop()
        print("Press Ctrl+C to terminate")
        
    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label_time.configure(text=now)
        self.root.after(1000,self.update_clock)
        # Application loops
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
                #samples.append(va.find_peaks_and_troughs(vol_samples))
                samples.append(vol_samples)
                average_sample = va.average_samples(samples, 1)
                samples_fl.append(va.average_samples(samples, 1))
                plt.clf()
                #plt.figure()
                plt.plot(average_sample[7], label=(average_sample[3]))
                ax = plt.gca()
                ax.set_ylim([0, 4000])
                plt.axvline(average_sample[4], color='k')
                plt.legend()
                plt.show()
                export_to_csv()
            global messages_received
            global messages_received_fl
            messages_received += 1
            messages_received_fl += 1
            App.label_messages_received.configure(text=str(messages_received)+" : "+str(messages_received_fl))
            mts = time.strftime("%H:%M:%S")
            App.label_lastmessagetime.configure(text=mts)
    else:
        App.label_connection_status.configure(text="Disconnected")
        print("Waiting for connection")

def set_fill_level(App):
    if int(App.filllevel_entry.get()) > -1:
        global filllevel_defined
        filllevel_defined = True
        global filllevel_actual
        filllevel_actual = int(App.filllevel_entry.get())
        App.filllevel_label.config(text="Fill Level = " + str(filllevel_actual), bg="green")
        App.filllevel_entry.delete(0,"end")
        samples_fl.clear()
        global messages_received_fl
        messages_received_fl = 0
    else:
        print("Fill level entry not valid")

def export_to_csv():
    global filllevel_defined
    global filllevel_actual
    if filllevel_defined == True:
        pd.DataFrame(samples_fl).to_csv(str(filllevel_actual)+".csv")
        print(str(filllevel_actual)+".csv exported")
    else:
        pd.DataFrame(samples_fl).to_csv("output.csv")
        print("output.csv exported")

# CREATE APPLICATION
app = App("Kegtracker Volume Data Analyser")