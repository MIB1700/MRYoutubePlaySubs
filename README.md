# MRyouTubeFindNext

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
