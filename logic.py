##def take_umrella(weather_data):
  ##  return weather_data["precipitation_sum"]

def analyze_weather(weather_data):

    probability = weather_data["precipitation_probability"]
    rain = weather_data["rain_sum"]
    snow = weather_data["snowfall_sum"]
    wind = weather_data["wind_speed_max"]

    alerts =[]

    if probability>50:
        alerts.append("high chance of rain")

    if rain>10:
        alerts.append("heavy rain expected")

    if snow > 1:
        alerts.append("Snowfall expected")

    if wind > 40:
        alerts.append("Strong wind expected")

    return alerts
