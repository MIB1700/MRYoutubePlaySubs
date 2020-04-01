#! /usr/local/bin/python3.8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import threading
import time
import sys, getopt
import random
import math
import datetime
import re



keepLooping = True
loopLength = 5
youtube = "https://www.youtube.com/"
count = 0

#open a Safari window
driver = webdriver.Safari()
driver.get(youtube)
actions = ActionChains(driver)
#maximize window
driver.maximize_window()
wait = WebDriverWait(driver, 15)
waitForSearch = WebDriverWait(driver, 15)
waitForNext = WebDriverWait(driver, 15)

element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='contents']/ytd-rich-item-renderer[1]")))
element.click()

def skipAdFunction():

    threading.Timer(3, skipAdFunction).start()
    #skipAd = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/div[4]/div[2]/div[2]/div/div[4]/div/div/div[5]/button")
    try:
        waitForNext.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div/div[4]/div[2]/div[2]/div/div[4]/div/div/div[5]/button"))).click()
    except:
        pass
    

def clickNextFunction(): 
    #//*[@id='items']/ytd-compact-video-renderer[1]
    # //*[@id='contents']
    # //*[@id='contents']/ytd-compact-video-renderer
    #try:
       # nextElement = waitForNext.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='contents']/ytd-compact-video-renderer")))
                                        #style-scope ytd-compact-autoplay-renderer
    #    nextElement = waitForNext.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='items']/ytd-compact-autoplay-renderer[1]")))
    #    nextElement.click()

    #    if keepLooping:
    #        threading.Timer(6, clickNextFunction).start()
    #except:
    #    pass

    while keepLooping:
        try:
        #make the loop sleep for a random amount
            time.sleep(loopLength)
            print("nextVideo")
            #nextElement = waitForNext.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='items']/ytd-compact-autoplay-renderer")))
                                        #style-scope ytd-compact-autoplay-renderer
                                        #//*[@id='items']/ytd-compact-autoplay-renderer
            #nextElement = waitForNext.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='contents']/ytd-compact-video-renderer")))
            nextElement = waitForNext.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[12]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]")))
            nextElement.click()
            count += 1

            print(count)
        except:
            print("closing")
            driver.close()

#skipAdFunction()
clickNextFunction()