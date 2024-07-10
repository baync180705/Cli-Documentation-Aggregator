import requests 
from bs4 import BeautifulSoup 
import os
import pandas as pd
import re


#defining a search function to be called for scrapping GeekforGeeks website
def search(query, PROXY):

    google_search = requests.get("https://www.google.com/search?q="+query+" geekforgeeks",proxies=PROXY) #fetches relevant google result

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


    #fetching webpage
    gfg_req = requests.get(url,proxies=PROXY)
    gfg = BeautifulSoup(gfg_req.text,"html.parser")

    data = []
    #scrapping h1 tag for title
    h1_list = gfg.select("h1")
    title = h1_list[0].get_text()
    data.append(title)

    #creating articles list 
    articles = gfg.select("article")

     #creating gfg panels list for code snippets 
    gfg_panel = gfg.find_all("gfg-panel")

    #accessing first article
    article = articles[0]

    #declaring a constant to access third div
    i = 0

    for c in article.children:
        #accessing the third div
        if c.name == "div":
            i=i+1
            if i==3:
             for child in c.children:
                if child.name == "gfg-tabs": #handles code snippets
                    for g in gfg_panel:
                        if child in g.parents:
                            data.append(g.get_text()+"\n")
                elif child.name == "div" and child.has_attr("id") and child["id"] == "table_of_content": #ignores table of content
                     continue
                elif child.name == "p": #handles paragraph elements
                            data.append(child.get_text()+"\n")
                elif child.name == "ul": #handles list elements
                        list1 =[]
                        for c in child.children:
                            list1.append(c)
                        for i in list1:
                            data.append(str(list1.index(i)+1)+" " + i.get_text()+"\n")
                elif child.name == "table": #handles table elements
                            data.append(f"///RESPECTIVE TABLE IS SAVED IN {query.split(' ')[0]}.csv FILE")
                            body = child.find_all("tr")
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
                            df = pd.DataFrame(data=all_rows,columns=headings) #th and td tags are scrapped and table is made using pandas dataframes
                            data.append(df)
                elif child.name == "br": #breaks on reaching br tag i.e end of article
                        break
                else:
                     data.append(child.get_text()+"\n")

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

    #adds title
    updated_data.insert(0,title)

    #saving the data into article variable and dataframes into  a csv file in data directory

    article = ""
    for item in updated_data:
         if isinstance(item, pd.DataFrame):
              with open(os.path.join(os.path.dirname(__file__),f'data/{query.split(" ")[0]}.csv'), "w") as csv_file:
                item.to_csv(csv_file, sep='\t') 
         else:
            article += item + '\n'

    if len(article.strip()) == 0: #if no result is fetched then None is returned for the AI to be called
        return None
    else:
        return article #returns data



