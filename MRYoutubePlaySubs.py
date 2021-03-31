"""
    MRYoutubePlaySubs.py
    Script to open a browser and play videos of given channels

    Needed: text file with links to channels
    
    Input: -l or --links <textfile>
           -n or --numVids <int>
           -g or --graceTime <int/float>
            
    To stop the script:
            either close the  browser
            or ctrl + c (this will also quit the browser)
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support.expected_conditions import staleness_of
from contextlib import contextmanager

import datetime
import getopt as go
import random
import sys
import string
import re
import time

#--------- VARS -------------
date = ""
maxVids = 3
count = 0
totalTime = 0
browser = "Safari"
bailOnChannel = False
running = True
graceTime = 2
# input of text file with youtube channel links
fname = ''
youtube = "https://www.youtube.com/channel/UCLJffad_3eSofXkBwAR8pKA/"

#----------- process argv --------
try:
    opts, args = go.getopt(sys.argv[1:],'hl:n:b:g:', ['browser=', 'links=', 'numVids=', 'graceTime='])
except go.GetoptError:
     print(f'{sys.argv[0]}: something went wrong with the arguments')
     print('needs 2 arguments:')
     print('1) -l or --links: path to a textfile containing links to the channels')
     print('2) -n or --numVids: number of videos to play from each channel before moving on to the next (default 3)')
     print('3) (optional) -g or --graceTime: extra time after channel load to allow information to be downloaded (default 2)')
     print()
     print('use the -h flag to see usage examples...')
     exit(2)
for opt, arg in opts:
    if opt in  ('-b', '--browser'):
        browser = arg
        print(f"--browser: {browser}")
    elif opt in ('-l', '--links'):
        fname = arg
        print(f"--links: {fname}")
    elif opt in ('-n','--numVids'):
        maxVids = int(arg)
        print(f"--numVids: {maxVids}")
    elif opt in ('-g','--graceTime'):
        graceTime = float(arg)
        print(f"--graceTime: {graceTime}")
    elif opt == '-h':
        print(f'{sys.argv[0]}: needs 2 arguments:')
        print('1) -l or --links: path to a textfile containing links to the channels')
        print('2) -n or --numVids: number of videos to play from each channel before moving on to the next (default 3)')
        print('3) (optional) -g or --graceTime: extra time after channel load to allow information to be downloaded (default 2)')
        print('usage example')
        print()
        print('MRYoutubePlaySubs.py -l TextfileWithLinks.txt -n 2')
        print()
        print('or')
        print()
        print('MRYoutubePlaySubs.py --links TextfileWithLinks.txt --numVids 10 -g 1')
        exit(3)

def CheckURL(url, addStr):
    if url:
        #remove trailing/leading whitespaces... just in case
        url = url.strip()
        #add "s" to http
        if url.startswith('http://'):
            url = url.replace('http://', 'https://')
        #add https if not present
        elif url.startswith('www.'):
            url = 'https://' + url
        #make sure it ends in a slash -> so we can append a string later
        if not url.endswith('/'):
            url = url + '/'

        if not url.startswith('http'):
            print(f"the url: {url} is formatted incorrectly. Check your textfile.")
            print("make sure there are no empty lines")
            exit(1)
        #add requested string
        finalLink = url + addStr

        print(f"finalLink: {finalLink}")
        return finalLink
    else:
        print("link building went wrong...")
        print(f"the url: {url} is formatted incorrectly. Check your textfile.")
        print("make sure there are no empty lines")
        exit(1)

def getDateString():
    date = datetime.datetime.now()
    return date.strftime("%x_%X")

def WriteInfoToFile(url, vidInfo, totalTime):
    # vidInfo[time, title, views, upload date]

    fileName = re.sub(r"\|.|!|/|;|:", "_", url)
    fileName = fileName + "_" + getDateString()
    
    textFile = open(fileName + ".txt", "a+")
        

    text = "Iteration: " + str(count)
    textFile.write(text)
    textFile.write("\n")
    
    textFile.write("Video Name: ")
    textFile.write("\n")
    textFile.write(vidInfo[1])
    textFile.write("\n")
    
    textFile.write("Video Plays: ")
    textFile.write("\n")
    textFile.write(vidInfo[2])
    textFile.write("\n")
    
    textFile.write("Video Likes: ")
    textFile.write("\n")
    textFile.write(vidInfo[3])
    textFile.write("\n")

    textFile.write("Video Dislikes: ")
    textFile.write("\n")
    textFile.write(vidInfo[3])
    textFile.write("\n")

    textFile.write("Played for " + str(totalTime) + " secs")
    textFile.write("\n\n\n")

    textFile.close()
        

def PlaySomething(driver, wait, link):
    
    global maxVids
    global totalTime
    global bailOnChannel

    try:
        grid = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ytd-grid-video-renderer")))
        vidCount = len(grid)
        print(f"num Vids on page: {vidCount}")
        #make sure the maxVids count is equal or less than the total amount of videos available
        # //*[@id="container"]
        #//*[@id="subscriber-count"]
        # //*[@id="container"]
        # //*[@id="contentContainer"]
#        test = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='contentContainer']")))

        if vidCount <= maxVids:
            maxVids = vidCount
        
        if vidCount >= 1:
            randVid = random.randint(0, vidCount-1)
            print(f"randVid: {randVid}")

            #get a random vid from the grid
            curVid = grid[randVid]

            #extract info from the choosen vid
            info = GetVidInfo(curVid.text)

            #click on the vid and play it
            curVid.click()
        
            print(f"title: {info[1]}")
            print(f"duration: {info[0]}")
        
            secs = VidLength2Secs(info[1])
            #global totalTime
            totalTime += secs
            print(f"total time: {totalTime}")

            WriteInfoToFile(link, info, totalTime)

            bailOnChannel = False
            time.sleep(secs)
    except TimeoutException:
        print("no videos found on profile...")
        bailOnChannel = True
        pass
    except:
        print("something else happened :(")
        exit(66)
    
def VidLength2Secs(vidLen):
    #check for how many ":"
    try:
        numSep = vidLen.count(":")
         #if time was in minutes
        if numSep == 1:
            #add the hours
            vidLen = "00:" + vidLen

        #convert hr:min:sec string to integer -> seconds
        lengthSecs = sum(x * int(t) for x, t in zip([3600, 60, 1], vidLen.split(":")))
        return lengthSecs
    except:
        return 20

def GetVidInfo(info):
    splitting = [name.strip() for name in info.splitlines()]
    splitting2 = [i for i in splitting if i] 
    del splitting2[1]
    # [time, title, views, upload date]
    return splitting2

def OpenLinksFile(file):
    try:
        with open(file, 'r') as rawfile:
            lines = rawfile.readlines()
    finally:
        SneakyInsertion(lines)
        rawfile.close()
    return lines

def SneakyInsertion(lines):
     #sneakily insert my own channel a couple of times into your mix of things ;)
    origLen = len(lines)
    maxInsert = 3
    if origLen >= 10:
        maxInsert = int(round(origLen * 0.15))

    for _ in range(3):
        ind = random.randint(0, maxInsert)
        lines.insert(ind, youtube)

def PickRandomLink(links):
    link = random.choice(links)
    #make sure the link ends with a '/'
    return link
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
def main():
    try:
        global running
        global bailOnChannel
         #open a browser window
        #here you could switch to a different browser type like Chrome or Firefox
        driver = webdriver.Safari()
        #maybe should be implemented to be able to switch browsers?
        '''
        # [Safari (default), Chrome, Firefox, InternetExplorer, Opera]')
        if browser.upper() == "SAFARI":
        elif browser.upper() == "CHROME":
        elif browser.upper() == "FIREFOX":
        elif browser.upper() == "IE":
        '''
        #maximize window
        driver.maximize_window()
        size = driver.get_window_size()
        #make it REALLY long so more videos can load and used
        driver.set_window_size(size['width'], size['height'] * 4)
        
        #setup wait.until functions
        wait = WebDriverWait(driver, 10)

        #read in the text file and store all the links
        #in lines variable
        lines = OpenLinksFile(fname)

        #this will paly indefinitly or until something breaks
        #quit with ctr+d or by closing the browser
  
        while running:
            #pick a random link
            link = PickRandomLink(lines)

            #check the link is formatted properly 
            curLink = CheckURL(link, "videos")
    
            #pick a random video on the page and play it
            #when video is done, go back to all videos
            #and pick another random one 
            for _ in range(maxVids):
                
                #.get opens the link and waits until the page loads
                driver.get(curLink)
                #however, since we are trying to get some information of the video
                # (duration and title) this doesn't seem to load as quickly
                #the graceTime waits (2secs by default) to make sure that the info is there
                #increase if needed..
                time.sleep(graceTime)

                PlaySomething(driver, wait, curLink)                

                #bail if there aren't videos on the page
                if bailOnChannel:
                    break
    except SessionNotCreatedException:
        print("Chances are your Safari still has a tab open \nthat is/was in automation mode!!")
        print("CLOSE IT!!! and run the script again...")
        exit(1)
    except KeyboardInterrupt:
        raise
    except:
        print("----------------------------")
        print("----------------------------")
        print("program quit with ctr+c... closing browser and quitting!!!")
        print("----------------------------")
        print("----------------------------")
        running = False
        bailOnChannel = True
        driver.quit()
        exit(66)
    
    
#------------------------------------------------------
#------------------------------------------------------


if __name__ == "__main__":
    #run the program...
    main()
