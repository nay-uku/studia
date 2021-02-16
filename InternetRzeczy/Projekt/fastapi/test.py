import requests
url = 'http://0.0.0.0:8000/readings'

response = requests.post(url)
print(response.text) 
