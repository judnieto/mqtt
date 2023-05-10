# -*- coding: utf-8 -*-
"""
@author: Judit Nieto Parla
"""

from paho.mqtt.client import Client
import sys

def on_message(mqttc, userdata, msg,):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain)
    mqttc.publish('clients', msg.payload)
    
def main(broker, topic_s, topic_p):
    mqttc = Client()
    
    mqttc.on_message = on_message

    print(f'Connecting on channels {topic_s} on {broker}')
    mqttc.connect(broker)
    
    mqttc.publish(topic_p)
  
    mqttc.subscribe(topic_s)
    
    mqttc.loop_forever()
    
if __name__ == "__main__":
    if len(sys.argv)<4:
        print(f"Usage: {sys.argv[0]} broker topic_s topic_p")
    broker = sys.argv[1]
    topic_s = sys.argv[2]  # topic subscribe
    topic_p = sys.argv[3]  # topic publish
    main(broker, topic_s, topic_p)    