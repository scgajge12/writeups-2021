#!/usr/bin/python3
import requests
import base64
import json

def get_answer(cookie):
    ans = cookie.split('.')[0]
    missing_padding = len(ans) % 4
    if missing_padding:
        ans = ans + '=' * (4 - missing_padding)
    return json.loads(base64.b64decode(ans).decode('ascii'))

r = requests.get('http://34.121.84.161:8084/')
answer = get_answer(r.cookies['session'])

for i in range(500):
    params = {"guess": ' '.join([str(i) for i in answer['answer']])}
    jar = r.cookies
    r = requests.post('http://34.121.84.161:8084/', data=params, cookies=jar)
    answer = get_answer(r.cookies['session'])

print(r.text)