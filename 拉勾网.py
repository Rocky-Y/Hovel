#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Rocky-Y
# @Email   : 1347634801@qq.com

import requests
import re

response1 = requests.get('https://passport.lagou.com/login/login.html',
                 headers={
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',},
                 )

X_Anti_Forge_Token = re.findall("X_Anti_Forge_Token = '(.*?)'", response1.text, re.S)[0]
X_Anti_Forge_Code = re.findall("X_Anti_Forge_Code = '(.*?)'", response1.text, re.S)[0]
print(X_Anti_Forge_Token, X_Anti_Forge_Code)

response2 = requests.post(
    'https://passport.lagou.com/login/login.json',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Referer': 'https://passport.lagou.com/login/login.html',
        'X-Anit-Forge-Code': X_Anti_Forge_Code,
        'X-Anit-Forge-Token': X_Anti_Forge_Token,
        'X-Requested-With': 'XMLHttpRequest'
    },
    data={
        "isValidate": True,
        'username': '********************',
        'password': '********************',
        'request_form_verifyCode': '',
        'submit': ''
    },
    cookies=response1.cookies.get_dict()
)
print(response2.text)

