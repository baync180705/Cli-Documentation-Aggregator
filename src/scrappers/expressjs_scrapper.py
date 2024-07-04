import requests 
from bs4 import BeautifulSoup 
import proxy_ip
from dotenv import load_dotenv

#loading env variables
load_dotenv()


#fetching proxy url
PROXY = {
    'http': f'{proxy_ip.randomProxyPicker()}'
}

#getting user_input and fetching google search results
user_input = input("Enter something to search: ")
print("searching...")
google_search = requests.get("https://www.google.com/search?q="+user_input+" expressjs documentation",proxies=PROXY)

# creating b.soup object
soup = BeautifulSoup(google_search.text,"html.parser") 

#extracting the url of the docs to parse
url_to_parse = ""
url=""
for parent in soup.find("h3").parents:
    if parent.name == 'a':
        if "expressjs.com" in parent["href"]:
            url_to_parse = parent['href'].split('q=')
            url_to_parse = url_to_parse[1].split('&')
            url = url_to_parse[0]

#scrapping api url using h2 and h3 tags
if "api" in url:
    file_to_scrap = requests.get(url,proxies=PROXY)
    soup = BeautifulSoup(file_to_scrap.text,'html.parser')
  
    h2_list = soup.select("h2")
    h3_list = soup.select("h3")

    for h2 in h2_list:
        if user_input.lower() in h2.get_text().lower():
            print("h2 hai")
            title = h2.get_text()
            print(title)
            for sib in h2.find_next_siblings():
                if sib.name != "h2" and sib.name != "table":
                    print(sib.get_text())
                    print()
                elif sib.name == "table":
                    header = []
                    rows = []
                    for i, row in enumerate(sib.find_all('tr')):
                        if i == 0:
                            header = [el.text.strip() for el in row.find_all('th')]
                        else:
                            rows.append([el.text.strip() for el in row.find_all('td')])
                    for row in rows:
                        print("ffsfsjkfdfjksdfhsdfjkd")
                        print(header)
                        print(row)
                elif sib.name == "h2":
                    break
            print()
    for h3 in h3_list:
        if user_input.lower() in h3.get_text().lower():
            title = h3.get_text()
            print(title)
            for sib in h3.find_next_siblings():
                if sib.name != "h2" and sib.name != "table":
                    print(sib.get_text())
                    print()
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
                elif sib.name == "h3":
                    break
            print()
#scrapping guide url using h2 and h3 tags
else:
    file_to_scrap = requests.get(url,proxies=PROXY)
    soup = BeautifulSoup(file_to_scrap.text,'html.parser')
    title = ""
    for h in soup.find("h1"):
        title = h

    print(title)
    h2_list = soup.select("h2")
    for h2 in h2_list:
        if user_input.lower() in h2.get_text().lower():
            print("h2 hai")
            title = h2.get_text()
            print(title)
            for sib in h2.find_next_siblings():
                if sib.name != "h2" and sib.name != "table":
                    print(sib.get_text())
                    print()
                elif sib.name == "table":
                    header = []
                    rows = []
                    for i, row in enumerate(sib.find_all('tr')):
                        if i == 0:
                            header = [el.text.strip() for el in row.find_all('th')]
                        else:
                            rows.append([el.text.strip() for el in row.find_all('td')])
                    for row in rows:
                        print("ffsfsjkfdfjksdfhsdfjkd")
                        print(header)
                        print(row)
                elif sib.name == "h2":
                    break
            print()
