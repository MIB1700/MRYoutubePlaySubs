#! /usr/local/bin/python3.8

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains

import datetime
import getopt
import random
from sys import argv
import string
import re
import time

try:
    opts, args = getopt.getopt(argv[1:],'h:', ['browser=', 'links=', 'numVids='])
except getopt.GetoptError:
     print(f'{argv[0]} -browser [Safari (default), Chrome, Firefox, InternetExplorer, Opera]')
     exit(2)
for opt, arg in opts:
    if opt == '--browser':
        loopMin = float(arg)
    elif opt == '-h':
        print(f'{argv[0]} -browser [Safari (default), Chrome, Firefox, InternetExplorer, Opera]')


youtube = "https://www.youtube.com/channel/UCLJffad_3eSofXkBwAR8pKA/"

vid_title = ""
vid_duration = ""
date = ""
maxVids = 3;
count = 0
browser = "Safari"

if len(argv) <= 1:
    print("\n------------------")
    print(f"{argv[0]} needs 1 argument: \na .txt file with FULL links to youtube channels on each line")
    print("optional 2nd argument: number of videos to play on each channel (default: 1) - \n will check if that many vids are available and truncate if necessary")
    print("------------------\n")
    exit(66)

# input of text file with youtube channel links
fname = argv[1]

if len(argv) == 2:
    maxVids = argv[2]

def CheckAndGoToURL(url):
    if url:
        if not url.startswith('https'):
            url = 'https://' + url
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
    return random.choice(links)

lines = OpenLinksFile()
link = PickRandomLink(lines)
CheckAndGoToURL(link)


#open a Safari window
#driver = webdriver.Safari()
#maximize window
#driver.maximize_window()
#wait = WebDriverWait(driver, 30)
#waitTitle = WebDriverWait(driver, 30)
#waitDuration = WebDriverWait(driver, 30)
#waitInfo = WebDriverWait(driver, 30)

#CheckAndGoToURL(youtube + "videos")
#PlaySomething()
#driver.back()


#driver.close()