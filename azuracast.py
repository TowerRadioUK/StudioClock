from AzuracastPy import AzuracastClient
import tomli

try:
    with open("config.toml", mode="rb") as fp:
        config = tomli.load(fp)
except FileNotFoundError:
    print("config.toml not found.")
    exit()

client = AzuracastClient(
    radio_url=config["azuracast"]["radio_url"],
    x_api_key=config["azuracast"]["api_key"]
)

station = client.station(config["azuracast"]["station_id"])

def now_playing():
    np = client.now_playing(station.id).now_playing
    return np.song.title + " by " + np.song.artist

def is_autodj():
    return client.now_playing(station.id).now_playing.streamer == ''
