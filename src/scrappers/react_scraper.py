from bs4 import BeautifulSoup
import os
import requests
import proxy_ip
from dotenv import load_dotenv

load_dotenv()

FETCH_REACT_DOC = os.getenv('FETCH_REACT_DOC')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/react-home.html')

proxies = {
    'http': f'{proxy_ip.randomProxyPicker()}'
}

def reactDocsHomePageFetcher():
    data = requests.get(FETCH_REACT_DOC, proxies=proxies)
    with open(HOME_PATH,'w') as file:
        file.write(data.text)

def soupeObjectCreator():
    if(os.path.exists(HOME_PATH)):
        with open(HOME_PATH) as f:
            react_doc = f.read()
        soupe = BeautifulSoup(react_doc,'html.parser')

        return soupe
    else:
        reactDocsHomePageFetcher()
        soupeObjectCreator()

def fetchUrlFromKeyword(keyword):
    soupe = soupeObjectCreator()
    anchors = soupe.find_all('a')
    relevantUrls = []
    for anchor in anchors:
        hrefPath = anchor.get('href')
        if(keyword in hrefPath):
            relevantUrls.append(hrefPath)

    
    if(relevantUrls == []):
        return (f'ERROR: keyword: {keyword} not found. Please try with a different keyword.')
    else:
        return relevantUrls


fetchedUrls = fetchUrlFromKeyword('icon')
print(fetchedUrls)