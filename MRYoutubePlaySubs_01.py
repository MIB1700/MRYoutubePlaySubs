#! /usr/local/bin/python3.8

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

#from selenium.webdriver.common.action_chains import ActionChains

import datetime
import getopt as go
import random
from sys import *
import string
import re
import time

#--------- VARS -------------
vid_title = ""
vid_duration = ""
date = ""
maxVids = 3;
count = 0
browser = "Safari"

# input of text file with youtube channel links
fname = ''
youtube = "https://www.youtube.com/channel/UCLJffad_3eSofXkBwAR8pKA/"

#----------- process argv --------
try:
    opts, args = go.getopt(argv[1:],'hl:n:b:', ['browser=', 'links=', 'numVids='])
except go.GetoptError:
     print(f'{argv[0]}: something went wrong with the arguments')
     exit(2)
for opt, arg in opts:
    if opt in  ('-b', '--browser'):
        browser = arg
    elif opt in ('-l', '--links'):
        fname = arg
    elif opt in ('-n','--numVids'):
        maxVids = int(arg)
    elif opt == '-h':
        print(f'{argv[0]} --browser [Safari (default), Chrome, Firefox, InternetExplorer, Opera]')

def CheckAndGoToURL(url):
    if url:
        if not url.startswith('https'):
            url = 'https://' + url
        if url.endswith('/') == False:
            url = url + '/'

        driver.get(url)
    else:
        exit(66)

def getDateString():
    date = datetime.datetime.now()
    return date.strftime("%x_%X")

def PlaySomething():
    #get the grid each time just in case someting goes wrong
    #TODO: add a try statement
    grid = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ytd-grid-video-renderer")))
    vidCount = len(grid)

    #make sure the maxVids count is equal or less than the total amount of videos available
    if vidCount <= maxVids:
        maxVids = vidCount
    
    if vidCount > 1:
        randVid = random.randint(0, vidCount)
        grid[randVid].click()

        vid_title, vid_duration = GetVidInfo()
        print(f"title: {vid_title}")
        print(f"duration: {vid_duration}")
    elif vidCount == 1:
    #if only one grid element, play that 
        grid[0].click()

        vid_title, vid_duration = GetVidInfo()
    else:
        print("no videos found... moving on to next channel")
        return

    secs = VidLength2Secs(vid_duration)
    time.sleep(secs)
    
def VidLength2Secs(vidLen):
    #check for how many ":"
    numSep = vidLen.count(":")

    #if time was in minutes
    if numSep == 1:
        #add the hours
        vidLen = "00:" + vidLen

    #convert hr:min:sec string to integer -> seconds
    lengthSecs = sum(x * int(t) for x, t in zip([3600, 60, 1], vidLen.split(":")))
    return lengthSecs

def GetVidInfo():
    vid_title = waitTitle.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
    vid_duration = waitDuration.until(EC.presence_of_element_located((By.XPATH, "//span[@class='ytp-time-duration']"))).text
    return vid_title, vid_duration

def OpenLinksFile():
    with open(fname, 'r') as rawfile:
        lines = rawfile.readlines()
    
    rawfile.close()
    return lines

def PickRandomLink(links):
    link = random.choice(links)
    #make sure the link ends with a '/'

    return link

#open a browser window
'''
# [Safari (default), Chrome, Firefox, InternetExplorer, Opera]')
if browser.upper() == "SAFARI":
elif browser.upper() == "CHROME":
elif browser.upper() == "FIREFOX":
elif browser.upper() == "IE":
'''
try:
    driver = webdriver.Safari()
        #maximize window
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)
    waitTitle = WebDriverWait(driver, 30)
    waitDuration = WebDriverWait(driver, 30)
    waitInfo = WebDriverWait(driver, 30)
except WebDriverException:
    print("argh....")
    exit(66)
#------------------------------------------------------

#------------------------------------------------------
#------------------------------------------------------

CheckAndGoToURL(youtube)

subButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='items']/ytd-mini-guide-entry-renderer[3]")))
subButton.click()
#------------------------------------------------------
driver.quit()

