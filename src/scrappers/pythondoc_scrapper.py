import requests 
from bs4 import BeautifulSoup 
import proxy_ip
from dotenv import load_dotenv

load_dotenv()
PROXY = {
    'http': f'{proxy_ip.randomProxyPicker()}'
}

#taking user-input and searching google
user_input = input("Enter something to search: ")
print("searching...")

google_search = requests.get("https://www.google.com/search?q="+user_input+" python docs",proxies=PROXY)
 
#creating b.soup object of the search_results 
soup = BeautifulSoup(google_search.text,"html.parser") 
soup.prettify()

#extracting url of python docs
url_to_parse = ""
url=""
for parent in soup.find("h3").parents:
    if parent.name == 'a':
        if "docs.python.org" in parent["href"]:
            # if "tutorial" in parent["href"]: 
                # print("gvfgdfgdfg " + parent['href'])
                url_to_parse = parent['href'].split('q=')
                url_to_parse = url_to_parse[1].split('&')
                url = url_to_parse[0]


#creating b.soup object of the python docs webpage 
pyp_url = requests.get(url,proxies=PROXY)
pyp = BeautifulSoup(pyp_url.text,'html.parser')

#handling the case if there are gaps in user_input
user_input_array = []

#declaring constants and initializing lists for storing heading with h2, dt tags and section tags
title =""
h2_hai = False
dt_hai = False
h2_list = pyp.select("h2")
dt_list = pyp.select("dt")
updated_h2_list = [] 
section_list = pyp.select("section")
user_input_array = user_input
h2_to_search = ""
dt_to_search = ""

#getting the h2 title after removing the numerical part
for i in h2_list:
    if section_list[0] in i.parents:
        # print(i)
        i = i.get_text().split(' ')
        st = ""
        for j in i:
            if j == i[0]:
                continue
            elif j == i[-1]:
                j = j[0:len(j)-2]
                st = st + j + " "
            else:
                st = st + j + " " 
        updated_h2_list.append(st)

#checking if required content to scrap has h2 heading or not
for i in updated_h2_list:
    if " " in user_input:
        user_input_array = user_input.split(" ")
        for j in user_input_array:
            if j.lower() in i: 
                title = i
                h2_to_search=i
                h2_hai = True
                break
    else:
        if user_input.lower() in i: 
                title = i
                h2_to_search=i
                h2_hai = True
                break
        
#checking if required content to scrap has dt heading or not
for i in dt_list:
    if " " in user_input:
        user_input_array = user_input.split(" ")
        for j in user_input_array:
            if j.lower() in i.get_text(): 
                title = i.get_text()
                dt_to_search = i.get_text()
                dt_hai = True
                # print(dt_hai)
                break
    else:
        if user_input.lower() in i.get_text(): 
                title = i.get_text()
                dt_to_search = i.get_text()
                dt_hai = True
                break
#function to get rid of special characters from h2
def get_text(i):
        i = i.get_text().split(' ')
        st = ""
        for j in i:
            if j == i[0]:
                continue
            elif j == i[-1]:
                j = j[0:len(j)-2]
                st = st + j + " "
            else:
                st = st + j + " " 
        return st

#scrapping text if h2 is the heading
if h2_hai:
    print(h2_to_search)
    for h2 in h2_list:
        if section_list[0] in h2.parents:
            if h2_to_search == get_text(h2):
                # print("ehdfhf")
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
                            print(header)
                            print(row)
                    elif sib.name == "h2":
                        break
                print()
        
# scrapping text if dt is the heading
if dt_hai:
    # print(dt_to_search)
    for d in dt_list:
        if dt_to_search in d.get_text():
                for child in d.parent.children:
                    print(child.get_text())
                print()






