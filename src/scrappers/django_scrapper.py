#importing packages
import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from proxy_ip import randomProxyPicker

load_dotenv() #load the env into python's os env

keyword = 'templates' #keyword entered

#initialized proxies and paths
FETCH_DJANGO_SEARCH = os.getenv('FETCH_DJANGO_SEARCH')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/django-search.html')
FILE_PATH = os.path.join(os.path.dirname(__file__),f'data/django-{keyword.lower()}.html')
PROXY = {
    'http': f'{randomProxyPicker()}'
}
AI_MODEL_SERVER = os.getenv('AI_MODEL_SERVER')

# Fetches the react search page
def djangoDocsSearchedPageFetcher():
    data = requests.get(FETCH_DJANGO_SEARCH+keyword, proxies=PROXY)
    with open(HOME_PATH,'w') as file:
        file.write(data.text)

djangoDocsSearchedPageFetcher()

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
def fetchRelevantPage():
    url = fetchRelevantUrl()

    if(url != 'ERROR'):
        data = requests.get(url, proxies= PROXY )
        with open(FILE_PATH,'w') as f:
            f.write(data.text)
    else:
        print(f'ERROR: keyword: {keyword} not found. Please try with a different keyword.') #catches error if keyword is not found

fetchRelevantPage()

#generates the paragraph list conatining all the scraped data
def createParagraphsList():
    paragraphs = [] #empty list initialized
    with open(FILE_PATH) as f:
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
if(os.path.exists(FILE_PATH)):
    paragraphs = createParagraphsList()
    try:
        article = (requests.post(AI_MODEL_SERVER, headers = {'Content-Type':'application/json'}, data=json.dumps(paragraphs))).text #throws paragraph to an ai model for documentation
    except:
        article = '. '.join(paragraphs) #raw data if the ai model apis do not work
    finally:
        article = article.replace('. ','.\n').replace('<','\n<').replace('>','>\n').replace(': ',':\n') #formats the data
        with open(os.path.join(os.path.dirname(__file__),f'data/{keyword.lower()}.txt'),'w') as f:
            f.write(article)