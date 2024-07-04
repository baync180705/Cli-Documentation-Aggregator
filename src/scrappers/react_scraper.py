from transformers import GPT2LMHeadModel, GPT2Tokenizer
from bs4 import BeautifulSoup
import os
import requests
import proxy_ip
from dotenv import load_dotenv

load_dotenv()

FETCH_REACT_DOC = os.getenv('FETCH_REACT_DOC')
FETCH_REACT_HOME = os.getenv('FETCH_REACT_HOME')
HOME_PATH = os.path.join(os.path.dirname(__file__),'data/react-home.html')

PROXY = {
    'http': f'{proxy_ip.randomProxyPicker()}'
}

model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

index = 1
keyword = 'usestate'

def reactDocsHomePageFetcher():
    data = requests.get(FETCH_REACT_DOC, proxies=PROXY)
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
        if(keyword in hrefPath.lower()):
            if(hrefPath in relevantUrls):
                continue
            else:
                relevantUrls.append(hrefPath)

    
    if(len(relevantUrls) ==0):
        print(f'ERROR: keyword: {keyword} not found. Please try with a different keyword.')
    else:
        return relevantUrls


fetchedUrls = fetchUrlFromKeyword(keyword.lower())

 
print(fetchedUrls)
paragraphs = []

def inPageRouteScrapper(url):

    soupe = soupeObjectCreator()
    anchor = soupe.find('a', href = url)
    parent = anchor.parent

    for sibling in parent.next_siblings:
        if(sibling.name == 'p'):
            cleaned_text = ' '.join(sibling.get_text().replace('\n', ' ').split())
            paragraphs.append(cleaned_text)
        elif(sibling.name == None):
            continue
        else:
            break

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




for url in fetchedUrls:
    if(url[0] == '#'):
        inPageRouteScrapper(url)

    if(url[0]=='/'):
        externalRouteScrapper(FETCH_REACT_HOME+url,index, keyword)
        index += 1



def generate_article(sentences):
    prompt = "\n".join(sentences)[:1024]

    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    outputs = model.generate(inputs, max_length=1024, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    
    article = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return article

article = generate_article(paragraphs).replace('. ','.\n').replace('<','\n<').replace('>','>\n')


with open(os.path.join(os.path.dirname(__file__),f'data/{keyword}.txt'),'w') as f:
    f.write(article)