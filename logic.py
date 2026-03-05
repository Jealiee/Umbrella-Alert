
def analyze_weather(weather_data):

    weather = weather_data["weather_code"]
    rain = weather_data["rain_sum"]
    snow = weather_data["snowfall_sum"]
    wind = weather_data["wind_speed_max"]
    temp_max = weather_data["temperature_max"]
    temp_min = weather_data["temperature_min"]
    apparent_max = weather_data["apparent_temperature_max"]
    apparent_min = weather_data["apparent_temperature_min"]
    uv = weather_data["uv_index_max"]
    avg_temp = (temp_min + temp_max)/2


    alerts =[]

    # rain and snow
    
    if rain >25:
        alerts.append("downpour expected")
    elif rain>10:
        alerts.append("heavy rain expected")
    elif rain>2 and rain<10:
        alerts.append("it's going to rain")
    elif snow > 1:
        alerts.append("Snowfall expected")
    
    # wind

    if wind>60:
        alerts.append("dangerour win expected")
    elif wind > 40:
        alerts.append("Strong wind expected")
    elif wind>20:
        alerts.append("It's going to be windy")

    


    # uv

    if uv>7:
        alerts.append("high uv exposure expected")
    elif uv>10:
        alerts.append("extreme uv exposure expected")

    # type of weather

    if weather<3:
        alerts.append("clear sky expected")
    elif weather>3 and weather<45:
        alerts.append("cloudy weather expected")
    if weather==45:
        alerts.append("fog expected")
    if weather == 95:
        alerts.append("thunderstorm expected")

    # temperature
    
    temperature = f"""
    Temperature today
    Min: {temp_min:.1f}°C
    Max: {temp_max:.1f}°C
    Average: {avg_temp:.1f}°C

    Feels like
    Min: {apparent_min:.1f}°C
    Max: {apparent_max:.1f}°C
    """
    alerts.append(temperature)
    
    final_message = "\n\n".join(alerts)

    return final_message




