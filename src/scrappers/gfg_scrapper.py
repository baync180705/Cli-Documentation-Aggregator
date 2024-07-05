import requests 
from bs4 import BeautifulSoup 
import proxy_ip
from dotenv import load_dotenv

load_dotenv()
PROXY = {
    'http': f'{proxy_ip.randomProxyPicker()}'
}

#taking user input 
user_input = input("Enter something to search: ")
print("searching...")

google_search = requests.get("https://www.google.com/search?q="+user_input+" geekforgeeks",proxies=PROXY)
 

#creating b.soup object of google-search
soup = BeautifulSoup(google_search.text,"html.parser") 
soup.prettify()


#extracting the url of the website to parse
url_to_parse = ""
url=""
for parent in soup.find("h3").parents:
    if parent.name == 'a':
        if "geeksforgeeks" in parent["href"]:
            url_to_parse = parent['href'].split('q=')
            url_to_parse = url_to_parse[1].split('&')
            url = url_to_parse[0]

#fetching webpage and scrapping it
gfg_req = requests.get(url,proxies=PROXY)
gfg = BeautifulSoup(gfg_req.text,"html.parser")
# with open("/home/deenank/Desktop/BeautifulSoup/search.html","w") as f:
#     f.write(gfg.prettify())

#declaring constants and heading lists
h1_list = gfg.select("h1")
title = h1_list[0].get_text()
print(title)
article = gfg.find("article")
h2_list = gfg.select("h2")
h3_list = gfg.select("h3")
code_list = gfg.find_all("code")
is_style = True
h2_hi_hai = False


#checking the condition for which type of webpage to scrap
for h2 in h2_list:
    if article in h2.parents:
        if h2.has_attr("class"): 
            if h2["class"][0] != "tabtitle":
                h2_hi_hai = True
        else:
            h2_hi_hai = True  


#if page contains h2tag
if h2_hi_hai:
    for h2 in h2_list:
        if article in h2.parents and is_style:
            print(h2.get_text())
            for sib in h2.find_next_siblings():
                if sib.name == "h2":
                    break
                elif sib.name == "ul":
                    list1 =[]
                    for child in sib.children:
                        list1.append(child)
                    for i in list1:
                        print(str(list1.index(i)+1)+" " + i.get_text())
                    print()
                elif sib.name=="gfg-tabs":
                    for code in code_list:
                        for parent in code.parents:
                            if parent == sib:
                                print(code.get_text())
                elif sib.name == "img":
                    continue
                elif sib.name == "table":
                        header = []
                        rows = []
                        for i, row in enumerate(sib.find_all('tr')):
                            if i == 0:
                                header = [el.text.strip() for el in row.find_all('th')]
                            else:
                                rows.append([el.text.strip() for el in row.find_all('td')])
                        for row in rows:
                            print(header)
                            print(row)
                            print()
                elif sib.name == "br":
                    is_style = False
                    break
                else:
                    print(sib.get_text()) 
                    print()
#if page contains h3tags only
else:
    for h3 in h3_list:
        if article in h3.parents and is_style:
            print(h3.get_text())
            for sib in h3.find_next_siblings():
                if sib.name == "h3":
                    break
                elif sib.name == "ul":
                    list1 =[]
                    for child in sib.children:
                        list1.append(child)
                    for i in list1:
                        print(str(list1.index(i)+1)+" " + i.get_text())
                    print()
                elif sib.name=="gfg-tabs":
                    for code in code_list:
                        for parent in code.parents:
                            if parent == sib:
                                print(code.get_text())
                elif sib.name == "img":
                    continue
                elif sib.name == "table":
                        header = []
                        rows = []
                        for i, row in enumerate(sib.find_all('tr')):
                            if i == 0:
                                header = [el.text.strip() for el in row.find_all('th')]
                            else:
                                rows.append([el.text.strip() for el in row.find_all('td')])
                        for row in rows:
                            print(header)
                            print(row)
                            print()
                elif sib.name == "br":
                    is_style = False
                    break
                else:
                    print(sib.get_text()) 
                    print()
    