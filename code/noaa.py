from noaa_wbgt import downloadWbgt


# Takes lat (str) and lon (str) to download WBGT data from NOAA
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

# Takes WBGT (int) and its corresponding alert condition (str)
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

