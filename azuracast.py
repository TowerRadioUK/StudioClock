from AzuracastPy import AzuracastClient
import tomli

try:
    with open("config.toml", mode="rb") as fp:
        config = tomli.load(fp)
except FileNotFoundError:
    print("config.toml not found.")
    exit()

client = AzuracastClient(
    radio_url=config["azuracast"]["radio_url"], x_api_key=config["azuracast"]["api_key"]
)

try:
    station = client.station(config["azuracast"]["station_id"])
except:
    print("Error: Unable to obtain station information. Check your internet connection and configuration settings.")


def get_now_playing():
    try:
        np = client.now_playing(station.id).now_playing
        return np.song.title + " by " + np.song.artist
    except:
        return "No song playing."


def get_streamer():
    try:
        return client.now_playing(station.id).now_playing.streamer
    except:
        return "FAULT"
