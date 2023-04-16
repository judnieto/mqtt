# -*- coding: utf-8 -*-
"""
@author: Judit Nieto Parla
"""

from paho.mqtt.client import Client
import sys

def on_message(mqttc, userdata, msg,):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain)
    mqttc.publish('clients/propio', msg.payload)
    
def main(broker, topics):
    mqttc = Client()
    
    mqttc.on_message = on_message

    print(f'Connecting on channels {topics} on {broker}')
    mqttc.connect(broker)
  
    mqttc.subscribe(topics)
    
    mqttc.loop_forever()
    
if __name__ == "__main__":
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic")
    broker = sys.argv[1]
    topics = sys.argv[2]
    main(broker, topics)    