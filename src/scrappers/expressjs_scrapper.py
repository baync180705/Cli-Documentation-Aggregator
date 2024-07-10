import requests 
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
import pandas as pd
import re
import os

#loading env variables
load_dotenv()


#defining the search function to be called in cli.py
def search(query, PROXY):

    #defining scrapGuide function to scrap the guide page of express js docs
    def scrapGuide(): 
        file_to_scrap = requests.get(guide_url)
        ejs = BeautifulSoup(file_to_scrap.text,'html.parser')
        h1_list = ejs.select("h1")
        h2_list = ejs.select("h2")
        #scrapping on guide page is done using h1 and h2 tags
        for h1 in h1_list:
            if query.lower() == h1.get_text().lower(): #if h1 tag and user_input matches
                data.append(h1.get_text())
                for sib in h1.find_next_siblings():
                    if sib.name != "h2" and sib.name != "table": #handles cases other than h2 and table tags
                        data.append(sib.get_text())
                    elif sib.name == "table": 
                                data.append(f"///RESPECTIVE TABLE IS SAVED IN {query.split(' ')[0]}.csv FILE")
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
                                df = pd.DataFrame(data=all_rows,columns=headings) #th and td tags are scrapped and table is made using pandas dataframes
                                data.append(df)
                
                    elif sib.name == "pre": # handles pre tags to handle code snippets
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")
                    elif sib.name == "h2": 
                        data.append(sib.get_text())

                    elif sib.name == "h1": #stops at the next h1 tag
                         break
                print()

        for h2 in h2_list:
            if query.lower() in h2.get_text().lower(): #if h2 tag and user_input matches
                data.append(h2.get_text())
                for sib in h2.find_next_siblings():
                    if sib.name != "h2" and sib.name != "table": #handles cases other than h2 and table tags
                        data.append(sib.get_text())
                    elif sib.name == "table":
                                data.append(f"///RESPECTIVE TABLE IS SAVED IN {query.split(' ')[0]}.csv FILE")
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
                                df = pd.DataFrame(data=all_rows,columns=headings) #th and td tags are scrapped and table is made using pandas dataframes
                                data.append(df)
                
                    elif sib.name == "pre": # handles pre tags to handle code snippets
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")

                    elif sib.name == "h2": #stops scraping at the next h2 tag
                        break
                print()

    def scrapAPI():
        file_to_scrap = requests.get(api_url)
        soup = BeautifulSoup(file_to_scrap.text,'html.parser')
    
        h2_list = soup.select("h2")
        h3_list = soup.select("h3")
        #scrapping on api page is done using h2 and h3 tags
        for h2 in h2_list:
            if query.lower() in h2.get_text().lower(): #if user input and h2 heading matches
                data.append(h2.get_text())
                for sib in h2.find_next_siblings():
                    if sib.name != "h2" and sib.name != "table":#handles cases other than h2 and table tags
                        data.append(sib.get_text())
                    elif sib.name == "table":
                                data.append(f"///RESPECTIVE TABLE IS SAVED IN {query.split(' ')[0]}.csv FILE")
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
                                df = pd.DataFrame(data=all_rows,columns=headings) #th and td tags are scrapped and table is made using pandas dataframes
                                data.append(df)
                    elif sib.name == "pre": # handles pre tags to handle code snippets
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")


                    elif sib.name == "h2": #stops scrapping at next h2 tag
                        break
                print()



        for h3 in h3_list:
            if query.lower() in h3.get_text().lower(): #if user input and h2 heading matches
                data.append(h3.get_text())
                for sib in h3.find_next_siblings():
                    if sib.name != "h3" and sib.name != "table": #handles cases other than h3 and table tags
                        data.append(sib.get_text())
                    elif sib.name == "table":
                                data.append(f"///RESPECTIVE TABLE IS SAVED IN {query.split(' ')[0]}.csv FILE")
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
                                df = pd.DataFrame(data=all_rows,columns=headings) #th and td tags are scrapped and table is made using pandas dataframes
                                data.append(df)
                    elif sib.name == "pre": # handles pre tags to handle code snippets
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")
                    elif sib.name == "h3":#stops scrapping at next h3 tag
                        break
                print()



    query = query.lower() 
    google_search = requests.get("https://www.google.com/search?q="+query+" expressjs documentation",proxies=PROXY) #fetches relevant google result

    # creating b.soup object
    soup = BeautifulSoup(google_search.text,"html.parser") 

    article = ""

    #extracting the docs url of the docs to parse
    url_to_parse = ""
    api_url = ""
    guide_url = ""
    data=[]
    guide_first=True
    for h3 in soup.find_all("h3"):
        if api_url == "" or guide_url == "":
            for parent in h3.parents:
                if parent.name == 'a' and guide_url=="":
                    if "expressjs.com/en/guide" in parent["href"]:
                        url_to_parse = parent['href'].split('q=')
                        url_to_parse = url_to_parse[1].split('&')
                        url = url_to_parse[0]
                        guide_url=url
                        guide_first = True
                        break
                if parent.name == 'a' and api_url=="":
                    if "expressjs.com/en/api" in parent["href"]:
                        url_to_parse = parent['href'].split('q=')
                        url_to_parse = url_to_parse[1].split('&')
                        url = url_to_parse[0]
                        api_url = url
                        guide_first=False
                        break
    
    #conditional scrapping based upon the webpage i.e. whether it is api or guide
    if guide_first:
     scrapGuide()
     if data==[]:
          scrapAPI()
    elif not guide_first:
     scrapAPI()
     if data==[]:
          scrapGuide()

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
