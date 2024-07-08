import requests 
from bs4 import BeautifulSoup 
import re
import pandas as pd
import proxy_ip
from dotenv import load_dotenv
import os

#loading env variables
load_dotenv()


# fetching proxy url
PROXY = {
    'http': f'{proxy_ip.randomProxyPicker()}'
}

#getting user_input and fetching google search results
user_input = input("Enter something to search: ")
print("searching...")
google_search = requests.get("https://www.google.com/search?q="+user_input+" express js docs")

# creating b.soup object
soup = BeautifulSoup(google_search.text,"html.parser") 

#function for scrapping express js guide webpage 
def scrapGuide():
    file_to_scrap = requests.get(guide_url)
    ejs = BeautifulSoup(file_to_scrap.text,'html.parser')
    # title = ""
    h1_list = ejs.select("h1")
    h2_list = ejs.select("h2")
    for h1 in h1_list:
        if user_input.lower() == h1.get_text().lower():
            data.append(h1.get_text())
            for sib in h1.find_next_siblings():
                if sib.name != "h2" and sib.name != "table":
                    data.append(sib.get_text())
                elif sib.name == "table":
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
        if user_input.lower() in h2.get_text().lower():
            data.append(h2.get_text())
            for sib in h2.find_next_siblings():
                if sib.name != "h2" and sib.name != "table":
                    data.append(sib.get_text())
                elif sib.name == "table":
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

#function for scrapping express js api webpage 
def scrapAPI():
    file_to_scrap = requests.get(api_url)
    soup = BeautifulSoup(file_to_scrap.text,'html.parser')
  
    h2_list = soup.select("h2")
    h3_list = soup.select("h3")

    for h2 in h2_list:
        if user_input.lower() in h2.get_text().lower():
            data.append(h2.get_text())
            for sib in h2.find_next_siblings():
                if sib.name != "h2" and sib.name != "table":
                    data.append(sib.get_text())
                elif sib.name == "table":
                    # for child in sib.children:
                        # if child.name=="table":
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
        if user_input.lower() in h3.get_text().lower():
            data.append(h3.get_text())
            # print(h3.get_text())
            for sib in h3.find_next_siblings():

                print(sib)
                if sib.name != "h3" and sib.name != "table":
                    data.append(sib.get_text())
                elif sib.name == "table":
                    # for child in sib.children:
                        # if child.name=="table":
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
# print(guide_url)
# print(api_url)

#conditional scraping based upon the url and data scrapped
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

     
#scrapping guide url using h2 and h3 tags

    
# print(data)
# updated_data = []
# for item in data:
#     updated_list = []
#     if "\n" in item:
#         list1 = item.split("\n")
#         for i in list1:  
#             if i != '': 
#                 updated_list.append(i)

#     up_string = '\n'.join(updated_list)  
#     updated_data.append(up_string)

# updated_data.insert(0,title)

#saving the output
with open(os.path.join(os.path.dirname(__file__),'data/search.html', "w")) as file:
   for item in data:
        if isinstance(item, pd.DataFrame):
            with open(os.path.join(os.path.dirname(__file__),'data/table.csv'), "w") as csv_file:
                item.to_csv(csv_file, sep='\t') 
        else:
            file.write(item + "\n\n") 

                