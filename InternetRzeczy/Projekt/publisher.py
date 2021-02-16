import paho.mqtt.client as mqtt
import requests, json
import random
from time import sleep
from sense_emu import SenseHat
def on_connect(client, userdata, flags, rc):
    print('Connected to Broker')

client = mqtt.Client()
client.on_connect = on_connect
client.connect("0.0.0.0", 1883, 60)
sense = SenseHat()
sense.clear()

while True:
  	# Pomiar temperatury
	tem = round(sense.get_temperature())
	# Pomiar wilgotności
	hum = round(sense.get_humidity())
  	# Wyświetlenie wiadomości na aktuatorze
	sense.show_message('T:'+str(tem)+'C '+' H:'+str(hum)+'%')
	# Ublikacja na 2 tematy pogodowe
	client.publish("meteo/temperature", payload=tem, qos=0)
	client.publish("meteo/humidity", payload=hum, qos=0)
	print("Wysłano pomiary z sensorów.")
	sleep(1)