# -*- coding: utf-8 -*-
"""
@author: Judit Nieto Parla
"""

from threading import Lock
from paho.mqtt.client import Client
from time import sleep
import random

def on_message(mqttc, data, msg):
    print ('on_message', msg.topic, msg.payload)
    n = len('temperature/')
    lock = data['lock']
    lock.acquire()
    try:
        key = msg.topic[n:]
        if key in data['temp']:
            data['temp'][key].append(msg.payload)
        else:
            data['temp'][key]=[msg.payload]
    finally:
        lock.release()
    print ('on_message', data)


def main(broker):
    data  = {'lock':Lock(), 'temp':{}}
    mqttc = Client(userdata=data)
    mqttc.on_message = on_message
    mqttc.connect(broker)
    mqttc.subscribe('temperature/#')
    mqttc.loop_start()
    
    while True:
        time_random=random.randint(4,8)
        sleep(time_random)
        temp_max=[]
        temp_min=[]
        for key,temp in data['temp'].items():
            maximum=max(temp)
            minimum=min(temp)
            temp_max.append(maximum)
            temp_min.append(minimum)
            mean = sum(map(lambda x: int(x), temp))/len(temp) #media
            print(f'mean {key}: {mean}')
            print("Temperatura maxima:", temp_max, "Temperatura minima:", temp_min)
            data[key]=[]
        maximum_all=max(temp_max)
        minimum_all=min(temp_min)
        print("Temperatura total maxima:", maximum_all, "Temperatura total minima:", minimum_all)

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)