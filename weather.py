import openmeteo_requests
import requests_cache
from retry_requests import retry


def get_weather(latitude: float, longitude: float):

    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "weather_code",
            "uv_index_max",
            "rain_sum",
            "snowfall_sum",
            "wind_speed_10m_max",
            "precipitation_sum",
            "wind_direction_10m_dominant",
        ],
        "timezone": "auto",
        "forecast_days": 1,
    }
    response = openmeteo.weather_api(url, params=params)[0]
    daily = response.Daily()

    weather_data = {
        "temperature_max": float(daily.Variables(0).ValuesAsNumpy()[0]),
        "temperature_min": float(daily.Variables(1).ValuesAsNumpy()[0]),
        "apparent_temperature_max": float(daily.Variables(2).ValuesAsNumpy()[0]),
        "apparent_temperature_min": float(daily.Variables(3).ValuesAsNumpy()[0]),
        "weather_code": int(daily.Variables(4).ValuesAsNumpy()[0]),
        "uv_index_max": float(daily.Variables(5).ValuesAsNumpy()[0]),
        "rain_sum": float(daily.Variables(6).ValuesAsNumpy()[0]),
        "snowfall_sum": float(daily.Variables(7).ValuesAsNumpy()[0]),
        "wind_speed_max": float(daily.Variables(8).ValuesAsNumpy()[0]),
        "precipitation_sum": float(daily.Variables(9).ValuesAsNumpy()[0]),
        "wind_direction_dominant": float(daily.Variables(10).ValuesAsNumpy()[0]),
    }

    return weather_data
