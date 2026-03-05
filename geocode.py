import requests

def get_coordinates(city_name):
    url="https://nominatim.openstreetmap.org/search"
    parameters = {"q":city_name, "format": "json", "limit":1}

    response=requests.get(url, params=parameters)
    data=response.json()

    if not data:
        return None, None
    
    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])
    return latitude, longitude
