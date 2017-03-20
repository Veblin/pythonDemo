import requests
import time
from selenium import webdriver
# file path
import os
BASE_DIR = os.path.dirname(__file__)
phjs_path = os.path.join(BASE_DIR,'login.phjs.js') 
print ('*******'+phjs_path+'*******')
driver = webdriver.PhantomJS(executable_path=phjs_path)
driver.get('http://autoinsights.autodmp.com/user/login')
time.sleep(3)
print(driver.find_element_by_tag_name('form').text)
driver.close()