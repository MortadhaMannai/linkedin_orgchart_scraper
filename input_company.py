'''
Created by Carlo Occhiena on Dec 2020
'''

from selenium import webdriver   #to handle chromium webdriver
from bs4 import BeautifulSoup as BS4   #for handling xml page
import time #to pause the scrolling 
import getpass #to handle the dynamic password input (in the case you follow that path)

#load the chrome webdriver (get the right one from https://chromedriver.chromium.org/downloads)
browser = webdriver.Chrome("c:\yourpath\chromedriver.exe")

#login into the website
browser.get("https://www.linkedin.com/login?")

'''
#use this if you want to ask the user to input username & psw
user = input ("insert username:\n")
password = getpass.getpass(prompt='Insert password: ', stream=None) 
'''
#submitting login info (replace "username" & "password" with your real login info)
user = "yourusername"
password = "yourpassword"

userID = browser.find_element_by_id("username")
userID.send_keys(user)

pswID = browser.find_element_by_id("password")
pswID.send_keys(password)

pswID.submit()

#get the desidered page & get the company name as input user
company_name = input ("Requested Company Name:\n")
browser.get(f"https://www.linkedin.com/search/results/people/?keywords={company_name}&origin=SWITCH_SEARCH_VERTICAL")

'''
We have to go to the bottom of the page otherwise the results will include just the first few results
'''

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

#appending results in a dictionary and printing it
name_list =[]
title_list = []

for name in people:
    name_list.append(name.text)

for title in titles:
    title_list.append(title.text)

org_chart = dict(zip(name_list, title_list)) 

for key, value in org_chart.items():
    print(key, ': ', value)
