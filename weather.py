import requests

def get_coordinates(postcode):
    # Use an API to convert postcode to latitude and longitude
    url = f"https://nominatim.openstreetmap.org/search?postalcode={postcode}&country=UK&format=json"
    response = requests.get(url)
    
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    else:
        raise ValueError("Unable to fetch coordinates. Check the postcode.")

def get_weather(lat, lon):
    # Use Open-Meteo API to get current weather data
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()['current_weather']
        temperature = data['temperature']
        windspeed = data['windspeed']
        weather_code = data['weathercode']
        return temperature, weather_code, windspeed
    else:
        raise ValueError("Unable to fetch weather data.")

def weather_description(weather_code):
    # Mapping weather codes to descriptions
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light",
        53: "Drizzle: Moderate",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight",
        63: "Rain: Moderate",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight",
        73: "Snow fall: Moderate",
        75: "Snow fall: Heavy intensity",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers slight",
        86: "Snow showers heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(weather_code, "Unknown weather condition")

def main():
    postcode = input("Enter the UK postcode: ")
    try:
        lat, lon = get_coordinates(postcode)
        print(f"Coordinates: {lat}, {lon}")
        temperature, weather_code, windspeed = get_weather(lat, lon)
        description = weather_description(weather_code)
        print(f"{temperature}°C, {description} with windspeed {windspeed} km/h")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
