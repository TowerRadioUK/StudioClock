import requests


def get_weather(town, api):
    # Use the OpenWeatherMap API to get current weather data.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={town},uk&APPID={api}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["main"]
        wind = response.json()["wind"]
        weather = response.json()["weather"]
        temperature = round(int(data["temp"]))
        windspeed = wind["speed"]
        desc = weather[0]["description"]
        return temperature, desc, windspeed
    elif response.status_code == 401:  # Unauthorised - invalid API key
        raise ValueError("Invalid API key")
    else:
        raise ValueError("Unable to fetch weather data.")
