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
* また別ユーザとしてコマンドを実行する必要がなく、別ユーザ権限でのファイル閲覧のみ行いたいのなら、net useを利用する方法がある
* Htb: Bart

  ```console
  PS C:\Users\Public> net use x: \\localhost\c$ /user:Administrator 3130438f31186fbaf962f407711faddb
  The command completed successfully.
  PS C:\Users\Public> 
  ```

  
