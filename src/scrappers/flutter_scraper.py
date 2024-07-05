import os
import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from proxy_ip import randomProxyPicker
from selenium import webdriver


load_dotenv()

keyword = 'listview'

FETCH_FLUTTER_SEARCH = os.getenv('FETCH_FLUTTER_SEARCH')
FLUTTER_HOME_URL = os.getenv('FLUTTER_HOME_URL')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/flutter-search.html')
FILE_PATH = os.path.join(os.path.dirname(__file__),f'data/flutter-{keyword.lower()}.html')
PROXY = {
    'http': f'{randomProxyPicker()}'
}

model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

def flutterDocsSearchPageFetcher():
    try:
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            'httpProxy': f'{randomProxyPicker()}'
        }

        driver.get(FETCH_FLUTTER_SEARCH+keyword)

        data = driver.page_source

        with open(HOME_PATH, 'w') as file:
            file.write(data)

    except:
        print('ERROR')

flutterDocsSearchPageFetcher()

def fetchRelevantUrl():
    with open(HOME_PATH) as f:
        flutter_doc = f.read()

    soupe = BeautifulSoup(flutter_doc,'html.parser')
    path = soupe.find('p').next_sibling.get('data-href')
    return (FLUTTER_HOME_URL+path)

    
def fetchRelevantPage():
    url = fetchRelevantUrl()
    data = requests.get(url, proxies= PROXY )

    with open(FILE_PATH,'w') as f:
        f.write(data.text)

fetchRelevantPage()

def createParagraphsList():
    paragraphs = []
    with open(FILE_PATH) as f:
        flutter_page = f.read()

    soupe = BeautifulSoup(flutter_page, 'html.parser')
    elements = soupe.find_all(['p','code'])

    for element in elements:
        if(element.name == 'p'):
            cleaned_text = ' '.join(element.get_text().replace('\n', ' ').split())
            paragraphs.append(cleaned_text)
        
        if(element.name == 'code'):
            code = ' '.join(['This is a sample code:', element.get_text()])
            paragraphs.append(code)
        
    return paragraphs

paragraphs = createParagraphsList()

def generate_article(sentences):
    prompt = "\n".join(sentences)[:1024]

    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    outputs = model.generate(inputs, max_length=1024, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    
    article = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return article

article = generate_article(paragraphs).replace('. ','.\n').replace('<','\n<').replace('>','>\n').replace(': ',':\n')


with open(os.path.join(os.path.dirname(__file__),f'data/{keyword.lower()}.txt'),'w') as f:
    f.write(article)



