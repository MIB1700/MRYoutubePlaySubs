#! /usr/local/bin/python3.8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from sys import *
from string import *
import re
import time

youtube = "https://www.youtube.com/channel/UCLJffad_3eSofXkBwAR8pKA"
#fname = argv[1]

#open a Safari window
driver = webdriver.Safari()
#maximize window
#driver.maximize_window()
wait = WebDriverWait(driver, 30)
waitAll = WebDriverWait(driver, 30)
waitForSubscribe = WebDriverWait(driver, 30)

driver.get(youtube)
#test = driver.find_element_by_xpath("//text()[contains(.,'Subscribe')]")
#if test.text.upper() == "SUBSCRIBE":
#       print("subscribe")

#subButton = driver.find_element(By.XPATH, "//paper-button[contains(@aria-label,'Subscribe')]")
subButton = waitForSubscribe.until(EC.presence_of_element_located((By.XPATH, "//paper-button[contains(@aria-label,'Subscribe')]")))
subButton.click()
#with open( fname, 'r' ) as rawfile:
#     for l in rawfile.readlines():
#        a = l.split()
#        youtube = ' '.join(map(str, a))

 #       driver.get(youtube + "videos")
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tabsContent']/paper-tab[2]/div"))).click()
#        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'paper-tab') and contains(.//span, 'Videos')]"))).click()
       #waitAll.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='text']"))).click()
        
#        driver.switch_to.Window(driver.window_handles.first())
#        if driver.find_element(By.XPATH, "//text()[contains(.,'Subscribe')]/ancestor::paper-button[1]").size() > 0:
#            driver.find_element(By.XPATH, "//text()[contains(.,'Subscribe')]/ancestor::paper-button[1]").click()
#          #  driver.close()

            
        
#        break
#time.sleep(5)
        
#tabsContent > paper-tab:nth-child(4) > div
#//*[@id="tabsContent"]/paper-tab[2]/div

#//*[@id="tabsContent"]/paper-tab[2]/div

#element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='play-button']")))
#element.click()

driver.close()