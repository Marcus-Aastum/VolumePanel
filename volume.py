import pyautogui
from comtypes.GUID import GUID
import pyfirmata
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from serial.serialutil import SerialException

#Initialize Windows Audio utility
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.GetMute()
    volume.GetMasterVolumeLevel()
    volume.GetVolumeRange()
except:
    print("Error 30, Win Volume can't initialize")

x = 0

#Disable pyautogui's automatic deactivation when mouse is in a corner
pyautogui.FAILSAFE = False

import requests
import time

from pprint import pprint
import serial
import time

#Start the serial connection
s = serial.Serial("COM4", 115200) 
time.sleep(2)    #wait for the Serial to initialize

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/'
ACCESS_TOKEN = input("Input your Spotify OAuth token:\n")

#Getting song and artist info
def get_current_track(ACCESS_TOKEN):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )
    try:
        json_resp = response.json()

        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]

        link = json_resp['item']['external_urls']['spotify']

        artist_names = ', '.join([artist['name'] for artist in artists])

        current_track_info = {
        	"id": track_id,
        	"track_name": track_name,
        	"artists": artist_names,
        	"link": link
        }
        return current_track_info
    except:
        current_track_info = {"id": "Error", "track_name": "_", "artists": "_", "link": "Error"}
        return current_track_info
#Declaring variables to be used
current_track_id = None
starttime = time.time()
startit = False
timeout = time.time()

while True:
        #Request new token after the previous has run out
        if time.time() - timeout > 3600:
            ACCESS_TOKEN = input("Input your Spotify OAuth token:\n")
            timeout = time.time()
        #Reads data from arduino, and assigns it to variables
        everysplit = s.readline().decode("utf-8")
        play = everysplit[0]
        skip = everysplit[1]
        vol = everysplit[2:-1]

        #Debugprint:
        #print(f"Playstate: {play} Skipstate: {skip} Volume: {vol}")

        #Plays or pauses if a button is pressed
        if vol != None:
            if play == "1":
                pyautogui.press("playpause")
                time.sleep(.5)    

            #Detects if a long OR short press is performed
            elif skip == "1":
                time.sleep(.2)
                x += 1
            #Skips to next/previous track when button 2 is released
            else:
                try:
                    if x == 1:
                        pyautogui.press("nexttrack")
                        x = 0
                    elif x >= 2:
                        pyautogui.press("prevtrack")
                        x = 0
                    else:
                        x = 0
                except:
                    print("Error 40: Can't press play/skip")

                #Sets volume
                try:
                    volume.SetMasterVolumeLevel((int(vol)/1023) * -36, None)
                except:
                    print("Error 31: Can't set volume")

        #Reading playback data
        current_track_info = get_current_track(ACCESS_TOKEN)

        #Starts a timer if the last timer has elapsed             
        if startit == True:            
            starttime = time.time()
            startit = False

        #Writes the songname or artist
        
        str = current_track_info["track_name"]
        str = str.strip()
        str = str.encode()
        s.write(str)
        str = "\1"
        str=str.strip()
        str=str.encode()
        s.write(str)
    
        str = current_track_info["artists"]
        str = str.strip()
        str = str.encode()
        s.write(str)
        str = "\0"
        str=str.strip()
        str=str.encode()
        s.write(str)