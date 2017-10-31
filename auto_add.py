import requests

URL = 'http://fa17-cs411-08.cs.illinois.edu:8080/polls/add_i/'

payload = {
    'name': 'web spider',
    'snack': 'F',
    'vege': 'F',
    'calorie': '10',
    'protein': '1',
    'fat': '0.4',
    'sodium': '0'
}

session = requests.session()
r = requests.post(URL, data=payload)
print r.cookies
