from fastapi import FastAPI
from sklearn.tree import DecisionTreeClassifier
import statistics
import csv 
import random
import json
import random

# Inicjalizacja zbioru uczącego
X = [[random.randint(-30, 10), random.randint(75, 100)] for i in range(10000)]
Y = []
for i in range(len(X)):
	if X[i][0]<5 and X[i][1]>80:
		Y.append(1)
	else:
		Y.append(0)
classifier = DecisionTreeClassifier()
classifier.fit(X, Y) # nauczenie klasyfikatora

app = FastAPI()


# ML - przewidzenie następnej temperatury na podstawie ostatnich 30
@app.get('/readings/')
async def get_mean_stdev():
	temps = []
	file =  open('readings.csv','r')     
	csvFile = csv.reader(file)
	for line in csvFile:
		temps.append(int(line[1].split(';')[1]))
	file.close()
	
	message = {}
	# średnia ostatnich 30 temperatur
	message['mean'] = str(round(statistics.mean([temp for temp in temps[-30:]]),2))
	# odchylenie standardowe 
	message['stdev'] = str(round(statistics.stdev([temp for temp in temps[-30:]]),2))
	data = json.dumps(message)
	return data

# ML - przewidzenie następnej temperatury na podstawie ostatnich 30
@app.post('/readings/')
async def get_prediction():
	pairs = []  
	file =  open('readings.csv','r')     
	csvFile = csv.reader(file)
	for line in csvFile:
		pairs.append([int(line[1].split(';')[1]), int(line[1].split(';')[2])])
	file.close()

	predict = True if classifier.predict([pairs[-1]])[0] == 1 else False

	message = {}
	message['is_snowy']=str(predict)
	print(message)
	data = json.dumps(message)
	return data