import openweather

# Takes lat (str), lon (str) and API key (str) to download
#   precip (chance of rain, %), lightning forecast and UV Index. 
# Returns precip (str; e.g. "10"), lightning (str: "Y" or "N") and UVI (float).
#
def getOwmData(lat, lon, apiKey):
    weatherData = openweather.getLatLonWeather(lat, lon, apiKey,
                                               exclude="minutely,daily,alerts")
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
    return (str(precip), lightning, uvi)

# Takes UVI (int) and its corresponding exposure category (str) 
#
def uviCondition(uvi):
    if uvi<=2:
        condition = "Low"
    elif 3<=uvi<=5:
        condition = "Moderate"
    elif 6<=uvi<=7:
        condition = "High"
    elif 8<=uvi<=10:
        condition  = "Very High"
    else:
        condition = "Extreme"
        
    return condition

