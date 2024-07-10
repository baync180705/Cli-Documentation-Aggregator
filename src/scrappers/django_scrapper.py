#importing packages
import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from proxy_ip.proxy_ip import randomProxyPicker

load_dotenv() #load the env into python's os env

#initialized proxies and paths
FETCH_DJANGO_SEARCH = os.getenv('FETCH_DJANGO_SEARCH')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/django-search.html')
AI_MODEL_SERVER = os.getenv('AI_MODEL_SERVER')

# Fetches the react search page
def djangoDocsSearchedPageFetcher(query,PROXY):
    data = requests.get(FETCH_DJANGO_SEARCH+query, proxies=PROXY)
    with open(HOME_PATH,'w') as file:
        file.write(data.text)

#fetches the relevant url containint the keyword
def fetchRelevantUrl():
    with open(HOME_PATH) as f:
        django_doc = f.read()

    soupe = BeautifulSoup(django_doc,'html.parser')

    if(soupe.find('h2',class_ = 'result-title') != None):
        a_tag = soupe.find('h2',class_ = 'result-title').children
        for anchor in a_tag:
            if(hasattr(anchor,'get')):
                href = anchor.get('href')
                return(href)
    else:
        return 'ERROR'
    

#get the webpage of the fetched relevant url and catches error if keyword not found
def fetchRelevantPage(query, PROXY):
    url = fetchRelevantUrl()

    if(url != 'ERROR'):
        data = requests.get(url, proxies= PROXY )
        with open(os.path.join(os.path.dirname(__file__),f'data/django-{query.lower()}.html'),'w') as f:
            f.write(data.text)
        return('ok')
    else:
        return None

#generates the paragraph list conatining all the scraped data
def createParagraphsList(query):
    paragraphs = [] #empty list initialized
    with open(os.path.join(os.path.dirname(__file__),f'data/django-{query.lower()}.html')) as f:
        django_page = f.read()

    soupe = BeautifulSoup(django_page, 'html.parser')
    elements = soupe.find_all(['p','pre']) 

    for element in elements:
        if(element.name == 'p'):
            cleaned_text = ' '.join(element.get_text().replace('\n', ' ').split())
            if(cleaned_text != 'The web framework for perfectionists with deadlines.'):
                paragraphs.append(cleaned_text) #paragraphs appended
        
        if(element.name == 'pre'):
            code = ' '.join(['This is a sample code:', element.get_text()])
            paragraphs.append(code) #codes appended
        
    return paragraphs


#Shows the result if keyword exists
def search(query, proxy):
    djangoDocsSearchedPageFetcher(query,proxy)
    if (fetchRelevantPage(query, proxy) == None):
        return None
    else:
        fetchRelevantPage(query,proxy)
        paragraphs = createParagraphsList(query)
        try:
            article = (requests.post(AI_MODEL_SERVER,headers = {'Content-Type':'application/json'}, data=json.dumps(paragraphs))).text #throws paragraph to an ai model for documentation
        except:
            article = '. '.join(paragraphs) #raw data if the ai model apis do not work
        finally:
            article = article.replace('. ','.\n').replace('<','\n<').replace('>','>\n').replace(': ',':\n') #formats the data
        return article