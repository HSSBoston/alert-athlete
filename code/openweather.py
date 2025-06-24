# Library to use OpenWeatherMap One Call API 3.0
# June 16, 2025 v0.01
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/
#
# OpenWeather's One Call API 3.0:
#   https://openweathermap.org/api/one-call-3
# As for weather conditions ("id", "main", "description" and "icon"), see:
#   https://openweathermap.org/weather-conditions

import badger2040, urequests, json, openweather_extractors

# Takes lat (str), lon (str), API key (str) to call OpenWeather's API
# Returns JSON weather data (dict)
#   Optional inputs: unit
#     "imperial", "metric" or "standard"
#   Optional inputs: exclude
#     Comma-delimited list of "current", "minutely", "hourly", "daily" and "alerts"
#
def getLatLonWeather(lat, lon, apiKey, unit="imperial", exclude=""):
    assert unit in ["imperial", "metric", "standard"], "Invalid unit"
    
    url = "https://api.openweathermap.org/data/3.0/onecall?" + \
              "lat="      + str(lat) + \
              "&lon="     + str(lon) + \
              "&appid="   + apiKey + \
              "&units="   + unit + \
              "&exclude=" + exclude
    response = urequests.get(url)
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        return responseDict
    else:
        raise RuntimeError("OpenWeather API call error. Status code: " +
                           str(response.status_code) + response.text)

# Takes a cityName (str), US state code (str) and API key (str) to
#   call OpenWeatherMap API
# Returns JSON weather data (dict)
# 
def getUsWeather(cityName, stateCode, apiKey, unit="imperial", exclude=""):
    try:
        lat, lon = openweather_geocoding.getUsLatLon(cityName, stateCode, apiKey)
        return getLatLonWeather(lat, lon, apiKey, unit, exclude)
    except RuntimeError:
        raise        

# Takes a cityName (str), country code (str) and API key (str) to
#   call OpenWeatherMap API
# Returns JSON weather data (dict)
# 
def getIntlWeather(cityName, countryCode, apiKey, unit, exclude=""):
    try:
        lat, lon = openweather_geocoding.getIntlLatLon(cityName, countryCode, apiKey)
        return getLatLonWeather(lat, lon, apiKey, unit, exclude)
    except RuntimeError:
        raise        

# Takes a zip code (str), country code (str) and API key (str) to
#   call OpenWeatherMap API
# Returns JSON weather data (dict)
# 
def getZipWeather(zipCode, countryCode, apiKey, unit="imperial", exclude=""):
    try:
        lat, lon = openweather_geocoding.getZipLatLon(zipCode, countryCode, apiKey)
        return getLatLonWeather(lat, lon, apiKey, unit, exclude)
    except RuntimeError:
        raise        

# Takes downloaded JSON weather data (dict)
# Returns the current temp (float), feelsLike (float), humidity (float) as a tuple
#
def getCurrentTempHumidity(weatherDataDict):
    if "current" in weatherDataDict:
        return openweather_extractors.extractTempHumidity( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current UV Index (float)
#
def getCurrentUvi(weatherDataDict): 
    if "current" in weatherDataDict:
            return openweather_extractors.extractUvi( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current precip (float) in mm/hr. 
#
def getCurrentRain(weatherDataDict):
    if "current" in weatherDataDict:
        return openweather_extractors.extractRain( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current precip (float) in mm/hr. 
#
def getCurrentSnow(weatherDataDict): 
    if "current" in weatherDataDict:
        return openweather_extractors.extractSnow( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current wind speed (float, meters/miles per hr),
#   wind direction (float, degrees) and wind gust (float, meters/miles per hr)
#   as a tuple. 
#
def getCurrentWind(weatherDataDict): 
    if "current" in weatherDataDict:
        return openweather_extractors.extractWind( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current weather ID (int), condition main name (str), 
#   condition sub name (str) and icon ID (str) as a tuple. 
#
def getCurrentWeatherCondition(weatherDataDict):
    if "current" in weatherDataDict:
        return openweather_extractors.extractWeatherCond( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current atmospheric pressure on the sea level, hPa (float).
#
def getCurrentAtmosphericPressure(weatherDataDict):
    if "current" in weatherDataDict:
        return openweather_extractors.extractAtmosphericPressure( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the current cloud cover (%) as an int. 
#
def getCurrentCloudCover(weatherDataDict):
    if "current" in weatherDataDict:
        return openweather_extractors.extractCloudCover( weatherDataDict["current"] )
    else:
        raise RuntimeError("Current weather data not found.")

# Takes downloaded JSON weather data (dict)
# Returns the UV Index in the next hour (float)
#
def getUviNextHr(weatherDataDict):
    if "hourly" in weatherDataDict:
        return openweather_extractors.extractUvi( weatherDataDict["hourly"][0] )
    else:
        raise RuntimeError("Data not found for the next hour.")

# Takes downloaded JSON weather data (dict)
# Returns the prob of precip (float: [0,1]) for the next hour.
#
def getProbPrecipNextHr(weatherDataDict):
    if "hourly" in weatherDataDict:
        return openweather_extractors.extractProbPrecip( weatherDataDict["hourly"][0] )
    else:
        raise RuntimeError("Data not found for the next hour.")

# Takes downloaded JSON weather data (dict)
# Returns the precip (float) for the next hour (in mm/hr). 
#
def getRainNextHr(weatherDataDict):
    if "hourly" in weatherDataDict:
        return openweather_extractors.extractRain( weatherDataDict["hourly"][0] )
    else:
        raise RuntimeError("Data not found for the next hour.")

# Takes downloaded JSON weather data (dict)
# Returns the weather ID (int), condition main name (str), 
#   condition sub name (str) and icon ID (str) for the next hour as a tuple. 
#
def getWeatherConditionNextHr(weatherDataDict):
    if "hourly" in weatherDataDict:
        return openweather_extractors.extractWeatherCond( weatherDataDict["hourly"][0] )
    else:
        raise RuntimeError("Data not found for the next hour.")

if __name__ == "__main__":    
    apiKey = ""
    lat = 42.36
    lon = -71.01

    display = badger2040.Badger2040()
    # Connects to the wireless network. Make sure to complete WIFI_CONFIG.py.
    display.connect()

    weatherData = getLatLonWeather(lat, lon, apiKey, exclude="minutely,daily,alerts")

    print("Current temp, feels-like and humidity:", getCurrentTempHumidity(weatherData))
    print("Current UVI:",                  getCurrentUvi(weatherData))
    print("Current rain:",                 getCurrentRain(weatherData))
    print("Current snow:",                 getCurrentSnow(weatherData))
    print("Current wind:",                 getCurrentWind(weatherData))
    print("Current weather condition:",    getCurrentWeatherCondition(weatherData))
    print("Current atmospheric pressure:", getCurrentAtmosphericPressure(weatherData))
    print("Current cloud cover:",          getCurrentCloudCover(weatherData))

    print("Next hr UVI:",                getUviNextHr(weatherData))
    print("Next hr precip probability:", getProbPrecipNextHr(weatherData))
    print("Next hr rain:",               getRainNextHr(weatherData))    
    print("Next hr weather condition:",  getWeatherConditionNextHr(weatherData))
           
