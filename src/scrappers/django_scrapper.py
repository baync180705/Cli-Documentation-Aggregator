import os
import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from proxy_ip import randomProxyPicker

load_dotenv()

keyword = 'models'

FETCH_DJANGO_SEARCH = os.getenv('FETCH_DJANGO_SEARCH')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/django-search.html')
FILE_PATH = os.path.join(os.path.dirname(__file__),f'data/django-{keyword.lower()}.html')
PROXY = {
    'http': f'{randomProxyPicker()}'
}

model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def djangoDocsSearchedPageFetcher():
    data = requests.get(FETCH_DJANGO_SEARCH+keyword, proxies=PROXY)
    with open(HOME_PATH,'w') as file:
        file.write(data.text)

djangoDocsSearchedPageFetcher()

def fetchRelevantUrl():
    with open(HOME_PATH) as f:
        django_doc = f.read()

    soupe = BeautifulSoup(django_doc,'html.parser')
    a_tag = soupe.find('h2',class_ = 'result-title').children
    
    for anchor in a_tag:
        if(hasattr(anchor,'get')):
            href = anchor.get('href')
            return(href)
        
def fetchRelevantPage():
    url = fetchRelevantUrl()
    data = requests.get(url, proxies= PROXY )

    with open(FILE_PATH,'w') as f:
        f.write(data.text)

fetchRelevantPage()

def createParagraphsList():
    paragraphs = []
    with open(FILE_PATH) as f:
        django_page = f.read()

    soupe = BeautifulSoup(django_page, 'html.parser')
    elements = soupe.find_all(['p','pre'])

    for element in elements:
        if(element.name == 'p'):
            cleaned_text = ' '.join(element.get_text().replace('\n', ' ').split())
            if(cleaned_text != 'The web framework for perfectionists with deadlines.'):
                paragraphs.append(cleaned_text)
        
        if(element.name == 'pre'):
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

article = generate_article(paragraphs).replace('. ','.\n').replace('<','\n<').replace(': ',':\n')


with open(os.path.join(os.path.dirname(__file__),f'data/{keyword.lower()}.txt'),'w') as f:
    f.write(article)