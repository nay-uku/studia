import paho.mqtt.client as mqtt
import requests, json
import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import numpy as np


# Dane AWS
host = 'YOUR_AWS_ADDRESS.iot.eu-central-1.amazonaws.com'
rootCAPath = 'root-CA.crt'
certificatePath = 'meteoPI.cert.pem'
privateKeyPath = 'meteoPI.private.key'
port = 8883
clientId = 'basicPubSub'
topic = 'readings'

# Dane fastAPI
url = 'http://0.0.0.0:8000/readings/'

readings = [] # odczyty
counter = 0


def on_connect(client, userdata, flags, rc):
    print('Połączono z brokerem MQTT')
    client.subscribe("meteo/temperature", 0)
    client.subscribe("meteo/humidity", 0)


def on_message_tem(client, userdata, message):
	readings.append(int(str(message.payload, 'utf-8')))


def on_message_hum(client, userdata, message):
	readings.append(int(str(message.payload, 'utf-8')))
	print(readings)
	now = datetime.datetime.now()
	record = now.strftime("%m/%d/%Y, %H:%M:%S")+";"\
	+str(readings[0])+";"+str(readings[1])+"\n"
	
	# zapis do csv
	with open('readings.csv', 'a') as csv_f:
		csv_f.write(record)
	
	# wysłanie na topic do AWS
	message = {}
	message['timestamp'] = now.strftime("%m/%d/%Y, %H:%M:%S")
	message['temperature'] = readings[0]
	message['humidity'] = readings[1]
    
	messageJson = json.dumps(message)
	myAWSIoTMQTTClient.publish(topic, messageJson, 0)
	print('Published topic %s: %s\n' % (topic, messageJson))

	# Zapis wykresu co 30 pomiarów
	global counter
	if counter % 5 == 0:
		tems = [] # lista temperatur
		hums = [] # lista wilgotności
		dates = [] # lista dat
		file =  open('readings.csv','r')     
		csvFile = csv.reader(file)
		for line in csvFile:
			tems.append(int(line[1].split(';')[1]))
			hums.append(int(line[1].split(';')[2]))
			date = line[0]+","+line[1].split(';')[0]
			dates.append(datetime.datetime.strptime(date,"%m/%d/%Y, %H:%M:%S"))
		file.close()
		plt.figure()
		# Na wykresie ostatnie 30 pomiarów
		plt.plot_date(dates[-30:], tems[-30:], linestyle='-', label="temperatura C",color="orange")
		plt.plot_date(dates[-30:], hums[-30:], linestyle='-', label="wilgotność %", color="blue")
		# Upiększanie wykresów
		plt.title("Temperatura i wilgotność w czasie")
		plt.xticks(x='datetime', rotation='vertical')
		plt.yticks(np.arange(-30, 101, 10))
		plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=20))
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
		plt.legend()
		plt.tight_layout()
		plt.savefig("./wykresy/"+str(now)+".jpg") # zapis wykresu
		del tems[:]
		del hums[:]  
		del dates[:]

	counter += 1
	del readings[:]

	# fastAPI GET - zwrócenie średniej i odchylenia
	response = requests.get(url)
	data = json.loads(response.text)
	print("Średnia temperatura oraz odchylenie z ostatnich 30 pomiarów są następujące:")
	print(data)

	record = now.strftime("%m/%d/%Y, %H:%M:%S")+";"\
	+str(data)+"\n"
	with open('means.csv', 'a') as csv_f:
		csv_f.write(record)
		
	# fastAPI POST - zwrócenie wyniku ML - czy pada śnieg (>0.5 - pada)
	response = requests.post(url)
	data = json.loads(response.text)
	print("Czy pada śnieg:")
	print(data)

		
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add('meteo/temperature', on_message_tem)
client.message_callback_add('meteo/humidity', on_message_hum)
client.connect("0.0.0.0", 1883, 60)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()

client.loop_forever()