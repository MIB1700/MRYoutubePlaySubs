#! /usr/local/bin/python3.8
"""
    MRYoutubeFindNext.py
    
    Script to open a Chrome browser, go to Youtube and endlessly play videos
    for a random amount of time by always clicking on the "Up Next" video
    
    "Up Next" has to be visible on the screen for this to work!!!
    
    TODO: record screen and upload/stream video directly back to youtube
    
    Input: --tmin <inSecs>
           --tmax <inSecs>
           --bail <inSecs>
           --iterations <num vids after which to bail>
           --vid <string: everything after "www.youtube.com/">
           --fullvid <string: entire string of initial video>
           
            sets the random range of how long to wait before clicking to next video
            --bail sets the amount of time (in secs) before the loop is stopped and
                no new videos will be played
            --iterations, number of videos to click on before stopping
            
    To stop the script:
            either close the Chrome browser
            or ctrl + c (this will also quit the browser)
"""



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys, getopt
import random
import math
import datetime
import re

#set variables to default values
loopMin = 1
loopMax = 5
loopLength = 4
totalTime = 0
keepLooping = True

#time before the loop gets broken
#later on this could be used to make sure that the streaming size doesn't get to long
#by default infinity...
bailTime = math.inf

initial = True
vidString = ""
youtube = "http://www.youtube.com/"
fullVid = ""

vidAll = ""
date = ""
count = 0
iterations = math.inf

def getDateString():
    date = datetime.datetime.now()
    return date.strftime("%x_%X")

#get arguments from terminal
#use: --tmin and --tmax to set the random range between videos
try:
    opts, args = getopt.getopt(sys.argv[1:],'h:', ['tmin=', 'tmax=', 'bail=', 'vid=', 'fullvid=', 'iterations='])
except getopt.GetoptError:
    print('MRYoutubeFindNext.py -tmin <timeInSecs> -tmax <timeInSecs>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '--tmin':
        loopMin = float(arg)
    elif opt == '--tmax':
        loopMax = float(arg)
    elif opt == '--bail':
        bailTime = int(arg)
        print("bailTime = ", bailTime)
    elif opt =='--vid':
        initial = False
        vidString = arg
    elif opt =='--fullvid':
        initial = 3
        fullVid = arg
    elif opt =='--iterations':
        iterations = int(arg)
    elif opt == '-h':
        print('MRYoutubeFindNext.py -tmin <timeInSecs> -tmax <timeInSecs>')

def WriteInfoToFile(vidLink = youtube):
    # use first vid name as fileName
    # write all vid info from VidInfo() here
    # add length of vid played
    
    #get video title, plays, likes, and dislikes
    with wait_for_page_load(driver):
        vidAll = driver.find_element_by_css_selector("ytd-video-primary-info-renderer").text.split('\n')
    #vidAll = driver.find_element_by_xpath("//*[@id='info-contents']")
    
    fileName = re.sub('\|\.|\!|\/|\;|\:', '_', vidLink + date)
    textFile = open(fileName + ".txt", "a+")
    strLen = len(vidAll)
    print(vidAll)

    if strLen > 6:
        print("length = ", strLen)
        offset = 0
        
        text = "Interation: " + str(count)
        textFile.write(text)
        textFile.write("\n")
        
        if strLen == 7:
            offset = 1
            textFile.write(vidAll[0])
            textFile.write("\n")
        
        textFile.write("Video Name: ")
        textFile.write("\n")
        textFile.write(vidAll[0 + offset])
        textFile.write("\n")
        
        textFile.write("Video Plays: ")
        textFile.write("\n")
        textFile.write(vidAll[1 + offset])
        textFile.write("\n")
        
        textFile.write("Video Likes: ")
        textFile.write("\n")
        textFile.write(vidAll[2 + offset])
        textFile.write("\n")

        textFile.write("Video Dislikes: ")
        textFile.write("\n")
        textFile.write(vidAll[3 + offset])
        textFile.write("\n")

        textFile.write("Played for " + str(loopLength) + " secs")
        textFile.write("\n\n\n")

        textFile.close()

#helper function to check if the new page has loaded yet
class wait_for_page_load(object):
    
    def __init__(self, browser):
        self.browser = browser
    
    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')
    
    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id
    
    def __exit__(self, *_):
        wait_for_page_load(self.page_has_loaded)


date = getDateString()

#open a Safari window
driver = webdriver.Safari()

#load Youtube
#default (i.e. no argument) youtube home page
if initial == True:
    driver.get(youtube)
    
#once youtube is loaded, click on the first recommended video
    with wait_for_page_load(driver):
        firstclick = driver.find_element_by_xpath("//*[@id='items']/ytd-grid-video-renderer[1]")
        firstclick.click()

elif initial == False:
    #plays the video at the given link (string after "youtube.com/")
    fullVid = youtube + vidString
    driver.get(fullVid)

elif initial == 3:
    #full youtube link to vid
    driver.get(fullVid)

#make sure the first video plays before we enter the loop
loopLength = round(random.uniform(loopMin, loopMax), 3)
print("next in = ", loopLength, "secs")
time.sleep(loopLength)

count += 1
WriteInfoToFile()


#sys.exit(2)

#until we quit the program in terminal do:
while keepLooping:
    
    with wait_for_page_load(driver):
        
        #find the "up next" element on the screen
        # upnext = driver.find_element_by_xpath("//*[@id='contents']/ytd-compact-video-renderer")
        upnext = driver.find_element_by_xpath("//*[@id='items']/ytd-compact-autoplay-renderer")
        upnext.click()

        #print out some stuff...
        totalTime += round(loopLength, 3)
        print("")
        print("")
        print("-------------------------------")
        print("TOTAL TIME = ", totalTime)
        print("-------------------------------")
        print("")
        
        #get a new length before clicking on vid
        loopLength = round(random.uniform(loopMin, loopMax),3)
        
        print("next in = ", loopLength, "secs")
        
        #make the loop sleep for a random amount
        time.sleep(loopLength)
        
        #get info on vid
        count += 1
        print("")
        print("current count = ", count)
        print("")
        
        WriteInfoToFile()

        if totalTime > bailTime:
            keepLooping = False
            driver.close()

        if count >= iterations:
            keepLooping = False
            driver.close()



#need to close file after done writing to it!


#things TO DO:
#   somehow record the screen
#   upload the recording to youtube
#       either after rec is done
#       OR streaming directly to youtube

"""
youtube community guidlines
what is the "objective" meaning of the piece?

"""
