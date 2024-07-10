#importing packages
from bs4 import BeautifulSoup
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv() #load the env into python's os env

#initialized proxies and paths
FETCH_REACT_DOC = os.getenv('FETCH_REACT_DOC')
FETCH_REACT_HOME = os.getenv('FETCH_REACT_HOME')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/react-home.html')

AI_MODEL_SERVER = os.getenv('AI_MODEL_SERVER')

paragraphs = [] #initialized an empty list which later conatins all the scraped data
#variables for multiple instances of a keyword
index = 1

# Fetches the react home page
def reactDocsHomePageFetcher(PROXY):
    data = requests.get(FETCH_REACT_DOC, proxies=PROXY)
    with open(HOME_PATH,'w') as file:
        file.write(data.text)



#creates bs4 soup object
def soupeObjectCreator():
    with open(HOME_PATH) as f:
        react_doc = f.read()
    soupe = BeautifulSoup(react_doc,'html.parser')

    return soupe

#fetches all urls containing the keyword
def fetchUrlFromKeyword(keyword):
    soupe = soupeObjectCreator()
    anchors = soupe.find_all('a')
    relevantUrls = []
    for anchor in anchors:
        hrefPath = anchor.get('href')
        if(keyword in hrefPath.lower()):
            if(hrefPath in relevantUrls):
                continue
            else:
                relevantUrls.append(hrefPath)

    
    if(len(relevantUrls) ==0):
        return('ERROR')
    else:
        return relevantUrls

#scraped pages which are internally hyperlinked in the home page
def inPageRouteScrapper(url):
    soupe = soupeObjectCreator()
    anchor = soupe.find('a', href = url)
    parent = anchor.parent

    for sibling in parent.next_siblings:
        if(sibling.name == 'p'):
            cleaned_text = ' '.join(sibling.get_text().replace('\n', ' ').split())
            paragraphs.append(cleaned_text) #appends to the paragraphs list
        elif(sibling.name == None):
            continue
        else:
            break

#scraped pages which are externally hyperlinked in the home page
def externalRouteScrapper(url, index, keyword):
    data = requests.get(url)

    with open(os.path.join(os.path.dirname(__file__),f'data/react-{keyword}-{index}.html'), 'w') as file:
        file.write(data.text)

    with open(os.path.join(os.path.dirname(__file__),f'data/react-{keyword}-{index}.html')) as file:
        react_doc = file.read()

    soup = BeautifulSoup(react_doc, 'html.parser')
    tags = soup.find_all(['p'])
    
    for i in tags:
        cleaned_text = ' '.join(i.get_text().replace('\n', ' ').split())
        if(cleaned_text!='Is this page useful?'):
            paragraphs.append(cleaned_text)


#Shows the result or returns NONE depending on the availability of the keyword

def search(query, proxy):
    reactDocsHomePageFetcher(proxy)
    index = 1
    fetchedUrls = fetchUrlFromKeyword(query.lower())
    if(fetchedUrls != 'ERROR'):
        for url in fetchedUrls:
            if(url[0] == '#'):
                inPageRouteScrapper(url)

            if(url[0]=='/'):
                externalRouteScrapper(FETCH_REACT_HOME+url,index, query)
                index += 1
        try:
            article = (requests.post(AI_MODEL_SERVER ,headers = {'Content-Type':'application/json'}, data=json.dumps(paragraphs))).text #throws paragraph to an ai model for documentation
        except:
            article = '. '.join(paragraphs) #raw data if the ai model apis do not work
        finally:
            #formats the result
            article = article.replace('. ','.\n').replace('<','\n<').replace('>','>\n').replace(': ',':\n') #formats the data
        return article

    else:
        return None
    
