import badger2040
from utils import displayEnvInfo, displayWbgtSuggestions

LAT = 42.0
LON = -71.0
OWM_API_KEY = ""

DEEP_SLEEP_INTERVAL = 10 # in minutes 
LED_BRIGHTNESS = 128 # [0,256]

display = badger2040.Badger2040()
display.led(LED_BRIGHTNESS)

if badger2040.pressed_to_wake(badger2040.BUTTON_DOWN):
    displayWbgtSuggestions(display)
elif badger2040.pressed_to_wake(badger2040.BUTTON_UP):
    displayEnvInfo(display, LAT, LON, OWM_API_KEY, useWifi=False)
else:
    displayEnvInfo(display, LAT, LON, OWM_API_KEY)

while True:
    if display.pressed(badger2040.BUTTON_DOWN):
        displayWbgtSuggestions(display)
    elif display.pressed(badger2040.BUTTON_UP):
        displayEnvInfo(display, LAT, LON, OWM_API_KEY, useWifi=False)
    
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)
        # Set an RTC alert that will fire in DEEP_SLEEP_INTERVAL mins. 
        # Shut off power supply if the device is on battery.
        # Blocks until a button event or an RTC alert if the device is on USB power.
    