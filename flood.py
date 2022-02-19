# DDOS TCP FLOODER
# v0.0.2

import re
import requests
import threading


URL = input('[+] URL: ')
def start():
    res = dict()
    for i in range(2000):
        response = requests.get(URL)
        host = response.text.splitlines()[-1].split()[-1]
        if(host in res.keys()):
            res[host] = res[host]+1
        else:
            res[host] = 1
    print(res)
    

# for x in range(thread):
#     thred = threading.Thread(target=start)
#     thred.start()

start()