import badger2040
from machine import Pin
from utils import displayEnvInfo, displayWbgtSuggestions, displayUviSuggestions

LAT = 42.0
LON = -71.0
WEATHER_API_KEY = ""

DEEP_SLEEP_INTERVAL = 5   # in minutes 
LED_BRIGHTNESS      = 128 # [0,255]

display = badger2040.Badger2040()
display.led(LED_BRIGHTNESS)

# If Button A pressed on battery
if badger2040.pressed_to_wake(badger2040.BUTTON_A):
    displayWbgtSuggestions(display)
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)
# If Button C pressed on battery
elif badger2040.pressed_to_wake(badger2040.BUTTON_C):
    displayUviSuggestions(display)
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)
# If Button Up or Down pressed on battery
elif badger2040.pressed_to_wake(badger2040.BUTTON_UP) or \
     badger2040.pressed_to_wake(badger2040.BUTTON_DOWN):
    displayEnvInfo(display, LAT, LON, WEATHER_API_KEY, useWifi=False)
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)
# If Button B pressed on battery
elif badger2040.pressed_to_wake(badger2040.BUTTON_B):
    displayEnvInfo(display, LAT, LON, WEATHER_API_KEY)
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)

while True:
    print("Currently powered by USB")
    if display.pressed(badger2040.BUTTON_A):
        displayWbgtSuggestions(display)
    elif display.pressed(badger2040.BUTTON_B):
        displayEnvInfo(display, LAT, LON, WEATHER_API_KEY)
    elif display.pressed(badger2040.BUTTON_C):
        displayUviSuggestions(display)        
    elif display.pressed(badger2040.BUTTON_UP) or display.pressed(badger2040.BUTTON_DOWN):
        displayEnvInfo(display, LAT, LON, WEATHER_API_KEY, useWifi=False)
    else:
        displayEnvInfo(display, LAT, LON, WEATHER_API_KEY)
    
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)
        # Set an RTC alert that will fire in DEEP_SLEEP_INTERVAL mins. 
        # Shut off power supply if the device is on battery.
        # Blocks until a button event or an RTC alert if the device is on USB power.
    