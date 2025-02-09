import requests 
from bs4 import BeautifulSoup 

import os
import pandas as pd
import re


def search(query, PROXY): 
#defining a search function to be called for scrapping python docs

    google_search = requests.get("https://www.google.com/search?q="+query+" python docs",proxies=PROXY) #fetches relevant google result
 
    #creating b.soup object of the search_results 
    soup = BeautifulSoup(google_search.text,"html.parser") 
    soup.prettify()

    #extracting url of python docs and tracking if the relevant url is from tutorial/library/reference webpage
    url_to_parse = ""
    url=""
    tutorial=False
    library=False
    reference=False
    h3_list = soup.find_all("h3")
    google_link_found = False
    for h3 in h3_list:
        if not google_link_found:
            for parent in h3.parents:
                if parent.name == 'a':
                    if "docs.python.org/3/tutorial" in parent["href"] and url=="":
                            url_to_parse = parent['href'].split('q=')
                            url_to_parse = url_to_parse[1].split('&')
                            url = url_to_parse[0]
                            tutorial = True
                            google_link_found=True
                            break

                    if "docs.python.org/3/library" in parent["href"] and url=="":
                            url_to_parse = parent['href'].split('q=')
                            url_to_parse = url_to_parse[1].split('&')
                            url = url_to_parse[0]
                            library = True
                            google_link_found=True
                            break
                    
                    if "docs.python.org/3/reference" in parent["href"] and url=="":
                            url_to_parse = parent['href'].split('q=')
                            url_to_parse = url_to_parse[1].split('&')
                            url = url_to_parse[0]
                            reference = True
                            google_link_found=True
                            break


    data =[]

    #creating b.soup object of the python docs webpage 
    pyp_url = requests.get(url,proxies=PROXY)
    pyp = BeautifulSoup(pyp_url.text,'html.parser')

# scraps tutorial webpage by scrapping sections
    if tutorial:
        sections = pyp.find_all("section")
        for section in sections:
            if section.has_attr("id"):
                id = section["id"]
                id = id.replace("-","")
                if query.lower().split(' ')[0] in id:
                    for child in section.children:
                            # if child.name=="h2":
                            #     title = child.get_text()
                            #     continue
                            # else:
                                data.append(child.get_text())

# scraps library webpage by scrapping h2/h3/dt tags based upon user input
    elif library:
        #creating lists and conditions
        h2_list = pyp.find_all("h2")
        h3_list = pyp.find_all("h3")
        dt_list = pyp.find_all("dt")
        is_h3 = False
        is_h2 = False

    #checking h2 tags based upon user input and handles table tags and other cases
        for h2 in h2_list:
            if not is_h3 and not is_h2:  
                for child in h2.children:
                    if child.name == "a":
                        if query.lower().split(" ")[0] in child["href"].split("-"):
                            data.append(h2.get_text())
                            for sib in h2.next_siblings():
                                if sib.name == "div" and sib.child.name == "table":
                                    body = sib.find_all("tr")
                                    head = body[0] 
                                    body_rows = body[1:]
                                    headings = []
                                    for item in head.find_all("th"):
                                        item = (item.text).rstrip("\n")
                                        headings.append(item)
                                    all_rows = []
                                    for row_num in range(len(body_rows)):       
                                        row = []
                                        for row_item in body_rows[row_num].find_all("td"):   
                                                    aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
                                                    row.append(aa)
                                        all_rows.append(row)
                                    df = pd.DataFrame(data=all_rows,columns=headings)
                                    data.append(df)
                                else:
                                    data.append(sib.get_text()) 
                            is_h2=True #if relevant h2 is found then loop is breaked
                            break

    #checking h3 tags based upon user input and handles table tags and other cases
        for h3 in h3_list:
            if not is_h3 and not is_h2:  
                for child in h3.children:
                    if child.name == "a":
                        if query.lower().split(" ")[0] in child["href"].split("-"):
                            title = h3.get_text()
                            for sib in h3.next_siblings():
                                if sib.name == "div" and sib.child.name == "table":
                                    body = sib.find_all("tr")
                                    head = body[0] 
                                    body_rows = body[1:]
                                    headings = []
                                    for item in head.find_all("th"):
                                        item = (item.text).rstrip("\n")
                                        headings.append(item)
                                    all_rows = []
                                    for row_num in range(len(body_rows)):       
                                        row = []
                                        for row_item in body_rows[row_num].find_all("td"):   
                                                    aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
                                                    row.append(aa)
                                        all_rows.append(row)
                                    df = pd.DataFrame(data=all_rows,columns=headings)
                                    data.append(df)
                                else:
                                    data.append(sib.get_text()) 
                            is_h3=True  #if relevant h3 is found then loop is breaked
                            break

     #checking dt tags based upon user input                    
        for dt in dt_list:
            if not is_h3 and not is_h2:
                if dt.has_attr("id") and query.lower().split(" ")[0] in dt["id"]:
                    data.append(dt.get_text())
                    siblings = dt.find_next_siblings()
                    for sib in siblings:
                        data.append(sib.get_text())
                    break        

# scraps reference webpage by scrapping sections based upon user input
    elif reference:
        sections = pyp.find_all("section")
        for section in sections:
            if section.has_attr("id"):
                id = section["id"]
                id = id.replace("-","")
                if query.lower().split(' ')[0] in id:
                    for child in section.children:
                            # if child.name=="h2":
                            #     title = child.get_text()
                            #     continue
                            # else:
                                data.append(child.get_text())

# formats the data by removing excess of \n 
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


    article = ""
    #saving the data into article variable and dataframes into  a csv file in data directory
    for item in data:
         if isinstance(item, pd.DataFrame):
              with open(os.path.join(os.path.dirname(__file__),f'data/{query.split(" ")[0]}.csv'), "w") as csv_file:
                item.to_csv(csv_file, sep='\t') 
         else:
            article += item + '\n'

    if len(article.strip()) == 0: #if no result is fetched then None is returned for the AI to be called
        return None
    else:
        return article #returns data

