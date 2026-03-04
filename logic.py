##def take_umrella(weather_data):
  ##  return weather_data["precipitation_sum"]

def analyze_weather(weather_data):

    probability = weather_data["precipitation_probability"]
    rain = weather_data["rain_sum"]
    snow = weather_data["snowfall_sum"]
    wind = weather_data["wind_speed_max"]

    if snow > 1:
        return snow_alert

    if rain > 10 and wind > 50:
        return storm_alert

    if probability >= 40 and rain >= 1:
        return umbrella_alert

    return no_alert
