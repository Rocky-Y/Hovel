#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Rocky-Y
# @Email   : 1347634801@qq.com

import subprocess
import time
import os

PATH = os.path.dirname(os.path.abspath(__file__))+'/list.txt'
COMMAND_PREFIX_CHECK = 'youtube-dl -F '
COMMAND_PREFIX_DOWNLOAD = 'youtube-dl -f 137+140 '

def download_by_url(url):
    p = subprocess.Popen(COMMAND_PREFIX_DOWNLOAD + url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    start = time.time()
    print("***\tStart download:" + url + "\t" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))
    while True:
        line = p.stdout.readline()
        if not line == '':
            print(line.strip('\n'))
        else:
            break
    p.wait()
    end = time.time()
    print("********\tEnd\t"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end)),)
    print("taking："+str(int(end-start))+" seconds")
    mark_downloaded_url(url)

def get_url_from_list():
    print("\n********\tGet url")
    f = open(PATH, 'r+')
    for line in f.readlines():
        if not line == '\n':
            if line[0] == 'h':
                return line.strip('\n')
    return ''

def mark_downloaded_url(url):
    output = []
    f = open(PATH, 'r+')
    i = 0
    for line in f.readlines():
        line = line.strip('\n')
        url = url.strip('\n')
        if line == url:
            line = "*" + line
        output.append(line+"\n")
        i = i + 1
    f.close()
    f = open(PATH, 'w+')
    f.writelines(output)
    f.close()

if __name__ == '__main__':
    if not os.path.exists(PATH):
        print("can't find "+PATH)
        exit(0)
    while True:
        # 暂停下载，在同级目录下建一个stop.txt
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/stop.txt'):
            exit(0)
        url = get_url_from_list()
        print("\t\t\tRead:" + url)
        if url == '':
            print("FINISH DOWNLOAD")
            exit(0)
        download_by_url(url)
