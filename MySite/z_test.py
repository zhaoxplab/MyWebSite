import requests

response = requests.get(url='http://192.168.0.104:8000/diary/api/v1')
print(response.json())
