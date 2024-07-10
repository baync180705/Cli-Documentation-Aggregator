import requests 
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
import pandas as pd
import re
import os

#loading env variables
load_dotenv()


def search(query, PROXY):
    def scrapGuide():
        file_to_scrap = requests.get(guide_url)
        ejs = BeautifulSoup(file_to_scrap.text,'html.parser')
        # title = ""
        h1_list = ejs.select("h1")
        h2_list = ejs.select("h2")
        for h1 in h1_list:
            if query.lower() == h1.get_text().lower():
                data.append(h1.get_text())
                for sib in h1.find_next_siblings():
                    if sib.name != "h2" and sib.name != "table":
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
                                df = pd.DataFrame(data=all_rows,columns=headings)
                                data.append(df)
                
                    elif sib.name == "pre":
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")
                    elif sib.name == "h2":
                        data.append(sib.get_text())
                print()

        for h2 in h2_list:
            if query.lower() in h2.get_text().lower():
                data.append(h2.get_text())
                for sib in h2.find_next_siblings():
                    if sib.name != "h2" and sib.name != "table":
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
                                df = pd.DataFrame(data=all_rows,columns=headings)
                                data.append(df)
                
                    elif sib.name == "pre":
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")

                    elif sib.name == "h2":
                        break
                print()

    def scrapAPI():
        file_to_scrap = requests.get(api_url)
        soup = BeautifulSoup(file_to_scrap.text,'html.parser')
    
        h2_list = soup.select("h2")
        h3_list = soup.select("h3")

        for h2 in h2_list:
            if query.lower() in h2.get_text().lower():
                data.append(h2.get_text())
                for sib in h2.find_next_siblings():
                    if sib.name != "h2" and sib.name != "table":
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
                                df = pd.DataFrame(data=all_rows,columns=headings)
                                data.append(df)
                    elif sib.name == "pre":
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")


                    elif sib.name == "h2":
                        break
                print()



        for h3 in h3_list:
            # print("helloji")
            if query.lower() in h3.get_text().lower():
                data.append(h3.get_text())
                # print(h3.get_text())
                for sib in h3.find_next_siblings():

                    # print(sib)
                    if sib.name != "h3" and sib.name != "table":
                        data.append(sib.get_text())
                    elif sib.name == "table":
                        # for child in sib.children:
                            # if child.name=="table":
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
                                df = pd.DataFrame(data=all_rows,columns=headings)
                                data.append(df)
                    elif sib.name == "pre":
                        data.append("\n")
                        data.append(sib.get_text())
                        data.append("\n")
                    elif sib.name == "h3":
                        break
                print()



    query = query.lower()
    google_search = requests.get("https://www.google.com/search?q="+query+" expressjs documentation",proxies=PROXY)

    # creating b.soup object
    soup = BeautifulSoup(google_search.text,"html.parser") 

    article = ""

    #extracting the url of the docs to parse
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
                        # print(url)
                        guide_first=False
                        break
    
    if guide_first:
     scrapGuide()
     if data==[]:
          scrapAPI()
    elif not guide_first:
     scrapAPI()
     if data==[]:
          scrapGuide()


     
    #scrapping api url using h2 and h3 tags
    # if "api" in url:
    #     file_to_scrap = requests.get(url,proxies=PROXY)
    #     soup = BeautifulSoup(file_to_scrap.text,'html.parser')
  
    #     h2_list = soup.select("h2")
    #     h3_list = soup.select("h3")

    #     for h2 in h2_list:
    #         if query in h2.get_text().lower():
    #             title = h2.get_text()
    #     #         print(title)
    #             article += title
    #             for sib in h2.find_next_siblings():
    #                 if sib.name != "h2" and sib.name != "table":
    #     #                 print(sib.get_text())
    #                     article += sib.get_text()
    #     #                 print()
    #                     article += '\n'
    #                 elif sib.name == "table":
    #                     header = []
    #                     rows = []
    #                     for i, row in enumerate(sib.find_all('tr')):
    #                         if i == 0:
    #                             header = [el.text.strip() for el in row.find_all('th')]
    #                         else:
    #                             rows.append([el.text.strip() for el in row.find_all('td')])
    #                     for row in rows:
    #     #                     print(header)
    #                         article += header
    #     #                     print(row)
    #                         article += row
    #                 elif sib.name == "h2":
    #                     break
    #     #         print()
    #             article += '\n'
    #     for h3 in h3_list:
    #         if query in h3.get_text().lower():
    #             title = h3.get_text()
    #     #         print(title)
    #             article += title
    #             for sib in h3.find_next_siblings():
    #                 if sib.name != "h2" and sib.name != "table":
    #     #                 print(sib.get_text())
    #                     article += sib.get_text()
    #     #                 print()
    #                     article += '\n'
    #                 elif sib.name == "table":
    #                     header = []
    #                     rows = []
    #                     for i, row in enumerate(sib.find_all('tr')):
    #                         if i == 0:
    #                             header = [el.text.strip() for el in row.find_all('th')]
    #                         else:
    #                             rows.append([el.text.strip() for el in row.find_all('td')])
    #                     for row in rows:
    #     #                     print(header)
    #                         article += header
    #     #                     print(row)
    #                         article += row
    #     #                     print()
    #                         article += '\n'
    #                 elif sib.name == "h3":
    #                     break
    #     #         print()
    #             article += '\n'
    # #scrapping guide url using h2 and h3 tags
    # else:
    #     file_to_scrap = requests.get(url,proxies=PROXY)
    #     soup = BeautifulSoup(file_to_scrap.text,'html.parser')
    #     title = ""
    #     for h in soup.find("h1"):
    #         title = h

    #     # print(title)
    #     article += title
    #     h2_list = soup.select("h2")
    #     for h2 in h2_list:
    #         if query in h2.get_text().lower():
    #     #         print("h2 hai")
    #             # article += "h2 hai"
    #             title = h2.get_text()
    #     #         print(title)
    #             article += title
    #             for sib in h2.find_next_siblings():
    #                 if sib.name != "h2" and sib.name != "table":
    #     #                 print(sib.get_text())
    #                     article += sib.get_text()
    #     #                 print()
    #                     article += '\n'
    #                 elif sib.name == "table":
    #                     header = []
    #                     rows = []
    #                     for i, row in enumerate(sib.find_all('tr')):
    #                         if i == 0:
    #                             header = [el.text.strip() for el in row.find_all('th')]
    #                         else:
    #                             rows.append([el.text.strip() for el in row.find_all('td')])
    #                     for row in rows:
    #     #                     print("ffsfsjkfdfjksdfhsdfjkd")
    #                         # article += "ffsfsjkfdfjksdfhsdfjkd"
    #     #                     print(header)
    #                         article += header
    #     #                     print(row)
    #                         article += row
    #                 elif sib.name == "h2":
    #                     break
    #     #         print()
    #             article += '\n'
    article = ""

    for item in data:
         if isinstance(item, pd.DataFrame):
              with open(os.path.join(os.path.dirname(__file__),f'data/{query.split(" ")[0]}.csv'), "w") as csv_file:
                item.to_csv(csv_file, sep='\t') 
         else:
            article += item + '\n'
    if len(article.strip()) == 0:
        return None
    else:
        return article
