# Windows
----

## 32 Bit or 64 Bit Process
* OSが32bitか、64bitか、シェルを実行しているプロセスが32bitか、64bitかチェック
* Kernel Exploitによっては、WOW64リダイレクトのために、32bitプロセスでは動作しない可能性がある
* Htb: Bart
  ```console
  PS C:\Users\Public> [environment]::Is64BitOperatingSystem
  True
  PS C:\Users\Public> [environment]::Is64BitProcess
  False
  ```

## Runas
* Windowsではrunasコマンドで別ユーザとしてコマンドを実行可能
* ただし、runasはインタラクティブにパスワードを入力を要求されるため、reverse shellなどの環境では実行できない
* そこで、reverse shellでは[PowerShell-Suite/Invork-Runas.ps1](https://github.com/FuzzySecurity/PowerShell-Suite)もしくはInvoke-Commandを利用する
  * PSCredentialを生成する際に、ドメイン名（BART）が必要であることに注意
  * Htb: Bart
  
    ```console
    PS C:\Users\Public> $pass = ConvertTo-SecureString "3130438f31186fbaf962f407711faddb" -AsPlainText -Force
    PS C:\Users\Public> $cred = New-Object System.Management.Automation.PSCredential('BART\Administrator', $pass)
    PS C:\Users\Public> Invoke-Command -ScriptBlock {whoami} -Credential $cred -Computer localhost
    bart\administrator
    PS C:\Users\Public>
    ```

* Administratorとしてrunasを実行可能なのは、 Administratorアカウントが有効化されている場合のみ
* 現在のWindowsではAdministratorは、セキュリティのため初期状態で無効化されているため、そのような場合は限られる
* Pentestにおいてrunasの実行が必要となるのは、SMBなどの遠隔ログイン可能なポートが外部に開放されていない状況である
* ただし、そのような状況でもSMBはローカルホストには開放されている可能性がある
* SMBがローカルホストに開放されているならば、ポートフォワーディングを行うことで、そもそもrunasを利用せずとも別ユーザとして遠隔ログイン可能である
* また別ユーザ権限でのファイル閲覧のみ行いたいのなら、net useを利用し、SMBでcドライブをマウントする方法がある
* Htb: Bart

  ```console
  PS C:\Users\Public> net use x: \\localhost\c$ /user:Administrator 3130438f31186fbaf962f407711faddb
  The command completed successfully.
  PS C:\Users\Public> 
  ```

## Crash Dump 
* Volatilityを利用
* imageinfoでimageのprofileを特定する
* 特定したprofileでhashdumpなどを実行
* Htb: Silo

  ```console
  ┌─[rio@parrot]─[~/Htb/Silo]
  └──╼ $vol.py -f SILO-20180105-221806.dmp imageinfo
  Volatility Foundation Volatility Framework 2.6.1
  INFO    : volatility.debug    : Determining profile based on KDBG search...
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
  WARNING : volatility.debug    : Alignment of WindowsCrashDumpSpace64 is too small, plugins will be extremely slow
            Suggested Profile(s) : Win2016x64_14393, Win8SP0x64, Win10x64_17134, Win81U1x64, Win10x64_10240_17770, Win10x64_18362, Win10x64_14393, Win10x64, Win2012R2x64_18340, Win10x64_16299, Win2012R2x64, Win10x64_19041, Win2012x64, Win10x64_17763, Win8SP1x64_18340, Win10x64_10586, Win8SP1x64, Win10x64_15063 (Instantiated with Win10x64_15063)
                       AS Layer1 : SkipDuplicatesAMD64PagedMemory (Kernel AS)
                       AS Layer2 : WindowsCrashDumpSpace64 (Unnamed AS)
                       AS Layer3 : FileAddressSpace (/home/rio/Htb/Silo/SILO-20180105-221806.dmp)
                        PAE type : No PAE
                             DTB : 0x1a7000L
                            KDBG : 0xf80078520a30L
            Number of Processors : 2
       Image Type (Service Pack) : 0
                  KPCR for CPU 0 : 0xfffff8007857b000L
                  KPCR for CPU 1 : 0xffffd000207e8000L
               KUSER_SHARED_DATA : 0xfffff78000000000L
             Image date and time : 2018-01-05 22:18:07 UTC+0000
       Image local date and time : 2018-01-05 22:18:07 +0000
  
  ┌─[✗]─[rio@parrot]─[~/Htb/Silo]
  └──╼ $vol.py -f SILO-20180105-221806.dmp --profile Win2012R2x64 hashdump
  Volatility Foundation Volatility Framework 2.6.1
  Administrator:500:aad3b435b51404eeaad3b435b51404ee:9e730375b7cbcebf74ae46481e07b0c7:::
  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
  Phineas:1002:aad3b435b51404eeaad3b435b51404ee:8eacdd67b77749e65d3b3d5c110b0969:::
  ```

  