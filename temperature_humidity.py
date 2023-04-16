# -*- coding: utf-8 -*-
"""
@author: Judit Nieto Parla
"""
from paho.mqtt.client import Client
import sys

TEMP = 'temperature'
HUMIDITY = 'humidity'

def on_message(mqttc, data, msg):
    print (f'message:{msg.topic}:{msg.payload}:{data}')
    if data['status'] == 0:
        temp = int(msg.payload)
        if temp>data['temp_threshold']:
            print(f'umbral superado {temp}, suscribiendo a humidity')
            mqttc.subscribe(HUMIDITY)
            data['status'] = 1
    elif data['status'] == 1:
        if msg.topic==HUMIDITY:
            humidity = int(msg.payload)
            if humidity>data['humidity_threshold']:
                print(f'umbral humedad {humidity} superado, cancelando suscripciÃ³n')
                mqttc.unsubscribe(HUMIDITY)
                data['status'] = 0
        elif TEMP in msg.topic:
            temp = int(msg.payload)
            if temp<=data['temp_threshold']:
                print(f'temperatura {temp} por debajo de umbral, cancelando suscripciÃ³n')
                data['status']=0
                mqttc.unsubscribe(HUMIDITY)

def on_log(mqttc, data, level, msg):
    print(f"LOG: {data}:{msg}")
    
def main(broker):
    data = {'temp_threshold':20,
            'humidity_threshold':80,
            'status': 0}
    mqttc = Client(userdata=data)
    mqttc.on_message = on_message
    mqttc.enable_logger()

    mqttc.connect(broker)
    mqttc.subscribe(f'{TEMP}/t1')
    mqttc.loop_forever()
    
    
if __name__ == "__main__":
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)