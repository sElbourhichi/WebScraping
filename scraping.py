# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:13:54 2020

@author: El-bourhichi
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pandas as pd
import time


    
#initialisation and configuration :
max_articles=10
max_pages=100000
jsonFile='www.mubawab.ma_output.json'

PATH ="C:\Program Files (x86)\chromedriver.exe"



# Run the argument with incognito
option = webdriver.ChromeOptions()
option.add_argument(' — incognito')
driver = webdriver.Chrome(executable_path=PATH, chrome_options=option)
lien= "https://www.mubawab.ma/fr/ct/berrechid/immobilier-a-vendre"

#check the website if working correctly
driver.get(lien)

# Wait 30 seconds for page to load and extract the element after it loads
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "ltr.mubaWeb.mubaMA.listingPage")))
except TimeoutException:
    print('Timed out waiting for page to load')
    driver.quit()


print("it works i will follow any article in the settings")


with open(jsonFile, 'w',encoding='UTF-8') as ff:
    ff.write('[')

types=[lien] 
for type in types:
    nbArticles = 0
    for page_number in range(1,max_pages,1):#start and step must be edited
        if nbArticles >= max_articles:
            break
        p = str(page_number)
        # web navigation using url and page number format for this web site
        if p == "1":
            driver.get(type)
        else:
            driver.get(type+':p:'+p)
        articles = driver.find_elements_by_class_name("basicList")#list of all "lire la suite"
        print(articles)
        print('Number of articles in the page '+p+' of '+type+': ', len(articles))
        if len(articles)==0:
            break

        for i in range(len(articles)):
            if nbArticles > max_articles:
                break
            else:
                if(nbArticles>0):
                    with open(jsonFile, 'a',encoding='UTF-8') as ff:
                        ff.write(',')
            if p == "1":
                driver.get(type)
            else:
                driver.get(type+':p:'+p)
            element = driver.find_elements(By.CLASS_NAME,"basicList")[i]



            title=""
            price=""
            place=""
            surface=""
            pieces=""
            chambres=""
            bains=""
            age=""
            etat=""
            tel=[]
            owner=""
            date=""
            #get the data
            try:
                dat=element.find_elements(By.CLASS_NAME,"controlBar")[0]
               
                date=dat.find_elements(By.CLASS_NAME,"premiumDetails")[0].text
            except:
                print("oops can't find date")
            print(date)
           
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            
            time.sleep(5)
            to_click=driver.find_element(By.CLASS_NAME,"hide-phone-number-box")
            
            webdriver.ActionChains(driver).move_to_element(to_click).click(to_click).perform()
            

            try:
                title=driver.find_elements(By.CLASS_NAME,"searchTitle")[0].text
                price=driver.find_elements(By.CLASS_NAME,"orangeTit")[0].text
                place=driver.find_elements(By.CLASS_NAME,"greyTit")[0].text
                surface=driver.find_elements(By.CLASS_NAME,"tagProp")[0].text
                pieces=driver.find_elements(By.CLASS_NAME,"tagProp")[1].text
                chambres=driver.find_elements(By.CLASS_NAME,"tagProp")[2].text
                bains=driver.find_elements(By.CLASS_NAME,"tagProp")[3].text
                age=driver.find_elements(By.CLASS_NAME,"tagProp")[5].text
                etat=driver.find_elements(By.CLASS_NAME,"tagProp")[4].text

                time.sleep(5)
                owner=driver.find_elements(By.CLASS_NAME,"phoneLeadPop.alert.alert-success.inBlock.w100")[0].find_elements(By.TAG_NAME,"div")[1].find_elements(By.TAG_NAME,"p")[1].find_elements(By.TAG_NAME,"b")[0].text
                print(owner)
                
                for p_tag in driver.find_elements(By.CLASS_NAME,"phoneLeadPop.alert.alert-success.inBlock.w100")[0].find_elements(By.TAG_NAME,"div")[2].find_elements(By.TAG_NAME,"p"):
                    tel.append(p_tag.text)

            except:
                print("ERROR in an article")
            #preparing the json object representing one article
            data = "{\"title\":"+"\""+str(title)+"\""
            data+=",\"price\":"+"\""+str(price)+"\""
            data+=",\"place\":"+"\""+str(place)+"\""
            data+=",\"surface\":"+"\""+str(surface)+"\""
            data+=",\"pieces\":"+"\""+str(pieces)+"\""
            data+=",\"chambres\":"+"\""+str(chambres)+"\""
            data+=",\"bains\":"+"\""+str(bains)+"\""
            data+=",\"age\":"+"\""+str(age)+"\""
            data+=",\"etage\":"+"\""+str(etat)+"\""
            data+=",\"tel\":"+str(tel).replace("'","\"")
            data+=",\"owner\":"+"\""+str(owner)+"\""
            data+=",\"date\":"+"\""+str(date)+"\""
            data+="}"
            
            with open(jsonFile, 'a',encoding='UTF-8') as ff:
                ff.write(data)
            nbArticles+=1
            print(data)
            print("*************")

#Close the json file
with open(jsonFile, 'a',encoding='UTF-8') as ff:
    ff.write(']')

#convert the json to csv using pandas
df = pd.read_json(jsonFile)
df.to_csv(jsonFile+'.csv',sep=',', index = None, header=True, encoding="UTF-8")

print("done...")
driver.close()
driver.quit()
