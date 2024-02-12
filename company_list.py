from selenium import webdriver   #to handle chromium webdriver
from bs4 import BeautifulSoup as BS4   #for handling xml page
import time #to pause the scrolling 

#global var
name_list = []
title_list = []

#load the chrome webdriver (get the right one from https://chromedriver.chromium.org/downloads)
browser = webdriver.Chrome("your_path\chromedriver.exe")

#login into the website
browser.get("https://www.linkedin.com/login?")

#submitting login info (replace "username" & "password" with your real login info)
username = "my_user_name"
password = "my_password"

userID = browser.find_element_by_id("username")
userID.send_keys(username)

pswID = browser.find_element_by_id("password")
pswID.send_keys(password)

pswID.submit()

with open ('operatori.txt', 'r', encoding='utf8') as f:
    companies = f.readlines()
    
for company in companies:
    
    browser.get(f"https://www.linkedin.com/search/results/people/?keywords={company}&origin=SWITCH_SEARCH_VERTICAL")

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        #preparing the soup
        search = browser.page_source
        soup = BS4(search, "html.parser")

    #searching all the span attribute to the actor name class  
        people = soup.findAll("span", {"class": "entity-result__title-line flex-shrink-1 entity-result__title-text--black"})
        
        for name in people:
            name_list.append(name.text)
            
        for name in people:
            title_list.append(company)
            
clean_list=[]
new_string=[]
for i in name_list:
    new_string = (i.replace("\n","",-1))
    new_string = new_string.replace("• 1st1st degree connection", "",-1)
    new_string = new_string.replace("• 2nd2nd degree connection", "",-1)
    new_string = new_string.replace("• 3rd+3rd+ degree connection", "",-1)
    clean_list.append(new_string)        
            
org_chart = dict(zip(clean_list, title_list)) 

for key, value in org_chart.items():
    print(key, ': ', value)
