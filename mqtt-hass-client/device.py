import wiringpi as pi
#from utils import *
import json
from constants import *

def init():
    try:
        pi.wiringPiSetup()
        return 
    except:
        print('Failed to initialize wiringpi')
        return 0
        
def gpioGet(client,payload):
    try:
        param = json.loads(payload)
    except Exception as e:
        print(f"Error converting json: {e}")
        return
    
    pin = param['pin']
    try:
        # Read pin state
        state = pi.digitalRead(pin)
    except:
        print(f"failed to read state on pin {pin}")
        return
    
    # Return message
    msg = {}
    msg['pin'] = pin
    msg['state'] = state
    
    client.publish(mqttParam.TOPIC_BROADCAST, json.dumps(msg))
    
def gpioSet(client,payload):
    try:
        param = json.loads(payload)
    except Exception as e:
        print(f"Error converting json: {e}")
        return
    
    pin = param['pin']
    state = param['state']
    try:
        # Read pin state
        state = pi.digitalWrite(pin,state)
        client.publish(mqttParam.TOPIC_BROADCAST,payload)
    except:
        print(f"failed to write state on pin {param['pin']}")
        return
    