from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib2
 
searchterm = 'person' 
url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
browser.get(url)
 
header={'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"}
counter = 0
succounter = 0
 
print(os.path)
if not os.path.exists(searchterm):
    os.mkdir(searchterm)
 
for _ in range(500):
    browser.execute_script("window.scrollBy(0,10000)")
 
for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
    counter = counter + 1
    print ("Total Count:", counter)
    print ("Succsessful Count:", succounter)
    print ("URL:",json.loads(x.get_attribute('innerHTML'))["ou"])
 
    img = json.loads(x.get_attribute('innerHTML'))["ou"]
    imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
    
    try:
        req = urllib2.Request(img, headers={'User-Agent': header})
        raw_img = urllib2.urlopen(req).read()
        File = open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb")
        File.write(raw_img)
        File.close()
        succounter = succounter + 1
    except:
            print ("can't get img")
            
print (succounter, "succesfully downloaded")
browser.close()
