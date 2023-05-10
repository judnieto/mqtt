# -*- coding: utf-8 -*-
"""
@author: Judit Nieto Parla
"""

from paho.mqtt.client import Client
import time
import sys
from multiprocessing import Process
from time import sleep
import paho.mqtt.publish as publish

def work_on_message(message, broker):
    print("process body", message)
    topic, timeout, text = message[2:-1].split(",")
    print("process body", timeout, topic, text)
    sleep(int(timeout))
    publish.single(topic, payload=text, hostname=broker)
    print("end process body",message)
    
def on_message(mqttc, userdata, msg):
    print("on_message", msg.topic, msg.payload)
    worker = Process(target=work_on_message, args=(str(msg.payload), userdata["broker"]))
    worker.start()
    print("end on_message", msg.payload)
    
def main (broker):
    data={'status':0}
    mqttc=Client(userdata=data)
    mqttc.enable_logger()
    mqttc.on_message=on_message
    mqttc.connect(broker)
    res_topics=['clients/a','clients/b']
    for t in res_topics:
        mqttc.subscribe(t)
    mqttc.loop_start()
    tests=[ (res_topics[0],4,'uno'),
            (res_topics[1],1,'dos'),
            (res_topics[0],2,'tres'),
            (res_topics[1],5,'cuatro')]
    topic = 'clients/timeout'
    for test in tests:
        mqttc.publish(topic, f'{test[0]},{test[1]},{test[2]}')
    time.sleep(10)
    
if __name__ == "__main__":
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker=sys.argv[1]
    main(broker)