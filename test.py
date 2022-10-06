import requests
import json

url = 'http://localhost:8000/main'

with open('test2.wav', 'rb') as wav:

    files = {"file": wav}
    d = {"body": "Foo Bar"}

    req = requests.post(url, files=files, json=d)

    print(req.status_code)
    print(req.text)
