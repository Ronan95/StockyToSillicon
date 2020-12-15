import requests

BASE = "http://localhost:5000/"

response = requests.put(BASE + "stock/1")

print(response.json())

#acá ya no supe que hacer 