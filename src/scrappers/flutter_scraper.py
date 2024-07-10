#importing packages
import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from proxy_ip.proxy_ip import randomProxyPicker
from selenium import webdriver


load_dotenv() #load the env into python's os env


#initialized proxies and paths
FETCH_FLUTTER_SEARCH = os.getenv('FETCH_FLUTTER_SEARCH')
FLUTTER_HOME_URL = os.getenv('FLUTTER_HOME_URL')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/flutter-search.html')

AI_MODEL_SERVER = os.getenv('AI_MODEL_SERVER')



options = webdriver.ChromeOptions()
options.add_argument('--headless') #options for the driver

driver = webdriver.Chrome(options=options) #sets up a selenium webdriver for chrome with the given options

# Fetches the react search page
def flutterDocsSearchPageFetcher(query):
    try:
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            'httpProxy': f'{randomProxyPicker()}'
        }

        driver.get(FETCH_FLUTTER_SEARCH+query)

        data = driver.page_source

        with open(HOME_PATH, 'w') as file:
            file.write(data)

    except:
        print('ERROR')


#fetches the relevant url containint the keyword
def fetchRelevantUrl():
    with open(HOME_PATH) as f:
        flutter_doc = f.read()


    soupe = BeautifulSoup(flutter_doc,'html.parser')
    if (soupe.find('p') != None):
        path = soupe.find('p').next_sibling.get('data-href')
        return (FLUTTER_HOME_URL+path)
    else:
        return ("ERROR")


#gets the webpage of the fetched relevant url and catches error if keyword not found
def fetchRelevantPage(query, PROXY):
    url = fetchRelevantUrl()
    if(url != 'ERROR'):
        data = requests.get(url, proxies= PROXY )

        with open(os.path.join(os.path.dirname(__file__),f'data/flutter-{query.lower()}.html'),'w') as f:
            f.write(data.text)
    else:
        return None #returns None if the keyword is not found


#generates the paragraph list conatining all the scraped data
def createParagraphsList(query):
    paragraphs = []
    with open(os.path.join(os.path.dirname(__file__),f'data/flutter-{query.lower()}.html')) as f:
        flutter_page = f.read()

    soupe = BeautifulSoup(flutter_page, 'html.parser')
    elements = soupe.find_all(['p','code'])

    for element in elements:
        if(element.name == 'p'):
            cleaned_text = ' '.join(element.get_text().replace('\n', ' ').split())
            paragraphs.append(cleaned_text) #paragraphs appended
        
        if(element.name == 'code'):
            code = ' '.join(['This is a sample code:', element.get_text()])
            paragraphs.append(code) #codes appended
        
    return paragraphs

#Shows the result if keyword exists

def search(query, proxy):
    flutterDocsSearchPageFetcher(query)
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


