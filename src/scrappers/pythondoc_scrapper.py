import requests 
from bs4 import BeautifulSoup 
# import scrappers.proxy_ip
import os

# PROXY = {
#     'http': f'{proxy_ip.randomProxyPicker()}'
# }

#taking user-input and searching google
# user_input = input("Enter something to search: ")
# print("searching...")
def search(query, PROXY):
    query_first_word = query.lower().split()[0]
    google_search = requests.get("https://www.google.com/search?q="+query+" python docs",proxies=PROXY)
 
    #creating b.soup object of the search_results 
    soup = BeautifulSoup(google_search.text,"html.parser") 
    soup.prettify()

    #extracting url of python docs
    url_to_parse = ""
    url=""
    tutorial=False
    h3_list = soup.find_all("h3")
    google_link_found = False
    for h3 in h3_list:
     if not google_link_found:
        for parent in h3.parents:
            if parent.name == 'a':
                if "docs.python.org/3/tutorial" in parent["href"]:
                        # print("tutorial")
                        url_to_parse = parent['href'].split('q=')
                        url_to_parse = url_to_parse[1].split('&')
                        url = url_to_parse[0]
                        tutorial = True
                        google_link_found=True
                        break

                if "docs.python.org/3/library" in parent["href"] and not tutorial:
                        # print("library")
                        url_to_parse = parent['href'].split('q=')
                        url_to_parse = url_to_parse[1].split('&')
                        url = url_to_parse[0]
                        tutorial = False
                        google_link_found=True
                        break

    title=""
    data =[]
    # print(url)
    #creating b.soup object of the python docs webpage 
    pyp_url = requests.get(url,proxies=PROXY)
    pyp = BeautifulSoup(pyp_url.text,'html.parser')

    sections = pyp.find_all("section")
    if tutorial:
        for section in sections:
            if section.has_attr("id"):
                id = section["id"]
                id = id.replace("-","")
                if query_first_word in id:
                    for child in section.children:
                            if child.name=="h2":
                                title = child.get_text()
                                continue
                            else:
                                data.append(child.get_text())

    elif not tutorial:
        h3_list = pyp.find_all("h3")
        dt_list = pyp.find_all("dt")
        is_h3 = False

        for h3 in h3_list:
          if not is_h3:  
            for child in h3.children:
                if child.name == "a":
                    if query_first_word in child["href"].split("-"):
                        title = h3.get_text()
                        for sib in h3.next_siblings():
                            data.append(sib.get_text()) 
                        is_h3=True
                        break
        for dt in dt_list:
            if not is_h3:
                if dt.has_attr("id") and query_first_word in dt["id"]:
                    title = dt.get_text()
                    siblings = dt.find_next_siblings()
                    for sib in siblings:
                        data.append(sib.get_text())
                    break        


    updated_data = []
    for item in data:
        updated_list = []
        if "\n" in item:
            list1 = item.split("\n")
            for i in list1:  
                if i != '': 
                    updated_list.append(i)

        up_string = '\n'.join(updated_list)  
        updated_data.append(up_string)

    updated_data.insert(0,title)
    article = ""
    for data in updated_data:
        article += data + '\n'

    return article
    # with open(os.path.join(os.path.dirname(__file__),'data/search.html'), "w") as file:
    #     # file.write(gfg.prettify())
    #   for item in updated_data:
    #     file.write(item + "\n")
          
