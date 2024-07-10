#importing packages
import requests
import random
import os

FETCH_PROXY_URL = os.getenv('FETCH_PROXY_URL') #api endpoint for fetching proxy ips
PATH = os.path.join(os.path.dirname(__file__),'data/free-proxy-list.txt') #file location to store all ip addresses 

proxyList = []

data = requests.get(FETCH_PROXY_URL)

#generates free-proxy-list.txt file
def generateFile():
    with open(PATH,'w') as file:
            file.write(data.text)

#initializes proxyList[]
def createProxyList():
    with open(PATH) as file:
        for index in range(0,20):
            line = file.readline().split('\n')[0]
            proxyList.append(line)

    
    return(proxyList)

#returns a random ip address from proxyList
def randomProxyPicker():
    generateFile()
    proxies = createProxyList()
    return random.choice(proxies)

