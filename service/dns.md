# Attack
----
## Basics
* 127.0.0.1の逆引きからドメインを特定（`dig @dns.com -x 127.0.0.1`）
* ターゲットのIPアドレスの逆引きからドメインを特定（`dig @dns.com -x $TARGET`）

## Zone Transfer
* ゾーン転送を利用し、サブドメインを列挙する
* Htb: FriendZone

  ```console
  ┌─[rio@parrot]─[~/Htb/FriendZone]
  └──╼ $dig @friendzone.htb axfr friendzone.red
  
  ; <<>> DiG 9.16.15-Debian <<>> @friendzone.htb axfr friendzone.red
  ; (1 server found)
  ;; global options: +cmd
  friendzone.red.         604800  IN      SOA     localhost. root.localhost. 2 604800 86400 2419200 604800
  friendzone.red.         604800  IN      AAAA    ::1
  friendzone.red.         604800  IN      NS      localhost.
  friendzone.red.         604800  IN      A       127.0.0.1
  administrator1.friendzone.red. 604800 IN A      127.0.0.1
  hr.friendzone.red.      604800  IN      A       127.0.0.1
  uploads.friendzone.red. 604800  IN      A       127.0.0.1
  friendzone.red.         604800  IN      SOA     localhost. root.localhost. 2 604800 86400 2419200 604800
  ;; Query time: 1432 msec
  ;; SERVER: 10.129.1.225#53(10.129.1.225)
  ;; WHEN: 木  7月 15 11:06:56 JST 2021
  ;; XFR size: 8 records (messages 1, bytes 289)
  ```

  
