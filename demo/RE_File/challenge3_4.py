#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re 
from datetime import datetime

def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'
                   r'\[(.+)\]\s'
                   r'"GET\s(.+)\s\w+/.+"\s'
                   r'(\d+)\s'
                   r'(\d+)\s'
                   r'"(.+)"\s'  
                   r'"(.+)"'
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers
def main():
    logs = open_parser('/home/shiyanlou/Code/nginx.log')                
    allip_dict={}
    allurl_dict={}
    for item in logs:
        ip=item[0]
        time=item[1]
        url=item[2]
        status=item[3]
        if datetime.strptime(time.split(':')[0],'%d/%b/%Y')==datetime(2017,1,11):
            if allip_dict.get(ip) is not None:
                num=allip_dict[ip]
                allip_dict[ip]=num+1
            else:
                allip_dict[ip]=1
        if status=="404":
            if allurl_dict.get(url) is not None:
                num=allurl_dict[url]
                allurl_dict[url]=num+1
            else:
                allurl_dict[url]=1
    ip_dict={}
    url_dict={}
    maxip=''
    maxurl=''
    maxip_num=0
    maxurl_num=0
    for key,value in allip_dict.items():
        if value>maxip_num:
            maxip=key
            maxip_num=value
    for key,value in allurl_dict.items():
        if value>maxurl_num:
            maxurl=key
            maxurl_num=value
    ip_dict[maxip]=maxip_num
    url_dict[maxurl]=maxurl_num
    return ip_dict,url_dict

if __name__ == '__main__':
    #main()
    ip_dict, url_dict = main()
    print(ip_dict,url_dict)
    #print(ip_dict, url_dict)
