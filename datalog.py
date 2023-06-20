import paho.mqtt.client as mqtt
from datetime import datetime
import time
import csv
import numpy as np

# MQTT broker settings
broker_address = "10.0.0.45"
broker_port = 1883
topic = "us/01973988"

# MQTT broker credentials
username = "sem-rabbitmq"
password = "sem-rabbitmq123"



# File settings
output_file = "EBM_PLUG_TEST.csv"

header = ["Timestamp", "Volt RMS", "Current RMS", "Real Power","PF","RAW Packet"]

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)


def err_percent(val_true,val_test):
    Comp = np.abs(val_true- val_test)/val_true
    return Comp * 100

def test_sequence_increment(test_seq):
    #Read the file line at the test sequence 
    #Compare the test sequence 
    #If the test sequence error is out of bounds increment the sequence
    pass
    


def compare_last_line(csv_file, new_data):
    last_row = ""
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            last_row = row
    return last_row == new_data

#parsing function
def parse(dec_pl):

    Time = dec_pl.split(",")[1]
    Time = (Time.split(":")[-1])
    timestamp = int(Time)
    Time = datetime.fromtimestamp(timestamp / 1000.0)

    V_rms = dec_pl.split(",")[3]
    V_rms = float(V_rms.split(":")[-1])

    I_rms = dec_pl.split(",")[4]
    I_rms = float(I_rms.split(":")[-1])

    Div_Zero = 0
    if (I_rms == 0):
        Div_Zero = 1
        I_rms = 0.0000000000000001

    Real_Power = dec_pl.split(",")[6]
    Real_Power = float(Real_Power.split(":")[-1])

    PF =  Real_Power / (V_rms * I_rms)
            
    data = [Time,V_rms,I_rms,Real_Power,PF,dec_pl]
     
    return data

# MQTT client callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    # Append received message to the file
    with open(output_file, "a", newline="") as file:
        dec = msg.payload.decode()
        print(dec)
        if dec[2] == 'S':
            if not compare_last_line(output_file, parse(dec)):
                writer = csv.writer(file)
                writer.writerow(parse(dec))
        else:
             pass   
            
        

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

# Create MQTT client instance
client = mqtt.Client()

# Set username and password for MQTT broker authentication
client.username_pw_set(username, password)

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to MQTT broker
client.connect(broker_address, broker_port)

# with open(output_file, "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(header)

# Start MQTT loop
client.loop_start()

try:
    # Run indefinitely
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Stop MQTT loop and disconnect
    client.loop_stop()
    client.disconnect()
