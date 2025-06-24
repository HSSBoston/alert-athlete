import badger2040, noaa, weather
from badger2040 import WIDTH, HEIGHT

ENV_COND_FILE_NAME = "envcond.txt"
WHITE = 15
BLACK = 0

# Takes environmental conditions and a file name, and write 
#   those conditions to the file
#
def writeEnvCond(date, time, wbgt, precip, lightning, uvi, fileName):
    with open(fileName, "w") as f:
        lines = date      + "\n" +\
                time      + "\n" +\
                str(wbgt) + "\n" +\
                precip    + "\n" +\
                lightning + "\n" +\
                str(uvi)
        f.write(lines)

# Takes a file name, and reads environmental conditions from the file.
# Returns date (str), time (str), wbgt (int), precip (str),
#   lightning (str) and uvi (float)
#
def readEnvCond(fileName):
    try:
        with open(fileName) as f:
            date      = f.readline().strip()
            time      = f.readline().strip()
            wbgt      = int(f.readline().strip())
            precip    = f.readline().strip()
            lightning = f.readline().strip()
            uvi       = float(f.readline().strip())
    except OSError:
        date      = "00-00"
        time      = "00:00"
        wbgt      = 0
        precip    = "--"
        lightning = "--"
        uvi       = -1
    return(date, time, wbgt, precip, lightning, uvi)

def displayEnvInfo(display, lat, lon, apiKey, useWifi=True):
    if useWifi:
        # Connects to the wireless network. Make sure to complete WIFI_CONFIG.py.
        display.connect()
        
        try:
            date, time, wbgt = noaa.getWbgt(lat, lon)
        except RuntimeError:
            date = "00-00"
            time = "00:00"
            wbgt = 0
        try:
            precip, lightning, uvi = weather.getOwmData(lat, lon, apiKey)
        except RuntimeError:
            precip    = "--"
            lightning = "--"
            uvi       = -1
        writeEnvCond(date, time, wbgt, precip, lightning, uvi, ENV_COND_FILE_NAME)
    else:
        date, time, wbgt, precip, lightning, uvi = readEnvCond(ENV_COND_FILE_NAME)
    
    print(date, time, wbgt, precip, lightning, uvi)
    
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
    display.text(str(wbgt), 1, upperRecHeight+10, scale=8)
    # WGBT condition
    wCondition = noaa.wbgtCondition(wbgt)
    display.text(wCondition, 1, int(HEIGHT*4/5), scale=3)
    # precip
    display.text("Rain: "+precip+"%", int(WIDTH*2/5+13), upperRecHeight+10, scale=3)
    # lightning
    display.text("Lightning: "+lightning, int(WIDTH*2/5+13), upperRecHeight+43, scale=3)
    # UVI
    display.text("UVI: "+str(uvi), int(WIDTH*2/5+13), upperRecHeight+80, scale=3)
    
    display.update()

# Displays activity adjustment suggestions according to the current
# heat alert condition.
#
def displayWbgtSuggestions(display):
    date, time, wbgt, precip, lightning, uvi = readEnvCond(ENV_COND_FILE_NAME)
    condition = noaa.wbgtCondition(wbgt)
    
    # Clear to white
    display.set_pen(WHITE)
    display.clear()
    display.set_font("bitmap8")
    
    display.set_pen(BLACK)
    display.text(condition+":\n", 5, 5, wordwrap=int(WIDTH),scale=3)
    #"Normal Activites. At least 3 seperate 3-min breaks each hr."
    if condition=="Good":
        display.text("Normal Activites. At least 3 seperate 3-min breaks each hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="Cautious":
        display.text("Use discreation for intese or long exercise. At least 3 seperate 4-min breaks each hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="Risky":
        display.text("Be alert. Max 2 hrs of practice. 4 seperate 4-min breaks each hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="High Risk":
        display.text("Be extremely cautious. Max 1 hr of practice. No conditioning activities. 20-min breaks distributes throughout the hr.",
                     0, 39, wordwrap=WIDTH, scale=2)
    else:
        display.text("No outdoor workouts. Delay practice/events until a cooler WBGT is reached.",
                     0, 39, wordwrap=WIDTH, scale=2)
    display.update()

def displayUviSuggestions(display):
    date, time, wbgt, precip, lightning, uvi = readEnvCond(ENV_COND_FILE_NAME)
    condition = weather.uviCondition(uvi)
    
    # Clear to white
    display.set_pen(WHITE)
    display.clear()
    display.set_font("bitmap8")
    
    display.set_pen(BLACK)
    display.text(condition+":\n", 5, 5, wordwrap=int(WIDTH),scale=3)

    if condition=="Low":
        display.text("You can safely enoy being outside. Wear sunglasses on bright days. If you burn easily, cover up and use sunscreen SPF 15+.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="Moderate":
        display.text("Take precations such as wearing a hat and sunglasses and using sunscreen SPF 30+. Seek shade during midday hours.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="High":
        display.text("Protection against sun damage is needed. Wear a hat, sunglasses, and long pants. Use sunscreen SPF 30+ and seek shade during midday hours.",
                     0, 39, wordwrap=WIDTH, scale=2)
    elif condition=="Risky":
        display.text("Protection against sun damage is needed. Opt to be outside between 10 AM and 4 PM. A shirt, hat and sunscreen are a must. Be sure to seek shade.",
                     0, 39, wordwrap=WIDTH, scale=2)
    else:
        display.text("Protection against sun damage is needed. Opt to be outside between 10 AM and 4 PM. A shirt, hat and sunscreen are a must. Be sure to seek shade.",
                     0, 39, wordwrap=WIDTH, scale=2)

    display.update()
