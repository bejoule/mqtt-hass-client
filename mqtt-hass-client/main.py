import paho.mqtt.client as mqtt
import random
from constants import *
import time
from device import *

# The callback function when connecting to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to the broker!")
        client.subscribe(mqttParam.TOPIC_SET)  # Subscribe to a topic
        client.subscribe(mqttParam.TOPIC_GET)
        #client.subscribe(mqttParam.TOPIC_BROADCAST)
    else:
        print(f"Failed to connect, return code {rc}")

# The callback function when receiving a message
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(topic,payload)
    match topic:
        case mqttParam.TOPIC_GET:
            gpioGet(client,payload)
        case mqttParam.TOPIC_SET:
            gpioSet(client,payload)

# The callback function for when a message is published
def on_publish(client, userdata, mid, properties=None):
    print("Message published!")
    
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed with mid: {mid} and QoS: {granted_qos}")
    
def on_disconnect(client, userdata, rc, properties=None):
    print('Disconnected')
    if rc != 0:
        while True:
            try:
                print('Attempting to reconnect ...')
                cilent.reconnect()
                break
            except Exception as e:
                print(f"Reconnection failed: {e}")
                time.sleep(5)

def main():
    if init() == 0:
        print("Failed to initialize wiringpi...")
        return
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    
    print(mqttParam.BROKER,mqttParam.PORT)
    # Connect to the broker
    client.connect(mqttParam.BROKER, mqttParam.PORT, 60)
    
    # Start the loop to process incoming and outgoing messages
    client.loop_forever()
    

if __name__ == '__main__':
    main()