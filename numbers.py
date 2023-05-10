# -*- coding: utf-8 -*-
"""
@author: Judit Nieto Parla
"""

from paho.mqtt.client import Client
import sys


NUMBERS = 'numbers'
CLIENTS = 'clients'
TIMER_STOP = f'{CLIENTS}/timerstop'
HUMIDITY = 'humidity'

def is_prime(n):
    i = 2
    while i*i < n and n % i != 0:
        i += 1
    return i*i > n

def is_real(n):
    n_real=float(n)
    n_int=round(n)
    if n_real==n_int:
        return False
    else:
        return True

def on_message(mqttc, data, msg):
    print(f"MESSAGE:data:{data}, msg.topic:{msg.topic}, payload:{msg.payload}")
    if is_real(msg.payload):
        data["suma_reales"]+=float(msg.payload)
        print("El número", float(msg.paload), "es real")
    else:
        data["suma_enteros"]+=round(msg.payload)
        if is_prime(round(msg.payload)):
            data["primos"]+=1
            print("El numero", round(msg.payload), "es entero y primo")
        else:
            print("El numero", round(msg.payload), "es entero y no es primo")
    
def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)
    
def main(broker):
    data = {"client":None, "broker":broker, "suma_reales":0, "suma_enteros":0, "primos":0}
    mqttc = Client(client_id="numbers", userdata=data)
    data['client'] = mqttc
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(NUMBERS)
    mqttc.loop_forever()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)