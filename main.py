from weather import get_weather

if __name__ == '__main__':
    print("Umbrella Alert loading...")
    
    weather_data = get_weather(43.71,10.39)
    
    print(weather_data)
