import pyautogui
from comtypes.GUID import GUID
import pyfirmata
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from serial.serialutil import SerialException

try:
    board = pyfirmata.Arduino('COM4')
    it = pyfirmata.util.Iterator(board)
    it.start()
except SerialException:
    print("Error 10, Serial can't open")
    input()
    exit()
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.GetMute()
    volume.GetMasterVolumeLevel()
    volume.GetVolumeRange()
except:
    print("Error 30, Win Volume can't initialize")
#print("volume.GetMasterVolume(): %s" % volume.GetMasterVolumeLevel())
#volume.SetMasterVolumeLevel(0.6, None)
#print("volume.GetMasterVolume(): %s" % volume.GetMasterVolumeLevel())
#volume.SetMasterVolumeLevel(.10, None)
analog_input = board.get_pin('a:0:i')
but1 = board.get_pin("d:2:i")
but2 = board.get_pin("d:7:i")
print(volume.GetChannelCount())
x = 0
pyautogui.FAILSAFE = False

import requests
import time

from pprint import pprint
import serial
import time

#s = serial.Serial("COM4", 9600) #port is 11 (for COM12, and baud rate is 9600
time.sleep(2)    #wait for the Serial to initialize

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/'
ACCESS_TOKEN = 'BQCS6V6WFG0rM4PRq976SdbLK-KOX9geRhmdAcowKFKyL_E83NIOlhbhAA4dw4N9TrC8bu9zi_86Rbdw91YOipZ0KXlex4-WUxbqtdM7r_NENfmKz7_sY2m8c5Xo1CixU0UHzHZ1W7HRao1Yw6LW1vSF-0eZan2pQaE37Ks0iud18305jyRSsUrIACB9bL30_wVdJbooPEuiPeUkqWOOVT4g4oQHMjzVFiHhJ0fO2LGhYO5SSbPov3YvqQuwsr_IaBkUX5vBM2ESiGmwBgWJEF0'

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
        print(track_id)
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
        current_track_info = {"id": "Error", "track_name": "Error", "artists": "Error", "link": "Error"}
        return current_track_info
current_track_id = None
while True:
    #Reads potentiometer value, and assigns it
    analog_value = analog_input.read()

    #Plays or pauses if a button is pressed
    if analog_value != None:
        if but1.read() == True:
            pyautogui.press("playpause")
            time.sleep(.5)    

        #Detects if a long OR short press is performed
        elif but2.read() == True:
            time.sleep(.5)
            x += 1
        #Skips to next/previous track when button 2 is released
        else:
            try:
                if x == 1:
                    pyautogui.press("nexttrack")
                    x = 0
                elif x == 2:
                    pyautogui.press("prevtrack")
                    x = 0
            except:
                print("Error 40: Can't press play/skip")

            #
            try:
                volume.SetMasterVolumeLevel(analog_value * -36, None)
            except:
                print("Error 31: Can't set volume")
        print(f"Volume: {round((1 - analog_value)*100)}% Button 1: ", but1.read(), "Button 2: ", but2.read())

        current_track_info = get_current_track(ACCESS_TOKEN)
     
        
        if current_track_info['id'] != current_track_id:
        
              
        
             pprint(current_track_info, indent=4,)
        
             current_track_id = current_track_info['id']
        
                 
        
        #     str = current_track_info["track_name"]
        #
        #     str = str.strip()
        #
        #     str = str.encode()
        #
        #      
        #
        #     #s.write(str)
        #
        #     #time.sleep(6)
        #
        #     str = current_track_info["artists"]
        #
        #     str = str.strip()
        #
        #     str = str.encode()
        #
        #     #s.write(str)
        #
        #     #time.sleep(6)
        #
        #     str = current_track_info["track_name"]
        #
        #     str = str.strip()
        #
        #     str = str.encode()


        
        #     #s.write(str)
        #
        #     #time.sleep(6)
        #
        #     str = current_track_info["artists"]
        #
        #     str = str.strip()
        #
        #     str = str.encode()
        #
        #     #s.write(str)
        #
        #     #time.sleep(6)
        #
        #     str = current_track_info["track_name"]
        #
        #     str = str.strip()
        #
        #     str = str.encode()

            #s.write(str)