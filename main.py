import requests
import csv
import json
from itertools import islice
URL = "http://127.0.0.1:8000/api/students/"
with open('MOCK_DATA.csv') as f:
    reader = csv.reader(f)
    for row in islice(reader, 1, None):
        print(row)
        headers = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA5NTU2MzIxLCJqdGkiOiJiMjhlY2JiN2M5MmE0NjRiYjMxN2MxYWRmNzc1OGQzNyIsInVzZXJfaWQiOjJ9.qL4v53GXmM-LuTYNwOAGZNV_g469EkCEn8tXXT882Mk',
            'Content-Type': 'application/json'
        }
        data = {
            'rollNo': row[0],
            'name': row[1],
            'cId': row[2]
        }
        json_data = json.dumps(data)
        r = requests.post(url=URL, data=json_data, headers=headers)
        data = r.json()
        print(data)


