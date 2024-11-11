import requests


def get_weather(town, api):
    # Use the OpenWeatherMap API to get current weather data.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={town},uk&APPID={api}&units=metric"
    try:
        response = requests.get(url)
    except:
        print("Error: Unable to obtain weather information. Check your internet connection and configuration settings.")
        return "0", "", ""

    if response.status_code == 200:
        data = response.json()["main"]
        wind = response.json()["wind"]
        weather = response.json()["weather"]
        temperature = round(int(data["temp"]))
        windspeed = wind["speed"]
        desc = weather[0]["description"]
        return temperature, desc, windspeed
    elif response.status_code == 401:  # Unauthorised - invalid API key
        return "1", "", ""
    else:
        return "0", "", ""
