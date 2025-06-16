import badger2040
from badger2040 import WIDTH, HEIGHT
from unoaa_wbgt import downloadWbgt
import openweather

WHITE = 15
BLACK = 0

wbgt = 0
condition = "a"
rainPercent = "20%"
lightningPercent = "20%"
UVI = "4"

# Takes lat and lon in string
# Returns date (str), time (str) and wbgt forecast (int).
#
def getWbgt(lat, lon):
    timeStamp, wbgt = downloadWbgt(lat, lon)
    # timeStamp: UTC in the ISO format: YYYY-MM-DDTHH:mm:ss.SSSZ
    date = timeStamp.split("T")[0][5:]
    time = timeStamp.split("T")[1][:5]
    hr = int(time[:2])
    
    # UTC to EST conversion
    if hr <= 12:
        if hr-4<=0:
            time = time.replace(str(hr), str(hr+8), 1) + " PM"
        else:
            time = time.replace(str(hr),str(hr-4),1) + " AM"
    else:
        if hr-4 < 12:
            time = time.replace(str(hr), str(hr-4),1) + " AM"
        elif hr-4 == 12:
            time = time.replace(str(hr),str(12),1) + " PM"
        else:
            time = time.replace(str(hr), str(hr-16), 1) + " PM"
        
    return (date, time, int(wbgt))

# Takes WBGT (int) and its corresponding alert condition
#
def wbgtCondition(wbgt):
    if wbgt <= 76:
        condition = "Good"
    elif 76.1 <= wbgt <= 81:
        condition = "Cautious"
    elif 81.1 <= wbgt <=84:
        condition = "Risky"
    elif 84.1 <= wbgt <=86:
        condition = "High Risk"
    else:
        condition = "Extreme"
    return condition

def getOwmData(lat, lon, apiKey):
    weatherData = openweather.getLatLonWeather(lat, lon, apiKey, exclude="minutely,daily,alerts")
    # Chance of rain (%)
    precip = openweather.getProbPrecipNextHr(weatherData)
    precip = int(precip*100)
    # Lightning
    _, condMain, _, _ = openweather.getWeatherConditionNextHr(weatherData)
    if condMain == "Thunderstorm":
        lightning = "Y"
    else:
        lightning = "N"
    # UVI
    uvi = openweather.getCurrentUvi(weatherData)
    uvi = round(uvi, 1)
    return (str(precip), lightning, str(uvi))    

def displayEnvInfo(display, lat, lon, apiKey, useWifi=True):
    if useWifi:
        # Connects to the wireless network. Make sure to complete WIFI_CONFIG.py.
        display.connect()
        
        try:
            date, time, wbgt = getWbgt(lat, lon)
        except RuntimeError:
            date = "00-00"
            time = "00:00"
            wbgt = "0"
            
        try:
            precip, lightning, uvi = getOwmData(lat, lon, apiKey)
        except RuntimeError:
            precip = "--"
            lightning = "--"
            uvi = "--"

        with open("envcond.txt", "w") as f:
            f.write(date + "\n" + time + "\n" + str(wbgt) + "\n" +\
                    precip + "\n" + lightning + "\n" + uvi)
    else:
        try:
            with open("envcond.txt") as f:
                date = f.readline()
                time = f.readline()
                wbgt = int(f.readline())
                precip = f.readline()
                lightning = f.readline()
                uvi = f.readline()
        except OSError:
            date = "00-00"
            time = "00:00"
            wbgt = 0
            precip = 0
            lightning = "N"
            uvi = 0

    # Clear to white
    display.set_pen(WHITE)
    display.clear()
    display.set_font("bitmap8")
    
    # upper black rectangle
    display.set_pen(BLACK)
    upperRecHeight = int(HEIGHT/6)
    display.rectangle(0, 0, WIDTH, upperRecHeight)
    # date, time, "WBGT"
    display.set_pen(WHITE)
    display.text("WBGT", 5, 5, scale=2)
    display.text(date, int(WIDTH*2/5), 5, scale=2)
    display.text(time, int(WIDTH-display.measure_text(time)-5), 5, scale=2)
    # wbgt number
    display.set_pen(BLACK)
    display.text(str(wbgt), 5, upperRecHeight+10, scale=8)
    # WGBT condition
    condition = wbgtCondition(wbgt)
    display.text(condition, 7, int(HEIGHT*4/5), scale=3)
    # precip
    display.text("Rain: "+precip+"%", int(WIDTH/3), upperRecHeight+10, scale=3)
    # lightning
    display.text("Lightning: "+lightning, int(WIDTH/3), upperRecHeight+43, scale=3)
    # UVI
    display.text("UVI: "+uvi, int(WIDTH/3), upperRecHeight+80, scale=3)
    
    display.update()

# Displays activity adjustment suggestions according to the current
# heat alert condition.
#
def displayWbgtSuggestions(display):
    # Clear to white
    condition = wbgtCondition(wbgt)
    display.set_pen(WHITE)
    display.clear()
    display.set_font("bitmap8")
    
    display.set_pen(BLACK)
    display.text(condition+":\n", 5, 5, wordwrap=int(WIDTH),scale=3)
    #"Normal Activites. At least 3 seperate 3-min breaks each hr."
    if condition=="Good":
        display.text("Normal Activites. At least 3 seperate 3-min breaks each hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="Fine":
        display.text("Use discreation for intese or long exercise. At least 3 seperate 4-min breaks each hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="Poor":
        display.text("Be alert. Max 2 hrs of practice. 4 seperate 4-min breaks each hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="High Risk":
        display.text("Be extremely cautious. Max 1 hr of practice. No conditioning activities. 20-min breaks distributes throughout the hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    else:
        display.text("No outdoor workouts. Delay practice/events until a cooler WBGT is reached.",
                     0, 39, wordwrap=WIDTH, scale=2)
    display.update()
