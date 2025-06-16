
# Takes a weather dataset (dict)
# Returns temp (float), feelsLike (float), humidity (float) as a tuple
#
def extractTempHumidity(wDataDict):
    try:
        temp      = wDataDict["temp"]
        feelsLike = wDataDict["feels_like"]
        humidity  = wDataDict["humidity"]
        return (float(temp), float(feelsLike), float(humidity))
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns a UV Index (float)
#
def extractUvi(wDataDict):
    try:
        return float(wDataDict["uvi"])
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns precip (float) in mm/hr
#
def extractRain(wDataDict):
    try:
        if "rain" in wDataDict:
            return float(currentDict["rain"]["1h"])
        else:
            return 0
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns precip (float) in mm/hr
#
def extractSnow(wDataDict):
    try:
        if "snow" in wDataDict:
            return float(currentDict["snow"]["1h"])
        else:
            return 0
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns wind speed (float, meters/miles per hr), wind direction (float, degrees),
#   and wind gust (float, meters/miles per hr) as a tuple
#
def extractWind(wDataDict):
    try:
        windSpeed = wDataDict["wind_speed"]
        windDeg   = wDataDict["wind_deg"]
        windGust  = wDataDict["wind_gust"]
        return (float(windSpeed), float(windDeg), float(windGust))
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns weather ID (int), condition main name (str), 
#   condition sub name (str) and icon ID (str) as a tuple. 
#
def extractWeatherCond(wDataDict):
    try:
        weatherCondDict = wDataDict["weather"][0]
        id     = weatherCondDict["id"]
        main   = weatherCondDict["main"]
        desc   = weatherCondDict["description"]
        iconId = weatherCondDict["icon"]
        return (int(id), main, desc, iconId)
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns atmospheric pressure on the sea level, hPa (float).
#
def extractAtmosphericPressure(wDataDict):
    try:
        return float(wDataDict["pressure"])
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns cloud cover (%) as an int.
#
def extractCloudCover(wDataDict):
    try:
        return int(wDataDict["clouds"])
    except Exception:
        raise

# Takes a weather dataset (dict)
# Returns prob of precip (float: [0,1]).
#
def extractProbPrecip(wDataDict):
    try:
        return float(wDataDict["pop"])
    except Exception:
        raise


