import requests
import csv
import json
from itertools import islice
URL = "https://attandancemanagerapi.herokuapp.com/api/students/"
with open('MOCK_DATA.csv') as f:
    reader = csv.reader(f)
    for row in islice(reader, 1, None):
        print(row)
        headers = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4MjA2MzEyLCJqdGkiOiJkYTA3ZjdiZWQ4Njk0NTg3ODI3NWRiODdmZWRhODBiNyIsInVzZXJfaWQiOjJ9.lYqxlq9D8tPUxatmiDWwAJNSyjDbQy5no9ZfRy2PK18',
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


