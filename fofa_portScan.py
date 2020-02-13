# coding: utf-8
# code by kafroc - https://github.com/kafroc/utilCodes
# fofa port scan

import struct
import socket
import re
import base64
import requests

email = 'place your fofa email'
key = 'place your fofa key'

req = 'https://fofa.so/api/v1/search/all?email=' + \
    email + '&key=' + key + '&fields=port&qbase64='

iplist = '''example.com
8.8.8.8
tmp.test.com'''


def isIP(strin):
    try:
        struct.unpack('!I', socket.inet_aton(strin))[0]
    except Exception as exp:
        return False

    return True


fp = open('fofascan.txt', 'w')

for line in iplist.split('\n'):
    if isIP(line) == False:
        if line[-1] == '.':
            line = line[:-1]

        try:
            ip = socket.gethostbyname(line)
        except:
            ip = line
    else:
        ip = line

    if isIP(ip) == True:
        qbase64 = base64.b64encode(('ip=' + ip).encode()).decode()
    else:
        qbase64 = base64.b64encode(('domain="' + ip + '"').encode()).decode()
    res = requests.get(req + qbase64).json()

    print('%s --> %s\t%s' % (line, res['query'], set(res['results'])))
    fp.write('%s --> %s\t%s' % (line, res['query'], set(res['results'])))

fp.close()
